<template>
  <div class="dashboard-container">
    <v-container>
      <v-card class="welcome-card mb-6 elevation-4" color="primary" dark>
        <v-card-title class="text-h4">
          <v-icon class="me-3">mdi-account-circle</v-icon>
          Olá, {{ user.name }}!
        </v-card-title>
        <v-card-subtitle class="text-h6">Bem-vindo(a) ao seu dashboard.</v-card-subtitle>
      </v-card>

      <v-row>
        <v-col v-if="user.role === 1" cols="12" md="6">
          <v-card class="elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="primary--text">
              <v-icon class="me-2">mdi-calendar-star</v-icon>
              Eventos que organizo
            </v-card-title>
            <v-card-text>
              <v-list v-if="organizedEvents.length > 0" density="comfortable">
                <v-list-item
                  v-for="event in organizedEvents"
                  :key="event.id"
                  :to="`/events/${event.id}`"
                  class="mb-2 rounded"
                >
                  <template #prepend>
                    <v-icon color="primary">mdi-calendar</v-icon>
                  </template>
                  <v-list-item-title>{{ event.title }}</v-list-item-title>
                  <v-list-item-subtitle>Data: {{ formatDate(event.start_date) }}</v-list-item-subtitle>
                  <template #append>
                    <v-chip
                      :color="event.status === 1 ? 'warning' : 'success'"
                      size="small"
                      variant="elevated"
                    >
                      {{ event.status === 1 ? 'Rascunho' : 'Publicado' }}
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
              <div v-else class="text-center py-4">
                <v-icon size="48" color="grey">mdi-calendar-blank</v-icon>
                <p class="mt-2">Você ainda não organizou nenhum evento.</p>
                <v-btn color="primary" variant="outlined" to="/events/new" class="mt-2">
                  Criar um evento
                </v-btn>
                <v-btn color="secondary" variant="outlined" to="/manage-turmas" class="mt-2 ml-2">
                  Gerenciar Turmas
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card class="elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="primary--text">
              <v-icon class="me-2">mdi-calendar-check</v-icon>
              Minhas Próximas Inscrições
            </v-card-title>
            <v-card-text>
              <v-list v-if="inscribedEvents.length > 0" density="comfortable">
                <v-list-item
                  v-for="event in inscribedEvents"
                  :key="event.id"
                  :to="`/events/${event.id}`"
                  class="mb-2 rounded"
                >
                  <template #prepend>
                    <v-icon color="secondary">mdi-calendar</v-icon>
                  </template>
                  <v-list-item-title>{{ event.title }}</v-list-item-title>
                  <v-list-item-subtitle>Organizado por: {{ event.organizer.name }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <div v-else class="text-center py-4">
                <v-icon size="48" color="grey">mdi-calendar-blank-outline</v-icon>
                <p class="mt-2">Você não está inscrito em nenhum evento.</p>
                <v-btn color="secondary" variant="outlined" to="/events" class="mt-2">
                  Ver eventos
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-if="user.role === 2">
        <v-col cols="12">
          <v-card class="elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="primary--text">
              <v-icon class="me-2">mdi-file-document</v-icon>
              Minhas Submissões
            </v-card-title>
            <v-card-text>
              <v-data-table
                v-if="submissions.length > 0"
                :headers="submissionHeaders"
                :items="submissions"
                item-key="id"
                density="comfortable"
                class="elevation-1"
              >
                <template #item.event="{ item }">
                  <router-link :to="`/events/${item.event.id}`" class="text-decoration-none primary--text">
                    {{ item.event.title }}
                  </router-link>
                </template>
                <template #item.status="{ item }">
                  <v-chip
                    :color="getStatusColor(item.status)"
                    size="small"
                    variant="elevated"
                  >
                    {{ getStatusText(item.status) }}
                  </v-chip>
                </template>
              </v-data-table>
              <div v-else class="text-center py-4">
                <v-icon size="48" color="grey">mdi-file-document-outline</v-icon>
                <p class="mt-2">Você ainda não enviou nenhum trabalho.</p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-if="user.role === 3">
        <v-col cols="12">
          <v-card class="elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="primary--text">
              <v-icon class="me-2">mdi-calendar-multiple</v-icon>
              Próximos Eventos Públicos
            </v-card-title>
            <v-card-text>
              <v-list v-if="upcomingEvents.length > 0" density="comfortable">
                <v-list-item
                  v-for="event in upcomingEvents"
                  :key="event.id"
                  :to="`/events/${event.id}`"
                  class="mb-2 rounded"
                >
                  <template #prepend>
                    <v-icon color="accent">mdi-calendar</v-icon>
                  </template>
                  <v-list-item-title>{{ event.title }}</v-list-item-title>
                  <v-list-item-subtitle>
                    Data: {{ formatDate(event.start_date) }} - Organizado por: {{ event.organizer.name }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <div v-else class="text-center py-4">
                <v-icon size="48" color="grey">mdi-calendar-blank-multiple</v-icon>
                <p class="mt-2">Não há eventos públicos futuros no momento.</p>
              </div>
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
  name: 'Dashboard',
  data() {
    return {
      user: {},
      inscribedEvents: [],
      submissions: [],
      organizedEvents: [],
      upcomingEvents: [],
      submissionHeaders: [
        { title: 'Trabalho', key: 'title' },
        { title: 'Evento', key: 'event' },
        { title: 'Status', key: 'status' }
      ]
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/')
      if (response.data.authenticated) {
        this.user = response.data.user
        this.inscribedEvents = response.data.data.inscribed_events
        this.submissions = response.data.data.submissions
        this.organizedEvents = response.data.data.organized_events
        this.upcomingEvents = response.data.data.upcoming_events
      } else {
        this.$router.push('/login')
      }
    } catch (err) {
      console.error(err)
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR')
    },
    getStatusColor(status) {
      switch (status) {
        case 1: return 'info'
        case 3: return 'success'
        case 4: return 'error'
        default: return 'default'
      }
    },
    getStatusText(status) {
      switch (status) {
        case 1: return 'Submetido'
        case 3: return 'Aprovado'
        case 4: return 'Rejeitado'
        default: return 'Em avaliação'
      }
    },
    async logout() {
      try {
        await axios.post('/api/logout')
        this.$router.push('/')
      } catch (err) {
        console.error(err)
      }
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding-top: 2rem;
}
</style>