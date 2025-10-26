<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h5">Meu Perfil</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="user.name"
              label="Nome"
              readonly
              disabled
            ></v-text-field>
            <v-text-field
              v-model="user.email"
              label="Email"
              readonly
              disabled
            ></v-text-field>

            <v-divider class="my-4"></v-divider>
            
            <v-switch
              v-model="form.allow_public_profile"
              label="Habilitar perfil público"
              color="primary"
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
          this.form.allow_public_profile = response.data.user.allow_public_profile
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