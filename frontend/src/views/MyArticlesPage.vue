<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useArticleStore } from '@/stores/article'
import { AppRoutes } from '../constants/appRoutes';
import { useRouter } from 'vue-router';
import { Edit, Delete } from '@element-plus/icons-vue';

const articleStore = useArticleStore()
const router = useRouter()

const articles = computed(() => articleStore.articles);

const showDeleteDialog = ref(false)
const deleteArticleId = ref<string | null>(null)

function onEdit(id: string) {
  router.push(`${AppRoutes.ARTICLE_DETAILS.replace(':id', id)}`)
}

function onDeleteModalOpen(id: string) {
  showDeleteDialog.value = true
  deleteArticleId.value = id
}

function onDelete() {
  if (deleteArticleId.value) {
    articleStore.deleteArticle(deleteArticleId.value)
    showDeleteDialog.value = false
    deleteArticleId.value = null
  }
}

onMounted(() => {
  articleStore.fetchArticles()
})
</script>

<template>
  <div class="w-full flex flex-col gap-4">
    <h1 class="text-xl font-bold">My Articles</h1>

    <div v-if="articles.length" class="w-full items-center p-6 flex flex-col gap-4 bg-gray-100 rounded-xl">
      <div class="w-full grid grid-cols-3 gap-4">
        <div v-for="article in articles" :key="article.id" class="flex justify-between gap-2 bg-white rounded-xl p-4">
          <div class="flex flex-col gap-2">
            <h3 class="text-lg font-bold">
              {{ article.title }}
            </h3>
            <p class="text-sm text-gray-500">
              {{ article.content }}
            </p>
          </div>
          <div class="flex gap-1">
            <el-icon :size="20" class="cursor-pointer m-1" color="blue" @click="onEdit(article.id)">
              <Edit />
            </el-icon>
            <el-icon :size="20" class="cursor-pointer m-1" color="red" @click="onDeleteModalOpen(article.id)">
              <Delete />
            </el-icon>
          </div>
        </div>
      </div>
      <el-button type="primary" class="w-fit" size="large">
        <RouterLink :to="AppRoutes.CREATE_ARTICLE" class="text-lg">Create Article</RouterLink>
      </el-button>
    </div>
    <div v-if="!articles.length" class="p-4 flex flex-col justify-center items-center gap-4 bg-gray-100 rounded-xl">
      <p>No articles found. Create your first article to get started.</p>
      <el-button type="primary" class="w-fit">
        <RouterLink :to="AppRoutes.CREATE_ARTICLE">Create Article</RouterLink>
      </el-button>
    </div>
  </div>


  <el-dialog v-model="showDeleteDialog" title="Attention!" class="max-w-[450px]">
    <div class="flex flex-col gap-2">
      <p class="text-sm text-gray-500">Are you sure you want to delete this article?</p>
      <div class="flex justify-end gap-2">
        <el-button @click="onDelete">Yes</el-button>
        <el-button type="primary" @click="showDeleteDialog = false">No</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
</style>

