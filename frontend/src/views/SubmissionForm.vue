<template>
  <div class="submission-section">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card class="submission-card elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-2">
              <v-icon size="32" class="me-2">mdi-file-plus</v-icon>
              Submeter Trabalho
            </v-card-title>
            <v-card-subtitle class="text-center secondary--text mb-4">{{
              event.title
            }}</v-card-subtitle>
            <v-card-text class="pa-6">
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SubmissionForm',
  props: ['id'],
  data() {
    return {
      event: {},
      form: {
        title: '',
        file: null,
      },
      error: '',
      message: '',
    };
  },
  async created() {
    try {
      const response = await axios.get(`/api/events/${this.id}`);
      this.event = response.data.event;
    } catch (err) {
      console.error(err);
    }
  },
  methods: {
    onFileChange(event) {
      this.form.file = event.target.files[0];
    },
    async submitWork() {
      const formData = new FormData();
      formData.append('title', this.form.title);
      formData.append('file', this.form.file);

      try {
        const response = await axios.post(`/api/events/${this.id}/submit`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.message = response.data.message;
        this.$router.push('/my-submissions');
      } catch (err) {
        this.error = err.response.data.error;
      }
    },
  },
};
</script>

<style scoped>
.submission-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px 0;
}

.submission-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 600px) {
  .submission-section {
    padding: 10px;
  }
}
</style>
