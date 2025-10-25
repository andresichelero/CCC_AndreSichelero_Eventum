<template>
  <v-container>
    <v-card-title class="text-h4">Próximos Eventos</v-card-title>

    <v-row>
      <v-col
        v-for="event in events"
        :key="event.id"
        cols="12"
      >
        <v-card>
          <v-card-title>{{ event.title }}</v-card-title>
          <v-card-text>
            <p><strong>Organizado por:</strong> {{ event.organizer.name }}</p>
            <p><strong>Data:</strong> de {{ formatDate(event.start_date) }} a {{ formatDate(event.end_date) }}</p>
            <p>{{ event.description }}</p>
            <v-btn :to="`/events/${event.id}`" color="primary">Ver Evento</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="events.length === 0" cols="12">
        <p>Nenhum evento cadastrado no momento.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Events',
  data() {
    return {
      events: []
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/events')
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