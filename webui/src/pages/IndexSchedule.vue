<script lang="ts" setup>
import ScheduleTable from '@/coms/ScheduleTable.vue'
import {onMounted, ref} from 'vue'
import {useRoute} from 'vue-router'
import type {CourseDto} from '@/types/schedule.ts'

const route = useRoute()

const courses = ref<CourseDto[]>([])
const title = ref('')
const subtitle = ref('')

onMounted(() => {
  if (route.query.data) {
    courses.value = JSON.parse(route.query.data as string)
  } else {
    console.warn('🐔 未提供 data query参数，无法渲染课程表》')
  }

  if (route.query.title) title.value = route.query.title as string
  if (route.query.subtitle) subtitle.value = route.query.subtitle as string
})
</script>

<template>
  <schedule-table v-if="courses.length !== 0" :courses :subtitle :title />
</template>

<style scoped></style>
