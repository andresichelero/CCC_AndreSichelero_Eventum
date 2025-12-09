<template>
  <ion-page>
    <ion-content class="ion-padding">
      <div class="login-container">
        <div class="logo-container">
          <h1>Eventum</h1>
          <p>Gestão de Eventos Acadêmicos</p>
        </div>

        <form @submit.prevent="handleLogin">
          <ion-item>
            <ion-label position="floating">Email</ion-label>
            <ion-input v-model="email" type="email" required></ion-input>
          </ion-item>

          <ion-item>
            <ion-label position="floating">Senha</ion-label>
            <ion-input v-model="password" type="password" required></ion-input>
          </ion-item>

          <div class="ion-padding-top">
            <ion-button expand="block" type="submit" :disabled="loading">
              {{ loading ? 'Entrando...' : 'Entrar' }}
            </ion-button>
          </div>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <div class="ion-text-center ion-margin-top">
            <router-link to="/forgot-password" class="auth-link">
              Esqueci minha senha
            </router-link>
          </div>
          <div class="ion-text-center ion-margin-top">
            <router-link to="/register" class="auth-link">
              Não tem conta? Registre-se
            </router-link>
          </div>
        </form>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { IonPage, IonContent, IonItem, IonLabel, IonInput, IonButton } from '@ionic/vue';
import { useAuthStore } from '@/stores/auth';

const email = ref('');
const password = ref('');
const loading = ref(false);
const errorMessage = ref('');
const router = useRouter();
const authStore = useAuthStore();

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = '';
  
  try {
    await authStore.login(email.value, password.value);
    router.replace('/tabs/events');
  } catch (error: any) {
    errorMessage.value = 'Falha no login. Verifique suas credenciais.';
    console.error(error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.logo-container {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-container h1 {
  color: var(--ion-color-primary);
  font-weight: bold;
}

.error-message {
  color: var(--ion-color-danger);
  text-align: center;
  margin-top: 1rem;
}

.auth-link {
  text-decoration: none;
  color: var(--ion-color-secondary);
  font-size: 0.9rem;
  display: block;
}
</style>
