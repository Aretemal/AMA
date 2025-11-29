<script setup lang="ts">
import { AppRoutes } from '@/constants/appRoutes'
import { useRoute } from 'vue-router'

const route = useRoute()

const links = [
  {
    to: AppRoutes.HOME,
    label: 'Home',
  },
  {
    to: AppRoutes.MY_ARTICLES,
    label: 'My Articles',
  },
  {
    to: AppRoutes.SETTINGS,
    label: 'Settings',
  },
]

const isActive = (to: string) => {
  return route.path === to
}

</script>

<template>
  <nav class="w-full px-10 bg-white flex gap-4">
    <RouterLink
      v-for="link in links"
      :key="link.to"
      :to="link.to"
      :class="[
        'p-4 inline-block',
        isActive(link.to) ? 'text-black bg-gray-100' : 'text-gray-500'
      ]"
    >
      {{ link.label }}
    </RouterLink>
  </nav>
</template>

<style scoped>
</style>

