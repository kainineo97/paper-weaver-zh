# 上传到自己的 fork 分支

此包是可以叠放到 ReoNa-paper-digest 仓库根目录的文件树，不含 `.git` 历史，不是已经创建的远端 branch。上游核对基线为 `1062cb0496abadcc018f0025fe9522632c168c96`。如果你的目标分支已有其他修改，先比较差异，尤其是 README、根 SKILL、render、publish-check 和主题文件；不要盲目覆盖。

## GitHub 网页上传

1. 在你自己的 ReoNa-paper-digest fork 中创建或切换到目标分支，例如 `codex/paper-weaver-zh`。
2. 解压交付的 ZIP。展开后应直接看到 `README.md`、`SKILL.md`、`scripts/`、`skills/` 和 `docs/`，不要再嵌套一层 repository 目录。
3. 在目标分支根目录选择 **Add file → Upload files**，将上述根层文件及文件夹上传。隐藏的 `.gitignore` 也需要上传；使用 GitHub Desktop 更容易完整保留点文件。
4. 检查提交目标是你的 fork 和预期 branch，查看变更后提交。可使用提交说明 `Add Paper Weaver scientific writing workflow and bundled skills`。
5. 确认根 README 显示流程图，`skills/paper-weaver-zh/SKILL.md` 可访问。交互图在 GitHub 文件页显示源码/下载入口是正常现象，下载 HTML 后打开即可交互。

GitHub 网页每批最多上传 100 个文件、单文件不超过 25 MiB；本包的文件数量与最大文件大小记在验证记录中。网页上传不会自动解压 ZIP，所以只上传压缩包本身并不能形成可运行的仓库结构。[GitHub 文件上传说明](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)

## 已经克隆到本地

在你的 fork 克隆目录确认工作区没有未处理的修改，然后创建分支：

```bash
git status --short
git switch -c codex/paper-weaver-zh
```

把解压出的文件树合并到该克隆目录，保留 `.git` 和包外原有文件。先用 `git diff` 审阅；如果存在同名用户修改，逐文件合并。确认后仅暂存本包涉及的路径，再提交和推送。例如全新 fork 可使用：

```bash
git add README.md SKILL.md LICENSE requirements.txt .gitignore references scripts tests skills docs licenses THIRD_PARTY_NOTICES.md BUNDLE-MANIFEST.json
git diff --cached --stat
git commit -m "Add Paper Weaver scientific writing workflow and bundled skills"
git push -u origin codex/paper-weaver-zh
```

以上命令供你在确认后的目标仓库中执行，本次打包没有运行它们。

## 可选的网页托管

如果今后希望交互图有在线网址，可另行将 `docs/paper-weaver.html` 配置到静态托管服务或 GitHub Pages。此包没有自动部署配置，也没有预填你的用户名、fork 地址或 Pages URL；启用托管前自行确认仓库公开范围及所发布文件。
