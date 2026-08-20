export type Category = { id: number; name: string; description?: string }
export type Instructor = { id: number; name: string; bio?: string; photo?: string | null }
export type Course = { id: number; title: string; description: string; category: Category; instructor: Instructor; price: string | number; image?: string | null; duration?: string | null; is_published?: boolean; is_enrolled?: boolean; created_at?: string }
export type AuthUser = { id: number; email: string; first_name: string; last_name: string; role: 'learner' | 'admin' }
export type TokenPair = { access_token: string; refresh_token: string; token_type?: string; user?: AuthUser }
export type Enrollment = { id: number; course_id: number; course_title: string; enrolled_at: string }
export type CourseList = { items: Course[]; total: number; page: number; page_size: number }

const API_URL = (process.env.NEXT_PUBLIC_API_URL ?? '/api/v1').replace(/\/$/, '')
let accessToken: string | null = null
let refreshToken: string | null = null
const ACCESS_KEY = 'coursehub_access_token'
const REFRESH_KEY = 'coursehub_refresh_token'

function saveTokens(tokens: TokenPair) {
  accessToken = tokens.access_token
  refreshToken = tokens.refresh_token
  if (typeof window !== 'undefined') {
    sessionStorage.setItem(ACCESS_KEY, accessToken)
    sessionStorage.setItem(REFRESH_KEY, refreshToken)
  }
}
function restoreTokens() {
  if (typeof window !== 'undefined' && !accessToken) {
    accessToken = sessionStorage.getItem(ACCESS_KEY)
    refreshToken = sessionStorage.getItem(REFRESH_KEY)
  }
}
async function request<T>(path: string, options: RequestInit = {}, authenticated = false, retry = true): Promise<T> {
  restoreTokens()
  const headers = new Headers(options.headers)
  if (options.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')
  if (authenticated && accessToken) headers.set('Authorization', `Bearer ${accessToken}`)
  let response: Response
  try { response = await fetch(`${API_URL}${path}`, { ...options, headers }) } catch { throw new Error('CourseHub API is not reachable. Start FastAPI on port 8001 and try again.') }
  if (response.status === 401 && retry && refreshToken) {
    try { const next = await request<TokenPair>('/auth/refresh', { method: 'POST', body: JSON.stringify({ refresh_token: refreshToken }) }); saveTokens(next); return request<T>(path, options, authenticated, false) } catch { clearAccessToken() }
  }
  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    const detail = payload?.detail
    throw new Error(Array.isArray(detail) ? detail.map((item: { msg?: string }) => item.msg).join(', ') : detail || `Request failed (${response.status})`)
  }
  return response.status === 204 ? (undefined as T) : response.json()
}

export const coursehubApi = {
  listCourses: (params = '') => request<CourseList>(`/courses${params}`),
  getCourse: (id: number) => request<Course>(`/courses/${id}`),
  login: async (email: string, password: string) => { const tokens = await request<TokenPair>('/auth/login', { method: 'POST', body: JSON.stringify({ email: email.trim(), password }) }); saveTokens(tokens); return tokens.user ?? await coursehubApi.me() },
  register: async (email: string, password: string, first_name: string, last_name: string) => { const tokens = await request<TokenPair>('/auth/register', { method: 'POST', body: JSON.stringify({ email: email.trim(), password, first_name, last_name }) }); saveTokens(tokens); return tokens.user ?? await coursehubApi.me() },
  me: () => request<AuthUser>('/auth/me', {}, true),
  logout: async () => { try { await request('/auth/logout', { method: 'POST' }, true) } finally { clearAccessToken() } },
  enroll: (course_id: number) => request<{ enrollment: Enrollment; already_enrolled: boolean }>('/enrollments', { method: 'POST', body: JSON.stringify({ course_id }) }, true),
  myLearning: () => request<Enrollment[]>('/me/enrollments', {}, true),
  adminCourses: () => request<Course[]>('/admin/courses', {}, true),
  createCourse: (course: Record<string, unknown>) => request<Course>('/admin/courses', { method: 'POST', body: JSON.stringify(course) }, true),
  updateCourse: (id: number, course: Record<string, unknown>) => request<Course>(`/admin/courses/${id}`, { method: 'PATCH', body: JSON.stringify(course) }, true),
  deleteCourse: (id: number) => request(`/admin/courses/${id}`, { method: 'DELETE' }, true),
}
export function clearAccessToken() { accessToken = null; refreshToken = null; if (typeof window !== 'undefined') { sessionStorage.removeItem(ACCESS_KEY); sessionStorage.removeItem(REFRESH_KEY) } }
export function hasSession() { restoreTokens(); return Boolean(accessToken) }
