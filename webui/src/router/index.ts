import {createRouter, createWebHashHistory} from 'vue-router'
import Overview from '@/pages/Overview.vue'
import Schedule from '@/pages/Schedule.vue'
import Log from '@/pages/Log.vue'
import Style from '@/pages/Style.vue'
import Config from '@/pages/Config.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Overview, name: 'Overview' },
    { path: '/schedule', component: Schedule, name: 'Schedule' },
    { path: '/style', component: Style, name: 'Style' },
    { path: '/log', component: Log, name: 'Log' },
    { path: '/config', component: Config, name: 'Config' },
  ],
})

export default router
