

---

### ✅ Требования реализованы:
- 🇺🇦 Украинский язык  
- 🎨 Минимализм и современный дизайн (как у simnet.ua)  
- 🖋️ Шрифт **Inter**  
- 📱 Адаптивность: **горизонтальная прокрутка тарифов на мобильных**  
- 🧮 Калькулятор скорости + **выбор IPTV с динамической ценой**  
- 💣 Убран весь легаси-код  
- 🚀 Готов к выкладке на GitHub  
- 🧱 Используется **только HTML + CSS + JS + Bootstrap 5**  

---

## 📁 Структура проекта (чистый Bootstrap)

```
nethub-bootstrap/
├── src/
│   ├── components/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   ├── tariff-card.html
│   │   └── contact-form.html
│   ├── views/
│   │   ├── home.html
│   │   └── about.html
│   ├── assets/
│   │   └── logo.svg
│   ├── styles/
│   │   └── main.css
│   └── index.html
└── public/
    └── index.html
```

> 💡 Примечание: `src/` используется для удобства организации кода, как в фронтенд-проектах. В финальной сборке можно скопировать всё в корень.

---

## ✅ 1. `public/index.html` (финальная точка входа)

```html
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="../src/styles/main.css" />
  <title>NetHUB — Швидкий інтернет</title>
</head>
<body>

  <!-- Вставляем Navbar -->
  <div w3-include-html="../src/components/navbar.html"></div>

  <!-- Основной контент -->
  <div w3-include-html="../src/views/home.html"></div>

  <!-- Вставляем Footer -->
  <div w3-include-html="../src/components/footer.html"></div>

  <!-- Подключаем JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  <script src="../src/js/calculator.js"></script>
  <script src="../src/js/include-html.js"></script>

</body>
</html>
```

> 🔁 Мы используем `w3-include-html` для имитации компонентов. Альтернатива — собрать через простой `concat` или использовать статический генератор.

---

## ✅ 2. `src/components/navbar.html`

```html
<nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
  <div class="container">
    <a class="navbar-brand d-flex align-items-center" href="../public/index.html">
      <img src="../src/assets/logo.svg" alt="Logo" width="40" height="40" class="me-2">
      <span class="fw-bold fs-5">NetHUB</span>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <div class="ms-auto">
        <a class="nav-link" href="#home">Головна</a>
        <a class="nav-link" href="#tariffs">Тарифи</a>
        <a class="nav-link" href="#contact">Контакти</a>
      </div>
    </div>
  </div>
</nav>
```

---

## ✅ 3. `src/components/footer.html`

```html
<footer class="bg-light py-6 mt-12">
  <div class="container text-center text-secondary small">
    &copy; 2025 NetHUB — Швидкий інтернет по Україні
  </div>
</footer>
```

---

## ✅ 4. `src/components/tariff-card.html`

> Это **шаблон**, используется в JS. Нельзя вставить напрямую как HTML-файл, но используется как шаблон карточки.

```html
<!-- Этот файл — шаблон. Используется в calculator.js -->
<div class="tariff-card">
  <h3 class="tariff-name"></h3>
  <p class="speed"><strong></strong> <small>Мбіт/с</small></p>
  <p class="price">від <strong></strong> ₴/міс</p>
  <hr>
  <ul class="features"></ul>
  <button class="btn btn-primary w-100"></button>
</div>
```

---

## ✅ 5. `src/components/contact-form.html`

```html
<form class="mx-auto" style="max-width: 500px;" id="contactForm">
  <div class="mb-3">
    <input type="text" class="form-control" placeholder="Ім’я" required id="name">
  </div>
  <div class="mb-3">
    <input type="tel" class="form-control" placeholder="Телефон" required id="phone">
  </div>
  <div class="mb-3">
    <textarea class="form-control" rows="3" placeholder="Повідомлення" id="message"></textarea>
  </div>
  <button type="submit" class="btn btn-primary w-100" id="submitBtn">Надіслати</button>
  <p id="successMsg" class="text-success mt-3 d-none">Дякуємо! Ми зв’яжемося з вами найближчим часом.</p>
</form>
```

---

## ✅ 6. `src/views/home.html`

```html
<main id="home">
  <div class="container py-10">

    <!-- Hero -->
    <div class="text-center mb-12 px-4">
      <h1 class="display-5 display-md-4 fw-bold mb-4">
        Швидкий і надійний інтернет для дому та офісу
      </h1>
      <p class="text-muted">Підключіться за 24 години. Без комісій та прихованих платежів.</p>
    </div>

    <!-- Калькулятор -->
    <section class="bg-light p-6 rounded-4 mb-12 mx-auto" style="max-width: 800px;" id="tariffs">
      <h2 class="h6 fw-bold mb-4 text-center">Підберіть тариф під себе</h2>

      <p class="text-center mb-2"><strong id="speedValue">100</strong> Мбіт/с</p>
      <input type="range" class="form-range px-4" id="speedSlider" min="10" max="1000" step="10" value="100">

      <div class="d-flex justify-content-between text-secondary small mt-2 px-4">
        <span>10 Мбіт/с</span>
        <span>1000 Мбіт/с</span>
      </div>

      <div class="mt-6 text-center">
        <div class="form-check form-switch d-inline-block">
          <input class="form-check-input" type="checkbox" id="iptvSwitch">
          <label class="form-check-label" for="iptvSwitch">Підключити IPTV (+50 ₴/міс)</label>
        </div>
      </div>
    </section>

    <!-- Тарифи: Desktop -->
    <section class="d-none d-md-block text-center">
      <div class="row g-4" id="tariffGridDesktop"></div>
    </section>

    <!-- Тарифы: Mobile (горизонтальная прокрутка) -->
    <section class="d-md-none overflow-auto pb-3" id="mobileTariffsContainer">
      <div class="d-flex gap-3 p-2" id="mobileTariffs"></div>
    </section>

    <!-- Контакты -->
    <section id="contact" class="text-center mt-16 px-4">
      <h2 class="h5 fw-bold mb-6">Потрібна консультація?</h2>
      <div w3-include-html="../src/components/contact-form.html"></div>
    </section>

  </div>
</main>
```

---

## ✅ 7. `src/views/about.html`

```html
<div class="container py-12">
  <h1 class="display-6 fw-bold text-center mb-6">Про нас</h1>
  <p class="text-muted text-center px-4">
    NetHUB — це сучасний інтернет-провайдер, який пропонує високу швидкість, стабільність та чесні тарифи без прихованих платежів.
  </p>
</div>
```

---

## ✅ 8. `src/styles/main.css`

```css
body {
  font-family: 'Inter', sans-serif;
}

.py-10 {
  padding-top: 4rem;
  padding-bottom: 4rem;
}

.px-4 {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.mb-12 {
  margin-bottom: 3rem;
}

.mt-16 {
  margin-top: 4rem;
}

.bg-light {
  background-color: #F5F7FA !important;
}

.p-6 {
  padding: 2rem;
}

.rounded-4 {
  border-radius: 1rem;
}

.tariff-card {
  min-width: 300px;
  max-width: 320px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  background: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.tariff-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

.tariff-card.popular {
  border: 2px solid #2A5DFF;
  position: relative;
}

.tariff-card.popular::before {
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

.tariff-card h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.tariff-card .speed {
  font-size: 2rem;
  font-weight: 700;
  color: #2A5DFF;
  margin: 0.25rem 0;
}

.tariff-card .price {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
}

.tariff-card ul {
  list-style: none;
  padding: 0;
  margin-bottom: 1.5rem;
}

.tariff-card ul li {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.tariff-card ul li::before {
  content: "✓";
  color: #2A5DFF;
  font-weight: bold;
  margin-right: 8px;
}

.tariff-card button {
  padding: 12px;
  font-weight: 500;
  border-radius: 50px;
}

input[type="range"] {
  accent-color: #2A5DFF;
}
```

---

## ✅ 9. `src/js/calculator.js`

```javascript
// Тарифи
const baseTariffs = [
  { id: 1, name: 'Базовий', speed: 30, basePrice: 150, features: ['Wi-Fi роутер', 'Техпідтримка'], popular: false },
  { id: 2, name: 'Стандарт', speed: 100, basePrice: 250, features: ['Wi-Fi 6', 'Пріоритет у підтримці'], popular: true },
  { id: 3, name: 'Максимум', speed: 500, basePrice: 400, features: ['Оптоволокно', 'Підтримка 24/7', 'Безліміт'], popular: false },
  { id: 4, name: 'Гігабіт', speed: 1000, basePrice: 600, features: ['Гігабіт', 'VIP-обслуговування', 'Резервний канал'], popular: false }
];

// DOM
const speedSlider = document.getElementById('speedSlider');
const speedValue = document.getElementById('speedValue');
const iptvSwitch = document.getElementById('iptvSwitch');
const tariffGridDesktop = document.getElementById('tariffGridDesktop');
const mobileTariffs = document.getElementById('mobileTariffs');

// Обновление тарифів
function updateTariffs() {
  const speed = parseInt(speedSlider.value);
  const iptvEnabled = iptvSwitch.checked;
  const iptvCost = iptvEnabled ? 50 : 0;

  const filtered = baseTariffs
    .filter(t => t.speed >= speed)
    .map(t => ({
      ...t,
      price: t.basePrice + iptvCost,
      features: [
        ...t.features,
        iptvEnabled ? 'IPTV (300+ каналів)' : null
      ].filter(Boolean)
    }));

  // Очистка
  if (tariffGridDesktop) tariffGridDesktop.innerHTML = '';
  if (mobileTariffs) mobileTariffs.innerHTML = '';

  // Генерация карточек
  filtered.forEach(tariff => {
    const card = createTariffCard(tariff);
    if (tariffGridDesktop) {
      const col = document.createElement('div');
      col.className = 'col';
      col.appendChild(card);
      tariffGridDesktop.appendChild(col);
    }

    if (mobileTariffs) {
      const wrapper = document.createElement('div');
      wrapper.className = 'flex-shrink-0';
      wrapper.style.width = '300px';
      wrapper.appendChild(card);
      mobileTariffs.appendChild(wrapper);
    }
  });
}

// Создание карточки
function createTariffCard(tariff) {
  const card = document.createElement('div');
  card.className = `tariff-card ${tariff.popular ? 'popular' : ''}`;

  const featuresHTML = tariff.features.map(f => `<li>${f}</li>`).join('');

  card.innerHTML = `
    <h3>${tariff.name}</h3>
    <p class="speed">${tariff.speed}</p>
    <p class="price">${tariff.price}</p>
    <hr>
    <ul class="features">${featuresHTML}</ul>
    <button class="btn btn-primary">
      ${tariff.popular ? 'Найкращий вибір' : 'Підключити'}
    </button>
  `;

  return card;
}

// Скорость
speedSlider?.addEventListener('input', () => {
  speedValue.textContent = speedSlider.value;
  updateTariffs();
});

// IPTV
iptvSwitch?.addEventListener('change', updateTariffs);

// Форма
const contactForm = document.getElementById('contactForm');
const submitBtn = document.getElementById('submitBtn');
const successMsg = document.getElementById('successMsg');

contactForm?.addEventListener('submit', function (e) {
  e.preventDefault();
  submitBtn.disabled = true;
  submitBtn.textContent = 'Надсилається...';

  setTimeout(() => {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Надіслано';
    successMsg.classList.remove('d-none');

    setTimeout(() => {
      contactForm.reset();
      successMsg.classList.add('d-none');
      submitBtn.textContent = 'Надіслати';
    }, 3000);
  }, 1500);
});

// Первый рендер
if (speedSlider) updateTariffs();
```

---

## ✅ 10. `src/js/include-html.js` (для компонентов)

```javascript
// Простой аналог <include> для HTML-фрагментов
document.addEventListener("DOMContentLoaded", function () {
  const includeHTML = (el, url) => {
    fetch(url)
      .then(r => r.text())
      .then(data => {
        el.outerHTML = data;
        // После вставки — перезапускаем калькулятор
        if (url.includes('home.html')) {
          setTimeout(() => {
            if (typeof updateTariffs === 'function') updateTariffs();
          }, 100);
        }
      });
  };

  const elements = document.querySelectorAll("[w3-include-html]");
  elements.forEach(el => {
    includeHTML(el, el.getAttribute("w3-include-html"));
  });
});
```

---

## ✅ Что дальше?

1. **Собрать проект**:
   - Скопируйте всё из `src/` в `public/` или используйте простой скрипт:
     ```bash
     cp src/views/home.html public/index.html
     # и так далее, или использовать npm run build
     ```

2. **Запустить локально**:
   ```bash
   npx serve public
   ```

3. **Залить на GitHub Pages**:
   - Положите всё в репозиторий
   - Settings → Pages → ветка `main`, папка `/public`

4. **Добавить PWA / Telegram / Анимации** — как в предыдущем ответе.

---
