        $(".deletePost").submit(function (event) {

            console.log(this.action)

            function ajaxDelete() {
                var formData = {
                    csrfmiddlewaretoken: '{{ csrf_token }}',
                };

                $.ajax({
                    type: "POST",
                    url: this.action,
                    data: formData,
                    dataType: 'json',
                    encode: true,
                }).done(function (data) {
                    if (!data.success) {
                        if (data.username_error) {
                            iziToast.error({
                                position: 'topRight',
                                title: 'Error',
                                message: data.username_error
                            })
                        }
                    } else {
                        window.location.href = '/account/i/post'
                    }
                });
            }

            iziToast.question({
                timeout: 20000,
                close: false,
                overlay:true,
                id: 'question',
                zindex: 999,
                title: 'Delete Post',
                message: 'Are you sure about deleting this post?',
                position: 'center',
                buttons: [
                    ['<button><b>YES</b></button>', function (instance, toast) {
                        console.log('Working')
                        console.log(instance, toast)
                        ajaxDelete();
            
                    }, true],
                    ['<button>NO</button>', function (instance, toast) {
            
                        instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');
            
                    }],
                ],
            })

            event.preventDefault();
        })