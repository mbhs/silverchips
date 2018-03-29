$(document).ready(function() {
    var onResize, onScroll, window_width;
    var logo = $(".logo").width(),
        lead = $(".navbar-wrapper-header .lead").css(["height", "padding", "margin"]),
        navlink = $(".navbar .nav-link").css(["padding"]);
    onResize = function() {
        window_width = $(window).width();
        $(".logo").width(window_width * 0.5);
        logo = $(".logo").width();
    };
    onScroll = _.debounce(function() {
        var scroll = $(window).scrollTop();
        if (scroll > 85 && window_width > 992) {
            $(".logo").animate({
                "width": logo * 0.75
            }, 250, "easeOutExpo");
            $(".navbar .nav-link").animate({
                "padding": "4px 8px"
            }, 250, "easeOutExpo");
        } else if (scroll < 10) {
            $(".logo").animate({
                "width": logo
            }, 250, "easeOutExpo");
            $(".navbar .nav-link").animate({
                "padding": navlink["padding"]
            }, 250, "easeOutExpo");
        }
    }, 100);
    onResize(); onScroll();
    $(window).on("resize", onResize);
    $(window).on("scroll", onScroll);
});
