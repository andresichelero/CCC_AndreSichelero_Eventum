<template>
  <div class="edit-event-section">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card class="edit-card elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-4">
              <v-icon size="32" class="me-2">mdi-calendar-edit</v-icon>
              Editar Evento
            </v-card-title>
            <v-card-text class="pa-6">
              <v-alert v-if="eventStarted" type="warning" class="mb-4">
                Este evento já começou e não pode ser editado.
              </v-alert>
              <v-form @submit.prevent="updateEvent" novalidate>
                <v-text-field v-model="form.title" label="Título do Evento" required></v-text-field>
                <v-textarea v-model="form.description" label="Descrição" rows="4"></v-textarea>
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
                <v-autocomplete
                  v-model="form.faculdade_id"
                  :items="faculdades"
                  item-title="name"
                  item-value="id"
                  label="Faculdade Organizadora (Opcional)"
                  clearable
                  searchable
                  auto-select-first="never"
                  :hide-no-data="false"
                  open-on-focus
                ></v-autocomplete>
                <v-autocomplete
                  v-model="form.curso_id"
                  :items="cursos"
                  item-title="name"
                  item-value="id"
                  label="Curso Organizador (Opcional)"
                  clearable
                  searchable
                ></v-autocomplete>
                <v-btn type="submit" color="primary" block :disabled="eventStarted"
                  >Salvar Alterações</v-btn
                >
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
import axios from 'axios';

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
        status: '1',
        workload: 0,
        faculdade_id: null,
        curso_id: null,
      },
      error: '',
      message: '',
      faculdades: [],
      cursos: [],
      statusOptions: [
        { text: 'Rascunho', value: '1' },
        { text: 'Publicado', value: '2' },
      ],
      eventStarted: false,
    };
  },
  async created() {
    await this.loadFaculdades();
    try {
      const response = await axios.get(`/api/events/${this.id}`);
      const event = response.data.event;
      this.form = {
        title: event.title,
        description: event.description,
        start_date: event.start_date.slice(0, 16), // datetime-local
        end_date: event.end_date.slice(0, 16),
        inscription_start_date: event.inscription_start_date.slice(0, 16),
        inscription_end_date: event.inscription_end_date.slice(0, 16),
        submission_start_date: event.submission_start_date
          ? event.submission_start_date.slice(0, 16)
          : '',
        submission_end_date: event.submission_end_date
          ? event.submission_end_date.slice(0, 16)
          : '',
        status: event.status.toString(),
        workload: event.workload,
        faculdade_id: event.faculdade_id,
        curso_id: event.curso_id,
      };
      if (this.form.faculdade_id) {
        await this.loadCursos(this.form.faculdade_id);
      }
      // Verificar se o evento já começou
      this.eventStarted = new Date(event.start_date) <= new Date();
    } catch (err) {
      console.error(err);
    }
  },
  methods: {
    async loadFaculdades() {
      try {
        const response = await axios.get('/api/faculdades');
        this.faculdades = response.data.faculdades;
      } catch (err) {
        console.error('Erro ao carregar faculdades:', err);
      }
    },
    async loadCursos(faculdadeId) {
      if (!faculdadeId) {
        this.cursos = [];
        this.form.curso_id = null;
        return;
      }
      try {
        const response = await axios.get(`/api/cursos?faculdade_id=${faculdadeId}`);
        this.cursos = response.data.cursos;
      } catch (err) {
        console.error('Erro ao carregar cursos:', err);
      }
    },
    async updateEvent() {
      // Converte datetime-local para o formato ISO
      const data = { ...this.form };
      data.start_date = new Date(data.start_date).toISOString().replace('Z', '+00:00');
      data.end_date = new Date(data.end_date).toISOString().replace('Z', '+00:00');
      data.inscription_start_date = new Date(data.inscription_start_date)
        .toISOString()
        .replace('Z', '+00:00');
      data.inscription_end_date = new Date(data.inscription_end_date)
        .toISOString()
        .replace('Z', '+00:00');
      if (data.submission_start_date)
        data.submission_start_date = new Date(data.submission_start_date)
          .toISOString()
          .replace('Z', '+00:00');
      if (data.submission_end_date)
        data.submission_end_date = new Date(data.submission_end_date)
          .toISOString()
          .replace('Z', '+00:00');

      try {
        const response = await axios.put(`/api/events/${this.id}`, data);
        this.message = response.data.message;
        setTimeout(() => { this.message = ''; }, 10000);
        this.$router.push(`/events/${this.id}`);
      } catch (err) {
        console.error('Erro ao atualizar evento:', err);
        let errorMsg = 'Erro ao atualizar evento.';
        if (err.response && err.response.data) {
          errorMsg = err.response.data.error || errorMsg;
          if (err.response.data.details) {
            errorMsg += ' Detalhes: ' + err.response.data.details;
          }
        }
        this.error = errorMsg;
        setTimeout(() => { this.error = ''; }, 10000);
      }
    },
  },
  watch: {
    'form.faculdade_id': function (newId) {
      this.loadCursos(newId);
    },
  },
};
</script>

<style scoped>
.edit-event-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0 20px 0;
}

.edit-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 600px) {
  .edit-event-section {
    padding: 2rem 10px 10px 10px;
  }
}
</style>
