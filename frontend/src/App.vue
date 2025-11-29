<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from './widgets/AppHeader.vue';
import AppFooter from './widgets/AppFooter.vue';
</script>

<template>
  <div id="app">
    <AppHeader />
    <main class="flex-1">
      <RouterView />
    </main>
    <AppFooter />
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #fafafa;
}
</style>
