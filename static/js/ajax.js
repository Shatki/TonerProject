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

/*----------------------------------------------------*/
/*	contact form
 ------------------------------------------------------*/

$('form#contactForm button.submit').click(function () {

    $('#image-loader').fadeIn();

    var contactName = $('#contactForm #contactName').val();
    var contactEmail = $('#contactForm #contactEmail').val();
    var contactSubject = $('#contactForm #contactSubject').val();
    var contactMessage = $('#contactForm #contactMessage').val();

    var data = 'contactName=' + contactName + '&contactEmail=' + contactEmail +
        '&contactSubject=' + contactSubject + '&contactMessage=' + contactMessage;

    $.ajax({

        type: "POST",
        url: "inc/sendEmail.php",
        data: data,
        success: function (msg) {

            // Message was sent
            if (msg == 'OK') {
                $('#image-loader').fadeOut();
                $('#message-warning').hide();
                $('#contactForm').fadeOut();
                $('#message-success').fadeIn();
            }
            // There was an error
            else {
                $('#image-loader').fadeOut();
                $('#message-warning').html(msg);
                $('#message-warning').fadeIn();
            }

        }

    });
    return false;
});

/*----------------------------------------------------*/
/*	Login/Register form
 ------------------------------------------------------*/

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

/*----------------------------------------------------*/
/*	Personal info form
 ------------------------------------------------------*/

$('#save-btn').click(function () {
    var data = $('DIV #personalinfo').serialize();
    $.ajax({
        url: '/auth/changeuserinfo/',
        method: 'POST',
        data: data,
        cache: false,
        success: function (data) {
            if (data != 'ok') {
                // Пока кокой-то деревянный способ
                alert(data);
            } else {
                location.href = "#";
                location.reload();
            }
        }
    });
    return false;
});
