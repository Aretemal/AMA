<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useArticleStore } from '@/stores/article'
import type { ArticleCreate } from '../api/types/article';
import { useRoute, useRouter } from 'vue-router';
import { ElNotification } from 'element-plus';
import { AppRoutes } from '../constants/appRoutes';
import { DEFAULT_EDIT_VALUE } from '../constants/editFields';

const articleStore = useArticleStore()

const formRef = ref()

console.log(articleStore.article)

const showDialog = ref(false)

const router = useRouter()

const route = useRoute()

const unSavedChanges = ref({
  title: DEFAULT_EDIT_VALUE.TEXT,
  content: DEFAULT_EDIT_VALUE.TEXT,
})

function onBack() {
  if (unSavedChanges.value.title.value !== articleStore.article?.title || unSavedChanges.value.content.value !== articleStore.article?.content  ) {
    showDialog.value = true
    return
  }
  router.back()
}

const onLeaveForm = () => {
  showDialog.value = false
  router.push(AppRoutes.MY_ARTICLES)
}

const onEditStart = (field: 'title' | 'content') => {
  unSavedChanges.value[field] = {
    value: articleStore.article?.[field] || '',
    originalValue: articleStore.article?.[field] || '',
    isEditing: true,
  }
}

const onSave = (field: 'title' | 'content') => {
  articleStore.updateArticle(route.params.id as string, {
    [field]: unSavedChanges.value[field].value,
  })
  unSavedChanges.value[field] = DEFAULT_EDIT_VALUE.TEXT;
}

onMounted(() => {
  if (route.params.id) {
    articleStore.fetchArticle(route.params.id as string)
  }
})
</script>

<template>
  <div class="w-full flex flex-col gap-4">
    <div class="flex items-center gap-2">
      <el-icon :size="20" class="cursor-pointer" @click="onBack()">
        <Back />
      </el-icon>
      <div class="flex items-center gap-2">
        <h1 v-if="!unSavedChanges.title.isEditing" class="text-xl font-bold">{{ articleStore.article?.title }}</h1>
        <el-input v-else v-model="unSavedChanges.title.value" />
        <el-icon v-if="!unSavedChanges.title.isEditing" :size="20" class="cursor-pointer" color="blue" @click="onEditStart('title')">
          <Edit />
        </el-icon>
        <el-icon v-if="unSavedChanges.title.isEditing" :size="20" class="cursor-pointer" color="green" @click="onSave('title')">
          <Check />
        </el-icon>
      </div>
    </div>
    <div class="w-1/2 p-4 flex flex-col gap-4 bg-gray-100 rounded-xl">
      <p>{{ articleStore.article?.content }}</p>
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

