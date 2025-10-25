<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h4">Login</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="email"
                type="email"
                label="Email"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                type="password"
                label="Password"
                required
              ></v-text-field>
              <v-btn type="submit" color="primary" block>Login</v-btn>
            </v-form>
            <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/login', { email: this.email, password: this.password })
        if (response.data.success) {
          this.$router.push('/dashboard')
        }
      } catch (err) {
        this.error = err.response.data.error
      }
    }
  }
}
</script>