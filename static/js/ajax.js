/*-----------------------------------------------------------------------------------
 /*
 /* Ajax JS
 /*
 -----------------------------------------------------------------------------------*/

/*----------------------------------------------------*/
/*	Login/Register form
 ------------------------------------------------------*/
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


function checkRegisterData() {
    alert('Проверяем регистрацию!')
}

$('#loadloginform').on('click', function () {
    $.ajax({
        type: "GET",
        url: "/auth/login/form/",
        success: function (mydata) {
            $("#signin-form").html(mydata);
        }
    });
    return false;
});


$('#loadregisterform').on('click', function () {
    $.ajax({
        type: "GET",
        url: "/auth/register/form/",
        success: function (mydata) {
            $("#signin-form").html(mydata);
        }
    });
    return false;
});
