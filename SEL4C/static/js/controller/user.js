import User from '../model/User.js' 

let users = [];

function loadUsers(){
    fetch('/api/user_data/')
        .then(response => response.json())
        .then(data => {
            console.log(userData.username);
            users = data.map(userData => new User(userData.username, userData.email, userData.password));
        })
        .catch(error => {
            console.error('ERROR al obtener los usuarios', error);
        });
}

function getUsers(){
    return users;
}
function createUser(nickname, email, password){
    const newUser = new User(nickname, email, password)
    users.push(newUser)
    return newUser
}
function updateUser(i, newNickname, newEmail, newPassword){
    users[i].nickname = newNickname
    users[i].email = newEmail
    users[i].password = newPassword
}
function deleteUser(i){
    users.splice(i, 1)
}

loadUsers();

export {getUsers, createUser, updateUser, deleteUser};