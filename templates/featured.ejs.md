```{=html}
<%
// "Selected work" cards on the home page (entries with featured: true).
const p = templateParams || {};
const cs = p.lang === 'cs';
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const withLine = (it) => {
  const w = it.coauthors_display || '';
  if (!cs || !w) return w;
  return 'Spoluautoři: ' + w.replace(/^with /, '').replace(/ and (\d+) others$/, ' a dalších $1').replace(/ and /g, ' a ');
};
const sorted = items.slice().sort((a, b) => (b.year || 0) - (a.year || 0));
%>
<% if (sorted.length) { %>
<ul class="card-grid list">
<% for (const it of sorted) { const url = it.doi ? 'https://doi.org/' + it.doi : (it.url || ''); %>
  <li class="card-pub" <%= metadataAttrs(it) %>>
    <span class="venue"><%= esc(it.journal) %> · <%- it.status === 'forthcoming' ? (cs ? 'v tisku' : 'forthcoming') : it.year %></span>
    <h3 class="card-title"><a href="<%= esc(url) %>"><%= esc(it.title) %></a></h3>
    <% if (withLine(it)) { %><p class="with"><%= esc(withLine(it)) %></p><% } %>
  </li>
<% } %>
</ul>
<% } %>
```
