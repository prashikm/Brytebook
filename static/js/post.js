function makePostRequest(e, url, FormData) {
    $.ajax({
        type: "POST",
        url: url,
        enctype: 'multipart/form-data',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: FormData,
        dataType: 'json',
    }).done(function (response) {
        return response
    })

    e.preventDefault();
}
