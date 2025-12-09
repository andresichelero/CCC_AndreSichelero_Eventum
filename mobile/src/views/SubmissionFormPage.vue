<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/events"></ion-back-button>
        </ion-buttons>
        <ion-title>Submeter Trabalho</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div v-if="loadingEvent" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else>
        <div class="ion-text-center ion-margin-bottom">
          <h2>{{ event.title }}</h2>
        </div>

        <form @submit.prevent="handleSubmit">
          <ion-item>
            <ion-label position="floating">Título do Trabalho</ion-label>
            <ion-input v-model="title" type="text" required></ion-input>
          </ion-item>

          <div class="ion-padding-top ion-padding-horizontal">
            <ion-label>Arquivo (PDF, DOCX, etc.)</ion-label>
            <input type="file" @change="onFileChange" accept=".pdf,.doc,.docx,.odt,.rtf" required class="file-input" />
          </div>

          <div class="ion-padding-top">
            <ion-button expand="block" type="submit" :disabled="submitting">
              {{ submitting ? 'Enviando...' : 'Enviar Submissão' }}
            </ion-button>
          </div>

          <div v-if="errorMessage" class="error-message ion-padding-top">
            {{ errorMessage }}
          </div>
        </form>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, 
  IonItem, IonLabel, IonInput, IonButton, IonButtons, IonBackButton, IonSpinner
} from '@ionic/vue';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();
const eventId = route.params.id;

const event = ref<any>({});
const title = ref('');
const file = ref<File | null>(null);
const loadingEvent = ref(true);
const submitting = ref(false);
const errorMessage = ref('');

const loadEvent = async () => {
  loadingEvent.value = true;
  try {
    const response = await api.get(`/api/events/${eventId}`);
    event.value = response.data.event;
  } catch (error) {
    console.error('Erro ao carregar evento', error);
    errorMessage.value = 'Erro ao carregar detalhes do evento.';
  } finally {
    loadingEvent.value = false;
  }
};

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    file.value = target.files[0];
  }
};

const handleSubmit = async () => {
  if (!title.value || !file.value) {
    errorMessage.value = 'Preencha todos os campos.';
    return;
  }

  submitting.value = true;
  errorMessage.value = '';

  const formData = new FormData();
  formData.append('title', title.value);
  formData.append('file', file.value);

  try {
    await api.post(`/api/events/${eventId}/submit`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    router.push('/tabs/submissions');
  } catch (error: any) {
    if (error.response && error.response.data && error.response.data.error) {
      errorMessage.value = error.response.data.error;
    } else {
      errorMessage.value = 'Erro ao enviar submissão.';
    }
  } finally {
    submitting.value = false;
  }
};

onMounted(() => {
  loadEvent();
});
</script>

<style scoped>
.file-input {
  margin-top: 10px;
  width: 100%;
}

.error-message {
  color: var(--ion-color-danger);
  text-align: center;
}
</style>
