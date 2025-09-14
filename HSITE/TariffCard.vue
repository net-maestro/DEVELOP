<template>
  <div class="tariff-section">
    <!-- Переключатель типов -->
    <div class="tariff-switcher">
      <button
        v-for="(type, key) in switchTypes"
        :key="key"
        :class="['btn', { active: activeType === key }]"
        @click="activeType = key"
      >
        <span v-if="type.icon" class="icon">{{ type.icon }}</span>
        {{ type.label }}
      </button>
    </div>

    <!-- Карусель тарифов -->
    <swiper
      :slides-per-view="1.2"
      :space-between="20"
      :breakpoints="{
        640: { slidesPerView: 1.8 },
        768: { slidesPerView: 2.5 },
        1024: { slidesPerView: 3.5 },
        1200: { slidesPerView: 4 }
      }"
      :navigation="true"
      :pagination="{ clickable: true }"
      :loop="false"
      :grab-cursor="true"
      class="tariff-slider"
    >
      <swiper-slide
        v-for="(tariff, index) in filteredTariffs"
        :key="index"
        class="tariff-card"
      >
        <div class="card-header">
          <h3 class="card-title">{{ tariff.name }}</h3>
          <div class="speed-badge" v-if="tariff.speed">
            <span class="speed-number">{{ tariff.speed }}</span>
            <span class="speed-unit">Мбіт</span>
          </div>
        </div>

        <div class="card-body">
          <!-- Опции -->
          <ul class="options-list">
            <li v-for="(option, i) in tariff.options" :key="i">
              <span>{{ option.text }}</span>
              <span :class="['check', option.available ? 'yes' : 'no']"></span>
            </li>
          </ul>

          <!-- Подключение -->
          <div class="connect-options">
            <span class="label">Підключення:</span>
            <div class="connect-buttons">
              <button
                v-for="conn in tariff.connections"
                :key="conn.type"
                :class="['connect-btn']"
                @click="selectConnection(conn.type)"
              >
                {{ conn.type }}
              </button>
            </div>
          </div>

          <!-- Цена -->
          <div class="price-block">
            <div class="price-current">{{ tariff.price }} ₴</div>
          </div>
        </div>

        <div class="card-footer">
          <button class="btn order-btn" @click="order(tariff)">Замовити</button>
        </div>
      </swiper-slide>
    </swiper>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'

// Пример данных
const tariffs = [
  {
    name: 'STANDART',
    speed: 100,
    options: [
      { text: 'Опція 1', available: false },
      { text: 'Опція 2', available: true },
    ],
    connections: [{ type: 'Ethernet' }, { type: 'GPON' }],
    price: 100,
  },
  {
    name: 'GIGABIT',
    speed: 1000,
    options: [
      { text: 'Опція 1', available: true },
      { text: 'Опція 2', available: true },
    ],
    connections: [{ type: 'Ethernet' }, { type: 'GPON' }],
    price: 200,
  },
]

const switchTypes = {
  multi: { label: 'Багатоквартирні', icon: '🏢' },
  private: { label: 'Приватні', icon: '🏠' },
}

const activeType = ref('multi')

const filteredTariffs = computed(() => {
  return tariffs
})

const selectConnection = (type) => {
  console.log('Выбрано:', type)
}

const order = (tariff) => {
  alert(`Вы замовили тариф ${tariff.name}`)
}
</script>

<style scoped>
.tariff-section {
  padding: 20px;
  background-color: #f5f5f5;
}

.tariff-switcher {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tariff-switcher .btn {
  padding: 10px 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.tariff-switcher .btn.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.tariff-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.tariff-card:hover {
  transform: translateY(-5px);
}

.card-header {
  background: #1a1a1a;
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.speed-number {
  font-size: 28px;
  font-weight: bold;
  color: white;
}

.speed-unit {
  font-size: 14px;
  color: #ccc;
}

.card-body {
  padding: 16px;
  background: #f9f9f9;
}

.options-list {
  list-style: none;
  padding: 0;
  margin: 10px 0;
}

.options-list li {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
  font-size: 14px;
}

.check {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.check.yes {
  background: #4CAF50;
}

.check.no {
  background: #ddd;
}

.connect-options {
  margin: 10px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.connect-buttons {
  display: flex;
  gap: 8px;
}

.connect-btn {
  padding: 6px 12px;
  border: 1px solid #4CAF50;
  border-radius: 4px;
  background: white;
  color: #4CAF50;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
}

.price-block {
  margin: 16px 0;
  text-align: center;
}

.price-current {
  font-size: 20px;
  font-weight: bold;
  color: #e91e63;
}

.card-footer {
  display: flex;
  padding: 16px;
  background: #f9f9f9;
  border-top: 1px solid #eee;
}

.order-btn {
  flex: 1;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px;
  font-size: 14px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .tariff-switcher {
    flex-direction: column;
  }
  .tariff-switcher .btn {
    width: 100%;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .card-header {
    flex-direction: column;
    text-align: center;
  }
}
</style>
