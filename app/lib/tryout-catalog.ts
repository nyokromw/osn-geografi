import { bisaAkses, requiredAccess, type AccessLevel } from './membership'
import { tryoutLevel, type TryoutLevel } from './tryout-levels'

export const predictionYear = 2027
export const tryoutCategoryLabels = { latihan: 'Latihan', prediksi: 'Prediksi' } as const
export type TryoutCategory = keyof typeof tryoutCategoryLabels
export type TryoutCategoryFilter = TryoutCategory | 'semua'
export const tryoutCategories: TryoutCategory[] = ['latihan', 'prediksi']
export const comparisonLevels = ['OSNK', 'OSNP'] as const

export const tryoutTargets = {
  // Cumulative packages each level can open (2026/2027 catalogue). Prediksi packages are all OSN-K.
  OSNK: { gratis: { latihan: 2, prediksi: 1 }, pemula: { latihan: 5, prediksi: 2 }, premium: { latihan: 12, prediksi: 2 }, platinum: { latihan: 20, prediksi: 5 } },
  OSNP: { gratis: { latihan: 2, prediksi: 0 }, pemula: { latihan: 3, prediksi: 0 }, premium: { latihan: 10, prediksi: 0 }, platinum: { latihan: 10, prediksi: 0 } },
} satisfies Record<(typeof comparisonLevels)[number], Record<AccessLevel, Record<TryoutCategory, number>>>

export type TryoutCatalogEntry = {
  jenis?: string | null
  kategori?: string | null
  tahun?: number | null
  akses?: string | null
  is_premium?: boolean | null
}

export function tryoutCategory(value: unknown): TryoutCategory {
  return value === 'prediksi' ? 'prediksi' : 'latihan'
}

export function tryoutCategoryLabel(entry: TryoutCatalogEntry) {
  const category = tryoutCategory(entry.kategori)
  return category === 'prediksi' && entry.tahun ? 'Prediksi ' + entry.tahun : tryoutCategoryLabels[category]
}

export function groupTryoutPackages<T extends TryoutCatalogEntry>(packages: T[]) {
  const groups = new Map<string, T[]>()
  for (const item of packages) {
    const label = tryoutCategoryLabel(item)
    const section = groups.get(label) ?? []
    section.push(item)
    groups.set(label, section)
  }
  return Array.from(groups.entries()).sort(([left], [right]) => left.localeCompare(right, 'id'))
}

export function countTryoutPackages(packages: TryoutCatalogEntry[], level: TryoutLevel, category: TryoutCategory, access: AccessLevel) {
  return packages.filter(item =>
    tryoutLevel(item.jenis) === level &&
    tryoutCategory(item.kategori) === category &&
    (category === 'latihan' || item.tahun === predictionYear) &&
    bisaAkses(access, requiredAccess(item))
  ).length
}
