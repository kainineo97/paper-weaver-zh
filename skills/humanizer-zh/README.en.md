# humanizer-zh

[![skills.sh](https://skills.sh/b/ai-zixun/humanizer-zh)](https://skills.sh/ai-zixun/humanizer-zh)

[中文](./README.md) | [English](./README.en.md)

`humanizer-zh` is a Chinese writing cleanup skill for Codex, Claude Code, and OpenClaw. It rewrites AI-sounding, translated, or overly mechanical Chinese prose so it reads like native Chinese writing instead of a stitched-together model draft.

This repository uses a single-directory skill layout: the repository root is the skill. Install with one command via the [skills.sh](https://www.skills.sh) ecosystem CLI.

Current version: `1.3.0`

## Use Cases

- Humanizing Chinese blog posts, essays, commentary, product analysis, and newsletters
- Removing translation-like phrasing, formulaic contrast frames, and inflated closing lines
- Explaining why a Chinese passage feels AI-written, with before/after examples
- Preserving facts and intent while improving paragraph rhythm and idiomatic phrasing

## Scope

- Detects and rewrites translation artifacts, rigid sentence patterns, and empty big words
- Detects article-level structure problems, including weak intro/conclusion alignment and off-topic body paragraphs
- Normalizes punctuation, dates, English term casing, and mixed Chinese/English typography
- Adjusts rewrite intensity by text type instead of flattening everything into one tone
- Loads `references/corpus-quickpick.md` for a fast genre/style pick
- Loads `references/patterns.md` only when a deeper diagnostic rewrite is needed
- Loads `references/corpus.md` when it needs Chinese-native reference material by genre
- Optional: channel one of 8 Chinese author voices during deep rewrites (李笑来 / 鹤老师 / 罗振宇 / 吴军 / 李尚龙 / 何帆 / 冯唐 / 刘子超), loaded on demand from `references/voices/`
- Defaults to full-width curly double quotes `""`; projects can opt into `「」` via a `CLAUDE.md` / `AGENTS.md` declaration

## Compatibility

`npx skills add` auto-detects the installed agents on your machine and drops the same `SKILL.md` into each one's skills directory. The three agents below are the primary tested targets; the full agent list lives in the [skills CLI docs](https://github.com/vercel-labs/skills#supported-agents).

| Platform | Status | CLI install path |
| --- | --- | --- |
| Codex | Supported | Project: `.agents/skills/humanizer-zh/`; global: `~/.codex/skills/humanizer-zh/` |
| Claude Code | Supported | Project: `.claude/skills/humanizer-zh/`; global: `~/.claude/skills/humanizer-zh/` |
| OpenClaw | Supported | Project: `skills/humanizer-zh/`; global: `~/.openclaw/skills/humanizer-zh/` |

The runtime behavior lives in `SKILL.md` and `references/`, not in this README. The README is copied into the local skill directory by `npx skills add`, but agents only load `SKILL.md` and the files it references at trigger time — the README is not part of the runtime context.

## Repository Layout

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

## Installation

Install via the [skills.sh](https://www.skills.sh) ecosystem CLI:

```bash
# Project skill (committed with your repo, shared with your team)
npx skills add ai-zixun/humanizer-zh

# Personal skill (available across all your projects)
npx skills add ai-zixun/humanizer-zh -g
```

The CLI auto-detects which agents (Codex, Claude Code, OpenClaw, and 50+ others) are installed on your machine and drops the skill into each one's correct path. To scope the install, pass `-a <agent>`, e.g. `npx skills add ai-zixun/humanizer-zh -a claude-code`. Full option list lives in the [skills CLI docs](https://github.com/vercel-labs/skills#readme).

## Versioning

- This repository uses Semantic Versioning.
- The single source of truth for the current version is
  [VERSION](./VERSION).
- Release notes live in [CHANGELOG.md](./CHANGELOG.md).
- To cut a release, bump `VERSION`, prepend a `CHANGELOG.md` entry, and push to `main`. The `.github/workflows/release.yml` workflow tags `v<version>` and creates the matching GitHub Release.

Example:

```bash
printf '1.1.1\n' > VERSION
# Prepend a [1.1.1] entry to CHANGELOG.md
git add VERSION CHANGELOG.md
git commit -m "[release] 1.1.1"
git push origin main
```

## Usage

All three platforms use the same runtime entry point, but discovery differs by agent.

### Codex

You can mention the skill explicitly:

```text
Use $humanizer-zh to rewrite this Chinese draft so it reads like native Chinese writing and loses the translation feel.
```

### Claude Code

Claude Code skills are usually model-invoked, so a direct request is often enough:

```text
Rewrite this Chinese draft so it sounds like native writing. Remove translation-like phrasing, empty big words, and stiff paragraph rhythm.
```

### OpenClaw

OpenClaw can auto-match the skill and may also expose it as a user-invocable command depending on local settings:

```text
Use humanizer-zh to rewrite this Chinese draft so it reads like native Chinese writing.
```

## Runtime Notes

- `SKILL.md` is the runtime entry point
- `agents/openai.yaml` is Codex-specific UI metadata
- `VERSION` is the single source of truth for the repository version
- `CHANGELOG.md` records released changes
- `references/corpus-quickpick.md` is the runtime fast path for picking a reference voice
- `references/patterns.md` is loaded on demand for deeper rewrite and diagnosis work
- `references/corpus.md` is a genre-based reading list for choosing Chinese-native reference voices
- `references/voices/` holds 8 opt-in Chinese author voice profiles; nothing is loaded by default. When a deep rewrite is requested, `SKILL.md` may ask once whether to adopt a voice and only loads the chosen file

## Acknowledgements

This skill is inspired by [blader/humanizer](https://github.com/blader/humanizer), which packaged AI-writing cleanup guidance as a reusable Claude Code skill. `humanizer-zh` extends that idea into Chinese writing, with extra attention to translation artifacts, Chinese paragraph rhythm, punctuation, and long-form nonfiction style.

## License

This repository is licensed under the [MIT License](./LICENSE).
