<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <nav class="navbar">
      <RouterLink to="/composition" class="nav-link">Composition API</RouterLink>
      <RouterLink to="/options" class="nav-link">Options API</RouterLink>
    </nav>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  background: #fafafa;
}

.navbar {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.nav-link {
  padding: 10px 20px;
  text-decoration: none;
  color: #2c3e50;
  border-radius: 4px;
  transition: all 0.3s;
  font-weight: 500;
}

.nav-link:hover {
  background: #f0f0f0;
}

.nav-link.router-link-active {
  background: #42b983;
  color: white;
}

main {
  padding: 20px 0;
}
</style>
