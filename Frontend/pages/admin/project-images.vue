<template>
  <div class="space-y-6 max-w-5xl">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-h1 mb-1">Mídia de Projetos</h1>
        <p class="text-body text-muted text-sm">Adicione fotos e vídeos aos seus projetos.</p>
      </div>
    </div>

    <div class="bg-surface border border-border rounded-2xl overflow-hidden p-6">
      <div v-if="loading" class="text-center text-muted animate-pulse">Carregando...</div>
      
      <div v-else>
        <!-- Select Project -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-meta text-muted mb-2">Selecione o Projeto</label>
          <select 
            v-model="selectedProjectId" 
            class="w-full bg-background border border-border rounded-xl px-4 py-3 text-text focus:outline-none focus:border-primary transition"
            @change="loadProjectImages"
          >
            <option value="" disabled>Escolha um projeto...</option>
            <option v-for="proj in projects" :key="proj.id" :value="proj.id">{{ proj.title }}</option>
          </select>
        </div>

        <!-- Add Image Form -->
        <div v-if="selectedProjectId" class="mb-8 p-4 border border-border rounded-xl bg-background/50">
          <h3 class="text-sm font-display small-caps font-semibold mb-4 text-paper">Adicionar Nova Mídia</h3>
          <form @submit.prevent="handleAddImage" class="flex gap-4 items-end">
            <div class="flex-1">
              <label class="block text-xs font-medium text-muted mb-1">URL da Imagem / Vídeo</label>
              <input 
                v-model="newImageUrl" 
                type="url" 
                required 
                placeholder="https://exemplo.com/imagem.png"
                class="w-full bg-background border border-border rounded-xl px-4 py-2 text-text focus:outline-none focus:border-primary transition"
              />
            </div>
            <button 
              type="submit" 
              :disabled="saving"
              class="bg-primary text-background px-6 py-2.5 rounded-xl font-semibold hover:opacity-90 transition disabled:opacity-50"
            >
              {{ saving ? 'Adicionando...' : 'Adicionar' }}
            </button>
          </form>
          <p class="text-xs text-muted mt-2">Dica: Se a URL terminar em .mp4 ou .webm, será tratada como vídeo.</p>
        </div>

        <!-- Project Images List -->
        <div v-if="selectedProjectId">
          <h3 class="text-sm font-display small-caps font-semibold mb-4 text-paper">Mídias do Projeto</h3>
          
          <div v-if="loadingImages" class="text-center text-muted animate-pulse py-4">Carregando mídias...</div>
          
          <div v-else-if="currentImages.length > 0" class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div 
              v-for="img in currentImages" 
              :key="img.id" 
              class="relative rounded-xl overflow-hidden border border-border aspect-square group bg-background"
            >
              <video v-if="isVideo(img.image_path)" :src="img.image_path" class="w-full h-full object-cover"></video>
              <img v-else :src="img.image_path" alt="Project Media" class="w-full h-full object-cover" />
              
              <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <button @click="handleDeleteImage(img.id)" class="text-error bg-error/20 px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-error/40 transition">
                  Excluir
                </button>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center text-muted py-8 bg-background rounded-xl border border-border">
            Nenhuma mídia cadastrada para este projeto.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { definePageMeta } from '#imports'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useAuth } from '~/composables/useAuth'

definePageMeta({ layout: 'admin', middleware: 'auth' })

const { projects, loading, loadData, getProjectImages, createProjectImage, deleteProjectImage } = usePortfolioApi()
const { adminUserId } = useAuth()

const selectedProjectId = ref('')
const currentImages = ref<any[]>([])
const loadingImages = ref(false)
const newImageUrl = ref('')
const saving = ref(false)

onMounted(() => {
  loadData(adminUserId.value)
})

const isVideo = (url: string) => {
  if (!url) return false
  const lower = url.toLowerCase()
  return lower.endsWith('.mp4') || lower.endsWith('.webm')
}

const loadProjectImages = async () => {
  if (!selectedProjectId.value) return
  loadingImages.value = true
  try {
    const images = await getProjectImages(selectedProjectId.value)
    currentImages.value = images || []
  } catch (error) {
    console.error('Erro ao carregar imagens:', error)
    currentImages.value = []
  } finally {
    loadingImages.value = false
  }
}

const handleAddImage = async () => {
  if (!newImageUrl.value || !selectedProjectId.value) return
  saving.value = true
  try {
    await createProjectImage({
      project_id: selectedProjectId.value,
      image_path: newImageUrl.value
    })
    newImageUrl.value = ''
    await loadProjectImages()
  } catch (error) {
    alert('Erro ao adicionar mídia.')
    console.error(error)
  } finally {
    saving.value = false
  }
}

const handleDeleteImage = async (imageId: string) => {
  if (!confirm('Tem certeza que deseja excluir esta mídia?')) return
  try {
    await deleteProjectImage(imageId)
    await loadProjectImages()
  } catch (error) {
    alert('Erro ao excluir mídia.')
    console.error(error)
  }
}
</script>
