<template>
  <div class="profile-section">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card class="profile-card elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-4">
              <v-icon size="32" class="me-2">mdi-account-circle</v-icon>
              Meu Perfil
            </v-card-title>
            <v-card-text class="pa-6">
              <v-text-field
                v-model="form.name"
                label="Nome"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                class="mb-4"
              ></v-text-field>
              <v-text-field
                v-model="form.email"
                label="E-mail"
                type="email"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                class="mb-4"
              ></v-text-field>

              <v-divider class="my-4"></v-divider>
              
              <v-switch
                v-model="form.allow_public_profile"
                label="Habilitar perfil público"
                color="primary"
                class="mb-2"
              ></v-switch>
              <p class="text-caption">
                Ao habilitar, seu nome será listado na seção "Quem Vai"
                dos eventos em que você está inscrito (visível apenas para 
                outros participantes inscritos).
              </p>

              <v-alert v-if="message" type="success" class="mt-4">{{ message }}</v-alert>
              <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>

            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="saveSettings">Salvar Alterações</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Profile',
  data() {
    return {
      user: {
        name: '',
        email: ''
      },
      form: {
        name: '',
        email: '',
        allow_public_profile: false
      },
      message: '',
      error: ''
    }
  },
  async created() {
    await this.loadUserData()
  },
  methods: {
    async loadUserData() {
      try {
        // Reutiliza a API do dashboard para pegar dados do usuário
        const response = await axios.get('/api/')
        if (response.data.authenticated) {
          this.user = response.data.user
          this.form = { ...this.form, ...response.data.user }
        } else {
          this.$router.push('/login')
        }
      } catch (err) {
        this.error = 'Erro ao carregar dados do perfil.'
        console.error(err)
      }
    },
    async saveSettings() {
      this.message = ''
      this.error = ''
      try {
        await axios.put('/api/me/settings', this.form)
        this.message = 'Configurações salvas com sucesso!'
      } catch (err) {
        this.error = err.response?.data?.error || 'Erro ao salvar configurações.'
        console.error(err)
      }
    }
  }
}
</script>

<style scoped>
.profile-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px 0;
}

.profile-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 600px) {
  .profile-section {
    padding: 10px;
  }
}
</style>