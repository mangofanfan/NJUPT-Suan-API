<script lang="ts" setup>
import ApiCard from '@/coms/ApiCard.vue'
import ToolCard from '@/coms/ToolCard.vue'
</script>

<template>
  <n-alert title="通用参数" type="info">
    <n-p class="no-margin">
      <n-code inline>week</n-code> 数字，指示获取第几周的课表。可选，默认值为 0 表明获取全部。
    </n-p>
    <n-p class="no-margin">
      <n-code inline>img</n-code> 布尔值，指示是否生成课表图片。可选，默认值为 False。若为
      True，生成的图片的临时链接会在 <n-code inline>img_url</n-code> 中提供。
    </n-p>
    <n-p class="no-margin">
      <n-text strong type="warning">
        目前课表图片只考虑了生成某一周的课程表，因此
        <n-code inline>week=0;img=true</n-code>
        是未定义行为，请注意避免。
      </n-text>
    </n-p>
  </n-alert>

  <n-collapse style="margin-top: 1rem">
    <n-collapse-item name="1" title="可用接口">
      <n-flex vertical>
        <api-card description="获取班级课表" method="POST" path="/api/schedule/class">
          <n-p>
            可以携带
            <n-code inline>username</n-code>
            和
            <n-code inline>password</n-code>
            两个参数，携带时将会使用它们登录教务系统并查询。携带时，将会查询该学生所在班级的课表。
          </n-p>
          <n-p>
            不携带上述参数调用时，会返回数据库中存储的班级课表。你可以在下方的「课表查询」中保存一个班级课表。
          </n-p>
        </api-card>
        <api-card description="获取学生课表" method="POST" path="/api/schedule/student">
          <n-p>
            需要携带
            <n-code inline>username</n-code>
            和
            <n-code inline>password</n-code>
            两个参数，确保学生本人查询。
          </n-p>
        </api-card>
        <api-card description="获取课表图片" method="GET" path="/api/schedule/img/{name}">
          <n-p>
            <n-text strong type="warning">不接收包括上面的通用参数在内的任何参数。</n-text>
          </n-p>
          <n-p>
            图片名需要被包含在请求路径中。如果你在调用上面两个方法时指示生成图片，那么图片的完整路径应当已经被提供给你。
          </n-p>
        </api-card>
      </n-flex>
    </n-collapse-item>

    <n-collapse-item name="2" title="可用工具">
      <n-flex vertical>
        <tool-card description="获取默认班级课表" name="tool_schedule_class" type="Tool">
          返回数据库中存储的班级课表。你可以在下方的「课表查询」中保存一个班级课表。
        </tool-card>
        <tool-card
          description="获取指定学生的班级课表"
          name="tool_schedule_class_special"
          type="Tool"
        >
          <n-p>
            需要携带
            <n-code inline>username</n-code>
            和
            <n-code inline>password</n-code>
            两个参数，确保学生本人查询。
          </n-p>
        </tool-card>
        <tool-card
          description="获取指定学生的个人课表"
          name="tool_schedule_student_special"
          type="Tool"
        >
          <n-p>
            需要携带
            <n-code inline>username</n-code>
            和
            <n-code inline>password</n-code>
            两个参数，确保学生本人查询。
          </n-p>
        </tool-card>
        <tool-card description="直接获取课表图片" name="tool_schedule_image" type="Tool">
          <n-p>
            <n-text strong type="warning">本工具不接收上面的公共参数。</n-text>
          </n-p>
          <n-p>
            与其他工具返回图片的不同点在于，此工具会以 MCP 协议直接返回图片本身，避免客户端及 LLM
            二次下载。图片直接包含在会话中也可以避免酸 API 本地的图片被清理时导致 404。
          </n-p>
          <n-p>
            本工具只接收一个参数 <n-code inline>img_name</n-code> 作为图片的
            <n-text strong type="success">文件名</n-text>。
          </n-p>
        </tool-card>
      </n-flex>
    </n-collapse-item>
  </n-collapse>
</template>

<style scoped></style>
