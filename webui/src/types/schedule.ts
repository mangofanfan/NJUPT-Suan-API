export interface CourseDto {
  classroom: string
  name: string
  alias: string | null
  teacher: string
  day: number
  weeks: number[]
  classes: number[]
}

export interface CourseDatumDto {
  name: string
  alias: string | null
  teacher: string
  classroom: string
  during: number
}

export interface AliasDto {
  id: number
  originalName: string
  aliasName: string
}
