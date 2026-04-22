<script lang="ts" setup></script>

<template>
  <div id="nav-container">
    <div id="nav-title">
      <n-h3 class="no-margin-bottom">NJUPT Suan API</n-h3>
    </div>
    <a href="https://suan.mangofanfan.cn/" target="_blank">
      <n-button secondary type="primary">概览</n-button>
    </a>
    <n-popover trigger="hover">
      <template #trigger>
        <n-button secondary type="info">源码</n-button>
      </template>
      <n-p class="no-margin-bottom"
        >NJUPT Suan API 的代码开源在以下两个地方，后面的那个可能更快？</n-p
      >
      <n-flex justify="center">
        <a href="https://github.com/mangofanfan/NJUPT-Suan-API" target="_blank">
          <n-button secondary type="info">GitHub</n-button>
        </a>
        <a href="https://gitea.mangofanfan.cn/SuanDev/NJUPT-Suan-API" target="_blank">
          <n-button secondary type="success">Mango Gitea</n-button>
        </a>
      </n-flex>
    </n-popover>
    <a href="https://mangofanfan.cn/" target="_blank">
      <n-button secondary type="error">芒果</n-button>
    </a>
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
