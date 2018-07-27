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
        /*  Функция "точка" вызова плагина EasyDoc
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
    $.fn.easydoc.methods = {};
    $.fn.easydoc.defaults = {
        test: 'easydoc-defaults',
        type: 'consignment'  // Потом поменять на 'all'
    };
})(jQuery);


(function ($) {
    /*  Функция инициализации компонента journal у EasyDoc
        @param      target (jQuery) целевой элемент DOM
        @param      options (object) параметры настройки плагина
        @return             (object) содержит options, journal, table, toolbar, menu
        */
    function init(target, options) {
        var journal = $(target);
        if (journal) {
            var table = journal.find('.easyui-datagrid');
            if (!table) {
                $.error('jQuery.journal: Не могу обнаружить datagrid table');
                return false;
            } else {
                table.addClass('easydoc-journal-table')
            }
        } else {
            $.error('jQuery.journal: Не могу обнаружить easydoc-journal');
            return false;
        }

        //alert(journal.html().toSource());
        var menu = $(table.datagrid('options').popupmenu);
        var toolbar = $(table.datagrid('options').toolbar);
        var dateFrom = toolbar.find('input.journal-datefrom');
        var dateTo = toolbar.find('input.journal-dateto');

        table.datagrid({
            clickToEdit: false,
            dblclickToEdit: true
        }).datagrid({
            onRowContextMenu: function (e, index, row) {
                e.preventDefault();
                // Включаем контекстное меню для редактирования таблицы документов
                popupmenu(target, index, row).menu('show', {
                    left: e.pageX,
                    top: e.pageY
                });
            }
        }).datagrid({
            loadFilter: function (data) {
                dateFrom.datetimebox('setValue', data.date_from);
                dateTo.datetimebox('setValue', data.date_to);
                return data;
            }
        });
        // Активный диапазон дат
        dateTo.datetimebox({
            onChange: function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    table.datagrid({
                        queryParams: {
                            dateTo: newValue,
                            dateFrom: dateFrom.datetimebox('getValue')
                        }
                    })
                }
            }
        });
        dateFrom.datetimebox({
            onChange: function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    table.datagrid({
                        queryParams: {
                            dateFrom: newValue,
                            dateTo: dateTo.datetimebox('getValue')
                        }
                    })
                }
            }
        });
        return {
            options: options,
            journal: journal,
            table: table,
            toolbar: toolbar,
            menu: menu
        };
    }

    $.fn.journal = function (options, params) {
        if (typeof options === 'string') {
            var result = $.fn.journal.methods[options](this, params);
            if (result) {
                return result(this, params);
            } else {
                $.error('Метод с именем ' + options + ' не существует для jQuery.journal');
                return this;
            }
        }

        options = options || {};
        //alert($(this).html().toSource());
        return this.each(function () {
            // Делаем инициализацию
            var state = $.data(this, 'journal');
            if (state) {
                $.extend(state.options, options);
            } else {
                var r = init(this, options);
                //alert(r.toSource());
                $.data(this, 'journal', {
                    options: $.extend($.fn.journal.defaults, options),
                    journal: r.journal,
                    table: r.table,
                    toolbar: r.toolbar,
                    menu: r.menu
                });
                $(this).removeAttr('disabled');
            }
            //$('input.combo-text', state.combo).attr('readonly', !state.options.editable);
            //setDisabled(this, state.options.disabled);
            //setSize(this);
            //-----bindEvents(this);
            //validate(this);
        });
    };

    $.fn.journal.methods = {};

    $.fn.journal.defaults = {
        test: 'journal-defaults',
        timedelta: 90,     // период журнала в днях
        dateto: null,
        datefrom: null,
        url: '/',
        title: 'Журнал документов',
        journal: '#journal-table'
    };

})(jQuery);





