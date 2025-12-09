<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Eventos Disponíveis</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding-top">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Eventos</ion-title>
        </ion-toolbar>
      </ion-header>

      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else>
        <div v-for="event in events" :key="event.id">
          <EventCard :event="event" />
        </div>
        
        <div v-if="events.length === 0" class="ion-text-center ion-padding">
          <p>Nenhum evento encontrado.</p>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonSpinner } from '@ionic/vue';
import api from '@/services/api';
import EventCard from '@/components/EventCard.vue';

const events = ref<any[]>([]);
const loading = ref(true);

const fetchEvents = async () => {
  try {
    const response = await api.get('/api/events');
    events.value = response.data.events;
  } catch (error) {
    console.error('Error fetching events', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchEvents();
});
</script>
