<template>
  <div class="container">
    <h1>Minhas Inscrições</h1>

    <div class="row">
      <div v-for="event in events" :key="event.id" class="col-md-12">
        <div class="panel panel-default">
          <div class="panel-heading">
            <h3 class="panel-title">
              <router-link :to="`/events/${event.id}`">{{ event.title }}</router-link>
            </h3>
          </div>
          <div class="panel-body">
            <p><strong>Data:</strong> de {{ formatDate(event.start_date) }} a {{ formatDate(event.end_date) }}</p>
            <p><strong>Organizado por:</strong> {{ event.organizer.name }}</p>
          </div>
          <div class="panel-footer">
            <button @click="unsubscribe(event.id)" class="btn btn-danger btn-xs">
              Cancelar Inscrição
            </button>
          </div>
        </div>
      </div>
      <div v-if="events.length === 0" class="col-md-12">
        <p>Você ainda não se inscreveu em nenhum evento.</p>
      </div>
    </div>
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
.panel {
  margin-bottom: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.panel-heading {
  padding: 10px 15px;
  border-bottom: 1px solid #ddd;
  background-color: #f5f5f5;
}

.panel-title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}

.panel-body {
  padding: 15px;
}

.panel-footer {
  padding: 10px 15px;
  background-color: #f5f5f5;
  border-top: 1px solid #ddd;
}

.btn {
  display: inline-block;
  padding: 1px 5px;
  font-size: 12px;
  line-height: 1.5;
  border-radius: 3px;
}

.btn-danger {
  color: #fff;
  background-color: #d9534f;
  border-color: #d43f3a;
}

.btn-danger:hover {
  background-color: #c9302c;
  border-color: #ac2925;
}
</style>