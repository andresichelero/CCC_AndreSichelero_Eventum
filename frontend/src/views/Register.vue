<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h4">Registrar Nova Conta</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="register" novalidate>
              <v-text-field
                v-model="name"
                label="Nome"
                placeholder="Nome"
                required
              ></v-text-field>
              <v-text-field
                v-model="email"
                type="email"
                label="Email"
                placeholder="Email"
                required
              ></v-text-field>
              <v-select
                v-model="role"
                :items="roleOptions"
                label="Tipo de Conta"
                item-title="text"
                item-value="value"
              ></v-select>
              <v-text-field
                v-model="password"
                type="password"
                label="Senha"
                placeholder="Senha"
                required
              ></v-text-field>
              <v-text-field
                v-model="password2"
                type="password"
                label="Repetir Senha"
                placeholder="Repetir Senha"
                required
              ></v-text-field>
              <p>
                Por favor, leia e concorde com nossos
                <router-link to="/termos-de-uso" target="_blank">Termos de Uso</router-link> e
                <router-link to="/politica-de-privacidade" target="_blank">Política de Privacidade</router-link> antes de continuar.
              </p>
              <v-checkbox
                v-model="acceptTerms"
                label="Eu aceito os Termos de Uso e Política de Privacidade"
                required
              ></v-checkbox>
              <v-btn type="submit" color="primary" block>Registrar</v-btn>
            </v-form>
            <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
            <v-alert v-if="message" type="success" class="mt-4">{{ message }}</v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
      roleOptions: [
        { text: 'Participante', value: '3' },
        { text: 'Palestrante/Autor', value: '2' },
        { text: 'Organizador', value: '1' }
      ]
    }
  },
  methods: {
    async register() {
      if (this.password !== this.password2) {
        this.error = 'As senhas não coincidem'
        return
      }
      if (!this.acceptTerms) {
        this.error = 'Você deve aceitar os termos'
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
        this.$router.push('/login')
      } catch (err) {
        this.error = err.response.data.error
      }
    }
  }
}
</script>

<style scoped>
.v-container {
  max-width: 600px;
  margin: 0 auto;
}

.text-h4 {
  text-align: center;
}

.mt-4 {
  margin-top: 16px !important;
}

.mb-4 {
  margin-bottom: 16px !important;
}
</style>