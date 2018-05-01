function remargin() {
    $("body").css("marginTop", $(".navbar-wrapper").outerHeight(true));
}

$(document).ready(function() {
    remargin();
    $(window).on("resize", _.debounce(remargin, 300));

    $(window).on("scroll", function() {
        if ($(window).scrollTop() > 10) {
            $(".navbar-wrapper").removeClass("not-scrolled").addClass("scrolled");
        } else {
            $(".navbar-wrapper").removeClass("scrolled").addClass("not-scrolled");
        }
    });
});
