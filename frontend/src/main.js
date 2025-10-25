import 'vuetify/styles'
import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const vuetify = createVuetify({
  components,
  directives,
})

axios.defaults.withCredentials = true

createApp(App).use(router).use(vuetify).mount('#app')