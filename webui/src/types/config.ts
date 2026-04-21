export interface ConfigSystemDto {
  host?: string
  port?: number
  reload?: boolean
}

export interface ConfigScheduleDto {
  playwright_headless?: true
  jwxt_login_method?: 'jwxt' | 'sso'
  semester_start_date?: string
  schedule_title_template?: string
  schedule_subtitle_template?: string
}

export interface ConfigLogDto {
  log_api_request_details?: boolean
  log_mcp_request_details?: boolean
  log_assets_request?: boolean
}

export interface ConfigDataDto {
  system: ConfigSystemDto
  schedule: ConfigScheduleDto
  log: ConfigLogDto
}
