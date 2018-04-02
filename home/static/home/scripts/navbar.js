$(document).ready(function() {
    $(window).on("resize", _.debounce(function() {
        $(".navbar-wrapper").removeClass("static-top").addClass("fixed-top");
        $("body").css("marginTop", $(".navbar-wrapper").outerHeight(true));
    }, 300));
    $(window).on("scroll", function() {
        if ($(window).scrollTop() > 10) {
            $(".navbar-wrapper").removeClass("not-scrolled").addClass("scrolled");
        } else {
            $(".navbar-wrapper").removeClass("scrolled").addClass("not-scrolled");
        }
    });
});
