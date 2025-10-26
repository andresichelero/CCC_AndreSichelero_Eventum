<template>
  <div class="my-events-section">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card class="my-events-card elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-4">
              <v-icon size="32" class="me-2">mdi-calendar-star</v-icon>
              Meus Eventos Organizados
            </v-card-title>
            <v-card-text class="pa-6">
              <p class="text-center mb-4">Esta lista inclui seus eventos publicados e também os rascunhos.</p>
              <v-row>
                <v-col
                  v-for="event in events"
                  :key="event.id"
                  cols="12"
                >
                  <v-card class="mb-4 event-card" variant="outlined">
                    <v-card-title>
                      <router-link :to="`/events/${event.id}`" class="event-link">{{ event.title }}</router-link>
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
                  <p class="text-center">Você ainda não criou nenhum evento. <router-link to="/events/new" class="primary--text">Criar seu primeiro evento?</router-link></p>
                </v-col>
              </v-row>
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
.my-events-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px 0;
}

.my-events-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.event-link {
  text-decoration: none;
  color: inherit;
}

.event-link:hover {
  color: #1976d2;
}

.event-card {
  border-radius: 12px;
}

@media (max-width: 600px) {
  .my-events-section {
    padding: 10px;
  }
}
</style>