---
tags:
  - investigation
  - clues-dsl
cssclasses:
  - graphviz-large-preview
---

# 阿拉拉

> [!NOTE] 寫法
> 只需維護下方 ```clues 區塊，執行 `python scripts/clues_to_graphviz.py <本檔>` 即重生下方圖。
> - `# 群組`：cluster，`##` 為巢狀。
> - `類型 內容 = 別名 @時點 #狀態`：類型可用 證據／事件／實體／假設／未決／矛盾；別名、時點、狀態皆可省略。
> - `A -支持-> B | C`：關係可用 支持／導致／推導／矛盾／時序／屬於，省略即為「關係未定」的灰虛線。
> - 填色與形狀＝類型；邊框粗細與虛實＝狀態（已確認／預定／推論／補丁）。

```clues
標題: 阿拉拉
// 由 draw.io SVG 匯出；未分類 = 原圖非圖例顏色，請自行改類型

# 阿拉拉
未分類 成為明星推出人魚公主平常唱的歌吸引人魚公主注意，引導她們懷疑長老
未分類 背後有完整團隊
未分類 告訴米迦勒海因茨是舒華澤的人，且知道舒華澤的人法力沒有共振特性
未分類 警告海因茨人魚公主比米迦勒更危險
未分類 態度不像米迦勒手下
未分類 真正的幕後黑手
未分類 可能知道人魚公主的秘密
未分類 認為人魚公主危險是不尋常的想法
未分類 使監視者對海因茨懷疑加深

## 南極埋伏
未分類 在神殿出口埋伏
未分類 米迦勒料到人魚公主會到神殿調查並從海底的隱藏出口離開
未分類 自行前往埋伏，引導人魚公主懷疑己方存在叛徒
未分類 米迦勒不知道神殿的存在
未分類 米迦勒故意引導人魚公主調查，好趁人魚公主落單時捉走
未分類 知道神殿構造、不受米迦勒指揮


成為明星推出人魚公主平常唱的歌吸引人魚公主注意，引導她們懷疑長老 -> 背後有完整團隊
自行前往埋伏，引導人魚公主懷疑己方存在叛徒 -> 知道神殿構造、不受米迦勒指揮
在神殿出口埋伏 -> 米迦勒料到人魚公主會到神殿調查並從海底的隱藏出口離開
在神殿出口埋伏 -> 自行前往埋伏，引導人魚公主懷疑己方存在叛徒
米迦勒不知道神殿的存在 -> 自行前往埋伏，引導人魚公主懷疑己方存在叛徒
米迦勒料到人魚公主會到神殿調查並從海底的隱藏出口離開 -> 米迦勒故意引導人魚公主調查，好趁人魚公主落單時捉走
警告海因茨人魚公主比米迦勒更危險 -> 態度不像米迦勒手下
警告海因茨人魚公主比米迦勒更危險 -> 認為人魚公主危險是不尋常的想法
態度不像米迦勒手下 -> 真正的幕後黑手
認為人魚公主危險是不尋常的想法 -> 可能知道人魚公主的秘密
知道神殿構造、不受米迦勒指揮 -> 真正的幕後黑手
// 原圖連線中另有 289 條因端點缺失或不在本子集而未匯出
```

```dot
// clues-auto 由上方 clues 區塊生成，請勿手改；重新執行 scripts/clues_to_graphviz.py
digraph clues {
  graph [
    rankdir="TB", bgcolor="#FFFFFF", newrank="true", compound="true",
    splines="spline", nodesep="0.30", ranksep="0.60", pad="0.15",
    fontname="Microsoft JhengHei, Noto Sans CJK TC, PingFang TC, sans-serif", fontsize="16", labelloc="t",
    label="阿拉拉"
  ];
  node [fontname="Microsoft JhengHei, Noto Sans CJK TC, PingFang TC, sans-serif", fontsize="9", fontcolor="#1F2937", margin="0.10,0.06"];
  edge [fontname="Microsoft JhengHei, Noto Sans CJK TC, PingFang TC, sans-serif", fontsize="8", fontcolor="#475569", arrowsize="0.65"];

  subgraph cluster_00 {
    label="阿拉拉"; color="#CBD5E1"; fillcolor="#FAFAFA";
    fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
    n001 [label="成為明星推出人魚公主平常唱的\n歌吸引人魚公主注意，引導她們\n懷疑長老", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    n002 [label="背後有完整團隊", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    n003 [label="告訴米迦勒海因茨是舒華澤的人\n，且知道舒華澤的人法力沒有共\n振特性", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    n004 [label="警告海因茨人魚公主比米迦勒更\n危險", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    n005 [label="態度不像米迦勒手下", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    n006 [label="真正的幕後黑手", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    n007 [label="可能知道人魚公主的秘密", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    n008 [label="認為人魚公主危險是不尋常的想\n法", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    n009 [label="使監視者對海因茨懷疑加深", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    subgraph cluster_01 {
      label="南極埋伏"; color="#CBD5E1"; fillcolor="#FAFAFA";
      fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
      n010 [label="在神殿出口埋伏", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
      n011 [label="米迦勒料到人魚公主會到神殿調\n查並從海底的隱藏出口離開", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
      n012 [label="自行前往埋伏，引導人魚公主懷\n疑己方存在叛徒", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
      n013 [label="米迦勒不知道神殿的存在", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
      n014 [label="米迦勒故意引導人魚公主調查，\n好趁人魚公主落單時捉走", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
      n015 [label="知道神殿構造、不受米迦勒指揮", shape="box", style="filled,dashed", fillcolor="#FFFFFF", color="#94A3B8", penwidth="1.2"];
    }
  }

  n001 -> n002 [color="#94A3B8", style="dashed"];
  n012 -> n015 [color="#94A3B8", style="dashed"];
  n010 -> n011 [color="#94A3B8", style="dashed"];
  n010 -> n012 [color="#94A3B8", style="dashed"];
  n013 -> n012 [color="#94A3B8", style="dashed"];
  n011 -> n014 [color="#94A3B8", style="dashed"];
  n004 -> n005 [color="#94A3B8", style="dashed"];
  n004 -> n008 [color="#94A3B8", style="dashed"];
  n005 -> n006 [color="#94A3B8", style="dashed"];
  n008 -> n007 [color="#94A3B8", style="dashed"];
  n015 -> n006 [color="#94A3B8", style="dashed"];
}
```
