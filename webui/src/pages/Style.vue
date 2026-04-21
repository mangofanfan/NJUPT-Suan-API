<script lang="ts" setup>
import ScheduleTable from '@/coms/ScheduleTable.vue'
import {onMounted, ref} from 'vue'
import type {AliasDto, CourseDto} from '@/types/schedule.ts'
import {admin, api} from '@/tools/web.ts'
import type {FastApiDto} from '@/types/fastapi.ts'
import SettingCard from '@/coms/SettingCard.vue'
import {scheduleTypeOptions} from '@/types/options.ts'
import {useMessage} from 'naive-ui'

const MESSAGE = useMessage()

defineOptions({
  name: 'Style',
})

const courses = ref<CourseDto[] | null>(null)
const aliases = ref<AliasDto[]>([])

const originalName = ref('')
const aliasName = ref('')

const scheduleImgUrl = ref<string | null>(null)

function query() {
  courses.value = null
  console.log(formValue.value)
  api
    .post(scheduleType.value === 'class' ? 'schedule/class' : 'schedule/student', {
      username: formValue.value.username === '' ? null : formValue.value.username,
      password: formValue.value.password === '' ? null : formValue.value.password,
      week: formValue.value.week,
      img: formValue.value.img,
    })
    .then((res) => res.data)
    .then((data: FastApiDto) => {
      courses.value = data.result as CourseDto[]
      scheduleImgUrl.value = data.img_url
    })
}

function addAlias() {
  if (originalName.value === '' || aliasName.value === '') {
    MESSAGE.error('需要输入别名……')
    return
  }
  admin
    .post('schedule/alias', {
      originalName: originalName.value,
      aliasName: aliasName.value,
    })
    .then((res) => res.data)
    .then((data: FastApiDto) => {
      if (data.success) {
        MESSAGE.success('课程别名添加成功~')
        originalName.value = ''
        aliasName.value = ''
      } else {
        MESSAGE.error(`课程别名添加失败：${data.message}`)
        console.error(`课程别名添加失败：${data.message}`)
      }
    })
  refreshAlias()
}

function refreshAlias() {
  admin
    .get('schedule/alias')
    .then((res) => res.data)
    .then((data: FastApiDto) => (aliases.value = data.result as AliasDto[]))
}

onMounted(() => {
  query()
  refreshAlias()
})

const formValue = ref({
  username: '',
  password: '',
  week: 7,
  img: false,
})

const scheduleType = ref('class')
</script>

<template>
  <div id="style-container">
    <n-h2 prefix="bar">样式设计</n-h2>
    <n-p>在这里预览酸 API 返回的课程表图片的样式效果。</n-p>

    <n-flex>
      <setting-card
        message="看看谁的哪一周的课表呢？学号也可以为空，以预览默认班级课表。"
        title="预览设置"
      >
        <template #header-extra>
          <n-flex justify="right" style="width: max-content">
            <n-select
              v-model:value="scheduleType"
              :options="scheduleTypeOptions"
              class="min-width max-width"
            />
            <n-button type="success" @click="query()">查</n-button>
          </n-flex>
        </template>
        <template #default>
          <n-form :model="formValue" class="no-margin-bottom" inline label-width="auto">
            <n-form-item label="学号" path="username">
              <n-input v-model:value="formValue.username" />
            </n-form-item>
            <n-form-item label="密码" path="password">
              <n-input v-model:value="formValue.password" />
            </n-form-item>
            <n-form-item label="第（）周" path="week">
              <n-input-number v-model:value="formValue.week" />
            </n-form-item>
            <n-form-item label="生成图片" path="img">
              <n-switch v-model:value="formValue.img" />
            </n-form-item>
          </n-form>
          <n-p v-if="scheduleImgUrl">
            课表图片位于 <n-text strong type="success">{{ scheduleImgUrl }}</n-text>
          </n-p>
        </template>
      </setting-card>

      <setting-card
        message="为前几个字易混淆的课程设置别名，方便区分。例如，将「计算机问题求解（使用C语言）」的别名设置为「C语言」。"
        title="课程别名"
      >
        <template #header-extra>
          <n-flex justify="right" style="width: max-content">
            <n-input
              v-model:value="originalName"
              class="min-width-large max-width-large"
              placeholder="计算机问题求解（使用C语言）"
            />
            <n-input v-model:value="aliasName" class="min-width max-width" placeholder="C" />
            <n-button type="primary" @click="addAlias()">添加别名</n-button>
            <n-button secondary type="info" @click="refreshAlias()">刷新</n-button>
          </n-flex>
        </template>
        <template #default>
          <n-flex>
            <n-tag v-for="alias in aliases" :key="alias.id" type="info">
              {{ alias.originalName }} => {{ alias.aliasName }}
            </n-tag>
          </n-flex>
          <n-p
            >如需更新预览效果，添加别名之后需要重新<n-text strong type="success">查</n-text
            >一次课表哦。</n-p
          >
        </template>
      </setting-card>
    </n-flex>

    <schedule-table v-if="courses !== null" :courses />
  </div>
</template>

<style scoped></style>
