function showOrHideLogin(){
    var dropdownmenu = document.getElementById('dropdown-menu');
    var display = dropdownmenu.style.display;
    if(display === 'block'){
        dropdownmenu.style.display = 'none';
    }else{
        dropdownmenu.style.display = 'block';
    }
}

function showOrHideOptions(){
  var dropdownmenu = document.getElementById('dropdown-options');
  var display = dropdownmenu.style.display;
  if(display === 'block'){
      dropdownmenu.style.display = 'none';
  }else{
      dropdownmenu.style.display = 'block';
  }
}
