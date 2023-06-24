function titleValidation(title) {
    if (title === '') {
        return 'Title cannot be empty'
    } else {
        return true
    }
}

function contentValidation(content) {
    if (content === '') {
        return 'Content cannot be blank'
    } else {
        return true
    }
}

function coverValidation(cover) {
    if (cover.length === 0) {
        return 'Upload cover image'
    } else {
        return true
    }
}


function coverImageValidation(imgCover) {
    if (imgCover === '' || imgCover === '#') {
        return 'Upload cover image'
    } else {
        return true
    }
}