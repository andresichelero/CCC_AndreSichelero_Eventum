<template>
  <div class="events-section">
    <v-container>
      <v-card class="elevation-4" color="rgba(255,255,255,0.95)">
        <v-card-title class="text-h4 primary--text font-weight-bold">
          <v-icon size="32" class="me-2">mdi-calendar-multiple</v-icon>
          Próximos Eventos
        </v-card-title>
        <v-card-text>
          <v-row v-if="events.length > 0">
            <v-col v-for="event in events" :key="event.id" cols="12" md="6" lg="4">
              <v-card class="event-card elevation-4" color="rgba(255,255,255,0.95)" hover>
                <v-card-title class="primary--text">
                  <v-icon class="me-2">mdi-calendar-star</v-icon>
                  {{ event.title }}
                </v-card-title>
                <v-card-subtitle class="secondary--text">
                  Organizado por: {{ event.organizer.name }}
                </v-card-subtitle>
                <v-card-text>
                  <div class="mb-2">
                    <v-icon small class="me-1">mdi-calendar-range</v-icon>
                    <strong>De:</strong> {{ formatDate(event.start_date) }} <strong>a</strong>
                    {{ formatDate(event.end_date) }}
                  </div>
                  <p class="text-body-2 mb-4">{{ truncateDescription(event.description) }}</p>
                  <v-btn
                    :to="`/events/${event.id}`"
                    color="primary"
                    variant="elevated"
                    prepend-icon="mdi-eye"
                    block
                  >
                    Ver Evento
                  </v-btn>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <div v-else class="text-center py-8">
            <v-icon size="64" color="grey">mdi-calendar-blank-multiple</v-icon>
            <h3 class="mt-4">Nenhum evento cadastrado no momento.</h3>
            <p class="text-body-1">Volte em breve para ver os próximos eventos!</p>
          </div>
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Events',
  data() {
    return {
      events: [],
    };
  },
  async created() {
    try {
      const response = await axios.get('/api/events');
      this.events = response.data.events;
    } catch (err) {
      console.error(err);
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR');
    },
    truncateDescription(description) {
      if (!description) return '';
      return description.length > 150 ? description.substring(0, 150) + '...' : description;
    },
  },
};
</script>

<style scoped>
.events-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0 20px 0;
}

.event-card {
  border-radius: 12px;
  transition: transform 0.2s;
}

.event-card:hover {
  transform: translateY(-4px);
}

@media (max-width: 600px) {
  .events-section {
    padding: 2rem 10px 10px 10px;
  }
}
</style>
