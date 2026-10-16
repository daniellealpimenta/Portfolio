<template>
  <div class="max-w-2xl">
    <div class="mb-6 flex items-center gap-4">
      <NuxtLink to="/admin/skills" class="w-10 h-10 rounded-full bg-surface border border-border flex items-center justify-center text-muted hover:text-text hover:bg-background transition-colors">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
      </NuxtLink>
      <h1 class="text-h2 m-0 text-text">Editar Habilidade</h1>
    </div>

    <form @submit.prevent="handleSubmit" class="bg-surface border border-border rounded-2xl p-6 space-y-6">
      
      <div>
        <label class="block text-meta text-xs text-muted mb-2">Nome *</label>
        <input v-model="form.name" type="text" required class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text text-body focus:outline-none focus:border-primary transition-colors">
      </div>
      <div>
        <label class="block text-meta text-xs text-muted mb-2">Ícone URL </label>
        <input v-model="form.icon_url" type="text"  class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text text-body focus:outline-none focus:border-primary transition-colors">
      </div>
      <div>
        <label class="block text-meta text-xs text-muted mb-2">Descrição *</label>
        <input v-model="form.description" type="text" required class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text text-body focus:outline-none focus:border-primary transition-colors">
      </div>
      <div>
        <label class="block text-meta text-xs text-muted mb-2">Ícone URL </label>
        <input v-model="form.icon_url" type="text"  class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text text-body focus:outline-none focus:border-primary transition-colors">
      </div>
      
      <div v-if="errorMsg" class="text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-xl p-3">
        {{ errorMsg }}
      </div>

      <div class="pt-4 border-t border-border flex justify-end">
        <button type="submit" :disabled="saving" class="btn-cta bg-primary text-background px-6 py-3 rounded-xl hover:opacity-90 disabled:opacity-50 transition-all flex items-center gap-2">
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

definePageMeta({ layout: 'admin', middleware: 'auth' })

const router = useRouter()
const route = useRoute()
const id = route.params.id as string

const { skills, updateSkill, loadData, getRecord } = usePortfolioApi()
const { adminUserId } = useAuth()

const form = ref({
  name: '',
  icon_url: '',
  description: ''
})

const saving = ref(false)
const errorMsg = ref('')

onMounted(async () => {
  if (skills.value.length === 0) {
    await loadData(adminUserId.value)
  }
  syncData()
})


// Busca o registro completo na API: os dados do site público são simplificados
// e não têm todos os campos (datas, ícones, imagem), o que deixava o formulário vazio.
async function syncData() {
  try {
    fillForm(form.value, await getRecord('skills', id))
  } catch (e) {
    console.error('Erro ao carregar o registro:', e)
    errorMsg.value = 'Não foi possível carregar os dados salvos. Recarregue a página.'
  }
}

async function handleSubmit() {
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
    
    await updateSkill(id, payload)
    router.push('/admin/skills')
  } catch (e: any) {
    console.error(e)
    errorMsg.value = 'Ocorreu um erro ao salvar as alterações.'
  } finally {
    saving.value = false
  }
}
</script>
