# CHANGELOG

此文件中记录 NJUPT Suan API 的主要的版本变更日志。

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

6 种更新类别：Added、Changed、Deprecated、Removed、Fixed、Security。

## [0.1.4] - 2026-04-26

### Fixed

- 修复从命令行运行 `njupt-suan-api init` 时由于 playwright 命令未找到而失败的问题。

## [0.1.3] - 2026-04-26

### Changed

- 更改项目的 cli 入口别名与包名 `njupt-suan-api` 一致，以支持更简单地通过 uv tool / uvx 部署本项目。
- 依赖更新：
    - fastapi -> 0.136.1
    - typer -> 0.25.0
