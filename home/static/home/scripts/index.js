//For index.html ONLY (found in _site-index-masthead.html)
//Changes navbar color when scrolling past index masthead &
//Animates scroll button
$(document).ready(function() {
    //Masthead text+logo Animation
    var tl = new TimelineMax();
    tl.from($(".welcome"), 2, {top: 0, opacity: 0});
    tl.staggerTo($(".masthead .logo-container path"), 0.2, {fill: "#ffffff"},
        0.1, "-=2");
    tl.from($(".subhead"), 1, {top: 0, opacity: 0});
    tl.from($("#scroll"), 2, {top: 0, opacity: 0}, "-=2");
    tl.play();
    //Change navbar color when scrolling past index masthead
    var resizeOrScroll = function() {
        var scroll = $(window).scrollTop();
        var logo_height = $(".logo-container").height();
        if ($(window).width() >= 1200) {
            if (scroll > $(".site-index-masthead-wrapper").height()) {
                $(".site-navbar-wrapper").addClass("fixed-top");
                $(".navbar").removeClass("absolute-top");
                $(".navbar").css({
                    "background-color": "#a52714",
                    "margin-top": "1em",
                    "padding-top": 0,
                    "padding-bottom": 0
                });
                $(".navbar-header").css({
                    "max-height": logo_height + 100,
                    "background-color": "#f4f4f4"
                });
                $(".navbar-brand").css({
                    "display": "none",
                    "color": "#373737",
                });
                $(".navbar-nav").addClass("mx-auto");
                $(".site-index-masthead-wrapper").css({
                    "marginBottom": logo_height + $(".navbar").outerHeight()
                });
            } else {
                $(".site-navbar-wrapper").removeClass("fixed-top");
                $(".navbar").addClass("absolute-top");
                $(".navbar").css("background-color", "transparent");
                $(".navbar-header").css({
                    "max-height": "0px",
                    "background-color": "transparent"
                });
                $(".navbar-brand").css({
                    "display": "block",
                    "color": "#f4f4f4",
                });
                $(".navbar-nav").removeClass("mx-auto");
                $(".site-index-masthead-wrapper").css({
                    "marginBottom": 0
                });
            }
        } else {
            $('.site-navbar-wrapper').css("background-color", '#f4f4f4');
            $(".site-navbar-wrapper").addClass("fixed-top");
        }
    };
    resizeOrScroll();
    $(window).on('resize scroll', resizeOrScroll);

    //Scrolling animation
    $(function() {
        $("#scroll-btn").on("click", function(e) {
            e.preventDefault();
            $("html, body").animate(
                {scrollTop: $($(this).attr("href")).offset().top
                    + $($(this).attr("href")).height()
                    + parseInt($($(this).attr("href")).css("marginBottom"))},
                600,"linear");
        });
    });
});
