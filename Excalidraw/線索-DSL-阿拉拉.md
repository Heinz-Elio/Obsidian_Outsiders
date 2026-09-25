---
tags:
  - investigation
  - clues-dsl
cssclasses:
  - graphviz-large-preview
---

# 阿拉拉

> [!NOTE] 寫法見 [[線索-DSL-寫法]]。圖上只顯示短鍵，細節在 Canvas 卡片裡。
> 結構：「事件／假設」依連線流向推導；群組內用 -支持/推導-> 串起推論。

```clues
標題: 阿拉拉

# 阿拉拉
假設 以明星身份推歌吸引注意 : 成為明星推出人魚公主平常唱的歌吸引人魚公主注意，引導她們懷疑長老
假設 背後有完整團隊
事件 告知米迦勒海因茨為舒華澤人 : 告訴米迦勒海因茨是舒華澤的人，且知道舒華澤的人法力沒有共振特性
事件 警告海因茨人魚比米迦勒更危險 : 警告海因茨人魚公主比米迦勒更危險
假設 態度不像米迦勒手下
假設 真正的幕後黑手
假設 可能知道人魚公主秘密 : 可能知道人魚公主的秘密
假設 視人魚為危險屬異常想法 : 認為人魚公主危險是不尋常的想法
假設 加深監視者對海因茨懷疑 : 使監視者對海因茨懷疑加深

## 南極埋伏
事件 在神殿出口埋伏
假設 米迦勒預料神殿出口離開 : 米迦勒料到人魚公主會到神殿調查並從海底的隱藏出口離開
假設 自行埋伏引導懷疑叛徒 : 自行前往埋伏，引導人魚公主懷疑己方存在叛徒
假設 米迦勒不知神殿存在 : 米迦勒不知道神殿的存在
假設 米迦勒故意引導以便捉走 : 米迦勒故意引導人魚公主調查，好趁人魚公主落單時捉走
假設 知神殿構造不受米迦勒指揮 : 知道神殿構造、不受米迦勒指揮


以明星身份推歌吸引注意 -> 背後有完整團隊
自行埋伏引導懷疑叛徒 -> 知神殿構造不受米迦勒指揮
在神殿出口埋伏 -> 米迦勒預料神殿出口離開
在神殿出口埋伏 -> 自行埋伏引導懷疑叛徒
米迦勒不知神殿存在 -> 自行埋伏引導懷疑叛徒
米迦勒預料神殿出口離開 -> 米迦勒故意引導以便捉走
警告海因茨人魚比米迦勒更危險 -> 態度不像米迦勒手下
警告海因茨人魚比米迦勒更危險 -> 視人魚為危險屬異常想法
態度不像米迦勒手下 -> 真正的幕後黑手
視人魚為危險屬異常想法 -> 可能知道人魚公主秘密
知神殿構造不受米迦勒指揮 -> 真正的幕後黑手
```

```dot
// clues-auto 由上方 clues 區塊生成，請勿手改；重新執行 scripts/clues_to_graphviz.py
// 稽核：第 4 行：推論「以明星身份推歌吸引注意」沒有證據或推論連入
// 稽核：第 6 行：「告知米迦勒海因茨為舒華澤人」沒有任何連線
// 稽核：第 12 行：「加深監視者對海因茨懷疑」沒有任何連線
// 稽核：第 18 行：推論「米迦勒不知神殿存在」沒有證據或推論連入
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
    n001 [label="以明星身份推歌吸引注意", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="成為明星推出人魚公主平常唱的歌吸引人魚公主注意，引導她們懷疑長老"];
    n002 [label="背後有完整團隊", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n003 [label="告知米迦勒海因茨為舒華澤人", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0", tooltip="告訴米迦勒海因茨是舒華澤的人，且知道舒華澤的人法力沒有共振特性"];
    n004 [label="警告海因茨人魚比米迦勒更危險", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0", tooltip="警告海因茨人魚公主比米迦勒更危險"];
    n005 [label="態度不像米迦勒手下", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n006 [label="真正的幕後黑手", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n007 [label="可能知道人魚公主秘密", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="可能知道人魚公主的秘密"];
    n008 [label="視人魚為危險屬異常想法", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="認為人魚公主危險是不尋常的想法"];
    n009 [label="加深監視者對海因茨懷疑", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="使監視者對海因茨懷疑加深"];
    subgraph cluster_01 {
      label="南極埋伏"; color="#CBD5E1"; fillcolor="#FAFAFA";
      fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
      n010 [label="在神殿出口埋伏", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
      n011 [label="米迦勒預料神殿出口離開", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="米迦勒料到人魚公主會到神殿調查並從海底的隱藏出口離開"];
      n012 [label="自行埋伏引導懷疑叛徒", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="自行前往埋伏，引導人魚公主懷疑己方存在叛徒"];
      n013 [label="米迦勒不知神殿存在", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="米迦勒不知道神殿的存在"];
      n014 [label="米迦勒故意引導以便捉走", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="米迦勒故意引導人魚公主調查，好趁人魚公主落單時捉走"];
      n015 [label="知神殿構造不受米迦勒指揮", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2", tooltip="知道神殿構造、不受米迦勒指揮"];
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
