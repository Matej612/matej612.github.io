```{=html}
<%
// Topic filter chips. Quarto's listing script wires up every
// `.quarto-listing-category .category` element and filters all listings on the page.
const p = templateParams || {};
const cs = p.lang === 'cs';
const names = p.labels || {};
const counts = {};
for (const it of items) for (const c of (it.categories || [])) counts[c] = (counts[c] || 0) + 1;
const cats = Object.keys(counts).sort((a, b) => counts[b] - counts[a] || a.localeCompare(b));
%>
<div class="topic-bar quarto-listing-category" role="group" aria-label="<%- cs ? 'Filtrovat podle tématu' : 'Filter by topic' %>">
  <span class="topic-label"><%- cs ? 'Filtrovat podle tématu' : 'Filter by topic' %></span>
  <button type="button" class="category active" data-category="" aria-pressed="true"><%- cs ? 'Vše' : 'All' %><span class="n"><%- items.length %></span></button>
<% for (const c of cats) { %>
  <button type="button" class="category" data-category="<%- utils.b64encode(c) %>" aria-pressed="false"><%- names[c] || c %><span class="n"><%- counts[c] %></span></button>
<% } %>
</div>
<ul class="list" hidden></ul>
```
