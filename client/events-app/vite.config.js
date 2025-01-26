import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls } //Quasar related template transform
    }),
    vueDevTools(),
    quasar()
  ],
  build: {
    outDir: path.join('../../server', 'dist')
  }
});
