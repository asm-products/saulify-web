$(document).ready(function() {
  
    // Scroll down landing page
    $(document).on('click', '.js-learn-more', function(e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $('.main').offset().top
        }, 500);
    });

});