<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/profile"></ion-back-button>
        </ion-buttons>
        <ion-title>Meus Eventos</ion-title>
        <ion-buttons slot="end">
          <ion-button router-link="/events/create">
            <ion-icon :icon="addOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else>
        <ion-list v-if="events.length > 0">
          <ion-card v-for="event in events" :key="event.id">
            <ion-card-header>
              <ion-card-title>{{ event.title }}</ion-card-title>
              <ion-card-subtitle>
                {{ formatDate(event.start_date) }} - {{ formatDate(event.end_date) }}
              </ion-card-subtitle>
            </ion-card-header>
            <ion-card-content>
              <p>{{ event.description }}</p>
              <div class="ion-margin-top">
                <ion-badge :color="event.status === 1 ? 'warning' : 'success'">
                  {{ event.status === 1 ? 'Rascunho' : 'Publicado' }}
                </ion-badge>
              </div>
            </ion-card-content>
            <div class="ion-padding-horizontal ion-padding-bottom" style="display: flex; justify-content: flex-end; gap: 10px;">
              <ion-button size="small" fill="outline" :router-link="`/events/${event.id}/edit`">
                Editar
              </ion-button>
              <ion-button size="small" :router-link="`/events/${event.id}/manage-schedule`">
                Programação
              </ion-button>
              <ion-button size="small" color="danger" fill="clear" @click="deleteEvent(event.id)">
                <ion-icon :icon="trashOutline"></ion-icon>
              </ion-button>
            </div>
          </ion-card>
        </ion-list>

        <div v-else class="ion-text-center ion-padding">
          <p>Você ainda não organizou nenhum evento.</p>
          <ion-button router-link="/events/create">Criar Evento</ion-button>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonBackButton,
  IonList, IonCard, IonCardHeader, IonCardTitle, IonCardSubtitle, IonCardContent,
  IonButton, IonIcon, IonBadge, IonSpinner, toastController, alertController
} from '@ionic/vue';
import { addOutline, trashOutline } from 'ionicons/icons';
import api from '@/services/api';

const events = ref<any[]>([]);
const loading = ref(true);

const fetchEvents = async () => {
  try {
    const response = await api.get('/api/my-organized-events');
    events.value = response.data.events;
  } catch (error) {
    console.error('Error fetching organized events', error);
    const toast = await toastController.create({
      message: 'Erro ao carregar eventos.',
      duration: 3000,
      color: 'danger'
    });
    await toast.present();
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

const deleteEvent = async (id: number) => {
  const alert = await alertController.create({
    header: 'Confirmar Exclusão',
    message: 'Tem certeza que deseja excluir este evento? Esta ação não pode ser desfeita.',
    buttons: [
      {
        text: 'Cancelar',
        role: 'cancel'
      },
      {
        text: 'Excluir',
        role: 'destructive',
        handler: async () => {
          try {
            await api.delete(`/api/events/${id}`);
            const toast = await toastController.create({
              message: 'Evento excluído com sucesso.',
              duration: 2000,
              color: 'success'
            });
            await toast.present();
            fetchEvents();
          } catch (error) {
            console.error('Error deleting event', error);
            const toast = await toastController.create({
              message: 'Erro ao excluir evento.',
              duration: 3000,
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

onMounted(() => {
  fetchEvents();
});
</script>
