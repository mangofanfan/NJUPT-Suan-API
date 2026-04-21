<script lang="ts" setup>
import {onMounted, ref} from 'vue'
import {useConfig} from '@/stores/config.ts'
import type {FastApiDto} from '@/types/fastapi.ts'

defineOptions({
  name: 'Overview',
})

const config = useConfig()

const api_version = ref('unknown')
const webui_version = __VERSION__

interface VerDto {
  version: string
}

onMounted(() => {
  fetch('/version', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((res) => res.json())
    .then((data: FastApiDto) => data.result as VerDto)
    .then((data: VerDto) => {
      api_version.value = data.version
    })
})
</script>

<template>
  <div id="overview-container">
    <n-h1 prefix="bar">NJUPT Suan API WebUI</n-h1>

    <n-flex vertical>
      <n-card title="FastAPI 后端状态">
        <template #header-extra>
          <n-tag type="info">版本 {{ api_version }}</n-tag>
        </template>
      </n-card>
      <n-card title="WebUI 前端状态">
        <template #header-extra>
          <n-tag type="info">版本 {{ webui_version }}</n-tag>
        </template>
      </n-card>
    </n-flex>

    <n-p>
      欢迎使用 NJUPT Suan API。本项目仍然处于早期开发阶段，更多新功能和稳定性改善仍在计划中~
    </n-p>
  </div>
</template>

<style scoped></style>
