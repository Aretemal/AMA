<script setup lang="ts">
import { computed, ref } from 'vue'
import { useArticleStore } from '@/stores/article'
import type { ArticleCreate } from '../api/types/article';
import { useRouter } from 'vue-router';
import { ElNotification } from 'element-plus';
import { AppRoutes } from '../constants/appRoutes';

const articleStore = useArticleStore()

const formRef = ref()

const showDialog = ref(false)

const router = useRouter()

const form = ref<ArticleCreate>({
  title: '',
  content: '',
})

const isFormDisabled = computed(() => {
  return !form.value.title.trim() || form.value.title.length > 100
})

const rules = {
  title: [{
    required: true,
    message: 'Title is required',
  }, {
    max: 100,
    message: 'Title must be less than 100 characters long'
  }],
}

const onLeaveForm = () => {
  showDialog.value = false
  router.back()
}

function onBack() {
  if (form.value.title || form.value.content) {
    showDialog.value = true
    return
  }
  router.back()
}

async function onSubmit() {
  await articleStore.createArticle(form.value)

  if (articleStore.error) {
    ElNotification({
      message: articleStore.error,
      type: 'error',
      duration: 3000,
    })
  } else {
    router.push(AppRoutes.MY_ARTICLES)
    ElNotification({
      message: 'Article created successfully!',
      type: 'success',
      duration: 3000,
    })
  }
}
</script>

<template>
  <div class="w-full flex flex-col gap-4">
    <div class="flex items-center gap-2">
      <el-icon :size="20" class="cursor-pointer" @click="onBack()">
        <Back />
      </el-icon>
      <h1 class="text-xl font-bold">New Article</h1>
    </div>
    <div class="w-1/2 p-4 flex flex-col gap-4 bg-gray-100 rounded-xl">
      <el-form ref="formRef" :model="form" :rules="rules">
          <el-form-item :label-position="'top'" label="Title" prop="title">
            <el-input v-model="form.title" placeholder="Enter the title of the article" />
          </el-form-item>
          <el-form-item :label-position="'top'" label="Content"  prop="content">
            <el-input
              v-model="form.content"
              type="textarea"
              :rows="10"
              placeholder="Enter the content of the article"
            />
          </el-form-item>
          <el-form-item>
            <el-button :disabled="isFormDisabled" type="primary" @click="onSubmit" :loading="articleStore.isCreating">Create</el-button>
            <el-button @click="formRef.resetFields()">Clear</el-button>
          </el-form-item>
      </el-form>
    </div>


    <el-dialog v-model="showDialog" title="Attention!" class="max-w-[450px]">
      You have unsaved changes. Are you sure you want to leave?
      <div class="flex justify-end gap-2">
        <el-button @click="onLeaveForm">Yes</el-button>
        <el-button type="primary" @click="showDialog = false">No</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
</style>

