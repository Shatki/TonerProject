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
     * Создание меню журнала плагина EasyDoc
     * @param       target      (object DOM)    DOM Объект плагина
     * @param       options     (object)        Настройки плагина
     * Динамическое создание меню для journal
     */
    function journalMenuCreate(target, options) {
        menu = $('#journal-popupmenu');
        menu.//empty().
        menu('appendItem', {
            text: `${options.title_create}`,
            name: 'create',
            iconCls: 'icon-add'
        }).menu('appendItem', {
            text: `${options.title_edit}`,
            name: 'edit',
            iconCls: 'icon-edit'
        }).menu('appendItem', {
            text: `${options.title_remove}`,
            name: 'remove',
            iconCls: 'icon-remove'
        }).menu('appendItem', {
            separator: true
        }).menu('appendItem', {
            text: `${options.title_copy}`,
            name: 'copy',
            iconCls: 'icon-copy'
        }).menu('appendItem', {
            text: `${options.title_paste}`,
            name: 'paste',
            iconCls: 'icon-paste'
        }).menu('appendItem', {
            text: `${options.title_dublicate}`,
            name: 'dublicate',
            iconCls: 'icon-paste'
        }).menu('appendItem', {
            separator: true
        }).menu('appendItem', {
            text: `${options.title_reload}`,
            name: 'reload',
            iconCls: 'icon-reload'
        }).menu('appendItem', {
            text: `${options.title_print}`,
            name: 'print',
            iconCls: 'icon-print'
        }).menu('options').onClick = function (action) {
            $(target).easydoc(action.name)
        };
        return menu;
    }

    /**
     * Функция создания журнала документов
     * @param       target      (object DOM)    DOM Объект плагина
     * @param       options     (object)        Настройки плагина
     */
    function journalCreate(target, options) {
        //let easydoc = $(target);
        //let tab = easydoc.tabs('getTab', 0);
        let table = $('<table></table>', {
            'class': "easyui-datagrid",
            'id': "journal-table",
            'data-options': `
                            popupmenu: '#journal-popupmenu',
                            clickToEdit: false,
                            dblclickToEdit: true,
                            fit:true,
                            fitColumns:true,
                            idField:'id',
                            rownumbers:true,
                            autoRowHeight:false,
                            singleSelect:true,
                            columns:[[
                                    {field: 'id', width: 3, title: 'ID'},
                                    {field: 'ck', width: 2, checkbox: 'true'},
                                    {field: 'name', width: 30, title: '${options.title_field_name}', align: 'left'},
                                    {field: 'seller', width: 20, title: '${options.title_field_seller}', align: 'left'},
                                    {field: 'buyer', width: 20, title: '${options.title_field_buyer}', align: 'left'},
                                    {field: 'total', width: 5, title: '${options.title_field_total}',align: 'center'},
                                    {field: 'enable', width: 5, title: '${options.title_field_active}',
                                     align: 'center', editor:"{type:'checkbox',options:{on:'True',off:'False'}}"},                         
                                    ]]`
        });
        // toolbar
        let toolbar = $('<div></div>', {
            'id': "journal-toolbar",
            'style': "padding: 5px"
        }).appendTo(table);
        // dateFilter
        let datefilter = $('<div></div>', {
            'id': "journal-datefilter",
            'style': "padding: 5px"
        }).appendTo(toolbar);
        // dateFrom
        $('<input>', {
            'id': "journal-datefrom",
            'class': "easyui-datetimebox",
            'style': "padding: 5px",
            'required': "required",
            'title': "From",
            'data-options': "width:200,labelWidth:40,labelPosition:'before',labelAlign:'right'"
        }).appendTo(datefilter);
        // dateTo
        $('<input>', {
            'id': "journal-dateto",
            'class': "easyui-datetimebox",
            'style': "padding: 5px",
            'required': "required",
            'title': "To",
            'data-options': "width:200,labelWidth:40,labelPosition:'before',labelAlign:'right'"

        }).appendTo(datefilter);
        // buttonCreate
        $('<a></a>', {
            'id': "journal-createdoc",
            'class': "easyui-linkbutton",
            'text': `${options.title_create}`,
            'href': "javascript:void(0)",
            'data-options': "iconCls:'icon-add'",
            'plain': "true"
        }).appendTo(toolbar);
        // buttonEdit
        $('<a></a>', {
            'id': "journal-editdoc",
            'class': "easyui-linkbutton",
            'text': `${options.title_edit}`,
            'href': "javascript:void(0)",
            'data-options': "iconCls:'icon-edit'",
            'plain': "true"
        }).appendTo(toolbar);
        // buttonDelete
        $('<a></a>', {
            'id': "journal-deletedoc",
            'class': "easyui-linkbutton",
            'text': `${options.title_remove}`,
            'href': "javascript:void(0)",
            'data-options': "iconCls:'icon-remove'",
            'plain': "true"
        }).appendTo(toolbar);

        // popupmenu
        $('<div></div>', {
            'id': "journal-popupmenu",
            'class': "easyui-menu"
        }).appendTo(table);
        // Общее содержимое вкладки
        return table;
    }

    /**
     * Инициализация вкладок для работы
     * @param       target      (object DOM)    DOM объект нашего плагина
     * @param       options     (object)        Настройки плагина
     * @returns     tab         (object DOM)    DOM
     */
    function initTabs(target, options) {
        // Обернем DOM объект в jQuery функционал
        let easydoc = $(target);
        easydoc.tabs({
            onAdd: function (title, index) {
                // Первая вкладка всегда journal с индексом 0
                let tab = easydoc.tabs('getTab', index);
                let tabtitle = options.getTitle({index: index});
                if (index === 0) {
                    // Тут журнал
                    tab.addClass('easydoc-journal');
                    // Инициализация журнала
                    easydoc.tabs('update', {
                        tab: tab,
                        options: {
                            title: tabtitle,
                            content: journalCreate(target, options)
                        }
                    });
                    let table = tab.find('#journal-table');
                    let datefrom = tab.find('input#journal-datefrom');
                    let dateto = tab.find('input#journal-dateto');
                    let popupmenu = journalMenuCreate(target, options);

                    // Привязка событий
                    datefrom.datetimebox({
                        label: options.title_dateFrom,
                        onChange: function (newValue, oldValue) {
                            if (newValue !== oldValue && oldValue) {
                                table.datagrid({
                                    queryParams: {
                                        dateFrom: newValue,
                                        dateTo: dateto.datetimebox('getValue')
                                    }
                                })
                            }
                        }
                    });
                    dateto.datetimebox({
                        label: options.title_dateTo,
                        onChange: function (newValue, oldValue) {
                            if (newValue !== oldValue && oldValue) {
                                table.datagrid({
                                    queryParams: {
                                        dateTo: newValue,
                                        dateFrom: datefrom.datetimebox('getValue')
                                    }
                                })
                            }
                        }
                    });
                    table.datagrid({
                        toolbar: '#journal-toolbar',
                        //popupmenu:'#journal-popupmenu',
                        url: `${options.getUrl({
                            document_type: options.document_type,
                            target: options.all,
                            option: options.json
                        })}`,
                        loadFilter: function (data) {
                            datefrom.datetimebox('setValue', data.date_from);
                            dateto.datetimebox('setValue', data.date_to);
                            return data;
                        },
                        onRowContextMenu: function (e, index, row) {
                            e.preventDefault();
                            // Включаем контекстное меню для редактирования таблицы документов
                            popupmenu.menu('show', {
                                left: e.pageX,
                                top: e.pageY
                            });
                        }
                    });

                    $.data(target, 'journal', {
                        table: table,
                        popupmenu: popupmenu,
                        datefrom: datefrom,
                        dateto: dateto
                    });
                } else if (index > 0) {
                    // Тут документ
                    tab.addClass('easydoc-document');
                    // Инициализация документа
                    easydoc.tabs('update', {
                        tab: tab,
                        options: {
                            title: tabtitle,
                            content: documentOpen(target, options)
                        }
                    });
                } else {
                    $.error('jQuery.easydoc: index of tab error');
                }
            }
        }).tabs('add', {
            //Принудительно делаем индекс журнала 0
            index: 0,
            closable: false,
            selected: true
        });
        return easydoc.tabs('getTab', 0);
    }

    /**
     * Функция инициализатор плагина easyDoc
     * @param      target   (object DOM)        Объект DOM класса easyui-tabs  для активации на нем плагина easyDoc
     * @param      options  (object)            Объект с настройками плагина
     * @return              (object)            Объект содержащий {настройки, ициализированные jQuery.easydoc, jQuery.journal}
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
        // Создадим нулевую вкладку
        let result = initTabs(target, options);
        return {
            options: options,
            easydoc: target,  // или easydoc?
            journal: result
        };
    }

    /**
     * Функция "точка" вызова плагина easyDoc
     * @param      options  (string, необяз)    Имя вызываемого метода
     * @param      params   (object)            Параметры настройки плагина
     * @return     this     (object)            Объект экземпляра для поддержки цепочки вызовов
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
        options: function (jq) {
            return $.data(jq[0], 'easydoc').options;
        },
        easydoc: function (jq) {
            return $.data(jq[0], 'easydoc').easydoc;
        },
        journal: function (jq) {
            return $.data(jq[0], 'easydoc').table;
        },
        create: function (jq, params) {
            jq.each(function () {
                alert('create');
            });
        },
        edit: function (jq, params) {
            jq.each(function () {
                alert('edit');
            })

        }
    };

    $.fn.easydoc.defaults = {
        option: null,                       // Url параметр запроса {json, ...}
        json: `json/`,
        all: `all`,
        edit: `edit/`,
        new: ``,
        target: `new`,

        document_date: `01/01/2001`,
        selector: '.easydoc-journal',

        timedelta: 90,     // период журнала в днях
        dateto: null,
        datefrom: null,

        /* Настройки локализации */
        title_create: 'Create',
        title_edit: 'Edit',
        title_remove: 'Remove',
        title_copy: 'Copy',
        title_paste: 'Paste',
        title_dublicate: 'Dublicate',
        title_print: 'Print',
        title_reload: 'Reload',
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

        getTitle: function (params) {
            params = params || {};
            // Если не пришла дата, то возьмем ее из defaults
            if (params.index === 0) return this.journal_title;
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

