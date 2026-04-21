<script setup lang="ts">
defineProps<{
  method: 'GET' | 'POST'
  path: string
  description: string
}>()
</script>

<template>
  <n-card>
    <template #header>
      <n-flex>
        <n-tag type="primary">{{ method }}</n-tag>
        <n-tag type="info">{{ path }}</n-tag>
        <n-text strong>{{ description }}</n-text>
      </n-flex>
    </template>
    <template #default>
      <slot />
    </template>
  </n-card>
</template>

<style scoped></style>
