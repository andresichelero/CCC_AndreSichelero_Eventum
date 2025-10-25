<template>
  <div class="container">
    <h1>Meus Eventos Organizados</h1>
    <p>Esta lista inclui seus eventos publicados e também os rascunhos.</p>

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
            <p>{{ event.description }}</p>
          </div>
          <div class="panel-footer">
            <strong>Status:</strong>
            <span v-if="event.status === 1" class="label label-warning">Rascunho</span>
            <span v-else-if="event.status === 2" class="label label-success">Publicado</span>
            <span v-else class="label label-default">Indefinido</span>

            <router-link :to="`/events/${event.id}/edit`" class="btn btn-primary btn-xs pull-right" style="margin-left: 10px;">Editar</router-link>
            <router-link :to="`/events/${event.id}/manage-schedule`" class="btn btn-info btn-xs pull-right">Gerenciar Programação</router-link>
          </div>
        </div>
      </div>
      <div v-if="events.length === 0" class="col-md-12">
        <p>Você ainda não criou nenhum evento. <router-link to="/events/new">Criar seu primeiro evento?</router-link></p>
      </div>
    </div>
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
  margin-right: 10px;
}

.label-warning {
  background-color: #f0ad4e;
}

.label-success {
  background-color: #5cb85c;
}

.label-default {
  background-color: #777;
}

.btn {
  display: inline-block;
  padding: 1px 5px;
  font-size: 12px;
  line-height: 1.5;
  border-radius: 3px;
  text-decoration: none;
}

.btn-primary {
  color: #fff;
  background-color: #337ab7;
  border-color: #2e6da4;
}

.btn-info {
  color: #fff;
  background-color: #5bc0de;
  border-color: #46b8da;
}

.pull-right {
  float: right;
}
</style>