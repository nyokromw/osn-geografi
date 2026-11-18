export const landingVideoSlots = [1, 2, 3] as const

export type LandingVideo = {
  posisi: (typeof landingVideoSlots)[number]
  judul: string
  youtube_id: string
}
