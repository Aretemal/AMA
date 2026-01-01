import { defineStore } from 'pinia'
import { ref } from 'vue'
import { albumService } from '@/api/services/albumService'
import type { Album, AlbumCreate, AlbumUpdate } from '@/api/types/album'

export const useAlbumStore = defineStore('album', () => {
  const albums = ref<Album[]>([])
  const album = ref<Album | null>(null)
  const isLoading = ref(false)
  const isCreating = ref(false)
  const error = ref<string | null>(null)

  async function fetchAlbums() {
    try {
      isLoading.value = true
      error.value = null

      const response = await albumService.getAll()
      albums.value = response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
    } finally {
      isLoading.value = false
    }
  }

  async function createAlbum(albumData: AlbumCreate) {
    try {
      isCreating.value = true
      error.value = null

      const response = await albumService.create(albumData)
      albums.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      throw err
    } finally {
      isCreating.value = false
    }
  }

  async function deleteAlbum(id: number, {
    needUpdate = true
  }: {
    needUpdate?: boolean
  } = {}) {
    try {
      error.value = null
      await albumService.delete(id)
      if (needUpdate) {
        albums.value = albums.value.filter(album => album.id !== id)
        if (album.value?.id === id) {
          album.value = null
        }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      throw err
    }
  }

  async function fetchAlbum(id: number) {
    try {
      error.value = null
      const response = await albumService.getById(id)
      album.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      throw err
    }
  }

  async function updateAlbum(id: number, albumData: AlbumUpdate, {
    needUpdate = true
  }: {
    needUpdate?: boolean
  } = {}) {
    try {
      error.value = null
      const response = await albumService.update(id, albumData)
      if (needUpdate) {
        const index = albums.value.findIndex(a => a.id === id)
        if (index !== -1) {
          albums.value[index] = response.data
        }
        if (album.value?.id === id) {
          album.value = response.data
        }
      }
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      throw err
    }
  }

  return {
    albums,
    album,
    isLoading,
    isCreating,
    error,
    fetchAlbums,
    fetchAlbum,
    createAlbum,
    updateAlbum,
    deleteAlbum,
  }
})

