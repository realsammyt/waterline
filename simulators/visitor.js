'use strict';
(() => {
  const offer = document.getElementById('offer');
  const receipt = document.getElementById('receipt');
  const result = document.getElementById('result');
  let choice;
  function show(screen) {
    for (const panel of [offer, receipt, result]) panel.hidden = panel !== screen;
    (screen.querySelector('[tabindex="-1"]') || screen.querySelector('button')).focus();
  }
  for (const button of offer.querySelectorAll('button')) {
    button.onclick = () => {
      choice = button.querySelector('strong').textContent;
      receipt.querySelector('h2').textContent = 'You chose ' + choice + '.';
      result.querySelector('h2').textContent = choice === 'Water' ? 'Water holds the hour.' : 'Water and ' + choice + ' share the hour.';
      document.getElementById('bands').textContent = choice === 'Water'
        ? 'One terracotta band travels along the Water rib, from one foot to the other.'
        : 'Water carries the leading terracotta band. A dimmer ' + button.dataset.tone + ' band travels alongside it on the ' + choice + ' rib.';
      show(receipt);
    };
  }
  document.getElementById('advance').onclick = () => show(result);
  document.getElementById('again').onclick = () => show(offer);
})();
