function previewFile(input) {
    var file = $("#coverImg").get(0).files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function() {
            $("#pic").attr("src", reader.result);
        }
        reader.readAsDataURL(file);
    }
}

// See current pic or upload new pic
$("#changePic").click(function(e) {
    e.preventDefault();

    $("#pic").hide()
    $("#uploadPic").show()
    $("#changePic").hide()
    $("#seePic").show()
})

$("#seePic").click(function(e) {
    e.preventDefault();

    $("#pic").show()
    $("#uploadPic").hide()
    $("#changePic").show()
    $("#seePic").hide()
})