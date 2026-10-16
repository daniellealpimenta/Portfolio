<template>
  <div class="min-h-screen grid place-items-center bg-background text-text px-6 py-12">
    <div class="card w-full max-w-sm p-8 flex flex-col gap-6">
      <div class="flex flex-col gap-2 text-center">
        <span class="eyebrow justify-center">Hire Me</span>
        <h1 class="title-page">Painel administrativo</h1>
        <p class="text-sm text-muted">
          {{ sent
            ? 'Enviamos um código de 6 dígitos para o seu e-mail. Ele vale por 10 minutos.'
            : 'O código de acesso vai para o e-mail de admin configurado no backend.' }}
        </p>
      </div>

      <!-- Antes de enviar: um botão só. Depois: o campo do código. -->
      <button v-if="!sent" type="button" class="btn btn-primary w-full" :disabled="loading" @click="handleSend">
        {{ loading ? 'Enviando...' : 'Enviar código para o meu e-mail' }}
      </button>

      <form v-else class="flex flex-col gap-4" @submit.prevent="handleCodeSubmit">
        <label for="login-code" class="sr-only">Código</label>
        <input
          id="login-code"
          ref="codeInput"
          v-model="code"
          type="text"
          inputmode="numeric"
          autocomplete="one-time-code"
          pattern="[0-9]{6}"
          maxlength="6"
          required
          placeholder="000000"
          class="field text-center text-2xl tracking-[0.5em] tabular-nums"
          @input="onCodeInput"
        />
        <button type="submit" class="btn btn-primary w-full" :disabled="loading || code.length !== 6">
          {{ loading ? 'Entrando...' : 'Entrar' }}
        </button>
        <button
          type="button"
          class="btn btn-ghost self-center text-sm"
          :disabled="loading || resendCooldown > 0"
          @click="handleSend"
        >
          {{ resendCooldown > 0 ? `Reenviar em ${resendCooldown}s` : 'Reenviar código' }}
        </button>
      </form>

      <p v-if="error" class="text-sm text-danger text-center" role="alert">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { definePageMeta } from '#imports'
import { useAuth } from '~/composables/useAuth'

definePageMeta({ layout: 'auth' })

const { loading, error, requestCode, verifyCode } = useAuth()

// O código vale 10 minutos: se a página for recarregada nesse intervalo,
// volta direto pro campo do código sem mandar outro e-mail.
const SENT_KEY = 'admin-code-sent-at'
const CODE_TTL_MS = 10 * 60 * 1000

const sent = ref(false)
const code = ref('')
const codeInput = ref<HTMLInputElement | null>(null)

const resendCooldown = ref(0)
let cooldownTimer: ReturnType<typeof setInterval> | null = null

function startResendCooldown() {
  resendCooldown.value = 30
  if (cooldownTimer) clearInterval(cooldownTimer)
  cooldownTimer = setInterval(() => {
    resendCooldown.value -= 1
    if (resendCooldown.value <= 0 && cooldownTimer) {
      clearInterval(cooldownTimer)
      cooldownTimer = null
    }
  }, 1000)
}

async function focusCode() {
  await nextTick()
  codeInput.value?.focus()
}

async function handleSend() {
  if (resendCooldown.value > 0) return
  code.value = '' // o código antigo deixa de valer assim que um novo é gerado
  try {
    await requestCode()
    sent.value = true
    try { sessionStorage.setItem(SENT_KEY, String(Date.now())) } catch {}
    startResendCooldown()
    focusCode()
  } catch {
    // a mensagem já fica em `error`, exibida no template
  }
}

function onCodeInput() {
  code.value = code.value.replace(/\D/g, '').slice(0, 6)
  if (code.value.length === 6) handleCodeSubmit()
}

async function handleCodeSubmit() {
  if (code.value.length !== 6 || loading.value) return
  const ok = await verifyCode(code.value)
  if (ok) {
    try { sessionStorage.removeItem(SENT_KEY) } catch {}
  }
}

onMounted(() => {
  error.value = ''
  try {
    const at = Number(sessionStorage.getItem(SENT_KEY) || 0)
    if (at && Date.now() - at < CODE_TTL_MS) {
      sent.value = true
      focusCode()
    }
  } catch {}
})

onUnmounted(() => {
  if (cooldownTimer) clearInterval(cooldownTimer)
})
</script>
