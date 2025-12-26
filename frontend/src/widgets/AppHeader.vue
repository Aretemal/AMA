<script setup lang="ts">
import { AppRoutes } from '@/constants/appRoutes'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const links = [
  {
    to: AppRoutes.HOME,
    label: 'Home',
  },
  {
    to: AppRoutes.MY_ARTICLES,
    label: 'My Articles',
    children: [
      AppRoutes.CREATE_ARTICLE,
    ]
  },
  {
    to: AppRoutes.SETTINGS,
    label: 'Settings',
  },
]

const isActive = (to: string) => {
  return route.path === to
}

async function handleLogout() {
  await authStore.logout()
  router.push(AppRoutes.LOGIN)
}

</script>

<template>
  <nav v-if="isAuthenticated" class="w-full px-10 bg-white flex gap-4 items-center justify-between">
    <div class="flex gap-4">
      <RouterLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        :class="[
          'p-4 inline-block',
          isActive(link.to) || link?.children?.includes?.(route.path) ? 'text-black bg-gray-100' : 'text-gray-500'
        ]"
      >
        {{ link.label }}
      </RouterLink>
    </div>
    <div v-if="authStore.isAuthenticated" class="flex items-center gap-4">
      <span class="text-gray-600">Hello, {{ authStore.user?.username }}!</span>
      <el-button type="danger" size="small" @click="handleLogout">
        Logout
      </el-button>
    </div>
    <div v-else>
      <RouterLink :to="AppRoutes.LOGIN">
        <el-button type="primary" size="small">Login</el-button>
      </RouterLink>
    </div>
  </nav>
</template>

<style scoped>
</style>

