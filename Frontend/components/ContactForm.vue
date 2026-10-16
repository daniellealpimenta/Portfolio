<template>
  <form class="card p-6 md:p-8 flex flex-col gap-4" novalidate @submit.prevent="handleSubmit">
    <div class="grid gap-4 sm:grid-cols-2">
      <div class="flex flex-col gap-1.5">
        <label for="contact-name" class="text-sm small-caps tracking-wide text-muted">{{ t('contact.name') }}</label>
        <input id="contact-name" v-model="name" required maxlength="200" type="text" autocomplete="name" class="field" />
      </div>
      <div class="flex flex-col gap-1.5">
        <label for="contact-email" class="text-sm small-caps tracking-wide text-muted">{{ t('contact.email') }}</label>
        <input id="contact-email" v-model="email" required type="email" autocomplete="email" class="field" />
      </div>
    </div>
    <div class="flex flex-col gap-1.5">
      <label for="contact-subject" class="text-sm small-caps tracking-wide text-muted">{{ t('contact.subject') }}</label>
      <input id="contact-subject" v-model="subject" required maxlength="200" type="text" class="field" />
    </div>
    <div class="flex flex-col gap-1.5">
      <label for="contact-message" class="text-sm small-caps tracking-wide text-muted">{{ t('contact.message') }}</label>
      <textarea id="contact-message" v-model="message" required maxlength="5000" rows="5" class="field resize-none"></textarea>
    </div>

    <div class="flex flex-wrap items-center justify-between gap-4 pt-1">
      <p
        class="text-sm min-h-[1.25rem]"
        :class="status === 'sent' ? 'text-success' : 'text-danger'"
        role="status"
        aria-live="polite"
      >{{ statusText }}</p>
      <button type="submit" class="btn btn-primary" :disabled="sending || !canSend">
        {{ sending ? t('contact.sending') : t('contact.send') }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useI18n } from '~/composables/useI18n'

const { user, sendContactMessage } = usePortfolioApi()
const { t } = useI18n()

const name = ref('')
const email = ref('')
const subject = ref('')
const message = ref('')
const sending = ref(false)
const status = ref<'' | 'sent' | 'error' | 'tooMany'>('')

const canSend = computed(() =>
  !!(name.value.trim() && /\S+@\S+\.\S+/.test(email.value) && subject.value.trim() && message.value.trim() && user.value?.id),
)

const statusText = computed(() => {
  if (status.value === 'sent') return t('contact.sent')
  if (status.value === 'error') return t('contact.error')
  if (status.value === 'tooMany') return t('contact.tooMany')
  return ''
})

async function handleSubmit() {
  if (!canSend.value || !user.value) return
  sending.value = true
  status.value = ''

  try {
    await sendContactMessage({
      user_id: user.value.id,
      name: name.value.trim(),
      email: email.value.trim(),
      subject: subject.value.trim(),
      message: message.value.trim(),
    })
    status.value = 'sent'
    name.value = ''
    email.value = ''
    subject.value = ''
    message.value = ''
  } catch (error: any) {
    console.error('Erro ao enviar mensagem:', error)
    status.value = error?.response?.status === 429 ? 'tooMany' : 'error'
  } finally {
    sending.value = false
  }
}
</script>
