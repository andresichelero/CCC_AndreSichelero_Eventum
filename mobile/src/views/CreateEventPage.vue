<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/events"></ion-back-button>
        </ion-buttons>
        <ion-title>Criar Evento</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <form @submit.prevent="handleCreate">
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
            <ion-select-option value="1">Rascunho</ion-select-option>
            <ion-select-option value="2">Publicado</ion-select-option>
          </ion-select>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Carga Horária (horas)</ion-label>
          <ion-input v-model="form.workload" type="number" min="0" step="0.1"></ion-input>
        </ion-item>

        <div class="ion-padding-top">
          <ion-text color="medium">
            <p class="ion-no-margin ion-padding-start">Organização (Opcional)</p>
          </ion-text>

          <ion-item>
            <ion-label position="floating">Faculdade</ion-label>
            <ion-select v-model="form.faculdade_id" @ionChange="onFaculdadeChange" interface="action-sheet" cancel-text="Cancelar">
              <ion-select-option v-for="faculdade in faculdades" :key="faculdade.id" :value="faculdade.id">
                {{ faculdade.name }}
              </ion-select-option>
            </ion-select>
          </ion-item>

          <ion-item>
            <ion-label position="floating">Curso</ion-label>
            <ion-select v-model="form.curso_id" @ionChange="onCursoChange" :disabled="!form.faculdade_id" interface="action-sheet" cancel-text="Cancelar">
              <ion-select-option v-for="curso in cursos" :key="curso.id" :value="curso.id">
                {{ curso.name }}
              </ion-select-option>
            </ion-select>
          </ion-item>

          <ion-item>
            <ion-label position="floating">Turma</ion-label>
            <ion-select v-model="form.turma_id" :disabled="!form.curso_id" interface="action-sheet" cancel-text="Cancelar">
              <ion-select-option v-for="turma in turmas" :key="turma.id" :value="turma.id">
                {{ turma.name }}
              </ion-select-option>
            </ion-select>
          </ion-item>
        </div>

        <div class="ion-padding-top">
          <ion-button expand="block" type="submit" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Salvar Evento' }}
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
import { useRouter } from 'vue-router';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, 
  IonItem, IonLabel, IonInput, IonTextarea, IonButton, IonSelect, IonSelectOption,
  IonButtons, IonBackButton, IonText
} from '@ionic/vue';
import api from '@/services/api';

const router = useRouter();

const form = reactive({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  inscription_start_date: '',
  inscription_end_date: '',
  submission_start_date: '',
  submission_end_date: '',
  status: '1',
  workload: '',
  faculdade_id: null,
  curso_id: null,
  turma_id: null
});

const faculdades = ref<any[]>([]);
const cursos = ref<any[]>([]);
const turmas = ref<any[]>([]);

const loading = ref(false);
const errorMessage = ref('');

const loadFaculdades = async () => {
  try {
    const response = await api.get('/api/faculdades');
    faculdades.value = response.data.faculdades;
  } catch (error) {
    console.error('Erro ao carregar faculdades', error);
  }
};

const onFaculdadeChange = async () => {
  form.curso_id = null;
  form.turma_id = null;
  cursos.value = [];
  turmas.value = [];
  
  if (form.faculdade_id) {
    try {
      const response = await api.get(`/api/cursos?faculdade_id=${form.faculdade_id}`);
      cursos.value = response.data.cursos;
    } catch (error) {
      console.error('Erro ao carregar cursos', error);
    }
  }
};

const onCursoChange = async () => {
  form.turma_id = null;
  turmas.value = [];
  
  if (form.curso_id) {
    try {
      const response = await api.get(`/api/turmas?curso_id=${form.curso_id}`);
      turmas.value = response.data.turmas;
    } catch (error) {
      console.error('Erro ao carregar turmas', error);
    }
  }
};

const handleCreate = async () => {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    await api.post('/api/events', form);
    router.push('/tabs/events');
  } catch (error: any) {
    if (error.response && error.response.data && error.response.data.error) {
      errorMessage.value = error.response.data.error;
    } else {
      errorMessage.value = 'Erro ao criar evento.';
    }
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadFaculdades();
});
</script>

<style scoped>
.error-message {
  color: var(--ion-color-danger);
  text-align: center;
}
</style>
