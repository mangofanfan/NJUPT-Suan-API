<script lang="ts" setup></script>

<template>
  <div id="nav-container">
    <div id="nav-title">
      <n-h3 class="no-margin-bottom">NJUPT Suan API</n-h3>
    </div>
    <n-button secondary type="primary">概览</n-button>
    <n-button secondary type="info">GitHub</n-button>
    <n-button secondary type="error">芒果</n-button>
  </div>
</template>

<style scoped>
#nav-container {
  display: flex;
  flex-direction: row;
  max-width: 100vw;
  align-items: center;
  padding: 10px;
  gap: 10px;
}

#nav-title {
  flex: 1;
}
</style>
