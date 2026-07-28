<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
let prefix = data.name_en.toLowerCase()
let id = await tp.system.prompt("id") || "001";
data.id = `loc_${prefix}_${id}`

data.subtype = await tp.system.suggester(
  ["city", "building, natural"],
  ["city", "building, natural"]
);

data.isUnderwater = await tp.system.suggester(["underwater","no"],[true,false]);

data.isRuin = await tp.system.suggester(["ruin","no"],[true,false]);
-%>
---
type: location
id: <% data.id %>
name_en: <% data.name_en %>
subtype: <% data.subtype %>
underwater: <% data.isUnderwater %>
ruin: <% data.isRuin %>

---
# 
<% data.name_en %>

---
位置: 
所屬: [[]]
<%* if (data.isUnderwater) { -%>
深度: 約米
<%* } -%>
<%* if (data.subtype === "city") { -%>
人口: 
<%* } -%>

---
## 簡介

