(()=>{
  const shells=[...document.querySelectorAll('.vs-booking-shell')];

  shells.forEach(shell=>{
    if(!shell.querySelector('.vs-booking-pill')){
      const pill=document.createElement('div');
      pill.className='vs-booking-pill';
      pill.textContent=shell.dataset.bookingPill|| (shell.querySelector('.vs-variable-panel')?'CHECK YOUR DATE':'CHOOSE YOUR DAY');
      const copy=shell.querySelector('.vs-booking-copy');
      if(copy) shell.insertBefore(pill,copy);
      else shell.prepend(pill);
    }
    shell.querySelector('.vs-plan-ahead')?.remove();
    const allDates=shell.querySelector('.vs-all-dates');
    if(allDates) allDates.textContent='See all dates & times →';
  });

  document.querySelectorAll('.vs-booking-shell[data-ticket-url]').forEach(shell=>{
    const ticket=shell.dataset.ticketUrl;
    const days=[...shell.querySelectorAll('.vs-day[data-day]')];
    const grid=shell.querySelector('.vs-time-grid');
    const primary=shell.querySelector('.vs-primary-book');
    const heading=shell.querySelector('.vs-time-panel h3');
    let label=shell.querySelector('[data-selected-day]');
    if(!days.length||!grid||!primary)return;

    if(heading){
      const initialDay=(label?.textContent||'').trim();
      heading.innerHTML='Choose a time <span class="vs-selected-day-context">for <span data-selected-day></span></span>';
      label=heading.querySelector('[data-selected-day]');
      if(label) label.textContent=initialDay;
    }

    const bindTimes=()=>{
      [...grid.querySelectorAll('a')].forEach(a=>a.addEventListener('click',()=>{
        grid.querySelectorAll('a').forEach(x=>{
          const on=x===a;
          x.classList.toggle('is-selected',on);
          if(on)x.setAttribute('aria-current','true');
          else x.removeAttribute('aria-current');
        });
      }));
    };

    const render=btn=>{
      days.forEach(b=>{
        const on=b===btn;
        b.classList.toggle('is-active',on);
        b.setAttribute('aria-selected',on?'true':'false');
      });
      const day=btn.dataset.day;
      const times=(btn.dataset.times||'').split('|').filter(Boolean);
      if(label) label.textContent=day;
      grid.innerHTML=times.map(t=>`<a href="${ticket}" rel="noopener sponsored" target="_blank">${t}</a>`).join('');
      primary.textContent='Get Tickets →';
      primary.setAttribute('aria-label',`Get tickets for ${day}`);
      bindTimes();
    };

    days.forEach(btn=>btn.addEventListener('click',()=>render(btn)));
    const initial=days.find(b=>b.classList.contains('is-active'))||days[0];
    if(initial)render(initial);
  });
})();
