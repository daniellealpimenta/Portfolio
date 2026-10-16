import { gsap } from 'gsap'

export default defineNuxtPlugin((nuxtApp) => {
  if (!import.meta.client) return

  nuxtApp.hook('app:mounted', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const isFinePointer = window.matchMedia('(pointer: fine)').matches

    if (!isFinePointer) {
      document.documentElement.classList.add('no-fine-pointer')
    }

    initStarfield({ reduceMotion })
    initCursorGlow({ enabled: isFinePointer && !reduceMotion })
    initMagneticButtons({ enabled: isFinePointer && !reduceMotion })
    // initScrollDots() is now handled natively by components/ui/ScrollSpy.vue
  })
})

/* Starfield Canvas Background (Optimized 60 FPS) */
function initStarfield({ reduceMotion }: { reduceMotion: boolean }) {
  if (document.body.classList.contains('light')) return

  let canvas = document.getElementById('starfield') as HTMLCanvasElement | null
  if (!canvas) {
    canvas = document.createElement('canvas')
    canvas.id = 'starfield'
    document.body.prepend(canvas)
  }

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  let stars: Array<{ x: number; y: number; r: number; baseAlpha: number; phase: number; speed: number }> = []
  let width = 0
  let height = 0

  function resize() {
    if (!canvas) return
    width = canvas.width = window.innerWidth
    height = canvas.height = window.innerHeight
    const density = Math.min(90, Math.floor((width * height) / 12000))
    stars = Array.from({ length: density }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 1.2 + 0.3,
      baseAlpha: Math.random() * 0.4 + 0.2,
      phase: Math.random() * Math.PI * 2,
      speed: Math.random() * 0.001 + 0.0005,
    }))
  }

  function draw(time: number) {
    if (!ctx) return
    ctx.clearRect(0, 0, width, height)
    ctx.fillStyle = '#F1F0F7'
    
    for (let i = 0; i < stars.length; i++) {
      const s = stars[i]
      const twinkle = reduceMotion ? s.baseAlpha : s.baseAlpha + Math.sin(time * s.speed + s.phase) * 0.15
      ctx.globalAlpha = Math.max(0.1, Math.min(0.8, twinkle))
      ctx.beginPath()
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2)
      ctx.fill()
    }
    ctx.globalAlpha = 1
    if (!reduceMotion) requestAnimationFrame(draw)
  }

  resize()
  window.addEventListener('resize', resize)
  requestAnimationFrame(draw)
}

/* Fast & Fluid Cursor Glow (0.15s duration) */
function initCursorGlow({ enabled }: { enabled: boolean }) {
  if (!enabled) return

  let glow = document.querySelector('.cursor-glow') as HTMLDivElement | null
  if (!glow) {
    glow = document.createElement('div')
    glow.className = 'cursor-glow'
    document.body.appendChild(glow)
  }

  const moveX = gsap.quickTo(glow, 'x', { duration: 0.15, ease: 'power2.out' })
  const moveY = gsap.quickTo(glow, 'y', { duration: 0.15, ease: 'power2.out' })

  window.addEventListener('mousemove', e => {
    moveX(e.clientX)
    moveY(e.clientY)
  })
}

/* Magnetic Buttons Attraction
   Delegação no document: funciona também em botões que aparecem depois
   (dados da API, troca de página). Volta ao lugar sem elástico (MASTER.md: sem bounce). */
function initMagneticButtons({ enabled }: { enabled: boolean }) {
  if (!enabled) return

  const strength = 0.3
  let active: HTMLElement | null = null

  const release = (el: HTMLElement) => {
    gsap.to(el, { x: 0, y: 0, duration: 0.32, ease: 'power3.out' })
  }

  document.addEventListener('pointermove', e => {
    const target = (e.target as Element | null)?.closest?.('[data-magnetic]') as HTMLElement | null
    if (active && active !== target) {
      release(active)
      active = null
    }
    if (!target) return
    active = target
    const rect = target.getBoundingClientRect()
    const x = (e.clientX - (rect.left + rect.width / 2)) * strength
    const y = (e.clientY - (rect.top + rect.height / 2)) * strength
    gsap.to(target, { x, y, duration: 0.18, ease: 'power3.out' })
  }, { passive: true })

  document.addEventListener('pointerleave', () => {
    if (active) release(active)
    active = null
  })
}

// Scroll-Spy Dots logic was removed in favor of components/ui/ScrollSpy.vue
