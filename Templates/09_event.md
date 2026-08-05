<%*
const data = {}

data.title = await tp.system.prompt("name") || "Unknown";
data.subtype = await tp.system.suggester(
  ["backstory", "history", "plot"],
  ["backstory", "history", "plot"]
);

data.timeline = await tp.system.suggester(
  ["iu0", "iu7"],
  ["iu0", "iu7"]
);

data.id = `event_${data.subtype}_${data.title}`
-%>
---
type: event
id: <% data.id %>
sub_type: <% data.subtype %>
timeline: <% data.timeline %>
involved:
- 
start_date: 
end_date: 
location: 
- 
prev:
- 
next:
- 

---
# <% data.title %>

---

