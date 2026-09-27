/* Compatibility only; content and navigation do not depend on JavaScript. */
(() => {
  const routes = {
    work: 'research.html', team: 'people.html', papers: 'publications.html',
    news: 'news.html', funding: 'funding.html'
  };
  function followLegacyLink() {
    const destination = routes[location.hash.slice(1)];
    if (destination) location.replace(destination);
  }
  window.addEventListener('hashchange', followLegacyLink);
  followLegacyLink();
})();
