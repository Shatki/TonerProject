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
    /**
     * Функция создания журнала документов
     * @param       target      (object DOM)    DOM Объект плагина
     * @param       options     (object)        Настройки плагина
     */
    function journalCreate(target, options) {
        let easydoc = $(target);

        let dateTo = $('<input>', {
            'id': "journal-datefrom",
            'class': "easyui-datetimebox",
            'style': "padding: 5px",
            'required': "required",
            'title': "From",
            'data-options': `width:200,labelWidth:30,label:'${options.title_dateFrom}',
                                labelPosition:'before',labelAlign:'right'`
        });
        let dateFrom = $('<input>', {
            'id': "journal-dateto",
            'class': "easyui-datetimebox",
            'style': "padding: 5px",
            'required': "required",
            'title': "To",
            'data-options': `width:200,labelWidth:30,label:'${options.title_dateTo}',
                                labelPosition:'before',labelAlign:'right'`

        });
        let datefilter = $('<div></div>', {
            'id': "journal-datefilter",
            'style': "padding: 5px"
        }).append(dateTo).append(dateFrom);

        let button_create = $('<a></a>', {
            'id': "journal-createdoc",
            'class': "easyui-linkbutton",
            'text': `${options.title_button_create}`,
            'href': "javascript:void(0)",
            'style': "padding: 5px",
            'data-options': "iconCls:'icon-add'",
            'plain': "true"
        });
        let button_edit = $('<a></a>', {
            'id': "journal-editdoc",
            'class': "easyui-linkbutton",
            'text': `${options.title_button_edit}`,
            'href': "javascript:void(0)",
            'style': "padding: 5px",
            'data-options': "iconCls:'icon-edit'",
            'plain': "true"
        });

        let toolbar = $('<div></div>', {
            'id': "journal-toolbar",
            'style': "padding: 5px"
        }).append(datefilter).append(button_create).append(button_edit);

        easydoc.tabs('add', {
            //Принудительно делаем индекс журнала 0
            index: 0,
            content: toolbar,
            //title: options.getTitle(options),
            title: options.journal_title,
            closable: false,
            selected: true
        }).tabs({
            onLoad: function (panel) {
                // Переименовывание панели
            }
        });
        //let journal = easydoc.tabs('getTab',0).append(toolbar);

        //alert(journal.html().toSource());

        //append(`<div id="journal-toolbar" class="journal-toolbar"></div>`);

        //

        //let journal = $(, );

        //let toolbar = `<div id="journal-toolbar" class="journal-toolbar"></div>`;
        //let table = `<table class ="easyui-datagrid"></table>`;
    }


    /**
     * Функция инициализатор плагина easyDoc
     * @param      target   (object DOM)    Объект DOM класса easyui-tabs  для активации на нем плагина easyDoc
     * @param      options  (object)    Объект с настройками плагина
     * @return              (object)    Объект содержащий {настройки, ициализированные jQuery.easydoc, jQuery.journal}
     */
    function init(target, options) {
        // Если options === undefined, сделаем ее просто пустой
        options = options || {};
        // Обернем DOM объект в jQuery функционал
        let easydoc = $(target);
        // Полученый target должен быть класса easyui-tabs
        if (!easydoc || !easydoc.hasClass('easyui-tabs')) {
            $.error('jQuery.easydoc: can\'t find easyui-tabs or easydoc');
            return this;
        }

        let journal = journalCreate(target, options);
        //alert(options.toSource());

        return {
            options: options,
            easydoc: target,  // или easydoc?
            journal: journal
        };
    }



    /**
     * Функция "точка" вызова плагина easyDoc
     * @param      options  (string, необязательный) имя вызываемого метода
     * @param      params   (object) параметры настройки плагина
     * @return     this     (object) объект экземпляра для поддержки цепочки вызовов
     * */
    $.fn.easydoc = function (options, params) {
        // Если пришло имя функции то string
        if (typeof options === 'string') {
            // Передаем в метод контекст и настройки
            return $.fn.easydoc.methods[options](this, params);
        }

        // Пришел объект с данными
        options = options || {};
        // Для поддержания цепочки вызовов вернем для каждого контекста результат индивидуально
        return this.each(function () {
            // Ищем в data уже существующий компонент
            let state = $.data(this, 'easydoc');
            if (state) {
                // Если уже создан, расширим опции
                $.extend(state.options, options);
            } else {
                // Инициализируем объект с требуемыми опциями
                // Возвращается объект с options/easydoc/journal
                let result = init(this, $.extend({}, $.fn.easydoc.defaults, options));
                // Сохраним созданный объект с элементами easydoc и journal
                // с нашими настройками для данного контекста в data
                $.data(this, 'easydoc', {
                    // Сохраним jQuery объект нашего элемента DOM
                    easydoc: result.easydoc,
                    // Берем для easyDoc настройки по-умолчанию и дополняем их полученными
                    options: result.options,
                    // При инициализации создается и журнал, сохраним его jQuery объект
                    journal: result.journal
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

    };

    $.fn.easydoc.defaults = {
        option: null,                       // Url параметр запроса {json, ...}
        common: `all`,
        edit: `edit/`,
        new: ``,
        target: `new`,


        title_button_create: 'Создать',
        title_button_edit: 'Редактировать',
        title_button_delete: 'Удалить',
        title_dateTo: 'До:',
        title_dateFrom: 'От:',
        document_type: `all`,
        document_type_name: `document`,
        document_type_name_new: `a new document`,
        document_type_name_plural: `documents`,
        journal_title: 'documents\'s journal',

        document_date: `01/01/2001`,

        //journal:      '#journal-table',
        //title:        `Журнал документов`,
        selector: '.easydoc-journal',

        timedelta: 90,     // период журнала в днях
        dateto: null,
        datefrom: null,

        getTitle: function (params) {
            params = params || {};
            // Если не пришла дата, то возьмем ее из defaults
            // params.date = $.fn.datebox.defaults.formatter(new Date());
            // Если не пришли параметры, то создадим новый документ
            return params.index ?
                params.document_type_name :
                `${params.document_type_name_new} от ${params.document_date ? params.document_date : this.document_date }`;
        },

        getUrl: function (params) {
            // Доделать!!!
            let type = params.document_type;
            let target = params.target ? params.target : this.target;   // all or number
            let option = params.index > 0 ? this.edit : this.option;             // json or null
            return `/document/${type}/${target}/${option}`;
        }
    }
})(jQuery);

