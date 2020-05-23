$(document).ready(function () {
    $(".pro>button").click(function () {

        var index = $(this).index();
        console.log(index);
        var $img = $(".information>div").eq(index);
        $img.siblings().removeClass("show");
        $img.addClass("show");
    })
})
$(document).ready(function () {
    $(".set>button").click(function () {

        var index = $(this).index();
        console.log(index);
        var $img = $(".information>div").eq(index);
        $img.siblings().removeClass("show");
        $img.addClass("show");
    })
})