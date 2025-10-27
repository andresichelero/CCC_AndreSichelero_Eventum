<template>
  <div class="manage-turmas-section">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card class="manage-card elevation-4" color="rgba(255,255,255,0.95)">
            <v-card-title class="text-h4 text-center primary--text font-weight-bold mb-4">
              <v-icon size="32" class="me-2">mdi-account-group</v-icon>
              Gerenciar Turmas
            </v-card-title>
            <v-card-text class="pa-6">
              <!-- Criar Novo Curso -->
              <v-card outlined class="mb-4">
                <v-card-title>Criar Novo Curso</v-card-title>
                <v-card-text>
                  <v-form @submit.prevent="createCurso">
                    <v-autocomplete
                      v-model="newCurso.faculdade_id"
                      :items="faculdades"
                      item-title="name"
                      item-value="id"
                      label="Faculdade"
                      required
                      searchable
                      auto-select-first="never"
                      :hide-no-data="false"
                      open-on-focus
                    ></v-autocomplete>
                    <v-text-field
                      v-model="newCurso.name"
                      label="Nome do Curso"
                      required
                    ></v-text-field>
                    <v-btn type="submit" color="primary">Criar Curso</v-btn>
                  </v-form>
                </v-card-text>
              </v-card>

              <!-- Criar Nova Turma -->
              <v-card outlined class="mb-4">
                <v-card-title>Criar Nova Turma</v-card-title>
                <v-card-text>
                  <v-form @submit.prevent="createTurma">
                    <v-autocomplete
                      v-model="newTurma.faculdade_id"
                      :items="faculdades"
                      item-title="name"
                      item-value="id"
                      label="Faculdade"
                      @update:modelValue="loadCursos"
                      required
                      searchable
                      auto-select-first="never"
                      :hide-no-data="false"
                      open-on-focus
                    ></v-autocomplete>
                    <v-autocomplete
                      v-model="newTurma.curso_id"
                      :items="cursos"
                      item-title="name"
                      item-value="id"
                      label="Curso"
                      required
                      searchable
                      auto-select-first="never"
                      :hide-no-data="false"
                      open-on-focus
                    ></v-autocomplete>
                    <v-text-field
                      v-model="newTurma.name"
                      label="Nome da Turma"
                      required
                    ></v-text-field>
                    <v-btn type="submit" color="primary">Criar Turma</v-btn>
                  </v-form>
                </v-card-text>
              </v-card>

              <!-- Lista de Turmas -->
              <v-card outlined>
                <v-card-title>Turmas Existentes</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-autocomplete
                        v-model="filterFaculdade"
                        :items="faculdades"
                        item-title="name"
                        item-value="id"
                        label="Filtrar por Faculdade"
                        clearable
                        searchable
                        auto-select-first="never"
                        :hide-no-data="false"
                        open-on-focus
                        @update:modelValue="filterTurmas"
                      ></v-autocomplete>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-autocomplete
                        v-model="filterCurso"
                        :items="filteredCursos"
                        item-title="name"
                        item-value="id"
                        label="Filtrar por Curso"
                        clearable
                        searchable
                        auto-select-first="never"
                        :hide-no-data="false"
                        open-on-focus
                        @update:modelValue="filterTurmas"
                      ></v-autocomplete>
                    </v-col>
                  </v-row>
                  <v-list v-if="filteredTurmas.length > 0">
                    <v-list-item v-for="turma in filteredTurmas" :key="turma.id">
                      <v-list-item-title>{{ turma.name }}</v-list-item-title>
                      <v-list-item-subtitle
                        >Curso: {{ getCursoName(turma.curso_id) }}</v-list-item-subtitle
                      >
                      <template #append>
                        <div class="d-flex flex-column align-end">
                          <v-switch
                            v-model="turma.is_public"
                            label="Pública"
                            @change="updateTurmaPublic(turma)"
                            class="mb-1"
                          ></v-switch>
                          <v-btn icon @click="showManageStudents(turma)" size="small">
                            <v-icon>mdi-account-multiple</v-icon>
                          </v-btn>
                        </div>
                      </template>
                    </v-list-item>
                  </v-list>
                  <div v-else class="text-center py-4">
                    <v-icon size="48" color="grey">mdi-account-group-outline</v-icon>
                    <p class="mt-2">Nenhuma turma criada ainda. Crie uma nova turma acima.</p>
                  </div>
                </v-card-text>
              </v-card>

              <!-- Dialog para Gerenciar Alunos -->
              <v-dialog v-model="manageStudentsDialog" max-width="600px">
                <v-card>
                  <v-card-title>Gerenciar Alunos - {{ selectedTurma?.name }}</v-card-title>
                  <v-card-text>
                    <v-text-field
                      v-model="searchStudent"
                      label="Buscar Aluno"
                      prepend-inner-icon="mdi-magnify"
                    ></v-text-field>
                    <v-list>
                      <v-list-item v-for="user in filteredUsers" :key="user.id">
                        <v-list-item-title>{{ user.name }}</v-list-item-title>
                        <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
                        <template #append>
                          <v-btn
                            v-if="user.turma_id !== selectedTurma.id"
                            color="primary"
                            @click="addStudent(user)"
                          >
                            Adicionar
                          </v-btn>
                          <v-btn v-else color="error" @click="removeStudent(user)"> Remover </v-btn>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="manageStudentsDialog = false">Fechar</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
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
  name: 'ManageTurmas',
  data() {
    return {
      faculdades: [],
      cursos: [],
      turmas: [],
      users: [],
      newTurma: {
        faculdade_id: null,
        curso_id: null,
        name: '',
      },
      newCurso: {
        faculdade_id: null,
        name: '',
      },
      manageStudentsDialog: false,
      selectedTurma: null,
      searchStudent: '',
      filterFaculdade: null,
      filterCurso: null,
    };
  },
  computed: {
    filteredUsers() {
      if (!this.searchStudent) return this.users;
      return this.users.filter(
        (user) =>
          user.name.toLowerCase().includes(this.searchStudent.toLowerCase()) ||
          user.email.toLowerCase().includes(this.searchStudent.toLowerCase())
      );
    },
    filteredTurmas() {
      let filtered = this.turmas;
      if (this.filterFaculdade) {
        filtered = filtered.filter((turma) => {
          const curso = this.cursos.find((c) => c.id === turma.curso_id);
          return curso && curso.faculdade_id === this.filterFaculdade;
        });
      }
      if (this.filterCurso) {
        filtered = filtered.filter((turma) => turma.curso_id === this.filterCurso);
      }
      return filtered;
    },
    filteredCursos() {
      if (!this.filterFaculdade) return this.cursos;
      return this.cursos.filter((curso) => curso.faculdade_id === this.filterFaculdade);
    },
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
        this.newTurma.curso_id = null;
        return;
      }
      try {
        const response = await axios.get(`/api/cursos?faculdade_id=${faculdadeId}`);
        this.cursos = response.data.cursos;
      } catch (err) {
        console.error('Erro ao carregar cursos:', err);
      }
    },
    filterTurmas() {
      if (this.filterFaculdade) {
        this.loadCursos(this.filterFaculdade);
      } else {
        this.cursos = [];
        this.filterCurso = null;
      }
    },
    async loadTurmas() {
      try {
        const response = await axios.get('/api/turmas');
        this.turmas = response.data.turmas;
      } catch (err) {
        console.error('Erro ao carregar turmas:', err);
      }
    },
    async loadUsers() {
      try {
        const response = await axios.get('/api/users');
        this.users = response.data.users;
      } catch (err) {
        console.error('Erro ao carregar usuários:', err);
      }
    },
    async createTurma() {
      try {
        const response = await axios.post('/api/turmas', this.newTurma);
        this.turmas.push(response.data.turma);
        this.newTurma = { faculdade_id: null, curso_id: null, name: '' };
      } catch (err) {
        console.error('Erro ao criar turma:', err);
      }
    },
    async createCurso() {
      try {
        await axios.post('/api/cursos', this.newCurso);
        this.loadCursos(this.newCurso.faculdade_id);
        this.newCurso = { faculdade_id: null, name: '' };
      } catch (err) {
        console.error('Erro ao criar curso:', err);
      }
    },
    async updateTurmaPublic(turma) {
      try {
        await axios.put(`/api/turmas/${turma.id}`, { is_public: turma.is_public });
      } catch (err) {
        console.error('Erro ao atualizar turma:', err);
      }
    },
    showManageStudents(turma) {
      this.selectedTurma = turma;
      this.loadUsers();
      this.manageStudentsDialog = true;
    },
    async addStudent(user) {
      try {
        await axios.post(`/api/turmas/${this.selectedTurma.id}/add_student`, { user_id: user.id });
        user.turma_id = this.selectedTurma.id;
      } catch (err) {
        console.error('Erro ao adicionar aluno:', err);
      }
    },
    async removeStudent(user) {
      try {
        await axios.post(`/api/turmas/${this.selectedTurma.id}/remove_student`, {
          user_id: user.id,
        });
        user.turma_id = null;
      } catch (err) {
        console.error('Erro ao remover aluno:', err);
      }
    },
    getCursoName(cursoId) {
      const curso = this.cursos.find((c) => c.id === cursoId);
      return curso ? curso.name : 'Desconhecido';
    },
  },
  async created() {
    try {
      const response = await axios.get('/api/');
      if (response.data.authenticated && (response.data.user.role === 1 || response.data.user.role === 4)) {
        this.loadFaculdades();
        this.loadTurmas();
      } else {
        this.$router.push('/dashboard');
      }
    } catch (err) {
      this.$router.push('/login');
    }
  },
};
</script>

<style scoped>
.manage-turmas-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px 0;
}

.manage-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 600px) {
  .manage-turmas-section {
    padding: 10px;
  }
}
</style>
