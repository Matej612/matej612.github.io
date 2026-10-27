```{=html}
<%
// One research section in the Robert E. Hall style:
//   Title (linked) / with co-authors / Journal, Vol(Issue), pages / [DOI] [PDF] [Data] [Code] … [Abstract]
// templateParams: lang (en|cs), heading, anchor, order (status|year)
const p = templateParams || {};
const cs = p.lang === 'cs';
const T = cs ? {
  ur: 'V recenzním řízení', rr: 'Revize a nové podání', wip: 'Rozpracováno', fc: 'V tisku',
  article: 'článek', no: 'č.', abstract: 'Abstrakt', none: 'V této části nic neodpovídá zvolenému tématu.',
  links: { pdf: 'PDF', data: 'Data', code: 'Kód', slides: 'Prezentace', video: 'Video', ssrn: 'SSRN', repec: 'RePEc', media: 'Média' },
} : {
  ur: 'Under review', rr: 'Revise & resubmit', wip: 'Work in progress', fc: 'Forthcoming',
  article: 'Article', no: 'No.', abstract: 'Abstract', none: 'Nothing in this section matches the selected topic.',
  links: { pdf: 'PDF', data: 'Data', code: 'Code', slides: 'Slides', video: 'Video', ssrn: 'SSRN', repec: 'RePEc', media: 'Media' },
};
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const dash = (s) => String(s ?? '').replace(/-/g, '–');
const withLine = (it) => {
  const w = it.coauthors_display || '';
  if (!cs || !w) return w;
  return 'Spoluautoři: ' + w.replace(/^with /, '').replace(/ and (\d+) others$/, ' a dalších $1').replace(/ and /g, ' a ');
};
const href = (it) => it.doi ? 'https://doi.org/' + it.doi : (it.url || (it.links && it.links.pdf) || '');
const venue = (it) => {
  const j = it.journal ? `<em>${esc(it.journal)}</em>` : '';
  if (it.status === 'under_review') return `<span class="badge-status">${T.ur}</span>${j ? ' ' + j : ''}`;
  if (it.status === 'rr') return `<span class="badge-status">${T.rr}</span>${j ? ' ' + j : ''}`;
  if (it.status === 'forthcoming') return `${j} <span class="badge-status is-forthcoming">${T.fc}</span>`;
  if (it.type === 'working_paper') return j ? `${j}${it.issue ? ' ' + T.no + ' ' + esc(it.issue) : ''}` : `<span class="badge-status is-wip">${T.wip}</span>`;
  const parts = [j];
  if (it.volume) parts.push(esc(it.volume) + (it.issue ? `(${esc(it.issue)})` : ''));
  if (it.pages) parts.push(dash(it.pages));
  else if (it.article_number) parts.push(`${T.article} ${esc(it.article_number)}`);
  return parts.filter(Boolean).join(', ');
};
const rank = { forthcoming: 0, rr: 1, under_review: 2, wip: 3, published: 4 };
const sorted = items.slice().sort((a, b) =>
  (p.order === 'status' ? (rank[a.status] ?? 9) - (rank[b.status] ?? 9) : 0) ||
  (b.year || 0) - (a.year || 0) || String(a.title).localeCompare(String(b.title)));
%>
<% if (sorted.length) { %>
<section class="pub-section" id="<%- p.anchor || '' %>">
<h2><%- p.heading || '' %><span class="count"><%- sorted.length %></span></h2>
<ul class="pub-list list">
<% for (const it of sorted) { const url = href(it); const links = it.links || {}; %>
  <li class="pub" <%= metadataAttrs(it) %>>
    <div class="pub-year"><%- it.status === 'forthcoming' ? (cs ? 'V tisku' : 'In press') : (it.year || '') %></div>
    <div class="pub-body">
      <h3 class="pub-title"><% if (url) { %><a href="<%= esc(url) %>"><%= esc(it.title) %></a><% } else { %><%= esc(it.title) %><% } %></h3>
      <% if (withLine(it)) { %><p class="pub-with"><%= esc(withLine(it)) %></p><% } %>
      <p class="pub-venue"><%= venue(it) %></p>
      <div class="pub-links">
        <% if (it.doi) { %><a class="pill" href="https://doi.org/<%= esc(it.doi) %>" aria-label="DOI <%= esc(it.doi) %>">DOI</a><% } %>
        <% for (const k of ['pdf', 'data', 'code', 'slides', 'video', 'ssrn', 'repec', 'media']) { if (links[k]) { %>
        <a class="pill" href="<%= esc(links[k]) %>"><%- T.links[k] %></a>
        <% } } %>
        <% if (it.abstract) { %>
        <details class="abstract">
          <summary class="pill"><%- T.abstract %></summary>
          <div class="abstract-body" lang="en"><%= esc(it.abstract) %></div>
        </details>
        <% } %>
      </div>
    </div>
  </li>
<% } %>
</ul>
<div class="listing-no-matching d-none"><%- T.none %></div>
</section>
<% } %>
```
