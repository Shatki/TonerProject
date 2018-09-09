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
        easyconsole = $(target).empty().append('Пусто');
        //alert(target.toSource());
    }

    $.fn.easyconsole = function (message, params) {
        // Проинициализирован ли плагин?
        let options = $.data(this, 'easyconsole');
        // 
        if (options) {

        }


        if (typeof message === 'string') {
            // Выдаем сообщение в консоль
            let response = $.fn.easyconsole.methods[message](this, message, params);
            if (response) {
                return response;
            }

        }

        options = options || {};
        return this.each(function () {
            let state = $.data(this, 'easyconsole');
            if (state) {
                $.extend(state.options, options);
            } else {
                // Инициализируем объект с требуемыми опциями
                let result = init(this, $.extend({}, $.fn.easyconsole.defaults, options));
                return result
            }
        })
    };

    $.fn.easyconsole.methods = {};

    $.fn.easyconsole.defaults = {};
})(jQuery);