import { ref, type Ref } from 'vue'
import { zh, en, type MessageKey } from '../i18n/messages'

export type Locale = 'zh' | 'en'

const LOCALE_KEY = 'uisvg-editor-locale'

function loadInitialLocale(): Locale {
  const s = localStorage.getItem(LOCALE_KEY)
  if (s === 'en' || s === 'zh') return s
  return 'zh'
}

/** 供非组件模块在启动时同步 `document.documentElement.lang` */
export function initDocumentLangFromStorage(): void {
  if (typeof document === 'undefined') return
  const s = localStorage.getItem(LOCALE_KEY)
  document.documentElement.lang = s === 'en' ? 'en' : 'zh-CN'
}

function interpolate(s: string, params?: Record<string, string | number>): string {
  if (!params) return s
  return s.replace(/\{(\w+)\}/g, (_, k: string) =>
    params[k] !== undefined ? String(params[k]) : `{${k}}`,
  )
}

/** 全局单例 locale，保证各组件共用同一语言状态 */
const locale = ref<Locale>(loadInitialLocale())

export function useI18n(): {
  locale: Ref<Locale>
  t: (key: MessageKey, params?: Record<string, string | number>) => string
  setLocale: (l: Locale) => void
} {
  function t(key: MessageKey, params?: Record<string, string | number>): string {
    locale.value
    const map = locale.value === 'zh' ? zh : en
    const raw = map[key] ?? key
    return interpolate(raw, params)
  }

  function setLocale(l: Locale) {
    locale.value = l
    localStorage.setItem(LOCALE_KEY, l)
    if (typeof document !== 'undefined') {
      document.documentElement.lang = l === 'zh' ? 'zh-CN' : 'en'
    }
  }

  return { locale, t, setLocale }
}

/** 脚本中根据当前语言取文案（不订阅响应式；仅用于非组件逻辑） */
export function tStatic(key: MessageKey, params?: Record<string, string | number>): string {
  const map = locale.value === 'zh' ? zh : en
  return interpolate(map[key] ?? key, params)
}
