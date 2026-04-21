<script lang="ts" setup>
import HeaderNav from '@/coms/HeaderNav.vue'
import SidebarNav from '@/coms/SidebarNav.vue'

import {dateZhCN, zhCN} from 'naive-ui'
import hljs from 'highlight.js'
import javascript from 'highlight.js/lib/languages/javascript'
import LoginCard from '@/coms/LoginCard.vue'
import {onMounted} from 'vue'
import {getCookie, removeCookie, setCookie} from 'typescript-cookie'
import {validateAdminToken} from '@/tools/web.ts'
import {useConfig} from '@/stores/config.ts'
import FooterNav from '@/coms/FooterNav.vue'

const CONFIG = useConfig()

hljs.registerLanguage('javascript', javascript)

onMounted(async () => {
  const token = getCookie('token')
  if (token) {
    if (await validateAdminToken(token)) {
      CONFIG.tokenValidated = true
      setCookie('token', token)
    } else {
      removeCookie('token')
    }
  }
})
</script>

<template>
  <n-config-provider
    :date-locale="dateZhCN"
    :hljs
    :locale="zhCN"
    :theme-overrides="{
      common: {
        fontFamily: 'Maple Mono CN, sans-serif',
        fontFamilyMono: 'Maple Mono CN, monospace',
        fontWeightStrong: '700',
        fontWeight: '500',
      },
    }"
    inline-theme-disabled
  >
    <n-message-provider>
      <div v-if="CONFIG.tokenValidated" class="main-container">
        <div id="start-container">
          <header-nav />
        </div>
        <div id="center-container">
          <div id="center-sidebar">
            <sidebar-nav />
          </div>
          <div id="center-content">
            <div id="content-container">
              <router-view v-slot="{ Component }">
                <keep-alive>
                  <component :is="Component" />
                </keep-alive>
              </router-view>
            </div>
          </div>
        </div>
        <div id="end-container" style="padding-top: 6px">
          <footer-nav />
        </div>
      </div>

      <div v-else class="main-container">
        <login-card />
      </div>
    </n-message-provider>
    <n-global-style />
  </n-config-provider>
</template>

<style lang="scss" scoped>
.main-container {
  width: 100vw;
  max-width: 100vw;
  height: 100svh;
  max-height: 100svh;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  #start-container,
  #end-container {
    flex-shrink: 0;
  }

  #center-container {
    flex: 1;
    display: flex;
    flex-direction: row;
    gap: 10px;
    padding: 10px;
    min-height: 0;

    #center-sidebar {
      flex: 0;
      min-width: 160px;
    }

    #center-content {
      flex: 1;
      min-height: 0;

      #content-container {
        border: 1px solid #519f72;
        border-radius: 10px;
        padding: 10px;
        height: 100%;
        overflow: auto;
      }
    }
  }
}
</style>
