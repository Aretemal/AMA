import apiClient from '../client'
import type { Album, AlbumCreate, AlbumUpdate } from '../types/album'

export const albumService = {
  getAll: () => apiClient.get<Album[]>('/albums'),
  getById: (id: number) => apiClient.get<Album>(`/albums/${id}`),
  create: (album: AlbumCreate) => apiClient.post<Album>('/albums', album),
  update: (id: number, album: AlbumUpdate) => apiClient.put<Album>(`/albums/${id}`, album),
  delete: (id: number) => apiClient.delete<void>(`/albums/${id}`),
}

