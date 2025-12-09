<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/tabs/profile"></ion-back-button>
        </ion-buttons>
        <ion-title>Gerenciar Turmas</ion-title>
      </ion-toolbar>
      <ion-toolbar>
        <ion-segment v-model="segment" @ionChange="segmentChanged">
          <ion-segment-button value="list">
            <ion-label>Listar</ion-label>
          </ion-segment-button>
          <ion-segment-button value="create-curso">
            <ion-label>Novo Curso</ion-label>
          </ion-segment-button>
          <ion-segment-button value="create-turma">
            <ion-label>Nova Turma</ion-label>
          </ion-segment-button>
        </ion-segment>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else>
        <!-- List Turmas -->
        <div v-if="segment === 'list'" class="ion-padding">
          <ion-item>
            <ion-select label="Filtrar por Faculdade" label-placement="floating" v-model="filterFaculdade" @ionChange="filterTurmas">
              <ion-select-option :value="null">Todas</ion-select-option>
              <ion-select-option v-for="fac in faculdades" :key="fac.id" :value="fac.id">
                {{ fac.name }}
              </ion-select-option>
            </ion-select>
          </ion-item>

          <ion-list>
            <ion-item v-for="turma in filteredTurmas" :key="turma.id">
              <ion-label>
                <h2>{{ turma.name }}</h2>
                <p>{{ getCursoName(turma.curso_id) }}</p>
                <p>{{ getFaculdadeName(turma.faculdade_id) }}</p>
              </ion-label>
              <ion-button fill="clear" color="danger" slot="end" @click="deleteTurma(turma.id)">
                <ion-icon :icon="trashOutline"></ion-icon>
              </ion-button>
            </ion-item>
          </ion-list>
          
          <div v-if="filteredTurmas.length === 0" class="ion-text-center ion-padding">
            <p>Nenhuma turma encontrada.</p>
          </div>
        </div>

        <!-- Create Curso -->
        <div v-if="segment === 'create-curso'" class="ion-padding">
          <ion-list>
            <ion-item>
              <ion-select label="Faculdade" label-placement="floating" v-model="newCurso.faculdade_id">
                <ion-select-option v-for="fac in faculdades" :key="fac.id" :value="fac.id">
                  {{ fac.name }}
                </ion-select-option>
              </ion-select>
            </ion-item>
            <ion-item>
              <ion-input label="Nome do Curso" label-placement="floating" v-model="newCurso.name"></ion-input>
            </ion-item>
          </ion-list>
          <div class="ion-padding">
            <ion-button expand="block" @click="createCurso">Criar Curso</ion-button>
          </div>
        </div>

        <!-- Create Turma -->
        <div v-if="segment === 'create-turma'" class="ion-padding">
          <ion-list>
            <ion-item>
              <ion-select label="Faculdade" label-placement="floating" v-model="newTurma.faculdade_id" @ionChange="loadCursosForNewTurma">
                <ion-select-option v-for="fac in faculdades" :key="fac.id" :value="fac.id">
                  {{ fac.name }}
                </ion-select-option>
              </ion-select>
            </ion-item>
            <ion-item>
              <ion-select label="Curso" label-placement="floating" v-model="newTurma.curso_id" :disabled="!newTurma.faculdade_id">
                <ion-select-option v-for="curso in cursosForNewTurma" :key="curso.id" :value="curso.id">
                  {{ curso.name }}
                </ion-select-option>
              </ion-select>
            </ion-item>
            <ion-item>
              <ion-input label="Nome da Turma" label-placement="floating" v-model="newTurma.name"></ion-input>
            </ion-item>
          </ion-list>
          <div class="ion-padding">
            <ion-button expand="block" @click="createTurma" :disabled="!newTurma.curso_id || !newTurma.name">Criar Turma</ion-button>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonBackButton,
  IonSegment, IonSegmentButton, IonLabel, IonList, IonItem, IonInput, IonButton,
  IonSelect, IonSelectOption, IonSpinner, IonIcon, toastController, alertController
} from '@ionic/vue';
import { trashOutline } from 'ionicons/icons';
import api from '@/services/api';

const segment = ref('list');
const loading = ref(true);
const faculdades = ref<any[]>([]);
const cursos = ref<any[]>([]);
const turmas = ref<any[]>([]);
const filterFaculdade = ref<number | null>(null);

const newCurso = ref({
  faculdade_id: null,
  name: ''
});

const newTurma = ref({
  faculdade_id: null,
  curso_id: null,
  name: ''
});

const cursosForNewTurma = ref<any[]>([]);

const fetchData = async () => {
  loading.value = true;
  try {
    const [facResponse, cursosResponse, turmasResponse] = await Promise.all([
      api.get('/api/faculdades'),
      api.get('/api/cursos'),
      api.get('/api/turmas')
    ]);
    faculdades.value = facResponse.data.faculdades;
    cursos.value = cursosResponse.data.cursos;
    turmas.value = turmasResponse.data.turmas;
  } catch (error) {
    console.error('Error fetching data', error);
    showToast('Erro ao carregar dados', 'danger');
  } finally {
    loading.value = false;
  }
};

const filteredTurmas = computed(() => {
  if (!filterFaculdade.value) return turmas.value;
  return turmas.value.filter(t => t.faculdade_id === filterFaculdade.value);
});

const getCursoName = (id: number) => {
  const curso = cursos.value.find(c => c.id === id);
  return curso ? curso.name : 'Desconhecido';
};

const getFaculdadeName = (id: number) => {
  const fac = faculdades.value.find(f => f.id === id);
  return fac ? fac.name : 'Desconhecida';
};

const loadCursosForNewTurma = () => {
  if (newTurma.value.faculdade_id) {
    cursosForNewTurma.value = cursos.value.filter(c => c.faculdade_id === newTurma.value.faculdade_id);
  } else {
    cursosForNewTurma.value = [];
  }
};

const createCurso = async () => {
  if (!newCurso.value.faculdade_id || !newCurso.value.name) {
    showToast('Preencha todos os campos', 'warning');
    return;
  }
  try {
    await api.post('/api/cursos', newCurso.value);
    showToast('Curso criado com sucesso!', 'success');
    newCurso.value = { faculdade_id: null, name: '' };
    fetchData();
    segment.value = 'list';
  } catch (error) {
    console.error('Error creating curso', error);
    showToast('Erro ao criar curso', 'danger');
  }
};

const createTurma = async () => {
  if (!newTurma.value.curso_id || !newTurma.value.name) {
    showToast('Preencha todos os campos', 'warning');
    return;
  }
  try {
    await api.post('/api/turmas', {
      curso_id: newTurma.value.curso_id,
      name: newTurma.value.name,
      faculdade_id: newTurma.value.faculdade_id // Backend might need this or infer from curso
    });
    showToast('Turma criada com sucesso!', 'success');
    newTurma.value = { faculdade_id: null, curso_id: null, name: '' };
    fetchData();
    segment.value = 'list';
  } catch (error) {
    console.error('Error creating turma', error);
    showToast('Erro ao criar turma', 'danger');
  }
};

const deleteTurma = async (id: number) => {
  const alert = await alertController.create({
    header: 'Confirmar Exclusão',
    message: 'Tem certeza que deseja excluir esta turma?',
    buttons: [
      { text: 'Cancelar', role: 'cancel' },
      {
        text: 'Excluir',
        role: 'destructive',
        handler: async () => {
          try {
            await api.delete(`/api/turmas/${id}`);
            showToast('Turma excluída com sucesso', 'success');
            fetchData();
          } catch (error) {
            console.error('Error deleting turma', error);
            showToast('Erro ao excluir turma', 'danger');
          }
        }
      }
    ]
  });
  await alert.present();
};

const showToast = async (message: string, color: string) => {
  const toast = await toastController.create({
    message,
    duration: 2000,
    color
  });
  await toast.present();
};

const segmentChanged = (e: any) => {
  segment.value = e.detail.value;
};

const filterTurmas = () => {
  // Triggered by ionChange, but computed property handles it
};

onMounted(() => {
  fetchData();
});
</script>
