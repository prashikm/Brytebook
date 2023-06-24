$(".copyLink").click(function (e) {
    var copyText = $(this).attr('href');

    document.addEventListener('copy', function(e) {
        e.clipboardData.setData('text/plain', copyText);
        e.preventDefault();
    }, true);

    document.execCommand('copy'); 

    iziToast.success({
        position: 'topRight',
        message: 'Link copied',
    });

    e.preventDefault();
})