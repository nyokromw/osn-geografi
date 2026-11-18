export const landingVideoSlots = [1, 2, 3] as const

export type LandingVideo = {
  posisi: (typeof landingVideoSlots)[number]
  judul: string
  youtube_id: string
  thumbnail_url?: string | null
}

export function landingThumbnail(video: Pick<LandingVideo, 'thumbnail_url'>, youtubeId: string) {
  return video.thumbnail_url || 'https://img.youtube.com/vi/' + youtubeId + '/hqdefault.jpg'
}

export const thumbnailPattern = /^(\/[A-Za-z0-9._/-]+|https:\/\/\S+)$/
