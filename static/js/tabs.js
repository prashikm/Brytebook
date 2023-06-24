$("#posts-btn").click(function (e) {
    $("#posts-btn").attr("class", "cursor-pointer font-semibold text-xl pb-2 text-black")
    $("#curated-btn").attr("class", "cursor-pointer font-semibold text-xl pb-2 text-gray-500 hover:text-black")
})

$("#curated-btn").click(function (e) {
    $("#posts-btn").attr("class", "cursor-pointer font-semibold text-xl pb-2 text-gray-500 hover:text-black")
    $("#curated-btn").attr("class","cursor-pointer font-semibold text-xl pb-2 text-black")
})