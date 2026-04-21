<script lang="ts" setup></script>

<template>
  <n-config-provider
    :theme-overrides="{
      common: {
        fontFamily: 'Maple Mono CN, sans-serif',
        fontFamilyMono: 'Maple Mono CN, monospace',
        fontWeightStrong: '700',
        fontWeight: '500',
      },
    }"
  >
    <router-view />
    <n-global-style />
  </n-config-provider>
</template>

<style scoped></style>
