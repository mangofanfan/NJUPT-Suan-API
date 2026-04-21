<script lang="tsx" setup>
import SettingCard from '@/coms/SettingCard.vue'
import {useConfig} from '@/stores/config.ts'
import {onActivated, onDeactivated, onMounted, ref} from 'vue'
import {JwxtLoginMethodOptions} from '@/types/options.ts'
import {NCode, NTag, useMessage} from "naive-ui"

defineOptions({
  name: 'Config',
})

const CONFIG = useConfig()
const MESSAGE = useMessage()

const extraVisible = ref(true)

onMounted(() => {
  CONFIG.update()
})

onDeactivated(() => {
  extraVisible.value = false
})

onActivated(() => {
  extraVisible.value = true
})

function varTag(code: string, description: string) {
  return (
    <NTag type="info">
      <NCode inline>{code}</NCode> - {description}
    </NTag>
  )
}
</script>

<template>
  <div id="config-container">
    <n-h2 prefix="bar">酸酸设置</n-h2>
    <n-alert title="设置注意" type="info">
      <n-p class="no-margin">
        <n-text strong type="warning">系统设置</n-text>
        - 需要完全重新启动 Suan API 才能应用；
      </n-p>
      <n-p class="no-margin">其他的设置可以即时生效。</n-p>
    </n-alert>

    <n-collapse v-if="CONFIG.dataStatus" style="margin-top: 1rem">
      <n-collapse-item name="system" title="系统设置">
        <n-flex vertical>
          <setting-card
            v-model:string-value="CONFIG.data.system.host"
            message="host"
            show-input
            title="监听地址"
          />
          <setting-card
            v-model:number-value="CONFIG.data.system.port"
            message="port"
            show-number
            title="监听端口"
          />
          <setting-card
            v-model:boolean-value="CONFIG.data.system.reload"
            message="使用 uvicorn.run(..., reload=True) ，不建议在正式部署时开启。（据说会降低性能且可能导致内存泄露）"
            show-switch
            title="热重载 Python 代码文件"
          />
          <setting-card
            v-model:string-value="CONFIG.data.system.public_host"
            message="Suan API 需要对外提供资源（例如课表图片）时，使用此主机名"
            show-input
            title="外部域名 / 主机名"
          />
        </n-flex>
      </n-collapse-item>
      <n-collapse-item name="schedule" title="课表设置">
        <n-flex vertical>
          <setting-card
            v-model:boolean-value="CONFIG.data.schedule.playwright_headless"
            message="在生产环境中应当为 True，请参阅文档。"
            show-switch
            title="Playwright Headless 模式"
          />
          <setting-card
            v-model:selection-value="CONFIG.data.schedule.jwxt_login_method"
            :selection-options="JwxtLoginMethodOptions"
            message="连接到校园网时，可以使用教务系统直接登录；在校园外则需要使用 SSO 统一身份认证。"
            show-select
            title="教务系统登录方式"
          />
          <setting-card
            v-model:date-value="CONFIG.data.schedule.semester_start_date"
            message="当前学期从哪一天开始？我说的是第一周的星期一。给出非星期一的日期是未定义行为，请避免。"
            show-date-picker
            title="学期开始日期"
          />
          <setting-card
            v-model:string-value="CONFIG.data.schedule.schedule_title_template"
            show-input
            title="课表渲染图片的标题"
          >
            <n-p>标题中支持添加 Python 风格占位符，以代表动态填充的内容。</n-p>
            <n-p>
              具体来说，支持以下变量：
              <component :is="varTag('week', '第几周课表')" />、
              <component :is="varTag('week_start_day', '该周开始日期（YYYY-MM-DD）')" />、
              <component :is="varTag('week_end_day', '该周结束日期（YYYY-MM-DD）')" />。
            </n-p>
            <n-p>
              使用
              <n-code inline>第 {week} 周</n-code>
              来插入这些变量。
            </n-p>
          </setting-card>
          <setting-card
            v-model:string-value="CONFIG.data.schedule.schedule_subtitle_template"
            message="简单来说，和上面一样可以使用变量。"
            show-input
            title="课表渲染图片的副标题"
          />
        </n-flex>
      </n-collapse-item>
      <n-collapse-item name="log" title="日志设置">
        <n-flex vertical>
          <setting-card
            v-model:boolean-value="CONFIG.data.log.log_api_request_details"
            message="除去下面的特殊端点之外的所有端点"
            show-switch
            title="记录 API 调用详细日志"
          />
          <setting-card
            v-model:boolean-value="CONFIG.data.log.log_mcp_request_details"
            message="端点 /mcp 的请求会被自动忽略，MCP 调用日志"
            show-switch
            title="记录 MCP 调用详细日志"
          />
          <setting-card
            v-model:boolean-value="CONFIG.data.log.log_assets_request"
            message="端点位于 /assets（建议关闭，只有在生成图片和使用 WebUI 时才会访问其中资源。）"
            show-switch
            title="记录静态资源调用请求"
          />
        </n-flex>
      </n-collapse-item>
    </n-collapse>

    <teleport v-if="extraVisible" defer to="#center-container">
      <div class="header-card">
        <n-flex vertical>
          <n-button
            circle
            size="large"
            type="success"
            @click="
              () => {
                CONFIG.save()
                MESSAGE.success('保存设置成功，后端会自动应用新的设置 ~')
              }
            "
            >保存</n-button
          >
          <n-button circle size="large" type="warning">重启</n-button>
          <n-button circle size="large" type="error">关闭</n-button>
        </n-flex>
      </div>
    </teleport>
  </div>
</template>

<style scoped></style>
