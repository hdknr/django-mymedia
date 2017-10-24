  jQuery(document).ready(function($) {

    $('#myCarousel').carousel({pause: true, interval: false});

    $("#app").on({
        "click":function(){
          var id_selector = $(this).attr("id");
          try {
            var id = /-(\d+)$/.exec(id_selector)[1];
            jQuery('#myCarousel').carousel(parseInt(id));
          } catch (e) {
            // console.log('Regex failed!', e);
          }
        }
    }, "a.thumbnail" );

    // When the carousel slides, auto update the text
    $('#myCarousel').on('slid.bs.carousel', function (e) {
        var id = $('.item.active').data('slide-number');
        $('#carousel-text').html($('#slide-content-'+id).html());
    });
  });
