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

process_form_errors = function(errors) {
    /* Remove all preexisting error messages */
    jQuery('.errorlist').remove();
    jQuery('.error').removeClass('error');
    for (error in errors) {
        var obj = jQuery('#id_'+error);
        obj.addClass('error');
        var html = '<ul class="errorlist">';
        for (msg in errors[error]) { html += '<li>'+errors[error][msg]+'</li>'; }
        html += '</ul>';
        obj.after(html);
        }
    }

process_form_response = function(response) {
    var json = JSON.parse(response);
    process_json_response(json);
    }

/* Function to process json response */
process_json_response = function(json) {
    /* Process single notifications, messages and errors */
    if (json.notification) { jQuery.adjax_callbacks.show_notification(json.notification); }
    if (json.message) { jQuery.adjax_callbacks.show_message(json.message); }
    if (json.error) { jQuery.adjax_callbacks.show_error_message(json.error); }
    /* Process series of notifications, messages and errors */
    if (json.notifications) { for ( var notification in json.notifications) { jQuery.adjax_callbacks.show_notification(notification); } }
    if (json.messages) { for ( var message in json.messages) { jQuery.adjax_callbacks.show_message(message); } }
    if (json.errors) { for ( var error in json.errors) { jQuery.adjax_callbacks.show_error_message(error); } }
    process_form_errors(json.form_errors);
    /* if (json.form_errors) { process_form_errors(json.form_errors); } */
    /* If any update data have been provided, update the relevant elements */
    if (json.replace) {
        for (index in json.replace) {
            jQuery('#'+index).html(json.replace[index]);
            }
        }
    if (json.data) {
        for (index in json.data) {
            jQuery('.'+index).html(json.data[index]);
            }
        }
    }

/* Call a url that is served by an adjax decorated view */
jQuery.adjax = function(url, data) {
    jQuery.getJSON(url, data, process_json_response);
    /* Return false to prevent any links from being followed */
    return false;
    }

/* Make an ajax call (immediately) to the given url or object's href 
 * attribute, or post to the form's target.
 * USAGE:   $('#vote').adjax()
 */
jQuery.fn.adjax = function(data) {
    this.each(function() {
        if (jQuery(this).attr('href')) {
            var url = jQuery(this).attr('href').split("?")[0];
            jQuery.adjax(url, data);
            /* Return false to prevent any links from being followed */
            return false;
        } else if (jQuery(this).attr('action')) {
            /* TODO attach our callback */
            jQuery(this).ajaxSubmit(process_json_response);
            return false;
        }
        });

    /* Return object to allow chaining */
    return jQuery(this);  
    }

/* Automatically take a clickable object, doing an ajax call on click. */
jQuery.fn.adjaxify = function(data) {
    this.each(function() {
        var obj = jQuery(this)
        if (obj.attr('href')) {
            obj.click(function() { return obj.adjax(); });
            }
        else if (obj.attr('action')) {
            obj.ajaxForm(process_form_response);
            }
        });
    }


/* Convenient function to get objects to pause/wait for certain amount of time. */
jQuery.fn.wait = function(time) { 
    var obj = jQuery(this); 
    obj.queue(function() { setTimeout(function() {obj.dequeue();}, time); });
    return obj;
    };

