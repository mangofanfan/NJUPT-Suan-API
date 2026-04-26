# NJUPT Suan API

NJUPT Suan API 是一个 FastAPI 项目，目标在于实现对 NJUPT（南京邮电大学）的信息获取 API 和 MCP 服务。

在 `pyproject.toml` 中，本项目的包名，以及命令行入口名为 `njupt-suan-api`。

## 文档

虽然项目还没个两样，但是文档其实也没个两样 ~~（什么东西）~~

[中文名叫芒果酸](https://suan.mangofanfan.cn) - `suan.mangofanfan.cn`

## 功能

| 计划功能（芒果画饼中）   | 支持进度          |
|---------------|---------------|
| 教务系统 - 课程表获取  | ✅             |
| 教务系统 - 课程获取   | ⌛️            |
| 教务系统 - 成绩获取   | ⌛️            |
| 体育部系统 - 早锻炼获取 | ⌛️（等待体育部系统修复） |

## 运行

建议查阅文档了解更多部署方式。

如需从源代码直接运行的话，项目的源码位于 `src/njupt_suan_api` 目录下，`main.py` 是旧的入口文件，可以直接传统方式启动。

`manage.py` 是命令行入口，提供了完整的帮助信息。

`server.py` 是 FastAPI app 所在文件，可以使用 uvicorn 命令启动。

另外如需从源代码启动项目，你需要自行构建 WebUI。

```bash
cd webui/
pnpm install
pnpm run build
```

AI 说 `npm install` 然后 `npm run build` 也可以，但我还没试过，你可以帮我试试（？）

vite 的构建产物会放在 `src/njupt_suan_api/static` 目录下，**构建产物不会被 git 管理，但是会被项目打包进 wheel。**
