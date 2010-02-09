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

form_processor_factory = function(form_obj) {
  if (!form_obj) { form_obj = jQuery; }

  process_form_errors = function(response) {
    var json = JSON.parse(response);
    /* Process the json, like links do */
    process_json_response(json);
    var errors = json.form_errors

    /* Remove all preexisting error messages */
    form_obj.find('.errorlist').remove();
    form_obj.find('.error').removeClass('error');
    for (error in errors) {
        /* Generate the error message html */
        var html = '<ul class="errorlist">';
        for (msg in errors[error]) { html += '<li>'+errors[error][msg]+'</li>'; }
        html += '</ul>';
        /* Attach the messages somewhere and add classes */
        if (error == '__all__') {
            var obj = form_obj;
            obj.prepend(html); }
        else {
            var obj = form_obj.find('#id_'+error);
            obj.addClass('error');
            obj.after(html); }
        }
    }
    return process_form_errors
  }


/* Function to process json response */
process_json_response = function(json) {
    /* Process any redirection first */
    if (json.redirect) { window.location.replace(json.redirect); }
    /* Process single notifications, messages and errors */
    if (json.notification) { jQuery.adjax_callbacks.show_notification(json.notification); }
    if (json.message) { jQuery.adjax_callbacks.show_message(json.message); }
    if (json.error) { jQuery.adjax_callbacks.show_error_message(json.error); }
    /* Process series of notifications, messages and errors */
    if (json.notifications) { for ( var notification in json.notifications) { jQuery.adjax_callbacks.show_notification(notification); } }
    if (json.messages) { for ( var message in json.messages) { jQuery.adjax_callbacks.show_message(message); } }
    if (json.errors) { for ( var error in json.errors) { jQuery.adjax_callbacks.show_error_message(error); } }
    /* if (json.form_errors) { process_form_errors(json.form_errors); } */
    /* If any update data have been provided, update the relevant elements */
    if (json.replace) {
        for (index in json.replace) {
            jQuery(index).html(json.replace[index]).show();
            }
        /* If a function is defined for document.ready, reapply that. */
        if (document_ready) { document_ready() }
        }
    if (json.hide) {
        for (element in json.hide) {
            jQuery(element).hide();
            }
        }
    if (json.data) {
        for (index in json.data) {
            jQuery("." + index).html(json.data[index]);
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
            return false;
        } else if (jQuery(this).attr('action')) {
            var form_processor = form_processor_factory(obj)
            jQuery(this).ajaxSubmit(form_processor);
            return false;
        }
        });

    /* Return false to avoid the link being followed or form submitted */
    return false;
    }

/* Automatically take a clickable object, doing an ajax call on click. */
jQuery.fn.adjaxify = function(data) {
    this.each(function() {
        var obj = jQuery(this)
        if (obj.attr('href')) {
            obj.click(function() { return obj.adjax(); });
            }
        else if (obj.attr('action')) {
            var form_processor = form_processor_factory(obj)
            obj.ajaxForm(form_processor);
            }
        });
    }


/* Convenient function to get objects to pause/wait for certain amount of time. */
jQuery.fn.wait = function(time) { 
    var obj = jQuery(this); 
    obj.queue(function() { setTimeout(function() {obj.dequeue();}, time); });
    return obj;
    };

