<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title class="text-h4">Gerenciar Programação</v-card-title>
      <v-card-subtitle>Evento: {{ event.title }}</v-card-subtitle>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <h5>{{ editing ? 'Editar Atividade' : 'Adicionar Nova Atividade' }}</h5>
            <p><strong>Período do Evento:</strong> {{ formatDateTime(event.start_date) }} até {{ formatDateTime(event.end_date) }}</p>
            <div>
              <v-text-field
                v-model="form.title"
                label="Título da Atividade"
                required
              ></v-text-field>
              <v-textarea
                v-model="form.description"
                label="Descrição"
                rows="3"
              ></v-textarea>
              <v-text-field
                v-model="form.start_time"
                type="datetime-local"
                label="Horário de Início"
                required
              ></v-text-field>
              <v-text-field
                v-model="form.end_time"
                type="datetime-local"
                label="Horário de Fim"
                required
              ></v-text-field>
              <v-text-field
                v-model="form.location"
                label="Local"
                required
              ></v-text-field>
              <v-btn @click="addActivity" color="primary" block>{{ editing ? 'Salvar Alterações' : 'Salvar Atividade' }}</v-btn>
              <v-btn v-if="editing" @click="cancelEdit" color="secondary" block class="mt-2">Cancelar</v-btn>
            </div>
            <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
            <v-alert v-if="message" type="success" class="mt-4">{{ message }}</v-alert>
          </v-col>
          <v-col cols="12" md="8">
            <h5>Programação Atual</h5>
            <div v-if="activities.length > 0">
              <v-row>
                <v-col cols="12" v-for="act in activities" :key="act.id">
                  <v-card class="mb-2">
                    <v-card-title>{{ act.title }}</v-card-title>
                    <v-card-text>
                      <strong>Data/Horário:</strong> {{ formatDateTime(act.start_time) }} - {{ formatTime(act.end_time) }}<br>
                      <strong>Local:</strong> {{ act.location }}
                    </v-card-text>
                    <v-card-actions>
                      <v-btn @click="editActivity(act.id)" color="primary" size="small">Editar</v-btn>
                      <v-btn @click="deleteActivity(act.id)" color="error" size="small">Remover</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </div>
            <p v-else>Nenhuma atividade cadastrada para este evento ainda.</p>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
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
      editing: false,
      editingId: null,
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
      this.error = ''
      this.message = ''

      if (!data.title || !data.start_time || !data.end_time || !data.location) {
        this.error = 'Por favor, preencha todos os campos obrigatórios.'
        return
      }

      try {
        data.start_time = data.start_time.length === 16 ? data.start_time + ':00' : data.start_time
        data.end_time = data.end_time.length === 16 ? data.end_time + ':00' : data.end_time
      } catch (e) {
        this.error = 'Data/hora inválida.'
        return
      }

      try {
        if (this.editing) {
          await axios.put(`/api/activities/${this.editingId}`, data)
          this.message = 'Atividade atualizada com sucesso!'
        } else {
          await axios.post(`/api/events/${this.id}/activities`, data)
          this.message = 'Atividade adicionada com sucesso!'
        }
        this.form = { title: '', description: '', start_time: '', end_time: '', location: '' }
        this.editing = false
        this.editingId = null
        await this.loadData()
      } catch (err) {
        this.error = err.response?.data?.error || 'Erro ao adicionar atividade.'
      }
    },
    editActivity(activityId) {
      const act = this.activities.find(a => a.id === activityId)
      if (act) {
        this.form = {
          title: act.title,
          description: act.description,
          start_time: new Date(act.start_time).toISOString().slice(0, 16),
          end_time: new Date(act.end_time).toISOString().slice(0, 16),
          location: act.location
        }
        this.editing = true
        this.editingId = activityId
      }
    },
    async updateActivity() {
      const data = { ...this.form }
      data.start_time = new Date(data.start_time).toISOString()
      data.end_time = new Date(data.end_time).toISOString()

      try {
        await axios.put(`/api/activities/${this.editingId}`, data)
        this.message = 'Atividade atualizada com sucesso!'
        this.form = { title: '', description: '', start_time: '', end_time: '', location: '' }
        this.editing = false
        this.editingId = null
        await this.loadData()
      } catch (err) {
        this.error = err.response.data.error
      }
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
    },
    cancelEdit() {
      this.form = { title: '', description: '', start_time: '', end_time: '', location: '' }
      this.editing = false
      this.editingId = null
      this.error = ''
      this.message = ''
    }
  }
}
</script>

<style scoped>
</style>