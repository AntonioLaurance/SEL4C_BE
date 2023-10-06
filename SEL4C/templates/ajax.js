document.addEventListener('DOMContentLoaded', function() {
    // Realizar una solicitud AJAX para obtener los datos de la primera API
    fetch('/api/graph-social/')
        .then(response => response.json())
        .then(data => {
            // Crear la primera gráfica
            crearGrafica('grafica1', 'Grafica 1', data);
        });

    // Realizar una solicitud AJAX para obtener los datos de la segunda API
    fetch('/api/graph-thinking/')
        .then(response => response.json())
        .then(data => {
            // Crear la segunda gráfica
            crearGrafica('grafica2', 'Grafica 2', data);
        });

    // Función para crear una gráfica
    function crearGrafica(contenedorId, titulo, data) {
        var ctx = document.getElementById(contenedorId).getContext('2d');
        new Chart(ctx, {
            type: 'bar', // Tipo de gráfica (puedes cambiarlo según tus necesidades)
            data: {
                labels: ['Antes', 'Después'], // Etiquetas para el eje X
                datasets: [{
                    label: titulo,
                    data: [data.before, data.after], // Los valores de los datos
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 99, 132, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
