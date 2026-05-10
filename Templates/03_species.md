<%*
const data = {}

data.name_en = await tp.system.prompt("name") || "Unknown";
data.id = `species_${data.name_en.toLowerCase()}`;

data.isBranch = await tp.system.suggester(["branch","no"],[true,false]);

data.isExtinct = await tp.system.suggester(["extinct","no"],[true,false]);
-%>
---
type: species
id: <% data.id %>
name_en: <% data.name_en %>
branch: <% data.isBranch %>
extinct: <% data.isExtinct %>

---
# 
<% data.name_en %>

<%* if (data.isBranch)
{ -%>

---
屬於: [[]]
<%* } -%>
<%* if (data.isExtinct)
{ -%>
滅絕時間: 
<%* } -%>

---
## 簡介

## 特徵

## 政治

## 歷史