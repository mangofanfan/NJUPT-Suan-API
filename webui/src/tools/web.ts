import axios from 'axios'
import type { FastApiDto } from '@/types/fastapi.ts'

export const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json;charset=UTF-8' },
})

export const admin = axios.create({
  baseURL: '/admin',
  headers: { 'Content-Type': 'application/json;charset=UTF-8' },
})

/**
 * 验证给定的 Token 是否正确。
 * 不读取、不保存，仅在正确时自动设置 admin axios 的验证头。
 */
export async function validateAdminToken(token: string) {
  const success = await axios
    .post(
      '/admin/validateToken',
      { token: token },
      { headers: { 'Content-Type': 'application/json' } },
    )
    .then((res) => res.data)
    .then((data: FastApiDto) => data.success)
  if (success) {
    admin.defaults.headers.common['Authorization'] = `Bearer ${token}`
    console.log('✅ Token 有效，已经为 admin axios 设置。')
  } else {
    console.log('❌ Token 验证失败。')
  }
  return success
}
