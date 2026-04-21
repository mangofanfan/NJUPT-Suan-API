<script lang="ts" setup>
import { ref } from 'vue'
import { useMessage } from 'naive-ui'
import { validateAdminToken } from '@/tools/web.ts'
import { useConfig } from '@/stores/config.ts'
import { setCookie } from 'typescript-cookie'

const MESSAGE = useMessage()
const CONFIG = useConfig()

const token = ref('')

async function login() {
  if (await validateAdminToken(token.value)) {
    MESSAGE.success('令牌验证成功，欢迎使用 NJUPT Suan API WebUI ~')
    CONFIG.tokenValidated = true
    setCookie('token', token.value, { expires: 2 })
  } else {
    MESSAGE.error('令牌验证失败，请重新验证！')
  }
}
</script>

<template>
  <div id="login-card">
    <n-h1 class="no-margin-bottom" prefix="bar" style="width: 90%">NJUPT Suan API 的 WebUI</n-h1>
    <n-p style="font-size: 20px">请提供令牌（在启动日志中打印）</n-p>
    <n-flex align="center" style="width: 90%" vertical>
      <n-input v-model:value="token" />
      <n-button-group>
        <n-button type="primary" @click="login()">登录</n-button>
        <n-button type="info">O.o?</n-button>
      </n-button-group>
    </n-flex>
  </div>
</template>

<style scoped>
#login-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: 460px;
  background: linear-gradient(to bottom right, lightblue, #cbb4ff);
  border: solid 2px #000000;
  border-radius: 16px;

  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
