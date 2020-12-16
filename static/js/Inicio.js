function cerrarSesion(value){
    if(value.value === "cerrar"){
        window.location.href = "/index";
    }
}

function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}