<template>
  <div class="register-section">
    <v-container class="register-content">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" md="6" lg="5">
          <v-card
            class="register-card elevation-10"
            color="rgba(255,255,255,0.95)"
          >
            <v-card-title
              class="text-h4 text-center primary--text font-weight-bold mb-4"
            >
              Registrar Nova Conta
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="register" novalidate class="pa-4">
                <v-text-field
                  v-model="name"
                  label="Nome"
                  placeholder="Nome completo"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-text-field
                  v-model="email"
                  type="email"
                  label="E-mail"
                  placeholder="seu@email.com"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-select
                  v-model="role"
                  :items="roleOptions"
                  label="Tipo de Conta"
                  item-title="text"
                  item-value="value"
                  prepend-inner-icon="mdi-account-group"
                  variant="outlined"
                  class="mb-4"
                ></v-select>
                <div class="mt-4">
                  <p class="text-subtitle-1">Vínculo Acadêmico (Opcional)</p>
                  <v-autocomplete
                    v-model="faculdade_id"
                    :items="faculdades"
                    item-title="name"
                    item-value="id"
                    label="Faculdade"
                    clearable
                    filterable
                    variant="outlined"
                    class="mb-4"
                  ></v-autocomplete>
                  <div class="text-center mb-4">
                    <v-btn
                      variant="text"
                      color="secondary"
                      @click="contatoFaculdade"
                    >
                      Sua faculdade não está listada? Fale conosco
                    </v-btn>
                  </div>
                  <v-autocomplete
                    v-model="curso_id"
                    :items="cursos"
                    item-title="name"
                    item-value="id"
                    label="Curso"
                    :disabled="!faculdade_id"
                    clearable
                    filterable
                    variant="outlined"
                    class="mb-4"
                  ></v-autocomplete>
                  <v-autocomplete
                    v-model="turma_id"
                    :items="turmas"
                    item-title="name"
                    item-value="id"
                    label="Turma"
                    :disabled="!curso_id"
                    clearable
                    filterable
                    variant="outlined"
                    class="mb-4"
                  ></v-autocomplete>
                </div>
                <v-text-field
                  v-model="password"
                  type="password"
                  label="Senha"
                  placeholder="Digite sua senha"
                  prepend-inner-icon="mdi-lock"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-text-field
                  v-model="password2"
                  type="password"
                  label="Repetir Senha"
                  placeholder="Confirme sua senha"
                  prepend-inner-icon="mdi-lock-check"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <div class="mb-4">
                  <p class="text-body-2">
                    Por favor, leia e concorde com nossos
                    <router-link
                      to="/termos-de-uso"
                      target="_blank"
                      class="text-decoration-none primary--text"
                      >Termos de Uso</router-link
                    >
                    e
                    <router-link
                      to="/politica-de-privacidade"
                      target="_blank"
                      class="text-decoration-none primary--text"
                      >Política de Privacidade</router-link
                    >
                    antes de continuar.
                  </p>
                  <v-switch
                    v-model="acceptTerms"
                    label="Eu aceito os Termos de Uso e Política de Privacidade"
                    color="primary"
                  ></v-switch>
                </div>
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="loading"
                  prepend-icon="mdi-account-plus"
                >
                  Registrar
                </v-btn>
              </v-form>
              <v-alert v-if="error" type="error" class="mt-4" variant="tonal">
                {{ error }}
              </v-alert>
              <v-alert
                v-if="message"
                type="success"
                class="mt-4"
                variant="tonal"
              >
                {{ message }}
              </v-alert>
              <div class="text-center mt-4">
                <router-link
                  to="/login"
                  class="text-decoration-none secondary--text"
                >
                  Já tem conta? Faça login
                </router-link>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Register",
  data() {
    return {
      name: "",
      email: "",
      password: "",
      password2: "",
      role: "3",
      acceptTerms: false,
      error: "",
      message: "",
      loading: false,
      roleOptions: [
        { text: "Participante", value: "3" },
        { text: "Palestrante/Autor", value: "2" },
        { text: "Organizador", value: "1" },
      ],
      faculdade_id: null,
      curso_id: null,
      turma_id: null,
      faculdades: [],
      cursos: [],
      turmas: [],
    };
  },
  methods: {
    async loadFaculdades() {
      try {
        const response = await axios.get("/api/faculdades");
        this.faculdades = response.data.faculdades;
      } catch (err) {
        console.error("Erro ao carregar faculdades:", err);
      }
    },
    async loadCursos(faculdadeId) {
      if (!faculdadeId) {
        this.cursos = [];
        this.turmas = [];
        this.curso_id = null;
        this.turma_id = null;
        return;
      }
      try {
        const response = await axios.get(
          `/api/cursos?faculdade_id=${faculdadeId}`
        );
        this.cursos = response.data.cursos;
      } catch (err) {
        console.error("Erro ao carregar cursos:", err);
      }
    },
    async loadTurmas(cursoId) {
      if (!cursoId) {
        this.turmas = [];
        this.turma_id = null;
        return;
      }
      try {
        const response = await axios.get(`/api/turmas?curso_id=${cursoId}`);
        this.turmas = response.data.turmas;
      } catch (err) {
        console.error("Erro ao carregar turmas:", err);
      }
    },
    async register() {
      this.error = "";
      this.message = "";
      this.loading = true;
      if (!this.name.trim()) {
        this.error = "Nome é obrigatório";
        this.loading = false;
        return;
      }
      if (!this.email.trim()) {
        this.error = "E-mail é obrigatório";
        this.loading = false;
        return;
      }
      if (!this.password.trim()) {
        this.error = "Senha é obrigatória";
        this.loading = false;
        return;
      }
      if (this.password !== this.password2) {
        this.error = "As senhas não coincidem";
        this.loading = false;
        return;
      }
      if (!this.acceptTerms) {
        this.error = "Você deve aceitar os termos";
        this.loading = false;
        return;
      }
      try {
        const response = await axios.post("/api/register", {
          name: this.name,
          email: this.email,
          password: this.password,
          role: this.role,
          accept_terms: this.acceptTerms,
          faculdade_id: this.faculdade_id,
          curso_id: this.curso_id,
          turma_id: this.turma_id,
        });
        this.message = response.data.message;
        setTimeout(() => {
          this.$router.push("/login");
        }, 2000);
      } catch (err) {
        this.error = err.response.data.error;
      } finally {
        this.loading = false;
      }
    },
    async fetchFaculdades() {
      try {
        const response = await axios.get("/api/faculdades");
        this.faculdades = response.data.faculdades;
      } catch (err) {
        this.error = "Erro ao carregar faculdades";
      }
    },
    async fetchCursos() {
      if (!this.faculdade_id) {
        this.cursos = [];
        this.turmas = [];
        return;
      }
      try {
        const response = await axios.get(
          `/api/cursos?faculdade_id=${this.faculdade_id}`
        );
        this.cursos = response.data.cursos;
        this.turmas = [];
      } catch (err) {
        this.error = "Erro ao carregar cursos";
      }
    },
    async fetchTurmas() {
      if (!this.curso_id) {
        this.turmas = [];
        return;
      }
      try {
        const response = await axios.get(
          `/api/turmas?curso_id=${this.curso_id}`
        );
        this.turmas = response.data.turmas;
      } catch (err) {
        this.error = "Erro ao carregar turmas";
      }
    },
    contatoFaculdade() {
      alert("Entre em contato conosco pelo email: contato@eventum.com");
    },
  },
  created() {
    this.fetchFaculdades();
  },
  watch: {
    faculdade_id() {
      this.fetchCursos();
    },
    curso_id() {
      this.fetchTurmas();
    },
  },
};
</script>

<style scoped>
.register-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-content {
  max-width: 1200px;
}

.register-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.register-card .v-card-text {
  color: rgba(0, 0, 0, 0.87);
}

.register-card .v-checkbox {
  color: rgba(0, 0, 0, 0.87);
}

.register-card .v-checkbox .v-label {
  color: rgba(0, 0, 0, 0.87) !important;
}

.register-card .v-checkbox input[type="checkbox"] {
  accent-color: #1976d2;
}

.register-card a {
  color: #1976d2 !important;
}

.register-card .v-switch .v-label {
  color: rgba(0, 0, 0, 0.87) !important;
}

.register-card .v-switch {
  color: rgba(0, 0, 0, 0.87) !important;
}

.register-card .terms-checkbox .v-label {
  color: black !important;
  font-weight: bold;
}

.terms-checkbox {
  --v-theme-surface: white;
}

.v-btn .v-btn__content {
  align-items: center;
}

.custom-checkbox {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.checkbox-input {
  margin-right: 8px;
  width: 16px;
  height: 16px;
  accent-color: #1976d2;
}

.checkbox-label {
  color: black;
  font-size: 14px;
  cursor: pointer;
}

.register-card .d-flex.align-center {
  width: 100%;
}

.register-card .d-flex.align-center .v-text-field {
  flex: 1;
}

.register-card .d-flex.align-center .v-btn {
  flex-shrink: 0;
  margin-left: 8px;
}

@media (max-width: 600px) {
  .register-section {
    padding: 20px;
  }
}
</style>