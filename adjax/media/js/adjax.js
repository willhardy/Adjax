/* The following three functions can, and maybe should be overwritten with custom functions for a particular site. */

/* Display the given message as a notification (passive non-vital information) */
jQuery.adjax_callbacks = { 
    show_notification: function(message) {
        msg_content = jQuery('<div class="notification"><p>'+message+'</p></div>')
        msg_content.slideDown('slow').wait(2000).slideUp('slow')
        jQuery('#content').prepend(msg_content);
        },
    /* Display the given message as a message (important information that the user must see, ie popup) */
    show_message: function(message) { jQuery.adjax_callbacks.show_notification(message); },
    /* Display the given message as an error message (attempted action unsuccessful) */
    show_error_message: function(message) { jQuery.adjax_callbacks.show_notification(message); },
    }

/* Call a url that is served by an adjax decorated view */
jQuery.adjax = function(url, data) {
    jQuery.getJSON(url, data, function(json) {
        /* Process single notifications, messages and errors */
        if (json.notification) { jQuery.adjax_callbacks.show_notification(json.notification); }
        if (json.message) { jQuery.adjax_callbacks.show_message(json.message); }
        if (json.error) { jQuery.adjax_callbacks.show_error_message(json.error); }
        /* Process series of notifications, messages and errors */
        if (json.notifications) { for ( var notification in json.notifications) { jQuery.adjax_callbacks.show_notification(notification); } }
        if (json.messages) { for ( var message in json.messages) { jQuery.adjax_callbacks.show_message(message); } }
        if (json.errors) { for ( var error in json.errors) { jQuery.adjax_callbacks.show_error_message(error); } }
        /* If any update data have been provided, update the relevant elements */
        if (json.data) {
            for (index in json.data) {
                jQuery('.'+index).html(json.data[index]);
                }
            }
    });
    /* Return false to prevent any links from being followed */
    return false;
    }

/* Make an ajax call to the given url or object's href attribute. */
jQuery.fn.adjax = function(data) {
    this.each(function() {
        if (jQuery(this).attr('href')) {
            var url = jQuery(this).attr('href').split("?")[0];
        } else { 
            var url = this;}
        jQuery.adjax(url, data);
        /* Return false to prevent any links from being followed */
        return false;
        });
    return false;  
    }

/* Automatically take a clickable object, doing an ajax call on click. */
jQuery.fn.adjaxify = function(data) {
    this.each(function() {
        jQuery(this).click(function() { return jQuery(this).adjax(); });
        });
    }


/* Convenient function to get objects to pause/wait for certain amount of time. */
jQuery.fn.wait = function(time) { 
    var obj = jQuery(this); 
    obj.queue(function() { setTimeout(function() {obj.dequeue();}, time); });
    return obj;
    };

