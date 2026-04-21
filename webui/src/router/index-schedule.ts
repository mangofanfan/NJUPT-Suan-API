import {createRouter, createWebHashHistory} from 'vue-router'
import IndexSchedule from '@/pages/IndexSchedule.vue'

const scheduleRouter = createRouter({
  history: createWebHashHistory(),
  routes: [{ path: '/', component: IndexSchedule }],
})

export default scheduleRouter
