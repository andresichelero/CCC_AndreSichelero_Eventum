<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="text-h4">Submeter Trabalho para o Evento:</v-card-title>
          <v-card-subtitle>{{ event.title }}</v-card-subtitle>
          <v-card-text>
            <v-form @submit.prevent="submitWork" enctype="multipart/form-data">
              <v-text-field
                v-model="form.title"
                label="Título do Trabalho"
                required
              ></v-text-field>
              <v-file-input
                v-model="form.file"
                label="Arquivo do Trabalho (PDF, DOCX, etc.)"
                accept=".pdf,.doc,.docx,.odt,.rtf"
                required
                @change="onFileChange"
              ></v-file-input>
              <v-btn type="submit" color="primary" block>Enviar Submissão</v-btn>
            </v-form>
            <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
            <v-alert v-if="message" type="success" class="mt-4">{{ message }}</v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SubmissionForm',
  props: ['id'],
  data() {
    return {
      event: {},
      form: {
        title: '',
        file: null
      },
      error: '',
      message: ''
    }
  },
  async created() {
    try {
      const response = await axios.get(`/api/events/${this.id}`)
      this.event = response.data.event
    } catch (err) {
      console.error(err)
    }
  },
  methods: {
    onFileChange(event) {
      this.form.file = event.target.files[0]
    },
    async submitWork() {
      const formData = new FormData()
      formData.append('title', this.form.title)
      formData.append('file', this.form.file)

      try {
        const response = await axios.post(`/api/events/${this.id}/submit`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        this.message = response.data.message
        this.$router.push('/my-submissions')
      } catch (err) {
        this.error = err.response.data.error
      }
    }
  }
}
</script>