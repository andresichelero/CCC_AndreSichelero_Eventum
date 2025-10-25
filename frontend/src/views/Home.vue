<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h4">Bem-vindo ao Eventum</v-card-title>
          <v-card-text>
            <p>Gerencie seus eventos facilmente.</p>
            <v-btn to="/login" color="primary" class="mr-2">Login</v-btn>
            <v-btn to="/register" color="secondary">Registrar</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  async created() {
    try {
      const response = await axios.get('/api/')
      if (response.data.authenticated) {
        this.$router.push('/dashboard')
      }
    } catch (err) {
      console.error(err)
    }
  }
}
</script>