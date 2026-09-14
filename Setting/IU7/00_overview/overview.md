## Outsiders

```dataview
TABLE alive, ranger, military, process_srune
FROM "Setting/IU7/01_character" // full path
WHERE entity_type = "outsider" 
```
## Rangers

```dataview
TABLE entity_type
FROM "Setting/IU7/01_character" // full path
WHERE ranger = true 
```
## Dead

```dataview
TABLE entity_type,alive 
FROM "Setting/IU7/01_character" // full path
WHERE alive = false 
```
## Military

```dataview
TABLE entity_type
FROM "Setting/IU7/01_character" // full path
WHERE military = true 
```
## Srune

```dataview
TABLE entity_type
FROM "Setting/IU7/01_character" // full path
WHERE process_srune = true 
```
## Kingdom

```dataview
TABLE type, subtype
FROM "Setting/IU7/08_organization" // full path
WHERE subtype = "kingdom" 
```

## IU7 科技與物品演進

> 實線代表前置技術或直接派生；虛線代表使用、替代或關聯。年份以各文件現有欄位為準，標示「年份待補」的項目尚未在文件中記載明確年份。

```mermaid
flowchart LR
    subgraph era_early["早期／1960年代"]
        w_kao["北冰洋制式弩<br/>武器｜數百年前（近似）"]
        w_sa68["克洛克斯蒂爾 SA 68 法力弩<br/>武器｜投產 1968年"]
        w_sscg69["克洛克斯蒂爾 SSCG 69 複合狙擊步槍<br/>武器｜投產 1969年"]
    end

    subgraph era_1970["1970年代"]
        w_m2["M2法力弩<br/>武器｜1972年"]
        w_m3["M3狙擊用法力弩<br/>武器｜1973年"]
        t_compress["壓縮法力發射<br/>技術｜1979年"]
    end

    subgraph era_1980["1980年代"]
        w_ulsa["克洛克斯蒂爾 ULSA 82 超輕法力弩<br/>武器｜投產 1982年"]
        w_m5["M5法力步槍<br/>武器｜1983年"]
        a_bm1["BM-1水中用子彈<br/>彈藥｜1983年"]
        a_bm3["BM-3壓縮法力彈<br/>彈藥｜1984年"]
        w_m4a["M4A 60毫米壓縮法力砲<br/>武器｜1985年"]
        a_60mm["60毫米蝕刻彈<br/>彈藥｜1985年"]
        w_m5a1["M5A1法力狙擊步槍<br/>武器｜1987年"]
        a_bm2["BM-2法力助推彈<br/>彈藥｜1987年"]
    end

    subgraph era_2000["2000年代"]
        i_chip["小型紀錄晶片<br/>工具｜2001年"]
        w_hcsa["HCSA-1「守護神」超高壓縮法力砲<br/>武器｜2002年"]
        i_drone["Kafziel自製四軸偵察無人機<br/>工具｜2002年"]
        w_sscg04["克洛克斯蒂爾 SSCG 04 複合狙擊步槍<br/>武器｜2004年"]
    end

    subgraph pending["年代待補／其他項目"]
        t_etch["蝕刻彈<br/>技術／彈藥基礎｜年份待補"]
        t_encrypt["法力加密通訊協定<br/>技術｜年份待補"]
        t_defeat["去特徵化<br/>技術｜年份待補"]
        i_crystal["晶核<br/>材料｜年份待補"]
        i_evum["艾方合金<br/>材料｜年份待補"]
        i_fpsa["可現場編程法力邏輯陣列<br/>材料｜年份待補"]
        i_sec["基質能-能量轉換器<br/>機器｜年份待補"]
        i_smc["基質能-物質轉換器<br/>機器｜年份待補"]
        i_soul["靈池<br/>機器｜年代待補"]
        i_seccs["法力加密戰鬥通訊系統<br/>機器｜年份待補"]
        i_ct1["CT-1 SMC工程船<br/>機器｜年份待補"]
        i_record["紀錄節點<br/>工具｜千萬年前"]
        i_interactive["可互動紀錄板<br/>工具｜年份待補"]
        i_portable["便攜法術媒介<br/>工具｜年份待補"]
        i_universal["萬用晶核棒<br/>工具｜年份待補"]
        i_mermaid["美人魚占卜卡牌<br/>工具｜年份待補"]
        w_csmg["CSMG-2六聯裝壓縮法力機砲<br/>武器｜年份待補"]
        w_lcsa["LCSA-4「劍魚」三聯裝壓縮法力砲<br/>武器｜年份待補"]
        w_psml["PSML-5「逐火」單兵法力導彈發射器<br/>武器｜年份待補"]
        w_m1["M1晶核軍刀<br/>武器｜年份待補"]
        w_spear["晶核長槍<br/>武器｜年份待補"]
        w_sscg69e["克洛克斯蒂爾 SSCG 69E 複合狙擊步槍<br/>武器｜年份待補"]
    end

    w_kao -.->|被 M2 取代／採購替換| w_m2
    w_sa68 -.->|替代需求| w_m2
    w_sa68 --> w_ulsa
    w_sscg69 --> w_sscg69e
    w_m2 --> w_m3
    w_m2 --> t_compress

    t_etch --> a_60mm
    t_compress --> w_m5
    t_compress --> w_m4a
    t_compress --> w_csmg
    t_compress --> w_lcsa
    t_compress --> w_hcsa
    t_compress --> a_60mm
    t_compress --> a_bm2
    t_compress --> a_bm3

    w_m5 --> w_m5a1
    a_bm1 -.->|改良型| a_bm2
    a_60mm -.->|小型化／技術沿用| a_bm2
    w_m4a -.->|使用| a_60mm
    w_m4a -.->|助推器小型化來源| a_bm2
    a_bm2 -.->|專用彈藥| w_m5a1
    w_m5 -.->|可用彈藥| a_bm1

    i_evum --> i_portable
    i_evum --> w_sscg69e
    i_portable -.->|固定架設| w_m4a
    i_portable -.->|固定底座| w_csmg

    i_crystal --> w_spear
    i_crystal --> w_m1
    i_crystal --> i_universal
    i_sec -.->|高級型號可搭載| w_spear

    i_record --> i_interactive
    i_record --> i_chip
    i_smc --> i_ct1
    t_encrypt -.->|最高級別加密| i_seccs
    t_defeat -.->|實例| i_soul
    t_defeat -.->|關聯技術| t_compress

    classDef technology fill:#2563eb,color:#ffffff,stroke:#1e3a8a
    classDef material fill:#d97706,color:#ffffff,stroke:#92400e
    classDef weapon fill:#b91c1c,color:#ffffff,stroke:#7f1d1d
    classDef ammunition fill:#7c3aed,color:#ffffff,stroke:#4c1d95
    classDef tool fill:#059669,color:#ffffff,stroke:#064e3b
    classDef machine fill:#0891b2,color:#ffffff,stroke:#164e63

    class t_compress,t_etch,t_encrypt,t_defeat technology
    class i_crystal,i_evum,i_fpsa material
    class w_kao,w_sa68,w_sscg69,w_m2,w_m3,w_ulsa,w_m5,w_m4a,w_m5a1,w_hcsa,w_csmg,w_lcsa,w_psml,w_m1,w_spear,w_sscg69e,w_sscg04 weapon
    class a_bm1,a_bm2,a_bm3,a_60mm ammunition
    class i_record,i_interactive,i_chip,i_portable,i_universal,i_mermaid,i_drone tool
    class i_sec,i_smc,i_soul,i_seccs,i_ct1 machine
```








