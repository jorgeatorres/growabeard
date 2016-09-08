jQuery(function($) {
    $('.beards .entry a').magnificPopup({
        type: 'ajax',
        closeBtnInside: true,
        overflowY: 'scroll',
        callbacks: {
            open: function() {
                location.hash = '#entry-' + $(this.currItem.el).parents('.entry').data('entry-id');
            },

            afterClose: function() {
                location.hash = '';
            }
        }
    });

    $('body').on('click', 'a.heart-it', function(e) {
        e.preventDefault();
        alert('¡Partíte 🍪! 💁');
    });

    var hash = window.location.hash.substring(1);
    if ( 'beard-' == hash.substring(0, 6) ) {
        var id = hash.substring(hash.indexOf('-') + 1);

        if ( $( '.entry[data-entry-id="' + id + '"]' ).length > 0 )
            $( '.entry[data-entry-id="' + id + '"] a' ).click();
    }

});

