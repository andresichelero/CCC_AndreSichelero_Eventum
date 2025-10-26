<template>
  <div class="hero-section">
    <v-container class="hero-content">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" md="8" lg="6">
          <v-card class="hero-card elevation-10" color="rgba(255,255,255,0.9)">
            <v-card-title
              class="text-h3 text-center primary--text font-weight-bold"
            >
              Bem-vindo ao Eventum
            </v-card-title>
            <v-card-subtitle class="text-h6 text-center secondary--text mb-4">
              Gerencie seus eventos de forma fácil e eficiente
            </v-card-subtitle>
            <v-card-text class="text-center">
              <p class="body-1 mb-6">
                Organize conferências, workshops e muito mais com nossa
                plataforma intuitiva.
              </p>
              <v-row justify="center">
                <v-col cols="12" sm="6">
                  <v-btn
                    to="/login"
                    color="primary"
                    size="large"
                    block
                    class="mb-3"
                    prepend-icon="mdi-login"
                  >
                    Entrar
                  </v-btn>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-btn
                    to="/register"
                    color="secondary"
                    size="large"
                    block
                    variant="outlined"
                    prepend-icon="mdi-account-plus"
                  >
                    Registrar
                  </v-btn>
                </v-col>
              </v-row>
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
  name: "Home",
  async created() {
    try {
      const response = await axios.get("/api/");
      if (response.data.authenticated) {
        this.$router.push("/dashboard");
      }
    } catch (err) {
      console.error(err);
    }
  },
};
</script>

<style scoped>
.hero-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  max-width: 1200px;
}

.hero-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 600px) {
  .hero-section {
    padding: 20px;
  }
}
</style>