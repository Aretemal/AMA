<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

// Реактивные переменные
const message = ref('Привет из Composition API!')
const inputText = ref('')
const items = ref<string[]>([])
const timer = ref(0)

// Computed свойство
const reversedMessage = computed(() => {
  return message.value.split('').reverse().join('')
})

// Использование Pinia store
const counterStore = useCounterStore()

// Методы
function addItem() {
  if (inputText.value.trim()) {
    items.value.push(inputText.value)
    inputText.value = ''
  }
}

function removeItem(index: number) {
  items.value.splice(index, 1)
}

// Lifecycle hooks
let intervalId: number | undefined

onMounted(() => {
  intervalId = window.setInterval(() => {
    timer.value++
  }, 1000)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<template>
  <div class="composition-page">
    <h1>Composition API Page</h1>

    <section class="section">
      <h2>Реактивные данные</h2>
      <p>{{ message }}</p>
      <p>Перевернутое сообщение: {{ reversedMessage }}</p>
      <input v-model="message" type="text" placeholder="Измените сообщение" />
    </section>

    <section class="section">
      <h2>Pinia Store (Counter)</h2>
      <p>Счетчик: {{ counterStore.count }}</p>
      <p>Удвоенный счетчик: {{ counterStore.doubleCount }}</p>
      <button @click="counterStore.increment">Увеличить</button>
    </section>

    <section class="section">
      <h2>Список элементов</h2>
      <div class="input-group">
        <input v-model="inputText" @keyup.enter="addItem" type="text" placeholder="Добавить элемент" />
        <button @click="addItem">Добавить</button>
      </div>
      <ul v-if="items.length > 0">
        <li v-for="(item, index) in items" :key="index" class="list-item">
          {{ item }}
          <button @click="removeItem(index)" class="remove-btn">Удалить</button>
        </li>
      </ul>
      <p v-else>Список пуст</p>
    </section>

    <section class="section">
      <h2>Lifecycle Hooks</h2>
      <p>Таймер: {{ timer }} секунд</p>
    </section>
  </div>
</template>

<style scoped>
.composition-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #42b983;
  margin-bottom: 30px;
}

.section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

h2 {
  color: #2c3e50;
  margin-bottom: 15px;
}

input {
  padding: 8px 12px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
  max-width: 300px;
}

button {
  padding: 8px 16px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

button:hover {
  background: #35a372;
}

.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.input-group input {
  flex: 1;
  max-width: none;
}

ul {
  list-style: none;
  padding: 0;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin: 5px 0;
  background: white;
  border-radius: 4px;
}

.remove-btn {
  background: #e74c3c;
  margin-left: 10px;
}

.remove-btn:hover {
  background: #c0392b;
}
</style>

