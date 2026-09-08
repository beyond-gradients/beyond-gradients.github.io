/* Progressive enhancement only: content and all links work without JavaScript. */
'use strict';
document.documentElement.classList.add('js');
const menuToggle = document.querySelector('[data-menu-toggle]');
const navigation = document.querySelector('[data-navigation]');
function closeMenu(returnFocus = false) {
  navigation.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.querySelector('.sr-only').textContent = 'Open navigation';
  if (returnFocus) menuToggle.focus();
}
if (menuToggle && navigation) {
  menuToggle.addEventListener('click', () => {
    const open = menuToggle.getAttribute('aria-expanded') !== 'true';
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.querySelector('.sr-only').textContent = open ? 'Close navigation' : 'Open navigation';
    navigation.classList.toggle('is-open', open);
  });
  navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header') && menuToggle.getAttribute('aria-expanded') === 'true') closeMenu();
  });
  matchMedia('(min-width: 801px)').addEventListener('change', () => closeMenu());
}
// Illustrative, normalized weights for one head; deliberately not model measurements.
const attentionExamples = {
  The: [0.68, 0.08, 0.08, 0.08, 0.08],
  model: [0.12, 0.48, 0.14, 0.18, 0.08],
  uses: [0.05, 0.40, 0.15, 0.10, 0.30],
  the: [0.09, 0.12, 0.14, 0.45, 0.20],
  context: [0.05, 0.25, 0.15, 0.05, 0.50]
};
const controls = document.querySelector('.token-controls');
if (controls) {
  controls.hidden = false;
  controls.addEventListener('click', event => {
    const button = event.target.closest('button[data-token]');
    if (!button) return;
    const token = button.dataset.token;
    const weights = attentionExamples[token];
    controls.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.querySelector('[data-query-label]').textContent = token;
    document.querySelectorAll('[data-attention-line]').forEach((line, index) => {
      line.style.strokeWidth = 1 + weights[index] * 9;
      line.style.opacity = 0.2 + weights[index] * 1.4;
    });
    document.querySelectorAll('[data-attention-weight]').forEach((label, index) => { label.textContent = `${Math.round(weights[index] * 100)}%`; });
    document.querySelector('[data-attention-status]').textContent = `For “${token}”, line thickness shows how strongly it attends to each token. These example weights sum to 100%.`;
    document.querySelector('#attention-desc').textContent = `Illustrative attention weights for ${token}: ${Object.keys(attentionExamples).map((name, index) => `${name} ${Math.round(weights[index] * 100)} percent`).join(', ')}. These are invented teaching values, not measurements from a model.`;
  });
}
