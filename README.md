# cuotiji-redo-paper（错题重做卷生成器）

> A WorkBuddy / Codex skill that turns a scanned homework PDF (with handwritten
> teacher corrections) into a clean, printable "wrong-question redo sheet" (错题重做卷).

把一份带**手写订正**的作业 / 试卷扫描 PDF，整理成一张干净的、可打印的**错题重做卷** HTML：
孩子重做，家长对照答案。

## 为什么需要它

小学家长常遇到这种情况：孩子带回一本订正过的作业，老师用红笔在旁边写了"订 / 订正"。
想把这些**真正做错、被订正过的题**挑出来，单独做成一张练习卷给孩子重做。

难点在于：
- 扫描件经 OCR 识别**抓不到手写红笔"订"**，纯文字会大量漏题。
- 直接裁原卷图会带上孩子的手写和红笔，不干净。
- 自己用 SVG 重绘图，又"跟原卷不太一样"。

这个 skill 的套路（经过反复验证）：
1. `pdftoppm` 把 PDF 每页渲染成 PNG；
2. 逐页用**视觉模型**看红笔"订 / 订正"标记（OCR 不可靠，必须看图）；
3. 只收录**有明确红笔订正**或**算式明显必错**的题，排除只是打勾 ✓ 的；
4. **纯文字**呈现，原卷带配图的题用文字把数据 / 关系描述清楚——**绝不生成任何图片**；
5. 按原卷顺序输出，底部附"订正答案（家长留存 / 可遮挡）"区；
6. 生成 HTML，浏览器直接 ⌘+P 打印，不导出 PDF。

## 安装

把本目录放到你的 skills 目录下即可（需支持 Skill 的 agent，如 WorkBuddy / Codex）：

```bash
# WorkBuddy
cp -r cuotiji-redo-paper ~/.workbuddy/skills/

# 或 Codex
cp -r cuotiji-redo-paper ~/.codex/skills/
```

重启会话后，当对话里出现"整理错题 / 把订正的题做成练习卷 / 错题重做卷"等意图时，skill 会被自动触发。

## 用法

直接对 agent 说，例如：

> 整理错题：把这份 PDF 里老师红笔订正的题，做成一张可打印的错题重做卷。

agent 会走完上面"工作流"，最终给你一份 HTML 预览。

如果你想**只改题项、重新生成**（不必让 agent 重新识别 PDF），可以手动跑自带脚本：

```bash
python3 scripts/build_paper.py \
  --data examples/sample_problems.json \
  --out 错题重做卷.html
```

数据格式见 `examples/sample_problems.json`：一个 `{ "title": "...", "source": "...", "problems": [ ... ] }` 结构，
每道题含 `section`（分节名）、`q`（题干 HTML，可用 `<span class="blank"></span>` 表示填空）、
`answer`（订正答案）、`note`（可选说明）、`confidence`（`sure` / `doubt`）。

## 目录结构

```
cuotiji-redo-paper/
├── SKILL.md                    # skill 定义与工作流（核心）
├── README.md                   # 本文件
├── scripts/
│   └── build_paper.py          # 读 JSON → 生成可打印 HTML
└── examples/
    └── sample_problems.json    # 数据格式示例
```

## 必须遵守的硬规则（踩坑经验）

1. **OCR 不可靠，必须逐页看图**找红笔"订 / 订正"，否则大量漏题。
2. **绝不生成任何图片**——不裁原卷截图、不用 SVG 重绘，有图题一律纯文字描述。
3. 按原卷顺序、保留原貌（题号、分节名都不动）。
4. 不导出 PDF，浏览器直接打印。
5. 存疑题（无明确"订"字、或原卷答案与解析矛盾）标"**疑·请家长核对**"，不擅自判定。

## License

[MIT](./LICENSE) © CarbonJ
