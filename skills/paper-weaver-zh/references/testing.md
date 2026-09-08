# 本地测试与迭代

修改脚本或依赖后读取。使用隔离的测试目录，不重写已有专栏文章；不为测试调用付费图像生成、上传微信或创建仓库。

```text
python -m unittest discover -s SKILL/scripts/tests -v
python SKILL/scripts/pipeline.py doctor
python SKILL/scripts/pipeline.py check ARTICLE
python SKILL/scripts/pipeline.py build ARTICLE --screenshot
```

依赖不在默认 skills 目录时给 doctor/init/build 添加一个或多个 `--skills-root`。Windows 中文终端按需设置 `PYTHONUTF8=1` 和 `PYTHONIOENCODING=utf-8`；环境组合与浏览器位置由本机运行时决定，不硬编码开发机路径。

验收分层：

1. 单元测试：Prompt/Response、You/ChatGPT、中文角色与代码围栏；无角色输入明确报错；多个来源 ID 和补充材料归属；官方导出当前分支；审核摘要失效、错误引用和未核实事实拦截。
2. 真实输入收料：用用户提供的导出文件检查轮次与角色，人工抽查首尾，不把成功解析等同于正确理解。
3. 本地构建：隔离稿执行渲染与双页同步，验证字体、强调、科学上标、图片，以及富文本复制/降级分支。无封面测试不得出现坏图占位。
4. 行为验收：真实论文与讨论形成中心问题、证据账本、三阶段草稿和最终页，人工审查是否通顺且不越界。确定性测试不能替代这一项；只做短例时标明未完成长文全流程验收。

测试失败先修复可复现的问题，再重跑相关案例。新增规则应对应实际故障，不把某篇稿件的措辞或结构写成全局硬约束。测试报告保留在开发/测试工作目录，不把测试 PDF、用户对话、截图和生成文章安装进 skill。
