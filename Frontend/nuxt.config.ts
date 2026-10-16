// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  app: {
    head: {
      title: 'Daniel — Desenvolvedor Full Stack & Mobile',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Portfólio profissional de Daniel - Desenvolvedor Full Stack & Mobile' },
        { name: 'theme-color', content: '#0B1120' }
      ],
      link: [
        // Ícone: balão do "Hire Me" com o prompt ">_" (SVG nítido em qualquer tamanho, PNG de reserva)
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32.png' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=JetBrains+Mono:wght@500&display=swap' }
      ]
    }
  },
  css: [
    '~/assets/css/main.css'
  ],
  routeRules: {
    // Painel autenticado, sem necessidade de SEO — roda só no cliente, o que evita
    // ter que reencaminhar cookies pro backend durante o SSR pra checar login.
    '/admin/**': { ssr: false }
  },
  runtimeConfig: {
    public: {
      // Endereço da API FastAPI. Em produção, defina NUXT_PUBLIC_API_BASE
      // (o Nuxt sobrescreve este valor automaticamente a partir dela).
      // "localhost" e não "127.0.0.1": o site roda em localhost:3000 e, pro navegador,
      // localhost e 127.0.0.1 são sites diferentes, então o cookie de login do admin
      // não era salvo nem enviado.
      apiBase: 'http://localhost:8000'
    }
  }
})
