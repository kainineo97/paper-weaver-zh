# paper-weaver-zh

`paper-weaver-zh` 是一个本地 Codex skill：把科研论文、补充材料和研究讨论整理成证据可追溯的中文科研长文，并生成微信公众号草稿、独立阅读页和富文本预览。

当前版本为 `0.3.0-local`，新增了可选的秀米排版导入分流：使用时会先区分普通账号、VIP 账号和未登录状态，再选择直接导入 HTML 或复制富文本/Word/Markdown 的回退路径。

## 目录

- `SKILL.md`：skill 入口和主工作流。
- `references/`：证据、写作、审核、依赖和秀米导入说明。
- `scripts/pipeline.py`：收料、检查、构建和依赖诊断脚本。
- `agents/openai.yaml`：Codex 界面元数据。
- `dependencies.lock.json`：本地依赖来源和指纹记录。
- `BUNDLE-MANIFEST.json`：本压缩包的文件清单和依赖说明。
- `THIRD_PARTY_NOTICES.md`：组合依赖的来源与许可证备注。

## 安装

解压后，将其中的 `paper-weaver-zh/` 文件夹复制到 Codex 的 skills 目录：

```text
<CODEX_HOME>/skills/paper-weaver-zh/
```

如果已存在同名目录，请先备份用户自己的修改，再合并或替换对应文件。这个压缩包不会自动安装依赖，也不会创建 GitHub 仓库。

## 依赖与检查

此 skill 是组合层，不把上游 skills 打包进来。首次使用前运行：

```text
python scripts/pipeline.py doctor --skills-root <CODEX_HOME>/skills
```

需要的能力包括 `ReoNa-paper-digest`、`note-organizing`、`article-writing`、`humanizer-zh` 和 `reona-paper-digest-zh`。路径由 `doctor` 实际查找，不应把本机绝对路径写进项目配置。

本地测试：

```text
python -m unittest discover -s scripts/tests -v
```

## 秀米导入

只有用户明确选择秀米时才走该分支：

- VIP 账号：登录秀米后，可尝试“更多 → 导入 HTML 代码”，上传生成的 `dist/xiumi-import.html`，预览并确认标题、图注、段落间距和图片加载后保存草稿。
- 普通账号：不假定能看到 HTML 导入入口，改用富文本复制、Word/Markdown/公众号文章导入或秀米原生组件手动排版。
- 账号未知或未登录：先生成本地可复制版本，询问账号状态，不索要密码或验证码。

秀米可能清洗复杂 CSS，也可能清除 `data:image/...` 图片源；本地生成 HTML 不等于秀米草稿已保存。公开发布、同步公众号和群发均需另行操作。

## 许可证

本地组合 skill 的整体许可证尚未在本包中擅自指定。上游依赖的观察到的许可证和归属见 `THIRD_PARTY_NOTICES.md`。公开发布前，请作者确认组合层和新增文档的许可证选择。

