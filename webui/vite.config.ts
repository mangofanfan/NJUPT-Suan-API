import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import vueJsx from '@vitejs/plugin-vue-jsx'
import AutoImport from 'unplugin-auto-import/vite'
import {NaiveUiResolver} from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'
import path from 'node:path/posix'
import {readFileSync} from "node:fs";
import {resolve} from 'path';

// 从 package.json 里搞到 WebUI 版本号
const pkg = JSON.parse(readFileSync(resolve(__dirname, 'package.json'), 'utf-8'));

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    vueJsx(),
    AutoImport({
      imports: ['vue', 'vue-router'],
    }),
    Components({
      resolvers: [NaiveUiResolver()],
    }),
  ],
  define: {
    __VERSION__: JSON.stringify(pkg.version)
  },
  build: {
    rolldownOptions: {
      input: {
        index: path.resolve(__dirname, 'index.html'),
        'index-schedule': path.resolve(__dirname, 'index-schedule.html'),
      }
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/admin': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/version': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
