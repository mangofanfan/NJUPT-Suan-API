<script lang="ts" setup>
import ScheduleDescription from '@/pages/ScheduleDescription.vue'
import ScheduleQuery from '@/pages/ScheduleQuery.vue'

defineOptions({
  name: 'Schedule',
})
</script>

<template>
  <div id="schedule-container">
    <n-h2 prefix="bar">课表管理</n-h2>
    <n-p>可以设置 API 以及 MCP 如何获取你的课表数据。</n-p>

    <schedule-description />

    <schedule-query />
  </div>
</template>

<style scoped></style>
