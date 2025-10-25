<template>
  <v-container>
    <v-card-title class="text-h4">Minhas Inscrições</v-card-title>
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
            <p><strong>Organizado por:</strong> {{ event.organizer.name }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="unsubscribe(event.id)" color="error" size="small">
              Cancelar Inscrição
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col v-if="events.length === 0" cols="12">
        <p>Você ainda não se inscreveu em nenhum evento.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MyInscriptions',
  data() {
    return {
      events: []
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/my-inscriptions')
      this.events = response.data.events
    } catch (err) {
      console.error(err)
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR')
    },
    async unsubscribe(eventId) {
      if (confirm('Tem certeza que deseja cancelar sua inscrição neste evento?')) {
        try {
          await axios.delete(`/api/events/${eventId}/inscribe`)
          // Refresh list
          this.events = this.events.filter(e => e.id !== eventId)
        } catch (err) {
          console.error(err)
        }
      }
    }
  }
}
</script>

<style scoped>
</style>