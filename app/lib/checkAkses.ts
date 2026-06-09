import { supabase } from './supabase'

export async function getUserStatus(): Promise<'gratis' | 'premium' | 'platinum'> {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return 'gratis'

  const { data: profile } = await supabase
    .from('profiles')
    .select('status, status_expired')
    .eq('id', user.id)
    .single()

  if (!profile || profile.status === 'gratis') return 'gratis'

  // Cek expired
  if (profile.status_expired) {
    const expired = new Date(profile.status_expired)
    if (expired < new Date()) return 'gratis' // sudah expired
  }

  return profile.status as 'premium' | 'platinum'
}

export function bisaAkses(statusUser: string, aksesKonten: string): boolean {
  if (aksesKonten === 'gratis') return true
  if (aksesKonten === 'premium') return statusUser === 'premium' || statusUser === 'platinum'
  if (aksesKonten === 'platinum') return statusUser === 'platinum'
  return false
}