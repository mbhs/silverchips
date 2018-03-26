//For index.html ONLY (found in _site-index-masthead.html)
//Changes navbar color when scrolling past index masthead &
//Animates scroll button
$(document).ready(function() {
    //Masthead text+logo Animation
    var tl = new TimelineMax();
    tl.from($(".welcome"), 2, {top: 0, opacity: 0});
    tl.staggerTo($(".logo-container path"), 0.2, {fill: "#ffffff"},
        0.1, "-=2");
    tl.from($(".subhead"), 1, {top: 0, opacity: 0});
    tl.from($("#scroll"), 2, {top: 0, opacity: 0}, "-=2");
    tl.play();
    //Change navbar color when scrolling past index masthead
    var resizeOrScroll = function() {
        var scroll = $(window).scrollTop();
        if ($(window).width() >= 1200) {
            if (scroll > $(".site-index-masthead-wrapper").height()) {
                $('.navbar').css({"background-color": 'rgba(55,55,55,0.85)'});
                $('.navbar').removeClass("absolute-top");
                $('.navbar').addClass("fixed-top");
            } else {
                $('.navbar').css({"background-color": 'transparent'});
                $('.navbar').removeClass("fixed-top");
                $('.navbar').addClass("absolute-top");
            }
        } else {
            $('.navbar').css({"background-color": '#f4f4f4'});
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
            console.log($($(this).attr("href")).offset().top);
        });
    });
});
