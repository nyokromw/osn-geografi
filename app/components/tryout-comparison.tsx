import { accessLabels, type AccessLevel } from '../lib/membership'
import { comparisonLevels, countTryoutPackages, predictionYear, tryoutCategories, tryoutCategoryLabels, tryoutTargets, type TryoutCatalogEntry } from '../lib/tryout-catalog'
import { tryoutLevelLabels } from '../lib/tryout-levels'

const plans: AccessLevel[] = ['gratis', 'premium', 'platinum']

export function TryoutComparison({ catalog }: { catalog: TryoutCatalogEntry[] | null }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {comparisonLevels.map(level => (
        <div className="atlas-card min-w-0 overflow-x-auto" key={level}>
          <table className="w-full text-left text-sm">
            <caption className="p-4 text-left text-base font-bold text-forest-900">{tryoutLevelLabels[level]}</caption>
            <thead className="border-y border-gray-200 bg-gray-50 text-xs text-gray-700">
              <tr><th scope="col" className="px-3 py-2">Akses</th>
                {tryoutCategories.map(category => <th key={category} scope="col" className="px-3 py-2">
                  {category === 'prediksi' ? 'Prediksi ' + predictionYear : tryoutCategoryLabels[category]}
                </th>)}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {plans.map(access => (
                <tr key={access}>
                  <th scope="row" className="px-3 py-2.5 font-semibold">{accessLabels[access]}</th>
                  {tryoutCategories.map(category => {
                    const target = tryoutTargets[level][access][category]
                    const count = catalog && countTryoutPackages(catalog, level, category, access)
                    return <td key={category} className="px-3 py-2.5 tabular-nums">
                      {target} paket
                      {count !== null && count !== target && <span className="block text-xs text-gray-600">{count} tersedia</span>}
                    </td>
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  )
}
