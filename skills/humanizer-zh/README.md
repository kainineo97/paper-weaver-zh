# humanizer-zh

[![skills.sh](https://skills.sh/b/ai-zixun/humanizer-zh)](https://skills.sh/ai-zixun/humanizer-zh)

[中文](./README.md) | [English](./README.en.md)

`humanizer-zh` 是一个兼容 Codex、Claude Code 和 OpenClaw 的中文去 AI 味技能。它用于重写、润色或审阅中文博客、评论、产品分析、newsletter、书稿章节等长文本，让文字更像中文母语者写出来的，而不是翻译腔、模型拼接稿或营销通稿。

这个仓库采用「单目录即技能包」结构：仓库根目录本身就是技能目录，通过 [skills.sh](https://www.skills.sh) 生态的 `npx skills` 命令行一键安装到各类代理。

当前版本：`1.3.0`

## 适用场景

- 中文博客、专栏、社论、评论稿的去 AI 味改写
- 中文产品分析、行业观察、长邮件、newsletter 的自然化润色
- 中译中修订，重点清理翻译腔、机械对照句、空泛大词和口号式收束
- 需要解释「这段中文为什么像 AI 写的」并给出修改前后示例

## 能力范围

- 识别并改写翻译腔、结构腔、排版腔和判断腔
- 识别并校正文级结构问题，检查开头、主体、结尾是否服务同一条主线
- 统一中文引号、日期、英文术语大小写与排版细节
- 根据文本类型调整改写力度，避免把说明文硬改成抒情文
- 深度改写时按需读取 `references/patterns.md`，解释常见问题模式
- 快速选择中文参照时，先读 `references/corpus-quickpick.md`
- 需要找中文母语参照时，按需读取 `references/corpus.md`
- 可选：在深度改写时套用 8 位中文作者的声音（李笑来 / 鹤老师 / 罗振宇 / 吴军 / 李尚龙 / 何帆 / 冯唐 / 刘子超），按需读取 `references/voices/`
- 默认引号样式为全角双引号 `""`，项目可在 `CLAUDE.md`/`AGENTS.md` 里声明改用 `「」`

## 兼容性

`npx skills add` 会自动识别本机安装的代理，并把同一份 `SKILL.md` 放到对应的 skills 目录。以下三个是本仓库重点测试过的运行环境，完整支持列表见 [skills CLI 文档](https://github.com/vercel-labs/skills#supported-agents)。

| 平台 | 状态 | CLI 安装路径 |
| --- | --- | --- |
| Codex | 支持 | 项目：`.agents/skills/humanizer-zh/`；个人：`~/.codex/skills/humanizer-zh/` |
| Claude Code | 支持 | 项目：`.claude/skills/humanizer-zh/`；个人：`~/.claude/skills/humanizer-zh/` |
| OpenClaw | 支持 | 项目：`skills/humanizer-zh/`；个人：`~/.openclaw/skills/humanizer-zh/` |

真正决定技能行为的是 `SKILL.md` 与它引用的 `references/` 文件，不是 README。README 会随 `npx skills add` 一并复制到本地技能目录，但代理在触发时只读 `SKILL.md` 及其引用的 `references/` 文件，不会把 README 当成上下文。

## 仓库结构

```text
humanizer-zh/
├── .claude-plugin/
│   └── plugin.json
├── .github/
│   └── workflows/
│       └── release.yml
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── SKILL.md
├── README.md
├── README.en.md
├── VERSION
├── agents/
│   └── openai.yaml
└── references/
    ├── corpus-quickpick.md
    ├── corpus.md
    ├── patterns.md
    └── voices/
        ├── index.md
        ├── lixiaolai.md
        ├── helaoshi.md
        ├── luozhenyu.md
        ├── wujun.md
        ├── lishanglong.md
        ├── hefan.md
        ├── fengtang.md
        └── liuzichao.md
```

## 安装

通过 [skills.sh](https://www.skills.sh) 生态的 `skills` CLI 一键安装：

```bash
# 项目技能：随项目仓库一起提交，团队共享
npx skills add ai-zixun/humanizer-zh

# 个人技能：在你所有项目里可用
npx skills add ai-zixun/humanizer-zh -g
```

CLI 会自动检测本机的 Codex/Claude Code/OpenClaw 等代理，并把技能装到对应的 skills 目录。也可以用 `-a` 指定只装到某些代理，例如 `npx skills add ai-zixun/humanizer-zh -a claude-code`。详细选项见 [skills CLI 文档](https://github.com/vercel-labs/skills#readme)。

## 版本管理

- 仓库使用 Semantic Versioning。
- 当前版本号只放在 [VERSION](./VERSION)。
- 版本变更记录放在 [CHANGELOG.md](./CHANGELOG.md)。
- 发布新版本时，更新 `VERSION` 与 `CHANGELOG.md` 并推到 `main`；`.github/workflows/release.yml` 会自动打 `v<version>` tag 并生成 GitHub Release。

示例：

```bash
printf '1.1.1\n' > VERSION
# 在 CHANGELOG.md 顶部追加 [1.1.1] 条目
git add VERSION CHANGELOG.md
git commit -m "[release] 1.1.1"
git push origin main
```

## 使用方式

不同代理的触发方式略有区别，但运行入口都是同一份 `SKILL.md`。

### Codex

可以显式提到技能名：

```text
请用 $humanizer-zh 把这段中文改得更像中文母语者写的，减少翻译腔和空泛大词。
```

### Claude Code

Claude Code 的 Skills 以自动匹配为主，通常直接描述需求即可：

```text
把这篇中文稿子润色成更自然的母语表达，重点去掉翻译腔、机械排比和过火结论。
```

### OpenClaw

OpenClaw 既可以自动匹配，也可能把技能暴露为用户可调用命令，具体取决于本地配置：

```text
Use humanizer-zh to rewrite this Chinese draft so it reads like native Chinese writing.
```

## 运行时布局

- `SKILL.md` 是运行时入口，包含触发描述、工作流和输出约定
- `agents/openai.yaml` 只提供 Codex 的展示元数据，不影响 Claude Code 或 OpenClaw
- `VERSION` 是仓库唯一版本源
- `CHANGELOG.md` 记录已发布版本的变化
- `references/corpus-quickpick.md` 是运行时速查表，先帮模型缩小参照范围
- `references/patterns.md` 是按需加载的深度参考，不会在每次触发时都占用上下文
- `references/corpus.md` 是按文体选参照的语料索引，不是固定模仿模板
- `references/voices/` 收录 8 位中文作者的声音档案，默认不加载；只有当用户在深度改写时主动选择某位作者后，才会加载对应文件

## 设计约束

- frontmatter 只依赖通用字段 `name` 和 `description`，避免把代理私有配置写进运行入口
- 技能名使用小写连字符 `humanizer-zh`，便于兼容多代理的命名与路径约定
- 所有资源都通过相对路径组织，整个目录可以被直接复制或 symlink 到任意 skills 根目录

## 致谢

这个技能的整体方向与分享方式受到 [blader/humanizer](https://github.com/blader/humanizer) 的启发。原仓库把英文文本去 AI 味整理成可复用的 Claude Code skill；`humanizer-zh` 在这个思路上扩展到中文场景，重点处理翻译腔、中文节奏、标点排版和长篇非虚构写作中的机械表达。

## 许可证

本仓库采用 [MIT License](./LICENSE)。
