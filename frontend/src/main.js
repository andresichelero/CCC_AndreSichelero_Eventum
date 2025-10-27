import 'vuetify/styles';
import { createApp } from 'vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { pt } from 'vuetify/locale';
import App from './App.vue';
import router from './router';
import axios from 'axios';

const vuetify = createVuetify({
  components,
  directives,
  locale: {
    locale: 'pt',
    messages: { pt },
  },
  theme: {
    defaultTheme: 'light',
  },
});

axios.defaults.withCredentials = true;

// Global error handler for Vue
const app = createApp(App);
app.config.errorHandler = (err, instance, info) => {
  console.error('Erro global do Vue:', err, info);
  // You can emit an event or use a global store to show user error
  // For now, log it
};

// Axios interceptors for error handling
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('Erro de resposta:', error.response.status, error.response.data);
      // Show user-friendly message
      const message = getFriendlyErrorMessage(error.response.status, error.response.data);
      window.showError(message);
    } else if (error.request) {
      // Request made but no response
      console.error('Erro de requisição:', error.request);
      window.showError('Erro de conexão. Verifique sua internet.');
    } else {
      // Something else
      console.error('Erro:', error.message);
      window.showError('Ocorreu um erro inesperado.');
    }
    return Promise.reject(error);
  }
);

function getFriendlyErrorMessage(status, data) {
  switch (status) {
    case 400:
      return 'Dados inválidos. Verifique as informações e tente novamente.';
    case 401:
      return 'Não autorizado. Faça login novamente.';
    case 403:
      return 'Acesso negado.';
    case 404:
      return 'Página ou recurso não encontrado.';
    case 500:
      return 'Erro interno do servidor. Tente novamente mais tarde.';
    default:
      return data?.message || 'Ocorreu um erro. Tente novamente.';
  }
}

window.showError = function (message) {
  document.dispatchEvent(new CustomEvent('show-error', { detail: message }));
};

app.use(router).use(vuetify).mount('#app');
