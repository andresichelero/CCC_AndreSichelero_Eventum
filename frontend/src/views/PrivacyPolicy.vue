<template>
  <div class="container">
    <h1>Política de Privacidade</h1>
    <div v-html="content"></div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PrivacyPolicy',
  data() {
    return {
      content: ''
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/politica-de-privacidade')
      this.content = response.data.content
    } catch (err) {
      console.error(err)
    }
  }
}
</script>