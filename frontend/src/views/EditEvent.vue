<template>
  <div class="container">
    <div class="row">
      <div class="col-md-8 col-md-offset-2">
        <h1>Editar Evento</h1>
        <form @submit.prevent="updateEvent" novalidate>
          <div class="form-group">
            <label for="title">Título do Evento</label>
            <input v-model="form.title" id="title" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="description">Descrição</label>
            <textarea v-model="form.description" id="description" class="form-control" rows="4"></textarea>
          </div>
          <div class="form-group">
            <label for="start_date">Data de Início</label>
            <input v-model="form.start_date" id="start_date" type="datetime-local" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="end_date">Data de Fim</label>
            <input v-model="form.end_date" id="end_date" type="datetime-local" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="inscription_start_date">Início das Inscrições</label>
            <input v-model="form.inscription_start_date" id="inscription_start_date" type="datetime-local" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="inscription_end_date">Fim das Inscrições</label>
            <input v-model="form.inscription_end_date" id="inscription_end_date" type="datetime-local" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="submission_start_date">Início das Submissões</label>
            <input v-model="form.submission_start_date" id="submission_start_date" type="datetime-local" class="form-control">
          </div>
          <div class="form-group">
            <label for="submission_end_date">Fim das Submissões</label>
            <input v-model="form.submission_end_date" id="submission_end_date" type="datetime-local" class="form-control">
          </div>
          <div class="form-group">
            <label for="status">Status</label>
            <select v-model="form.status" id="status" class="form-control" required>
              <option value="1">Rascunho</option>
              <option value="2">Publicado</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Salvar Alterações</button>
        </form>
        <p v-if="error" class="text-danger">{{ error }}</p>
        <p v-if="message" class="text-success">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EditEvent',
  props: ['id'],
  data() {
    return {
      form: {
        title: '',
        description: '',
        start_date: '',
        end_date: '',
        inscription_start_date: '',
        inscription_end_date: '',
        submission_start_date: '',
        submission_end_date: '',
        status: '1'
      },
      error: '',
      message: ''
    }
  },
  async created() {
    try {
      const response = await axios.get(`/api/events/${this.id}`)
      const event = response.data.event
      this.form = {
        title: event.title,
        description: event.description,
        start_date: event.start_date.slice(0, 16), // for datetime-local
        end_date: event.end_date.slice(0, 16),
        inscription_start_date: event.inscription_start_date.slice(0, 16),
        inscription_end_date: event.inscription_end_date.slice(0, 16),
        submission_start_date: event.submission_start_date ? event.submission_start_date.slice(0, 16) : '',
        submission_end_date: event.submission_end_date ? event.submission_end_date.slice(0, 16) : '',
        status: event.status.toString()
      }
    } catch (err) {
      console.error(err)
    }
  },
  methods: {
    async updateEvent() {
      // Convert datetime-local to ISO format
      const data = { ...this.form }
      data.start_date = new Date(data.start_date).toISOString()
      data.end_date = new Date(data.end_date).toISOString()
      data.inscription_start_date = new Date(data.inscription_start_date).toISOString()
      data.inscription_end_date = new Date(data.inscription_end_date).toISOString()
      if (data.submission_start_date) data.submission_start_date = new Date(data.submission_start_date).toISOString()
      if (data.submission_end_date) data.submission_end_date = new Date(data.submission_end_date).toISOString()

      try {
        const response = await axios.put(`/api/events/${this.id}`, data)
        this.message = response.data.message
        this.$router.push(`/events/${this.id}`)
      } catch (err) {
        this.error = err.response.data.error
      }
    }
  }
}
</script>

<style scoped>
</style>