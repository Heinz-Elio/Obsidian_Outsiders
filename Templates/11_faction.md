<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
data.id = `org_${data.name_en.toLowerCase()}`
-%>
---
type: faction
id: <% data.id %>
name_en: <% data.name_en %>
relation: 
- ally: [[]]
- neutral: [[]]
- enemy: [[]]

---
# 
<% data.name_en %>

---
領導: [[]]
成員: [[]]

---
## 簡介



