/**
 * easyDoc for jQuery.EasyUI
 *
 * Copyright (c) Seliverstov Dmitriy. All rights reserved.
 *
 * Licensed under the freeware license: http://www.-------.-----/--------
 * To use it on other terms please contact us: selidimail@gmail.com
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
        let button_delete = $('<a></a>', {
            'id': "journal-deletedoc",
            'class': "easyui-linkbutton",
            'text': `${options.title_button_delete}`,
            'href': "javascript:void(0)",
            'style': "padding: 5px",
            'data-options': "iconCls:'icon-remove'",
            'plain': "true"
        });
        let toolbar = $('<div></div>', {
            'id': `${options.journal_toolbar}`,
            'style': "padding: 5px"
        }).append(datefilter).append(button_create).append(button_edit).append(button_delete);
        let table = $('<table></table>', {
            'class': "easyui-datagrid",
            'data-options': `url:'${options.getUrl({
                document_type: options.document_type,
                target: options.all,
                option: options.json
            })}',
                            method: 'post',
                            fit:true,
                            fitColumns:true,
                            idField:'id',
                            toolbar:'#${options.journal_toolbar}',
                            popupmenu:'#${options.journal_popupmenu}',
                            rownumbers:true,
                            autoRowHeight:false,
                            singleSelect:true,
                            columns:[[
                                    {field: 'id', width: 3, title: 'ID'},
                                    {field: 'ck', width: 3, checkbox: 'true'},
                                    {field: 'name', width: 30, title: '${options.title_field_name}', align: 'left'},
                                    {field: 'seller', width: 20, title: '${options.title_field_seller}', align: 'left'},
                                    {field: 'buyer', width: 20, title: '${options.title_field_buyer}', align: 'left'},
                                    {field: 'total', width: 5, title: '${options.title_field_total}',align: 'center'},
                                    {field: 'enable', width: 3, title: '${options.title_field_active}',
                                     align: 'center', editor:"{type:'checkbox',options:{on:'True',off:'False'}}"},                         
                                    ]]`
        });

        easydoc.tabs('add', {
            // Принудительно делаем индекс журнала 0
            index: 0,
            content: table,
            //title: options.getTitle(options),
            title: options.journal_title,
            closable: false,
            selected: true
        }).tabs({
            onLoad: function (panel) {
                // Переименовывание панели
            }
        });

        let journal = easydoc.tabs('getTab', 0).addClass("easydoc-journal").append(toolbar);


        //alert(journal.html().toSource());
        //append(`<div id="journal-toolbar" class="journal-toolbar"></div>`);

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
        json: `json/`,
        all: `all`,
        edit: `edit/`,
        new: ``,
        target: `new`,

        title_button_create: 'Create',
        title_button_edit: 'Edit',
        title_button_delete: 'Delete',
        title_dateTo: 'To:',
        title_dateFrom: 'From:',
        document_type: `all`,
        document_type_name: `document`,
        document_type_name_new: `a new document`,
        document_type_name_plural: `documents`,
        journal_title: 'documents\'s journal',

        title_field_name: 'Kind, number, date of document',
        title_field_seller: 'Seller',
        title_field_buyer: 'Buyer',
        title_field_total: 'Total',
        title_field_active: 'Active',

        document_date: `01/01/2001`,

        journal_table: 'journal-table',
        journal_toolbar: 'journal-toolbar',
        journal_popupmenu: 'journal-popupmenu',

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
            return `/document/${type}/${target}/${params.option ? params.option : option}`;
        }
    }
})(jQuery);

