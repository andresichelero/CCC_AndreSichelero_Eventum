<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/events"></ion-back-button>
        </ion-buttons>
        <ion-title>Editar Evento</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div v-if="loadingEvent" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <form v-else @submit.prevent="handleUpdate">
        <ion-item>
          <ion-label position="floating">Título</ion-label>
          <ion-input v-model="form.title" type="text" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Descrição</ion-label>
          <ion-textarea v-model="form.description" :rows="4"></ion-textarea>
        </ion-item>

        <ion-item>
          <ion-label position="stacked">Data de Início</ion-label>
          <ion-input v-model="form.start_date" type="datetime-local" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="stacked">Data de Fim</ion-label>
          <ion-input v-model="form.end_date" type="datetime-local" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="stacked">Início das Inscrições</ion-label>
          <ion-input v-model="form.inscription_start_date" type="datetime-local" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="stacked">Fim das Inscrições</ion-label>
          <ion-input v-model="form.inscription_end_date" type="datetime-local" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="stacked">Início das Submissões</ion-label>
          <ion-input v-model="form.submission_start_date" type="datetime-local"></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="stacked">Fim das Submissões</ion-label>
          <ion-input v-model="form.submission_end_date" type="datetime-local"></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Status</ion-label>
          <ion-select v-model="form.status" interface="popover">
            <ion-select-option :value="1">Rascunho</ion-select-option>
            <ion-select-option :value="2">Publicado</ion-select-option>
          </ion-select>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Carga Horária (horas)</ion-label>
          <ion-input v-model="form.workload" type="number" min="0" step="0.1"></ion-input>
        </ion-item>

        <div class="ion-padding-top">
          <ion-button expand="block" type="submit" :disabled="saving">
            {{ saving ? 'Salvando...' : 'Salvar Alterações' }}
          </ion-button>
        </div>

        <div v-if="errorMessage" class="error-message ion-padding-top">
          {{ errorMessage }}
        </div>
      </form>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, 
  IonItem, IonLabel, IonInput, IonTextarea, IonButton, IonSelect, IonSelectOption,
  IonButtons, IonBackButton, IonSpinner
} from '@ionic/vue';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();
const eventId = route.params.id;

const form = reactive({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  inscription_start_date: '',
  inscription_end_date: '',
  submission_start_date: '',
  submission_end_date: '',
  status: 1,
  workload: ''
});

const loadingEvent = ref(true);
const saving = ref(false);
const errorMessage = ref('');

const loadEvent = async () => {
  loadingEvent.value = true;
  try {
    const response = await api.get(`/api/events/${eventId}`);
    const event = response.data.event;
    
    form.title = event.title;
    form.description = event.description;
    form.start_date = formatDateForInput(event.start_date);
    form.end_date = formatDateForInput(event.end_date);
    form.inscription_start_date = formatDateForInput(event.inscription_start_date);
    form.inscription_end_date = formatDateForInput(event.inscription_end_date);
    form.submission_start_date = formatDateForInput(event.submission_start_date);
    form.submission_end_date = formatDateForInput(event.submission_end_date);
    form.status = event.status;
    form.workload = event.workload;
    
  } catch (error) {
    console.error('Erro ao carregar evento', error);
    errorMessage.value = 'Erro ao carregar evento.';
  } finally {
    loadingEvent.value = false;
  }
};

const formatDateForInput = (dateString: string) => {
  if (!dateString) return '';
  // Assuming dateString is ISO or similar, we need YYYY-MM-DDTHH:mm
  // If it comes as "Mon, 08 Dec 2025 12:00:00 GMT", we need to parse it.
  // But usually API returns ISO. Let's assume ISO or standard JS Date string.
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '';
  
  // Format to YYYY-MM-DDTHH:mm
  const pad = (n: number) => n < 10 ? '0' + n : n;
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
};

const handleUpdate = async () => {
  saving.value = true;
  errorMessage.value = '';
  
  try {
    await api.put(`/api/events/${eventId}`, form);
    router.push('/tabs/events');
  } catch (error: any) {
    if (error.response && error.response.data && error.response.data.error) {
      errorMessage.value = error.response.data.error;
    } else {
      errorMessage.value = 'Erro ao atualizar evento.';
    }
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadEvent();
});
</script>

<style scoped>
.error-message {
  color: var(--ion-color-danger);
  text-align: center;
}
</style>
