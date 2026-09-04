---
tags:
  - investigation
  - clues-dsl
  - operation-siskin
source:
  - "[[Story/The Outsiders [Vol. Stargazer]]]"
  - "[[線索-DSL-米迦勒與V]]"
  - "[[線索-DSL-陸地現場-音樂會與孤兒院]]"
  - "[[線索-DSL-綁架行動與VPTS]]"
cssclasses:
  - graphviz-large-preview
---

# 第一封信 → 孤兒院 → 米迦勒襲擊 → 綁架事件（DSL）

> [!NOTE] 寫法
> 只需維護下方 clues 區塊，執行 `python scripts/clues_to_graphviz.py <本檔>` 重生下方圖，`python scripts/clues_to_canvas.py <本檔>` 重生同名 .canvas。
> - `# 群組`：cluster，`##` 為巢狀。
> - `類型 內容 = 別名 @時點 #狀態`：類型可用 證據／事件／實體／假設／未決／矛盾；別名、時點、狀態皆可省略。
> - `A -支持-> B | C`：關係可用 支持／導致／推導／矛盾／時序／屬於，省略即為「關係未定」的灰虛線。
> - 填色與形狀＝類型；邊框粗細與虛實＝狀態（已確認／預定／推論／補丁）。
>
> 依 Operation Siskin 正文（[[Story/The Outsiders [Vol. Stargazer]]]）整理四個階段；`證據` 皆有正文出處，`假設` 為 Kafziel／麗奈等角色在文中提出的推論，`未決` 為文中明言尚無答案的問題。「串連假設」群組是原 SVG 中跨階段的推理，正文尚未證實。
> 印度寄存櫃（4/6）一段不在本卷正文，只以 `未決` 佔位。

```clues
標題: 第一封信 → 孤兒院 → 米迦勒襲擊 → 綁架事件（Operation Siskin）
時序: 2004-02-22, 2004-02-25, 2004-04-05, 2004-04-06, 2004-04-15

# 第一封信（檀香山公園）
事件 V 經 Glove 留在公園的錨點送來只裝著一張合照的信封 = 第一封信 @2004-02-22
證據 合照：十來個小孩圍著白髮花襯衫男人與數名中年女人，攝於紅磚建築前，被燒掉一角 = 合照
證據 照片背面「檀香山，2004-2-25」為 V 筆跡，書寫時間約在送信前十天 = 背面日期
證據 合照至少三十年歷史，但保存狀況良好 = 合照年代
證據 封蠟成份常見，圖案是獨特的十字變體，表面不平整且缺角 = 封蠟
證據 錨點沉寂十幾年後於 22 日啟用；V 在字母表排第 22，檔案顯示他偏愛此數字 = 二十二
假設 背面日期是 V 預告他們抵達孤兒院的日子 = 預告日期
假設 合照由倖存者帶出火場保存；V 控制了倖存者之一或其身邊人 = 倖存者來源
假設 封蠟圖案是家徽或組織印章，可大幅收窄排查範圍 = 印章
假設 封蠟者技術生疏，可能是新手而非 V 本人 = 新手封蠟
未決 三名倖存者被領養後改名，公開紀錄查不到下落 = 倖存者下落
假設 堂本薰是倖存者之一（見 [[線索-DSL-米迦勒與V]]） = 堂本薰

# 孤兒院（檀香山）
事件 Kafziel 與 Acer 調查廢棄孤兒院 = 孤兒院調查 @2004-02-25
證據 29 年前半夜火災，起火點廚房，期間數次爆炸，僅 3 名小孩生還 = 火災
證據 圍牆缺口有纖維與泥土，窗框有本地泥土，腳印動線只有窗前、鐵櫃前、牆前三個停留點 = 現場痕跡
證據 洞口木屑顯示是火災後鑽開，登山靴鞋印與綠色人造纖維皆屬常見品 = 痕跡不足
證據 壁畫 Hangman：Execute at ＿＿＿＿＿ ＿＿＿＿＿ 19:00，橙色 = Hangman
證據 字體刻意強調 v，此前只在 V 的挑釁訊息中出現 = V字體
證據 由畫的頂端高度推估畫者身高 1.75 至 1.85 米 = 畫者身高
證據 字母積木與藍色盒子（貝殼凹槽、橙色圓珠）帶特殊能量，構成開關、發射、接收的答題系統 = 答題系統
證據 謎題答案：APRIL FIFTH，配合 19:00 = 四月五日
事件 完成謎題後圓珠隨未知語言歌聲飛起，落入地下室 = 圓珠引路
證據 地下室橙色七芒星圓陣，橙色圓珠代表印度洋王國；粉、黃（北太平洋、南太平洋）缺失 = 七芒星
證據 陣心躺著昏迷的游離者沙羅，護著第二封信；身體乾淨，無海水、泥土痕跡 = 沙羅現身
證據 貝殼下一美分硬幣是 Glove（AS-1053）的傳送錨點，外覆圓柱狀 APCS = Glove錨點
證據 藍色盒子內有不導電但對法力反應的類電路板，量產工業品，含未知合金與稀土 = 類電路板
假設 V 以 Glove 錨點把沙羅從海底傳來，中途替她清洗更衣或直接換了身體 = 沙羅被搬運
假設 Glove 與 V 不是一次性合作 = 持續合作
假設 V 刻意用橙色配合沙羅的髮色（他過去偏好紅色） = 橙色
假設 作畫者可能是 V 控制的代理人，身材不必與 V 相近 = 代理人
假設 選孤兒院是暗指人魚公主沒有父母，形同孤兒 = 孤兒象徵
假設 Hangman 暗含處刑者與阻止者的對立，「被處死者」可能另有指向 = 處刑隱喻
未決 粉、黃兩顆圓珠缺失的含意 = 缺失圓珠
未決 類電路板的供應鏈——沙羅從未見過此物 = 板材來源

## 第二封信
證據 阿奎斯托語詩文：深海之王已落幕、背叛者戲份未完、擊穿堡壘的長槍、歡迎回到舞台前公主 = 詩文
證據 紅色戲票：4 月 5 日 19:00，公海座標附高度，劇目 Stargazer = 戲票
證據 印度車站行李寄存收據，截止日由 2 月 10 日塗改為 4 月 6 日晚 = 收據
證據 封蠟樣式與第一封信相同 = 同封蠟
假設 收信對象是沙羅；V 懂阿奎斯托語，且知道她是前公主 = 對象沙羅
假設 V 自視為導演，要把「已殺青」的沙羅抓回舞台；「擊穿堡壘」不會只是重演侵略 = 導演劇本
假設 戲票是要他們「參演」而非「觀賞」 = 參演
假設 兒童元素加孤兒院加 4/5 19:00，指向新任人魚公主誕生 = 誕生推論
假設 V 在 IU7 生活過、待過阿奎斯托群體，甚至可能在此出生 = V的出身
未決 沙羅自己都不知道的誕生日期，V 為何知道 = 誕生情報源
未決 寄存櫃內容物；持塗改收據如何提領 = 寄存櫃

# 米迦勒襲擊（印度洋誓約之泉）
事件 沙羅將露芝亞送往印度洋歸還珍珠，星羅自貝殼誕生 = 星羅誕生 @2004-04-05
事件 米迦勒與 Black Beauty Sisters、水妖現身，宣告要把新生公主化為自己的一部分 = 米迦勒襲擊 @2004-04-05
事件 Kafziel 以閃光彈干擾、防護壁抵擋，將露芝亞與星羅傳送脫離 = 救援
證據 米迦勒自稱「阿奎斯托的王」，卻對人魚公主說標準日語 = 標準日語
證據 空間只拉入生物與誓約之泉，術式有特定作用對象且刻意 = 空間篩選
證據 空間與廢墟之下的大量修正力同源，編號 AS-1079；分析結果為 Type: Programme = AS-1079
證據 米迦勒稱 Kafziel 為「倫道爾的舒華澤」、「傲慢的彭達拉薩人」，並提及他曾拒絕邀請 = 舒華澤
證據 沙羅事前委託 Kafziel 救人，卻只向露芝亞提星羅的事 = 沙羅委託
證據 沙羅事後以電話聯絡露芝亞 = 沙羅在陸地
證據 米迦勒得手失敗後主動撤退 = 撤退
假設 米迦勒不是游離者，只是修正力術式的作用主體 = 術式主體
假設 詩詩與美美的復活是米迦勒所為 = 復活
假設 Kafziel 曾與米迦勒接觸並拒絕邀請，或米迦勒認錯了人 = 曾接觸
假設 沙羅事先知道米迦勒會出現 = 沙羅預知
未決 米迦勒的情報來源是誰；V 是情報鏈一環還是想利用事件的第三方 = 情報鏈
未決 AS-1079 是誰；是否主動參與；與米迦勒、V 的關係 = 未知游離者
未決 沙羅能直接傳送，為何要露芝亞經印度陸路回國 = 經印度

# 綁架事件（印度 → 魁北克）
事件 傭兵在印度搜索星羅，被 Kafziel 一方捷足先登（第一次行動失敗） = 印度搜索 @2004-04-06
事件 傭兵啟動後備計劃，以七位人魚公主為目標並展開監視 = 後備計劃
事件 兩支傭兵小隊夜襲哈佛聖皮埃爾小屋，注射鎮靜劑帶走諾愛爾與可伶 = 魁北克綁架 @2004-04-15
事件 Kafziel、Soar 冒充傭兵擊殺 A 隊，B 隊清除狙擊手，並拉上可可安撫兩人 = 攔截
事件 第三方隱匿人員持步槍逼近，意圖殺人，被擊殺 = 第三方
證據 傭兵無隊伍標識，用北美流通槍械，行動模式屬前駐軍 = 傭兵特徵
證據 上層堅持派兩隊，並傾向把上次失敗歸為人為失誤 = 上層判斷
證據 第三方使用不同無線電頻道，資料庫無此人紀錄 = 不同頻道
證據 行李袋文件：所有公主的情報、監視紀錄、行動計劃與事後報告，金澤同事已核實 = 行李袋文件
證據 諾愛爾與可伶幾乎在入境當刻就被監視 = 入境監視
證據 鎮靜劑對人魚提早失效 = 鎮靜劑
假設 第三方與要活口的傭兵不是一夥，局面至少是三方混戰 = 三方混戰
假設 委託人知道公主的真實身分，否則沒有委託動機 = 委託動機
假設 傭兵背後有掌握所有公主行蹤的情報源 = 行蹤情報
未決 傭兵真正僱主；「寶物」的吸引力；與 V 的關係 = 僱主
未決 傭兵為何知道星羅存在 = 星羅情報

# 串連假設（原 SVG 推理，正文未證實）
假設 V 引導游騎士介入，是為了讓彭達拉薩人出現在人魚面前 = 引導介入
假設 V 是傭兵的真正委託人；只有 V 知道公主必經印度回國 = V委託
假設 寄存櫃 4/6 時限迫使 Kafziel 一方經印度，與傭兵搜索時空重疊 = 時限重疊
假設 沙羅是 V 賦予的翻譯與解讀者角色 = 沙羅角色
矛盾 V 若是委託人，為何同時引導 Kafziel 破壞綁架（劇本需要衝突，或藉此測試 SWI） = 委託矛盾

// 第一封信
第一封信 -屬於-> 合照 | 背面日期 | 封蠟 | 二十二
合照 -支持-> 合照年代 | 火災
合照年代 -支持-> 倖存者來源
倖存者來源 -推導-> 倖存者下落
倖存者來源 -支持-> 堂本薰
背面日期 -支持-> 預告日期
封蠟 -支持-> 印章 | 新手封蠟
合照 -導致-> 孤兒院調查

// 孤兒院
孤兒院調查 -屬於-> 現場痕跡 | Hangman | 答題系統 | 痕跡不足
現場痕跡 -支持-> 畫者身高
Hangman -支持-> V字體 | 畫者身高 | 處刑隱喻
V字體 -支持-> 代理人
畫者身高 -支持-> 代理人
答題系統 -導致-> 四月五日
答題系統 -支持-> 類電路板
類電路板 -推導-> 板材來源
四月五日 -導致-> 圓珠引路
圓珠引路 -導致-> 七芒星
七芒星 -推導-> 缺失圓珠
七芒星 -屬於-> 沙羅現身 | Glove錨點
沙羅現身 -支持-> 沙羅被搬運
Glove錨點 -支持-> 沙羅被搬運 | 持續合作
Hangman -支持-> 橙色
七芒星 -支持-> 橙色
火災 -支持-> 孤兒象徵
沙羅現身 -屬於-> 詩文 | 戲票 | 收據 | 同封蠟
同封蠟 -支持-> 新手封蠟
詩文 -支持-> 對象沙羅 | 導演劇本 | V的出身
戲票 -支持-> 參演
四月五日 -支持-> 誕生推論
戲票 -支持-> 誕生推論
孤兒象徵 -支持-> 誕生推論
誕生推論 -推導-> 誕生情報源
收據 -推導-> 寄存櫃
類電路板 -支持-> V的出身

// 米迦勒襲擊
誕生推論 -導致-> 星羅誕生
戲票 -時序-> 星羅誕生
星羅誕生 -導致-> 米迦勒襲擊
米迦勒襲擊 -導致-> 救援
米迦勒襲擊 -屬於-> 標準日語 | 空間篩選 | AS-1079 | 舒華澤 | 撤退
AS-1079 -支持-> 術式主體
標準日語 -支持-> 術式主體
舒華澤 -支持-> 曾接觸
米迦勒襲擊 -支持-> 復活
沙羅委託 -支持-> 沙羅預知
沙羅在陸地 -支持-> 沙羅預知
沙羅預知 -推導-> 情報鏈
米迦勒襲擊 -推導-> 情報鏈
AS-1079 -推導-> 未知游離者
救援 -推導-> 經印度
誕生情報源 -支持-> 情報鏈

// 綁架事件
經印度 -導致-> 印度搜索
救援 -時序-> 印度搜索
印度搜索 -導致-> 後備計劃
後備計劃 -導致-> 入境監視 | 魁北克綁架
魁北克綁架 -導致-> 攔截 | 第三方
魁北克綁架 -屬於-> 傭兵特徵 | 上層判斷 | 鎮靜劑
攔截 -屬於-> 行李袋文件
第三方 -屬於-> 不同頻道
不同頻道 -支持-> 三方混戰
行李袋文件 -支持-> 行蹤情報 | 入境監視
行蹤情報 -支持-> 委託動機
印度搜索 -推導-> 星羅情報
星羅情報 -支持-> 行蹤情報
委託動機 -推導-> 僱主
三方混戰 -推導-> 僱主

// 串連
救援 -支持-> 引導介入
戲票 -支持-> 引導介入
經印度 -支持-> 時限重疊
寄存櫃 -支持-> 時限重疊
時限重疊 -支持-> V委託
僱主 -支持-> V委託
星羅情報 -支持-> V委託
對象沙羅 -支持-> 沙羅角色
V委託 -矛盾-> 委託矛盾
引導介入 -矛盾-> 委託矛盾
```

```dot
// clues-auto 由上方 clues 區塊生成，請勿手改；重新執行 scripts/clues_to_graphviz.py
digraph clues {
  graph [
    rankdir="TB", bgcolor="#FFFFFF", newrank="true", compound="true",
    splines="spline", nodesep="0.30", ranksep="0.60", pad="0.15",
    fontname="Microsoft JhengHei, Noto Sans CJK TC, PingFang TC, sans-serif", fontsize="16", labelloc="t",
    label="第一封信 → 孤兒院 → 米迦勒襲擊 → 綁架事件（Operation Siskin）"
  ];
  node [fontname="Microsoft JhengHei, Noto Sans CJK TC, PingFang TC, sans-serif", fontsize="9", fontcolor="#1F2937", margin="0.10,0.06"];
  edge [fontname="Microsoft JhengHei, Noto Sans CJK TC, PingFang TC, sans-serif", fontsize="8", fontcolor="#475569", arrowsize="0.65"];

  subgraph cluster_00 {
    label="串連假設（原 SVG 推理，正文未證實）"; color="#CBD5E1"; fillcolor="#FAFAFA";
    fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
    n079 [label="V 引導游騎士介入，是為了讓\n彭達拉薩人出現在人魚面前", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n080 [label="V 是傭兵的真正委託人；只有\nV 知道公主必經印度回國", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n081 [label="寄存櫃 4/6 時限迫使\nKafziel 一方經印度，\n與傭兵搜索時空重疊", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n082 [label="沙羅是 V\n賦予的翻譯與解讀者角色", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n083 [label="V 若是委託人，為何同時引導\nKafziel 破壞綁架（劇\n本需要衝突，或藉此測試\nSWI）", shape="box", style="filled", fillcolor="#FEE2E2", color="#DC2626", penwidth="2.6"];
  }
  subgraph cluster_01 {
    label="孤兒院（檀香山）"; color="#CBD5E1"; fillcolor="#FAFAFA";
    fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
    n013 [label="Kafziel 與 Acer\n調查廢棄孤兒院", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n014 [label="29 年前半夜火災，起火點廚\n房，期間數次爆炸，僅 3\n名小孩生還", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n015 [label="圍牆缺口有纖維與泥土，窗框有\n本地泥土，腳印動線只有窗前、\n鐵櫃前、牆前三個停留點", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n016 [label="洞口木屑顯示是火災後鑽開，登\n山靴鞋印與綠色人造纖維皆屬常\n見品", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n017 [label="壁畫 Hangman：Exe\ncute at ＿＿＿＿＿\n＿＿＿＿＿ 19:00，橙色", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n018 [label="字體刻意強調 v，此前只在\nV 的挑釁訊息中出現", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n019 [label="由畫的頂端高度推估畫者身高\n1.75 至 1.85 米", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n020 [label="字母積木與藍色盒子（貝殼凹槽\n、橙色圓珠）帶特殊能量，構成\n開關、發射、接收的答題系統", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n021 [label="謎題答案：APRIL\nFIFTH，配合 19:00", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n022 [label="完成謎題後圓珠隨未知語言歌聲\n飛起，落入地下室", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n023 [label="地下室橙色七芒星圓陣，橙色圓\n珠代表印度洋王國；粉、黃（北\n太平洋、南太平洋）缺失", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n024 [label="陣心躺著昏迷的游離者沙羅，護\n著第二封信；身體乾淨，無海水\n、泥土痕跡", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n025 [label="貝殼下一美分硬幣是 Glov\ne（AS-1053）的傳送錨\n點，外覆圓柱狀 APCS", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n026 [label="藍色盒子內有不導電但對法力反\n應的類電路板，量產工業品，含\n未知合金與稀土", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n027 [label="V 以 Glove 錨點把沙\n羅從海底傳來，中途替她清洗更\n衣或直接換了身體", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n028 [label="Glove 與 V\n不是一次性合作", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n029 [label="V 刻意用橙色配合沙羅的髮色\n（他過去偏好紅色）", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n030 [label="作畫者可能是 V\n控制的代理人，身材不必與 V\n相近", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n031 [label="選孤兒院是暗指人魚公主沒有父\n母，形同孤兒", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n032 [label="Hangman 暗含處刑者與\n阻止者的對立，「被處死者」可\n能另有指向", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n033 [label="粉、黃兩顆圓珠缺失的含意", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
    n034 [label="類電路板的供應鏈——沙羅從未\n見過此物", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
    subgraph cluster_02 {
      label="第二封信"; color="#CBD5E1"; fillcolor="#FAFAFA";
      fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
      n035 [label="阿奎斯托語詩文：深海之王已落\n幕、背叛者戲份未完、擊穿堡壘\n的長槍、歡迎回到舞台前公主", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
      n036 [label="紅色戲票：4 月 5 日 1\n9:00，公海座標附高度，劇\n目 Stargazer", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
      n037 [label="印度車站行李寄存收據，截止日\n由 2 月 10 日塗改為\n4 月 6 日晚", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
      n038 [label="封蠟樣式與第一封信相同", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
      n039 [label="收信對象是沙羅；V 懂阿奎斯\n托語，且知道她是前公主", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
      n040 [label="V 自視為導演，要把「已殺青\n」的沙羅抓回舞台；「擊穿堡壘\n」不會只是重演侵略", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
      n041 [label="戲票是要他們「參演」而非「觀\n賞」", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
      n042 [label="兒童元素加孤兒院加 4/5 \n19:00，指向新任人魚公主\n誕生", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
      n043 [label="V 在 IU7 生活過、待過\n阿奎斯托群體，甚至可能在此出\n生", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
      n044 [label="沙羅自己都不知道的誕生日期，\nV 為何知道", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
      n045 [label="寄存櫃內容物；持塗改收據如何\n提領", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
    }
  }
  subgraph cluster_03 {
    label="第一封信（檀香山公園）"; color="#CBD5E1"; fillcolor="#FAFAFA";
    fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
    n001 [label="V 經 Glove 留在公園\n的錨點送來只裝著一張合照的信\n封", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n002 [label="合照：十來個小孩圍著白髮花襯\n衫男人與數名中年女人，攝於紅\n磚建築前，被燒掉一角", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n003 [label="照片背面「檀香山，2004-\n2-25」為 V\n筆跡，書寫時間約在送信前十天", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n004 [label="合照至少三十年歷史，但保存狀\n況良好", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n005 [label="封蠟成份常見，圖案是獨特的十\n字變體，表面不平整且缺角", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n006 [label="錨點沉寂十幾年後於 22\n日啟用；V 在字母表排第\n22，檔案顯示他偏愛此數字", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n007 [label="背面日期是 V\n預告他們抵達孤兒院的日子", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n008 [label="合照由倖存者帶出火場保存；V\n控制了倖存者之一或其身邊人", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n009 [label="封蠟圖案是家徽或組織印章，可\n大幅收窄排查範圍", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n010 [label="封蠟者技術生疏，可能是新手而\n非 V 本人", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n011 [label="三名倖存者被領養後改名，公開\n紀錄查不到下落", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
    n012 [label="堂本薰是倖存者之一（見 [[\n線索-DSL-米迦勒與V]]\n）", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
  }
  subgraph cluster_04 {
    label="米迦勒襲擊（印度洋誓約之泉）"; color="#CBD5E1"; fillcolor="#FAFAFA";
    fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
    n046 [label="沙羅將露芝亞送往印度洋歸還珍\n珠，星羅自貝殼誕生", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n047 [label="米迦勒與 Black\nBeauty Sisters\n、水妖現身，宣告要把新生公主\n化為自己的一部分", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n048 [label="Kafziel 以閃光彈干擾\n、防護壁抵擋，將露芝亞與星羅\n傳送脫離", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n049 [label="米迦勒自稱「阿奎斯托的王」，\n卻對人魚公主說標準日語", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n050 [label="空間只拉入生物與誓約之泉，術\n式有特定作用對象且刻意", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n051 [label="空間與廢墟之下的大量修正力同\n源，編號\nAS-1079；分析結果為\nType:\nProgramme", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n052 [label="米迦勒稱 Kafziel 為\n「倫道爾的舒華澤」、「傲慢的\n彭達拉薩人」，並提及他曾拒絕\n邀請", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n053 [label="沙羅事前委託 Kafziel\n救人，卻只向露芝亞提星羅的事", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n054 [label="沙羅事後以電話聯絡露芝亞", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n055 [label="米迦勒得手失敗後主動撤退", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n056 [label="米迦勒不是游離者，只是修正力\n術式的作用主體", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n057 [label="詩詩與美美的復活是米迦勒所為", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n058 [label="Kafziel 曾與米迦勒接\n觸並拒絕邀請，或米迦勒認錯了\n人", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n059 [label="沙羅事先知道米迦勒會出現", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n060 [label="米迦勒的情報來源是誰；V 是\n情報鏈一環還是想利用事件的第\n三方", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
    n061 [label="AS-1079 是誰；是否主\n動參與；與米迦勒、V 的關係", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
    n062 [label="沙羅能直接傳送，為何要露芝亞\n經印度陸路回國", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
  }
  subgraph cluster_05 {
    label="綁架事件（印度 → 魁北克）"; color="#CBD5E1"; fillcolor="#FAFAFA";
    fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";
    n063 [label="傭兵在印度搜索星羅，被\nKafziel 一方捷足先登\n（第一次行動失敗）", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n064 [label="傭兵啟動後備計劃，以七位人魚\n公主為目標並展開監視", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n065 [label="兩支傭兵小隊夜襲哈佛聖皮埃爾\n小屋，注射鎮靜劑帶走諾愛爾與\n可伶", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n066 [label="Kafziel、Soar\n冒充傭兵擊殺 A 隊，B 隊\n清除狙擊手，並拉上可可安撫兩\n人", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n067 [label="第三方隱匿人員持步槍逼近，意\n圖殺人，被擊殺", shape="box", style="filled,rounded", fillcolor="#FFEDD5", color="#EA580C", penwidth="2.0"];
    n068 [label="傭兵無隊伍標識，用北美流通槍\n械，行動模式屬前駐軍", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n069 [label="上層堅持派兩隊，並傾向把上次\n失敗歸為人為失誤", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n070 [label="第三方使用不同無線電頻道，資\n料庫無此人紀錄", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n071 [label="行李袋文件：所有公主的情報、\n監視紀錄、行動計劃與事後報告\n，金澤同事已核實", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n072 [label="諾愛爾與可伶幾乎在入境當刻就\n被監視", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n073 [label="鎮靜劑對人魚提早失效", shape="note", style="filled", fillcolor="#DBEAFE", color="#2563EB", penwidth="2.0"];
    n074 [label="第三方與要活口的傭兵不是一夥\n，局面至少是三方混戰", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n075 [label="委託人知道公主的真實身分，否\n則沒有委託動機", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n076 [label="傭兵背後有掌握所有公主行蹤的\n情報源", shape="box", style="filled,dashed", fillcolor="#EDE9FE", color="#7C3AED", penwidth="1.2"];
    n077 [label="傭兵真正僱主；「寶物」的吸引\n力；與 V 的關係", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
    n078 [label="傭兵為何知道星羅存在", shape="octagon", style="filled,dashed", fillcolor="#F1F5F9", color="#64748B", penwidth="1.2"];
  }

  n001 -> n002 [color="#94A3B8", style="dotted", arrowhead="none"];
  n001 -> n003 [color="#94A3B8", style="dotted", arrowhead="none"];
  n001 -> n005 [color="#94A3B8", style="dotted", arrowhead="none"];
  n001 -> n006 [color="#94A3B8", style="dotted", arrowhead="none"];
  n002 -> n004 [color="#1F2937"];
  n002 -> n014 [color="#1F2937"];
  n004 -> n008 [color="#1F2937"];
  n008 -> n011 [color="#1F2937", style="dashed"];
  n008 -> n012 [color="#1F2937"];
  n003 -> n007 [color="#1F2937"];
  n005 -> n009 [color="#1F2937"];
  n005 -> n010 [color="#1F2937"];
  n002 -> n013 [color="#EA580C"];
  n013 -> n015 [color="#94A3B8", style="dotted", arrowhead="none"];
  n013 -> n017 [color="#94A3B8", style="dotted", arrowhead="none"];
  n013 -> n020 [color="#94A3B8", style="dotted", arrowhead="none"];
  n013 -> n016 [color="#94A3B8", style="dotted", arrowhead="none"];
  n015 -> n019 [color="#1F2937"];
  n017 -> n018 [color="#1F2937"];
  n017 -> n019 [color="#1F2937"];
  n017 -> n032 [color="#1F2937"];
  n018 -> n030 [color="#1F2937"];
  n019 -> n030 [color="#1F2937"];
  n020 -> n021 [color="#EA580C"];
  n020 -> n026 [color="#1F2937"];
  n026 -> n034 [color="#1F2937", style="dashed"];
  n021 -> n022 [color="#EA580C"];
  n022 -> n023 [color="#EA580C"];
  n023 -> n033 [color="#1F2937", style="dashed"];
  n023 -> n024 [color="#94A3B8", style="dotted", arrowhead="none"];
  n023 -> n025 [color="#94A3B8", style="dotted", arrowhead="none"];
  n024 -> n027 [color="#1F2937"];
  n025 -> n027 [color="#1F2937"];
  n025 -> n028 [color="#1F2937"];
  n017 -> n029 [color="#1F2937"];
  n023 -> n029 [color="#1F2937"];
  n014 -> n031 [color="#1F2937"];
  n024 -> n035 [color="#94A3B8", style="dotted", arrowhead="none"];
  n024 -> n036 [color="#94A3B8", style="dotted", arrowhead="none"];
  n024 -> n037 [color="#94A3B8", style="dotted", arrowhead="none"];
  n024 -> n038 [color="#94A3B8", style="dotted", arrowhead="none"];
  n038 -> n010 [color="#1F2937"];
  n035 -> n039 [color="#1F2937"];
  n035 -> n040 [color="#1F2937"];
  n035 -> n043 [color="#1F2937"];
  n036 -> n041 [color="#1F2937"];
  n021 -> n042 [color="#1F2937"];
  n036 -> n042 [color="#1F2937"];
  n031 -> n042 [color="#1F2937"];
  n042 -> n044 [color="#1F2937", style="dashed"];
  n037 -> n045 [color="#1F2937", style="dashed"];
  n026 -> n043 [color="#1F2937"];
  n042 -> n046 [color="#EA580C"];
  n036 -> n046 [color="#94A3B8", style="dotted"];
  n046 -> n047 [color="#EA580C"];
  n047 -> n048 [color="#EA580C"];
  n047 -> n049 [color="#94A3B8", style="dotted", arrowhead="none"];
  n047 -> n050 [color="#94A3B8", style="dotted", arrowhead="none"];
  n047 -> n051 [color="#94A3B8", style="dotted", arrowhead="none"];
  n047 -> n052 [color="#94A3B8", style="dotted", arrowhead="none"];
  n047 -> n055 [color="#94A3B8", style="dotted", arrowhead="none"];
  n051 -> n056 [color="#1F2937"];
  n049 -> n056 [color="#1F2937"];
  n052 -> n058 [color="#1F2937"];
  n047 -> n057 [color="#1F2937"];
  n053 -> n059 [color="#1F2937"];
  n054 -> n059 [color="#1F2937"];
  n059 -> n060 [color="#1F2937", style="dashed"];
  n047 -> n060 [color="#1F2937", style="dashed"];
  n051 -> n061 [color="#1F2937", style="dashed"];
  n048 -> n062 [color="#1F2937", style="dashed"];
  n044 -> n060 [color="#1F2937"];
  n062 -> n063 [color="#EA580C"];
  n048 -> n063 [color="#94A3B8", style="dotted"];
  n063 -> n064 [color="#EA580C"];
  n064 -> n072 [color="#EA580C"];
  n064 -> n065 [color="#EA580C"];
  n065 -> n066 [color="#EA580C"];
  n065 -> n067 [color="#EA580C"];
  n065 -> n068 [color="#94A3B8", style="dotted", arrowhead="none"];
  n065 -> n069 [color="#94A3B8", style="dotted", arrowhead="none"];
  n065 -> n073 [color="#94A3B8", style="dotted", arrowhead="none"];
  n066 -> n071 [color="#94A3B8", style="dotted", arrowhead="none"];
  n067 -> n070 [color="#94A3B8", style="dotted", arrowhead="none"];
  n070 -> n074 [color="#1F2937"];
  n071 -> n076 [color="#1F2937"];
  n071 -> n072 [color="#1F2937"];
  n076 -> n075 [color="#1F2937"];
  n063 -> n078 [color="#1F2937", style="dashed"];
  n078 -> n076 [color="#1F2937"];
  n075 -> n077 [color="#1F2937", style="dashed"];
  n074 -> n077 [color="#1F2937", style="dashed"];
  n048 -> n079 [color="#1F2937"];
  n036 -> n079 [color="#1F2937"];
  n062 -> n081 [color="#1F2937"];
  n045 -> n081 [color="#1F2937"];
  n081 -> n080 [color="#1F2937"];
  n077 -> n080 [color="#1F2937"];
  n078 -> n080 [color="#1F2937"];
  n039 -> n082 [color="#1F2937"];
  n080 -> n083 [color="#DC2626", arrowhead="tee", penwidth="1.6"];
  n079 -> n083 [color="#DC2626", arrowhead="tee", penwidth="1.6"];

  // 時序帶：@時點 相同的節點同層；帶與帶之間只約束先後
  time_00 [shape="plaintext", label="@2004-02-22", fontsize="8", fontcolor="#94A3B8"];
  { rank=same; time_00; n001; }
  time_01 [shape="plaintext", label="@2004-02-25", fontsize="8", fontcolor="#94A3B8"];
  { rank=same; time_01; n013; }
  time_02 [shape="plaintext", label="@2004-04-05", fontsize="8", fontcolor="#94A3B8"];
  { rank=same; time_02; n046; n047; }
  time_03 [shape="plaintext", label="@2004-04-06", fontsize="8", fontcolor="#94A3B8"];
  { rank=same; time_03; n063; }
  time_04 [shape="plaintext", label="@2004-04-15", fontsize="8", fontcolor="#94A3B8"];
  { rank=same; time_04; n065; }
  time_00 -> time_01 [style="invis", weight="50", minlen="2"];
  time_01 -> time_02 [style="invis", weight="50", minlen="2"];
  time_02 -> time_03 [style="invis", weight="50", minlen="2"];
  time_03 -> time_04 [style="invis", weight="50", minlen="2"];
}
```
