/**
 * Función para programar la ponencia en el calendario de Outlook
 * @param {string} titulo - Nombre de la ponencia
 * @param {string} ponente - Nombre del ponente
 * @param {string} horaStr - Rango de hora (ej: "09:00 - 09:45")
 */
function reservarEnOutlook(titulo, ponente, horaStr) {
    // 1. Preparar las fechas en formato ISO (Outlook requiere YYYY-MM-DDTHH:MM:SS)
    // Para este ejemplo, usaremos la fecha actual
    const fechaHoy = new Date().toISOString().split('T')[0]; 
    const partesHora = horaStr.split(' - ');
    
    const inicioISO = `${fechaHoy}T${partesHora[0]}:00`;
    const finISO = `${fechaHoy}T${partesHora[1]}:00`;

    // 2. Datos que enviaremos a la ruta /crear-evento en Python
    const datosEvento = {
        titulo: titulo,
        ponente: ponente,
        lugar: "Auditorio Virtual / Universidad Católica", // Puedes hacerlo dinámico si quieres
        inicio: inicioISO,
        fin: finISO
    };

    // 3. Petición al servidor Flask
    fetch('/crear-evento', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datosEvento)
    })
    .then(response => {
        if (response.status === 401) {
            // Si el servidor dice que no hay token de Outlook, redirigir al login de MS
            alert("Primero debes vincular tu cuenta de Outlook.");
            window.location.href = "/login-outlook";
            throw new Error("No autenticado");
        }
        return response.json();
    })
    .then(res => {
        if (res.status === "success") {
            // 4. Mostrar el Modal con la información organizada
            mostrarModalExito(datosEvento);
        } else {
            alert("Error al reservar: " + res.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Función para llenar y mostrar el modal emergente
 */
function mostrarModalExito(datos) {
    const modal = document.getElementById('modalConfirmacion');
    const detalles = document.getElementById('modalDetalles');

    // Llenar el contenido del modal dinámicamente
    detalles.innerHTML = `
        <p><strong>Ponencia:</strong> ${datos.titulo}</p>
        <p><strong>Ponente:</strong> ${datos.ponente}</p>
        <p><strong>Lugar:</strong> ${datos.lugar}</p>
        <p><strong>Horario:</strong> ${datos.inicio.split('T')[1]} - ${datos.fin.split('T')[1]}</p>
        <p style="color: #666; font-size: 0.9em;"><i>* Se ha programado una alarma 15 minutos antes.</i></p>
    `;

    // Mostrar el modal (cambiar style de none a block)
    modal.style.display = 'block';
}

/**
 * Función para cerrar el modal
 */
function cerrarModal() {
    document.getElementById('modalConfirmacion').style.display = 'none';
}