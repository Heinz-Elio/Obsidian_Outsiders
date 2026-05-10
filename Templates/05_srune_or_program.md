<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
data.id = `srune_${data.name_en.toLowerCase()}`;

data.level = await tp.system.suggester(["system","standalone"],["system","standalone"]);
-%>
---
type: srune
id: <% data.id %>
name_en: <% data.name_en %>
level: <% data.level %>

---
# 
<% data.name_en %>

---
發明: [[]]
<%* if (data.level === "system") { -%>
使用: [[]]
<%* } -%>

---
## 簡介
