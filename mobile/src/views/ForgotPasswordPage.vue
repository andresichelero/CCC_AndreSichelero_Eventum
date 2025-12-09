<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/login"></ion-back-button>
        </ion-buttons>
        <ion-title>Esqueci a Senha</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div class="forgot-container">
        <div class="ion-text-center ion-padding-bottom">
          <p>Digite seu email para receber as instruções de recuperação de senha.</p>
        </div>

        <form @submit.prevent="handleForgotPassword">
          <ion-item>
            <ion-label position="floating">Email</ion-label>
            <ion-input v-model="email" type="email" required></ion-input>
          </ion-item>

          <div class="ion-padding-top">
            <ion-button expand="block" type="submit" :disabled="loading">
              {{ loading ? 'Enviando...' : 'Enviar Instruções' }}
            </ion-button>
          </div>

          <div v-if="message" class="success-message ion-padding-top">
            {{ message }}
          </div>
          
          <div v-if="error" class="error-message ion-padding-top">
            {{ error }}
          </div>

          <div class="ion-text-center ion-margin-top">
            <router-link to="/login" class="auth-link">
              Voltar ao Login
            </router-link>
          </div>
        </form>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { 
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, 
  IonItem, IonLabel, IonInput, IonButton, IonButtons, IonBackButton 
} from '@ionic/vue';
import api from '@/services/api';

const email = ref('');
const loading = ref(false);
const message = ref('');
const error = ref('');

const handleForgotPassword = async () => {
  loading.value = true;
  message.value = '';
  error.value = '';
  
  try {
    const response = await api.post('/api/forgot-password', { email: email.value });
    message.value = response.data.message;
  } catch (err: any) {
    if (err.response && err.response.data && err.response.data.error) {
      error.value = err.response.data.error;
    } else {
      error.value = 'Erro ao enviar email. Tente novamente.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.forgot-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.success-message {
  color: var(--ion-color-success);
  text-align: center;
}

.error-message {
  color: var(--ion-color-danger);
  text-align: center;
}

.auth-link {
  text-decoration: none;
  color: var(--ion-color-secondary);
}
</style>
