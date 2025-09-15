<template>
 <v-container>
     <div class="tariffs-section">
    <h2 class="section-title" v-if="$vuetify.display.mdAndUp">
      {{ $t("menu.internet") }}
    </h2>

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
      :slides-per-view="1.15"
      :space-between="16"
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
        class="tariff-slide"
      >
        <div
          :class="[
            'tariff-card card-hover pa-6 card-animate',
            getTariffClass(tariff.name)
          ]"
          class="tariff-card"
        >
          <!-- Акцентная полоса -->
          <div class="accent-bar" :class="getAccentClass(tariff.name)"></div>

          <!-- Заголовок с иконкой -->
          <div class="text-center mb-1">
              <!-- Иконка -->
  <v-icon
    :icon="tariff.icon"
    :size="40"
    :color="getIconColor(tariff.name)"
    class="me-2"
  ></v-icon>
            <h3 class="tariff-title text-h5 font-weight-bold">
              {{ tariff.name }}
            </h3>
          </div>

          <!-- Цена и скорость -->
          <div class="price-section text-center mb-1">
            <div class="price-display d-flex justify-center align-center mb-2">
              <span class="currency">₴</span>
              <span class="amount text-h3 font-weight-bold mx-1">{{ tariff.price }}</span>
              <span class="frequency text-body-1">/{{ $t("prices.month") }}</span>
            </div>
            <div class="speed text-body-1">
              <span class="speed-icon">🌐</span>
              {{ $t("prices.up-to") }} {{ tariff.speed }} {{ $t("prices.Mbps") }}
            </div>
          </div>

          <div class="divider mb-2"></div>

          <!-- Батарейка / автономность -->
          <div class="battery-section mb-1" v-if="tariff.batteryText">
            <div class="battery-container">
              <div class="battery-fill" :style="{ width: tariff.chargeLevel + '%' }"></div>
            </div>
            <p class="battery-text">{{ tariff.batteryText }}</p>
          </div>

          <!-- Внешний IP -->
          <div class="option-section mb-1 py-3 px-4 rounded-lg" style="background-color: #f5f5f5;">
            <label class="switch-label">
              <input
                type="checkbox"
                v-model="tariff.externalIpEnabled"
                class="switch-input"
              />
              <span class="switch-slider"></span>
              {{ $t('prices.external-ip') }}
              <span v-if="tariff.externalIpPrice > 0" class="price-additional">(+{{ tariff.externalIpPrice }} ₴)</span>
            </label>
          </div>

          <!-- IPTV -->
          <template v-if="tariff.iptv">
            <div class="option-section mb-1 py-3 px-4 rounded-lg" style="background-color: #f5f5f5;">
              <label class="switch-label">
                <input
                  type="checkbox"
                  v-model="iptvEnabled"
                  class="switch-input"
                />
                <span class="switch-slider"></span>
                + IPTV
                <img
                  src="@/assets/prices/logo_sweettv_light.svg"
                  alt="Sweet.TV"
                  class="iptv-logo"
                  width="60"
                  height="30"
                />
              </label>

              <div v-if="iptvEnabled" class="iptv-options mt-2">
                <div
                  v-for="iptvTariff in iptvTariffs"
                  :key="iptvTariff.id"
                  class="iptv-option"
                  :class="{ 'selected': selectedIptvTariff?.id === iptvTariff.id }"
                  @click="selectIptvTariff(iptvTariff)"
                >
                  <span>{{ iptvTariff.name }} — {{ iptvTariff.tv_count }} каналів</span>
                  <span class="iptv-price">+{{ iptvTariff.price }} ₴</span>
                  <span class="iptv-chip">{{ iptvTariff.tv_count }} TV</span>
                </div>
              </div>
            </div>
          </template>

          <!-- Итоговая цена -->
          <div
            v-if="totalPrice(tariff) >= 0"
            :class="['total-price-alert', getAlertColor(tariff.name)]"
            class="text-h6 font-weight-bold text-center py-3  rounded-lg"
            :style="{ borderLeftColor: getIconColor(tariff.name) }"
          >
            {{ $t("prices.total") }}: {{ tariff.price + totalPrice(tariff) }} ₴/{{ $t("prices.month") }}
          </div>

          <!-- Кнопка заказа -->
          <v-card-actions class="justify-center">
            <RequestForm
                :FormData="getFormData(tariff)"
                :ButtonTitle="$t('prices.to-buy')"
                :ButtonColor="getIconColor(tariff.name)"
                :ButtonIcon="'mdi-cart-outline'"
              />
          </v-card-actions>

        </div>
      </swiper-slide>
    </swiper>
  </div>
 </v-container>
</template>

<script>
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import RequestForm from '@/components/RequestForm.vue'

export default {
  name: "TestPrice",
  components: { Swiper, SwiperSlide, RequestForm },

  data() {
    return {
      // Типы тарифов для переключения
      switchTypes: {
        multi: { label: 'Для квартир', icon: '🏢' },
        private: { label: 'Приватний сектор', icon: '🏠' },
      },
      activeType: 'multi',

      // Основные тарифы
      internetTariffs: [
        // MULTI — для багатоквартирних будинків
        {
          id: 1,
          name: "«Економ»",
          speed: 50,
          price: 200,
          iptv: true,
          icon: "mdi-microsoft-internet-explorer",
          features: [],
          externalIpPrice: 75,
          externalIpEnabled: false,
          chargeLevel: 80,
          batteryText: "",
          type: 'multi'
        },
        {
          id: 2,
          name: "«Стандарт»",
          speed: 100,
          price: 250,
          iptv: true,
          icon: "mdi-wifi",
          features: [],
          externalIpPrice: 75,
          externalIpEnabled: false,
          chargeLevel: 80,
          batteryText: "",
          type: 'multi'
        },
        {
          id: 3,
          name: "«Люкс»",
          speed: 1000,
          price: 350,
          iptv: true,
          icon: "mdi-wifi-star",
          features: [],
          externalIpPrice: 0,
          externalIpEnabled: true,
          chargeLevel: 80,
          batteryText: "",
          type: 'multi'
        },

        // PRIVATE — PON для приватних будинків
        {
          id: 4,
          name: "«Хатинка»",
          speed: 50,
          price: 250,
          iptv: true,
          icon: "mdi-microsoft-internet-explorer",
          features: [],
          externalIpPrice: 50,
          externalIpEnabled: false,
          chargeLevel: 72,
          batteryText: "Працює без світла до 72 годин",
          type: 'private'
        },
        {
          id: 5,
          name: "«Дім»",
          speed: 100,
          price: 320,
          iptv: true,
          icon: "mdi-wifi",
          features: [],
          externalIpPrice: 50,
          externalIpEnabled: false,
          chargeLevel: 72,
          batteryText: "Працює без світла до 72 годин",
          type: 'private'
        },
        {
          id: 6,
          name: "«Маєток»",
          speed: 1000,
          price: 420,
          iptv: true,
          icon: "mdi-wifi-star",
          features: [],
          externalIpPrice: 0,
          externalIpEnabled: true,
          chargeLevel: 72,
          batteryText: "Працює без світла до 72 годин",
          type: 'private'
        },
      ],

      // IPTV тарифы
      iptvTariffs: [
        { id: 1, name: "S", tv_count: 245, price: 80 },
        { id: 2, name: "M", tv_count: 333, price: 120 },
        { id: 3, name: "L", tv_count: 347, price: 180 },
      ],

      // Локальные состояния
      iptvEnabled: false,
      selectedIptvTariff: null,
    }
  },

  computed: {
    filteredTariffs() {
      return this.internetTariffs.filter(tariff => tariff.type === this.activeType)
    }
  },

  methods: {
    selectIptvTariff(tariff) {
      this.selectedIptvTariff = tariff
    },

    totalPrice(tariff) {
      let total = 0
      if (tariff.externalIpEnabled) total += tariff.externalIpPrice
      if (tariff.iptv && this.iptvEnabled && this.selectedIptvTariff)
        total += this.selectedIptvTariff.price
      return total
    },

    getTariffClass(name) {
      switch (name) {
        case "«Економ»": return "economy-tariff"
        case "«Стандарт»": return "standard-tariff"
        case "«Люкс»": return "premium-tariff"
        case "«Хатинка»": return "economy-tariff"
        case "«Дім»": return "standard-tariff"
        case "«Маєток»": return "premium-tariff"
        default: return ""
      }
    },

    getAccentClass(name) {
      switch (name) {
        case "«Економ»": return "accent-economy"
        case "«Стандарт»": return "accent-standard"
        case "«Люкс»": return "accent-premium"
        case "«Хатинка»": return "accent-economy"
        case "«Дім»": return "accent-standard"
        case "«Маєток»": return "accent-premium"
        default: return ""
      }
    },

    getIconColor(name) {
      switch (name) {
        case "«Економ»": return "#4CAF50"
        case "«Стандарт»": return "#49CBD6"
        case "«Люкс»": return "#D9534F"
        case "«Хатинка»": return "#4CAF50"
        case "«Дім»": return "#49CBD6"
        case "«Маєток»": return "#D9534F"
        default: return "#2c3e50"
      }
    },

    getAlertColor(name) {
      switch (name) {
        case "«Економ»": return "green-lighten-1"
        case "«Стандарт»": return "teal-lighten-1"
        case "«Люкс»": return "red-lighten-1"
        case "«Хатинка»": return "green-lighten-1"
        case "«Дім»": return "teal-lighten-1"
        case "«Маєток»": return "red-lighten-1"
        default: return "teal-lighten-1"
      }
    },

    getFormData(tariff) {
      const selectedFeatures = tariff.features.filter(f => f).join(", ")
      const iptvText =
        tariff.iptv && this.iptvEnabled && this.selectedIptvTariff
          ? ` + IPTV (${this.selectedIptvTariff.name})`
          : ""
      const externalIpText = tariff.externalIpEnabled
        ? ` ${this.$t('prices.external-ip')}`
        : ""

      return `${this.$t("prices.rates")}: ${tariff.name} ${selectedFeatures}${iptvText} ${externalIpText} = ${this.$t("prices.total")}: ₴${tariff.price + this.totalPrice(tariff)} / ${this.$t("prices.month")}`
    }
  }
}
</script>

<style scoped>
.tariffs-section {
  padding: 40px 0;
  max-height: 700px; /* ФИКСИРОВАННАЯ МИНИМАЛЬНАЯ ВЫСОТА */
}
.tariff-slider{
  max-height: 800px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  text-align: center;
  color: #2c3e50;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 25px;
  position: relative;
}

.section-title::after {
  content: "";
  display: block;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #49CBD6, #26A69A);
  margin: 12px auto 0;
  border-radius: 2px;
}

.tariff-switcher {
  display: flex;
  gap: 10px;
  margin-top: -10px;
  margin-bottom: 10px;
  justify-content: center;
}

.tariff-switcher .btn {
  padding: 10px 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.tariff-switcher .btn.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.tariff-slide {
  height: auto;
}

.tariff-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #f0f0f0;
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  /* min-height: 580px; */
  display: flex;
  flex-direction: column;
}

.tariff-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.accent-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}

.accent-economy {
  background: linear-gradient(to bottom, #4CAF50, #388E3C);
}

.accent-standard {
  background: linear-gradient(to bottom, #49CBD6, #26A69A);
}

.accent-premium {
  background: linear-gradient(to bottom, #D9534F, #C12E27);
}

.tariff-icon {
  font-size: 48px;
  line-height: 1;
  margin-bottom: 8px;
}

.tariff-title {
  color: #2c3e50;
  line-height: 1.3;
  margin: 0;
  font-size: 1.5rem;
}

.price-section {
  background: #f8fbfa;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
}

.price-display {
  gap: 4px;
  align-items: baseline;
}

.currency {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.amount {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: bold;
}

.frequency {
  color: #666;
  font-size: 0.9rem;
}

.speed {
  color: #424242;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.speed-icon {
  font-size: 16px;
}

.divider {
  border: none;
  border-top: 1px solid #eee;
}

.battery-section {
  text-align: center;
  margin: 16px 0;
}

.battery-container {
  width: 100%;
  height: 12px;
  background-color: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  margin: 8px 0;
  position: relative;
}

.battery-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #388E3C);
  border-radius: 6px;
  transition: width 0.4s ease;
}

.battery-text {
  color: #555;
  font-size: 0.9rem;
  margin: 0;
}

.option-section {
  transition: all 0.2s ease;
  border-radius: 8px;
}

.option-section:hover {
  background: #f0f0f0;
}

.switch-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 12px;
  font-weight: 500;
  font-size: 14px;
}

.switch-input {
  display: none;
}

.switch-slider {
  width: 40px;
  height: 20px;
  background-color: #ccc;
  border-radius: 10px;
  position: relative;
  transition: 0.3s;
}

.switch-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: white;
  top: 1px;
  left: 1px;
  transition: 0.3s;
}

.switch-input:checked + .switch-slider {
  background-color: #4CAF50;
}

.switch-input:checked + .switch-slider::before {
  transform: translateX(20px);
}

.price-additional {
  color: #e91e63;
  font-weight: 500;
  margin-left: 8px;
}

.iptv-logo {
  margin-left: 8px;
  opacity: 0.8;
}

.iptv-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.iptv-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 14px;
}

.iptv-option:hover {
  background: #e8f5e8;
}

.iptv-option.selected {
  background: #e8f5e8;
  border: 1px solid #4CAF50;
}

.iptv-price {
  font-weight: bold;
  color: #e91e63;
}

.iptv-chip {
  background-color: #e8f5e8;
  color: #2e7d32;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: 8px;
}

.total-price-alert {
  background-color: #f8f9fa;
  border-left: 4px solid transparent;
  margin-top: auto;
  margin-bottom: 16px;
}

.green-lighten-1 {
  border-left-color: #4CAF50 !important;
}

.teal-lighten-1 {
  border-left-color: #49CBD6 !important;
}

.red-lighten-1 {
  border-left-color: #D9534F !important;
}

.card-actions {
  margin-top: auto;
  padding-top: 16px;
}

/* Кнопка RequestForm — она будет рендериться внутри */
</style>
