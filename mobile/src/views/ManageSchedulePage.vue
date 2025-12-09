<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/events"></ion-back-button>
        </ion-buttons>
        <ion-title>Gerenciar Programação</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else>
        <div class="ion-text-center ion-margin-bottom">
          <h2>{{ event.title }}</h2>
          <p>{{ formatDate(event.start_date) }} - {{ formatDate(event.end_date) }}</p>
        </div>

        <ion-segment v-model="segment" class="ion-margin-bottom">
          <ion-segment-button value="activities">
            <ion-label>Atividades</ion-label>
          </ion-segment-button>
          <ion-segment-button value="checkin">
            <ion-label>Check-in</ion-label>
          </ion-segment-button>
        </ion-segment>

        <div v-if="segment === 'activities'">
          <ion-card>
            <ion-card-header>
              <ion-card-title>{{ editing ? 'Editar Atividade' : 'Nova Atividade' }}</ion-card-title>
            </ion-card-header>
            <ion-card-content>
              <form @submit.prevent="saveActivity">
                <ion-item>
                  <ion-label position="floating">Título</ion-label>
                  <ion-input v-model="form.title" required></ion-input>
                </ion-item>
                <ion-item>
                  <ion-label position="floating">Descrição</ion-label>
                  <ion-textarea v-model="form.description" :rows="2"></ion-textarea>
                </ion-item>
                <ion-item>
                  <ion-label position="stacked">Início</ion-label>
                  <ion-input v-model="form.start_time" type="datetime-local" required></ion-input>
                </ion-item>
                <ion-item>
                  <ion-label position="stacked">Fim</ion-label>
                  <ion-input v-model="form.end_time" type="datetime-local" required></ion-input>
                </ion-item>
                <ion-item>
                  <ion-label position="floating">Local</ion-label>
                  <ion-input v-model="form.location" required></ion-input>
                </ion-item>
                
                <div class="ion-padding-top">
                  <ion-button expand="block" type="submit">
                    {{ editing ? 'Salvar Alterações' : 'Adicionar Atividade' }}
                  </ion-button>
                  <ion-button v-if="editing" expand="block" color="medium" fill="outline" @click="cancelEdit" class="ion-margin-top">
                    Cancelar
                  </ion-button>
                  <ion-button v-if="editing" expand="block" color="danger" fill="outline" @click="deleteActivity" class="ion-margin-top">
                    Remover
                  </ion-button>
                </div>
              </form>
            </ion-card-content>
          </ion-card>

          <ion-list class="ion-margin-top">
            <ion-list-header>
              <ion-label>Programação Atual</ion-label>
            </ion-list-header>
            <ion-item v-for="activity in activities" :key="activity.id" button @click="editActivity(activity)">
              <ion-label>
                <h2>{{ activity.title }}</h2>
                <p>{{ formatDate(activity.start_time) }} - {{ formatDate(activity.end_time) }}</p>
                <p>{{ activity.location }}</p>
              </ion-label>
            </ion-item>
            <ion-item v-if="activities.length === 0">
              <ion-label class="ion-text-center">Nenhuma atividade cadastrada.</ion-label>
            </ion-item>
          </ion-list>
        </div>

        <div v-if="segment === 'checkin'">
          <ion-list>
            <ion-item v-for="activity in activities" :key="activity.id">
              <ion-label class="ion-text-wrap">
                <h2>{{ activity.title }}</h2>
                <p>{{ formatDate(activity.start_time) }}</p>
                
                <div v-if="activity.check_in_open" class="ion-margin-top ion-text-center">
                  <h1 class="checkin-code">{{ activity.check_in_code }}</h1>
                  <p>Código de Check-in Ativo</p>
                  <ion-button color="warning" expand="block" @click="closeCheckin(activity.id)">
                    Encerrar Check-in
                  </ion-button>
                </div>
                
                <div v-else class="ion-margin-top">
                  <ion-button color="success" expand="block" @click="openCheckin(activity.id)">
                    Abrir Check-in
                  </ion-button>
                </div>
                
                <p class="ion-margin-top">Participantes: {{ activity.attendees_count || 0 }}</p>
              </ion-label>
            </ion-item>
            <ion-item v-if="activities.length === 0">
              <ion-label class="ion-text-center">Nenhuma atividade para gerenciar check-in.</ion-label>
            </ion-item>
          </ion-list>
        </div>

      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, 
  IonButtons, IonBackButton, IonSpinner, IonSegment, IonSegmentButton,
  IonLabel, IonCard, IonCardHeader, IonCardTitle, IonCardContent,
  IonItem, IonInput, IonTextarea, IonButton, IonList, IonListHeader,
  alertController, toastController
} from '@ionic/vue';
import api from '@/services/api';
import { formatDate } from '@/utils/formatters';

const route = useRoute();
const eventId = route.params.id;

const event = ref<any>({});
const activities = ref<any[]>([]);
const loading = ref(true);
const segment = ref('activities');
const editing = ref(false);
const editingId = ref<number | null>(null);

const form = reactive({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: ''
});

const loadData = async () => {
  loading.value = true;
  try {
    const response = await api.get(`/api/events/${eventId}`);
    event.value = response.data.event;
    activities.value = response.data.activities || [];
  } catch (error) {
    console.error('Erro ao carregar dados', error);
  } finally {
    loading.value = false;
  }
};

const formatDateForInput = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '';
  const pad = (n: number) => n < 10 ? '0' + n : n;
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
};

const editActivity = (activity: any) => {
  editing.value = true;
  editingId.value = activity.id;
  form.title = activity.title;
  form.description = activity.description;
  form.start_time = formatDateForInput(activity.start_time);
  form.end_time = formatDateForInput(activity.end_time);
  form.location = activity.location;
  
  // Scroll to top to see form
  const content = document.querySelector('ion-content');
  content?.scrollToTop(500);
};

const cancelEdit = () => {
  editing.value = false;
  editingId.value = null;
  form.title = '';
  form.description = '';
  form.start_time = '';
  form.end_time = '';
  form.location = '';
};

const saveActivity = async () => {
  try {
    if (editing.value && editingId.value) {
      await api.put(`/api/activities/${editingId.value}`, { ...form, event_id: eventId });
    } else {
      await api.post(`/api/events/${eventId}/activities`, form);
    }
    
    const toast = await toastController.create({
      message: editing.value ? 'Atividade atualizada!' : 'Atividade criada!',
      duration: 2000,
      color: 'success'
    });
    await toast.present();
    
    cancelEdit();
    // Reload activities without full page reload
    const response = await api.get(`/api/events/${eventId}`);
    activities.value = response.data.activities || [];
    
  } catch (error: any) {
    const toast = await toastController.create({
      message: error.response?.data?.error || 'Erro ao salvar atividade.',
      duration: 2000,
      color: 'danger'
    });
    await toast.present();
  }
};

const deleteActivity = async () => {
  const alert = await alertController.create({
    header: 'Confirmar Exclusão',
    message: 'Tem certeza que deseja remover esta atividade?',
    buttons: [
      { text: 'Cancelar', role: 'cancel' },
      {
        text: 'Remover',
        role: 'destructive',
        handler: async () => {
          try {
            if (editingId.value) {
              await api.delete(`/api/activities/${editingId.value}`);
              const toast = await toastController.create({
                message: 'Atividade removida!',
                duration: 2000,
                color: 'success'
              });
              await toast.present();
              cancelEdit();
              const response = await api.get(`/api/events/${eventId}`);
              activities.value = response.data.activities || [];
            }
          } catch (error) {
            console.error(error);
          }
        }
      }
    ]
  });
  await alert.present();
};

const openCheckin = async (activityId: number) => {
  try {
    await api.post(`/api/activities/${activityId}/open-checkin`);
    // Reload to get code
    const response = await api.get(`/api/events/${eventId}`);
    activities.value = response.data.activities || [];
  } catch (error: any) {
    const toast = await toastController.create({
      message: error.response?.data?.error || 'Erro ao abrir check-in.',
      duration: 2000,
      color: 'danger'
    });
    await toast.present();
  }
};

const closeCheckin = async (activityId: number) => {
  try {
    await api.post(`/api/activities/${activityId}/close-checkin`);
    // Reload
    const response = await api.get(`/api/events/${eventId}`);
    activities.value = response.data.activities || [];
  } catch (error: any) {
    const toast = await toastController.create({
      message: error.response?.data?.error || 'Erro ao fechar check-in.',
      duration: 2000,
      color: 'danger'
    });
    await toast.present();
  }
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.checkin-code {
  font-size: 3rem;
  font-weight: bold;
  letter-spacing: 5px;
  color: var(--ion-color-primary);
  margin: 10px 0;
}
</style>
