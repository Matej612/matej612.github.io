```{=html}
<%
// Project cards from data/projects.yml.
const p = templateParams || {};
const cs = p.lang === 'cs';
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const sorted = items.filter((it) => it.visible).sort((a, b) => (b.start || 0) - (a.start || 0));
%>
<ul class="project-list list">
<% for (const it of sorted) {
     const role = cs ? (it.role_cs || it.role_en) : it.role_en;
     const summary = cs ? (it.summary_cs || it.summary_en) : it.summary_en; %>
  <li class="project" id="<%= esc(it.id) %>" <%= metadataAttrs(it) %>>
    <div class="project-head">
      <h2><%= esc(it.name) %></h2>
      <span class="years"><%= esc(String(it.years).replace(/–$/, cs ? '–dosud' : '–present')) %></span>
    </div>
    <% if (role) { %><p class="role"><%= esc(role) %></p><% } %>
    <p class="summary"><%= esc(summary) %></p>
    <% if (it.url) { %><a class="btn-outline" href="<%= esc(it.url) %>"><%- cs ? 'Web projektu' : 'Project website' %> <i class="bi bi-arrow-up-right" aria-hidden="true"></i></a><% } %>
  </li>
<% } %>
</ul>
```
