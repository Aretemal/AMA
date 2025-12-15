<template>
  <div class="login-page">
    <el-card class="login-card">
      <template #header>
        <h2>Login</h2>
      </template>
      <el-form @submit.prevent="handleLogin">
        <el-form-item label="Email">
          <el-input
            v-model="email"
            type="email"
            placeholder="Enter your email"
            :disabled="authStore.isLoading"
          />
        </el-form-item>
        <el-form-item label="Password">
          <el-input
            v-model="password"
            type="password"
            placeholder="Enter your password"
            show-password
            :disabled="authStore.isLoading"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="authStore.isLoading"
            @click="handleLogin"
            style="width: 100%"
          >
            Login
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-link type="primary" @click="$router.push('/register')">
            Don't have an account? Register
          </el-link>
        </el-form-item>
      </el-form>
      <el-alert
        v-if="authStore.error"
        :title="authStore.error"
        type="error"
        :closable="false"
        style="margin-top: 20px"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { AppRoutes } from '@/constants/appRoutes'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')

async function handleLogin() {
  const result = await authStore.login(email.value, password.value)

  if (result.success) {
    const redirect = (route.query.redirect as string) || AppRoutes.HOME
    router.push(redirect)
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
}
</style>

