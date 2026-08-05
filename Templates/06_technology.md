<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
data.id = `technology_${data.name_en.toLowerCase()}`

data.isNew = await tp.system.suggester(["new","old"],[true,false]);
-%>
---
type: technology
id: <% data.id %>
name_en: <% data.name_en %>
new: <% data.isNew %>

---
# 

<% data.name_en %>

---
<%* if (data.isNew) { -%>
發明者: 
發明時間:
<%* } -%>

---
## 簡介

