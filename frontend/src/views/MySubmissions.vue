<template>
  <div class="my-submissions-section">
    <v-container>
      <v-card-title class="text-h4">Minhas Submissões</v-card-title>
      <v-row>
        <v-col v-for="sub in submissions" :key="sub.id" cols="12">
          <v-card class="mb-4">
            <v-card-title>{{ sub.title }}</v-card-title>
            <v-card-text>
              <p>
                <strong>Evento:</strong>
                <router-link :to="`/events/${sub.event_id}`">{{ sub.event.title }}</router-link>
              </p>
              <p>
                <strong>Arquivo:</strong>
                <a :href="`/api/submissions/${sub.id}/download`" target="_blank">{{
                  sub.file_path
                }}</a>
              </p>
            </v-card-text>
            <v-card-actions>
              <v-chip :color="getStatusColor(sub.status)" size="small">
                {{ getStatusText(sub.status) }}
              </v-chip>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col v-if="submissions.length === 0" cols="12">
          <p>Você ainda não submeteu nenhum trabalho.</p>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MySubmissions',
  data() {
    return {
      submissions: [],
    };
  },
  async created() {
    try {
      const response = await axios.get('/api/my-submissions');
      this.submissions = response.data.submissions;
    } catch (err) {
      console.error(err);
    }
  },
  methods: {
    getStatusColor(status) {
      switch (status) {
        case 1:
          return 'info';
        case 3:
          return 'success';
        case 4:
          return 'error';
        default:
          return 'default';
      }
    },
    getStatusText(status) {
      switch (status) {
        case 1:
          return 'Submetido';
        case 3:
          return 'Aprovado';
        case 4:
          return 'Rejeitado';
        default:
          return 'Em avaliação';
      }
    },
  },
};
</script>

<style scoped>
.my-submissions-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0 20px 0;
}

@media (max-width: 600px) {
  .my-submissions-section {
    padding: 2rem 10px 10px 10px;
  }
}
</style>

<style scoped></style>
