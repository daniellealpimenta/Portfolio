import { useCookie, useState } from '#imports'

export function useLanguage() {
  // Cookie (e não localStorage) pra que a página renderizada no servidor já
  // venha no idioma escolhido, sem piscar o outro idioma ao carregar.
  const saved = useCookie<'pt' | 'en'>('lang', { maxAge: 60 * 60 * 24 * 365, sameSite: 'lax' })
  const lang = useState<'pt' | 'en'>('global_lang', () => (saved.value === 'en' ? 'en' : 'pt'))

  function toggleLang() {
    lang.value = lang.value === 'pt' ? 'en' : 'pt'
    saved.value = lang.value
  }

  return { lang, toggleLang }
}
