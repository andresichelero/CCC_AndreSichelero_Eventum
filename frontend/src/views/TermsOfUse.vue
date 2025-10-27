<template>
  <div class="container">
    <h1>Termos de Uso</h1>
    <div v-html="content"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TermsOfUse',
  data() {
    return {
      content: '',
    };
  },
  async created() {
    try {
      const response = await axios.get('/api/termos-de-uso');
      this.content = response.data.content;
    } catch (err) {
      console.error(err);
    }
  },
};
</script>
