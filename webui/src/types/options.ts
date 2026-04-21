import type {SelectOption} from 'naive-ui'

export const scheduleTypeOptions: SelectOption[] = [
  {
    label: '班级课表',
    value: 'class',
  },
  {
    label: '学生个人课表',
    value: 'student',
  },
]

export const JwxtLoginMethodOptions: SelectOption[] = [
  {
    label: '教务系统直接登录',
    value: 'jwxt',
  },
  {
    label: 'SSO 统一身份认证',
    value: 'sso',
  },
]
