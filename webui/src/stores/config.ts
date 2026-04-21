import {defineStore} from 'pinia'
import {ref} from 'vue'
import type {
  ConfigDataDto,
  ConfigLogDto,
  ConfigScheduleDto,
  ConfigSystemDto,
} from '@/types/config.ts'
import {admin} from '@/tools/web.ts'
import type {FastApiDto} from '@/types/fastapi.ts'

export const useConfig = defineStore('config', () => {
  const tokenValidated = ref(false)

  const dataStatus = ref(false)

  const data = ref<{
    system: ConfigSystemDto
    schedule: ConfigScheduleDto
    log: ConfigLogDto
  }>({
    system: {},
    schedule: {},
    log: {},
  })

  function update() {
    dataStatus.value = false
    admin
      .get('config')
      .then((res) => res.data)
      .then((_data: FastApiDto) => _data.result)
      // @ts-ignore
      .then((_data: ConfigDataDto) => {
        data.value.system = _data.system
        data.value.schedule = _data.schedule
        data.value.log = _data.log
      })
      .finally(() => (dataStatus.value = true))
  }

  function save() {
    dataStatus.value = false
    admin
      .post('config', { data: data.value })
      .then((res) => res.data)
      .then((_data: FastApiDto) => _data.result)
      // @ts-ignore
      .then((_data: ConfigDataDto) => {
        data.value.system = _data.system
        data.value.schedule = _data.schedule
        data.value.log = _data.log
      })
      .finally(() => (dataStatus.value = true))
  }

  return { tokenValidated, dataStatus, data, update, save }
})
