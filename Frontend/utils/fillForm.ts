/**
 * Copia pro formulário os campos que existem no registro vindo da API.
 * Os formulários do admin usam os mesmos nomes de campo do banco, então
 * isso preenche tudo o que já está salvo (null vira '' pros inputs).
 */
export function fillForm<T extends Record<string, any>>(form: T, record: Record<string, any> | null | undefined) {
  if (!record) return
  for (const key of Object.keys(form)) {
    if (!(key in record)) continue
    const value = record[key]
    if (Array.isArray(value)) (form as any)[key] = [...value]
    else if (value === null || value === undefined) (form as any)[key] = typeof form[key] === 'number' ? 0 : ''
    else (form as any)[key] = value
  }
}
