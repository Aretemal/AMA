import { defineStore } from 'pinia'
import { ref } from 'vue'
import { songService } from '@/api/services/songService'
import type { Song, SongCreate, SongUpdate } from '@/api/types/song'

export const useSongStore = defineStore('song', () => {
  const songs = ref<Song[]>([])
  const song = ref<Song | null>(null)
  const isLoading = ref(false)
  const isCreating = ref(false)
  const error = ref<string | null>(null)

  async function fetchSongs() {
    try {
      isLoading.value = true
      error.value = null

      const response = await songService.getAll()
      songs.value = response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchSongsByAlbum(albumId: number) {
    try {
      isLoading.value = true
      error.value = null

      const response = await songService.getByAlbum(albumId)
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      return []
    } finally {
      isLoading.value = false
    }
  }

  async function createSong(songData: SongCreate) {
    try {
      isCreating.value = true
      error.value = null

      const response = await songService.create(songData)
      songs.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      throw err
    } finally {
      isCreating.value = false
    }
  }

  async function deleteSong(id: number, {
    needUpdate = true
  }: {
    needUpdate?: boolean
  } = {}) {
    try {
      error.value = null
      await songService.delete(id)
      if (needUpdate) {
        songs.value = songs.value.filter(song => song.id !== id)
        if (song.value?.id === id) {
          song.value = null
        }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      throw err
    }
  }

  async function fetchSong(id: number) {
    try {
      error.value = null
      const response = await songService.getById(id)
      song.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      throw err
    }
  }

  async function updateSong(id: number, songData: SongUpdate, {
    needUpdate = true
  }: {
    needUpdate?: boolean
  } = {}) {
    try {
      error.value = null
      const response = await songService.update(id, songData)
      if (needUpdate) {
        const index = songs.value.findIndex(s => s.id === id)
        if (index !== -1) {
          songs.value[index] = response.data
        }
        if (song.value?.id === id) {
          song.value = response.data
        }
      }
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
      throw err
    }
  }

  function getStreamUrl(id: number): string {
    return songService.getStreamUrl(id)
  }

  return {
    songs,
    song,
    isLoading,
    isCreating,
    error,
    fetchSongs,
    fetchSongsByAlbum,
    fetchSong,
    createSong,
    updateSong,
    deleteSong,
    getStreamUrl,
  }
})

