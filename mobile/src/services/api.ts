import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

// Em um ambiente real, isso seria uma variável de ambiente
// Para Android Emulator use 'http://10.0.2.2:5000'
// Para iOS Simulator ou Web use 'http://localhost:5000'
const API_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar o token em todas as requisições
api.interceptors.request.use(
  (config) => {
    // Com autenticação via sessão (cookies), não precisamos injetar token manualmente
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar erros de resposta (ex: 401)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore();
    
    if (error.response && error.response.status === 401) {
      // Token expirado ou inválido
      await authStore.logout();
      // Redirecionar para login seria feito no router ou aqui se tiver acesso
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
