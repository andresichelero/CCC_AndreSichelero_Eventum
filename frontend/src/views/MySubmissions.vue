<template>
  <div class="container">
    <h1>Minhas Submissões</h1>

    <div class="row">
      <div v-for="sub in submissions" :key="sub.id" class="col-md-12">
        <div class="panel panel-default">
          <div class="panel-heading">
            <h3 class="panel-title">{{ sub.title }}</h3>
          </div>
          <div class="panel-body">
            <p><strong>Evento:</strong> <router-link :to="`/events/${sub.event_id}`">{{ sub.event.title }}</router-link></p>
            <p><strong>Arquivo:</strong> 
              <a :href="`/api/submissions/${sub.id}/download`" target="_blank">{{ sub.file_path }}</a>
            </p>
          </div>
          <div class="panel-footer">
            <span v-if="sub.status === 1" class="label label-info">Submetido</span>
            <span v-else-if="sub.status === 3" class="label label-success">Aprovado</span>
            <span v-else-if="sub.status === 4" class="label label-danger">Rejeitado</span>
            <span v-else class="label label-default">Em avaliação</span>
          </div>
        </div>
      </div>
      <div v-if="submissions.length === 0" class="col-md-12">
        <p>Você ainda não submeteu nenhum trabalho.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MySubmissions',
  data() {
    return {
      submissions: []
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/my-submissions')
      this.submissions = response.data.submissions
    } catch (err) {
      console.error(err)
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
}

.label-info {
  background-color: #5bc0de;
}

.label-success {
  background-color: #5cb85c;
}

.label-danger {
  background-color: #d9534f;
}

.label-default {
  background-color: #777;
}
</style>