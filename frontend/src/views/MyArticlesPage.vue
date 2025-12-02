<script setup lang="ts">
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import { AppRoutes } from '../constants/appRoutes';

const articleStore = useArticleStore()

const articles = articleStore.articles;

onMounted(() => {
  articleStore.fetchArticles()
})
</script>

<template>
  <div class="w-full flex flex-col gap-4">
    <h1 class="text-xl font-bold">My Articles</h1>
    <div v-if="!articles.length" class="p-4 flex flex-col justify-center items-center gap-4 bg-gray-100 rounded-xl">
      <p>No articles found. Create your first article to get started.</p>
      <el-button type="primary" class="w-fit">
        <RouterLink :to="AppRoutes.CREATE_ARTICLE">Create Article</RouterLink>
      </el-button>
    </div>
  </div>
</template>

<style scoped>
</style>

