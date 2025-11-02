// CopyPasteSaver - JavaScript functionality
// Copy to clipboard, edit snippets, delete modal

let deleteFormToSubmit = null;

// ========== Copy to Clipboard ==========
document.addEventListener('click', function(e){
  const btn = e.target.closest('.btn.copy');
  if(!btn) return;
  
  const text = btn.getAttribute('data-content') || '';
  if(!text) return;
  
  // Use modern clipboard API if available
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

// Fallback copy method for older browsers
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

// ========== Edit Functionality ==========
document.addEventListener('click', function(e){
  // Handle Edit button click
  const editBtn = e.target.closest('.btn.edit-btn');
  if(editBtn){
    const id = editBtn.getAttribute('data-id');
    const contentDiv = document.getElementById('content-' + id);
    const editForm = document.getElementById('edit-form-' + id);
    
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
    const contentDiv = document.getElementById('content-' + id);
    const editForm = document.getElementById('edit-form-' + id);
    
    if(contentDiv && editForm){
      contentDiv.style.display = 'block';
      editForm.style.display = 'none';
    }
    return;
  }
});

// ========== Delete Modal ==========
// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function(){
  // Handle delete button clicks
  document.addEventListener('click', function(e){
    const deleteBtn = e.target.closest('.btn.delete');
    if(deleteBtn && deleteBtn.closest('form')){
      e.preventDefault();
      deleteFormToSubmit = deleteBtn.closest('form');
      const modal = document.getElementById('deleteModal');
      if(modal){
        modal.style.display = 'flex';
      }
    }
  });

  // Close modal on overlay click
  const modal = document.getElementById('deleteModal');
  if(modal){
    modal.addEventListener('click', function(e){
      if(e.target === this){
        closeDeleteModal();
      }
    });
  }

  // Close modal on ESC key
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){
      closeDeleteModal();
    }
  });
});

// Make these functions global so they can be called from HTML onclick
window.closeDeleteModal = function(){
  const modal = document.getElementById('deleteModal');
  if(modal){
    modal.style.display = 'none';
  }
  deleteFormToSubmit = null;
};

window.confirmDelete = function(){
  if(deleteFormToSubmit){
    deleteFormToSubmit.submit();
  }
  closeDeleteModal();
};
