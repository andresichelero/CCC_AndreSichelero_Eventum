<template>
  <div class="login-section">
    <v-container class="login-content">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" md="6" lg="4">
          <v-card class="login-card elevation-10" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-4">
              Login
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="login" class="pa-4">
                <v-text-field
                  v-model="email"
                  type="email"
                  label="E-mail"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  type="password"
                  label="Senha"
                  prepend-inner-icon="mdi-lock"
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
                  prepend-icon="mdi-login-variant"
                >
                  Entrar
                </v-btn>
              </v-form>
              <v-alert v-if="error" type="error" class="mt-4" variant="tonal">
                {{ error }}
              </v-alert>
              <div class="text-center mt-4">
                <router-link to="/forgot-password" class="text-decoration-none secondary--text">
                  Esqueci minha senha
                </router-link>
              </div>
              <div class="text-center mt-2">
                <router-link to="/register" class="text-decoration-none secondary--text">
                  Não tem conta? Registre-se
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
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      loading: false,
    };
  },
  async created() {
    // Check if user is already logged in
    try {
      const response = await axios.get('/api/');
      if (response.data.authenticated) {
        this.$router.push('/dashboard');
      }
    } catch (err) {
      // Not logged in, stay on login page
    }
  },
  methods: {
    async login() {
      this.loading = true;
      try {
        const response = await axios.post('/api/login', {
          email: this.email,
          password: this.password,
        });
        if (response.data.success) {
          this.$router.push('/dashboard');
        }
      } catch (err) {
        this.error = err.response.data.error;
        setTimeout(() => {
          this.error = '';
        }, 10000);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.login-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-content {
  max-width: 1200px;
}

.login-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.v-btn .v-btn__content {
  align-items: center;
}

@media (max-width: 600px) {
  .login-section {
    padding: 20px;
  }
}
</style>
