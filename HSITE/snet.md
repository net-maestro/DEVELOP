
✅ Все секции: Hero, Услуги, Тарифы, Форма проверки адреса, Акции, Преимущества, FAQ, Контакты  
✅ Адаптивность (включая горизонтальную прокрутку тарифов на мобильных)  
✅ Современный минималистичный дизайн  
✅ Украинский язык  
✅ Подключение Bootstrap 5 через npm  
✅ Готов к выкладке на GitHub Pages

---

## 📁 Полная структура проекта

```
simnet-clone/
├── public/
│   └── index.html
├── src/
│   ├── assets/
│   │   ├── logo.svg
│   │   └── icons/
│   │       ├── internet.png
│   │       ├── internet-tv.png
│   │       ├── tv.png
│   │       ├── intercom.png
│   │       ├── video.png
│   │       ├── personal.png
│   │       └── pay.png
│   ├── components/
│   │   ├── Navbar.vue
│   │   ├── Footer.vue
│   │   ├── ServiceCard.vue
│   │   ├── TariffCard.vue
│   │   ├── ContactForm.vue
│   │   ├── PromoBanner.vue
│   │   ├── FeatureCard.vue
│   │   └── FaqItem.vue
│   ├── views/
│   │   └── HomeView.vue
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
  "name": "simnet-clone",
  "version": "1.0.0",
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
        api: 'modern-compiler'
      }
    }
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
    <link rel="icon" href="/src/assets/logo.svg" type="image/svg+xml" />
    <title>Simnet – Провайдер найкращого інтернету в Києві та області</title>
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
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap'
import './styles/main.scss'
import router from './router'

createApp(App).use(router).mount('#app')
```

---

## ✅ 5. `src/styles/main.scss`

```scss
body {
  font-family: 'Inter', sans-serif;
  color: #333;
}

.bg-primary { background-color: #2A5DFF !important; }
.text-primary { color: #2A5DFF !important; }
.bg-light-blue { background-color: #F5F7FA !important; }
.bg-dark-blue { background-color: #003399 !important; }

.py-10 { padding: 5rem 0; }
.mb-12 { margin-bottom: 4rem; }
.mt-8 { margin-top: 3rem; }

h2, h3, h4 {
  font-weight: 600;
}

.btn-primary {
  background-color: #2A5DFF;
  border: none;
  border-radius: 50px;
  padding: 10px 24px;
  font-weight: 500;
}

.btn-outline-primary {
  border-color: #2A5DFF;
  color: #2A5DFF;
}

// Карточка услуги
.service-card {
  text-align: center;
  padding: 1.5rem;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-5px);
  }

  img {
    width: 60px;
    height: 60px;
    margin-bottom: 1rem;
  }

  h3 {
    font-size: 1.125rem;
    font-weight: 600;
  }

  p {
    font-size: 0.875rem;
    color: #666;
    margin: 0.5rem 0;
  }
}

// Тарифная карточка
.tariff-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  background: white;
  transition: all 0.3s ease;
  min-width: 280px;
  max-width: 320px;

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
      padding: 4px 12px;
      border-radius: 20px;
    }
  }

  .speed {
    font-size: 2rem;
    font-weight: 700;
    color: #2A5DFF;
  }

  .price {
    font-size: 1.1rem;
    font-weight: 600;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 1.5rem 0;

    li {
      margin-bottom: 0.5rem;
      font-size: 0.9rem;
      color: #555;

      &::before {
        content: "✓";
        color: #2A5DFF;
        font-weight: bold;
        margin-right: 8px;
      }
    }
  }

  button {
    width: 100%;
    border-radius: 50px;
    font-weight: 500;
  }
}

// Промо-баннер
.promo-banner {
  background: linear-gradient(135deg, #2A5DFF, #003399);
  color: white;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
}

// Преимущества
.feature-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;

  .icon {
    font-size: 1.5rem;
    color: #2A5DFF;
  }
}

// FAQ
.faq-item {
  border-bottom: 1px solid #eee;
  padding: 1rem 0;

  h5 {
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
```

---

## ✅ 6. `src/router/index.js`

```js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  { path: '/', component: HomeView }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
```

---

## ✅ 7. `src/components/Navbar.vue`

```vue
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container">
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img src="@/assets/logo.svg" alt="Simnet" width="40" height="40" class="me-2">
        <span class="fw-bold fs-5">Simnet</span>
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
          <router-link class="nav-link" to="/#services">Послуги</router-link>
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
  <footer class="bg-dark text-white py-6 mt-12">
    <div class="container text-center small">
      &copy; 2025 Simnet – Провайдер найкращого інтернету в Києві та області
    </div>
  </footer>
</template>
```

---

## ✅ 9. `src/components/ServiceCard.vue`

```vue
<template>
  <div class="service-card p-3">
    <img :src="icon" :alt="title" class="mb-2">
    <h3>{{ title }}</h3>
    <p>{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  icon: String,
  title: String,
  description: String
})
</script>
```

---

## ✅ 10. `src/components/TariffCard.vue`

```vue
<template>
  <div class="tariff-card" :class="{ popular }">
    <h3 class="mb-2">{{ tariff.name }}</h3>
    <p class="speed mb-1">{{ tariff.speed }} <small>Мбіт/с</small></p>
    <p class="price text-primary mb-3">{{ tariff.price }} ₴/міс</p>

    <ul>
      <li v-for="feature in tariff.features" :key="feature">{{ feature }}</li>
    </ul>

    <button class="btn btn-primary">
      {{ popular ? 'Найкращий вибір' : 'Підключити' }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  tariff: { type: Object, required: true },
  popular: { type: Boolean, default: false }
})
</script>
```

---

## ✅ 11. `src/components/ContactForm.vue`

```vue
<template>
  <div class="text-center mb-8">
    <h3 class="h5 fw-bold mb-4">Перевірте свою адресу на можливість підключення</h3>
    <form class="d-flex flex-column flex-md-row gap-3 justify-content-center">
      <input type="text" class="form-control" placeholder="Вулиця" required>
      <input type="text" class="form-control" placeholder="Будинок" required>
      <button class="btn btn-primary">Перевірити</button>
    </form>
  </div>

  <div class="row text-center g-4">
    <div class="col-6 col-md-3">
      <img src="@/assets/icons/personal.png" alt="Особистий кабінет" width="50">
      <p class="small mt-2">Особистий кабінет</p>
    </div>
    <div class="col-6 col-md-3">
      <img src="@/assets/icons/pay.png" alt="Поповнити рахунок" width="50">
      <p class="small mt-2">Поповнити рахунок онлайн</p>
    </div>
  </div>
</template>
```

---

## ✅ 12. `src/components/PromoBanner.vue`

```vue
<template>
  <div class="promo-banner mb-12 text-white">
    <h2 class="h4 fw-bold">Акції</h2>
    <p>Користуйтеся вигідними пропозиціями від Simnet! Слідкуйте за оновленнями на сторінці та першими дізнавайтеся про нові акції та спеціальні умови</p>
    <button class="btn btn-light btn-sm mt-2">Детальніше</button>
  </div>
</template>
```

---

## ✅ 13. `src/components/FeatureCard.vue`

```vue
<template>
  <div class="feature-card">
    <div class="icon">
      <i :class="icon"></i>
    </div>
    <div class="content">
      <h5 class="mb-1">{{ title }}</h5>
      <p class="text-muted small">{{ description }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  icon: String,
  title: String,
  description: String
})
</script>
```

---

## ✅ 14. `src/components/FaqItem.vue`

```vue
<template>
  <div class="faq-item">
    <h5 @click="open = !open">
      {{ question }}
      <i :class="open ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
    </h5>
    <div v-if="open" class="answer text-muted">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
defineProps({ question: String })
const open = ref(false)
</script>
```

---

## ✅ 15. `src/views/HomeView.vue`

```vue
<template>
  <div id="home">
    <!-- Hero -->
    <section class="bg-light-blue py-10 text-center">
      <div class="container">
        <h1 class="display-5 fw-bold">Simnet – Провайдер найкращого інтернету в Києві та області!</h1>
        <p class="lead text-muted mt-3">
          Simnet - провідний інтернет-провайдер Києва та області, який забезпечує швидкісний інтернет та комплексні телекомунікаційні рішення для дому та бізнесу.
        </p>
        <button class="btn btn-primary mt-4">Читати повністю</button>
      </div>
    </section>

    <!-- Services -->
    <section class="container mb-12" id="services">
      <h2 class="text-center h4 fw-bold mb-6">Наші послуги</h2>
      <div class="row g-4">
        <div class="col-6 col-md-4 col-lg-2" v-for="service in services" :key="service.title">
          <ServiceCard v-bind="service" />
        </div>
      </div>
    </section>

    <!-- Tariffs -->
    <section class="container mb-12" id="tariffs">
      <h2 class="text-center h4 fw-bold mb-6">Оберіть тариф для підключення</h2>

      <div class="row g-4 justify-content-center d-none d-md-flex">
        <div class="col-12 col-sm-6 col-lg-3" v-for="tariff in tariffs" :key="tariff.id">
          <TariffCard :tariff="tariff" :popular="tariff.popular" />
        </div>
      </div>

      <div class="d-md-none overflow-auto pb-3">
        <div class="d-flex gap-3 p-2">
          <div v-for="tariff in tariffs" :key="tariff.id" style="min-width: 280px;">
            <TariffCard :tariff="tariff" :popular="tariff.popular" />
          </div>
        </div>
      </div>
    </section>

    <!-- Address Check -->
    <section class="bg-light-blue py-10">
      <div class="container">
        <ContactForm />
      </div>
    </section>

    <!-- Promo -->
    <section class="container mb-12">
      <PromoBanner />
    </section>

    <!-- Features -->
    <section class="container mb-12">
      <h2 class="h4 fw-bold mb-6">Чому обирають нас?</h2>
      <div class="feature-card" v-for="feature in features" :key="feature.title">
        <div class="icon"><i :class="feature.icon"></i></div>
        <div class="content">
          <h5>{{ feature.title }}</h5>
          <p class="text-muted">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="container mb-12">
      <h2 class="h4 fw-bold mb-6">Поширені питання</h2>
      <FaqItem question="Як швидко можна підключитися?">
        Підключення відбувається протягом 24 годин після подачі заявки.
      </FaqItem>
      <FaqItem question="Чи потрібна передоплата?">
        Ні, оплата за інтернет — після підключення, до 10 числа кожного місяця.
      </FaqItem>
      <FaqItem question="Як поповнити рахунок?">
        Через особистий кабінет, карткою онлайн або в касі.
      </FaqItem>
    </section>

    <!-- CTA -->
    <section class="bg-dark-blue text-white text-center py-10" id="contact">
      <div class="container">
        <h2 class="h4 fw-bold">Залишились питання?</h2>
        <p>Наші консультанти допоможуть обрати найкращий тариф</p>
        <button class="btn btn-light mt-3">Зв’язатися</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import ServiceCard from '@/components/ServiceCard.vue'
import TariffCard from '@/components/TariffCard.vue'
import ContactForm from '@/components/ContactForm.vue'
import PromoBanner from '@/components/PromoBanner.vue'
import FeatureCard from '@/components/FeatureCard.vue'
import FaqItem from '@/components/FaqItem.vue'

// Услуги (как на simnet.ua)
const services = [
  { title: 'Інтернет', description: 'Безперервний доступ до інформації, розваг та зв\'язку з високою швидкістю завантаження', icon: '/src/assets/icons/internet.png' },
  { title: 'Інтернет + ТБ', description: 'Швидкий та надійний Інтернет разом із великим вибором телевізійних каналів для всієї сім’ї', icon: '/src/assets/icons/internet-tv.png' },
  { title: 'Телебачення', description: 'Безліч улюблених каналів у високій якості звуку та зображення з підключенням від Simnet', icon: '/src/assets/icons/tv.png' },
  { title: 'ДОМОФОНІЯ', description: 'Зручне керування доступом для гостей та підвищений рівень безпеки для вашої родини', icon: '/src/assets/icons/intercom.png' },
  { title: 'Відеонагляд', description: 'Повний контроль та безпека за будинком за допомогою наших систем відеонагляду', icon: '/src/assets/icons/video.png' },
]

// Тарифы (аналогично happylink.net.ua)
const tariffs = [
  { id: 1, name: 'Базовий', speed: 100, price: 180, features: ['Wi-Fi роутер', 'Техпідтримка 24/7'], popular: false },
  { id: 2, name: 'Стандарт', speed: 200, price: 250, features: ['Wi-Fi 6', 'Пріоритет у підтримці', 'IPTV 150+ каналів'], popular: true },
  { id: 3, name: 'Максимум', speed: 500, price: 380, features: ['Оптоволокно', 'VIP-обслуговування', 'IPTV 300+ каналів'], popular: false },
  { id: 4, name: 'Гігабіт', speed: 1000, price: 550, features: ['Гігабіт', 'Резервний канал', 'Безліміт'], popular: false }
]

// Преимущества
const features = [
  { icon: 'bi-shield-check', title: 'Надійність', description: 'Ми гарантуємо стабільну роботу інтернету 24/7' },
  { icon: 'bi-speedometer2', title: 'Швидкість', description: 'Наша мережа побудована на сучасному обладнанні' },
  { icon: 'bi-headset', title: 'Підтримка', description: 'Техпідтримка працює цілодобово' },
  { icon: 'bi-cash', title: 'Чесні тарифи', description: 'Без прихованих платежів та комісій' }
]
</script>
```

---

## ✅ 16. `src/App.vue`

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
```

---

## ✅ Как запустить

```bash
npm install
npm run dev
```

## ✅ Деплой на GitHub Pages

```bash
npm run deploy
```

> Убедитесь, что в `package.json` указано:
> ```json
> "homepage": "https://ваш-юзер.github.io/simnet-clone"
> ```

---
