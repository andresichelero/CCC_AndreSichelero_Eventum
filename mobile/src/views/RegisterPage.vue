<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/login"></ion-back-button>
        </ion-buttons>
        <ion-title>Registrar</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <form @submit.prevent="handleRegister">
        <ion-item>
          <ion-label position="floating">Nome Completo</ion-label>
          <ion-input v-model="name" type="text" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Email</ion-label>
          <ion-input v-model="email" type="email" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Tipo de Conta</ion-label>
          <ion-select v-model="role" interface="popover">
            <ion-select-option value="3">Participante</ion-select-option>
            <ion-select-option value="2">Palestrante/Autor</ion-select-option>
            <ion-select-option value="1">Organizador</ion-select-option>
          </ion-select>
        </ion-item>

        <div class="ion-padding-top">
          <ion-text color="medium">
            <p class="ion-no-margin ion-padding-start">Vínculo Acadêmico (Opcional)</p>
          </ion-text>
          
          <ion-item>
            <ion-label position="floating">Faculdade</ion-label>
            <ion-select v-model="faculdadeId" @ionChange="onFaculdadeChange" interface="action-sheet" cancel-text="Cancelar">
              <ion-select-option v-for="faculdade in faculdades" :key="faculdade.id" :value="faculdade.id">
                {{ faculdade.name }}
              </ion-select-option>
            </ion-select>
          </ion-item>

          <ion-item>
            <ion-label position="floating">Curso</ion-label>
            <ion-select v-model="cursoId" @ionChange="onCursoChange" :disabled="!faculdadeId" interface="action-sheet" cancel-text="Cancelar">
              <ion-select-option v-for="curso in cursos" :key="curso.id" :value="curso.id">
                {{ curso.name }}
              </ion-select-option>
            </ion-select>
          </ion-item>

          <ion-item>
            <ion-label position="floating">Turma</ion-label>
            <ion-select v-model="turmaId" :disabled="!cursoId" interface="action-sheet" cancel-text="Cancelar">
              <ion-select-option v-for="turma in turmas" :key="turma.id" :value="turma.id">
                {{ turma.name }}
              </ion-select-option>
            </ion-select>
          </ion-item>
        </div>

        <ion-item>
          <ion-label position="floating">Senha</ion-label>
          <ion-input v-model="password" type="password" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Confirmar Senha</ion-label>
          <ion-input v-model="confirmPassword" type="password" required></ion-input>
        </ion-item>

        <ion-item lines="none" class="ion-margin-top">
          <ion-checkbox slot="start" v-model="acceptTerms"></ion-checkbox>
          <ion-label class="ion-text-wrap">
            Eu aceito os <a href="/termos-de-uso" target="_blank">Termos de Uso</a> e <a href="/politica-de-privacidade" target="_blank">Política de Privacidade</a>
          </ion-label>
        </ion-item>

        <div class="ion-padding-top">
          <ion-button expand="block" type="submit" :disabled="loading">
            {{ loading ? 'Registrando...' : 'Registrar' }}
          </ion-button>
        </div>

        <div v-if="errorMessage" class="error-message ion-padding-top">
          {{ errorMessage }}
        </div>
        
        <div v-if="successMessage" class="success-message ion-padding-top">
          {{ successMessage }}
        </div>

        <div class="ion-text-center ion-margin-top">
          <router-link to="/login" class="auth-link">
            Já tem conta? Faça login
          </router-link>
        </div>
      </form>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, 
  IonItem, IonLabel, IonInput, IonButton, IonSelect, IonSelectOption,
  IonButtons, IonBackButton, IonCheckbox, IonText
} from '@ionic/vue';
import api from '@/services/api';

const router = useRouter();

const name = ref('');
const email = ref('');
const role = ref('3');
const faculdadeId = ref<number | null>(null);
const cursoId = ref<number | null>(null);
const turmaId = ref<number | null>(null);
const password = ref('');
const confirmPassword = ref('');
const acceptTerms = ref(false);

const faculdades = ref<any[]>([]);
const cursos = ref<any[]>([]);
const turmas = ref<any[]>([]);

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const loadFaculdades = async () => {
  try {
    const response = await api.get('/api/faculdades');
    faculdades.value = response.data.faculdades;
  } catch (error) {
    console.error('Erro ao carregar faculdades', error);
  }
};

const onFaculdadeChange = async () => {
  cursoId.value = null;
  turmaId.value = null;
  cursos.value = [];
  turmas.value = [];
  
  if (faculdadeId.value) {
    try {
      const response = await api.get(`/api/cursos?faculdade_id=${faculdadeId.value}`);
      cursos.value = response.data.cursos;
    } catch (error) {
      console.error('Erro ao carregar cursos', error);
    }
  }
};

const onCursoChange = async () => {
  turmaId.value = null;
  turmas.value = [];
  
  if (cursoId.value) {
    try {
      const response = await api.get(`/api/turmas?curso_id=${cursoId.value}`);
      turmas.value = response.data.turmas;
    } catch (error) {
      console.error('Erro ao carregar turmas', error);
    }
  }
};

const handleRegister = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  
  if (!name.value || !email.value || !password.value) {
    errorMessage.value = 'Preencha todos os campos obrigatórios.';
    return;
  }
  
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'As senhas não coincidem.';
    return;
  }
  
  if (!acceptTerms.value) {
    errorMessage.value = 'Você deve aceitar os termos.';
    return;
  }

  loading.value = true;

  try {
    const response = await api.post('/api/register', {
      name: name.value,
      email: email.value,
      password: password.value,
      role: role.value,
      accept_terms: acceptTerms.value,
      faculdade_id: faculdadeId.value,
      curso_id: cursoId.value,
      turma_id: turmaId.value
    });
    
    successMessage.value = response.data.message || 'Registro realizado com sucesso!';
    
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (error: any) {
    if (error.response && error.response.data && error.response.data.error) {
      errorMessage.value = error.response.data.error;
    } else {
      errorMessage.value = 'Erro ao registrar. Tente novamente.';
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

.success-message {
  color: var(--ion-color-success);
  text-align: center;
}

.auth-link {
  text-decoration: none;
  color: var(--ion-color-secondary);
}
</style>
