<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { AppRoutes } from '@/constants/appRoutes'
import { Loading } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')

async function handleLogin() {
  const result = await authStore.login(email.value, password.value)

  if (result.success) {
    router.push(AppRoutes.HOME)
  }
}
</script>

<template>
  <div class="login-page">
    <el-card v-if="!authStore.isCheckingAuth" class="login-card">
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
        <div>
          <el-link type="primary" @click="$router.push('/register')">
            Don't have an account? Register
          </el-link>
        </div>
      </el-form>
      <el-alert
        v-if="authStore.error"
        :title="authStore.error"
        type="error"
        :closable="false"
        style="margin-top: 20px"
      />
    </el-card>
    <el-card v-else class="login-card">
      <div style="text-align: center; padding: 40px;">
        <el-icon class="is-loading" style="font-size: 32px;">
          <Loading />
        </el-icon>
        <p style="margin-top: 16px;">Проверка авторизации...</p>
      </div>
    </el-card>
  </div>
</template>

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

