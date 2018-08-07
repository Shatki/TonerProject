/**
 * easyDoc for jQuery.EasyUI
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
        /*  Функция инициализации плагина EasyDoc
            @param      target  (jQuery) целевой элемент DOM
            @param      options (object) параметры настройки плагина
            @return             (object) содержит options, easydoc, journal
            */

        // Если options === undefined, сделаем ее просто пустой
        options = options || {};
        // Получаем target для поиска элемента на который вешаем плагин
        var easydoc = $(target);
        // Полученый target должен быть класса easyui-tabs
        if (!easydoc || !easydoc.hasClass('easyui-tabs')) {
            $.error('jQuery.easydoc: can\'t find easyui-tabs or easydoc');
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
                    // Тут журнал
                    tab.addClass('easydoc-journal');
                    // Инициализация журнала
                    tab.journal({easydoc: easydoc});
                } else if (indexTab > 0) {
                    // Тут документ
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

    /**
     * Функция открытия документа из journal datagrid или создание нового документа
     * в новой tab вкладки для редактирования
     */
    function openDoc(container, params) {
        var easydoc = $(container);

        // Переработать для открытия через easyDoc
        if (easydoc.tabs('exists', params.title)) {
            // Если такой документ открыт, то переключимся на нее
            easydoc.tabs('select', params.title);
        } else {
            alert(params.url);
            $.ajax({
                url: params.url,
                cache: true,
                success: function (html) {
                    //Найдем в полученом HTML id документа и добавим его в data-options к tabs
                    var idDoc = +($("<div/>", {"html": html}).find('#doc-id').html());
                    if (idDoc >= 0) {
                        easydoc.tabs('add', {
                            //index: idDoc,
                            idDoc: idDoc,
                            title: params.title,
                            content: html,
                            closable: true,
                            selected: true
                        });
                    }
                }
            });
        }
        return this;
    }

    function closeDoc(container, param) {

    }

    $.fn.easydoc = function (options, params) {
        /*  Функция "точка" вызова плагина EasyDoc
            @param      options (string, необязательный) имя вызываемого метода
            @param      params (object) параметры настройки плагина
            @return     this (object) объект экземпляра для поддержки цепочки вызовов
            */
        // Если пришло имя функции то string
        if (typeof options === 'string') {
            return $.fn.easydoc.methods[options](this, params);
        }
        // Пришел объект с данными

        options = options || {};
        // Отобразим this для отладки

        return this.each(function () {
            // Ищем в data уже существующий компонент
            var state = $.data(this, 'easydoc');
            if (state) {
                // Если уже создан, расширим опции
                $.extend(state.options, options);
            } else {
                // Инициализируем объект с требуемыми опциями
                var r = init(this, options);
                // Получим созданный объект с элементами easydoc и journal
                // с нашими настройками и сохраним их в data
                $.data(this, 'easydoc', {
                    // Берем для EasyDoc настройки по-умолчанию и дополняем их полученными
                    options: $.extend($.fn.easydoc.defaults, options),
                    // Сохраним jQuery объект нашего элемента DOM
                    easydoc: r.easydoc,
                    // При инициализации создается и журнал, сохраним его jQuery объект
                    journal: r.journal
                });
                $(this).removeAttr('disabled');
            }
            /*  Тут алгоритм активации функций EasyDoc */

            //setDisabled(this, state.options.disabled);
            //Активация кнопок
            //bindEvents(this);
            //validate(this);
        });
    };
    $.fn.easydoc.methods = {
        options: function (jq) {
            return $.data(jq[0], 'easydoc').options;
        },
        journal: function (jq) {
            return $.data(jq[0], 'easydoc').journal;
        },
        tabs: function (jq) {
            return $.data(jq[0], 'easydoc').tabs;
        },

        close: function (jq, params) {
            return jq.each(function () {
                closeDoc(this, params);
            });
        },

        new: function (jq, params) {
            return jq.each(function () {
                alert(params.toSource());
                //openDoc(this, params);
            })
        }

    };
    $.fn.easydoc.defaults = {
        test: 'easydoc-defaults',
        type: 'consignment',                // Потом поменять на 'all'

        url: '/document/consignment/',
        open_url: '/open/',
        edit_url: '/edit/',
        new_url: '/new/'
    };
})(jQuery);

