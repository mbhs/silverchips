$(document).ready(function() {
    var logo = $(".navbar-wrapper-header .logo").width();
    var lead = $(".navbar-wrapper-header .lead").css(["height", "padding", "margin"]);
    var nav = $(".navbar .nav-link").css(["padding"]);
    $(window).on("resize scroll", function() {
        var scroll = $(this).scrollTop();
        if (scroll > 50) {
            // $(".navbar-wrapper").removeClass("static-top");
            // $(".navbar-wrapper").addClass("fixed-top");
            $(".navbar-wrapper-header .logo").width(logo * 0.7);
            $(".navbar-wrapper-header .lead").css({"height":0, "padding":0, "margin":0});
            $(".navbar .nav-link").css({"padding":"8 8"});
        } else if (scroll < 1) {
            // $(".navbar-wrapper").removeClass("fixed-top");
            // $(".navbar-wrapper").addClass("static-top");
            $(".navbar-wrapper-header .logo").width(logo);
            $(".navbar-wrapper-header .lead").css({"height":lead["height"],
                "padding":lead["padding"],"margin":lead["margin"]
            });
            $(".navbar .nav-link").css({"padding":nav["padding"]});
        }
    });
});
