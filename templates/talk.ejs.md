```{=html}
<%
// Conference and seminar presentations from data/talks.yml, grouped by year.
const p = templateParams || {};
const cs = p.lang === 'cs';
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const mon = cs ? ['led','úno','bře','dub','kvě','čvn','čvc','srp','zář','říj','lis','pro']
               : ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const withLine = (list) => {
  const xs = (list || []).filter(Boolean);
  if (!xs.length) return '';
  const etal = xs[xs.length - 1] === 'et al.';
  const names = etal ? xs.slice(0, -1) : xs;
  const and = cs ? ' a ' : ' and ';
  const joined = names.length > 1 ? names.slice(0, -1).join(', ') + and + names[names.length - 1] : names[0];
  return (cs ? 'Spoluautoři: ' : 'with ') + joined + (etal ? (cs ? ' a kol.' : ' et al.') : '');
};
const role = { invited: cs ? 'zvaná přednáška' : 'invited talk', discussant: cs ? 'diskutující' : 'discussant' };
const sorted = items.filter((it) => it.visible).sort((a, b) => String(b.month).localeCompare(String(a.month)));
let year = null;
%>
<div class="list">
<% for (const it of sorted) {
     const [y, m] = String(it.month).split('-');
     if (y !== year) { if (year !== null) { %></ul><% } year = y; %>
<p class="talk-year"><%- y %></p>
<ul class="timeline">
<% } %>
  <li <%= metadataAttrs(it) %>>
    <span class="when"><%- mon[Number(m) - 1] %> <%- y %></span>
    <div>
      <div class="talk-title" lang="en"><%- esc(it.title) %></div>
      <div class="where"><%- esc(it.event) %> · <%- esc(cs ? (it.place_cs || it.place) : it.place) %><% if (role[it.role]) { %> · <%- role[it.role] %><% } %></div>
      <% if (withLine(it.coauthors)) { %><div class="note"><%- esc(withLine(it.coauthors)) %></div><% } %>
    </div>
  </li>
<% } %>
<% if (year !== null) { %></ul><% } %>
</div>
```
