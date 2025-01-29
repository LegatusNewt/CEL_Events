import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createPinia } from 'pinia'
import { Quasar } from 'quasar'
import CalendarPlugin from '@quasar/quasar-ui-qcalendar/QCalendarAgenda'
import '@quasar/quasar-ui-qcalendar/dist/index.css'
import { useEventsStore } from './stores/events'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/dist/quasar.css'


// Create pinia state store
const pinia = createPinia()
const app = createApp(App)

// Add plugins
app.use(Quasar)
app.use(CalendarPlugin)
app.use(pinia)

const eventStore = useEventsStore()
app.mount('#app')

