import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    isAuthenticated: !!localStorage.getItem('user'),
  }),
  
  actions: {
    async login(email, password) {
      try {
        // 1. Realiza o login (cria a sessão no backend)
        await api.post('/api/login', { email, password });
        
        // 2. Busca os dados do usuário logado
        await this.fetchUser();
        
        return true;
      } catch (error) {
        console.error('Login failed', error);
        throw error;
      }
    },

    async fetchUser() {
      try {
        const response = await api.get('/api/');
        if (response.data.authenticated) {
          this.user = response.data.user;
          this.isAuthenticated = true;
          localStorage.setItem('user', JSON.stringify(this.user));
        } else {
          this.user = null;
          this.isAuthenticated = false;
          localStorage.removeItem('user');
        }
      } catch (error) {
        console.error('Error fetching user', error);
        this.user = null;
        this.isAuthenticated = false;
        localStorage.removeItem('user');
      }
    },
    
    async logout() {
      try {
        await api.post('/api/logout');
      } catch (error) {
        console.error('Logout error', error);
      } finally {
        this.user = null;
        this.isAuthenticated = false;
        localStorage.removeItem('user');
      }
    },
    
    async checkAuth() {
      await this.fetchUser();
      return this.isAuthenticated;
    }
  }
});
