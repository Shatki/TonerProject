/**
 * easyConsole for jQuery.EasyUI
 *
 * Copyright (c) Seliverstov Dmitriy. All rights reserved.
 *
 * Licensed under the freeware license: http://www.-------.-----/--------
 * To use it on other terms please contact us: selidimail@gmail.com
 *
 */

// Делаем замыкание
(function ($) {
    function init(target, params) {
        let easyconsole = $(target);
        easyconsole.addClass('easyconsole');
        //let easyconsole = $(target).empty().append('Инициализация');
        //alert(target.toSource());
        // Запишем статус


        $.data(target, 'easyconsole', {
            init: true
        });

    }

    $.fn.easyconsole = function (message, params) {
        // Проинициализирован ли плагин?
        let state = $(this).hasClass('easyconsole');
        // Проинициализирован, вызываем методы
        if (typeof message === 'string') {
            // Передаем в метод контекст и настройки
            if (message in $.fn.easyconsole.methods) {
                alert('есть');
            }
            //response = $.fn.easyconsole.methods[options](this, message, params);
            }
        //alert(options.toSource());

        // Сюда пришел объект с настройками
        message = message || {};
        return this.each(function () {
            let state = $.data(this, 'easyconsole');
            if (state) {
                $.extend(state.options, message);
            } else {
                // Инициализируем объект с требуемыми опциями
                let result = init(this, $.extend({}, $.fn.easyconsole.defaults, message));
                return result
            }
        })
    };

    $.fn.easyconsole.methods = {
        test: function (jq) {
            alert('test!!!');
        },
        message: function (jq, message, params) {
            alert(message);
        }
    };

    $.fn.easyconsole.defaults = {};
})(jQuery);