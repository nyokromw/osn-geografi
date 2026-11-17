export const tryoutLevelLabels = {
  OSNK: 'OSN-K',
  OSNP: 'OSN-P',
  Nasional: 'OSN Nasional',
  lainnya: 'Jenjang lainnya',
} as const

export type TryoutLevel = keyof typeof tryoutLevelLabels
export type TryoutLevelFilter = 'semua' | TryoutLevel

export const tryoutLevelOptions = Object.keys(tryoutLevelLabels) as TryoutLevel[]

export function tryoutLevel(value: unknown): TryoutLevel {
  const key = typeof value === 'string' ? value.trim().toUpperCase().replace(/[\s_-]+/g, '') : ''
  if (key === 'OSNK' || key === 'OSNP') return key
  if (key === 'NASIONAL' || key === 'OSNNASIONAL') return 'Nasional'
  return 'lainnya'
}
