/*-----------------------------------------------------------------------------------
 /*
 /* Init JS
 /*
 -----------------------------------------------------------------------------------*/

jQuery(document).ready(function ($) {

    "use strict";

    /*---------------------------------------------------- */
    /* Preloader
     ------------------------------------------------------ */
    $(window).load(function () {

        // will first fade out the loading animation
        $("#loader").fadeOut("slow", function () {

            // will fade out the whole DIV that covers the website.
            $("#preloader").delay(300).fadeOut("slow");

        });

    });


    /*----------------------------------------------------*/
    /* Flexslider
     /*----------------------------------------------------*/
    $(window).load(function () {

        $('#hero-slider').flexslider({
            namespace: "flex-",
            controlsContainer: ".hero-container",
            animation: 'fade',
            controlNav: true,
            directionNav: false,
            smoothHeight: true,
            slideshowSpeed: 7000,
            animationSpeed: 600,
            randomize: false,
            before: function (slider) {
                $(slider).find(".animated").each(function () {
                    $(this).removeAttr("class");
                });
            },
            start: function (slider) {
                $(slider).find(".flex-active-slide")
                    .find("h1").addClass("animated fadeInDown show")
                    .next().addClass("animated fadeInUp show");

                $(window).trigger('resize');
            },
            after: function (slider) {
                $(slider).find(".flex-active-slide")
                    .find("h1").addClass("animated fadeInDown show")
                    .next().addClass("animated fadeInUp show");
            }
        });

        $('#testimonial-slider').flexslider({
            namespace: "flex-",
            controlsContainer: "",
            animation: 'slide',
            controlNav: true,
            directionNav: false,
            smoothHeight: true,
            slideshowSpeed: 7000,
            animationSpeed: 600,
            randomize: false,
        });

    });

    /*----------------------------------------------------*/
    /* FitText Settings
     ------------------------------------------------------ */

    setTimeout(function () {
        $('h1.responsive-headline').fitText(1, {minFontSize: '40px', maxFontSize: '90px'});
    }, 100);


    /*----------------------------------------------------*/
    /* Smooth Scrolling
     ------------------------------------------------------ */

    $('.smoothscroll').on('click', function (e) {
        e.preventDefault();

        var target = this.hash,
            $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top
        }, 800, 'swing', function () {
            window.location.hash = target;
        });
    });


    /*----------------------------------------------------*/
    /* Highlight the current section in the navigation bar
     ------------------------------------------------------*/

    var sections = $("section");
    var navigation_links = $("#nav-wrap a");

    sections.waypoint({

        handler: function (event, direction) {

            var active_section;

            active_section = $(this);
            if (direction === "up") active_section = active_section.prev();

            var active_link = $('#nav-wrap a[href="#' + active_section.attr("id") + '"]');

            navigation_links.parent().removeClass("current");
            active_link.parent().addClass("current");

        },
        offset: '35%'

    });


    /*----------------------------------------------------*/
    /*	Make sure that #header-background-image height is
     /* equal to the browser height.
     ------------------------------------------------------ */

    $('header').css({'height': $(window).height()});
    $(window).on('resize', function () {

        $('header').css({'height': $(window).height()});
        $('body').css({'width': $(window).width()})
    });


    /*----------------------------------------------------*/
    /*	Fade In/Out Primary Navigation
     ------------------------------------------------------*/

    $(window).on('scroll', function () {

        var h = $('header').height();
        var y = $(window).scrollTop();
        var nav = $('#nav-wrap');

        if ((y > h * .20) && (y < h) && ($(window).outerWidth() > 768 )) {
            nav.fadeOut('fast');
        }
        else {
            if (y < h * .20) {
                nav.removeClass('opaque').fadeIn('fast');
            }
            else {
                nav.addClass('opaque').fadeIn('fast');
            }
        }

    });


    /*----------------------------------------------------*/
    /*	Modal Popup
     ------------------------------------------------------*/

    $('.item-wrap a').magnificPopup({

        type: 'inline',
        fixedContentPos: false,
        removalDelay: 200,
        showCloseBtn: false,
        mainClass: 'mfp-fade'

    });

    $(document).on('click', '.popup-modal-dismiss', function (e) {
        e.preventDefault();
        $.magnificPopup.close();
    });

    /*----------------------------------------------------*/
    /*	Modal dialogs
     ------------------------------------------------------*/

    // загрузка окна авторизации
    $('a#singin').click(function (event) { // лoвим клик пo ссылки с id="login"
        event.preventDefault(); // выключaем стaндaртную рoль элементa
        $('#overlay').fadeIn(400, // снaчaлa плaвнo пoкaзывaем темную пoдлoжку
            function () { // пoсле выпoлнения предыдущей aнимaции
                $('#login-dlg')
                    .css('display', 'block') // убирaем у мoдaльнoгo oкнa display: none;
                    .animate({opacity: 1, top: '40%'}, 200); // плaвнo прибaвляем прoзрaчнoсть oднoвременнo сo съезжaнием вниз
            });
    });
    /* Зaкрытие мoдaльнoгo oкнa, тут делaем тo же сaмoе нo в oбрaтнoм пoрядке */
    $('.modal-close, #overlay').click(function () { // лoвим клик пo крестику или пoдлoжке
        $('#login-dlg, #register-dlg')
            .animate({opacity: 0, top: '35%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
            function () { // пoсле aнимaции
                $(this).css('display', 'none'); // делaем ему display: none;
                $('#overlay').fadeOut(400); // скрывaем пoдлoжку
            }
        );
    });

    // Работает только так!!!
    $(document).on('click', "#loadregisterform", function (event) {   // лoвим клик пo ссылки с id="register"
        // Скрываем окно авторизации
        $('#login-dlg')
            .animate({opacity: 0, top: '35%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
            function () { // пoсле aнимaции
                $(this).css('display', 'none'); // делaем ему display: none;
            }
        );
        // Показываем окно регистрации
        $('#register-dlg')
            .css('display', 'block') // убирaем у мoдaльнoгo oкнa display: none;
            .animate({opacity: 1, top: '40%'}, 200); // плaвнo прибaвляем прoзрaчнoсть oднoвременнo сo съезжaнием вниз
        return false;
    });


    /*----------------------------------------------------*/
    /*	SELECTER ----> select system
     ------------------------------------------------------*/
    $('select').selecter();

    /*----------------------------------------------------*/
    /*	is_company визуализатор блока
     ------------------------------------------------------*/
    $('#iscompany').change(function () {
        <!-- Скрипт плавного открытия и закрытия блока -->
        if ($('#iscompany').prop('checked')) {
            $('#company-block').animate({
                height: 'show'
            }, 2000);
        }
        else {
            $('#company-block').animate({
                height: 'hide'
            }, 2000);
        }
    });

});








