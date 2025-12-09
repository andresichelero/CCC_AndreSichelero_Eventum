<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Meu Perfil</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding">
      <div class="profile-container" v-if="user">
        <div class="avatar-container">
          <ion-avatar class="large-avatar">
            <img src="https://ionicframework.com/docs/img/demos/avatar.svg" alt="Avatar" />
          </ion-avatar>
        </div>
        
        <div class="ion-text-center ion-margin-bottom">
          <h2>{{ user.name }}</h2>
          <p class="text-medium">{{ user.email }}</p>
          <ion-badge color="primary" class="ion-margin-top">{{ getRoleName(user.role) }}</ion-badge>
        </div>

        <ion-list inset>
          <ion-item button @click="openEditProfileModal">
            <ion-icon :icon="personOutline" slot="start"></ion-icon>
            <ion-label>Editar Perfil</ion-label>
          </ion-item>
          <ion-item button @click="openChangePasswordModal">
            <ion-icon :icon="lockClosedOutline" slot="start"></ion-icon>
            <ion-label>Alterar Senha</ion-label>
          </ion-item>
          <ion-item button router-link="/my-organized-events" v-if="user.role === 1">
            <ion-icon :icon="calendarOutline" slot="start"></ion-icon>
            <ion-label>Meus Eventos Organizados</ion-label>
          </ion-item>
          <ion-item button router-link="/manage-turmas" v-if="user.role === 1">
            <ion-icon :icon="schoolOutline" slot="start"></ion-icon>
            <ion-label>Gerenciar Turmas</ion-label>
          </ion-item>
          <ion-item>
            <ion-icon :icon="eyeOutline" slot="start"></ion-icon>
            <ion-label>Perfil Público</ion-label>
            <ion-toggle :checked="user.allow_public_profile" @ionChange="togglePublicProfile" slot="end"></ion-toggle>
          </ion-item>
          <ion-item button router-link="/privacy-policy">
            <ion-icon :icon="shieldCheckmarkOutline" slot="start"></ion-icon>
            <ion-label>Política de Privacidade</ion-label>
          </ion-item>
          <ion-item button router-link="/terms-of-use">
            <ion-icon :icon="documentTextOutline" slot="start"></ion-icon>
            <ion-label>Termos de Uso</ion-label>
          </ion-item>
        </ion-list>

        <div class="ion-padding-top ion-margin-top">
          <ion-button expand="block" color="danger" fill="outline" @click="handleLogout">
            <ion-icon :icon="logOutOutline" slot="start"></ion-icon>
            Sair
          </ion-button>
        </div>
      </div>

      <!-- Edit Profile Modal -->
      <ion-modal :is-open="isEditProfileOpen" @didDismiss="isEditProfileOpen = false">
        <ion-header>
          <ion-toolbar>
            <ion-title>Editar Perfil</ion-title>
            <ion-buttons slot="end">
              <ion-button @click="isEditProfileOpen = false">Fechar</ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>
        <ion-content class="ion-padding">
          <ion-item>
            <ion-label position="stacked">Nome</ion-label>
            <ion-input v-model="editForm.name" type="text"></ion-input>
          </ion-item>
          <ion-item>
            <ion-label position="stacked">Email</ion-label>
            <ion-input v-model="editForm.email" type="email"></ion-input>
          </ion-item>
          <div class="ion-padding-top">
            <ion-button expand="block" @click="saveProfile">Salvar</ion-button>
          </div>
        </ion-content>
      </ion-modal>

      <!-- Change Password Modal -->
      <ion-modal :is-open="isChangePasswordOpen" @didDismiss="isChangePasswordOpen = false">
        <ion-header>
          <ion-toolbar>
            <ion-title>Alterar Senha</ion-title>
            <ion-buttons slot="end">
              <ion-button @click="isChangePasswordOpen = false">Fechar</ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>
        <ion-content class="ion-padding">
          <ion-item>
            <ion-label position="stacked">Nova Senha</ion-label>
            <ion-input v-model="passwordForm.password" type="password"></ion-input>
          </ion-item>
          <ion-item>
            <ion-label position="stacked">Confirmar Senha</ion-label>
            <ion-input v-model="passwordForm.confirmPassword" type="password"></ion-input>
          </ion-item>
          <div class="ion-padding-top">
            <ion-button expand="block" @click="savePassword">Alterar Senha</ion-button>
          </div>
        </ion-content>
      </ion-modal>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { computed, ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel, IonButton, IonIcon, IonAvatar, IonBadge, IonToggle, IonModal, IonButtons, IonInput, toastController } from '@ionic/vue';
import { personOutline, lockClosedOutline, logOutOutline, eyeOutline, calendarOutline, schoolOutline, documentTextOutline, shieldCheckmarkOutline } from 'ionicons/icons';
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';

const authStore = useAuthStore();
const router = useRouter();
const user = computed(() => authStore.user);

const isEditProfileOpen = ref(false);
const isChangePasswordOpen = ref(false);

const editForm = reactive({
  name: '',
  email: ''
});

const passwordForm = reactive({
  password: '',
  confirmPassword: ''
});

const getRoleName = (role: number) => {
  switch (role) {
    case 1: return 'Organizador';
    case 2: return 'Palestrante';
    case 3: return 'Participante';
    case 4: return 'Professor';
    default: return 'Usuário';
  }
};

const handleLogout = async () => {
  await authStore.logout();
  router.replace('/login');
};

const openEditProfileModal = () => {
  if (user.value) {
    editForm.name = user.value.name;
    editForm.email = user.value.email;
    isEditProfileOpen.value = true;
  }
};

const openChangePasswordModal = () => {
  passwordForm.password = '';
  passwordForm.confirmPassword = '';
  isChangePasswordOpen.value = true;
};

const showToast = async (message: string, color: string = 'success') => {
  const toast = await toastController.create({
    message,
    duration: 3000,
    color,
    position: 'bottom'
  });
  await toast.present();
};

const saveProfile = async () => {
  try {
    const response = await api.put('/api/me/settings', {
      name: editForm.name,
      email: editForm.email
    });
    
    // Update local user data
    authStore.user = response.data.user;
    
    showToast('Perfil atualizado com sucesso!');
    isEditProfileOpen.value = false;
  } catch (error: any) {
    console.error('Error updating profile', error);
    showToast(error.response?.data?.error || 'Erro ao atualizar perfil', 'danger');
  }
};

const savePassword = async () => {
  if (passwordForm.password !== passwordForm.confirmPassword) {
    showToast('As senhas não conferem', 'warning');
    return;
  }
  
  if (passwordForm.password.length < 6) {
    showToast('A senha deve ter pelo menos 6 caracteres', 'warning');
    return;
  }

  try {
    await api.put('/api/me/settings', {
      password: passwordForm.password
    });
    
    showToast('Senha alterada com sucesso!');
    isChangePasswordOpen.value = false;
  } catch (error: any) {
    console.error('Error updating password', error);
    showToast(error.response?.data?.error || 'Erro ao alterar senha', 'danger');
  }
};

const togglePublicProfile = async (event: any) => {
  const isChecked = event.detail.checked;
  try {
    const response = await api.put('/api/me/settings', {
      allow_public_profile: isChecked
    });
    authStore.user = response.data.user;
    showToast(`Perfil público ${isChecked ? 'ativado' : 'desativado'}`);
  } catch (error: any) {
    console.error('Error toggling public profile', error);
    // Revert toggle if failed (might need more complex logic to revert UI)
    showToast('Erro ao atualizar configuração', 'danger');
  }
};
</script>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.avatar-container {
  display: flex;
  justify-content: center;
  padding: 2rem 0 1rem;
}

.large-avatar {
  width: 100px;
  height: 100px;
}

.text-medium {
  color: var(--ion-color-medium);
}
</style>
