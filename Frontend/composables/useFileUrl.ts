import { useRuntimeConfig } from '#imports'

// Arquivos enviados pelo /admin ficam no banco e são guardados como caminho
// relativo (/files/<id>.<ext>), pra não depender do domínio da API. Aqui o
// caminho vira um endereço completo; links externos passam sem mudança.
export function useFileUrl() {
  const apiBase = useRuntimeConfig().public.apiBase
  return (url?: string | null): string => {
    if (!url) return ''
    return url.startsWith('/files/') ? `${apiBase}${url}` : url
  }
}
