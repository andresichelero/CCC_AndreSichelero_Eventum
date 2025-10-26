<template>
  <div class="create-event-section">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card class="create-card elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-4">
              <v-icon size="32" class="me-2">mdi-calendar-plus</v-icon>
              Criar Novo Evento
            </v-card-title>
            <v-card-text class="pa-6">
              <v-form @submit.prevent="createEvent" novalidate>
                <v-text-field
                  v-model="form.title"
                  label="Título do Evento"
                  required
                ></v-text-field>
                <v-textarea
                  v-model="form.description"
                  label="Descrição"
                  rows="4"
                ></v-textarea>
                <v-text-field
                  v-model="form.start_date"
                  type="datetime-local"
                  label="Data de Início"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="form.end_date"
                  type="datetime-local"
                  label="Data de Fim"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="form.inscription_start_date"
                  type="datetime-local"
                  label="Início das Inscrições"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="form.inscription_end_date"
                  type="datetime-local"
                  label="Fim das Inscrições"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="form.submission_start_date"
                  type="datetime-local"
                  label="Início das Submissões"
                ></v-text-field>
                <v-text-field
                  v-model="form.submission_end_date"
                  type="datetime-local"
                  label="Fim das Submissões"
                ></v-text-field>
                <v-select
                  v-model="form.status"
                  :items="statusOptions"
                  label="Status"
                  item-title="text"
                  item-value="value"
                  required
                ></v-select>
                <v-text-field
                  v-model="form.workload"
                  label="Carga de Trabalho (horas)"
                  type="number"
                  min="0"
                  step="0.1"
                ></v-text-field>
                <v-btn type="submit" color="primary" block>Salvar Evento</v-btn>
              </v-form>
              <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
              <v-alert v-if="message" type="success" class="mt-4">{{ message }}</v-alert>
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
  name: 'CreateEvent',
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
        status: '1',
        workload: 0
      },
      error: '',
      message: '',
      statusOptions: [
        { text: 'Rascunho', value: '1' },
        { text: 'Publicado', value: '2' }
      ]
    }
  },
  methods: {
    async createEvent() {
      this.error = ''
      this.message = ''
      const data = { ...this.form }
      console.log('Sending data:', data)

      // Basic validation
      if (!data.title || !data.description || !data.start_date || !data.end_date || 
          !data.inscription_start_date || !data.inscription_end_date || !data.status) {
        this.error = 'Por favor, preencha todos os campos obrigatórios.'
        return
      }

      try {
        const response = await axios.post('/api/events', data)
        this.message = response.data.message
        this.$router.push(`/events/${response.data.event.id}`)
      } catch (err) {
        console.error('Error response:', err.response?.data)
        this.error = err.response?.data?.error || 'Erro ao criar evento.'
      }
    }
  }
}
</script>

<style scoped>
.create-event-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px 0;
}

.create-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 600px) {
  .create-event-section {
    padding: 10px;
  }
}
</style>