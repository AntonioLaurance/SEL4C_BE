const body = document.querySelector('body');
const tbody = document.querySelector('tbody');
const btnAddUpdate = document.querySelector('#btnAddUpdate')
const inNickName = document.querySelector('#inNickName')
const inEmail = document.querySelector('#inEmail')
const inPassword = document.querySelector('#inPassword')

btnAddUpdate.onclick = btnAddUser

body.onload = () => {
    fillTable()
}
function createRow(u, i){
    const tr = document.createElement('tr')
    const tdDelete = document.createElement('td')
    const iDelete = document.createElement('i')
    iDelete.className = 'fas fa-trash'
    const tdUpdate = document.createElement('td')
    const iUpdate = document.createElement('i')
    iUpdate.className = 'fas fa-pen'
    iDelete.onclick = () => {
        const isConfirm = confirm('Confirmar Eliminar Usuario')
        if(isConfirm){
            deleteUser(i)
            clearTable()
            fillTable()
        }
    }
    iUpdate.onclick = () => {
        btnAddUpdate.textContent='Actualizar'
        inNickName.value = u.nickname
        inPassword.value = u.password
        inEmail.value = u.email
        btnAddUpdate.onclick = (e) => btnUpdateUser(e, i)
    }
    const tdNickName = document.createElement('td')
    tdNickName.textContent = u.nickname
    const tdEmail = document.createElement('td')
    tdEmail.textContent = u.email
    const tdPassword = document.createElement('td')
    tdPassword.textContent = u.password
    tdDelete.appendChild(iDelete)
    tdUpdate.appendChild(iUpdate)
    tr.append(tdDelete, tdUpdate, tdNickName, tdEmail, tdPassword)
    return tr
}

function btnAddUser(e){
    const i = getUsers().length
    const newUser = createUser(inNickName.value, inEmail.value, inPassword.value)
    const tr = createRow(newUser, i)
    tbody.appendChild(tr)
    e.preventDefault();
    alert("Elemento guardado con Exito")  
}

function btnUpdateUser(e, i){
    updateUser(i, inNickName.value, inEmail.value, inPassword.value)
    clearTable()
    fillTable()
    e.preventDefault()
    alert("Elemento Actualizado con Exito")
    inNickName.value = ''
    inEmail.value = ''
    inPassword.value = ''
    btnAddUpdate.textContent = 'Agregar'
    btnAddUpdate.onclick = btnAddUser
}

function clearTable(){
    tbody.innerHTML = ''
}

function fillTable(){
    let trs = [];
    const users = getUsers()
    users.forEach((u, i)=>{
        const tr = createRow(u, i)
        trs.push(tr)
    })
    tbody.append(...trs)
}