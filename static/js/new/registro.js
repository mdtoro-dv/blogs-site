function showOrHideLogin(){
    var dropdownmenu = document.getElementById('dropdown-menu');
    var display = dropdownmenu.style.display;
    if(display === 'block'){
        dropdownmenu.style.display = 'none';
    }else{
        dropdownmenu.style.display = 'block';
    }
}