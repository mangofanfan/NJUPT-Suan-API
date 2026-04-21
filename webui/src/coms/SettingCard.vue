<script lang="ts" setup>
import type {SelectOption} from 'naive-ui'

defineProps<{
  title: string
  message?: string
  showSwitch?: boolean
  showInput?: boolean
  showNumber?: boolean
  showSelect?: boolean
  showDatePicker?: boolean
  disabled?: boolean
  selectionOptions?: SelectOption[]
}>()

const booleanValue = defineModel<boolean | undefined>('booleanValue', { required: false })
const stringValue = defineModel<string | undefined>('stringValue', { required: false })
const numberValue = defineModel<number | undefined>('numberValue', { required: false })
const selectionValue = defineModel<string | undefined>('selectionValue', { required: false })
const dateValue = defineModel<string | undefined>('dateValue', { required: false })
</script>

<template>
  <n-card :title="title">
    <template v-if="showSwitch" #header-extra>
      <n-switch v-model:value="booleanValue" :disabled size="large" />
    </template>
    <template v-if="showInput" #header-extra>
      <n-input v-model:value="stringValue" :disabled size="large" />
    </template>
    <template v-if="showNumber" #header-extra>
      <n-input-number v-model:value="numberValue" :disabled size="large" />
    </template>
    <template v-if="showDatePicker" #header-extra>
      <n-date-picker
        v-model:formatted-value="dateValue"
        :disabled
        format="yyyy-MM-dd"
        size="large"
        type="date"
      />
    </template>
    <template v-if="showSelect" #header-extra>
      <n-select
        v-model:value="selectionValue"
        :disabled
        :options="selectionOptions"
        class="min-width-large"
        size="large"
      />
    </template>
    <n-p v-if="message">{{ message }}</n-p>
    <slot />
    <template #header-extra><slot name="header-extra" /></template>
  </n-card>
</template>

<style></style>
