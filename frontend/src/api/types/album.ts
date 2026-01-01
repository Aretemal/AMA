export type Album = {
  id: number
  title: string | null
  creator: string | null
  song_ids: number[] | null
  user_ids: number[] | null
  created_at: string
  updated_at: string
}

export type AlbumCreate = {
  title: string
  creator: string
  song_ids: number[]
}

export type AlbumUpdate = {
  title?: string | null
  creator?: string | null
  song_ids?: number[] | null
}

