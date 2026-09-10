(() => {
  const menuToggle = document.querySelector('.menu-toggle');
  const siteNav = document.querySelector('.site-nav');
  const tabs = document.querySelectorAll('.timeline-tab');
  const panels = document.querySelectorAll('.timeline-panel');
  const progress = document.querySelector('.timeline-progress span');

  function closeMenu() {
    if (!menuToggle || !siteNav) return;
    menuToggle.setAttribute('aria-expanded', 'false');
    siteNav.classList.remove('is-open');
  }

  if (menuToggle && siteNav) {
    menuToggle.addEventListener('click', () => {
      const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!isOpen));
      siteNav.classList.toggle('is-open', !isOpen);
      if (isOpen) menuToggle.focus();
    });

    siteNav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        closeMenu();
        menuToggle.focus();
      }
    });
  }

  if (!tabs.length || !panels.length || !progress) return;

  function selectTimelineItem(tab) {
    const target = tab.dataset.target;
    const activeIndex = [...tabs].indexOf(tab);

    tabs.forEach((item) => {
      const isActive = item === tab;
      item.classList.toggle('is-active', isActive);
      item.setAttribute('aria-selected', String(isActive));
      item.tabIndex = isActive ? 0 : -1;
    });

    panels.forEach((panel) => {
      const isVisible = panel.id === `panel-${target}`;
      panel.hidden = !isVisible;
      panel.classList.toggle('is-visible', isVisible);
    });

    progress.style.width = `${((activeIndex + 1) / tabs.length) * 100}%`;
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTimelineItem(tab));
    tab.addEventListener('keydown', (event) => {
      if (!['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const nextIndex = event.key === 'Home'
        ? 0
        : event.key === 'End'
          ? tabs.length - 1
          : event.key === 'ArrowDown'
            ? (index + 1) % tabs.length
            : (index - 1 + tabs.length) % tabs.length;
      tabs[nextIndex].focus();
      selectTimelineItem(tabs[nextIndex]);
    });
  });

  selectTimelineItem(tabs[0]);
})();
