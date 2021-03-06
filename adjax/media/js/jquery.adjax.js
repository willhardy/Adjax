
/* The following three functions can, and maybe should be overwritten with custom functions for a particular site. */
jQuery.adjax_callbacks = {
    /* Display the given message as a notification (passive non-vital information) */
    show_message: function(message) {
        var msg_html = jQuery('<p class="message '+message.tags+'">'+message.content+'</p>');
        // Show the messages by sliding down.
        msg_html.hide();
        jQuery('#messages').prepend(msg_html);
        msg_html.slideDown('slow');
        // Hide unimportant messages after a few seconds
        if (message.level < 40) { msg_html.wait(2000).slideUp('slow'); }
        }
    };

/* Function to process json response. This is the main switchboard, routing the
   specific top-level json items to handler functions.
*/
var process_json_response = function(json) {
    /* Process any redirection first */
    /* TODO, recognise 3XX responses and redirect the entire window (may be impossible with js/jQuery) */
    // Redirect leaving an entry in the browser's history (ie back button)
    if (json.redirect) { window; window.location.href = json.redirect; }
    /* Process single notifications, messages and errors */
    if (json.messages) { for (var msg in json.messages) { jQuery.adjax_callbacks.show_message(json.messages[msg]); } }
    /* If any update data have been provided, update the relevant elements */
    if (json.replace) {
        for (var replace_idx in json.replace) {
            // TODO: Need to determine whether it is a class or an id. For now i'm passing this in the DJANGO code itself.
            jQuery(replace_idx).html(json.replace[replace_idx]).show();
            }
        /* If a function is defined for document.ready, reapply that.  TODO: Document this feature. */
        if (json.document_ready) { document_ready(); }
        }

    /* Hide any elements listed here */
    if (json.hide) {
        for (var element in json.hide) {
            // TODO: Allow this functionality to be overridden, like message display
            // to let developers eg fade or slide or display a message etc
            jQuery(json.hide[element]).hide();
            }
        }
    /* Replace content for elements with the given class (handled by ) */
    if (json.update) {
        for (var update_idx in json.update) {
            jQuery("." + update_idx).html(json.update[update_idx]);
            }
        }
    };

/* This factory generates a speical processor for handling form responses
   It is currently hardwired to handle Djangos standard form html.
   TODO: Allow this to be overridden.
   TODO: How are multiple forms handled?
*/
var form_processor_factory = function(form_obj, callback) {
  if (!form_obj) { form_obj = jQuery; }

  return function(json) {
    /* Process the json, like links do */
    process_json_response(json);
    var errors = json.forms;

    /* Remove all preexisting error messages */
    form_obj.find('.errorlist').remove();
    form_obj.find('.error').removeClass('error');
    var display_form_error = function() {
        jQuery(this).addClass('error');
        jQuery(this).after(html); 
    };
    for (var error in errors) {
        /* Generate the error message html */
        var html = '<ul class="errorlist">';
        for (var msg in errors[error]) { html += '<li>'+errors[error][msg]+'</li>'; }
        html += '</ul>';

        /* Attach the messages somewhere and add classes */
        if (error == '__all__') {
            form_obj.prepend(html); }
        else {
            form_obj.find('#form-error-'+error).each(display_form_error);
            form_obj.find('#'+error).each(display_form_error);
            }
      }
    if (callback) { callback(json); }
    };
  };


/* Call a url that is served by an adjax decorated view.
 * Note that caching is turned off as Adjax usually runs through a Django view.
 * IE is known to otherwise automatically cache Ajax responses.
 */
jQuery.adjax = function(url, data, callback) {
    jQuery.ajax({
        url: url,
        dataType: 'json',
        data: data,
        cache: false,
        success: function(json) { process_json_response(json); if (callback) { callback(json); }}
    });
    /* Return false to prevent any links from being followed */
    return false;
    };

/* Make an ajax call (immediately) to the given url or object's href
 * attribute, or post to the form's target.
 * USAGE:   $('#vote').adjax()
 */
jQuery.fn.adjax = function(data, callback) {
    this.each(function() {
        var obj = jQuery(this);
        if (obj.attr('href')) {
            var url = obj.attr('href').split("?")[0];
            jQuery.adjax(url, data, callback);
            return false;
        } else if (obj.attr('action')) {
            var form_processor = form_processor_factory(obj, callback);
            obj.ajaxSubmit({success:form_processor, dataType:'json'});
            return false;
        }
        });

    /* Return false to avoid the link being followed or form submitted */
    return false;
    };

/* Automatically take a clickable object, doing an ajax call on click. */
jQuery.fn.adjaxify = function(callback) {
    this.each(function() {
        var obj = jQuery(this);
        if (obj.attr('href')) {
            obj.click(function() { return obj.adjax(null,callback); }); 
            }
        else if (obj.attr('tagName') == 'FORM') {
            /* submits an ajax form and prevent reloading POST submit */
            var submit_form = function() {
                obj.ajaxSubmit({success: form_processor_factory(obj, callback), dataType:'json'}); 
                return false; };
            // Bind the ajax submit to the submit signal, so that it can be called from the form.
            obj.submit(submit_form);
        }});
    };


/* Convenient function to get objects to pause/wait for certain amount of time. */
jQuery.fn.wait = function(time) {
    var obj = jQuery(this);
    obj.queue(function() { setTimeout(function() {obj.dequeue();}, time); });
    return obj;
    };
