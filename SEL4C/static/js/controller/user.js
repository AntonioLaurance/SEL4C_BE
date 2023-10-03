const users = [
    new User('A YPZ', 'ypz@gmail.com', 12345),
    new User('A YPb', 'ypb@gmail.com', 12345),
    new User('bob', 'bob@gmail.com', 12345),
]
function getUsers(){
    return users
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