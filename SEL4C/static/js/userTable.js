// userTable.js

document.addEventListener('DOMContentLoaded', function () {
    const userTableBody = document.getElementById('userTableBody');
    const form = document.querySelector('form');

    // Función para cargar los datos de la API en la tabla
    function loadUserData() {
        // Hacer una solicitud a la API
        fetch('/api/user_data/')
            .then(response => response.json())
            .then(data => {
                // Limpiar la tabla antes de agregar nuevos datos
                userTableBody.innerHTML = '';

                // Iterar sobre los datos y crear filas en la tabla
                data.forEach(user => {
                    const row = document.createElement('tr');
                    const usernameCell = document.createElement('td');
                    const emailCell = document.createElement('td');
                    const passwordCell = document.createElement('td');
                    const actionsCell = document.createElement('td'); // Celda de acciones
        
                    usernameCell.textContent = user.username;
                    emailCell.textContent = user.email;
                    passwordCell.textContent = user.password;        

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Eliminar';
                    deleteButton.addEventListener('click', () => {
                        const confirmDelete = confirm('Estas seguro de borrar este usuario')
                        if (confirmDelete){
                            // Obtenemos url para el borrado
                            fetch('/api/delete_user/' + user.username + '/', {
                                method: 'DELETE',
                            })
                                .then(response => response.json())
                                .then(data => {
                                    if(data.success) {
                                        row.remove();
                                    }else{
                                        alert('error al eliminar el usuario');
                                    }
                                })
                                .catch(error => console.error('Error al eliminar', error));
                                
                        }
                    });

                    actionsCell.appendChild(deleteButton);

                    row.appendChild(usernameCell);
                    row.appendChild(emailCell);
                    row.appendChild(passwordCell);
                    row.appendChild(actionsCell);

                    userTableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error al cargar datos:', error));
    }
    // Función para crear un nuevo usuario
    function createUser(username, email, password) {
        fetch('/api/create_user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Agregar el nuevo usuario a la tabla
                    const row = document.createElement('tr');
                    const usernameCell = document.createElement('td');
                    const emailCell = document.createElement('td');
                    const passwordCell = document.createElement('td');
                    const actionsCell = document.createElement('td');

                    usernameCell.textContent = username;
                    emailCell.textContent = email;
                    passwordCell.textContent = password;

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Eliminar';
                    deleteButton.addEventListener('click', () => {
                        // ... (código de eliminación anterior) ...
                    });

                    actionsCell.appendChild(deleteButton);

                    row.appendChild(usernameCell);
                    row.appendChild(emailCell);
                    row.appendChild(passwordCell);
                    row.appendChild(actionsCell);

                    userTableBody.appendChild(row);

                    // Limpiar el formulario después de agregar el usuario
                    form.reset();
                } else {
                    alert('Error al crear el usuario.');
                }
            })
            .catch(error => console.error('Error al crear el usuario:', error));
    }

    // Manejar el envío del formulario
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const username = document.getElementById('inNickName').value;
        const email = document.getElementById('inEmail').value;
        const password = document.getElementById('inPassword').value;
        createUser(username, email, password);
    });

    // Cargar datos cuando se carga la página
    loadUserData();
});