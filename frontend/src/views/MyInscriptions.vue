<template>
  <div class="inscriptions-section">
    <v-container>
      <h1 class="text-h4 text-center primary--text font-weight-bold mb-6">
        <v-icon size="32" class="me-2">mdi-calendar-check</v-icon>
        Minhas Inscrições
      </h1>
      <v-row v-if="events.length > 0">
        <v-col
          v-for="event in events"
          :key="event.id"
          cols="12"
          md="6"
          lg="4"
        >
          <v-card class="inscription-card elevation-4" color="rgba(255,255,255,0.95)" hover>
            <v-card-title class="primary--text">
              <v-icon class="me-2">mdi-calendar</v-icon>
              <router-link :to="`/events/${event.id}`" class="text-decoration-none primary--text">
                {{ event.title }}
              </router-link>
            </v-card-title>
            <v-card-text>
              <div class="mb-2">
                <v-icon small class="me-1">mdi-calendar-range</v-icon>
                <strong>De:</strong> {{ formatDate(event.start_date) }} <strong>a</strong> {{ formatDate(event.end_date) }}
              </div>
              <p>
                <v-icon small class="me-1">mdi-account</v-icon>
                <strong>Organizado por:</strong> {{ event.organizer.name }}
              </p>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                @click="unsubscribe(event.id)"
                color="error"
                variant="outlined"
                size="small"
                prepend-icon="mdi-close-circle"
              >
                Cancelar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <div v-else class="text-center py-8">
        <v-icon size="64" color="grey">mdi-calendar-blank-outline</v-icon>
        <h3 class="mt-4">Você ainda não se inscreveu em nenhum evento.</h3>
        <p class="text-body-1 mb-4">Explore os eventos disponíveis e faça sua inscrição!</p>
        <v-btn
          to="/events"
          color="primary"
          variant="elevated"
          size="large"
          prepend-icon="mdi-calendar-multiple"
        >
          Ver Eventos Disponíveis
        </v-btn>
      </div>
    </v-container>
  </div>
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
.inscriptions-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px 0;
}

.inscription-card {
  border-radius: 12px;
  transition: transform 0.2s;
}

.inscription-card:hover {
  transform: translateY(-4px);
}

@media (max-width: 600px) {
  .inscriptions-section {
    padding: 10px;
  }
}
</style>