<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title class="text-h4">Olá, {{ user.name }}!</v-card-title>
      <v-card-subtitle>Bem-vindo(a) ao seu dashboard.</v-card-subtitle>
    </v-card>

    <v-row>
      <v-col v-if="user.role === 1" cols="12" md="6">
        <v-card>
          <v-card-title>Eventos que organizo</v-card-title>
          <v-card-text>
            <v-list v-if="organizedEvents.length > 0">
              <v-list-item
                v-for="event in organizedEvents"
                :key="event.id"
                :to="`/events/${event.id}`"
              >
                <v-list-item-title>{{ event.title }}</v-list-item-title>
                <v-list-item-subtitle>Data: {{ formatDate(event.start_date) }}</v-list-item-subtitle>
                <template #append>
                  <v-chip
                    :color="event.status === 1 ? 'warning' : 'success'"
                    size="small"
                  >
                    {{ event.status === 1 ? 'Rascunho' : 'Publicado' }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
            <p v-else>
              Você ainda não organizou nenhum evento.
              <router-link to="/events/new">Criar um evento?</router-link>
            </p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Minhas Próximas Inscrições</v-card-title>
          <v-card-text>
            <v-list v-if="inscribedEvents.length > 0">
              <v-list-item
                v-for="event in inscribedEvents"
                :key="event.id"
                :to="`/events/${event.id}`"
              >
                <v-list-item-title>{{ event.title }}</v-list-item-title>
                <v-list-item-subtitle>Organizado por: {{ event.organizer.name }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <p v-else>
              Você não está inscrito em nenhum evento.
              <router-link to="/events">Ver eventos?</router-link>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="user.role === 2">
      <v-col cols="12">
        <v-card>
          <v-card-title>Minhas Submissões</v-card-title>
          <v-card-text>
            <v-data-table
              v-if="submissions.length > 0"
              :headers="submissionHeaders"
              :items="submissions"
              item-key="id"
            >
              <template v-slot:item.event="{ item }">
                <router-link :to="`/events/${item.event.id}`">{{ item.event.title }}</router-link>
              </template>
              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="getStatusColor(item.status)"
                  size="small"
                >
                  {{ getStatusText(item.status) }}
                </v-chip>
              </template>
            </v-data-table>
            <p v-else>Você ainda não enviou nenhum trabalho.</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="user.role === 3">
      <v-col cols="12">
        <v-card>
          <v-card-title>Próximos Eventos Públicos</v-card-title>
          <v-card-text>
            <v-list v-if="upcomingEvents.length > 0">
              <v-list-item
                v-for="event in upcomingEvents"
                :key="event.id"
                :to="`/events/${event.id}`"
              >
                <v-list-item-title>{{ event.title }}</v-list-item-title>
                <v-list-item-subtitle>
                  Data: {{ formatDate(event.start_date) }} - Organizado por: {{ event.organizer.name }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <p v-else>Não há eventos públicos futuros no momento.</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
    }
  }
}
</script>

<style scoped>
/* Add some basic styling to match Bootstrap classes */
.list-group-item {
  display: block;
  padding: 10px 15px;
  margin-bottom: -1px;
  background-color: #fff;
  border: 1px solid #ddd;
  text-decoration: none;
  color: inherit;
}

.list-group-item:hover {
  background-color: #f5f5f5;
}

.label {
  display: inline;
  padding: .2em .6em .3em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  color: #fff;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: .25em;
}

.label-warning {
  background-color: #f0ad4e;
}

.label-success {
  background-color: #5cb85c;
}

.label-info {
  background-color: #5bc0de;
}

.label-danger {
  background-color: #d9534f;
}

.label-default {
  background-color: #777;
}

.pull-right {
  float: right;
}

.table {
  width: 100%;
  margin-bottom: 20px;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 8px;
  line-height: 1.42857143;
  vertical-align: top;
  border-top: 1px solid #ddd;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f9f9f9;
}
</style>