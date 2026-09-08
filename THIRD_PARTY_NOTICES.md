# 来源、修改与许可证

本分支是组合与本地修订，不宣称第三方项目为原创。根 `LICENSE` 保留 ReoNa 的 MIT 原文；新组合层与本分支新增代码按 MIT 提供，第三方文件继续遵循各自声明。

| 来源 | 本包位置 | 版本依据与处理 |
|---|---|---|
| [ReoNa0216/ReoNa-paper-digest](https://github.com/ReoNa0216/ReoNa-paper-digest) | 根目录工具链 | 2026-09-08 核对 HEAD 为 `1062cb0496abadcc018f0025fe9522632c168c96`；实际随包为用户修改后的 0.8.0，不声称该提交可重现全部本地文件。原作者署名和 MIT 许可证保留 |
| [Jachinx-ai/writter-skills](https://github.com/Jachinx-ai/writter-skills/tree/ace9fc4347659c1ff8528f5bbd570b5c69e3b733) | `skills/article-writing`、`skills/note-organizing` | 来自提交 `ace9fc4347659c1ff8528f5bbd570b5c69e3b733`，分别为 2.0.0 / 1.1.0。两者 README 与 SKILL 原样保留；SKILL 声明作者 Hermes Agent、`license: MIT`。该提交根目录未提供独立 LICENSE 文件，不虚构额外版权年份或权利人 |
| [ai-zixun/humanizer-zh](https://github.com/ai-zixun/humanizer-zh) | `skills/humanizer-zh` | 本机适配版，已观察上游提交 `f75f1ac9735c4f10da1bba0148e0ea7228c5c3b3` 仅作来源线索；不等于本地文件版本。保留 Copyright (c) 2026 aizixun 和 [原 MIT 许可证](skills/humanizer-zh/LICENSE)。语言示例及链接中的作品归其各自作者 |
| 本地 reona-paper-digest-zh 组合层 | `skills/reona-paper-digest-zh` | 保留原作者/许可证元数据和页面生成器；本次仅补充 fork 目录下的上游路径说明 |
| 本地 paper-weaver-zh 组合层 | `skills/paper-weaver-zh` | 由 0.1.0-local 打包为 0.1.1-fork，新增仓库路径解析、相应测试和最终审核指纹顺序说明 |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | `docs/paper-weaver.html` 及图源、预览图 | 使用本地下载的 `2.17.0-dev.1` 包生成，未固定远程提交。HTML 含 Archify 运行时代码；附 [Archify MIT](licenses/Archify-MIT.txt)，保留 tt-a1i 与 Cocoon AI 署名。未随包复制完整 Archify 工具链 |

ReoNa 已内置的 MathJax（Apache-2.0）与 Mermaid（MIT）继续归各自作者，vendored 文件保持不变。本包另附 [MathJax Apache-2.0](licenses/MathJax-Apache-2.0.txt)（取自官方 3.2.2）与 [Mermaid MIT](licenses/Mermaid-MIT.txt)（取自官方 develop，2026-09-08）；后者是许可证来源，不用于推断内置 Mermaid 的精确版本。本包不会用一个统一作者名覆盖这些来源。

## 实际改动如何追溯

`BUNDLE-MANIFEST.json` 记录包内每个其他文件的 SHA-256、字节数、来源类别，以及可用时的源文件摘要/上游 Git blob SHA。manifest 不包含开发机用户名或绝对路径。`skills/paper-weaver-zh/dependencies.lock.json` 记录组合层运行时用到的关键文件指纹；其含义是差异检测，不是包管理器、自动更新器或科学真实性证明。

对既有 skill 的科研场景限制集中放在 paper-weaver 的 integration 规则中，没有改写 article-writing / note-organizing 的原始内容，也没有将人文写作偏好提升为科研事实规则。
