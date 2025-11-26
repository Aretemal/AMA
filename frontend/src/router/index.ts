import { createRouter, createWebHistory } from 'vue-router'
import CompositionApiPage from '@/views/CompositionApiPage.vue'
import OptionsApiPage from '@/views/OptionsApiPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/composition',
      name: 'composition',
      component: CompositionApiPage,
    },
    {
      path: '/options',
      name: 'options',
      component: OptionsApiPage,
    },
    {
      path: '/',
      redirect: '/composition',
    },
  ],
})

export default router
