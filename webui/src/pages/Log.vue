<script lang="ts" setup>
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef} from 'vue'
import {AnsiUp} from 'ansi_up' // 用于解析日志颜色
import type {logDto} from '@/types/logger'

defineOptions({
  name: 'Log',
})

const logContent = ref('')
const logBox = useTemplateRef('logBox')
const ansiUp = new AnsiUp()
ansiUp.use_classes = true
let ws: WebSocket | null = null

const initWebSocket = () => {
  ws = new WebSocket(`ws://${window.location.hostname}:8000/ws/logs`)

  ws.onmessage = (event) => {
    // 1. 解析 ANSI 颜色编码
    const logs = JSON.parse(event.data)['logs'] as logDto[]
    for (const log of logs) {
      logContent.value += ansiUp.ansi_to_html(log.message) + '<br>'
    }

    // 2. 自动滚动到底部
    nextTick(() => {
      if (logBox.value) {
        logBox.value.scrollTop = logBox.value.scrollHeight
      }
    })
  }

  ws.onerror = (e) => console.error('WebSocket Error:', e)
  ws.onclose = () => {
    console.log('WebSocket Closed, reconnecting...')
    setTimeout(initWebSocket, 3000)
  }
}

onMounted(initWebSocket)
onBeforeUnmount(() => {
  if (ws) {
    ws.close()
  }
})
</script>

<template>
  <div id="log-container">
    <n-h2 prefix="bar">酸酸日志</n-h2>
    <n-alert title="酸……吗？" type="info">
      <n-p>
        FastAPI 后端的日志会在此处显示，这样也许可以方便你检查酸 API 的运行情况。
        <n-text strong type="warning">这不是 WebUI 的日志。</n-text>
      </n-p>
    </n-alert>
    <n-alert title="如果遇到严重错误" type="warning">
      <n-p>
        如果 FastAPI 后端遇到严重错误，日志可能无法被顺利发送到 WebUI。所以如果你发现酸 API
        出现事实性故障，那么你可能
        <n-text strong type="warning">需要亲自查看终端和文件中的日志。</n-text>
      </n-p>
    </n-alert>

    <div ref="logBox" class="log-container">
      <pre id="log-content" v-html="logContent" />
    </div>

    <n-p>
      日志会以追加模式（w）写入到
      <n-code inline>data/app.log</n-code>
      文件中。
    </n-p>
  </div>
</template>

<style scoped>
div.log-container {
  padding: 6px;
  width: 98%;
  min-width: 0;
  height: 500px;
  overflow: auto;

  margin-top: 10px;
  background-color: #191a1c;
  border: 1px solid #ccc;
  border-radius: 4px;
}

pre#log-content {
  min-width: 0;
  max-width: 100%;
  margin: 0;
  white-space: pre-wrap;
  line-height: 1;
  color: #cdcdcd;

  font-family:
    Maple Mono CN,
    sans-serif;
  letter-spacing: 0;
  font-size: 13px;
}
</style>
