<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app temporary :width="280">
      <v-list>
        <v-list-item v-if="isAuthenticated" to="/events">
          <v-list-item-title>Eventos</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAuthenticated && user && user.role === 1" to="/events/new">
          <v-list-item-title>Novo Evento</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAuthenticated && user && user.role === 2" to="/my-submissions">
          <v-list-item-title>Minhas Submissões</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAuthenticated" to="/my-inscriptions">
          <v-list-item-title>Minhas Inscrições</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAuthenticated && user && user.role === 1" to="/my-organized-events">
          <v-list-item-title>Meus Eventos</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAuthenticated" to="/profile">
          <v-list-item-title>Meu Perfil</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAuthenticated" @click="logout">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="!isAuthenticated" to="/login">
          <v-list-item-title>Login</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="!isAuthenticated" to="/register">
          <v-list-item-title>Registrar</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" height="64">
      <v-app-bar-nav-icon @click="drawer = !drawer" class="d-md-none"></v-app-bar-nav-icon>
      <v-toolbar-title>
        <v-btn variant="text" class="text-white" @click="$router.push('/dashboard')">
          EVENTUM
        </v-btn>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="d-none d-md-flex">
        <v-btn v-if="isAuthenticated" to="/events" variant="text">Eventos</v-btn>
        <v-btn v-if="isAuthenticated && user && user.role === 1" to="/events/new" variant="text"
          >Novo Evento</v-btn
        >
        <v-spacer></v-spacer>
        <v-btn v-if="isAuthenticated && user && user.role === 2" to="/my-submissions" variant="text"
          >Minhas Submissões</v-btn
        >
        <v-btn v-if="isAuthenticated" to="/my-inscriptions" variant="text">Minhas Inscrições</v-btn>
        <v-btn
          v-if="isAuthenticated && user && user.role === 1"
          to="/my-organized-events"
          variant="text"
          >Meus Eventos</v-btn
        >
        <v-btn v-if="isAuthenticated" to="/profile" variant="text">Meu Perfil</v-btn>
        <v-btn v-if="isAuthenticated" @click="logout" variant="text">Logout</v-btn>
        <v-btn v-if="!isAuthenticated" to="/login" variant="text">Login</v-btn>
        <v-btn v-if="!isAuthenticated" to="/register" variant="text">Registrar</v-btn>
      </div>
    </v-app-bar>
    <v-main>
      <v-container v-if="isAuthenticated" fluid>
        <v-row v-if="messages.length > 0">
          <v-col cols="12">
            <v-alert v-for="message in messages" :key="message.id" type="info" dismissible>{{
              message
            }}</v-alert>
          </v-col>
        </v-row>
      </v-container>
      <router-view />
    </v-main>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout">
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="snackbar.show = false"> Fechar </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      isAuthenticated: false,
      user: null,
      messages: [],
      drawer: false,
      snackbar: {
        show: false,
        text: '',
        color: 'error',
        timeout: 6000,
      },
    };
  },
  async created() {
    await this.checkAuth();
    document.addEventListener('show-error', (e) => this.showError(e.detail));
  },
  watch: {
    $route() {
      this.checkAuth();
    },
  },
  methods: {
    async checkAuth() {
      try {
        const response = await axios.get('/api/');
        if (response.data.authenticated) {
          this.isAuthenticated = true;
          this.user = response.data.user;
        } else {
          this.isAuthenticated = false;
          this.user = null;
        }
      } catch (err) {
        console.error(err);
        this.isAuthenticated = false;
        this.user = null;
      }
    },
    async logout() {
      try {
        await axios.post('/api/logout');
        this.isAuthenticated = false;
        this.user = null;
        this.$router.push('/login');
      } catch (err) {
        console.error(err);
      }
    },
    showError(message) {
      this.snackbar.text = message;
      this.snackbar.show = true;
    },
  },
};
</script>

<style>
#app {
  font-family: 'Noto Sans', sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #333;
}

.v-main {
  background: transparent !important;
}

.v-container {
  background: transparent !important;
  padding: 0 !important;
  max-width: none !important;
}

/* Performance optimizations */
.v-app-bar {
  transition: all 0.3s ease;
}

.v-navigation-drawer {
  transition: all 0.3s ease;
}

/* Responsive design */
@media (max-width: 960px) {
  .v-app-bar .v-toolbar-title {
    font-size: 1rem;
  }
}

@media (max-width: 600px) {
  .v-app-bar {
    height: 56px !important;
  }
}
</style>
