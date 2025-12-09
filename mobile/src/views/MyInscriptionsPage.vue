<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Minhas Inscrições</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding-top">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Minhas Inscrições</ion-title>
        </ion-toolbar>
      </ion-header>

      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else>
        <div v-for="inscription in inscriptions" :key="inscription.id">
          <EventCard :event="inscription" />
        </div>
        
        <div v-if="inscriptions.length === 0" class="empty-state ion-text-center ion-padding">
          <ion-icon :icon="calendarOutline" class="empty-icon"></ion-icon>
          <h3>Nenhuma inscrição encontrada</h3>
          <p>Você ainda não se inscreveu em nenhum evento.</p>
          <ion-button router-link="/tabs/events" fill="outline" class="ion-margin-top">Ver Eventos</ion-button>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonSpinner, IonButton, IonIcon, toastController } from '@ionic/vue';
import { calendarOutline } from 'ionicons/icons';
import api from '@/services/api';
import EventCard from '@/components/EventCard.vue';

const inscriptions = ref<any[]>([]);
const loading = ref(true);

const fetchInscriptions = async () => {
  try {
    const response = await api.get('/api/my-inscriptions');
    if (response.data && response.data.events) {
      inscriptions.value = response.data.events;
    } else {
      inscriptions.value = [];
    }
  } catch (error) {
    console.error('Error fetching inscriptions', error);
    const toast = await toastController.create({
      message: 'Erro ao carregar inscrições. Tente novamente.',
      duration: 3000,
      color: 'danger',
      position: 'bottom'
    });
    await toast.present();
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchInscriptions();
});
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
}

.empty-icon {
  font-size: 64px;
  color: var(--ion-color-medium);
  margin-bottom: 16px;
}

h3 {
  margin-bottom: 8px;
  color: var(--ion-color-dark);
}
</style>
