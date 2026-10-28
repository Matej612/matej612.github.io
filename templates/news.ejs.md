```{=html}
<%
// News from data/news.yml: "Coming up" (soonest first), then past items (newest first).
// templateParams: lang (en|cs), limit (number of past items; 0 = all), archive (true on the news page).
// The state (upcoming / now / past) is worked out at build time and re-checked in the
// browser by site-script.html, so an old build never shows a past event as upcoming.
const p = templateParams || {};
const cs = p.lang === 'cs';
const limit = Number(p.limit) || 0;
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const str = (v) => (v instanceof Date ? v.toISOString().slice(0, 10) : String(v ?? '').trim());
const pad = (n) => String(n).padStart(2, '0');
const lastDay = (y, m) => new Date(Date.UTC(y, m, 0)).getUTCDate();
const mon = cs ? ['leden','únor','březen','duben','květen','červen','červenec','srpen','září','říjen','listopad','prosinec']
               : ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const kinds = {
  conference:  { icon: 'mic',          en: 'Conference',     cs: 'Konference' },
  talk:        { icon: 'easel',        en: 'Talk',           cs: 'Přednáška' },
  publication: { icon: 'journal-text', en: 'Publication',    cs: 'Publikace' },
  stay:        { icon: 'geo-alt',      en: 'Research stay',  cs: 'Výzkumný pobyt' },
  award:       { icon: 'award',        en: 'Award',          cs: 'Ocenění' },
  policy:      { icon: 'bank',         en: 'Policy',         cs: 'Veřejná politika' },
  outreach:    { icon: 'megaphone',    en: 'Public engagement', cs: 'Popularizace vědy' },
  other:       { icon: 'dot',          en: 'News',           cs: 'Novinka' },
};
const now = new Date();
const today = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;

const label = (a, b) => {
  const [y1, m1, d1] = a.split('-').map(Number);
  if (!b) return d1 ? (cs ? `${d1}. ${m1}. ${y1}` : `${d1} ${mon[m1 - 1]} ${y1}`) : `${mon[m1 - 1]} ${y1}`;
  const [y2, m2, d2] = b.split('-').map(Number);
  if (d1 && d2) {
    if (cs) return y1 === y2 ? (m1 === m2 ? `${d1}.–${d2}. ${m1}. ${y1}` : `${d1}. ${m1}. – ${d2}. ${m2}. ${y1}`)
                             : `${d1}. ${m1}. ${y1} – ${d2}. ${m2}. ${y2}`;
    return y1 === y2 ? (m1 === m2 ? `${d1}–${d2} ${mon[m1 - 1]} ${y1}` : `${d1} ${mon[m1 - 1]} – ${d2} ${mon[m2 - 1]} ${y1}`)
                     : `${d1} ${mon[m1 - 1]} ${y1} – ${d2} ${mon[m2 - 1]} ${y2}`;
  }
  return y1 === y2 ? `${mon[m1 - 1]}–${mon[m2 - 1]} ${y1}` : `${mon[m1 - 1]} ${y1} – ${mon[m2 - 1]} ${y2}`;
};

const all = items.filter((it) => it.visible).map((it) => {
  const start = str(it.start), end = str(it.end);
  const from = start.length === 7 ? `${start}-01` : start;
  const last = end || start;
  const to = last.length === 7 ? `${last}-${pad(lastDay(...last.split('-').map(Number)))}` : last;
  const state = today < from ? 'upcoming' : today <= to ? 'now' : 'past';
  return { it, start, end, from, to, state };
});
const coming = all.filter((x) => x.state !== 'past').sort((a, b) => a.from.localeCompare(b.from));
let past = all.filter((x) => x.state === 'past').sort((a, b) => b.from.localeCompare(a.from));
if (limit) past = past.slice(0, limit);

const row = (x) => {
  const it = x.it;
  const k = kinds[it.kind] || kinds.other;
  const titleCs = cs && it.title_cs;
  const title = esc(titleCs ? it.title_cs : it.title_en);
  const detail = cs ? (it.detail_cs || it.detail_en) : it.detail_en;
  const titleLang = cs && !titleCs ? ' lang="en"' : '';
  return `<li class="news-item" data-from="${x.from}" data-to="${x.to}" ${metadataAttrs(it)}>
    <time class="news-date" datetime="${esc(x.start)}">${label(x.start, x.end)}</time>
    <div class="news-body">
      <p class="news-kind"><i class="bi bi-${k.icon}" aria-hidden="true"></i>${cs ? k.cs : k.en}${x.state === 'now' ? `<span class="news-flag">${cs ? 'Právě probíhá' : 'Now'}</span>` : ''}</p>
      <p class="news-title"${titleLang}>${it.url ? `<a href="${esc(it.url)}">${title}</a>` : title}</p>
      ${detail ? `<p class="news-detail">${esc(detail)}</p>` : ''}
    </div>
  </li>`;
};
%>
<div class="news list" data-limit="<%- limit %>" data-now-label="<%- cs ? 'Právě probíhá' : 'Now' %>">
  <p class="news-group"<%- coming.length ? '' : ' hidden' %>><%- cs ? 'Nadcházející' : 'Coming up' %></p>
  <ul class="news-list" data-group="coming"<%- coming.length ? '' : ' hidden' %>>
<%= coming.map(row).join('\n') %>
  </ul>
  <p class="news-group"<%- past.length ? '' : ' hidden' %>><%- p.archive ? (cs ? 'Proběhlo' : 'Past') : (cs ? 'Nedávno' : 'Recently') %></p>
  <ul class="news-list" data-group="past"<%- past.length ? '' : ' hidden' %>>
<%= past.map(row).join('\n') %>
  </ul>
</div>
```
