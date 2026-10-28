```{=html}
<%
// Notes list, used on the Notes pages and (shortened) on the home page.
// templateParams.home: on the home page the section, heading included, only appears once a
// note is published.
const p = templateParams || {};
const cs = p.lang === 'cs';
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const months = cs ? ['ledna','února','března','dubna','května','června','července','srpna','září','října','listopadu','prosince']
                  : ['January','February','March','April','May','June','July','August','September','October','November','December'];
const fmt = (d) => {
  const x = new Date(d);
  if (isNaN(x)) return esc(d);
  return cs ? `${x.getUTCDate()}. ${months[x.getUTCMonth()]} ${x.getUTCFullYear()}` : `${x.getUTCDate()} ${months[x.getUTCMonth()]} ${x.getUTCFullYear()}`;
};
const iso = (d) => { const x = new Date(d); return isNaN(x) ? '' : x.toISOString().slice(0, 10); };
%>
<% if (items.length && p.home) { %>
<div class="section-head">
  <h2><%- cs ? 'Nejnovější poznámky' : 'Latest notes' %></h2>
  <a href="<%- cs ? 'notes.html' : 'notes/index.html' %>"><%- cs ? 'Všechny poznámky →' : 'All notes →' %></a>
</div>
<% } %>
<% if (items.length) { %>
<ul class="note-list list">
<% for (const it of items) { %>
  <li class="note-item" <%= metadataAttrs(it) %>>
    <time class="note-date" datetime="<%- iso(it.date) %>"><%- fmt(it.date) %></time>
    <div>
      <h3 class="note-title"><a href="<%- it.path %>"><%= esc(it.title) %></a></h3>
      <% if (it.description) { %><p class="note-desc"><%= esc(it.description) %></p><% } %>
    </div>
  </li>
<% } %>
</ul>
<div class="listing-no-matching d-none"><%- cs ? 'Žádná poznámka k tomuto tématu.' : 'No notes on this topic yet.' %></div>
<% } else if (p.home) { %>
<ul class="list" hidden></ul>
<% } else { %>
<p class="empty-state"><%- cs ? 'První poznámky a komentáře se tu brzy objeví.' : 'The first notes and commentaries will appear here soon.' %></p>
<ul class="list" hidden></ul>
<% } %>
```
