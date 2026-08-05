<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
data.id = `org_${data.name_en.toLowerCase()}`

data.subtype = await tp.system.suggester(
  ["kingdom", "political", "military", "business", "research"],
  ["kingdom", "political", "military", "business", "research"]
);
-%>
---
type: organization
id: <% data.id %>
name_en: <% data.name_en %>
subtype: <% data.subtype %>

---
# 

<% data.name_en %>

---
上級單位: [[]]
下級單位: [[]]
領導人: [[]]
<%* if (data.subtype === "kingdom") { -%>
大長老: [[]]
代表色:
<%* } -%>
成員: 
- [[]]

---
## 簡介

<%* if (data.subtype === "military") { -%>
## 編制


### 階級


## 裝備


## 載具


<%* } -%>