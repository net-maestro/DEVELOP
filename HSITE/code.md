✅ Украинский язык  
✅ Минимализм и современный дизайн (как у simnet.ua)  
✅ Шрифт **Inter**  
✅ Адаптивность: **горизонтальная прокрутка тарифов на мобильных**  
✅ Калькулятор скорости + **выбор IPTV с динамической ценой**  
✅ Убран весь легаси-код  
✅ Готов к выкладке на GitHub и внедрению  

---

📁 Структура проекта (стандартный Vue 3 + Vite + Vuetify 3)

```
src/
├── plugins/
│   └── vuetify.js
├── components/
│   ├── Navbar.vue
│   ├── Footer.vue
│   ├── TariffCard.vue
│   └── ContactForm.vue
├── views/
│   ├── HomeView.vue
│   └── AboutView.vue
├── assets/
│   └── logo.svg
├── styles/
│   └── main.scss
└── App.vue
public/
└── index.html
```

---

## ✅ 1. `public/index.html`

```html
<!DOCTYPE html>
<html lang="uk">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
    <title>NetHUB — Швидкий інтернет</title>
  </head>
  <body>
    <div id="app"></div>
  </body>
</html>
```

---

## ✅ 2. `src/plugins/vuetify.js`

```js
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const lightTheme = {
  dark: false,
  colors: {
    primary: '#2A5DFF',
    secondary: '#F5F7FA',
    accent: '#FFB300',
    error: '#B00020',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
    background: '#FFFFFF',
    'on-background': '#000000',
    'on-surface': '#000000',
  },
};

const customTypescale = {
  'h1': { fontSize: '2.5rem', lineHeight: 1.2, fontWeight: '700', letterSpacing: '-0.02em', fontFamily: 'Inter, sans-serif' },
  'h2': { fontSize: '2rem', lineHeight: 1.25, fontWeight: '700', letterSpacing: '-0.02em', fontFamily: 'Inter, sans-serif' },
  'h3': { fontSize: '1.5rem', lineHeight: 1.3, fontWeight: '600', fontFamily: 'Inter, sans-serif' },
  'h4': { fontSize: '1.25rem', lineHeight: 1.4, fontWeight: '600', fontFamily: 'Inter, sans-serif' },
  'body-large': { fontSize: '1rem', lineHeight: 1.6, fontFamily: 'Inter, sans-serif' },
  'body-medium': { fontSize: '0.875rem', lineHeight: 1.5, fontFamily: 'Inter, sans-serif' },
};

export const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'lightTheme',
    themes: {
      lightTheme,
    },
  },
  defaults: {
    VCard: { variant: 'flat', rounded: 'lg', elevation: 2 },
    VBtn: { color: 'primary', rounded: 'pill', variant: 'flat' },
    VTextField: { variant: 'outlined', density: 'comfortable', color: 'primary' },
    VTextarea: { variant: 'outlined', color: 'primary' },
    VSwitch: { color: 'primary', inset: false },
  },
  typescale: customTypescale,
});
```

---

## ✅ 3. `src/components/Navbar.vue`

```vue
<template>
  <v-app-bar flat>
    <v-container class="d-flex align-center">
      <v-img src="@/assets/logo.svg" max-height="40" max-width="40" class="me-2"></v-img>
      <span class="text-h6 font-weight-bold">NetHUB</span>
      <v-spacer></v-spacer>
      <v-btn text href="#home">Головна</v-btn>
      <v-btn text href="#tariffs">Тарифи</v-btn>
      <v-btn text href="#contact">Контакти</v-btn>
    </v-container>
  </v-app-bar>
</template>
```

---

## ✅ 4. `src/components/Footer.vue`

```vue
<template>
  <v-footer class="bg-grey-lighten-4 py-6">
    <v-container>
      <div class="text-center text-body-2 text-grey">
        &copy; 2025 NetHUB — Швидкий інтернет по Україні
      </div>
    </v-container>
  </v-footer>
</template>
```

---

## ✅ 5. `src/components/TariffCard.vue`

```vue
<template>
  <v-card>
    <div v-if="tariff.popular" class="pa-1 bg-primary text-white text-caption rounded-pill d-inline-block mb-2">
      Популярно
    </div>

    <h3 class="text-h6 font-weight-bold mb-2">{{ tariff.name }}</h3>
    <p class="text-h4 font-weight-bold text-primary mb-1">
      {{ tariff.speed }} <small class="text-body-2">Мбіт/с</small>
    </p>
    <p class="text-body-1 text-grey mb-4">від {{ tariff.price }} ₴/міс</p>

    <v-divider class="mb-4"></v-divider>

    <ul class="list-unstyled text-body-2 mb-4 px-2 text-start">
      <li v-for="(feature, i) in tariff.features" :key="i" class="mb-1 d-flex align-center">
        <v-icon size="small" color="primary" icon="mdi-check" class="me-2"></v-icon>
        {{ feature }}
      </li>
    </ul>

    <v-btn size="large" block>{{ tariff.popular ? 'Найкращий вибір' : 'Підключити' }}</v-btn>
  </v-card>
</template>

<script setup>
defineProps({
  tariff: { type: Object, required: true },
});
</script>

<style scoped>
.list-unstyled {
  list-style: none;
  padding: 0;
}
</style>
```

---

## ✅ 6. `src/components/ContactForm.vue`

```vue
<template>
  <v-form v-model="valid" @submit.prevent="submit" class="mx-auto" max-width="500">
    <v-text-field v-model="name" label="Ім’я" :rules="[v => !!v || 'Обов’язково']"></v-text-field>
    <v-text-field v-model="phone" label="Телефон" :rules="[v => !!v || 'Обов’язково']"></v-text-field>
    <v-textarea v-model="message" label="Повідомлення" auto-grow rows="3"></v-textarea>
    <v-btn type="submit" color="primary" block size="large" :loading="loading">
      Надіслати
    </v-btn>
    <p v-if="success" class="text-success mt-4 text-body-2">
      Дякуємо! Ми зв’яжемося з вами найближчим часом.
    </p>
  </v-form>
</template>

<script setup>
import { ref } from 'vue';

const valid = ref(false);
const loading = ref(false);
const success = ref(false);
const name = ref('');
const phone = ref('');
const message = ref('');

const submit = async () => {
  if (!valid.value) return;
  loading.value = true;
  await new Promise(r => setTimeout(r, 1500));
  loading.value = false;
  success.value = true;
  setTimeout(() => success.value = false, 5000);
};
</script>
```

---

## ✅ 7. `src/views/HomeView.vue` (с IPTV и калькулятором)

```vue
<template>
  <div id="home">
    <v-container class="py-10" fluid>
      <!-- Заголовок -->
      <div class="text-center mb-12 px-4">
        <h1 class="text-h4 text-md-h3 font-weight-bold mb-4">
          Швидкий і надійний інтернет для дому та офісу
        </h1>
        <p class="text-body-1 text-grey">Підключіться за 24 години. Без комісій та прихованих платежів.</p>
      </div>

      <!-- Калькулятор -->
      <v-sheet id="tariffs" class="bg-secondary pa-6 rounded-lg mb-12 mx-auto" max-width="800">
        <h2 class="text-h6 font-weight-bold mb-4 text-center">Підберіть тариф під себе</h2>

        <!-- Швидкість -->
        <p class="text-center mb-2"><strong>{{ speed }} Мбіт/с</strong></p>
        <v-slider
          v-model="speed"
          :min="10"
          :max="1000"
          step="10"
          color="primary"
          track-color="accent"
          hide-details
          class="px-4"
        ></v-slider>
        <div class="d-flex justify-space-between text-caption text-grey mt-2">
          <span>10 Мбіт/с</span>
          <span>1000 Мбіт/с</span>
        </div>

        <!-- IPTV -->
        <div class="mt-6 text-center">
          <v-switch
            v-model="iptvEnabled"
            color="primary"
            label="Підключити IPTV (+50 ₴/міс)"
            hide-details
          ></v-switch>
        </div>
      </v-sheet>

      <!-- Тарифи -->
      <v-sheet color="transparent">
        <v-slide-group
          v-if="$vuetify.display.mobile"
          show-arrows
          center-active
          class="pa-2"
        >
          <v-slide-group-item
            v-for="tariff in filteredTariffs"
            :key="tariff.id"
            v-slot="{ isActive }"
          >
            <div class="pa-1">
              <TariffCard
                :tariff="tariff"
                :class="{ 'scale-card': isActive }"
                max-width="320"
              />
            </div>
          </v-slide-group-item>
        </v-slide-group>

        <v-row v-else justify="center" class="px-4">
          <v-col
            v-for="tariff in filteredTariffs"
            :key="tariff.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <TariffCard :tariff="tariff" />
          </v-col>
        </v-row>
      </v-sheet>

      <!-- Контакти -->
      <div id="contact" class="text-center mt-16 px-4">
        <h2 class="text-h5 font-weight-bold mb-6">Потрібна консультація?</h2>
        <ContactForm />
      </div>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import TariffCard from '@/components/TariffCard.vue';
import ContactForm from '@/components/ContactForm.vue';

const speed = ref(100);
const iptvEnabled = ref(false);

const baseTariffs = [
  { id: 1, name: 'Базовий', speed: 30, basePrice: 150, features: ['Wi-Fi роутер', 'Техпідтримка'], popular: false },
  { id: 2, name: 'Стандарт', speed: 100, basePrice: 250, features: ['Wi-Fi 6', 'Пріоритет у підтримці'], popular: true },
  { id: 3, name: 'Максимум', speed: 500, basePrice: 400, features: ['Оптоволокно', 'Підтримка 24/7', 'Безліміт'], popular: false },
  { id: 4, name: 'Гігабіт', speed: 1000, basePrice: 600, features: ['Гігабіт', 'VIP-обслуговування', 'Резервний канал'], popular: false },
];

const filteredTariffs = computed(() => {
  const iptvCost = iptvEnabled.value ? 50 : 0;
  return baseTariffs
    .filter(t => t.speed >= speed.value)
    .map(t => ({
      ...t,
      price: t.basePrice + iptvCost,
      features: [
        ...t.features,
        iptvEnabled.value ? 'IPTV (300+ каналів)' : null,
      ].filter(Boolean),
    }));
});
</script>

<style scoped>
.scale-card {
  transform: scale(1.05);
  z-index: 1;
}
</style>
```

---

## ✅ 8. `src/views/AboutView.vue` (опционально)

```vue
<template>
  <v-container class="py-12" fluid>
    <h1 class="text-h4 font-weight-bold text-center mb-6">Про нас</h1>
    <p class="text-body-1 text-center px-4">
      NetHUB — це сучасний інтернет-провайдер, який пропонує високу швидкість, стабільність та чесні тарифи без прихованих платежів.
    </p>
  </v-container>
</template>
```

---

## ✅ 9. `src/App.vue`

```vue
<script setup>
import { RouterView } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
</script>

<template>
  <Navbar />
  <RouterView />
  <Footer />
</template>
```
---

## ✅ Что дальше?

- Добавить **PWA** (работает оффлайн)
- Подключить **Firebase / Telegram-бота** для заявок
- Сделать **мультирегиональность** (выбор города → тарифы)
- Добавить **анимации появления блоков**
- Выложить на **Vercel / Netlify** бесплатно

---
