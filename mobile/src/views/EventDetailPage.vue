<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/events"></ion-back-button>
        </ion-buttons>
        <ion-title>Detalhes do Evento</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding">
      <ion-refresher slot="fixed" @ionRefresh="handleRefresh($event)">
        <ion-refresher-content></ion-refresher-content>
      </ion-refresher>

      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else-if="event">
        <img v-if="event.image_url" :src="event.image_url" alt="Event Image" class="event-image"/>
        <div v-else class="placeholder-image">
          <ion-icon :icon="imageOutline" class="placeholder-icon"></ion-icon>
        </div>
        
        <h1 class="ion-margin-top">{{ event.title }}</h1>
        
        <ion-item lines="none" class="ion-no-padding" v-if="event.organizer">
          <ion-icon :icon="personOutline" slot="start"></ion-icon>
          <ion-label>
            <h2>Organizador</h2>
            <p>{{ event.organizer.name }}</p>
          </ion-label>
        </ion-item>

        <ion-item lines="none" class="ion-no-padding">
          <ion-icon :icon="calendarOutline" slot="start"></ion-icon>
          <ion-label>
            <h2>Data</h2>
            <p>{{ formatDate(event.start_date) }} - {{ formatDate(event.end_date) }}</p>
          </ion-label>
        </ion-item>

        <ion-item lines="none" class="ion-no-padding" v-if="event.inscription_start_date">
          <ion-icon :icon="timeOutline" slot="start"></ion-icon>
          <ion-label>
            <h2>Inscrições</h2>
            <p>{{ formatDate(event.inscription_start_date) }} até {{ formatDate(event.inscription_end_date) }}</p>
          </ion-label>
        </ion-item>

        <ion-item lines="none" class="ion-no-padding" v-if="event.submission_start_date">
          <ion-icon :icon="documentTextOutline" slot="start"></ion-icon>
          <ion-label>
            <h2>Submissões</h2>
            <p>{{ formatDate(event.submission_start_date) }} até {{ formatDate(event.submission_end_date) }}</p>
          </ion-label>
        </ion-item>

        <div class="description ion-margin-top">
          <h3>Sobre o evento</h3>
          <p>{{ event.description }}</p>
        </div>

        <div v-if="authStore.user && event.organizer_id === authStore.user.id" class="organizer-actions ion-padding-top">
          <h3>Ações do Organizador</h3>
          <ion-button expand="block" fill="outline" :router-link="`/events/${event.id}/edit`">
            <ion-icon :icon="createOutline" slot="start"></ion-icon>
            Editar Evento
          </ion-button>
          <ion-button expand="block" color="danger" fill="outline" @click="deleteEvent" class="ion-margin-top">
            <ion-icon :icon="trashOutline" slot="start"></ion-icon>
            Remover Evento
          </ion-button>
        </div>

        <div v-if="isInscribed && isSubmissionOpen" class="submission-actions ion-padding-top">
          <ion-button expand="block" :router-link="`/events/${event.id}/submit`">
            <ion-icon :icon="cloudUploadOutline" slot="start"></ion-icon>
            Submeter Trabalho
          </ion-button>
        </div>

        <div v-if="activities.length > 0" class="activities-section ion-margin-top">
          <h3>Programação</h3>
          <ion-list>
            <div v-for="activity in activities" :key="activity.id">
              <ActivityItem :activity="activity" />
            </div>
          </ion-list>
        </div>

        <div class="ion-padding-top ion-margin-bottom">
          <ion-button 
            v-if="!isInscribed"
            expand="block" 
            @click="inscribe" 
            :disabled="inscribing || !isInscriptionOpen">
            {{ inscribing ? 'Inscrevendo...' : (isInscriptionOpen ? 'Inscrever-se' : 'Inscrições Fechadas') }}
          </ion-button>

          <ion-button 
            v-else
            expand="block" 
            color="danger"
            fill="outline"
            @click="unsubscribe" 
            :disabled="inscribing">
            {{ inscribing ? 'Processando...' : 'Cancelar Inscrição' }}
          </ion-button>

          <ion-button 
            v-if="isInscribed"
            expand="block" 
            color="tertiary"
            fill="outline"
            @click="handleCheckin" 
            class="ion-margin-top">
            <ion-icon :icon="checkmarkCircleOutline" slot="start"></ion-icon>
            Fazer Check-in
          </ion-button>

          <ion-button 
            v-if="isInscribed && isEventFinished"
            expand="block" 
            color="primary"
            fill="outline"
            @click="downloadCertificate" 
            class="ion-margin-top">
            <ion-icon :icon="ribbonOutline" slot="start"></ion-icon>
            Baixar Certificado
          </ion-button>
        </div>
      </div>
      
      <div v-else class="ion-text-center ion-padding">
        <p>Evento não encontrado.</p>
        <ion-button router-link="/tabs/events" fill="outline">Voltar</ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonBackButton, IonSpinner, IonButton, IonItem, IonLabel, IonIcon, toastController, IonList, alertController, IonRefresher, IonRefresherContent } from '@ionic/vue';
import { calendarOutline, imageOutline, personOutline, timeOutline, documentTextOutline, createOutline, trashOutline, cloudUploadOutline, checkmarkCircleOutline, ribbonOutline } from 'ionicons/icons';
import api from '@/services/api';
import { formatDate } from '@/utils/formatters';
import ActivityItem from '@/components/ActivityItem.vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const event = ref<any>(null);
const activities = ref<any[]>([]);
const loading = ref(true);
const inscribing = ref(false);
const isInscribed = ref(false);
const isInscriptionOpen = ref(false);
const isSubmissionOpen = ref(false);

const isEventFinished = computed(() => {
  if (!event.value) return false;
  return new Date(event.value.end_date) < new Date();
});

const handleRefresh = async (event: any) => {
  await fetchEventDetails();
  event.target.complete();
};

const fetchEventDetails = async () => {
  const id = route.params.id;
  try {
    const response = await api.get(`/api/events/${id}`);
    event.value = response.data.event;
    activities.value = response.data.activities || [];
    isInscriptionOpen.value = response.data.is_inscription_open;
    isSubmissionOpen.value = response.data.is_submission_open;
    
    checkIfInscribed(id);
    
  } catch (error) {
    console.error('Error fetching event details', error);
  } finally {
    loading.value = false;
  }
};

const checkIfInscribed = async (eventId: string | string[]) => {
  try {
    const response = await api.get('/api/my-inscriptions');
    const myInscriptions = response.data.events || [];
    const found = myInscriptions.find((e: any) => e.id == eventId);
    isInscribed.value = !!found;
  } catch (error) {
    console.error('Error checking inscription status', error);
  }
};

const inscribe = async () => {
  if (!event.value) return;
  
  inscribing.value = true;
  try {
    await api.post(`/api/events/${event.value.id}/inscribe`);
    isInscribed.value = true;
    
    const toast = await toastController.create({
      message: 'Inscrição realizada com sucesso!',
      duration: 2000,
      color: 'success',
      position: 'bottom'
    });
    await toast.present();
  } catch (error: any) {
    console.error('Error inscribing', error);
    const toast = await toastController.create({
      message: error.response?.data?.error || 'Erro ao realizar inscrição.',
      duration: 3000,
      color: 'danger',
      position: 'bottom'
    });
    await toast.present();
  } finally {
    inscribing.value = false;
  }
};

const unsubscribe = async () => {
  if (!event.value) return;
  
  inscribing.value = true;
  try {
    await api.delete(`/api/events/${event.value.id}/inscribe`);
    isInscribed.value = false;
    
    const toast = await toastController.create({
      message: 'Inscrição cancelada com sucesso!',
      duration: 2000,
      color: 'success',
      position: 'bottom'
    });
    await toast.present();
    
    await fetchEventDetails();
  } catch (error: any) {
    console.error('Error unsubscribing', error);
    const toast = await toastController.create({
      message: error.response?.data?.error || 'Erro ao cancelar inscrição.',
      duration: 3000,
      color: 'danger',
      position: 'bottom'
    });
    await toast.present();
  } finally {
    inscribing.value = false;
  }
};

const deleteEvent = async () => {
  const alert = await alertController.create({
    header: 'Confirmar Exclusão',
    message: 'Tem certeza que deseja remover este evento? Esta ação não pode ser desfeita.',
    buttons: [
      {
        text: 'Cancelar',
        role: 'cancel'
      },
      {
        text: 'Remover',
        role: 'destructive',
        handler: async () => {
          try {
            await api.delete(`/api/events/${event.value.id}`);
            const toast = await toastController.create({
              message: 'Evento removido com sucesso',
              duration: 2000,
              color: 'success'
            });
            await toast.present();
            router.replace('/tabs/events');
          } catch (error) {
            const toast = await toastController.create({
              message: 'Erro ao remover evento',
              duration: 2000,
              color: 'danger'
            });
            await toast.present();
          }
        }
      }
    ]
  });
  await alert.present();
};

const handleCheckin = async () => {
  const alert = await alertController.create({
    header: 'Check-in',
    inputs: [
      {
        name: 'code',
        type: 'text',
        placeholder: 'Código de Check-in'
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
          try {
            await api.post('/api/checkin', { code: data.code });
            const toast = await toastController.create({
              message: 'Check-in realizado com sucesso!',
              duration: 2000,
              color: 'success'
            });
            await toast.present();
          } catch (error: any) {
            const toast = await toastController.create({
              message: error.response?.data?.error || 'Erro ao fazer check-in',
              duration: 2000,
              color: 'danger'
            });
            await toast.present();
          }
        }
      }
    ]
  });
  await alert.present();
};

const downloadCertificate = () => {
  const url = `${api.defaults.baseURL}/api/events/${event.value.id}/certificate`;
  window.open(url, '_blank');
};

onMounted(() => {
  fetchEventDetails();
});
</script>

<style scoped>
.event-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.placeholder-image {
  height: 200px;
  background-color: #f0f0f0;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.placeholder-icon {
  font-size: 64px;
  color: #ccc;
}

.description {
  margin-top: 1rem;
  line-height: 1.5;
}
</style>
