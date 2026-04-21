<script lang="ts" setup>
import type {MenuOption} from 'naive-ui'
import {ref} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()

const activeKey = ref('/')
const options: MenuOption[] = [
  {
    label: '面板主页',
    key: '/',
  },
  {
    label: '课表管理',
    key: '/schedule',
  },
  {
    label: '样式设计',
    key: '/style',
  },
  {
    label: '酸酸日志',
    key: '/log',
  },
  {
    label: '酸酸设置',
    key: '/config',
  },
]

function handleClick(key: string) {
  router.push(key)
}
</script>

<template>
  <n-menu v-model:value="activeKey" :options @update:value="handleClick" />
</template>

<style scoped></style>
