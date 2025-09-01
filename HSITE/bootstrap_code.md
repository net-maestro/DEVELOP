
Требования:  
✅ Vue 3 + Vite  
✅ Bootstrap 5 (установлен через npm)  
✅ Шрифт Inter  
✅ Украинский язык  
✅ Адаптивность + горизонтальная прокрутка тарифов на мобильных  
✅ Калькулятор скорости + динамический IPTV  
✅ Минимализм и современный дизайн (как у simnet.ua)  
✅ Готов к выкладке на GitHub

---

## 📁 Структура проекта

```
nethub/
├── public/
│   └── index.html
├── src/
│   ├── assets/
│   │   └── logo.svg
│   ├── components/
│   │   ├── Navbar.vue
│   │   ├── Footer.vue
│   │   ├── TariffCard.vue
│   │   └── ContactForm.vue
│   ├── views/
│   │   ├── HomeView.vue
│   │   └── AboutView.vue
│   ├── styles/
│   │   └── main.scss
│   ├── router/
│   │   └── index.js
│   ├── App.vue
│   └── main.js
├── package.json
├── vite.config.js
└── README.md
```

---

## ✅ 1. `package.json`

```json
{
  "name": "nethub",
  "version": "1.0.0",
  "description": "Швидкий інтернет провайдер — NetHUB",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "deploy": "vite build && gh-pages -d dist"
  },
  "dependencies": {
    "bootstrap": "^5.3.2",
    "bootstrap-icons": "^1.11.3",
    "vue": "^3.4.0",
    "vue-router": "^4.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0",
    "sass": "^1.70.0",
    "gh-pages": "^6.1.1"
  }
}
```

---

## ✅ 2. `vite.config.js`

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern-compiler' // или 'legacy', если ошибка
      }
    }
  },
  build: {
    outDir: 'dist'
  }
})
```

---

## ✅ 3. `public/index.html`

```html
<!DOCTYPE html>
<html lang="uk">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="icon" href="/src/assets/logo.svg" type="image/svg+xml">
    <title>NetHUB — Швидкий інтернет</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

---

## ✅ 4. `src/main.js`

```js
import { createApp } from 'vue'
import App from './App.vue'

// === CSS ===
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './styles/main.scss'

// === JS ===
import 'bootstrap' // активирует тултипы, модалки и т.д.

// === Router ===
import router from './router'

createApp(App).use(router).mount('#app')
```

---

## ✅ 5. `src/styles/main.scss`

```scss
// Глобальные стили
body {
  font-family: 'Inter', sans-serif;
}

// Отступы
.py-10 { padding: 4rem 0; }
.mb-12 { margin-bottom: 3rem; }
.mt-16 { margin-top: 4rem; }

// Цвета
.bg-primary { background-color: #2A5DFF !important; }
.text-primary { color: #2A5DFF !important; }
.bg-secondary { background-color: #F5F7FA !important; }

// Карточка тарифу
.tariff-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  background: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  }

  &.popular {
    border: 2px solid #2A5DFF;
    position: relative;

    &::before {
      content: "Популярно";
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      background: #2A5DFF;
      color: white;
      font-size: 0.75rem;
      font-weight: 500;
      padding: 4px 12px;
      border-radius: 20px;
    }
  }

  h3 {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  .speed {
    font-size: 2rem;
    font-weight: 700;
    color: #2A5DFF;
  }

  .price {
    color: #666;
    font-size: 1rem;
  }

  ul {
    list-style: none;
    padding: 0;
    margin-bottom: 1.5rem;

    li {
      display: flex;
      align-items: center;
      font-size: 0.875rem;
      margin-bottom: 0.5rem;
      color: #333;

      &::before {
        content: "✓";
        color: #2A5DFF;
        font-weight: bold;
        margin-right: 8px;
      }
    }
  }

  button {
    border-radius: 50px;
    font-weight: 500;
    padding: 10px 0;
  }
}

// Кастомизация слайдера
.form-range {
  accent-color: #2A5DFF;
  width: 100%;
}
```

---

## ✅ 6. `src/router/index.js`

```js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/about', component: AboutView }
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})
```

---

## ✅ 7. `src/components/Navbar.vue`

```vue
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container">
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img src="@/assets/logo.svg" alt="Logo" width="40" height="40" class="me-2">
        <span class="fw-bold fs-5">NetHUB</span>
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <div class="ms-auto">
          <router-link class="nav-link" to="/">Головна</router-link>
          <router-link class="nav-link" to="/#tariffs">Тарифи</router-link>
          <router-link class="nav-link" to="/#contact">Контакти</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>
```

---

## ✅ 8. `src/components/Footer.vue`

```vue
<template>
  <footer class="bg-secondary py-6 mt-12">
    <div class="container text-center text-secondary small">
      &copy; 2025 NetHUB — Швидкий інтернет по Україні
    </div>
  </footer>
</template>
```

---

## ✅ 9. `src/components/TariffCard.vue`

```vue
<template>
  <div class="tariff-card" :class="{ popular: tariff.popular }">
    <h3 class="mb-2">{{ tariff.name }}</h3>
    <p class="speed mb-1">
      {{ tariff.speed }} <small>Мбіт/с</small>
    </p>
    <p class="price mb-4">від {{ tariff.price }} ₴/міс</p>

    <hr>

    <ul class="mb-4 px-2 text-start">
      <li v-for="(feature, i) in tariff.features" :key="i" class="mb-1">
        {{ feature }}
      </li>
    </ul>

    <button class="btn btn-primary w-100">
      {{ tariff.popular ? 'Найкращий вибір' : 'Підключити' }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  tariff: { type: Object, required: true }
})
</script>
```

---

## ✅ 10. `src/components/ContactForm.vue`

```vue
<template>
  <form @submit.prevent="submit" class="mx-auto" style="max-width: 500px;">
    <div class="mb-3">
      <input v-model="name" type="text" class="form-control" placeholder="Ім’я" required>
    </div>
    <div class="mb-3">
      <input v-model="phone" type="tel" class="form-control" placeholder="Телефон" required>
    </div>
    <div class="mb-3">
      <textarea v-model="message" class="form-control" rows="3" placeholder="Повідомлення"></textarea>
    </div>
    <button type="submit" class="btn btn-primary w-100" :disabled="loading">
      {{ loading ? 'Надсилається...' : 'Надіслати' }}
    </button>
    <p v-if="success" class="text-success mt-3 mb-0">
      Дякуємо! Ми зв’яжемося з вами найближчим часом.
    </p>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const phone = ref('')
const message = ref('')
const loading = ref(false)
const success = ref(false)

const submit = async () => {
  if (loading.value) return
  loading.value = true
  await new Promise(r => setTimeout(r, 1500))
  loading.value = false
  success.value = true
  setTimeout(() => success.value = false, 5000)
  name.value = phone.value = message.value = ''
}
</script>
```

---

## ✅ 11. `src/views/HomeView.vue`

```vue
<template>
  <div id="home">
    <div class="container py-10">

      <!-- Hero -->
      <div class="text-center mb-12 px-4">
        <h1 class="display-5 fw-bold mb-4">
          Швидкий і надійний інтернет для дому та офісу
        </h1>
        <p class="text-muted">Підключіться за 24 години. Без комісій та прихованих платежів.</p>
      </div>

      <!-- Калькулятор -->
      <section class="bg-secondary p-6 rounded-4 mb-12 mx-auto" style="max-width: 800px;" id="tariffs">
        <h2 class="h6 fw-bold mb-4 text-center">Підберіть тариф під себе</h2>

        <p class="text-center mb-2"><strong>{{ speed }} Мбіт/с</strong></p>
        <input
          v-model.number="speed"
          type="range"
          class="form-range px-4"
          min="10"
          max="1000"
          step="10"
        >

        <div class="d-flex justify-content-between text-secondary small mt-2 px-4">
          <span>10 Мбіт/с</span>
          <span>1000 Мбіт/с</span>
        </div>

        <div class="mt-6 text-center">
          <div class="form-check form-switch d-inline-block">
            <input
              v-model="iptvEnabled"
              class="form-check-input"
              type="checkbox"
              id="iptvSwitch"
            >
            <label class="form-check-label" for="iptvSwitch">
              Підключити IPTV (+50 ₴/міс)
            </label>
          </div>
        </div>
      </section>

      <!-- Тарифы -->
      <div class="mb-12">
        <!-- Desktop -->
        <div class="row g-4 justify-content-center d-none d-md-flex">
          <div
            v-for="tariff in filteredTariffs"
            :key="tariff.id"
            class="col-12 col-sm-6 col-md-4 col-lg-3"
          >
            <TariffCard :tariff="tariff" />
          </div>
        </div>

        <!-- Mobile (горизонтальная прокрутка) -->
        <div class="d-md-none overflow-auto pb-3">
          <div class="d-flex gap-3 p-2">
            <div
              v-for="tariff in filteredTariffs"
              :key="tariff.id"
              style="min-width: 300px; max-width: 320px;"
            >
              <TariffCard :tariff="tariff" />
            </div>
          </div>
        </div>
      </div>

      <!-- Контакты -->
      <div id="contact" class="text-center mt-16 px-4">
        <h2 class="h5 fw-bold mb-6">Потрібна консультація?</h2>
        <ContactForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import TariffCard from '@/components/TariffCard.vue'
import ContactForm from '@/components/ContactForm.vue'

const speed = ref(100)
const iptvEnabled = ref(false)

const baseTariffs = [
  { id: 1, name: 'Базовий', speed: 30, basePrice: 150, features: ['Wi-Fi роутер', 'Техпідтримка'], popular: false },
  { id: 2, name: 'Стандарт', speed: 100, basePrice: 250, features: ['Wi-Fi 6', 'Пріоритет у підтримці'], popular: true },
  { id: 3, name: 'Максимум', speed: 500, basePrice: 400, features: ['Оптоволокно', 'Підтримка 24/7', 'Безліміт'], popular: false },
  { id: 4, name: 'Гігабіт', speed: 1000, basePrice: 600, features: ['Гігабіт', 'VIP-обслуговування', 'Резервний канал'], popular: false },
]

const filteredTariffs = computed(() => {
  const iptvCost = iptvEnabled.value ? 50 : 0
  return baseTariffs
    .filter(t => t.speed >= speed.value)
    .map(t => ({
      ...t,
      price: t.basePrice + iptvCost,
      features: [
        ...t.features,
        ...(iptvEnabled.value ? ['IPTV (300+ каналів)'] : [])
      ]
    }))
})
</script>
```

---

## ✅ 12. `src/views/AboutView.vue`

```vue
<template>
  <div class="container py-12">
    <h1 class="display-6 fw-bold text-center mb-6">Про нас</h1>
    <p class="text-muted text-center px-4">
      NetHUB — це сучасний інтернет-провайдер, який пропонує високу швидкість, стабільність та чесні тарифи без прихованих платежів.
    </p>
  </div>
</template>
```

---

## ✅ 13. `src/App.vue`

```vue
<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<template>
  <Navbar />
  <RouterView />
  <Footer />
</template>

<style scoped></style>
```

---

## ✅ 14. `README.md` (опционально)

```md
# NetHUB — Швидкий інтернет

Сучасний сайт інтернет-провайдера на Vue 3 + Vite + Bootstrap 5.

## 🚀 Запуск

```bash
npm install
npm run dev
```

## 📦 Деплой на GitHub Pages

```bash
npm run deploy
```

> Перед этим укажите `homepage` в `package.json`.
```

---

## ✅ Как запустить

```bash
# 1. Установить зависимости
npm install

# 2. Запустить локально
npm run dev

# 3. Собрать
npm run build

# 4. Задеплоить на GitHub Pages
npm run deploy
```

---
