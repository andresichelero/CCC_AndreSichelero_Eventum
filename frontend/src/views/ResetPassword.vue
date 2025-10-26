<template>
  <div class="reset-section">
    <v-container class="reset-content">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" md="6" lg="4">
          <v-card
            class="reset-card elevation-10"
            color="rgba(255,255,255,0.95)"
          >
            <v-card-title
              class="text-h4 text-center primary--text font-weight-bold mb-4"
            >
              <v-icon size="32" class="me-2">mdi-lock-reset</v-icon>
              Redefinir Senha
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="resetPassword" class="pa-4">
                <v-text-field
                  v-model="password"
                  type="password"
                  label="Nova Senha"
                  prepend-inner-icon="mdi-lock"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-text-field
                  v-model="password2"
                  type="password"
                  label="Repetir Nova Senha"
                  prepend-inner-icon="mdi-lock-check"
                  variant="outlined"
                  required
                  class="mb-4"
                ></v-text-field>
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="loading"
                  prepend-icon="mdi-lock-reset"
                >
                  Redefinir Senha
                </v-btn>
              </v-form>
              <v-alert
                v-if="message"
                type="success"
                class="mt-4"
                variant="tonal"
              >
                {{ message }}
              </v-alert>
              <v-alert v-if="error" type="error" class="mt-4" variant="tonal">
                {{ error }}
              </v-alert>
              <div class="text-center mt-4">
                <router-link
                  to="/login"
                  class="text-decoration-none secondary--text"
                >
                  Voltar ao Login
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
  name: "ResetPassword",
  data() {
    return {
      password: "",
      password2: "",
      error: "",
      message: "",
      loading: false,
    };
  },
  created() {
    if (!this.$route.query.token) {
      this.$router.push("/login");
    }
  },
  methods: {
    async resetPassword() {
      if (this.password !== this.password2) {
        this.error = "As senhas não coincidem";
        return;
      }
      this.loading = true;
      this.error = "";
      this.message = "";
      try {
        const response = await axios.post("/api/reset-password", {
          token: this.$route.query.token,
          password: this.password,
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
  },
};
</script>

<style scoped>
.reset-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.reset-content {
  max-width: 1200px;
}

.reset-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.v-btn .v-btn__content {
  align-items: center;
}

@media (max-width: 600px) {
  .reset-section {
    padding: 20px;
  }
}
</style>