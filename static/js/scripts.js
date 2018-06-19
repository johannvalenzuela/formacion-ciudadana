var valorado = false;
window.onscroll = () => {
    const nav = document.querySelector('#navBarSection');
    if (nav) {
        if (this.scrollY <= 50) nav.className = 'navbar fixed-top navbar-expand-lg navbar-transparent'; else nav.className = 'navbar navbar-expand-lg sticky-top navbar-light bg-light py-2 shadow';
    }
};

var $total_star_rating = $('.total-star-rating .mi');
var $star_rating = $('.star-rating .mi');

var showRatingStar = function () {
    if(!valorado){
        return $total_star_rating.each(function () {
            if (parseInt($total_star_rating.siblings('input.total-rating-value').val()) >= parseInt($(this).data('rating'))) {
                return $(this).removeClass('mi-FavoriteStar').addClass('mi-FavoriteStarFill');
            } else {
                return $(this).removeClass('mi-FavoriteStarFill').addClass('mi-FavoriteStar');
            }
        });
    }
};

var SetRatingStar = function () {
    if(!valorado){
        return $star_rating.each(function () {
            if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
                return $(this).removeClass('mi-FavoriteStar').addClass('mi-FavoriteStarFill');
            } else {
                return $(this).removeClass('mi-FavoriteStarFill').addClass('mi-FavoriteStar');
            }
        });
    }
};

$star_rating.on('click', function () {
    if(!valorado){
        $star_rating.siblings('input.rating-value').val($(this).data('rating'));
        return SetRatingStar();
    }
});

showRatingStar();
SetRatingStar();

$(document).ready(function () {
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


function valorEstrella(estrella, token){
    if(!valorado){
        var valorEstrella = estrella.getAttribute("data-rating");
        $.ajax({
            url: 'valorar/',
            type: "POST",
            data: {valoracion: valorEstrella,
                'csrfmiddlewaretoken': token
            },
            success:function(m){
            alert('Gracias por tu valoración');
            valorado=true;
            },
        });
    }
}

// Script para mostrar modal de editar/eliminar recursos o comentarios
$(document).ready(function () {

    $(".recurso").click(function (ev) { // for each edit contact url
        ev.preventDefault(); // prevent navigation
        var url = $(this).data("form"); // get the contact form url
        console.log(url);
        $("#recursoModal").load(url, function () { // load the url into the modal
            $(this).modal('show'); // display the modal on url load
        });
    });

    $('.recurso-form').on('submit', function () {
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            context: this,
            success: function (data, status) {
                $('#recursoModal').html(data);
            }
        });
    });
});


$('option').mousedown(function(e) {
    e.preventDefault();
    $(this).prop('selected', !$(this).prop('selected'));
    return false;
});