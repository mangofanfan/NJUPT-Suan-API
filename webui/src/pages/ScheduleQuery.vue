<script lang="ts" setup>
import {computed, onMounted, ref} from 'vue'
import {scheduleTypeOptions} from '@/types/options.ts'
import {admin} from '@/tools/web.ts'

const formValue = ref({
  username: '',
  password: '',
  scheduleType: 'class',
})

const queryTestResult = ref<object | null>(null)
const queryTestResultJson = computed(() => JSON.stringify(queryTestResult.value, null, 2))

function query() {
  admin
    .post('schedule/test', formValue.value)
    .then((res) => res.data)
    .then((data) => {
      queryTestResult.value = data
    })
}

onMounted(() => {
  admin
    .get('schedule/test')
    .then((res) => res.data)
    .then((data) => {
      queryTestResult.value = data
    })
})
</script>

<template>
  <n-h3>课表查询</n-h3>

  <n-p>
    在这里尝试查询课表，检查是否成功。在此处查询的最后一次
    <n-text strong type="info">班级课表</n-text>
    会被保存在数据库中，以供无凭证无参数调用酸 API 获取班级课表时返回。
  </n-p>
  <n-p>
    <n-text strong type="warning"
      >出于隐私保护的考虑，个人课表不会被保存，需要每次都携带凭证查询。</n-text
    >
  </n-p>

  <n-card>
    <template #default>
      <n-form :model="formValue" class="no-margin-bottom" inline label-width="auto">
        <n-form-item label="学号" path="username">
          <n-input v-model:value="formValue.username" />
        </n-form-item>
        <n-form-item label="密码" path="password">
          <n-input v-model:value="formValue.password" />
        </n-form-item>
        <n-form-item label="课表类型" path="scheduleType">
          <n-select
            v-model:value="formValue.scheduleType"
            :options="scheduleTypeOptions"
            class="min-width"
          />
        </n-form-item>
        <n-form-item>
          <n-button type="primary" @click="query()">查询</n-button>
        </n-form-item>
      </n-form>
      <n-code :code="queryTestResultJson" language="json" />
    </template>
  </n-card>
</template>

<style scoped></style>
