<template>
  <v-container>
    <v-card-title class="text-h4">Meus Eventos Organizados</v-card-title>
    <p>Esta lista inclui seus eventos publicados e também os rascunhos.</p>
    <v-row>
      <v-col
        v-for="event in events"
        :key="event.id"
        cols="12"
      >
        <v-card class="mb-4">
          <v-card-title>
            <router-link :to="`/events/${event.id}`">{{ event.title }}</router-link>
          </v-card-title>
          <v-card-text>
            <p><strong>Data:</strong> de {{ formatDate(event.start_date) }} a {{ formatDate(event.end_date) }}</p>
            <p>{{ event.description }}</p>
          </v-card-text>
          <v-card-actions>
            <strong>Status:</strong>
            <v-chip
              :color="event.status === 1 ? 'warning' : 'success'"
              size="small"
              class="ml-2"
            >
              {{ event.status === 1 ? 'Rascunho' : 'Publicado' }}
            </v-chip>
            <v-spacer></v-spacer>
            <v-btn :to="`/events/${event.id}/edit`" color="primary" size="small" class="mr-2">Editar</v-btn>
            <v-btn :to="`/events/${event.id}/manage-schedule`" color="info" size="small">Gerenciar Programação</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col v-if="events.length === 0" cols="12">
        <p>Você ainda não criou nenhum evento. <router-link to="/events/new">Criar seu primeiro evento?</router-link></p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MyOrganizedEvents',
  data() {
    return {
      events: []
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/my-organized-events')
      this.events = response.data.events
    } catch (err) {
      console.error(err)
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR')
    }
  }
}
</script>

<style scoped>
</style>