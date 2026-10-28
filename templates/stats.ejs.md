```{=html}
<%
// The numbers under the home-page hero (six tiles, three per row). The tiles come from
// template-params in index.qmd / cs/index.qmd; "value: articles" is replaced by the number of
// visible published or forthcoming journal articles in data/publications.yml, so it stays current
// by itself. Citations and h-index are copied by hand from Google Scholar, with the month.
// "unit" is a word, or a list of plural forms: [one, many] in English, [1, 2–4, 5+] in Czech.
const p = templateParams || {};
const cs = p.lang === 'cs';
const articles = items.filter((it) => it.visible && it.type === 'article'
  && (it.status === 'published' || it.status === 'forthcoming')).length;
const plural = (n, unit) => {
  if (!Array.isArray(unit)) return unit;
  if (n === 1) return unit[0];
  if (cs && unit.length > 2 && n >= 2 && n <= 4) return unit[1];
  return unit[unit.length - 1];
};
const tiles = (p.tiles || []).map((t) => {
  const n = t.value === 'articles' ? articles : t.value;
  return { n, unit: plural(Number(n), t.unit), label: t.label };
});
%>
<ul class="stat-grid list">
<% for (const t of tiles) { %>
  <li class="stat">
    <span class="stat-value"><%- t.n %><span class="stat-unit"><%- t.unit %></span></span>
    <span class="stat-label"><%- t.label %></span>
  </li>
<% } %>
</ul>
```
