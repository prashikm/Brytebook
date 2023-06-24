function emailValidation(email) {
    if (email === '') {
        return 'Email cannot be blank';
    }

    let regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    let testEmail = regex.test(email);

    return (testEmail ? true : 'Not valid email')
}

function passwordValidation(password) {
    if (password === '') {
        return 'Password cannot be blank'
    }else if (password.length < 8) {
        return 'Password cannot be less than 8 characters'
    }else {
        return true
    }
}

function usernameValidation(username) {
    if (username === '') {
        return 'Username cannot be blank';
    } else if (username.length < 3) {
        return 'Username must be greater then 3'
    } else if (username.length > 20) {
        return 'Username must be less then 20'
    }

    let regex = /^[a-z0-9_]{3,20}$/;
    let testUsername = regex.test(username);

    return (testUsername ? true : 'Username can only contain alpha numeric characters, numbers or underscore')
}


function nameValidation(name) {
    if (name === '') {
        return 'Name cannot be blank'
    } else {
        return true
    }
}


function bioValidation(bio) {
    if (bio === '') {
        return 'Bio cannot be blank'
    } else if (bio.length > 150) {
        return 'Bio cannot be greater than 150 characters'
    } else {
        return true
    }
}


function inviteValidation(inviteCode) {
    if (inviteCode === '') {
        return 'Invitation code cannot be blank'
    } else {
        return true
    }
}


function setAlert(alert_id, msg) {
    $(`${alert_id}`).html(msg)
}
