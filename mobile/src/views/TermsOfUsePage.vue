<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/profile"></ion-back-button>
        </ion-buttons>
        <ion-title>Termos de Uso</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <div v-if="loading" class="ion-text-center">
        <ion-spinner></ion-spinner>
      </div>
      <div v-else v-html="content"></div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonBackButton, IonSpinner } from '@ionic/vue';
import api from '@/services/api';

const content = ref('');
const loading = ref(true);

onMounted(async () => {
  try {
    const response = await api.get('/api/termos-de-uso');
    content.value = response.data.content;
  } catch (error) {
    console.error('Error fetching terms of use', error);
    content.value = '<p>Erro ao carregar os termos de uso.</p>';
  } finally {
    loading.value = false;
  }
});
</script>
