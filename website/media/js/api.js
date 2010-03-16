
$(document).ready(function() {
activate_code('messages');
activate_code('ajax');
activate_code('hide');
activate_code('redirect');
activate_code('forms');
activate_code('replace');
activate_code('all');
$('#feature-all').click();
expand_emails();
});

function activate_code(name) {
    // Hover effect done by javascript so as 
    // not to appear clickable without javascript
    $('#feature-'+name).hover(function () {
      $(this).addClass("hover");
    }, function () {
      $(this).removeClass("hover");
    });

    $('#feature-'+name).click(function() {
        if (name == 'all') { 
            // unfade all items
            $('pre span').removeClass('fade'); 
        } else {
            // fade all items
            $('pre span').addClass('fade'); 
            // unfade current item
            $('pre span.feature-'+name).removeClass('fade');
            }
        // highlight current navigation item
        $('#feature-navigation li').removeClass('active');
        $('#feature-'+name).addClass('active');

        // insert active text
        title = $('#feature-'+name+' h3').html()
        if (!title) { title = '' } else { title = title.toLowerCase()+"&nbsp;"}
        $('.file p span').html(title)

        return false;
        });
    }

// Rewrite worded emails as clickable links
function expand_emails() {
    $('span.email-address').each(function(index) {
        var email = $(this).html().replace(/ at /gi, '@').replace(/ dot /gi, '.');
        $(this).html('<a href="mailto:'+email+'">'+email+'</a>');
        });
    }
