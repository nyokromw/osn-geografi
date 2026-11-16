import { supabase } from './supabase'
import { activeAccess, type AccessLevel } from './membership'

export async function getUserStatus(userId: string): Promise<AccessLevel> {
  const { data: profile } = await supabase
    .from('profiles')
    .select('status, status_expired, role')
    .eq('id', userId)
    .single()

  return profile?.role === 'admin' ? 'platinum' : activeAccess(profile)
}
