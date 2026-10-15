<template>
  <div class="max-w-2xl">
    <div class="mb-6 flex items-center gap-4">
      <h1 class="text-h2 m-0 text-text">Configurações do Perfil</h1>
    </div>

    <form @submit.prevent="handleSubmit" class="bg-surface border border-border rounded-2xl p-6 space-y-6">
      <div>
        <label class="block text-meta text-xs text-muted mb-2">Nome</label>
        <input v-model="form.name" type="text" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
      </div>
      
      <div>
        <label class="block text-meta text-xs text-muted mb-2">Descrição (Bio)</label>
        <textarea v-model="form.description" rows="4" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors"></textarea>
      </div>

      <div>
        <label class="block text-meta text-xs text-muted mb-2">Frase Principal</label>
        <input v-model="form.main_phrase" type="text" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-meta text-xs text-muted mb-2">Email</label>
          <input v-model="form.email" type="email" readonly title="É o e-mail de login do admin (ADMIN_EMAIL no .env do backend)" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-muted cursor-not-allowed focus:outline-none">
          <p class="text-xs text-muted mt-1">E-mail de login; muda pelo .env do backend.</p>
        </div>
        <div>
          <label class="block text-meta text-xs text-muted mb-2">Telefone</label>
          <input v-model="form.cellphone_number" type="text" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
        </div>
      </div>

      <!-- UPLOAD DE ARQUIVOS (SUPABASE) -->
      <div class="grid md:grid-cols-1 gap-6 p-5 bg-background border border-primary/20 rounded-xl">
        <div>
          <label class="block text-meta text-xs text-muted mb-2">Foto de Perfil (Atualize fazendo Upload)</label>
          <input @change="(e) => handleFileChange(e, 'avatar')" type="file" accept="image/jpeg,image/png,image/webp,image/gif" class="w-full bg-background border border-border rounded-xl px-4 py-2 text-text text-body focus:outline-none focus:border-primary transition-colors cursor-pointer file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-background hover:file:bg-primary/80">
          <div v-if="form.avatar_url" class="text-xs text-muted mt-2 flex items-center gap-4">
            <span>Atual: <a :href="fileUrl(form.avatar_url)" target="_blank" class="text-primary hover:underline">Ver Foto</a></span>
            <button type="button" @click="removeFile('avatar')" class="text-error hover:underline">Excluir</button>
          </div>
        </div>
        <div>
          <div class="flex items-center gap-4 mb-2">
            <label class="block text-meta text-xs text-muted">Currículo PDF (Atualize fazendo Upload)</label>
            <div class="flex items-center gap-2 text-xs">
              <button type="button" @click="resumeUploadLang = 'pt'" :class="resumeUploadLang === 'pt' ? 'text-primary font-bold underline' : 'text-muted'">PT</button>
              <span class="text-muted">|</span>
              <button type="button" @click="resumeUploadLang = 'en'" :class="resumeUploadLang === 'en' ? 'text-primary font-bold underline' : 'text-muted'">EN</button>
            </div>
          </div>
          <input @change="(e) => handleFileChange(e, 'curriculum')" type="file" accept="application/pdf" class="w-full bg-background border border-border rounded-xl px-4 py-2 text-text text-body focus:outline-none focus:border-primary transition-colors cursor-pointer file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-background hover:file:bg-primary/80">
          <div v-if="resumeUploadLang === 'pt' && form.curriculum_url" class="text-xs text-muted mt-2 flex items-center gap-4">
            <span>Atual (PT): <a :href="fileUrl(form.curriculum_url)" target="_blank" class="text-primary hover:underline">Ver PDF</a></span>
            <button type="button" @click="removeFile('curriculum_pt')" class="text-error hover:underline">Excluir</button>
          </div>
          <div v-if="resumeUploadLang === 'en' && form.curriculum_en_url" class="text-xs text-muted mt-2 flex items-center gap-4">
            <span>Atual (EN): <a :href="fileUrl(form.curriculum_en_url)" target="_blank" class="text-primary hover:underline">Ver PDF</a></span>
            <button type="button" @click="removeFile('curriculum_en')" class="text-error hover:underline">Excluir</button>
          </div>
        </div>
        <div>
          <label class="block text-meta text-xs text-muted mb-2">Teste de Personalidade PDF (Atualize fazendo Upload)</label>
          <input @change="(e) => handleFileChange(e, 'personality')" type="file" accept="application/pdf" class="w-full bg-background border border-border rounded-xl px-4 py-2 text-text text-body focus:outline-none focus:border-primary transition-colors cursor-pointer file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-background hover:file:bg-primary/80">
          <div v-if="form.personality_test_url" class="text-xs text-muted mt-2 flex items-center gap-4">
            <span>Atual: <a :href="fileUrl(form.personality_test_url)" target="_blank" class="text-primary hover:underline">Ver Teste PDF</a></span>
            <button type="button" @click="removeFile('personality')" class="text-error hover:underline">Excluir</button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-meta text-xs text-muted mb-2">LinkedIn URL</label>
          <input v-model="form.linkedin_url" type="url" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
        </div>
        <div>
          <label class="block text-meta text-xs text-muted mb-2">GitHub URL</label>
          <input v-model="form.github_url" type="url" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
        </div>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-meta text-xs text-muted mb-2">Instagram URL</label>
          <input v-model="form.instagram_url" type="url" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
        </div>
        <div>
          <label class="block text-meta text-xs text-muted mb-2">Medium URL</label>
          <input v-model="form.medium_url" type="url" class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
        </div>
      </div>
      
      <div v-if="errorMsg" class="text-sm text-error bg-error/10 border border-error/20 rounded-xl p-3">
        {{ errorMsg }}
      </div>

      <div v-if="savingStatus" class="text-sm text-primary bg-primary/10 border border-primary/20 rounded-xl p-3">
        {{ savingStatus }}
      </div>

      <div v-if="successMsg" class="text-sm text-success bg-success/10 border border-success/20 rounded-xl p-3">
        {{ successMsg }}
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
import { ref, onMounted, watch } from 'vue'
import { definePageMeta } from '#imports'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useAuth } from '~/composables/useAuth'
import { useFileUrl } from '~/composables/useFileUrl'

definePageMeta({ layout: 'admin', middleware: 'auth' })

const { updateUser, uploadFile } = usePortfolioApi()
const fileUrl = useFileUrl()
const { currentUser, adminUserId, fetchSession } = useAuth()

const form = ref({
  name: '',
  description: '',
  main_phrase: '',
  email: '',
  cellphone_number: '',
  avatar_url: '',
  curriculum_url: '',
  curriculum_en_url: '',
  personality_test_url: '',
  linkedin_url: '',
  github_url: '',
  instagram_url: '',
  medium_url: ''
})

const resumeUploadLang = ref<'pt' | 'en'>('pt')

const avatarFile = ref<File | null>(null)
const curriculumFile = ref<File | null>(null)
const personalityFile = ref<File | null>(null)

const saving = ref(false)
const savingStatus = ref('')
const errorMsg = ref('')
const successMsg = ref('')

onMounted(async () => {
  if (!currentUser.value?.email) {
    await fetchSession()
  }
  syncData()
})

watch(currentUser, () => syncData())

function syncData() {
  if (currentUser.value) {
    form.value.name = currentUser.value.name || ''
    form.value.description = currentUser.value.description || ''
    form.value.main_phrase = currentUser.value.main_phrase || ''
    form.value.email = currentUser.value.email || ''
    form.value.cellphone_number = currentUser.value.cellphone_number || ''
    form.value.avatar_url = currentUser.value.avatar_url || ''
    form.value.curriculum_url = currentUser.value.curriculum_url || ''
    form.value.curriculum_en_url = currentUser.value.curriculum_en_url || ''
    form.value.personality_test_url = currentUser.value.personality_test_url || ''
    form.value.linkedin_url = currentUser.value.linkedin_url || ''
    form.value.github_url = currentUser.value.github_url || ''
    form.value.instagram_url = currentUser.value.instagram_url || ''
    form.value.medium_url = currentUser.value.medium_url || ''
  }
}

function removeFile(type: 'avatar' | 'curriculum_pt' | 'curriculum_en' | 'personality') {
  if (confirm('Tem certeza que deseja remover este arquivo do seu perfil? (Lembre-se de salvar no final)')) {
    if (type === 'avatar') form.value.avatar_url = ''
    if (type === 'curriculum_pt') form.value.curriculum_url = ''
    if (type === 'curriculum_en') form.value.curriculum_en_url = ''
    if (type === 'personality') form.value.personality_test_url = ''
  }
}

function handleFileChange(event: Event, type: 'avatar' | 'curriculum' | 'personality') {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    if (type === 'avatar') avatarFile.value = target.files[0]
    if (type === 'curriculum') curriculumFile.value = target.files[0]
    if (type === 'personality') personalityFile.value = target.files[0]
  }
}

async function handleSubmit() {
  saving.value = true
  errorMsg.value = ''
  successMsg.value = ''
  savingStatus.value = 'Iniciando salvamento...'

  try {
    // O e-mail de login não é editável por aqui (o backend recusaria a troca)
    const { email: _email, ...payload } = form.value
    
    // Process Uploads
    if (avatarFile.value) {
      savingStatus.value = 'Enviando nova foto...'
      payload.avatar_url = await uploadFile(avatarFile.value, 'avatars')
    }
    
    if (curriculumFile.value) {
      savingStatus.value = 'Enviando novo currículo...'
      const uploadedUrl = await uploadFile(curriculumFile.value, 'curriculums')
      if (resumeUploadLang.value === 'pt') {
        payload.curriculum_url = uploadedUrl
      } else {
        payload.curriculum_en_url = uploadedUrl
      }
    }
    
    if (personalityFile.value) {
      savingStatus.value = 'Enviando teste de personalidade...'
      payload.personality_test_url = await uploadFile(personalityFile.value, 'tests')
    }

    // Clean empty values
    Object.keys(payload).forEach(k => {
      if ((payload as any)[k] === '') {
        (payload as any)[k] = null
      }
    })
    
    savingStatus.value = 'Atualizando banco de dados...'
    await updateUser(adminUserId.value, payload)
    await fetchSession() // recarrega o perfil completo (currentUser) com o que acabou de ser salvo

    successMsg.value = 'Perfil atualizado com sucesso!'
  } catch (e: any) {
    console.error(e)
    errorMsg.value = e.message || 'Ocorreu um erro ao salvar as alterações.'
  } finally {
    saving.value = false
    savingStatus.value = ''
    setTimeout(() => { successMsg.value = '' }, 3000)
  }
}
</script>