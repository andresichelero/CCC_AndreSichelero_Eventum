<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h4">Welcome to Eventum</v-card-title>
          <v-card-text>
            <p>Manage your events easily.</p>
            <v-btn to="/login" color="primary" class="mr-2">Login</v-btn>
            <v-btn to="/register" color="secondary">Register</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Home'
}
</script>