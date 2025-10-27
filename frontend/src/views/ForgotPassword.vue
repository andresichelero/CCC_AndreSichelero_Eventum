<template>
  <div class="forgot-section">
    <v-container class="forgot-content">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" md="6" lg="4">
          <v-card class="forgot-card elevation-10" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-4">
              <v-icon size="32" class="me-2">mdi-lock-reset</v-icon>
              Esqueci a Senha
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="forgotPassword" class="pa-4">
                <v-text-field
                  v-model="email"
                  type="email"
                  label="E-mail"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  required
                  class="mb-6"
                ></v-text-field>
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="loading"
                  prepend-icon="mdi-email-send"
                >
                  Enviar Instruções
                </v-btn>
              </v-form>
              <v-alert v-if="message" type="success" class="mt-4" variant="tonal">
                {{ message }}
              </v-alert>
              <v-alert v-if="error" type="error" class="mt-4" variant="tonal">
                {{ error }}
              </v-alert>
              <div class="text-center mt-4">
                <router-link to="/login" class="text-decoration-none secondary--text">
                  Voltar ao Login
                </router-link>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: '',
      error: '',
      message: '',
      loading: false,
    };
  },
  methods: {
    async forgotPassword() {
      this.loading = true;
      this.error = '';
      this.message = '';
      try {
        const response = await axios.post('/api/forgot-password', { email: this.email });
        this.message = response.data.message;
      } catch (err) {
        this.error = err.response.data.error;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.forgot-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.forgot-content {
  max-width: 1200px;
}

.forgot-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.v-btn .v-btn__content {
  align-items: center;
}

@media (max-width: 600px) {
  .forgot-section {
    padding: 20px;
  }
}
</style>
