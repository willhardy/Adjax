jQuery.noConflict();
(function($){

    /* Here we override the callbacks, with our custom message display */
    $.adjax_callbacks.show_notification = function(message) {
        msg_content = $('<div class="notification"><p>'+message+'</p></div>')
        msg_content.slideDown('slow').wait(2000).slideUp('slow')
        $('#content').prepend(msg_content);
        }
    $.adjax_callbacks.show_error = function(message) {
        alert(message);
        }
    $.adjax_callbacks.show_message = function(message) {
        msg_content = $('<div class="message"><p>'+message+'</p></div>')
        msg_content.slideDown('slow')
        $('#content').prepend(msg_content);
        }

    /* These are the links that point to Ajax-enabled views */
    $('.vote a, a.sms').adjaxify();
	$('a.heart, a span.heart').click(function(){
		$(this).toggleClass('heart-on');
        var data = { action: ($(this).hasClass('heart-on')) ? 'remove': 'add' }
        return $(this).adjax(data)
	});


})(jQuery);
