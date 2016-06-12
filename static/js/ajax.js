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
// Загрузка формы авторизации в модальное окно
$(document).on('click', '#loadloginform', function () {
    $.ajax({
        type: "GET",
        url: "/auth/login/form/",
        success: function (mydata) {
            $("#login-form").html(mydata);
        }
    });
    return false;
});

// Загрузка формы регистрации в модальное окно
$(document).on('click', '#loadregisterform', function () {
    $.ajax({
        type: "GET",
        url: "/auth/register/form/",
        success: function (mydata) {
            $("#register-form").html(mydata);
        }
    });
    return false;
});

// Отправка данных из формы авторизации
$(document).on('click', '#login-btn', function () {
    var data = $("form#login-form").serialize();
    $.ajax({
        url: '/auth/login/',
        method: 'POST',
        data: data,
        cache: false,
        success: function (data) {
            if (data != 'Ok') {
                // Пока кокой-то деревянный способ
                document.getElementById("username").style.backgroundColor = '#ff8888';
                document.getElementById("username").style.borderColor = '#cc0000';
                document.getElementById("password").style.backgroundColor = '#ff8888';
                document.getElementById("password").style.borderColor = '#cc0000';
            } else {
                location.href = "#";
                location.reload();
            }
        }
    });
    return false;
});

// Дополнительно: возвращает стиль элементов к исходному после индикации ошибки
$(document).on('click', 'form', function () {
    //Восстанавливаем значения стиля после индикации ошибки
    document.getElementById("username").style.backgroundColor = '#ffffff';
    document.getElementById("username").style.borderColor = '#cccccc';
    document.getElementById("password").style.backgroundColor = '#ffffff';
    document.getElementById("password").style.borderColor = '#cccccc';
    return false;
});

// Отправка данных из формы регистрации нового пользователя
$(document).on('click', '#register-btn', function () {
    var data = $("form#register-form").serialize();
    $.ajax({
        url: '/auth/register/',
        method: 'POST',
        data: data,
        cache: false,
        success: function (data) {
            if (data == 'Ok') {
                // Пока кокой-то деревянный способ
                //alert('Данные получены');
                location.href = "#";
                location.reload();
            } else {
                alert(data);
                // location.href = "#";
                // location.reload();
            }
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
            if (data == 'Ok') {
                // Пока кокой-то деревянный способ
                location.href = "#";
                location.reload();
            } else {
                alert(data);
            }
        }
    });
    return false;
});
