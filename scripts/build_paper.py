# -*- coding: utf-8 -*-
"""
错题重做卷生成脚本（纯文字，不生成任何图片）。

用法：
    python3 build_paper.py --data problems.json --out 错题重做卷.html

JSON 结构见 examples/sample_problems.json。
"""
import argparse, json, os, sys


CSS = """
@page { size: A4; margin: 16mm 14mm; }
* { box-sizing: border-box; }
body { font-family: "SimSun","宋体","Songti SC",serif; color:#1a1a1a;
       line-height:1.85; font-size:15px; margin:0; padding:10px 22px; }
h1 { text-align:center; font-size:21px; margin:4px 0 2px; letter-spacing:1px; }
.sub { text-align:center; font-size:13px; color:#666; margin-bottom:10px; }
.meta { display:flex; justify-content:space-between; flex-wrap:wrap; gap:6px;
        font-size:14px; margin:8px 2px 16px; border-bottom:1px solid #999; padding-bottom:6px; }
.ws { font-size:16px; font-weight:bold; margin:20px 0 4px;
      border-left:5px solid #c0392b; padding-left:8px; }
.item { margin:12px 0; }
.q { margin:4px 0; }
.blank { display:inline-block; min-width:46px; border-bottom:1px solid #1a1a1a;
         text-align:center; }
.key { margin-top:34px; padding-top:14px; border-top:2px dashed #999; }
.key h2 { text-align:center; color:#b00; font-size:17px; margin:0 0 12px; }
.ki { margin:6px 0; }
.ki b { color:#b00; }
.foot { margin-top:20px; font-size:12.5px; color:#666; border:1px solid #ccc;
        padding:10px 12px; background:#fafafa; }
@media print { .foot{background:#fff;} body{padding:0;} }
"""


def build(data, out_path):
    title = data.get("title", "错题重做卷")
    subtitle = data.get("subtitle", "")
    meta_labels = data.get("meta_labels", ["班级", "姓名", "学号", "得分"])
    items = data.get("items", [])
    answers = data.get("answers", [])
    notes = data.get("notes", [])

    h = ["<!DOCTYPE html><html lang='zh-CN'><head><meta charset='UTF-8'>",
         "<title>%s</title><style>%s</style></head><body>" % (title, CSS)]
    h.append("<h1>%s</h1>" % title)
    if subtitle:
        h.append("<div class='sub'>%s</div>" % subtitle)

    meta = "".join("<span>%s：__________</span>" % m for m in meta_labels)
    h.append("<div class='meta'>%s</div>" % meta)

    last_ws = None
    for it in items:
        ws = it.get("ws", "")
        num = it.get("num", "")
        q = it.get("q", "")
        if ws and ws != last_ws:
            h.append("<div class='ws'>%s</div>" % ws)
            last_ws = ws
        h.append("<div class='item'><div class='q'>%s. %s</div></div>" % (num, q))

    if answers:
        h.append("<div class='key'><h2>— 订正答案（家长留存 / 可遮挡）—</h2>")
        for a in answers:
            h.append("<div class='ki'><b>%s</b></div>" % a)
        h.append("</div>")

    if notes:
        foot = "<div class='foot'><b>整理说明：</b><br>" + \
               "<br>".join("· " + n for n in notes) + "</div>"
        h.append(foot)

    h.append("</body></html>")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(h))
    size = os.path.getsize(out_path)
    # 安全自检：确认没有任何图片被写进去
    img = 1 if ("<img" in "".join(h) or "<svg" in "".join(h) or "data:image" in "".join(h)) else 0
    print("written:", out_path, "size:", size, "图片残留:", img)
    if img:
        print("⚠️ 警告：检测到图片标签，违反'不生成图片'规则！", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="题目数据 JSON 路径")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    args = ap.parse_args()
    with open(args.data, encoding="utf-8") as f:
        data = json.load(f)
    build(data, args.out)


if __name__ == "__main__":
    main()
