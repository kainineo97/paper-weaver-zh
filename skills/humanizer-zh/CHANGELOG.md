# Changelog

All notable changes to this skill are recorded here.

This repository follows Semantic Versioning. The current released
version is stored in `VERSION`.

## [1.3.0] - 2026-05-18

Add optional author-voice adoption for deep rewrites.

### Added

- 8 opt-in author voice profiles under [references/voices/](./references/voices/),
  each capturing a distinct Chinese writing voice (persona, sentence templates,
  rhythm rules, anti-patterns): 李笑来, 鹤老师, 罗振宇, 吴军, 李尚龙, 何帆, 冯唐, 刘子超.
- [references/voices/index.md](./references/voices/index.md) — one-line catalog
  used by the new opt-in step in `SKILL.md`.
- New `## Voice Adoption (可选)` section in [SKILL.md](./SKILL.md): when a
  deep-rewrite request appears for the first time in a session, the skill may
  ask once whether to channel one of the eight voices. Silent otherwise.

### Changed

- `## Deep Review` and `## Final Check` in `SKILL.md` now reference the active
  voice profile (if any) and treat it as authoritative on conflicts with the
  generic Core Rules (e.g. permitted long em dashes for 李笑来 / 刘子超).
- Default neutral behavior is unchanged when no voice is selected.

## [1.2.0] - 2026-05-18

Add three new AI-essay anti-patterns covering macro-level rhythm
problems, plus a predictability soundcheck in the final review pass.

### Added

- [references/patterns.md](./references/patterns.md) §11 编号枚举撑全文 —
  body-text 第一/第二/第三 used as a recurring article-level rhythm, with
  time/causal/scene replacement strategies. Distinct from §5, which covers
  explicit bullet lists.
- [references/patterns.md](./references/patterns.md) §12 章末段末的预告式收束 —
  forward hooks like `接下来要…` / `下一步是…` that turn every section ending
  into a preview of the next, with open-question / cold-conclusion /
  scene-closure / reverse-limitation replacements. Distinct from §4, which
  covers sloganized endings.
- [references/patterns.md](./references/patterns.md) §13 抽象转义与重锤句 —
  abstract hammer phrases like `本质上` / `这件事` / `真正重要的是` /
  `归根结底` / `回到最初的那个问题`, with concrete-mechanism replacements.
- [references/patterns.md](./references/patterns.md) §10 now names the
  default AI essay shape (定义 → 拆项 → 拔高) as the macro template the six
  rewrite paths are meant to break.
- [SKILL.md](./SKILL.md) Final Check now includes a predictability
  soundcheck against the 定义 → 拆项 → 拔高 default rhythm.

## [1.1.0] - 2026-05-18

Adopt the [skills.sh](https://www.skills.sh) release and distribution model.

### Added

- One-line install via the `skills` CLI: `npx skills add ai-zixun/humanizer-zh`
  (auto-detects Codex, Claude Code, OpenClaw, and 50+ other agents).
- [.claude-plugin/plugin.json](./.claude-plugin/plugin.json) for Claude Code
  plugin marketplace compatibility.
- [.github/workflows/release.yml](./.github/workflows/release.yml) that
  auto-tags `v<version>` and creates a GitHub Release whenever `VERSION`
  changes, with the matching changelog section as the release body.
- skills.sh leaderboard badge in `README.md` and `README.en.md`.

### Changed

- README install instructions replaced with the `npx skills add` recipe.
  Per-agent `git clone` steps removed.
- Compatibility tables now document the CLI's install paths for each agent
  instead of manual `mkdir` / `git clone` commands.

## [1.0.0] - 2026-03-15

Initial stable release.

### Added

- Core rewrite guidance in [SKILL.md](./SKILL.md) for reducing
  translation-like phrasing, empty big words, rigid paragraph rhythm,
  and article-level structure problems.
- Deep diagnostic patterns in
  [references/patterns.md](./references/patterns.md), including
  article-structure checks and rewrite paths for long-form prose.
- Chinese-native reference material in
  [references/corpus.md](./references/corpus.md) and
  [references/corpus-quickpick.md](./references/corpus-quickpick.md).
- Codex display metadata in
  [agents/openai.yaml](./agents/openai.yaml).
