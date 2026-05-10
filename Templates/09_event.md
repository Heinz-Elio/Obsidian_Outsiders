<%*
const data = {}

data.title = await tp.system.prompt("name") || "Unknown";
data.id = `event_${data.name_en.toLowerCase()}`

data.timeline = await tp.system.suggester(
  ["iu0", "iu7"],
  ["iu0", "iu7"]
);
data.era = await tp.system.suggester(
  ["very old", "present"],
  ["very old", "present"]
);
tp.system.prompt("time") || "0000-00-00";
data.isAccurate = await tp.system.suggester(["accurate","range"],[true,false]);
data.precision = await tp.system.suggester(
  ["era", "year", "month", "day"],
  ["era", "year", "month", "day"]
);
-%>
---
type: event
id: <% data.id %>
title: <% data.name_en %>
timeline: <% data.timeline %>
era: <% data.era %>

<%* if (data.isAccurate) { -%>
date:
<%* } else { -%>
start_date: <% data.time %>
end_date: 
<%* } -%>
precision: <% data.precision %>
organization: 
- [[]]

---
#
## 簡介

## 關聯事件
- [[]]