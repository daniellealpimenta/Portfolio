import { computed } from 'vue'
import { useRouter, useRuntimeConfig, useState } from '#imports'

// Perfil completo — só é preenchido assim por /auth/me (autenticado, "seus
// próprios dados"). A resposta de /auth/verify-code traz
// só o essencial (id/name/username/email), o resto fica undefined até o
// fetchSession() rodar.
interface AuthUser {
  id: string
  name: string
  username: string | null
  email: string
  description?: string | null
  main_phrase?: string | null
  cellphone_number?: string | null
  avatar_url?: string | null
  linkedin_url?: string | null
  github_url?: string | null
  medium_url?: string | null
  instagram_url?: string | null
  personality_test_url?: string | null
  curriculum_url?: string | null
  curriculum_en_url?: string | null
}

function normalizeEmail(email: string): string {
  return email.trim().toLowerCase()
}

export const useAuth = () => {
  const router = useRouter()
  const API_BASE_URL = useRuntimeConfig().public.apiBase
  const currentUser = useState<AuthUser | null>('admin-current-user', () => null)
  const loading = useState('admin-auth-loading', () => false)
  const error = useState('admin-auth-error', () => '')

  // Mantidos com esses nomes por compatibilidade com o restante do admin,
  // que já usa adminUserId/adminUserName em várias telas.
  const adminUserId = computed(() => currentUser.value?.id || '')
  const adminUserName = computed(() => currentUser.value?.name || '')

  // Repopula currentUser a partir da sessão (cookie httpOnly) após um refresh de página.
  async function fetchSession(): Promise<boolean> {
    try {
      const res = await $fetch<AuthUser>(`${API_BASE_URL}/auth/me`, { credentials: 'include' })
      currentUser.value = res
      return true
    } catch {
      currentUser.value = null
      return false
    }
  }

  // O backend responde igual pra qualquer e-mail (só o ADMIN_EMAIL recebe o código),
  // então não há como — nem por que — distinguir "e-mail não encontrado" aqui.
  async function requestCode(rawEmail: string): Promise<'sent'> {
    if (loading.value) return 'sent' // já tem uma chamada em andamento, evita duplo código/e-mail
    const email = normalizeEmail(rawEmail)
    loading.value = true
    error.value = ''
    try {
      await $fetch(`${API_BASE_URL}/auth/request-code`, {
        method: 'POST',
        credentials: 'include',
        body: { email }
      })
      return 'sent'
    } catch (e: any) {
      if (e?.response?.status === 429) {
        error.value = 'Muitas tentativas. Aguarde um pouco antes de tentar de novo.'
      } else if (e?.response?.status === 503) {
        error.value = e?.data?.detail || 'Não foi possível enviar o e-mail agora.'
      } else {
        error.value = 'Erro ao solicitar o código. O backend está rodando?'
      }
      throw e
    } finally {
      loading.value = false
    }
  }

  async function verifyCode(rawEmail: string, rawCode: string): Promise<boolean> {
    if (loading.value) return false
    const email = normalizeEmail(rawEmail)
    const code = rawCode.trim()
    loading.value = true
    error.value = ''
    try {
      const res = await $fetch<AuthUser>(`${API_BASE_URL}/auth/verify-code`, {
        method: 'POST',
        credentials: 'include',
        body: { email, code }
      })
      currentUser.value = res
      router.push('/admin')
      return true
    } catch (e: any) {
      error.value = e?.response?.status === 429
        ? 'Muitas tentativas. Aguarde um pouco antes de tentar de novo.'
        : 'Código inválido ou expirado.'
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      await $fetch(`${API_BASE_URL}/auth/logout`, { method: 'POST', credentials: 'include' })
    } catch {
      // segue o baile mesmo se a chamada falhar — limpamos o estado local de qualquer forma
    }
    currentUser.value = null
    router.push('/admin/login')
  }

  return {
    currentUser,
    adminUserId,
    adminUserName,
    loading,
    error,
    fetchSession,
    requestCode,
    verifyCode,
    logout
  }
}
