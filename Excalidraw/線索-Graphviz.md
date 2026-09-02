---
tags:
  - investigation
  - graphviz
  - clues
source: "[[線索-Clues and Investigation.drawio.svg]]"
cssclasses:
  - graphviz-large-preview
---

# 線索與調查（Graphviz）

本圖由 `線索-Clues and Investigation.drawio.svg` 第一頁 `Clues and Investigation` 轉換。

- 依原圖容器保留事件、場地、人物與證物分類。
- 上至下沿用原圖的粗略時序；不把空間位置改寫成精確日期。
- 原圖未置於容器的節點保留在根圖，不擅自分類。
- 專題推理已拆至 [[線索-人魚公主真相與杜溫]]、[[線索-改革派對付保守派策略]]，並在專題筆記中區分原圖、設定與未決內容。
- 原圖連線沒有文字標籤，因此只保留方向、顏色與虛實線，不補寫「支持／矛盾」等語意。
- 本圖有文字節點：330（其中容器 46）；完整連線：224；拆出連線：68；粗略時序帶：8。

## Graphviz 圖

```dot
digraph clues {
  graph [
    rankdir="TB",
    bgcolor="#FFFFFF",
    compound="true",
    newrank="true",
    outputorder="edgesfirst",
    splines="ortho",
    nodesep="0.28",
    ranksep="0.70",
    pad="0.20",
    fontname="Microsoft JhengHei",
    label="線索與調查｜依原圖容器分類，上至下為粗略時序",
    labelloc="t",
    fontsize="20"
  ];

  node [
    fontname="Microsoft JhengHei",
    fontsize="10",
    margin="0.10,0.07"
  ];

  edge [
    fontname="Microsoft JhengHei",
    fontsize="8",
    color="#64748B",
    arrowsize="0.60"
  ];

  subgraph cluster_n001 {
    label="天城理人音樂會現場";
    color="#64748B";
    fillcolor="#E6FFCC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n001 [label="天城理人音樂會現場", shape="box", fillcolor="#E6FFCC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n002 [label="多人監視人魚公主", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n003 [label="保守派監視者", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n004 [label="改革派與保守派矛盾", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n008 [label="彭達拉薩人的存在十分敏感，會激化人魚內部矛盾", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n009 [label="就算不至內戰也會瓦解同盟", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n010 [label="塞雷亞明知而同意合作，且刻意淡化問題", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n011 [label="塞雷亞向VPTS洩密", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
    n012 [label="與北太平洋立場矛盾", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n013 [label="塞雷亞與長老目標不同", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
    n014 [label="北太平洋有意挑起爭端", shape="box", fillcolor="#DAE8FC", color="#6C8EBF", fontcolor="#111827", style="filled,rounded"];
    n015 [label="不利米迦勒復興海之住民", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n016 [label="復興不是米迦勒的真正目的", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n017 [label="長老向VPTS洩密", shape="box", fillcolor="#DAE8FC", color="#6C8EBF", fontcolor="#111827", style="filled,rounded"];
    n018 [label="有利米迦勒綁架人魚公主", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n019 [label="挑起內部爭端", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];

    subgraph cluster_n005 {
      label="尼歌娜";
      color="#64748B";
      fillcolor="#E6E6E622";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n005 [label="尼歌娜", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n006 [label="明明只是基層，卻知道監視者的存在", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n007 [label="暗中保護公主，並防止保守派抓到把柄", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }

  }

  subgraph cluster_n056 {
    label="南極考察點";
    color="#000000";
    fillcolor="#CCFF9922";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n056 [label="南極考察點", shape="box", fillcolor="#CCFF99", color="#000000", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n057 [label="航海日誌", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n058 [label="地圖", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n059 [label="南極一山洞深處的神殿遺跡", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n060 [label="恐懼使人瘋狂", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
    n061 [label="未知語言", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n062 [label="製造出信使實行計劃", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n063 [label="器具、建築設計不適合人型生物使用", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n064 [label="種族因不明原因步向衰落，族人研究復興種族之法", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n065 [label="張睿稱神殿大門處於關閉狀態", shape="box", fillcolor="#FFF2CC", color="#D6B656", fontcolor="#111827", style="filled,rounded"];
    n066 [label="天城博敏中止考察，回到美國完成論文後與化石先\n後下落不明", shape="box", fillcolor="#FFF2CC", color="#D6B656", fontcolor="#111827", style="filled,rounded"];
    n067 [label="傳家寶", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n068 [label="警告石碑", shape="box", fillcolor="#FFF2CC", color="#D6B656", fontcolor="#111827", style="filled,rounded"];
    n069 [label="星降神臨長期收集基質", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n070 [label="以奴隸之DNA進行製造容器實驗", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n071 [label="捨棄肉體保留靈魂，將來轉移至新容器", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n072 [label="信使是鳥人原生樣貌", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n073 [label="米迦勒：將奴隸DNA植入美嘉留產生", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n074 [label="壁畫", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n075 [label="完整化石不足半米高", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n076 [label="信使是王的複製品", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n077 [label="人頭鳥身，其中一隻有光環", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n078 [label="光環是特殊象徵", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n079 [label="美嘉留擁有彭達拉薩血統", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n080 [label="現代人類會對DNA產生排斥", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n081 [label="帶有古代人類血統的人不會排斥DNA，但僅能重\n現人格，且人格無法控制宿主，反而會受美嘉留影\n響", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n082 [label="出現意外，裝置變成怪物", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n083 [label="正本失蹤，副本只有抵達前的部分，抵達後（以未\n知語言寫成）的部分被撕走", shape="box", fillcolor="#FFF2CC", color="#D6B656", fontcolor="#111827", style="filled,rounded"];
    n084 [label="看懂的人想要隱瞞", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
    n085 [label="美嘉留與米迦勒氣息相似", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n086 [label="米迦勒出現時美嘉留衰弱", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n087 [label="大門打開，信使與怪物被喚醒，澤井陽基控制信使\n、天城博敏", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n088 [label="突然出現帶走美嘉留，不久後美嘉留被送回家", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n089 [label="不信邪的船員打開大門，船員與怪物戰鬥，暫時停\n止其行動後脫逃", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n090 [label="澤井陽基解封", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n091 [label="依靠美嘉留的力量顯現", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n092 [label="考察隊離開後有人進入神殿", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n093 [label="大門以人類的力氣無法推開", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n094 [label="米迦勒空間裡的城堡", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n095 [label="米迦勒與鳥人一族有關", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n096 [label="澤井陽基", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n097 [label="在南極考察後失蹤", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n098 [label="官方認定考察成果造假", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n099 [label="海之住民不會自稱海之住民", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n100 [label="米迦勒的自稱是現代人告訴他的", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n101 [label="有人喚醒/復活米迦勒", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n102 [label="使用法術", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n153 {
    label="第一封信件";
    color="#64748B";
    fillcolor="#CCE5FF22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n153 [label="第一封信件", shape="box", fillcolor="#CCE5FF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n154 [label="合照", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];

    subgraph cluster_n155 {
      label="封蠟";
      color="#64748B";
      fillcolor="#CCCCFF22";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n155 [label="封蠟", shape="box", fillcolor="#CCCCFF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n156 [label="與彭達拉薩族徽相似", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n157 [label="美國大眾牌子", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n158 [label="V與彭達拉薩族有關", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }

  }

  subgraph cluster_n159 {
    label="廢棄孤兒院";
    color="#64748B";
    fillcolor="#E6FFCC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n159 [label="廢棄孤兒院", shape="box", fillcolor="#E6FFCC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n176 [label="選擇孤兒院的理由：暗指人魚公主沒有父母，形同\n孤兒", shape="box", fillcolor="#CCCCCC", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n177 [label="29年前發生火災，案件紀錄3人倖存", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];

    subgraph cluster_n160 {
      label="地下室";
      color="#64748B";
      fillcolor="#FFFFCC22";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n160 [label="地下室", shape="box", fillcolor="#FFFFCC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n161 [label="地下室有APCS，導致未能提前發現沙羅", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n165 [label="手套", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];

      subgraph cluster_n162 {
        label="沙羅";
        color="#64748B";
        fillcolor="#E6E6E622";
        fontcolor="#111827";
        fontname="Microsoft JhengHei";
        fontsize="12";
        style="filled,rounded";
        penwidth="1.4";

        n162 [label="沙羅", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
        n163 [label="V前往海都城帶走沙羅", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
        n164 [label="V知道海都城位置", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      }


      subgraph cluster_n166 {
        label="第二封信件";
        color="#64748B";
        fillcolor="#CCE5FF22";
        fontcolor="#111827";
        fontname="Microsoft JhengHei";
        fontsize="12";
        style="filled,rounded";
        penwidth="1.4";

        n166 [label="第二封信件", shape="box", fillcolor="#CCE5FF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
        n167 [label="以阿奎斯托語寫成", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
        n168 [label="V懂得阿奎斯托語", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
        n169 [label="V知道沙羅是前公主", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
        n170 [label="對象為前公主", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
        n171 [label="地址、行李保險箱編號、密碼", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
        n172 [label="4月6日0時0分後至4月7日0時0分前領取", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      }


      subgraph cluster_n173 {
        label="第一張門票";
        color="#64748B";
        fillcolor="#CCE5FF22";
        fontcolor="#111827";
        fontname="Microsoft JhengHei";
        fontsize="12";
        style="filled,rounded";
        penwidth="1.4";

        n173 [label="第一張門票", shape="box", fillcolor="#CCE5FF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
        n174 [label="座標、海拔", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
        n175 [label="時間", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      }

    }


    subgraph cluster_n178 {
      label="Hangman 謎題";
      color="#64748B";
      fillcolor="#CCCCFF22";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n178 [label="Hangman 謎題", shape="box", fillcolor="#CCCCFF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n179 [label="時間", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n180 [label="場景含意", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }

  }

  subgraph cluster_n188 {
    label="南極考察造假事件";
    color="#64748B";
    fillcolor="#FFE6CC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n188 [label="南極考察造假事件", shape="box", fillcolor="#FFE6CC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n196 [label="奧德斯．法哈利", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n197 [label="資料十年未更新，聯繫方式已失效", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n203 [label="斯普魯恩斯為保密盜去化石並用媒體炒作為學術詐\n騙", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n204 [label="考察所得化石確屬海之住民", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n211 [label="法哈利為彭達拉薩人", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n212 [label="神殿附近有一塊內容未解明的石板", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];

    subgraph cluster_n189 {
      label="張睿";
      color="#64748B";
      fillcolor="#E6E6E622";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n189 [label="張睿", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n190 [label="天城博敏大學同事", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n191 [label="事件平息後離職，之後轉至私人研究機構，五年前\n回到大學任職", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }


    subgraph cluster_n192 {
      label="澤井陽基";
      color="#64748B";
      fillcolor="#E6E6E622";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n192 [label="澤井陽基", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n193 [label="天城博敏找來的古代語顧問，協助破譯航海日誌", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n194 [label="考察後失聯", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n195 [label="最清楚日誌內容", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }


    subgraph cluster_n198 {
      label="天城博敏";
      color="#64748B";
      fillcolor="#E6E6E622";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n198 [label="天城博敏", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n199 [label="妻子是彭達拉薩人，祖上是深海之星成員", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n200 [label="透過深海之星聯繫上其他彭達拉薩成員", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n201 [label="女兒天城美嘉留患有先天性疾病", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n202 [label="化石被盜後下落不明", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }


    subgraph cluster_n205 {
      label="化石";
      color="#64748B";
      fillcolor="#CCE5FF22";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n205 [label="化石", shape="box", fillcolor="#CCE5FF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n206 [label="人頭鳥身，高約30CM", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n207 [label="發現於南極一處山洞的神殿外", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n208 [label="已滅絕的海之住民", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n209 [label="生活於八十至一百萬年前", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n210 [label="基質稀薄期，海之住民大滅絕", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }

  }

  subgraph cluster_n213 {
    label="印度洋王國廢墟";
    color="#64748B";
    fillcolor="#E6FFCC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n213 [label="印度洋王國廢墟", shape="box", fillcolor="#E6FFCC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n214 [label="印度洋公主誕生", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n215 [label="廢墟下與米迦勒身上術式相同的修正力", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n216 [label="米迦勒與施術者有關，V與兩者關係不明", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n217 [label="米迦勒襲擊", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n218 [label="為游騎士（彭達拉薩人）介入提供契機", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n223 [label="米迦勒與V都知道印度洋公主將於何時誕生", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n224 [label="露芝亞高調出現", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n225 [label="遇知目標抵達", shape="box", fillcolor="#B3B3B3", color="#000000", fontcolor="#333333", style="filled,rounded"];
    n226 [label="海洋生物無法靠近", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n227 [label="空間的篩選邏輯", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];

    subgraph cluster_n219 {
      label="防禦法術";
      color="#64748B";
      fillcolor="#FFFFCC22";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n219 [label="防禦法術", shape="box", fillcolor="#FFFFCC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n220 [label="只剩下保護誓約之泉的部分仍在運作", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n221 [label="能量供給充足", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n222 [label="集成了環境能量收集", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }

  }

  subgraph cluster_n228 {
    label="VPTS綁架行動";
    color="#64748B";
    fillcolor="#FFE6CC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n228 [label="VPTS綁架行動", shape="box", fillcolor="#FFE6CC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n229 [label="VPTS掌握所有人魚公主的行蹤，並據此策劃連\n串行動", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n230 [label="V是真正的委託人", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n231 [label="委託人由中介組織僱用，情報由其他人提供", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n232 [label="以電郵聯繫，但其電腦只用作與單一對象聯繫，位\n址在法國", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n233 [label="只有V知道人魚公主必然會經印度回國", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n234 [label="實際上是秘密交易，委託只是形式", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n235 {
    label="堂本海斗";
    color="#64748B";
    fillcolor="#E6E6E622";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n235 [label="堂本海斗", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n236 [label="在海上遇到意外並失憶，被天城美嘉留所救，失去\n關於人魚的記憶", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n237 [label="遭到米迦勒襲擊", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
    n238 [label="力量與水妖、米迦勒同源", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n240 {
    label="米迦勒";
    color="#64748B";
    fillcolor="#E6E6E622";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n240 [label="米迦勒", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n241 [label="企圖綁架人魚公主吸收力量", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n242 [label="米迦勒太快擺出對立態度", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n243 [label="積極尋求合作對米迦勒理應是最優解", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n244 [label="長老才是權力核心，米迦勒不應找人魚公主談合作", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n245 [label="米迦勒對人魚內部並不了解", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n246 {
    label="海之住民化石再現";
    color="#64748B";
    fillcolor="#FFE6CC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n246 [label="海之住民化石再現", shape="box", fillcolor="#FFE6CC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n247 [label="LB奉命搶奪化石", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n248 [label="化石對米迦勒有用/不利", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n249 [label="斯普魯恩斯在人魚公主擊敗水妖後回收化石", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n250 [label="深海之星派斯普魯恩斯確認化石真實性，鑑定報告\n證明化石確屬海之住民，需回收以保密海之住民存\n在", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n251 [label="斯普魯恩斯追上水妖並短暫交手，因人魚公主出現\n而收手", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n252 [label="刻意讓人魚公主解決", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n253 [label="塞雷亞有保密義務", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n254 [label="美嘉收到信件，在海斗陪同下參觀展覽", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n255 [label="斯普魯恩斯無法提供詳細訊息予非成員，要求塞雷\n亞向深海之星提交查詢申請", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n256 [label="斯普魯恩斯對米迦勒事件態度冷漠", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n257 [label="深海之星知道人魚公主的真相", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n258 [label="化石已回收封存，應是內部人員賣至黑市", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n259 [label="化石來自南極，可能伴有遺跡，與米迦勒身份相關", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n272 {
    label="第二張門票";
    color="#64748B";
    fillcolor="#CCE5FF22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n272 [label="第二張門票", shape="box", fillcolor="#CCE5FF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n273 [label="準點傳送至保險箱", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n274 [label="V事前曾親自或派人到印度確認座標", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n275 {
    label="第三次綁架行動";
    color="#64748B";
    fillcolor="#FFE6CC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n275 [label="第三次綁架行動", shape="box", fillcolor="#FFE6CC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n276 [label="VPTS發現屍體失蹤", shape="box", fillcolor="#B3B3B3", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n287 [label="事後調查被列為機密", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];

    subgraph cluster_n277 {
      label="第三方人員";
      color="#64748B";
      fillcolor="#E6E6E622";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n277 [label="第三方人員", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n278 [label="全套防護裝備、隱匿術式", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n279 [label="預期會與其他人交鋒", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n280 [label="隸屬TI，公司核心成員是游離者", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n286 [label="明明可以在對手行動前直接在遠處狙殺，卻選擇正\n面交鋒", shape="box", fillcolor="#DAE8FC", color="#6C8EBF", fontcolor="#111827", style="filled,rounded"];

      subgraph cluster_n281 {
        label="未爆彈";
        color="#64748B";
        fillcolor="#CCE5FF22";
        fontcolor="#111827";
        fontname="Microsoft JhengHei";
        fontsize="12";
        style="filled,rounded";
        penwidth="1.4";

        n281 [label="未爆彈", shape="box", fillcolor="#CCE5FF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
        n282 [label="故意使用未爆彈測試SWI", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
        n283 [label="不知道是未爆彈，意圖殺害人魚公主", shape="box", fillcolor="#DAE8FC", color="#6C8EBF", fontcolor="#111827", style="filled,rounded"];
        n284 [label="策劃者欠缺判斷能力", shape="box", fillcolor="#DAE8FC", color="#6C8EBF", fontcolor="#111827", style="filled,rounded"];
        n285 [label="客戶要求", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
      }

    }

  }

  subgraph cluster_n288 {
    label="護照";
    color="#64748B";
    fillcolor="#CCE5FF22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n288 [label="護照", shape="box", fillcolor="#CCE5FF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n289 [label="諾愛爾與可伶為法國籍，可可卻是日本籍", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n290 [label="根據簽發日期與入境紀錄，諾愛爾在拿到護照後便\n馬上前往加拿大", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n291 [label="兩人本來就擁有法國國籍", shape="box", fillcolor="#B3B3B3", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n292 [label="兩人需辦理工作簽證", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n293 {
    label="廢棄研究所";
    color="#64748B";
    fillcolor="#E6FFCC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n293 [label="廢棄研究所", shape="box", fillcolor="#E6FFCC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n294 [label="有彈殼、榴彈碎片", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n295 [label="曾發生激烈戰鬥", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n296 [label="不只是帶走研究資料", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n297 [label="從事生物研究", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n298 [label="地點極為偏僻", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n299 [label="發生多人死傷也無人發現", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n300 [label="研究所與外界幾近隔絕，所有人起居飲食全在研究\n所內", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n301 {
    label="屍體";
    color="#64748B";
    fillcolor="#CCE5FF22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n301 [label="屍體", shape="box", fillcolor="#CCE5FF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];

    subgraph cluster_n302 {
      label="衣著";
      color="#64748B";
      fillcolor="#CCCCFF22";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n302 [label="衣著", shape="box", fillcolor="#CCCCFF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n303 [label="至少有研究員、保全、外來人員三種", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }

  }

  subgraph cluster_n304 {
    label="姿態";
    color="#64748B";
    fillcolor="#CCCCFF22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n304 [label="姿態", shape="box", fillcolor="#CCCCFF", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n305 [label="（原圖無文字）", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n306 {
    label="傭兵襲擊";
    color="#64748B";
    fillcolor="#FFE6CC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n306 [label="傭兵襲擊", shape="box", fillcolor="#FFE6CC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n307 [label="屍體有VPTS的識別章", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n308 [label="事前沒有發現VPTS在附近活動的跡象", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n309 [label="長期監視著研究所周邊活動", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n310 {
    label="張睿被殺";
    color="#64748B";
    fillcolor="#FFE6CC22";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n310 [label="張睿被殺", shape="box", fillcolor="#FFE6CC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n311 [label="會面後數天，張睿接到電話後匆忙離開辦公室，讓\n秘書通知學生有急事不上課，同日在小巷被槍殺", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n312 [label="因財物消失初步判定為隨機劫殺", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n313 [label="現場附近人跡罕至，沒有目擊者", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n317 [label="張睿與某人相約見面，之後遭殺害，兇手偽裝成隨\n機劫殺", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
    n318 [label="報案人為路過的流浪漢", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n319 [label="案發時三人已離境", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n320 [label="張睿是情報人員，懷疑自己被跟蹤", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n321 [label="空的公文包，文件實際已交出，張睿是在偽裝準備\n交收", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n322 [label="約見方出現在小巷滅口", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n323 [label="消失的領帶夾", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n324 [label="張睿稱是妻子所送", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n325 [label="妻子不認得該領帶夾", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n326 [label="假秘書所送", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n327 [label="GPS監控", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n328 [label="（原圖無文字）", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n329 [label="反追蹤", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n330 [label="引導他們調查教授之死", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n331 [label="警察懷疑可能受過相關訓練的道爾，但因其身份而\n謹慎處理", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n332 [label="兇手是假秘書", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n333 [label="約見方並未出現在小巷，兇手另有其人", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n334 [label="張睿死前與單一號碼多次通話，通話結束的時間點\n為張睿下車換線或換交通工具前", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n335 [label="死亡時間在掛上電話後一段時間", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n336 [label="約見者有張睿私人電話，不會經秘書聯絡", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n337 [label="約見方受過反偵察訓練", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];

    subgraph cluster_n314 {
      label="接載張睿的司機";
      color="#64748B";
      fillcolor="#E6E6E622";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n314 [label="接載張睿的司機", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n315 [label="張睿下車後沒有馬上走進巷子，而是在路邊接電話", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n316 [label="落客後至少15分鐘才聽到聲響，但出於怕麻煩未\n有回頭查看", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    }

  }

  subgraph cluster_n339 {
    label="暗殺委託人";
    color="#64748B";
    fillcolor="#E6E6E622";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n339 [label="暗殺委託人", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n340 [label="有財力聘用更好的傭兵達成目標", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n341 [label="行事謹慎，熟知地下商業的運作", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n342 [label="能夠判斷TI能力不足以完成委託", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n343 [label="經中介找人與TI接洽", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n344 [label="VPTS失敗的保險", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n345 [label="TI失敗後仍繼續委託，直到TI全滅", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n346 [label="非情報來源，情報提供方式與VPTS的委託人相\n同", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n347 [label="專業情報人員", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n348 [label="委託人想借TI消耗VPTS的力量", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n352 {
    label="遠古生物及文明研究所";
    color="#64748B";
    fillcolor="#E6E6E622";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n352 [label="遠古生物及文明研究所", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n353 [label="研究古代生物存在文明的可能性", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n354 [label="（原圖無文字）", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n355 [label="張睿離職時暗中帶走有關廢棄研究所的文件調查", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n378 {
    label="阿拉拉";
    color="#64748B";
    fillcolor="#E6E6E622";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n378 [label="阿拉拉", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n379 [label="成為明星推出人魚公主平常唱的歌吸引人魚公主注\n意，引導她們懷疑長老", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n380 [label="背後有完整團隊", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n381 [label="告訴米迦勒海因茨是舒華澤的人，且知道舒華澤的\n人法力沒有共振特性", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n389 [label="警告海因茨人魚公主比米迦勒更危險", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n390 [label="態度不像米迦勒手下", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n391 [label="真正的幕後黑手", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n392 [label="可能知道人魚公主的秘密", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n393 [label="認為人魚公主危險是不尋常的想法", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n394 [label="使監視者對海因茨懷疑加深", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];

    subgraph cluster_n382 {
      label="南極埋伏";
      color="#64748B";
      fillcolor="#FFE6CC22";
      fontcolor="#111827";
      fontname="Microsoft JhengHei";
      fontsize="12";
      style="filled,rounded";
      penwidth="1.4";

      n382 [label="南極埋伏", shape="box", fillcolor="#FFE6CC", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
      n383 [label="在神殿出口埋伏", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n384 [label="米迦勒料到人魚公主會到神殿調查並從海底的隱藏\n出口離開", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
      n385 [label="自行前往埋伏，引導人魚公主懷疑己方存在叛徒", shape="box", fillcolor="#DAE8FC", color="#6C8EBF", fontcolor="#111827", style="filled,rounded"];
      n386 [label="米迦勒不知道神殿的存在", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
      n387 [label="米迦勒故意引導人魚公主調查，好趁人魚公主落單\n時捉走", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
      n388 [label="知道神殿構造、不受米迦勒指揮", shape="box", fillcolor="#DAE8FC", color="#6C8EBF", fontcolor="#111827", style="filled,rounded"];
    }

  }

  subgraph cluster_n395 {
    label="張睿秘書";
    color="#64748B";
    fillcolor="#E6E6E622";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n395 [label="張睿秘書", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n396 [label="IN聯絡研究團隊成員表示希望見面，第一次全部\n遭拒", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n397 [label="第二次聯絡時張睿的秘書回覆可以約見", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n398 [label="刻意模仿真秘書說話方式，令情報人員未有察覺接\n聽者不同", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n399 [label="會面時假秘書旁聽", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n400 [label="第一次不答應是因為張睿正在外公幹", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n401 [label="實際上張睿請假與假秘書到法國旅遊", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n402 [label="暗中調查", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n403 [label="秘書是張睿的出軌對象", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n404 [label="選擇有人拜訪時幽會不合理", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n405 [label="假秘書甚少露臉，張睿亦不曾場向他人提及，所以\n張睿身邊的人都不知其存在", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n406 [label="真秘書的說法是張睿當時放假與妻子外遊，妻子的\n說法是張睿外出公幹，兩人都沒有和張睿出國", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
    n407 [label="監視張睿、誤導調查", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  subgraph cluster_n408 {
    label="孫天烺";
    color="#64748B";
    fillcolor="#E6E6E622";
    fontcolor="#111827";
    fontname="Microsoft JhengHei";
    fontsize="12";
    style="filled,rounded";
    penwidth="1.4";

    n408 [label="孫天烺", shape="box", fillcolor="#E6E6E6", color="#64748B", fontcolor="#111827", style="filled,bold,rounded", penwidth="1.6"];
    n409 [label="投資南極考察", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  }

  // 原圖未放入任何事件／場地容器的節點；保留在根圖，不另行臆測分類。
  n020 [label="信使有V的修正力殘留，由V操控", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n021 [label="（原圖無文字）", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n022 [label="沙羅記起自已被迪莉亞處以星盡", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n023 [label="信使暗示沙羅已死過一次", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n024 [label="塞雷亞、達姬懷疑沙羅是冒牌貨", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n025 [label="現任人魚公主死亡後新任公主才能誕生", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n050 [label="V有途徑獲得人魚機密", shape="box", fillcolor="#FFFFFF", color="#000000", fontcolor="#111827", style="filled,rounded"];
  n051 [label="研究將生物改造成MS", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n052 [label="星降神臨的核心功能是改造生物", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n053 [label="米迦勒被V操控", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n054 [label="MS資料", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n055 [label="V是阿奎斯托", shape="box", fillcolor="#FFFFFF", color="#000000", fontcolor="#111827", style="filled,rounded"];
  n103 [label="堂本薰是倖存者之一", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n104 [label="信使的行動目標不是復興海之住民，也不需要人魚\n公主的力量", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n105 [label="V與烏蘇拉是合作伙伴", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n106 [label="V是彭達拉薩人", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n107 [label="沙羅找到並解封埃爾確", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n108 [label="法力失控導致的爆炸使長老團陷入混亂，未能追回\n沙羅", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n109 [label="北太平洋王國在海都事件沒有大得益", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
  n110 [label="無法確定海都襲擊北太平洋王國是否克洛德自編自\n導", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n111 [label="證明自衛力量的重要性，衛隊得以明正言順存在", shape="box", fillcolor="#D5E8D4", color="#82B366", fontcolor="#111827", style="filled,rounded"];
  n112 [label="印度洋是保守派的勢力範圍，且未發現被克洛德滲\n透的跡象", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
  n113 [label="內戰對北太平洋沒有好處", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
  n114 [label="動機不明確", shape="box", fillcolor="#F8CECC", color="#B85450", fontcolor="#111827", style="filled,rounded"];
  n115 [label="秘書是當年送天城美嘉留回家的人", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n116 [label="天城博敏、張睿曾在同一研究所工作", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n117 [label="天城博敏曾帶天城美嘉留前往研究所治療", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n118 [label="天城博敏本答應完成收尾工作就回家，但再次失去\n聯絡", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n119 [label="研究可能與海之住民、化石有關", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n120 [label="廢棄研究所重新啟用", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n121 [label="澤井陽基是天城博敏的引薦人", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n122 [label="找回文件", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n123 [label="實驗參與者轉移文件", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n142 [label="SWI不確定露芝亞如何前往印度洋、不知道是「\n沙羅」讓她去", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n143 [label="SWI與「沙羅」並非同伴", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n144 [label="「沙羅」是長老的傀儡", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n151 [label="美喜留記憶中父親帶自己去治療的地方", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n152 [label="必須經印度才能在時限內打開保險櫃", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n239 [label="人魚方高層洩漏情報", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n268 [label="真秘書向警察透露曾有人想約見張睿，詢問考察造\n假事件", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n269 [label="事先安排與張睿身材接近的人接應，在擠迫的地鐵\n上貼著站，與張睿交換裝有文件的公事包", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n270 [label="清道夫開始核查諾愛爾背景", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n271 [label="清道夫試圖誤導終端機文件尚未交出", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n338 [label="發現之前收到的是假報告後馬上洗機並更換聯繫方\n式，無法繼續追查", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n349 [label="積極調查SWI", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n351 [label="董事長黑克勒認識的一名前軍方高層投資了遠古生\n物及文明研究所", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n357 [label="派遣O-117前往和歌山", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n358 [label="塞雷亞清楚人魚公主行蹤", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n359 [label="達姬與尼歌娜都大致理解其他王國的狀況", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n360 [label="尼歌姬會管束公主，達姬則鼓勵公主享受", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n361 [label="尼歌娜和達姬的角色與各自的身份閱歷不符，達姬\n理應比尼歌娜更清楚犯錯的後果以及帶來的外交問\n題", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n362 [label="其他王國十分重視規矩，犯規會被嚴懲", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n363 [label="水妖對人魚公主的行蹤有一定掌握，且從來不會在\n人魚公主忙碌時出現", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n364 [label="有人密切監視人魚公主動向", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];
  n365 [label="放任遠古生物及文明研究所進行研究", shape="box", fillcolor="#E51400", color="#B20000", fontcolor="#FFFFFF", style="filled,rounded"];
  n366 [label="深海之星支持研究所運作", shape="box", fillcolor="#0050EF", color="#001DBC", fontcolor="#FFFFFF", style="filled,rounded"];
  n410 [label="奧德斯欺騙天城博敏其女之病無法治療", shape="box", fillcolor="#FFFFFF", color="#64748B", fontcolor="#111827", style="filled,rounded"];

  // 原圖連線：所有邊的文字皆為空，因此不增添關係標籤。
  n063 -> n072;
  n077 -> n072;
  n088 -> n073;
  n086 -> n073;
  n101 -> n073;
  n161 -> n165;
  n178 -> n173;
  n379 -> n380;
  n385 -> n388;
  n383 -> n384;
  n383 -> n385;
  n386 -> n385;
  n384 -> n387;
  n389 -> n390;
  n389 -> n393;
  n390 -> n391;
  n393 -> n392;
  n388 -> n391;
  n002 -> n003;
  n003 -> n004;
  n007 -> n004;
  n002 -> n005;
  n004 -> n008;
  n008 -> n009;
  n010 -> n012;
  n012 -> n013;
  n012 -> n014;
  n013 -> n011;
  n014 -> n017;
  n015 -> n016;
  n018 -> n016;
  n008 -> n010;
  n009 -> n015;
  n009 -> n018;
  n011 -> n019;
  n022 -> n025;
  n023 -> n022;
  n024 -> n025;
  n024 -> n143;
  n052 -> n051;
  n054 -> n051;
  n055 -> n106;
  n057 -> n083;
  n057 -> n059;
  n058 -> n059;
  n061 -> n060;
  n057 -> n061;
  n060 -> n062;
  n059 -> n063;
  n064 -> n071;
  n060 -> n064;
  n065 -> n092;
  n059 -> n065;
  n098 -> n088;
  n087 -> n066;
  n067 -> n057;
  n067 -> n058;
  n068 -> n062;
  n059 -> n068;
  n069 -> n064;
  n071 -> n082;
  n071 -> n070;
  n074 -> n094;
  n059 -> n074;
  n075 -> n072;
  n074 -> n077;
  n077 -> n078;
  n078 -> n076;
  n070 -> n080;
  n081 -> n091;
  n070 -> n081;
  n083 -> n084;
  n084 -> n096;
  n085 -> n073;
  n062 -> n087;
  n082 -> n089;
  n089 -> n090;
  n091 -> n086;
  n092 -> n102;
  n093 -> n102;
  n094 -> n095;
  n096 -> n097;
  n066 -> n098;
  n099 -> n100;
  n100 -> n101;
  n104 -> n053;
  n108 -> n107;
  n109 -> n114;
  n110 -> n111;
  n113 -> n109;
  n112 -> n107 [color="#000000"];
  n111 -> n113;
  n116 -> n117;
  n116 -> n121;
  n117 -> n118;
  n117 -> n119;
  n117 -> n115;
  n123 -> n120;
  n142 -> n143;
  n143 -> n144;
  n156 -> n158;
  n163 -> n164;
  n167 -> n168;
  n170 -> n169;
  n174 -> n213;
  n154 -> n159;
  n158 -> n055;
  n177 -> n103;
  n164 -> n106;
  n193 -> n195;
  n196 -> n197;
  n196 -> n193 [style="dashed"];
  n199 -> n200;
  n203 -> n204;
  n200 -> n196;
  n206 -> n208;
  n209 -> n210;
  n210 -> n208;
  n204 -> n208;
  n196 -> n211;
  n214 -> n223;
  n215 -> n216;
  n217 -> n218;
  n220 -> n221;
  n221 -> n222;
  n217 -> n223;
  n224 -> n225;
  n175 -> n214;
  n234 -> n351;
  n231 -> n232;
  n231 -> n230;
  n233 -> n230;
  n231 -> n234;
  n236 -> n237;
  n050 -> n239;
  n241 -> n242;
  n243 -> n242;
  n244 -> n245;
  n247 -> n248;
  n249 -> n258;
  n249 -> n250;
  n251 -> n252;
  n251 -> n249;
  n252 -> n257;
  n250 -> n253;
  n255 -> n256;
  n256 -> n257;
  n249 -> n188;
  n223 -> n050;
  n273 -> n274;
  n171 -> n272;
  n276 -> n287;
  n278 -> n279;
  n279 -> n286;
  n282 -> n285;
  n283 -> n284;
  n286 -> n284 [color="#000000"];
  n172 -> n152;
  n289 -> n291;
  n289 -> n292;
  n294 -> n295;
  n298 -> n299;
  n311 -> n312;
  n312 -> n317;
  n317 -> n323;
  n319 -> n330;
  n320 -> n333;
  n321 -> n320;
  n317 -> n321;
  n321 -> n333;
  n336 -> n320;
  n337 -> n320;
  n323 -> n324;
  n324 -> n326;
  n325 -> n326;
  n337 -> n331;
  n315 -> n334;
  n334 -> n337;
  n334 -> n336;
  n315 -> n335;
  n316 -> n335;
  n313 -> n314;
  n311 -> n268;
  n228 -> n275;
  n229 -> n050;
  n232 -> n338;
  n277 -> n339;
  n340 -> n348;
  n343 -> n341;
  n341 -> n342;
  n342 -> n344;
  n345 -> n348;
  n346 -> n347;
  n347 -> n347;
  n349 -> n357;
  n276 -> n349;
  n213 -> n230;
  n338 -> n347;
  n218 -> n008;
  n358 -> n011;
  n242 -> n016;
  n152 -> n233;
  n359 -> n361;
  n360 -> n361;
  n362 -> n361;
  n363 -> n364;
  n217 -> n240;
  n310 -> n270;
  n396 -> n397;
  n397 -> n398;
  n399 -> n407;
  n397 -> n400;
  n403 -> n405;
  n405 -> n404;
  n400 -> n401;
  n401 -> n402;
  n401 -> n403;
  n406 -> n401;
  n404 -> n407;
  n397 -> n330;
  n196 -> n408;
  n191 -> n352;
  n202 -> n352;
  n268 -> n330;

  // 粗略時序約束：依原圖頂層項目的 Y 座標分帶，上方較早、下方較晚。
  time_anchor_00 [shape="point", width="0.01", label="", style="invis"];
  { rank=same; time_anchor_00; n159; n153; n293; n301; n304; n306; }
  time_anchor_01 [shape="point", width="0.01", label="", style="invis"];
  { rank=same; time_anchor_01; n142; n103; n235; }
  time_anchor_02 [shape="point", width="0.01", label="", style="invis"];
  { rank=same; time_anchor_02; n143; n144; n024; n025; n112; n022; n023; n213; n240; n228; n152; n272; }
  time_anchor_03 [shape="point", width="0.01", label="", style="invis"];
  { rank=same; time_anchor_03; n107; n108; n109; n110; n111; n113; n001; n055; n106; n288; n363; n364; n050; n239; n275; n349; n357; n351; }
  time_anchor_04 [shape="point", width="0.01", label="", style="invis"];
  { rank=same; time_anchor_04; n378; n114; n339; n338; n246; n365; n366; }
  time_anchor_05 [shape="point", width="0.01", label="", style="invis"];
  { rank=same; time_anchor_05; n056; n358; n359; n360; n362; n310; n270; n188; }
  time_anchor_06 [shape="point", width="0.01", label="", style="invis"];
  { rank=same; time_anchor_06; n395; n361; n268; n115; n122; n123; n116; n117; n118; n119; n121; n408; }
  time_anchor_07 [shape="point", width="0.01", label="", style="invis"];
  { rank=same; time_anchor_07; n269; n271; n120; n151; n020; n052; n053; n051; n054; n104; n105; n410; n352; }
  time_anchor_00 -> time_anchor_01 [style="invis", weight="100", minlen="2"];
  time_anchor_01 -> time_anchor_02 [style="invis", weight="100", minlen="2"];
  time_anchor_02 -> time_anchor_03 [style="invis", weight="100", minlen="2"];
  time_anchor_03 -> time_anchor_04 [style="invis", weight="100", minlen="2"];
  time_anchor_04 -> time_anchor_05 [style="invis", weight="100", minlen="2"];
  time_anchor_05 -> time_anchor_06 [style="invis", weight="100", minlen="2"];
  time_anchor_06 -> time_anchor_07 [style="invis", weight="100", minlen="2"];

  // 原圖圖例
  subgraph cluster_legend {
    label="原圖分類圖例";
    color="#CBD5E1";
    style="rounded,dashed";
    fontname="Microsoft JhengHei";
    legend_evidence [label="證物", shape="box", style="filled", fillcolor="#CCE5FF"];
    legend_evidence_detail [label="證物細節", shape="box", style="filled", fillcolor="#CCCCFF"];
    legend_scene [label="現場", shape="box", style="filled", fillcolor="#E6FFCC"];
    legend_scene_detail [label="現場細節", shape="box", style="filled", fillcolor="#FFFFCC"];
    legend_person [label="重要人物", shape="box", style="filled", fillcolor="#E6E6E6"];
    legend_event [label="事件", shape="box", style="filled", fillcolor="#FFE6CC"];
  }
}
```

## 轉換稽核

以下連線在原始 mxGraphModel 中缺少來源或目標，未加入圖中，以免猜測：

- `e044`：`缺失` → `缺失`
- `e045`：`缺失` → `缺失`
- `e046`：`信使有V的修正力殘留，由V操控` → `缺失`
- `e051`：`缺失` → `「沙羅」是長老的傀儡`
- `e085`：`捨棄肉體保留靈魂，將來轉移至新容器` → `缺失`
- `e099`：`信使是鳥人原生樣貌` → `缺失`
- `e132`：`天城博敏、張睿曾在同一研究所工作` → `缺失`
- `e171`：`V懂得阿奎斯托語` → `缺失`

> [!NOTE]
> 要重新同步 SVG，可在 vault 根目錄執行：
> `python scripts/drawio_svg_to_graphviz.py --check`
