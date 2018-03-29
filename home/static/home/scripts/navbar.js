$(document).ready(function() {
    $("body").css("marginTop", $(".navbar-wrapper").height() + 25);
    $(window).on("scroll", function() {
        if ($(window).scrollTop() > 100) {
            $(".navbar-wrapper").removeClass("not-scrolled").addClass("scrolled");
        } else {
            $(".navbar-wrapper").removeClass("scrolled").addClass("not-scrolled");
        }
    });
});
