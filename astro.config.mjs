// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  // Демо на GitHub Pages: сайт лежит в подпути репозитория, ссылки собираются через url() из src/data/site.ts
  site: 'https://ynkotp-webdev.github.io',
  base: '/Hubska-hair-studio',
  devToolbar: { enabled: false },
  // CSS маленький: встраиваем в HTML, чтобы на 4G не ждать отдельный запрос до первой отрисовки
  build: { inlineStylesheets: 'always' },
  vite: {
    plugins: [tailwindcss()]
  }
});