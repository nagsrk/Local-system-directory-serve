function chValie() {
  ess = new Array("old_password", "new_password1", "new_password2");
  for(i = 0; i < ess.length; i++) {
    txt = document.password.elements[ess[i]].value;
    if(txt == "") {
      var box = document.getElementById('error_text');
      box.innerHTML="Please, input all items.";
      return false;
    }
  }
  return true;
}

function escapeHtml(str) {
    str = str.replace(/&/g, '&amp;');
    str = str.replace(/</g, '&lt;');
    str = str.replace(/>/g, '&gt;');
    str = str.replace(/"/g, '&quot;');
    str = str.replace(/'/g, '&#39;');
    return str;
}
