<script setup lang="ts">
defineProps<{
  type: 'Tool' | 'Resource' | 'Prompt'
  name: string
  description: string
}>()
</script>

<template>
  <n-card>
    <template #header>
      <n-flex>
        <n-tag type="primary">{{ type }}</n-tag>
        <n-tag type="info">{{ name }}</n-tag>
        <n-text strong>{{ description }}</n-text>
      </n-flex>
    </template>
    <template #default>
      <slot />
    </template>
  </n-card>
</template>

<style scoped></style>
