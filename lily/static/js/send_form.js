function clearForm(form) {
    
    $(form).clearForm();
    $(form).find('.mws-error').remove();
    $(form).find('.field_error').each(function(index, element) {
       $(element).removeClass('field_error');
    });
}

// TODO: detect which button was clicked to be able to redirect to an edit view
function sendForm(dialog, successCallback, errorCallback) {
    var form = $(dialog).find('form'),
        counter = 0,
        cb = null;
    
    if( typeof(form === 'list') ){
        form = form[0]; 
    }
    
    var hideLoadingDialog = function(callback) {
        counter++;
        if(callback){ cb = callback; }
        if(counter === 2) {
            $('#loadingDialog').dialog('close');
            clearForm(form);
            $(dialog).dialog('close');
            cb();
        }
    };
    
    $(form).ajaxSubmit({
        type: 'post',
        dataType: 'json',
        url: $(dialog).attr('action'),
        data: {
            'csrfmiddlewaretoken': dialog.find('input[name="csrfmiddlewaretoken"]').val()
        }, beforeSubmit: function() {
            $(form).dialog('close');
            $('#loadingDialog').dialog('open');
                setTimeout(function() {
                    hideLoadingDialog();
                }, 1500);
        }, success: function(response) {
            if( response.error === true ) {
                $(form).html(response.html);
                if( typeof bindFormset == typeof Function )
                    bindFormset();
                $('#loadingDialog').dialog('close');
                $(dialog).dialog('open');
            } else if( response.redirect === true ) {
                window.location = response.url
            } else {
                if(!successCallback) {
                    successCallback = function() {
                        $('#successDialogMessage').text(response.html);
                        $('#successDialog').dialog('open');
                    };
                }
                hideLoadingDialog(successCallback);
            }
        }, error: function(){
            if(!errorCallback){
                errorCallback = function() {
                    $(dialog).dialog('close');
                    $('#errorDialog').dialog('open');
                };
            }            
            hideLoadingDialog(errorCallback);
        }
    });
}
