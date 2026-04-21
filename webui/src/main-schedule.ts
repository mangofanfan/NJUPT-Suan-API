import {createApp} from 'vue'

import '@/assets/style.css'

import AppSchedule from '@/AppSchedule.vue'
import scheduleRouter from '@/router/index-schedule.ts'

const app = createApp(AppSchedule)
app.use(scheduleRouter)

app.mount('#app')
