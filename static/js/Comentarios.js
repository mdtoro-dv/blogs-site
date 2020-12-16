function cerrarSesion(value){
    if(value.value === "cerrar"){
        window.location.href = "/index";
    }else{
        window.location.href = "/inicio";
    }
}