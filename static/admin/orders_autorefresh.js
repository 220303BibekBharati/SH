(function(){
  // Auto-refresh Orders changelist every 10s when the page is idle
  const isOrdersChangelist = /\/admin\/orders\/order\/?$/.test(window.location.pathname);
  if (!isOrdersChangelist) return;

  let timer = null;
  const INTERVAL = 10000; // 10s
  const start = () => { timer = setInterval(() => window.location.reload(), INTERVAL); };
  const stop = () => { if (timer) { clearInterval(timer); timer = null; } };

  // Pause on user interaction to avoid disrupting edits/filters
  ['focusin','mousemove','keydown','scroll','click'].forEach(evt => {
    window.addEventListener(evt, () => {
      stop();
      // restart after a short idle
      setTimeout(() => { if (!timer) start(); }, 5000);
    });
  });

  // Only start if no popup or change form is open
  const onChangeForm = document.querySelector('body.change-form');
  if (!onChangeForm) start();
})();
