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

// Edit functionality
document.addEventListener('click', function(e){
  // Handle Edit button click
  const editBtn = e.target.closest('.btn.edit-btn');
  if(editBtn){
    const id = editBtn.getAttribute('data-id');
    const contentDiv = document.getElementById(`content-${id}`);
    const editForm = document.getElementById(`edit-form-${id}`);
    
    if(contentDiv && editForm){
      contentDiv.style.display = 'none';
      editForm.style.display = 'block';
      editForm.querySelector('textarea').focus();
    }
    return;
  }
  
  // Handle Cancel button click
  const cancelBtn = e.target.closest('.cancel-edit');
  if(cancelBtn){
    const id = cancelBtn.getAttribute('data-id');
    const contentDiv = document.getElementById(`content-${id}`);
    const editForm = document.getElementById(`edit-form-${id}`);
    
    if(contentDiv && editForm){
      contentDiv.style.display = 'block';
      editForm.style.display = 'none';
    }
    return;
  }
});
