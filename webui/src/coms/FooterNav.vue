<script lang="ts" setup></script>

<template>
  <div class="footer-container">
    <div class="footer-card c1"><strong>NJUPT Suan API</strong></div>
    <div class="footer-card c2">made with love by MangoFanFanw</div>
  </div>
</template>

<style lang="scss" scoped>
div.footer-container {
  padding: 12px;
  display: flex;
  flex-direction: row;
  gap: 10px;

  div.footer-card {
    padding: 3px 6px;
    border-radius: 6px;

    &.c1 {
      border: 1px solid #2bf8ff;
      background-color: #d1fff1;
    }

    &.c2 {
      border: 1px solid #c3ff2b;
      background-color: #f7ffe2;
    }
  }
}
</style>
