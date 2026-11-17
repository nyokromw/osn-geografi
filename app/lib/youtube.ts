const youtubeHosts = new Set(['youtube.com', 'www.youtube.com', 'm.youtube.com'])
const embedHosts = new Set(['youtube-nocookie.com', 'www.youtube-nocookie.com'])
const shortHosts = new Set(['youtu.be', 'www.youtu.be'])
const validId = /^[A-Za-z0-9_-]{11}$/

export function getYouTubeVideoId(value: unknown): string | null {
  if (typeof value !== 'string') return null
  const text = value.trim()
  if (validId.test(text)) return text

  let url: URL
  try {
    url = new URL(text)
  } catch {
    return null
  }
  if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password || url.port) return null

  const path = url.pathname.replace(/\/$/, '')
  let id: string | null = null
  if (shortHosts.has(url.hostname)) {
    id = path.slice(1)
  } else if (youtubeHosts.has(url.hostname)) {
    if (path === '/watch') id = url.searchParams.get('v')
    else id = path.match(/^\/(?:embed|shorts|live)\/([^/]+)$/)?.[1] ?? null
  } else if (embedHosts.has(url.hostname)) {
    id = path.match(/^\/embed\/([^/]+)$/)?.[1] ?? null
  }
  return id && validId.test(id) ? id : null
}
