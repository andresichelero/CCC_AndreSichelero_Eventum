<template>
  <v-app>
    <v-app-bar v-if="isAuthenticated" app color="primary">
      <v-toolbar-title>Eventum</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/events" variant="text">Eventos</v-btn>
      <v-btn v-if="user && user.role === 1" to="/events/new" variant="text">Novo Evento</v-btn>
      <v-spacer></v-spacer>
      <span v-if="user" class="mr-4">Olá, {{ user.name }}</span>
      <v-btn v-if="user && user.role === 2" to="/my-submissions" variant="text">Minhas Submissões</v-btn>
      <v-btn v-if="user" to="/my-inscriptions" variant="text">Minhas Inscrições</v-btn>
      <v-btn v-if="user && user.role === 1" to="/my-organized-events" variant="text">Meus Eventos</v-btn>
      <v-btn v-if="user" @click="logout" variant="text">Logout</v-btn>
      <template v-else>
        <v-btn to="/login" variant="text">Login</v-btn>
        <v-btn to="/register" variant="text">Registrar</v-btn>
      </template>
    </v-app-bar>
    <v-main>
      <v-container v-if="isAuthenticated" fluid>
        <v-row v-if="messages.length > 0">
          <v-col cols="12">
            <v-alert v-for="message in messages" :key="message.id" type="info" dismissible>{{ message }}</v-alert>
          </v-col>
        </v-row>
      </v-container>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      isAuthenticated: false,
      user: null,
      messages: []
    }
  },
  async created() {
    await this.checkAuth()
  },
  methods: {
    async checkAuth() {
      try {
        const response = await axios.get('/api/')
        if (response.data.authenticated) {
          this.isAuthenticated = true
          this.user = response.data.user
        } else {
          this.isAuthenticated = false
          this.user = null
        }
      } catch (err) {
        console.error(err)
        this.isAuthenticated = false
        this.user = null
      }
    },
    async logout() {
      try {
        await axios.post('/api/logout')
        this.isAuthenticated = false
        this.user = null
        this.$router.push('/login')
      } catch (err) {
        console.error(err)
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>