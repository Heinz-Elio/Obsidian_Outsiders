<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
data.id = `lang_${data.name_en.toLowerCase()}`
-%>
---
type: language
id: <% data.id %>
name_en: <% data.name_en %>

---
# 
<% data.name_en %>

---
發明: [[]]
使用: [[]]

---
## 簡介
