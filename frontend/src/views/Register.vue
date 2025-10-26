<template>
  <div class="register-section">
    <v-container class="register-content">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" md="6" lg="5">
          <v-card class="register-card elevation-10" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-4">
              <v-icon size="32" class="me-2">mdi-account-plus</v-icon>
              Registrar Nova Conta
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="register" novalidate class="pa-4">
                <v-text-field
                  v-model="name"
                  label="Nome"
                  placeholder="Nome completo"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-text-field
                  v-model="email"
                  type="email"
                  label="E-mail"
                  placeholder="seu@email.com"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-select
                  v-model="role"
                  :items="roleOptions"
                  label="Tipo de Conta"
                  item-title="text"
                  item-value="value"
                  prepend-inner-icon="mdi-account-group"
                  variant="outlined"
                  class="mb-4"
                ></v-select>
                <v-text-field
                  v-model="password"
                  type="password"
                  label="Senha"
                  placeholder="Digite sua senha"
                  prepend-inner-icon="mdi-lock"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-text-field
                  v-model="password2"
                  type="password"
                  label="Repetir Senha"
                  placeholder="Confirme sua senha"
                  prepend-inner-icon="mdi-lock-check"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <div class="mb-4">
                  <p class="text-body-2">
                    Por favor, leia e concorde com nossos
                    <router-link to="/termos-de-uso" target="_blank" class="text-decoration-none primary--text">Termos de Uso</router-link> e
                    <router-link to="/politica-de-privacidade" target="_blank" class="text-decoration-none primary--text">Política de Privacidade</router-link> antes de continuar.
                  </p>
                  <v-checkbox
                    v-model="acceptTerms"
                    label="Eu aceito os Termos de Uso e Política de Privacidade"
                    color="primary"
                  ></v-checkbox>
                </div>
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="loading"
                  prepend-icon="mdi-account-plus"
                >
                  Registrar
                </v-btn>
              </v-form>
              <v-alert v-if="error" type="error" class="mt-4" variant="tonal">
                {{ error }}
              </v-alert>
              <v-alert v-if="message" type="success" class="mt-4" variant="tonal">
                {{ message }}
              </v-alert>
              <div class="text-center mt-4">
                <router-link to="/login" class="text-decoration-none secondary--text">
                  Já tem conta? Faça login
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
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      password2: '',
      role: '3',
      acceptTerms: false,
      error: '',
      message: '',
      loading: false,
      roleOptions: [
        { text: 'Participante', value: '3' },
        { text: 'Palestrante/Autor', value: '2' },
        { text: 'Organizador', value: '1' }
      ]
    }
  },
  methods: {
    async register() {
      this.error = ''
      this.message = ''
      this.loading = true
      if (this.password !== this.password2) {
        this.error = 'As senhas não coincidem'
        this.loading = false
        return
      }
      if (!this.acceptTerms) {
        this.error = 'Você deve aceitar os termos'
        this.loading = false
        return
      }
      try {
        const response = await axios.post('/api/register', {
          name: this.name,
          email: this.email,
          password: this.password,
          role: this.role,
          accept_terms: this.acceptTerms
        })
        this.message = response.data.message
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      } catch (err) {
        this.error = err.response.data.error
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-content {
  max-width: 1200px;
}

.register-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.v-btn .v-btn__content {
  align-items: center;
}

@media (max-width: 600px) {
  .register-section {
    padding: 20px;
  }
}
</style>