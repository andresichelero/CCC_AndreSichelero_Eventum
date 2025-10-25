<template>
  <div class="container">
    <div class="page-header">
      <h1>Gerenciar Programação</h1>
      <h3>Evento: {{ event.title }}</h3>
    </div>

    <div class="row">
      <div class="col-md-4">
        <h4>Adicionar Nova Atividade</h4>
        <p><strong>Período do Evento:</strong> {{ formatDateTime(event.start_date) }} até {{ formatDateTime(event.end_date) }}</p>
        <form @submit.prevent="addActivity">
          <div class="form-group">
            <label for="title">Título da Atividade</label>
            <input v-model="form.title" id="title" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="description">Descrição</label>
            <textarea v-model="form.description" id="description" class="form-control" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label for="start_time">Horário de Início</label>
            <input v-model="form.start_time" id="start_time" type="datetime-local" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="end_time">Horário de Fim</label>
            <input v-model="form.end_time" id="end_time" type="datetime-local" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="location">Local</label>
            <input v-model="form.location" id="location" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-primary">Salvar Atividade</button>
        </form>
        <p v-if="error" class="text-danger">{{ error }}</p>
        <p v-if="message" class="text-success">{{ message }}</p>
      </div>
      <div class="col-md-8">
        <h4>Programação Atual</h4>
        <ul v-if="activities.length > 0" class="list-group">
          <li v-for="act in activities" :key="act.id" class="list-group-item">
            <div class="pull-right" style="margin-left: 15px;">
              <button @click="editActivity(act.id)" class="btn btn-primary btn-xs">Editar</button>
              <button @click="deleteActivity(act.id)" class="btn btn-danger btn-xs" style="margin-left: 5px;">Remover</button>
            </div>
            <h5 class="list-group-item-heading"><strong>{{ act.title }}</strong></h5>
            <p class="list-group-item-text">
              <strong>Data e Horário:</strong> {{ formatDateTime(act.start_time) }} - {{ formatTime(act.end_time) }}<br>
              <strong>Local:</strong> {{ act.location }}
            </p>
          </li>
        </ul>
        <p v-else>Nenhuma atividade cadastrada para este evento ainda.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ManageSchedule',
  props: ['id'],
  data() {
    return {
      event: {},
      activities: [],
      form: {
        title: '',
        description: '',
        start_time: '',
        end_time: '',
        location: ''
      },
      error: '',
      message: ''
    }
  },
  async created() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        const response = await axios.get(`/api/events/${this.id}`)
        this.event = response.data.event
        this.activities = response.data.activities
      } catch (err) {
        console.error(err)
      }
    },
    formatDateTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('pt-BR')
    },
    formatTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    },
    async addActivity() {
      const data = { ...this.form }
      data.start_time = new Date(data.start_time).toISOString()
      data.end_time = new Date(data.end_time).toISOString()

      try {
        await axios.post(`/api/events/${this.id}/activities`, data)
        this.message = 'Atividade adicionada com sucesso!'
        this.form = { title: '', description: '', start_time: '', end_time: '', location: '' }
        await this.loadData()
      } catch (err) {
        this.error = err.response.data.error
      }
    },
    editActivity(activityId) {
      // TODO: Implement edit
      alert('Editar atividade não implementado ainda')
    },
    async deleteActivity(activityId) {
      if (confirm('Tem certeza que deseja remover esta atividade?')) {
        try {
          await axios.delete(`/api/activities/${activityId}`)
          await this.loadData()
        } catch (err) {
          console.error(err)
        }
      }
    }
  }
}
</script>

<style scoped>
.form-control {
  display: block;
  width: 100%;
  height: 34px;
  padding: 6px 12px;
  font-size: 14px;
  line-height: 1.42857143;
  color: #555;
  background-color: #fff;
  background-image: none;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea.form-control {
  height: auto;
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

.btn-danger {
  color: #fff;
  background-color: #d9534f;
  border-color: #d43f3a;
}

.list-group-item {
  position: relative;
  display: block;
  padding: 10px 15px;
  margin-bottom: -1px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.list-group-item-heading {
  margin: 0;
  font-size: 16px;
}

.pull-right {
  float: right;
}

.text-danger {
  color: #a94442;
}

.text-success {
  color: #3c763d;
}
</style>