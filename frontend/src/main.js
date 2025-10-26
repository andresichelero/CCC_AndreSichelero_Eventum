import 'vuetify/styles'
import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { pt } from 'vuetify/locale'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const vuetify = createVuetify({
  components,
  directives,
  locale: {
    locale: 'pt',
    messages: { pt },
  },
  theme: {
    defaultTheme: 'light'
  }
})

axios.defaults.withCredentials = true

createApp(App).use(router).use(vuetify).mount('#app')