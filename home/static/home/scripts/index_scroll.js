//For index.html ONLY (found in _site-index-masthead.html)
//Changes navbar color when scrolling past index masthead &
//Animates scroll button
$(document).ready(function() {
    //Change navbar color when scrolling past index masthead
    var resizeOrScroll = function() {
        var scroll = $(window).scrollTop();
        if ($(window).width() >= 1200) {
            if (scroll > $(".site-index-masthead-wrapper").height()) {
                $('.navbar').css({"background-color": 'rgba(55,55,55,0.85)'});
            } else {
                $('.navbar').css({"background-color": 'transparent'});
            }
        } else {
            $('.navbar').css({"background-color": '#f4f4f4'});
        }
    };
    resizeOrScroll();
    $(window).on('resize scroll', resizeOrScroll);

    //Scroll button animation
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
