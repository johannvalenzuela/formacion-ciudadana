 window.onscroll = () => {
    const nav = document.querySelector('#navBarSection');
    if (nav) {
        if (this.scrollY <= 50) nav.className = 'navbar fixed-top navbar-expand-lg navbar-transparent'; else nav.className = 'navbar navbar-expand-lg sticky-top navbar-light bg-light py-2 shadow';
    }
}; 

var $star_rating = $('.star-rating .mi');

var SetRatingStar = function() {
  return $star_rating.each(function() {
    if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
      return $(this).removeClass('mi-FavoriteStar').addClass('mi-FavoriteStarFill');
    } else {
      return $(this).removeClass('mi-FavoriteStarFill').addClass('mi-FavoriteStar');
    }
  });
};

SetRatingStar();

$(document).ready(function () {
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar, #content').toggleClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
});

$('#sidebarCollapse').on('click', function () {
    if ($('#hide-panel').css('display') != 'none') {
        $('#show-panel').show().siblings('span').hide();
    } else if ($('#show-panel').css('display') != 'none') {
        $('#hide-panel').show().siblings('span').hide();
    }
});