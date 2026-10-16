<template>
  <div ref="pageRef" class="pt-10 pb-24 md:pt-16">
    <div class="container-page">
      <NuxtLink :to="`/${route.params.user_id}/work`" class="btn btn-ghost -ml-1 mb-8">← {{ t('project.back') }}</NuxtLink>

      <p v-if="loading" class="py-20 text-center text-muted" role="status">{{ t('project.loading') }}</p>

      <article v-else-if="project" class="flex flex-col gap-12">
        <header class="flex flex-col gap-5 max-w-3xl" data-reveal>
          <span class="eyebrow tabular-nums">{{ project.year }}<template v-if="project.categories.length"> · {{ project.categories.join(' · ') }}</template></span>
          <h1 class="hero-statement font-semibold small-caps text-text text-balance">{{ project.title }}</h1>
          <div v-if="projectLinks.length" class="flex flex-wrap items-center gap-3 pt-1">
            <a
              v-for="(link, i) in projectLinks"
              :key="link.id"
              :href="link.url"
              target="_blank"
              rel="noopener noreferrer"
              class="btn"
              :class="i === 0 ? 'btn-primary' : 'btn-secondary'"
            >
              <IconRenderer :icon="link.icon" :size="16" />
              {{ link.name }}
            </a>
          </div>
        </header>

        <!-- Mídia principal: vídeo, senão a primeira imagem, senão a capa desenhada -->
        <div class="card overflow-hidden" data-reveal>
          <video v-if="videoMedia" controls playsinline class="w-full aspect-video bg-background">
            <source :src="videoMedia.image_path" />
            {{ t('project.noVideo') }}
          </video>
          <img v-else-if="imageMedias.length" :src="imageMedias[0].image_path" :alt="imageMedias[0].description || ''" class="w-full aspect-video object-cover" />
          <ProjectCover v-else :title="project.title" :categories="project.categories" large class="aspect-[21/9]" />
        </div>

        <div v-if="renderedDescription" class="markdown-content text-lg leading-relaxed text-text max-w-prose" data-reveal v-html="renderedDescription"></div>

        <section v-if="galleryImages.length" class="flex flex-col gap-6 pt-12 border-t border-divider" aria-labelledby="gallery-title">
          <h2 id="gallery-title" class="title-section" data-reveal>{{ t('project.gallery') }}</h2>
          <div class="grid gap-6 md:grid-cols-2">
            <figure v-for="(img, idx) in galleryImages" :key="idx" class="card overflow-hidden" data-reveal>
              <img :src="img.image_path" :alt="img.description || ''" loading="lazy" class="w-full h-auto" />
              <figcaption v-if="img.description" class="p-4 text-sm text-muted border-t border-divider">{{ img.description }}</figcaption>
            </figure>
          </div>
        </section>
      </article>

      <div v-else class="py-20 flex flex-col items-center gap-6 text-center">
        <p class="text-lead">{{ t('project.notFound') }}</p>
        <NuxtLink :to="`/${route.params.user_id}/work`" class="btn btn-secondary">{{ t('project.back') }}</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { usePortfolioApi, type ProjectLink } from '~/composables/usePortfolioApi'
import { useI18n } from '~/composables/useI18n'
import { useReveal } from '~/composables/useReveal'
import IconRenderer from '~/components/ui/IconRenderer.vue'
import ProjectCover from '~/components/ui/ProjectCover.vue'

const route = useRoute()
const projectId = route.params.project_id as string
const { projects, loadData, getProjectImages, getProjectLinks } = usePortfolioApi()
const { t } = useI18n()

const loading = ref(true)
const projectMedias = ref<any[]>([])
const projectLinks = ref<ProjectLink[]>([])
const pageRef = ref<HTMLElement | null>(null)

const project = computed(() => projects.value.find(p => String(p.id) === projectId))

const renderedDescription = computed(() => (project.value?.desc ? marked.parse(project.value.desc) : ''))

const isVideo = (m: any) => /\.(mp4|webm|mov)$/i.test(m.image_path || '')
const videoMedia = computed(() => projectMedias.value.find(isVideo))
const imageMedias = computed(() => projectMedias.value.filter(m => m.image_path && !isVideo(m)))
// Sem vídeo, a primeira imagem vira a mídia principal e não se repete na galeria
const galleryImages = computed(() => (videoMedia.value ? imageMedias.value : imageMedias.value.slice(1)))

useReveal(pageRef, () => [loading.value, projectMedias.value.length])

onMounted(async () => {
  if (projects.value.length === 0) {
    await loadData(route.params.user_id as string)
  }
  if (project.value) {
    const [medias, links] = await Promise.allSettled([getProjectImages(projectId), getProjectLinks(projectId)])
    if (medias.status === 'fulfilled') projectMedias.value = medias.value
    if (links.status === 'fulfilled') projectLinks.value = links.value
  }
  loading.value = false
})
</script>

<style>
/* Estilos do markdown renderizado (v-html) — a página não tem o plugin de
   tipografia do Tailwind instalado, então isso é escrito à mão, usando as
   variáveis de tema do site. overflow-wrap/overflow-x são de propósito:
   sem eles, um link comprido ou uma linha de código longa estoura a
   largura da página inteira. */
.markdown-content {
  overflow-wrap: anywhere;
  word-break: break-word;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4 {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 600;
  font-variant: small-caps;
  letter-spacing: 0.03em;
  color: var(--color-text);
  line-height: 1.25;
  margin-top: 2rem;
  margin-bottom: 1rem;
}
.markdown-content h1 { font-size: 1.75rem; }
.markdown-content h2 { font-size: 1.5rem; }
.markdown-content h3 { font-size: 1.25rem; }
.markdown-content h4 { font-size: 1.125rem; }
.markdown-content > :first-child {
  margin-top: 0;
}

.markdown-content p {
  margin-bottom: 1.5rem;
}

.markdown-content strong {
  color: var(--color-text);
  font-weight: 700;
}

.markdown-content a {
  color: var(--color-primary);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.markdown-content ul,
.markdown-content ol {
  margin: 0 0 1.5rem 1.5rem;
  color: var(--color-text);
}
.markdown-content ul { list-style: disc; }
.markdown-content ol { list-style: decimal; }
.markdown-content li { margin-bottom: 0.5rem; }

.markdown-content code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.875em;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  padding: 0.125rem 0.375rem;
  color: var(--color-primary);
}

.markdown-content pre {
  background-color: var(--color-surface);
  border: 1px solid var(--color-divider);
  border-radius: 16px;
  padding: 1.25rem;
  margin: 0 0 1.5rem;
  overflow-x: auto;
  max-width: 100%;
}
.markdown-content pre code {
  background: none;
  border: none;
  padding: 0;
  color: var(--color-text);
  white-space: pre;
  overflow-wrap: normal;
  word-break: normal;
}

.markdown-content table {
  display: block;
  overflow-x: auto;
  max-width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}
.markdown-content th,
.markdown-content td {
  border: 1px solid var(--color-border);
  padding: 0.5rem 1rem;
  text-align: left;
  white-space: nowrap;
}
.markdown-content th {
  background-color: var(--color-surface);
  color: var(--color-text);
  font-weight: 600;
}

.markdown-content blockquote {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-left: 3px solid var(--color-primary);
  border-radius: 1rem;
  padding: 1.5rem;
  margin: 0 0 1.5rem;
  font-style: italic;
  color: var(--color-muted);
}
.markdown-content blockquote p {
  margin-bottom: 0.5rem;
}
.markdown-content blockquote p:last-child {
  margin-bottom: 0;
}
</style>
