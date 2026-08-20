'use client'

import Link from 'next/link'
import { FormEvent, useState } from 'react'
import { ArrowLeft, Crown, Loader2, Shield } from 'lucide-react'
import { AuthUser, coursehubApi } from '@/lib/coursehub-api'
import { useRouter } from 'next/navigation'

export default function AdminLoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')

  async function submit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setMessage('')
    try {
      const profile: AuthUser = await coursehubApi.login(email, password)
      if (profile.role !== 'admin') throw new Error('This account does not have admin access.')
      router.replace('/admin')
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Admin sign in failed.')
    } finally {
      setBusy(false)
    }
  }

  return <main className="min-h-screen bg-background text-foreground"><header className="border-b border-border"><div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10"><Link href="/" className="flex items-center gap-3"><span className="brand-mark"><Crown size={17} /></span><span className="font-serif text-xl font-semibold text-primary">CourseHub</span></Link><Link href="/" className="inline-flex items-center gap-2 text-sm font-semibold text-primary"><ArrowLeft size={15} /> Collection</Link></div></header><section className="mx-auto grid min-h-[calc(100vh-89px)] max-w-7xl place-items-center px-6 py-16 lg:px-10"><form onSubmit={submit} className="w-full max-w-md border border-border bg-card p-8 shadow-xl"><div className="flex items-center gap-3"><Shield className="text-accent" size={20} /><p className="eyebrow">CourseHub admin</p></div><h1 className="mt-5 font-serif text-4xl text-primary">Sign in to the studio.</h1><p className="mt-4 text-sm leading-6 text-muted-foreground">Manage courses and the learning collection with your administrator account.</p><div className="mt-8 grid gap-4"><label className="grid gap-2 text-sm font-semibold text-primary">Email<input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="username" className="border border-border bg-background p-3 font-normal outline-none focus:border-accent" /></label><label className="grid gap-2 text-sm font-semibold text-primary">Password<input required type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" className="border border-border bg-background p-3 font-normal outline-none focus:border-accent" /></label>{message && <p className="text-sm font-semibold text-accent" role="alert">{message}</p>}<button disabled={busy} className="button-primary px-4 py-3">{busy ? <Loader2 className="mx-auto animate-spin" size={17} /> : 'Sign in as admin'}</button></div></form></section></main>
}
