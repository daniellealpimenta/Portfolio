export interface Project {
  id: string | number
  title: string
  year: number
  likes: number
  liked?: boolean
  cat: 'mobile' | 'back' | 'data' | string // balde simplificado, usado pelas abas de filtro do site público
  categories: string[] // categorias reais (podem ser mais de uma), usadas no admin e nos badges
  desc: string // vazio quando o projeto não tem descrição
  date?: string // ISO, usado pra ordenar do mais recente pro mais antigo
}

export interface ProjectLink {
  id: string
  project_id: string
  name: string
  url: string
  icon: string
}

export interface Tool {
  id: string | number
  name: string
}

export interface Skill {
  id: string | number
  name: string
  desc: string
}

export interface Experience {
  id: string | number
  year: string
  title: string
  desc: string
  company?: string
  endYear?: string | null // null = emprego atual
}

export interface Certificate {
  id: string | number
  title: string
  issuer: string
  workload?: number
  issue_date?: string
  description?: string
  digital_certificate_url?: string
}

export interface Testimonial {
  id: string | number
  name: string
  quote: string
  experience_id?: string | number
  linkedin_recommender_url?: string
  recommender_avatar_url?: string
  date?: string
  description?: string
}

export interface User {
  id: string
  name: string
  description: string
  main_phrase: string | null
  email: string
  cellphone_number: string | null
  avatar_url: string
  linkedin_url: string
  github_url: string | null
  medium_url: string | null
  instagram_url: string | null
  personality_test_url: string | null
  curriculum_url: string
}




// Reduz a lista real de categorias a um balde simples ('mobile'/'data'/'back'),
// usado só pelas abas de filtro simplificadas do site público (work.vue).
function normalizeCategory(categories?: string[]): string {
  if (!categories || categories.length === 0) return 'back'
  const lower = categories.map(c => c.toLowerCase())
  if (lower.some(c => c.includes('mobile') || c.includes('ios') || c.includes('swift'))) return 'mobile'
  if (lower.some(c => c.includes('data'))) return 'data'
  return 'back'
}

// Identificador anônimo persistido em cookie — usado só pra saber, no backend,
// se ESTE navegador já curtiu um projeto (sem precisar de login de visitante).
function getVisitorId(): string {
  const cookie = useCookie<string | null>('visitor_id', { maxAge: 60 * 60 * 24 * 365 * 2 })
  if (!cookie.value) {
    cookie.value = crypto.randomUUID()
  }
  return cookie.value
}

export function usePortfolioApi() {
  const API_BASE_URL = useRuntimeConfig().public.apiBase
  const user = useState<User | null>('portfolio-user', () => null)
  const projects = useState<Project[]>('portfolio-projects', () => [])
  const tools = useState<Tool[]>('portfolio-tools', () => [])
  const skills = useState<Skill[]>('portfolio-skills', () => [])
  const experiences = useState<Experience[]>('portfolio-experiences', () => [])
  const certificates = useState<Certificate[]>('portfolio-certificates', () => [])
  const testimonials = useState<Testimonial[]>('portfolio-testimonials', () => [])
  const loading = useState('portfolio-loading', () => false)
  // Guarda pra quem os dados atuais foram carregados — evita refazer a busca
  // inteira toda vez que o usuário navega de volta pra uma página já visitada.
  const loadedFor = useState<string | null>('portfolio-loaded-for', () => null)

  async function loadData(userIdOrUsername: string, force = false) {
    if (!userIdOrUsername) {
      console.error('loadData: userIdOrUsername is required')
      return
    }

    if (!force && loadedFor.value === userIdOrUsername && user.value) {
      return
    }

    loading.value = true
    try {
      // 1. Fetch user first using identifier (username or UUID)
      const userRes = await $fetch<any>(`${API_BASE_URL}/users/${userIdOrUsername}`, { timeout: 8000 }).catch(() => null)

      if (userRes) {
        user.value = userRes
        const actualUserId = userRes.id // Always the UUID
        const visitorId = getVisitorId()

        // 2. Fetch dependencies using the actual UUID
        // Sem fallback pra "buscar tudo" — cada portfólio é isolado por usuário
        // agora, então um erro/timeout aqui deve resultar em lista vazia, não
        // nos dados de outra pessoa.
        const [projRes, toolRes, skillRes, expRes, certRes, testRes, likedRes] = await Promise.allSettled([
          $fetch<any[]>(`${API_BASE_URL}/projects/user/${actualUserId}`, { timeout: 8000 }),
          $fetch<any[]>(`${API_BASE_URL}/tools/user/${actualUserId}`, { timeout: 8000 }),
          $fetch<any[]>(`${API_BASE_URL}/skills/user/${actualUserId}`, { timeout: 8000 }),
          $fetch<any[]>(`${API_BASE_URL}/experiences/user/${actualUserId}`, { timeout: 8000 }),
          $fetch<any[]>(`${API_BASE_URL}/certificates/user/${actualUserId}`, { timeout: 8000 }),
          $fetch<any[]>(`${API_BASE_URL}/recommendations/user/${actualUserId}`, { timeout: 8000 }),
          $fetch<string[]>(`${API_BASE_URL}/projects/liked/${visitorId}`, { timeout: 8000 }).catch(() => [])
        ])

        const likedIds = new Set(likedRes.status === 'fulfilled' ? likedRes.value : [])

        if (projRes.status === 'fulfilled' && Array.isArray(projRes.value)) {
          projects.value = projRes.value
            .map(p => ({
              id: p.id,
              title: p.name || p.title,
              year: p.date ? new Date(p.date).getFullYear() : (p.year || 2025),
              likes: p.likes ?? 0,
              liked: likedIds.has(p.id),
              cat: normalizeCategory(p.categories),
              categories: p.categories || [],
              desc: p.description || p.desc || '',
              date: p.date || ''
            }))
            .sort((a, b) => (b.date || '').localeCompare(a.date || ''))
        }

        if (toolRes.status === 'fulfilled' && Array.isArray(toolRes.value)) {
          tools.value = toolRes.value.map(t => ({ id: t.id, name: t.name }))
        }

        if (skillRes.status === 'fulfilled' && Array.isArray(skillRes.value)) {
          skills.value = skillRes.value.map(s => ({ id: s.id, name: s.name, desc: s.description || s.desc }))
        }

        if (expRes.status === 'fulfilled' && Array.isArray(expRes.value)) {
          experiences.value = expRes.value
            .map(e => ({
              id: e.id,
              year: e.year || e.start_date?.substring(0, 4) || '2025',
              title: e.position || e.role || e.title,
              desc: e.description || e.desc,
              company: e.company || '',
              endYear: e.exit_date ? e.exit_date.substring(0, 4) : null,
              start: e.start_date || ''
            }))
            .sort((a, b) => (b.start || '').localeCompare(a.start || ''))
        }

        if (certRes.status === 'fulfilled' && Array.isArray(certRes.value)) {
          certificates.value = certRes.value.map(c => ({ 
            id: c.id, 
            title: c.name_course || c.name || c.title, 
            issuer: c.plataform || c.institution || c.issuer,
            workload: c.workload || 0,
            issue_date: c.issue_date || '',
            digital_certificate_url: c.digital_certificate_url || '',
            description: c.description || ''
          }))
        }

        if (testRes.status === 'fulfilled' && Array.isArray(testRes.value)) {
          testimonials.value = testRes.value.map(r => ({ 
            id: r.id, 
            name: r.name_recommender || r.author || r.name, 
            quote: r.description || r.content || r.quote,
            description: r.description || r.content || r.quote,
            experience_id: r.experience_id || '',
            linkedin_recommender_url: r.linkedin_recommender_url || '',
            recommender_avatar_url: r.recommender_avatar_url || '',
            date: r.date || ''
          }))
        }

        loadedFor.value = userIdOrUsername
      }
    } catch (e) {
      console.warn('Erro ao buscar API backend:', e)
    } finally {
      loading.value = false
    }
  }

  // --- ADMIN MUTATIONS ---

  // User
  async function updateUser(id: string, data: any) {
    const res = await $fetch(`${API_BASE_URL}/users/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
    await loadData(id, true)
    return res
  }

  // Projects
  async function createProject(data: any) {
    const res = await $fetch(`${API_BASE_URL}/projects/`, { method: 'POST', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function updateProject(id: string, data: any) {
    const res = await $fetch(`${API_BASE_URL}/projects/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  // Curtida é pública (qualquer visitante pode curtir) — usa os endpoints dedicados,
  // não a rota de update geral (que agora exige login).
  async function likeProject(id: string, liked: boolean) {
    return await $fetch(`${API_BASE_URL}/projects/${id}/${liked ? 'like' : 'unlike'}`, {
      method: 'POST',
      body: { visitor_id: getVisitorId() }
    })
  }
  async function deleteProject(id: string) {
    await $fetch(`${API_BASE_URL}/projects/${id}`, { method: 'DELETE', credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
  }

  // Skills
  async function createSkill(data: any) {
    const res = await $fetch(`${API_BASE_URL}/skills/`, { method: 'POST', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function updateSkill(id: string, data: any) {
    const res = await $fetch(`${API_BASE_URL}/skills/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function deleteSkill(id: string) {
    await $fetch(`${API_BASE_URL}/skills/${id}`, { method: 'DELETE', credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
  }

  // Experiences
  async function createExperience(data: any) {
    const res = await $fetch(`${API_BASE_URL}/experiences/`, { method: 'POST', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function updateExperience(id: string, data: any) {
    const res = await $fetch(`${API_BASE_URL}/experiences/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function deleteExperience(id: string) {
    await $fetch(`${API_BASE_URL}/experiences/${id}`, { method: 'DELETE', credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
  }

  // Certificates
  async function createCertificate(data: any) {
    const res = await $fetch(`${API_BASE_URL}/certificates/`, { method: 'POST', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function updateCertificate(id: string, data: any) {
    const res = await $fetch(`${API_BASE_URL}/certificates/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function deleteCertificate(id: string) {
    await $fetch(`${API_BASE_URL}/certificates/${id}`, { method: 'DELETE', credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
  }

  // Tools
  async function createTool(data: any) {
    const res = await $fetch(`${API_BASE_URL}/tools/`, { method: 'POST', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function updateTool(id: string, data: any) {
    const res = await $fetch(`${API_BASE_URL}/tools/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function deleteTool(id: string) {
    await $fetch(`${API_BASE_URL}/tools/${id}`, { method: 'DELETE', credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
  }

  // Recommendations
  async function createRecommendation(data: any) {
    const res = await $fetch(`${API_BASE_URL}/recommendations/`, { method: 'POST', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function updateRecommendation(id: string, data: any) {
    const res = await $fetch(`${API_BASE_URL}/recommendations/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
    return res
  }
  async function deleteRecommendation(id: string) {
    await $fetch(`${API_BASE_URL}/recommendations/${id}`, { method: 'DELETE', credentials: 'include' })
    if (user.value) await loadData(user.value.id, true)
  }

  // Project Images
  async function getProjectImages(projectId: string) {
    return await $fetch<any[]>(`${API_BASE_URL}/project-images/project/${projectId}`)
  }
  async function createProjectImage(data: { project_id: string, image_path: string }) {
    return await $fetch(`${API_BASE_URL}/project-images/`, { method: 'POST', body: data, credentials: 'include' })
  }
  async function updateProjectImage(id: string, data: { image_path: string }) {
    return await $fetch(`${API_BASE_URL}/project-images/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
  }
  async function deleteProjectImage(id: string) {
    return await $fetch(`${API_BASE_URL}/project-images/${id}`, { method: 'DELETE', credentials: 'include' })
  }

  // Uploads (fotos e PDFs ficam no banco; devolve o caminho /files/<id>.<ext>, resolvido com useFileUrl)
  async function uploadFile(file: File, folder: 'avatars' | 'curriculums' | 'tests'): Promise<string> {
    const form = new FormData()
    form.append('folder', folder)
    form.append('file', file)
    try {
      const res = await $fetch<{ url: string }>(`${API_BASE_URL}/uploads/`, { method: 'POST', body: form, credentials: 'include' })
      return res.url
    } catch (e: any) {
      throw new Error(e?.data?.detail || 'Erro ao fazer upload do arquivo')
    }
  }

  // Project Links
  async function getProjectLinks(projectId: string) {
    return await $fetch<ProjectLink[]>(`${API_BASE_URL}/project-links/project/${projectId}`)
  }
  async function createProjectLink(data: { project_id: string, name: string, url: string, icon: string }) {
    return await $fetch<ProjectLink>(`${API_BASE_URL}/project-links/`, { method: 'POST', body: data, credentials: 'include' })
  }
  async function updateProjectLink(id: string, data: { name?: string, url?: string, icon?: string }) {
    return await $fetch<ProjectLink>(`${API_BASE_URL}/project-links/${id}`, { method: 'PATCH', body: data, credentials: 'include' })
  }
  async function deleteProjectLink(id: string) {
    return await $fetch(`${API_BASE_URL}/project-links/${id}`, { method: 'DELETE', credentials: 'include' })
  }

  // Admin: registro completo, direto da API (os dados do site público são
  // simplificados pra exibição e não têm todos os campos dos formulários)
  async function getRecord<T = any>(resource: 'projects' | 'skills' | 'tools' | 'experiences' | 'certificates' | 'recommendations', id: string) {
    return await $fetch<T>(`${API_BASE_URL}/${resource}/${id}`, { credentials: 'include' })
  }

  // Contact
  async function sendContactMessage(data: { user_id: string, name: string, email: string, subject: string, message: string }) {
    return await $fetch(`${API_BASE_URL}/contact/`, { method: 'POST', body: data })
  }

  // System
  async function importSystemData(userId: string, data: any) {
    const res = await $fetch(`${API_BASE_URL}/system/import/${userId}`, { method: 'POST', body: data, credentials: 'include' })
    await loadData(userId, true)
    return res
  }

  async function exportSystemData(userId: string) {
    return await $fetch(`${API_BASE_URL}/system/export/${userId}`, { credentials: 'include' })
  }

  return {
    user,
    projects,
    tools,
    skills,
    experiences,
    certificates,
    testimonials,
    loading,
    loadData,
    updateUser,
    createProject,
    updateProject,
    likeProject,
    deleteProject,
    getProjectImages,
    createProjectImage,
    updateProjectImage,
    deleteProjectImage,
    uploadFile,
    getProjectLinks,
    createProjectLink,
    updateProjectLink,
    deleteProjectLink,
    createSkill,
    updateSkill,
    deleteSkill,
    createExperience,
    updateExperience,
    deleteExperience,
    createCertificate,
    updateCertificate,
    deleteCertificate,
    createTool,
    updateTool,
    deleteTool,
    createRecommendation,
    updateRecommendation,
    deleteRecommendation,
    sendContactMessage,
    getRecord,
    importSystemData,
    exportSystemData
  }
}

