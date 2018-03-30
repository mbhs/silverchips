$(document).ready(function() {
    $("body").css("marginTop", $(".navbar-wrapper").height() + 45);
    $(window).on("scroll", function() {
        if ($(window).scrollTop() > 10) {
            $(".navbar-wrapper").removeClass("not-scrolled").addClass("scrolled");
        } else {
            $(".navbar-wrapper").removeClass("scrolled").addClass("not-scrolled");
        }
    });
});
