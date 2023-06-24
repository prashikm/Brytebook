$("#profile-btn").click(function (e) {
    $("#profile-btn").attr("class", "cursor-pointer font-semibold text-xl text-black")
    $("#account-btn").attr("class", "cursor-pointer font-semibold text-xl text-gray-500 hover:text-black hover:underline")
})

$("#account-btn").click(function (e) {
    $("#profile-btn").attr("class", "cursor-pointer font-semibold text-xl text-gray-500 hover:text-black hover:underline")
    $("#account-btn").attr("class","cursor-pointer font-semibold text-xl text-black")
})