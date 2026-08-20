'use client'

import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { ArrowLeft, BookOpen, Check, Clock3, GraduationCap, Loader2, LockKeyhole, PlayCircle, ShieldCheck, Sparkles } from 'lucide-react'
import { coursehubApi, type Course } from '@/lib/coursehub-api'

const fallbackLessons = ['Foundations and core principles', 'A practical framework for confident decisions', 'Live application and reflection', 'Your 30-day mastery plan']

export default function CourseDetailPage() {
  const params = useParams<{ id: string }>()
  const [course, setCourse] = useState<Course | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [enrolling, setEnrolling] = useState(false)
  const [enrolled, setEnrolled] = useState(false)

  useEffect(() => {
    let active = true
    async function load() {
      try {
        const result = await coursehubApi.getCourse(params.id)
        if (active) setCourse(result)
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : 'This course could not be loaded.')
      } finally {
        if (active) setLoading(false)
      }
    }
    if (params.id) load()
    return () => { active = false }
  }, [params.id])

  async function handleEnroll() {
    if (!course) return
    setEnrolling(true)
    setError('')
    try {
      await coursehubApi.enroll(course.id)
      setEnrolled(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Please sign in before enrolling.')
    } finally {
      setEnrolling(false)
    }
  }

  if (loading) return <main className="min-h-screen bg-background px-6 py-20 text-foreground"><div className="mx-auto flex max-w-6xl items-center justify-center gap-3"><Loader2 className="animate-spin" /> Loading course details</div></main>
  if (!course) return <main className="min-h-screen bg-background px-6 py-20 text-foreground"><div className="mx-auto max-w-2xl text-center"><p className="font-mono text-xs uppercase tracking-[0.2em] text-primary">Course unavailable</p><h1 className="mt-4 font-serif text-4xl">We couldn&apos;t find that course.</h1><p className="mt-4 text-muted-foreground">{error || 'The course may have been unpublished or removed.'}</p><Link href="/" className="mt-8 inline-flex items-center gap-2 rounded-full bg-primary px-5 py-3 font-semibold text-primary-foreground"><ArrowLeft className="size-4" /> Back to catalog</Link></div></main>

  return (
    <main className="min-h-screen bg-background text-foreground">
      <header className="border-b border-border/60 bg-background/90 px-6 py-5 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <Link href="/" className="inline-flex items-center gap-2 text-sm font-semibold text-primary"><ArrowLeft className="size-4" /> CourseHub catalog</Link>
          <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Private masterclass</span>
        </div>
      </header>
      <section className="mx-auto grid max-w-6xl gap-12 px-6 py-14 lg:grid-cols-[1fr_360px] lg:py-24">
        <div>
          <div className="flex flex-wrap items-center gap-3 font-mono text-[11px] uppercase tracking-[0.18em] text-primary"><span>{course.category.name}</span><span className="text-border">/</span><span>{course.level}</span></div>
          <h1 className="mt-6 max-w-3xl font-serif text-5xl leading-[0.98] tracking-tight sm:text-7xl">{course.title}</h1>
          <p className="mt-8 max-w-2xl text-lg leading-8 text-muted-foreground">{course.description}</p>
          <div className="mt-10 flex flex-wrap gap-6 border-y border-border/70 py-6 text-sm text-muted-foreground"><span className="inline-flex items-center gap-2"><Clock3 className="size-4 text-primary" /> 8 weeks</span><span className="inline-flex items-center gap-2"><BookOpen className="size-4 text-primary" /> Guided curriculum</span><span className="inline-flex items-center gap-2"><GraduationCap className="size-4 text-primary" /> Certificate included</span></div>
          <div className="mt-12"><p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Your curriculum</p><div className="mt-5 divide-y divide-border/70 rounded-2xl border border-border/70">{fallbackLessons.map((lesson, index) => <div key={lesson} className="flex items-center gap-4 px-5 py-5"><span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-secondary font-mono text-xs text-primary">0{index + 1}</span><span className="font-medium">{lesson}</span><PlayCircle className="ml-auto size-4 text-muted-foreground" /></div>)}</div></div>
        </div>
        <aside className="h-fit rounded-3xl border border-primary/20 bg-card p-7 shadow-[0_24px_70px_-32px_hsl(var(--primary)/0.45)] lg:sticky lg:top-8"><div className="flex items-center gap-3 text-sm font-semibold"><span className="flex size-11 items-center justify-center rounded-full bg-secondary text-primary"><Sparkles className="size-5" /></span><span>Executive access</span></div><div className="mt-8 font-serif text-4xl">${course.price}</div><p className="mt-2 text-sm leading-6 text-muted-foreground">One focused investment in your next level of capability.</p><button onClick={handleEnroll} disabled={enrolling || enrolled} className="mt-8 flex w-full items-center justify-center gap-2 rounded-full bg-primary px-5 py-4 font-semibold text-primary-foreground transition hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-70">{enrolling ? <Loader2 className="size-4 animate-spin" /> : enrolled ? <Check className="size-4" /> : <LockKeyhole className="size-4" />}{enrolled ? 'You are enrolled' : enrolling ? 'Enrolling…' : 'Enroll in course'}</button>{error && <p className="mt-4 rounded-xl bg-destructive/10 p-3 text-sm text-destructive">{error}</p>}<div className="mt-7 space-y-3 border-t border-border/70 pt-6 text-sm text-muted-foreground"><p className="flex items-center gap-2"><ShieldCheck className="size-4 text-primary" /> Secure enrollment</p><p className="flex items-center gap-2"><GraduationCap className="size-4 text-primary" /> {course.instructor.name}</p></div></aside>
      </section>
    </main>
  )
}
