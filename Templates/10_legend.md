<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
data.id = `legend_${data.name_en.toLowerCase()}`;
-%>
---
type: legend
id: <% data.id %>
name_en: <% data.name_en %>

---
# 
<% data.name_en %>

---
出處: [[]]

---
## 簡介
