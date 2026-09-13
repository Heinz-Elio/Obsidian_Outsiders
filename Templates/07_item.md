<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
data.id = `item_${data.name_en.toLowerCase()}`

data.subtype = await tp.system.suggester(
  ["weapon", "arrow", "ammunition", "tool", "machine", "material"],
  ["weapon", "arrow", "ammunition", "tool", "machine", "material"]
);

data.isNew = await tp.system.suggester(["new","old"],[true,false]);
-%>
---
type: item
id: <% data.id %>
name_en: <% data.name_en %>
subtype: <% data.subtype %>
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

