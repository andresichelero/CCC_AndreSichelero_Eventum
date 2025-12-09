<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/profile"></ion-back-button>
        </ion-buttons>
        <ion-title>Minhas Submissões</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else-if="submissions.length === 0" class="ion-text-center ion-padding">
        <p>Você ainda não submeteu nenhum trabalho.</p>
      </div>

      <ion-list v-else>
        <ion-card v-for="sub in submissions" :key="sub.id">
          <ion-card-header>
            <ion-card-subtitle>{{ sub.event.title }}</ion-card-subtitle>
            <ion-card-title>{{ sub.title }}</ion-card-title>
          </ion-card-header>

          <ion-card-content>
            <p>
              <strong>Arquivo:</strong> {{ sub.file_path }}
            </p>
            <div class="ion-margin-top">
              <ion-chip :color="getStatusColor(sub.status)">
                <ion-label>{{ getStatusText(sub.status) }}</ion-label>
              </ion-chip>
            </div>
            <div class="ion-margin-top">
              <ion-button fill="outline" size="small" @click="downloadFile(sub.id)">
                Baixar Arquivo
              </ion-button>
            </div>
          </ion-card-content>
        </ion-card>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, 
  IonList, IonCard, IonCardHeader, IonCardSubtitle, IonCardTitle, IonCardContent,
  IonChip, IonLabel, IonButton, IonButtons, IonBackButton, IonSpinner
} from '@ionic/vue';
import api from '@/services/api';

const submissions = ref<any[]>([]);
const loading = ref(true);

const loadSubmissions = async () => {
  loading.value = true;
  try {
    const response = await api.get('/api/my-submissions');
    submissions.value = response.data.submissions;
  } catch (error) {
    console.error('Erro ao carregar submissões', error);
  } finally {
    loading.value = false;
  }
};

const getStatusColor = (status: number) => {
  switch (status) {
    case 1: return 'primary'; // Submetido
    case 3: return 'success'; // Aprovado
    case 4: return 'danger';  // Rejeitado
    default: return 'medium'; // Em avaliação
  }
};

const getStatusText = (status: number) => {
  switch (status) {
    case 1: return 'Submetido';
    case 3: return 'Aprovado';
    case 4: return 'Rejeitado';
    default: return 'Em avaliação';
  }
};

const downloadFile = (id: number) => {
  // Assuming the API URL is accessible directly or via proxy
  // In a real mobile app, you might need to use FileTransfer plugin or similar
  // But for PWA/Web view, this works.
  const url = `${api.defaults.baseURL}/api/submissions/${id}/download`;
  window.open(url, '_blank');
};

onMounted(() => {
  loadSubmissions();
});
</script>
