// Shared across pages — single source of truth for nav/social links.
const SITE = {
  name: "Astro Poet",
  tagline: "for the restless seekers",
  author: "Mohammed Saqib",
  social: [
    { label: "Medium", url: "https://medium.com/@mohammedsaqibukn" },
    { label: "Substack", url: "https://substack.com/@astropoet1" },
    { label: "Wattpad", url: "https://www.wattpad.com/user/_Astro_Poet_" },
  ],
};

function renderNav(active) {
  const links = [
    { label: "Poems", href: "index.html" },
  ];
  return `
    <nav class="site-nav">
      <a class="wordmark" href="index.html">ASTRO<span>·</span>POET</a>
      <div class="nav-links">
        ${links.map(l => `<a href="${l.href}"${active === l.href ? ' aria-current="page"' : ''}>${l.label}</a>`).join('')}
        ${SITE.social.map(s => `<a href="${s.url}" target="_blank" rel="noopener">${s.label}</a>`).join('')}
      </div>
    </nav>`;
}

function renderFooter() {
  const year = new Date().getFullYear();
  return `
    <footer class="site-footer">
      <span>&copy; ${year} ${SITE.author}. Words kept, not sold.</span>
      <div class="footer-links">
        ${SITE.social.map(s => `<a href="${s.url}" target="_blank" rel="noopener">${s.label}</a>`).join('')}
      </div>
    </footer>`;
}
