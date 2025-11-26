<script lang="ts">
import { defineComponent } from 'vue'
import { useCounterStore } from '@/stores/counter'

export default defineComponent({
  name: 'OptionsApiPage',

  setup() {
    const counterStore = useCounterStore()
    return { counterStore }
  },

  data() {
    return {
      message: 'Привет из Options API!',
      inputText: '',
      items: [] as string[],
      timer: 0,
      intervalId: undefined as number | undefined,
    }
  },

  computed: {
    reversedMessage(): string {
      return this.message.split('').reverse().join('')
    },
  },

  methods: {
    addItem() {
      if (this.inputText.trim()) {
        this.items.push(this.inputText)
        this.inputText = ''
      }
    },

    removeItem(index: number) {
      this.items.splice(index, 1)
    },

    incrementCounter() {
      this.counterStore.increment()
    },
  },

  mounted() {
    this.intervalId = window.setInterval(() => {
      this.timer++
    }, 1000)
  },

  beforeUnmount() {
    if (this.intervalId) {
      clearInterval(this.intervalId)
    }
  },
})
</script>

<template>
  <div class="options-page">
    <h1>Options API Page</h1>

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
      <button @click="incrementCounter">Увеличить</button>
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
.options-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #e74c3c;
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
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

button:hover {
  background: #c0392b;
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

