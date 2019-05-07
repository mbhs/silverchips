function remargin() {
    var outerHeight;
    var scrolled = $(".navbar-wrapper").hasClass("scrolled");
    if (scrolled) {
        outerHeight = $(".navbar-wrapper").removeClass("scrolled").addClass("not-scrolled").outerHeight(true);
        outerHeight += 48; //navbar bottom padding
        $(".navbar-wrapper").removeClass("not-scrolled").addClass("scrolled");
    } else {
        outerHeight = $(".navbar-wrapper").outerHeight(true);
    }

    $("body").css("marginTop", outerHeight);
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
