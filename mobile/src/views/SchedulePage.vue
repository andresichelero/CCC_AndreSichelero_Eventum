<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Calendário</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="viewMode = viewMode === 'list' ? 'calendar' : 'list'">
            <ion-icon :icon="viewMode === 'list' ? calendarOutline : listOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else>
        <!-- Calendar View -->
        <div v-if="viewMode === 'calendar'">
          <div class="calendar-header ion-padding">
            <ion-button fill="clear" @click="prevMonth">
              <ion-icon :icon="chevronBackOutline"></ion-icon>
            </ion-button>
            <h2>{{ currentMonthName }} {{ currentYear }}</h2>
            <ion-button fill="clear" @click="nextMonth">
              <ion-icon :icon="chevronForwardOutline"></ion-icon>
            </ion-button>
          </div>

          <div class="calendar-grid">
            <div class="weekday" v-for="day in weekDays" :key="day">{{ day }}</div>
            <div 
              v-for="(day, index) in calendarDays" 
              :key="index" 
              class="day-cell"
              :class="{ 
                'current-month': day.isCurrentMonth, 
                'today': isToday(day.date),
                'has-events': day.events.length > 0,
                'selected': isSelected(day.date)
              }"
              @click="selectDate(day.date)"
            >
              <span class="day-number">{{ day.day }}</span>
              <div class="event-dots">
                <span v-for="evt in day.events.slice(0, 3)" :key="evt.id" class="dot" :class="evt.type"></span>
              </div>
            </div>
          </div>

          <div class="selected-date-events ion-padding" v-if="selectedDateEvents.length > 0">
            <h3>Eventos em {{ formatDate(selectedDate) }}</h3>
            <ion-list>
              <ion-item v-for="item in selectedDateEvents" :key="item.id" button @click="goToEvent(item)">
                <ion-label>
                  <h2>{{ item.title }}</h2>
                  <p>{{ formatTime(item.start) }} - {{ formatTime(item.end) }}</p>
                  <ion-badge :color="item.type === 'event' ? 'primary' : 'warning'">
                    {{ item.type === 'event' ? 'Evento' : 'Atividade' }}
                  </ion-badge>
                </ion-label>
              </ion-item>
            </ion-list>
          </div>
          <div class="ion-padding ion-text-center" v-else-if="selectedDate">
            <p>Nenhum evento nesta data.</p>
          </div>
        </div>

        <!-- List View (Existing) -->
        <ion-list v-else>
          <ion-item-group v-for="(activities, date) in groupedSchedule" :key="String(date)">
            <ion-item-divider sticky>
              <ion-label>{{ formatDate(String(date)) }}</ion-label>
            </ion-item-divider>
            
            <div v-for="activity in activities" :key="activity.id">
              <ActivityItem :activity="activity" />
            </div>
          </ion-item-group>
          
          <div v-if="Object.keys(groupedSchedule).length === 0" class="ion-text-center ion-padding">
            <p>Nenhuma atividade programada.</p>
          </div>
        </ion-list>
      </div>

      <ion-fab vertical="bottom" horizontal="end" slot="fixed">
        <ion-fab-button @click="openCheckinModal">
          <ion-icon :icon="qrCodeOutline"></ion-icon>
        </ion-fab-button>
      </ion-fab>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonSpinner, 
  IonItemGroup, IonItemDivider, IonLabel, IonFab, IonFabButton, IonIcon, 
  IonButtons, IonButton, IonItem, IonBadge,
  alertController, toastController 
} from '@ionic/vue';
import { qrCodeOutline, calendarOutline, listOutline, chevronBackOutline, chevronForwardOutline } from 'ionicons/icons';
import api from '@/services/api';
import ActivityItem from '@/components/ActivityItem.vue';

const router = useRouter();
const schedule = ref<any[]>([]);
const loading = ref(true);
const viewMode = ref('list'); // 'list' or 'calendar'

// Calendar Logic
const currentDate = ref(new Date());
const selectedDate = ref(new Date());
const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];

const currentMonthName = computed(() => {
  return currentDate.value.toLocaleDateString('pt-BR', { month: 'long' });
});

const currentYear = computed(() => {
  return currentDate.value.getFullYear();
});

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  
  const firstDayOfMonth = new Date(year, month, 1);
  const lastDayOfMonth = new Date(year, month + 1, 0);
  
  const daysInMonth = lastDayOfMonth.getDate();
  const startingDayOfWeek = firstDayOfMonth.getDay(); // 0 = Sunday
  
  const days = [];
  
  // Previous month days
  const prevMonthLastDay = new Date(year, month, 0).getDate();
  for (let i = startingDayOfWeek - 1; i >= 0; i--) {
    const day = prevMonthLastDay - i;
    const date = new Date(year, month - 1, day);
    days.push({ day, date, isCurrentMonth: false, events: getEventsForDate(date) });
  }
  
  // Current month days
  for (let i = 1; i <= daysInMonth; i++) {
    const date = new Date(year, month, i);
    days.push({ day: i, date, isCurrentMonth: true, events: getEventsForDate(date) });
  }
  
  // Next month days to fill grid (6 rows * 7 days = 42)
  const remainingDays = 42 - days.length;
  for (let i = 1; i <= remainingDays; i++) {
    const date = new Date(year, month + 1, i);
    days.push({ day: i, date, isCurrentMonth: false, events: getEventsForDate(date) });
  }
  
  return days;
});

const selectedDateEvents = computed(() => {
  return getEventsForDate(selectedDate.value);
});

const getEventsForDate = (date: Date) => {
  const dateStr = date.toISOString().split('T')[0];
  return schedule.value.filter(item => {
    if (!item.start) return false;
    return item.start.startsWith(dateStr);
  }).sort((a, b) => new Date(a.start).getTime() - new Date(b.start).getTime());
};

const prevMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1);
};

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1);
};

const selectDate = (date: Date) => {
  selectedDate.value = date;
  // If selected date is not in current month view, switch view
  if (date.getMonth() !== currentDate.value.getMonth()) {
    currentDate.value = new Date(date.getFullYear(), date.getMonth(), 1);
  }
};

const isToday = (date: Date) => {
  const today = new Date();
  return date.getDate() === today.getDate() && 
         date.getMonth() === today.getMonth() && 
         date.getFullYear() === today.getFullYear();
};

const isSelected = (date: Date) => {
  return date.getDate() === selectedDate.value.getDate() && 
         date.getMonth() === selectedDate.value.getMonth() && 
         date.getFullYear() === selectedDate.value.getFullYear();
};

const formatTime = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
};

const goToEvent = (item: any) => {
  if (item.type === 'event') {
    const id = item.id.toString().includes('_') ? item.id.split('_')[1] : item.id;
    router.push(`/tabs/events/${id}`);
  } else {
    if (item.event_id) {
      router.push(`/tabs/events/${item.event_id}`);
    } else {
      router.push('/tabs/events');
    }
  }
};

// Existing Logic
const fetchSchedule = async () => {
  try {
    const response = await api.get('/api/calendar');
    schedule.value = response.data.calendar_items;
  } catch (error) {
    console.error('Error fetching schedule', error);
    const toast = await toastController.create({
      message: 'Erro ao carregar programação.',
      duration: 3000,
      color: 'danger'
    });
    await toast.present();
  } finally {
    loading.value = false;
  }
};

const groupedSchedule = computed(() => {
  const groups: Record<string, any[]> = {};
  schedule.value.forEach(item => {
    const date = item.start ? item.start.split('T')[0] : '';
    if (date) {
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push(item);
    }
  });
  
  return Object.keys(groups).sort().reduce(
    (obj: any, key) => { 
      obj[key] = groups[key].sort((a: any, b: any) => new Date(a.start).getTime() - new Date(b.start).getTime()); 
      return obj;
    }, 
    {}
  );
});

const formatDate = (dateString: string | Date) => {
  if (!dateString) return '';
  const date = typeof dateString === 'string' ? new Date(dateString + (dateString.includes('T') ? '' : 'T00:00:00')) : dateString;
  return date.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' });
};

const openCheckinModal = async () => {
  const alert = await alertController.create({
    header: 'Realizar Check-in',
    message: 'Digite o código da atividade para confirmar sua presença.',
    inputs: [
      {
        name: 'code',
        type: 'text',
        placeholder: 'Código (ex: 12345)'
      }
    ],
    buttons: [
      {
        text: 'Cancelar',
        role: 'cancel'
      },
      {
        text: 'Confirmar',
        handler: async (data) => {
          if (data.code) {
            await performCheckin(data.code);
          }
        }
      }
    ]
  });

  await alert.present();
};

const performCheckin = async (code: string) => {
  try {
    await api.post('/api/checkin', { code });
    
    const toast = await toastController.create({
      message: 'Check-in realizado com sucesso!',
      duration: 2000,
      color: 'success'
    });
    await toast.present();
    
    fetchSchedule();
    
  } catch (error: any) {
    console.error('Check-in failed', error);
    const toast = await toastController.create({
      message: error.response?.data?.error || 'Código inválido ou erro ao realizar check-in.',
      duration: 2000,
      color: 'danger'
    });
    await toast.present();
  }
};

onMounted(() => {
  fetchSchedule();
});
</script>

<style scoped>
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calendar-header h2 {
  font-size: 1.2rem;
  font-weight: bold;
  text-transform: capitalize;
  margin: 0;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background-color: #e0e0e0;
  border: 1px solid #e0e0e0;
}

.weekday {
  background-color: #f5f5f5;
  text-align: center;
  padding: 5px;
  font-weight: bold;
  font-size: 0.8rem;
}

.day-cell {
  background-color: white;
  min-height: 60px;
  padding: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.day-cell.current-month {
  color: black;
}

.day-cell:not(.current-month) {
  color: #ccc;
  background-color: #fafafa;
}

.day-cell.today {
  background-color: #e3f2fd;
  font-weight: bold;
}

.day-cell.selected {
  border: 2px solid var(--ion-color-primary);
}

.day-number {
  font-size: 0.9rem;
}

.event-dots {
  display: flex;
  gap: 2px;
  margin-top: 2px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.dot.event {
  background-color: var(--ion-color-primary);
}

.dot.activity {
  background-color: var(--ion-color-warning);
}
</style>
