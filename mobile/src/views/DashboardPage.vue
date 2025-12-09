<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Início</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else class="ion-padding">
        <!-- Welcome Card -->
        <ion-card color="primary">
          <ion-card-header>
            <ion-card-subtitle>Bem-vindo(a)</ion-card-subtitle>
            <ion-card-title>{{ user?.name }}</ion-card-title>
          </ion-card-header>
          <ion-card-content>
            O que você deseja fazer hoje?
          </ion-card-content>
        </ion-card>

        <!-- Quick Actions -->
        <h3 class="ion-margin-top">Ações Rápidas</h3>
        <ion-grid>
          <ion-row>
            <ion-col size="6">
              <ion-button expand="block" router-link="/tabs/events" color="light">
                <ion-icon slot="start" :icon="calendarOutline"></ion-icon>
                Eventos
              </ion-button>
            </ion-col>
            <ion-col size="6" v-if="user?.role === 1">
              <ion-button expand="block" router-link="/events/create" color="secondary">
                <ion-icon slot="start" :icon="addCircleOutline"></ion-icon>
                Criar
              </ion-button>
            </ion-col>
            <ion-col size="6" v-if="user?.role === 1">
              <ion-button expand="block" router-link="/manage-turmas" color="tertiary">
                <ion-icon slot="start" :icon="schoolOutline"></ion-icon>
                Turmas
              </ion-button>
            </ion-col>
            <ion-col size="6">
              <ion-button expand="block" router-link="/tabs/schedule" color="light">
                <ion-icon slot="start" :icon="timeOutline"></ion-icon>
                Agenda
              </ion-button>
            </ion-col>
          </ion-row>
        </ion-grid>

        <!-- My Inscriptions Preview -->
        <div v-if="inscriptions.length > 0">
          <div class="section-header">
            <h3>Minhas Inscrições</h3>
            <ion-button fill="clear" size="small" router-link="/tabs/inscriptions">Ver todas</ion-button>
          </div>
          <ion-list>
            <ion-item v-for="inscription in inscriptions.slice(0, 3)" :key="inscription.id" button :router-link="`/tabs/events/${inscription.event_id}`">
              <ion-label>
                <h2>{{ inscription.event_title }}</h2>
                <p>{{ formatDate(inscription.event_start_date) }}</p>
              </ion-label>
            </ion-item>
          </ion-list>
        </div>

        <!-- Organized Events Preview -->
        <div v-if="user?.role === 1 && organizedEvents.length > 0">
          <div class="section-header">
            <h3>Meus Eventos</h3>
            <ion-button fill="clear" size="small" router-link="/my-organized-events">Ver todos</ion-button>
          </div>
          <ion-list>
            <ion-item v-for="event in organizedEvents.slice(0, 3)" :key="event.id" button :router-link="`/tabs/events/${event.id}`">
              <ion-label>
                <h2>{{ event.title }}</h2>
                <p>{{ formatDate(event.start_date) }}</p>
                <ion-badge :color="event.status === 1 ? 'warning' : 'success'">
                  {{ event.status === 1 ? 'Rascunho' : 'Publicado' }}
                </ion-badge>
              </ion-label>
            </ion-item>
          </ion-list>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, 
  IonCardSubtitle, IonCardTitle, IonCardContent, IonGrid, IonRow, IonCol, 
  IonButton, IonIcon, IonList, IonItem, IonLabel, IonBadge, IonSpinner
} from '@ionic/vue';
import { calendarOutline, addCircleOutline, schoolOutline, timeOutline } from 'ionicons/icons';
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';

const authStore = useAuthStore();
const user = computed(() => authStore.user);
const loading = ref(true);
const inscriptions = ref<any[]>([]);
const organizedEvents = ref<any[]>([]);

const fetchData = async () => {
  loading.value = true;
  try {
    // Fetch inscriptions
    const inscResponse = await api.get('/api/my-inscriptions');
    inscriptions.value = inscResponse.data.events;

    // Fetch organized events if organizer
    if (user.value?.role === 1) {
      const orgResponse = await api.get('/api/my-organized-events');
      organizedEvents.value = orgResponse.data.events;
    }
  } catch (error) {
    console.error('Error fetching dashboard data', error);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.section-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: bold;
}
</style>
