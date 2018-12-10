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
                {field: 'pic', title: `${options.title_field_type}`, width: 3, align: 'center'},
                {field: 'date', title: `${options.title_field_date}`, width: 10, align: 'center'},
                {field: 'message', title: `${options.title_field_message}`, width: 100, align: 'left'}
            ]]
        });
        easyconsole.addClass('easyconsole');
        // Запишем статус
        return easyconsole
    }


    /** Вывод сообщения
     * Типы сообщений:
     *
     */
    function showMessage(target, message, params) {
        let console = $(target);
        // alert(console.easyconsole('options').toSource());
        console.datagrid('insertRow', {
            row: {
                date: $.fn.datetimebox.defaults.formatter(new Date()),
                pic: console.easyconsole('options').icons[params.type],
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
                //alert('команда:' + message);
                return $.fn.easyconsole.methods[message](this, params);
            } else {
                // Пришел запрос ("Строка для вывода", параметр)
                return $.fn.easyconsole.methods.message(this, message, params);
            }
        }

        // Пришел запрос ({ настройки })
        let options = message || {};
        return this.each(function () {
            let state = $.data(this, 'easyconsole');
            if (state) {
                $.extend(state.options, options);
            } else {
                // Инициализируем объект с требуемыми опциями
                let r = init(this, $.extend(options, $.fn.easyconsole.defaults, options));
                //alert('init');
                $.data(this, 'easyconsole', {
                    options: options,
                    table: r
                });
                showMessage(this, 'Запуск консоли', {type: 'warning'});
            }
        })
    };

    $.fn.easyconsole.methods = {
        options: function (jq) {
            return $.data(jq[0], 'easyconsole').options;
        },
        comand: function (jq, params) {
            return jq.each(function () {
                alert('comand');
            })
        },
        message: function (jq, message, params) {
            return jq.each(function () {
                showMessage(this, message, params);
            })
        }
    };

    $.fn.easyconsole.defaults = {
        title_field_date: 'Дата',
        title_field_type: 'Тип',
        title_field_message: 'Лог',
        icons: {
            'ok': '<img src ="/static/js/easyui/themes/icons/ok.png">',   // ok
            'warning': '<img src ="/static/js/easyui/themes/icons/tip.png">',  // warning
            'error': '<img src ="/static/js/easyui/themes/icons/no.png">'    // error
        },
    };
})(jQuery);