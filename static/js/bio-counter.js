$(document).ready(function() {
    const messageEle = document.getElementById("bio");
    const counterEle = document.getElementById("counter");
    $("#counter").html(messageEle.value.length)
    
    messageEle.addEventListener("input", function (e) {
        $("#counter").show();
        const target = e.target;
        const maxLength = target.getAttribute("maxlength");
        const currentLength = target.value.length;
        counterEle.innerHTML = `${currentLength}/${maxLength}`;
    });
})
