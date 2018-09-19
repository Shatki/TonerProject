/**
 * jQuery.EasyUI.easyConsole
 *
 * Copyright (c) Seliverstov Dmitriy. All rights reserved.
 *
 * Licensed under the freeware license: http://www.-------.-----/--------
 * To use it on other terms please contact us: selidimail@gmail.com
 *
 */

// Делаем замыкание
(function ($) {
    function init(target, options) {
        let easyconsole = $(target);
        easyconsole.datagrid({
            fit: true,
            fitColumns: true,
            idField: 'date',
            textField: 'message',
            autoRowHeight: true,
            singleSelect: true,
            showFooter: true,
            columns: [[
                {field: 'type', title: `${options.title_field_type}`, width: 3},
                {field: 'date', title: `${options.title_field_date}`, width: 10},
                {field: 'message', title: `${options.title_field_message}`, width: 100, align: 'left'}
            ]]
        });

        easyconsole.addClass('easyconsole');
        //let easyconsole = $(target).empty().append('Инициализация');
        //alert(target.toSource());
        // Запишем статус
        return easyconsole
    }

    function consoleMessage(target, message, params) {
        $(target).datagrid('insertRow', {
            row: {
                date: '31-10-1985',
                age: 30,
                message: message
            }
        });
    }

    $.fn.easyconsole = function (message, params) {
        // Проинициализирован ли плагин?
        let initialized = $(this).hasClass('easyconsole');
        // Проинициализирован, вызываем методы
        if (typeof message === 'string' && initialized) {
            params = params || {};
            // Значит первым параметром пришла строка с текстом ии командой
            if (message in $.fn.easyconsole.methods) {
                // Пришел запрос ("Команда", параметр)
                //alert('команда');
                return $.fn.easyconsole.methods[message](this, params);
            } else {
                // Пришел запрос ("Строка для вывода", параметр)
                return $.fn.easyconsole.methods.message(this, message, params);
            }
        }
        //alert(options.toSource());

        // Пришел запрос ({ настройки })
        let options = message || {};
        return this.each(function () {
            let state = $.data(this, 'easyconsole');
            if (state) {
                $.extend(state.options, options);
            } else {
                // Инициализируем объект с требуемыми опциями
                let r = init(this, $.extend({}, $.fn.easyconsole.defaults, options));
                //alert('init');
                $.data(this, 'easyconsole', {
                    options: options,
                    table: r
                });
            }
        })
    };

    $.fn.easyconsole.methods = {
        comand: function (jq, params) {
            return jq.each(function () {
                alert('comand');
            })
        },
        message: function (jq, message, params) {
            return jq.each(function () {
                consoleMessage(this, message, params);
            })
        }
    };

    $.fn.easyconsole.defaults = {
        title_field_date: 'Дата',
        title_field_type: 'Тип',
        title_field_message: 'Лог',
    };
})(jQuery);