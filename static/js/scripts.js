window.onscroll = () => {
    const nav = document.querySelector('#navBarSection');
    if (nav) {
        if (this.scrollY <= 50) nav.className = 'navbar fixed-top navbar-expand-lg navbar-transparent'; else nav.className = 'navbar navbar-expand-lg sticky-top navbar-light bg-light py-2 shadow';
    }
};

var $total_star_rating = $('.total-star-rating .mi');
var $star_rating = $('.star-rating .mi');

var showRatingStar = function () {
    return $total_star_rating.each(function () {
        if (parseInt($total_star_rating.siblings('input.total-rating-value').val()) >= parseInt($(this).data('rating'))) {
            return $(this).removeClass('mi-FavoriteStar').addClass('mi-FavoriteStarFill');
        } else {
            return $(this).removeClass('mi-FavoriteStarFill').addClass('mi-FavoriteStar');
        }
    });
};

var SetRatingStar = function () {
    return $star_rating.each(function () {
        if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
            return $(this).removeClass('mi-FavoriteStar').addClass('mi-FavoriteStarFill');
        } else {
            return $(this).removeClass('mi-FavoriteStarFill').addClass('mi-FavoriteStar');
        }
    });
};

$star_rating.on('click', function () {
    $star_rating.siblings('input.rating-value').val($(this).data('rating'));
    return SetRatingStar();
});

showRatingStar();
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


function valorEstrella(estrella){
    var valorEstrella = estrella.getAttribute("data-rating");
   alert(valorEstrella);
    $.ajax({
        url: 'valorar',
        type: "POST",
        data: {valoracion: valorEstrella},
        success:function(m){
            alert('funcionó');
        },
    });
    
}

