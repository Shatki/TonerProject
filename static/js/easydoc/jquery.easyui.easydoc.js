/**
 * EasyDoc for jQuery.EasyUI
 *
 * Copyright (c) 2016-2018 Seliverstov Dmitriy. All rights reserved.
 *
 * Licensed under the freeware license: http://www.-------.-----/--------
 * To use it on other terms please contact us: -----@-------.---
 *
 */

// Делаем замыкание
(function ($) {
    function init(target, options) {
        // Если опция undefined, сделаем ее просто пустой
        alert('Work!');
        options = options || {};
        // Получаем target для поиска элемента на который вешаем плагин
        var easydoc = $(target);
        // Полученый target должен быть класса easyui-tabs
        if (!easydoc || !easydoc.hasClass('easyui-tabs')) {
            $.error('jQuery.easydoc: Не могу обнаружить easyui-tabs или easydoc');
            return this;
        }
        // Инициализируем Tabs

        easydoc.tabs({
            onLoad: function (panel) {
                // Первая вкладка всегда journal с индексом 0

                var indexTab = panel.panel('options').index;
                var tab = easydoc.tabs('getTab', indexTab);
                //alert(tab.find('div').classes().toSource());
                if (indexTab === 0) {
                    tab.addClass('easydoc-journal');
                    tab.journal(options);
                } else if (indexTab > 0) {
                    tab.addClass('easydoc-document');
                    alert(tab.classes().toSource());
                    tab.document(options);
                } else {
                    $.error('jQuery.easydoc: index of tab error');
                }
            }
        }).tabs('add', {
            //Принудительно делаем индекс журнала 0
            index: 0,
            href: options.url,
            method: 'POST',
            title: options.title,
            closable: false,
            selected: true
        });
        //var journal = easydoc.tabs('getTab',0);
        //alert(journal.classes().toSource());
        return {
            options: options,
            easydoc: easydoc,
            journal: easydoc.tabs('getTab', 0)
        };
    }

    $.fn.easydoc = function (options, params) {
        /*  Функция вызова головного плагина EasyDoc
            @param      options (string, необязательный) имя вызываемого метода
            @param      params (object) параметры настройки плагина
            @return     this (object) каждого экземпляра
            */
        // Если пришло имя функции то string
        if (typeof options === 'string') {
            return $.fn.easydoc.methods[options](this, params);
        }
        // Пришел объект с данными
        options = options || {};

        // Отобразим this для отладки
        // alert($(this).html().toSource());
        return this.each(function () {
            // Делаем инициализацию
            var state = $.data(this, 'easydocui');
            if (state) {
                $.extend(state.options, options);
            } else {
                // Инициализируем компонент
                var r = init(this, options);
                $.data(this, 'easydocui', {
                    //options: $.extend({}, $.fn.journal.defaults, parseOptions(this), options),
                    options: $.extend({}, $.fn.document.defaults, options),
                    easydocui: r.easydocui,
                    journal: r.journal
                });
                $(this).removeAttr('disabled');
            }
            //setDisabled(this, state.options.disabled);
            //Активация кнопок
            //bindEvents(this);
            //validate(this);
        });
    };
    $.fn.easydoc.methods = {};
    $.fn.easydoc.defaults = {};


})(jQuery);





