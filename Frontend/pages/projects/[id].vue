<template>
  <main class="max-w-4xl mx-auto px-6 pb-24" v-if="project">
    <!-- Breadcrumb -->
    <div class="mb-8 pt-8">
      <NuxtLink to="/#work" class="text-meta text-xs hover:text-primary transition-colors inline-flex items-center gap-1">
        &larr; Voltar
      </NuxtLink>
    </div>

    <div class="mb-8">
      <h1 class="text-h1 mb-3">{{ project.title }}</h1>
      <div class="flex items-center gap-4 text-sm text-muted">
        <span>{{ project.year }}</span>
        <span class="capitalize">{{ project.cat }}</span>
        <span class="flex items-center gap-1">
          <svg 
            width="14" height="14" viewBox="0 0 24 24" 
            :fill="project.liked ? 'currentColor' : 'none'" 
            stroke="currentColor" stroke-width="2" 
            stroke-linecap="round" stroke-linejoin="round"
            class="transition-colors"
            :class="project.liked ? 'text-primary' : ''"
          >
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
          </svg>
          {{ project.likes }}
        </span>
      </div>
    </div>

    <!-- Video -->
    <div v-if="videoUrl" class="mb-12 rounded-3xl overflow-hidden border border-border shadow-lg bg-surface aspect-video">
      <video :src="videoUrl" controls class="w-full h-full object-cover"></video>
    </div>

    <!-- Description -->
    <div class="prose prose-invert max-w-none mb-12">
      <p class="text-body text-muted leading-relaxed whitespace-pre-line">{{ project.desc }}</p>
    </div>

    <!-- Links -->
    <div v-if="links.length > 0" class="flex flex-wrap gap-4 mb-16">
      <a
        v-for="link in links"
        :key="link.id"
        :href="link.url"
        target="_blank"
        rel="noopener noreferrer"
        class="px-6 py-3 rounded-full border border-border bg-surface text-sm font-display small-caps hover:bg-border transition flex items-center gap-2"
      >
        <IconRenderer :icon="link.icon" :size="16" />
        {{ link.name }}
      </a>
    </div>

    <!-- Gallery -->
    <div v-if="galleryImages.length > 0">
      <h2 class="font-display text-2xl small-caps text-text font-semibold mb-6">Galeria</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div v-for="(img, idx) in galleryImages" :key="idx" class="rounded-2xl overflow-hidden border border-border bg-surface aspect-[4/3]">
          <img :src="img.image_path" alt="Project Image" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" />
        </div>
      </div>
    </div>
  </main>
  <div v-else-if="!loading" class="max-w-4xl mx-auto px-6 py-24 text-center">
    <h1 class="text-h2 text-text mb-4">Projeto não encontrado</h1>
    <NuxtLink to="/#work" class="text-primary hover:underline">Voltar à página inicial</NuxtLink>
  </div>
  <div v-else class="max-w-4xl mx-auto px-6 py-24 text-center text-muted">
    Carregando...
  </div>
</template>

<style scoped>
/* Removed old heart icon mask */
</style>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePortfolioApi, type Project, type ProjectLink } from '~/composables/usePortfolioApi'
import IconRenderer from '~/components/ui/IconRenderer.vue'

const route = useRoute()
const { getProjectImages, getProjectLinks } = usePortfolioApi()
const projectId = route.params.id as string

const project = ref<Project | null>(null)
const images = ref<any[]>([])
const links = ref<ProjectLink[]>([])
const loading = ref(true)

const videoUrl = computed(() => {
  const vid = images.value.find(img => img.image_path.toLowerCase().endsWith('.mp4') || img.image_path.toLowerCase().endsWith('.webm'))
  return vid ? vid.image_path : null
})

const galleryImages = computed(() => {
  return images.value.filter(img => !img.image_path.toLowerCase().endsWith('.mp4') && !img.image_path.toLowerCase().endsWith('.webm'))
})

const apiBase = useRuntimeConfig().public.apiBase

onMounted(async () => {
  try {
    loading.value = true
    const { user, loadData, projects } = usePortfolioApi()
    
    // We need the project info. It might already be in 'projects' state if we navigated from home.
    if (projects.value.length === 0) {
      // If refreshed directly on this page, we must fetch projects. But we need userId.
      // Alternatively, we can fetch project directly from backend.
      const res = await $fetch<any>(`${apiBase}/projects/${projectId}`)
      if (res) {
        project.value = {
          id: res.id,
          title: res.name || res.title,
          year: res.date ? new Date(res.date).getFullYear() : (res.year || 2025),
          likes: res.likes ?? 0,
          cat: (res.categories && res.categories[0]) || 'back',
          desc: res.description || res.desc || ''
        }
      }
    } else {
      project.value = projects.value.find(p => p.id === projectId) || null
    }

    if (project.value) {
      // Fetch images
      const imgRes = await getProjectImages(projectId)
      if (imgRes && Array.isArray(imgRes)) {
        images.value = imgRes
      }
      // Fetch links
      try {
        links.value = await getProjectLinks(projectId)
      } catch (e) {
        console.error('Erro ao carregar links do projeto:', e)
      }
    }
  } catch (error) {
    console.error('Failed to load project details', error)
  } finally {
    loading.value = false
  }
})
</script>
