<template>
  <ul class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
    <li v-for="cert in certificates" :key="cert.id" class="card p-6 flex flex-col gap-3" data-reveal>
      <span class="eyebrow">{{ cert.issuer }}</span>
      <h3 class="title-item">{{ cert.title }}</h3>
      <p class="text-sm text-muted tabular-nums">
        <template v-if="cert.workload">{{ cert.workload }}{{ t('about.hours') }}</template>
        <template v-if="cert.workload && cert.issue_date"> · </template>
        <template v-if="cert.issue_date">{{ formatDate(cert.issue_date) }}</template>
      </p>
      <p v-if="cert.description" class="text-sm text-muted leading-relaxed line-clamp-3">{{ cert.description }}</p>
      <a
        v-if="cert.digital_certificate_url"
        :href="cert.digital_certificate_url"
        target="_blank"
        rel="noopener noreferrer"
        class="btn btn-ghost self-start mt-auto"
      >{{ t('about.certSee') }} →</a>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { useI18n } from '~/composables/useI18n'

defineProps<{
  certificates: Array<{
    id: string | number
    title: string
    issuer: string
    workload?: number
    issue_date?: string
    description?: string
    digital_certificate_url?: string
  }>
}>()

const { t, locale } = useI18n()

function formatDate(iso: string) {
  const d = new Date(`${iso.substring(0, 10)}T12:00:00`)
  return isNaN(d.getTime()) ? iso : d.toLocaleDateString(locale.value, { month: 'short', year: 'numeric' })
}
</script>
