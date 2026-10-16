<template>
  <div class="max-w-2xl">
    <div class="mb-6 flex items-center gap-4">
      <NuxtLink to="/admin/projects" class="w-10 h-10 rounded-full bg-surface border border-border flex items-center justify-center text-muted hover:text-text hover:bg-border/50 transition-colors">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
      </NuxtLink>
      <h1 class="text-h2 m-0 text-text">Editar Projeto</h1>
    </div>

    <form @submit.prevent="handleSubmit" class="bg-surface border border-border rounded-2xl p-6 space-y-6">
      <div>
        <label class="block text-meta text-xs text-muted mb-2">Nome do Projeto *</label>
        <input v-model="form.name" type="text" required class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
      </div>

      <div>
        <label class="block text-meta text-xs text-muted mb-2">Data do Projeto * (o ano aparece no site)</label>
        <input v-model="form.date" type="date" required class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
      </div>

      <div>
        <label class="block text-meta text-xs text-muted mb-2">Categorias * (selecione uma ou mais)</label>
        <div class="flex flex-wrap gap-2">
          <label
            v-for="opt in categoryOptions"
            :key="opt"
            class="cursor-pointer select-none px-4 py-2 rounded-xl border text-sm transition-colors"
            :class="form.categories.includes(opt)
              ? 'bg-primary text-background border-primary'
              : 'bg-background border-border text-muted hover:text-text'"
          >
            <input type="checkbox" :value="opt" v-model="form.categories" class="hidden">
            {{ opt }}
          </label>
        </div>
        <p v-if="form.categories.length === 0" class="text-xs text-error mt-2">Selecione ao menos uma categoria.</p>
      </div>

      <div>
        <label class="block text-meta text-xs text-muted mb-2">Descrição</label>
        <textarea v-model="form.description" rows="4" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors"></textarea>
      </div>

      <div>
        <label class="block text-meta text-xs text-muted mb-2">Links do Projeto</label>
        <ProjectLinksEditor v-model="links" />
      </div>

      <div v-if="errorMsg" class="text-sm text-error bg-error/10 border border-error/20 rounded-xl p-3">
        {{ errorMsg }}
      </div>

      <div class="pt-4 border-t border-border flex justify-end">
        <button type="submit" :disabled="saving" class="bg-primary text-background px-6 py-3 rounded-xl font-semibold hover:opacity-90 disabled:opacity-50 transition-all flex items-center gap-2">
          <span v-if="saving">Salvando...</span>
          <span v-else>Salvar Alterações</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { definePageMeta, useRouter, useRoute } from '#imports'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useAuth } from '~/composables/useAuth'
import ProjectLinksEditor, { type EditableProjectLink } from '~/components/ProjectLinksEditor.vue'

definePageMeta({ layout: 'admin', middleware: 'auth' })

const router = useRouter()
const route = useRoute()
const id = route.params.id as string

const { projects, updateProject, loadData, getProjectLinks, createProjectLink, updateProjectLink, deleteProjectLink, getRecord } = usePortfolioApi()
const { adminUserId } = useAuth()

const categoryOptions = ['FrontEnd', 'BackEnd', 'FullStack', 'DataScience', 'GameDev', 'Mobile', 'Other']

const form = ref({
  name: '',
  categories: [] as string[],
  description: '',
  date: ''
})

const links = ref<EditableProjectLink[]>([])
const originalLinkIds = ref<string[]>([])

const saving = ref(false)
const errorMsg = ref('')

onMounted(async () => {
  if (projects.value.length === 0) {
    await loadData(adminUserId.value)
  }
  syncData()

  try {
    const existingLinks = await getProjectLinks(id)
    links.value = existingLinks.map(l => ({ id: l.id, name: l.name, url: l.url, icon: l.icon }))
    originalLinkIds.value = existingLinks.map(l => l.id)
  } catch (e) {
    console.error('Erro ao carregar links do projeto:', e)
  }
})


// Busca o registro completo na API: os dados do site público são simplificados
// e não têm todos os campos (datas, ícones, imagem), o que deixava o formulário vazio.
async function syncData() {
  try {
    fillForm(form.value, await getRecord('projects', id))
  } catch (e) {
    console.error('Erro ao carregar o registro:', e)
    errorMsg.value = 'Não foi possível carregar os dados salvos. Recarregue a página.'
  }
}

async function handleSubmit() {
  if (form.value.categories.length === 0) {
    errorMsg.value = 'Selecione ao menos uma categoria.'
    return
  }

  saving.value = true
  errorMsg.value = ''

  try {
    const payload = { ...form.value }
    // Clean empty values
    Object.keys(payload).forEach(k => {
      if ((payload as any)[k] === '') {
        (payload as any)[k] = null
      }
    })

    await updateProject(id, payload)

    // Sincroniza os links: remove os excluídos, atualiza os existentes, cria os novos
    const currentIds = links.value.filter(l => l.id).map(l => l.id!)
    const removedIds = originalLinkIds.value.filter(oid => !currentIds.includes(oid))
    for (const removedId of removedIds) {
      await deleteProjectLink(removedId)
    }

    for (const link of links.value) {
      if (!link.name.trim() || !link.url.trim() || !link.icon.trim()) continue
      if (link.id) {
        await updateProjectLink(link.id, { name: link.name, url: link.url, icon: link.icon })
      } else {
        await createProjectLink({ project_id: id, name: link.name, url: link.url, icon: link.icon })
      }
    }

    router.push('/admin/projects')
  } catch (e: any) {
    console.error(e)
    errorMsg.value = 'Ocorreu um erro ao salvar as alterações.'
  } finally {
    saving.value = false
  }
}
</script>
