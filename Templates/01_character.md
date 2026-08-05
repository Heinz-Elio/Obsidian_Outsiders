<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
const prefix = data.name_en.split(" ")[0].toLowerCase();

let idx = await tp.system.prompt("id") || "001";
idx = String(idx).padStart(3, "0");

data.id = `${prefix}_${idx}`;

data.importance = await tp.system.suggester(
  ["main", "important", "normal"],
  ["main", "important", "normal"]
);

data.entity_type = await tp.system.suggester(
  ["outsider", "blueprint", "normal"],
  ["outsider", "blueprint", "normal"]
);

data.isAlive = await tp.system.suggester(["alive","dead"],[true,false]);
data.isRanger = await tp.system.suggester(["ranger","no"],[true,false]);
data.isMilitary = await tp.system.suggester(["military","no"],[true,false]);
data.isCombat_eq = await tp.system.suggester(["combat_eq","no"],[true,false]);
data.isSrune = await tp.system.suggester(["srune","no"],[true,false]);

-%>
---
type: character
id: <% data.id %>
importance: <% data.importance %>
name_en: <% data.name_en %>
entity_type: <% data.entity_type %>
alive: <% data.isAlive %>
ranger: <% data.isRanger %>
military: <% data.isMilitary %>
have_combat_eq: <% data.isCombat_eq %>
process_srune: <% data.isSrune %>

---
# 

 | <% data.name_en %>
 
## 無

---
## 基本資訊

種族: 
國籍: 
<%* if (data.importance !== "normal") { -%>
身高: 公分
體重: 公斤
出生: 年月日 | 
<%* if (!data.isAlive) { -%>
逝世: 年月日 | 
<%* } -%>
<%* } -%>
<%* if (data.entity_type === "outsider") { -%>

---
## 相對合理存在

名字: |
出生: 年月日 | 
國籍: 
身份: 

### 簡介

<%* } -%>
<%* if (data.entity_type === "blueprint") { -%>

---
## 藍圖

所屬藍圖: 
代號: 
身份: 

### 簡介

<%* } -%>
<%* if (data.isRanger) { -%>

---
## 游騎士檔案

編號: R
職級: 等級
單位:
代號:
<%* } -%>
<%* if (data.isMilitary) { -%>

---
## 軍事檔案

所屬: 
職級: 
單位: 
職務: 
<%* } -%>

---
## 關係


- [[]] #
---
<%* if (data.importance !== "main") { -%>
## 簡介


<%* } else { -%>
## 外貌

## 性格


## 習慣與喜好


---
## 經歷

### 童年


### 青年


<%* } -%>
<%* if (data.entity_type === "outsider") { -%>

---
## 修正力結構

能力名稱:
散逸類別:
特性:

## 修正力術式

|     |     |
| --- | --- |
|     |     |
<%* } -%>
<%* if (data.isCombat_eq){ -%>

---
## 戰鬥

### 風格



### 裝備

| 類別  | 型號  | 數量  |
| --- | --- | --- |
| 護目鏡 |     |     |
| 戰鬥服 |     |     |
| 戰鬥褲 |     |     |
| 戰鬥靴 |     |     |
| 手套  |     |     |
<%* if (data.isSrune){ -%>

---
## 法術

- [[]]
<%* } -%>
<%* } -%>

---
## 事件

- [[ ]]