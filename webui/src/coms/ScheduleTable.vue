<script lang="tsx" setup>
import {getGradientColor} from "@/tools/random.ts";
import type {CourseDatumDto, CourseDto} from '@/types/schedule.ts'
import {NH4, NTooltip} from "naive-ui";
import {onMounted, reactive} from 'vue'
import FooterNav from "@/coms/FooterNav.vue";

const { courses } = defineProps<{
  courses: CourseDto[] | null
  title?: string
  subtitle?: string
}>()

// 生成空的 courseData
const generateCourseKeys = () => {
  const keys: Record<number, Record<number, CourseDatumDto | null>> = {}
  for (let i = 1; i <= 7; i++) {
    keys[i] ={}
    for (let j = 1; j <= 12; j++) {
      keys[i]![j] = null
    }
  }
  return keys
}

const courseData = reactive<Record<number, Record<number, CourseDatumDto | null>>>(generateCourseKeys())

onMounted(() => {
  if (courses === null) return
  for (const course of courses) {
    courseData[course.day]![course.classes.at(0)!] = {
      name: course.name,
      alias: course.alias,
      teacher: course.teacher,
      classroom: course.classroom,
      during: course.classes.length
    }
  }
})

// 生成基础 Course 卡片。
function baseCourseCard(
  title: string,
  content?: string | null,
  extraClass?: string | null,
  extraStyle?: object | null,
  during: number=1,
  tooltip: string | null = null) {
  // noinspection JSUnusedGlobalSymbols
  return (
    <div class={["base-card", extraClass]} style={{
      'min-height': 60 * during + 2 * (during - 1) + 'px',
      ...extraStyle
    }}>
      <NTooltip>{{
        trigger: () => <NH4 class={["no-margin-bottom", "line-1"]}>{title}</NH4>,
        default: () => tooltip ? tooltip : "O.o?"
      }}</NTooltip>
      { content ? <n-p class={["no-margin", "line-1"]} innerHTML={content}></n-p> : null}
    </div>
  )
}

function indexCardList() {
  return (
    <>
      {Array.from({length: 12}, (_, i) =>
        baseCourseCard((i + 1).toString(), null, `index-card-${i + 1}`))}
    </>
  )
}

function dayCourseCardList(day: number) {
  const items = Object.values(courseData[day]!)
  let left = 0
  return (
    <>
      {items.map((item, _) => {
        if (item === null) {
          if (left === 0) {
            return baseCourseCard('FREE TIME', null, 'no-course-card')
          }
          else {
            left -= 1
            return null
          }
        }
        left = item.during - 1
        if (item.teacher === null) item.teacher = ''
        return baseCourseCard(
          item.alias ? item.alias : item.name,
          item.teacher + ( item.classroom === null ? '' : '<br />' + item.classroom),
          'course-card',
          {'background-image': getGradientColor()},
          item.during,
          item.name
        )
      })}
    </>
  )
}
</script>

<template>
  <div class="schedule-table-container">
    <div class="schedule-table-header-container">
      <div class="header-card">
        <n-h1 class="title no-margin">{{ title ? title : '芒果酸的课程表' }}</n-h1>
        <n-h3 class="no-margin">{{ subtitle ? subtitle : '我也要上吗？' }}</n-h3>
      </div>
    </div>

    <div class="schedule-table-body-container">
      <!-- 标题列 -->
      <div class="background-panel">
        <component :is="indexCardList()" />
      </div>

      <div class="background-panel">
        <component :is="dayCourseCardList(1)" />
      </div>
      <div class="background-panel">
        <component :is="dayCourseCardList(2)" />
      </div>
      <div class="background-panel">
        <component :is="dayCourseCardList(3)" />
      </div>
      <div class="background-panel">
        <component :is="dayCourseCardList(4)" />
      </div>
      <div class="background-panel">
        <component :is="dayCourseCardList(5)" />
      </div>
      <div class="background-panel">
        <component :is="dayCourseCardList(6)" />
      </div>
      <div class="background-panel">
        <component :is="dayCourseCardList(7)" />
      </div>
    </div>

    <footer-nav />
  </div>
</template>

<style lang="scss" scoped>
div.schedule-table-container {
  div.schedule-table-header-container {
    padding: 10px;

    // 真正的标题卡片
    div.header-card {
      text-align: center;
      padding: 10px;
      background: linear-gradient(8deg, #a6ffe9, #f2fffc);
      border-radius: 6px;
      border: 2px solid #2bdbff;

      position: relative;

      display: flex;
      justify-content: center;
      align-items: baseline;
      flex-direction: row;
      gap: 20px;

      .title {
        font-family: 'Smiley sans', sans-serif;
      }
    }

    div.header-card::before,
    div.header-card::after {
      content: '';
      position: absolute;
      bottom: 0;
      right: 0;
      border-radius: 6px 0 0 0;
      width: 300px;
      height: 10px;
      background-color: #2bdbff;
    }

    div.header-card::before {
      top: 0;
      left: 0;
      border-radius: 0 0 6px 0;
    }

    div.header-card::after {
      bottom: 0;
      right: 0;
      border-radius: 6px 0 0 0;
    }
  }

  div.schedule-table-body-container {
    display: flex;
    flex-direction: row;
    gap: 10px;
    padding: 0 10px;

    div.background-panel {
      display: flex;
      flex-direction: column;
      width: 100%;
      height: max-content;
      background-color: #efefef;
      border-radius: 6px;
      gap: 2px;
      padding: 4px;

      div.base-card {
        width: 100%;
        border-radius: 6px;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        box-sizing: border-box;
      }

      div.index-card-1,
      div.index-card-2 {
        background-color: #ffefd1;
      }

      div.index-card-3,
      div.index-card-4,
      div.index-card-5 {
        background-color: #dbf4ff;
      }

      div.index-card-6,
      div.index-card-7,
      div.index-card-8,
      div.index-card-9 {
        background-color: #d1ffff;
      }

      div.index-card-10,
      div.index-card-11,
      div.index-card-12 {
        background-color: #d7d2ff;
      }

      div.no-course-card {
        background-color: rgb(255 255 255 / 0);
        h4 {
          color: #cdcdcd;
        }
      }

      div.course-card {
        border: 2px solid #ffffff;
      }
    }
  }
}
</style>
