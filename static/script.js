// copy-to-clipboard for CopyPasteSaver
document.addEventListener('click', function(e){
  const btn = e.target.closest('.btn.copy');
  if(!btn) return;
  const text = btn.getAttribute('data-content') || '';
  if(!text) return;
  // Use navigator clipboard if available
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(()=>{
      btn.textContent = 'Copied ✓';
      setTimeout(()=> btn.textContent = 'Copy', 1200);
    }).catch(()=> {
      fallbackCopy(text, btn);
    });
  } else {
    fallbackCopy(text, btn);
  }
});

function fallbackCopy(text, btn){
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  try{
    const ok = document.execCommand('copy');
    btn.textContent = ok ? 'Copied ✓' : 'Copy';
    setTimeout(()=> btn.textContent = 'Copy', 1200);
  }catch(e){
    alert('Copy failed. Select and copy manually.');
  }finally{
    document.body.removeChild(ta);
  }
}
