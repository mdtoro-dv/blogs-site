function opciones(opcion){
    if(opcion.value === "editar"){
        window.location.href = "/crear";
    }else if(opcion.value === "eliminar"){
        alert("¿Desea eliminar el blog?");
    }else if(opcion.value === "comentarios"){
        window.location.href = "/comentarios";
    }
}