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
        let menu = $('#journal-popupmenu');
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
     * Функция создания панели журнала документов
     * @param       target      (object DOM)    DOM объект плагина
     * @param       options     (object)        Настройки плагина
     */
    function journalCreate(target, options) {
        //let easydoc = $(target);
        //let tab = easydoc.tabs('getTab', 0);
        let table = $('<table></table>', {
            'id': "journal-table",
            'class': "easyui-datagrid",
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
        // buttonRemove
        $('<a></a>', {
            'id': "journal-removedoc",
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
     * Функция создания панели документа
     * @param       target      (object DOM)    DOM объект плагина
     * @param       options     (object)        Настройки плагина
     */
    function documentCreate(target, options) {
        let table = $('<table></table>', {
            'id': `document-table-`, //${options.index}
            'class': "easyui-datagrid",
            'data-options': `
                            fit:true,
                            fitColumns:true,
                            toolbar:'#document-toolbar-',
                            idField:'id',
                            textField:'name',
                            rownumbers:true,
                            autoRowHeight:true,
                            singleSelect:true,
                            showFooter:true
                            `
        });
        let thead = $('<thead></thead>').appendTo(table);
        let tr = $('<tr></tr>').appendTo(thead);
        $('<th></th>', {
            'data-options': `field:'ck',width:2,checkbox:true`
        }).appendTo(tr);
        $('<th></th>', {
            'data-options': `field:'itemId',width:3,align:'center',title:'${options.title_field_article}'`
        }).appendTo(tr);
        $('<th></th>', {
            'data-options': `field:'itemName',width:30,align:'center',title:'${options.title_field_name}',
                    editor:{
                        type: 'combotreegrid',
                        options: {
                            idField: 'itemId',
                            treeField: 'itemName',
                            url:'/catalog/product/json/',
                            fit:true,
                            fitColumns:true,
                            animate:true,
                            panelWidth: '50%',
                            loadFilter: function(rows){return productLoadFilter(rows);},
                            columns: [[
                                {field:'itemId',title:'Item ID',width:'10%'},
                                {field:'itemName',title:'Name',width:'80%'},
                                {field:'parentId',title:'parentId',width:'10%'}
                            ]]
                        }}`
        }).appendTo(tr);
        $('<th></th>', {
            'data-options': `field:'measure',width:5,align:'center',title:'${options.title_field_measure}',
                    editor:{
                        type: 'combogrid',
                        options: {
                            idField:'id',
                            textField: 'name',
                            scrollbarSize:0,
                            url:'/system/measure/json/',
                            columns:[[
                                    {field:'name',
                                     title:'Ед. изм.',
                                     width:'100%'},
                            ]]
                        }}`
        }).appendTo(tr);
        $('<th></th>', {
            'data-options': `field:'quantity',width:5,align:'center',title:'${options.title_field_quantity}',
                    editor:{
                        type: 'numberbox',
                        options: {
                            precision:2,
                        }}`
        }).appendTo(tr);
        $('<th></th>', {
            'data-options': `field:'country',width:10,align:'center',title:'${options.title_field_country}',
                    editor:{
                        type: 'combogrid',
                        options: {
                            idField: 'id',
                            textField: 'name',
                            scrollbarSize:0,
                            url:'/system/country/json/',
                            columns:[[
                                    {field:'name',
                                     title:'Страна изготовитель',
                                     width:'100%'},
                                    ]]
                        }}`
        }).appendTo(tr);
        $('<th></th>', {
            'data-options': `field:'cost',width:10,align:'center',title:'${options.title_field_cost}',
                    editor:{
                        type: 'numberbox',
                        options: {
                            precision:2,
                        }}`,
            'formatter': `${options.formatter}`,
        }).appendTo(tr);
        $('<th></th>', {
            'data-options': `field:'tax',width:10,align:'center',title:'${options.title_field_tax}',
                    editor:{
                        type: 'numberbox',
                        options: {
                            precision:2,
                        }}`,
            'formatter': `${options.formatter}`
        }).appendTo(tr);
        $('<th></th>', {
            'data-options': `field:'total',width:10,align:'center',title:'${options.title_field_total}',
                    editor:{
                        type: 'numberbox',
                        options: {
                            precision:2,
                        }}`,
            'formatter': `${options.formatter}`
        }).appendTo(tr);

        let toolbar = $('<div></div>', {
            'id': "document-toolbar-",
            'style': "padding: 5px"
        }).appendTo(table);
        let form = $('<form></form>', {
            'id': "document-form"
        }).appendTo(toolbar);
        // Номер документа в тулбаре
        $('<input>', {
            'id': "document-number",
            'name': "number",
            'class': "easyui-textbox",
            'placeholder': "0000000001",
            'required': "required",
            'label': `${options.document_type_name} №`,
            'title': "document:",
            'data-options': "width:250,labelWidth:100,labelPosition:'before',labelAlign:'right'"
        }).appendTo(form);
        // Дата документа в тулбаре
        $('<input>', {
            'id': "document-date",
            'name': "date",
            'class': "easyui-datetimebox",
            'placeholder': "31/10/1985",
            'required': "required",
            'label': `${options.title_dateFrom}:`,
            'title': "From:",
            'data-options': `width:220,labelWidth:50,labelPosition:'before',labelAlign:'right',
                            currentText:'${options.title_today}',closeText:'${options.title_close}'
                            `
        }).appendTo(form);
        // Продавец
        $('<select></select>', {
            'id': "document-receiver-",
            'name': "receiver",
            'label': `${options.title_seller}:`,
            'data-options': `labelPosition:'top'`
        }).appendTo(form);


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
                    tab.find('a#journal-createdoc').bind('click.easydoc', function () {
                        easydoc.easydoc('create')
                    });
                    tab.find('#journal-editdoc').bind('click.easydoc', function () {
                        easydoc.easydoc('edit')
                    });
                    tab.find('#journal-removedoc').bind('click.easydoc', function () {
                        easydoc.easydoc('remove')
                    });

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
                            content: documentCreate(target, options)
                        }
                    });

                    /*
                    let table = tab.find('#document-table-' + index);
                    let popupmenu = documentMenuCreate(target, options);

                    table.// Активация cell-editing функции, а также запуск дополнительных возможностей datagrid
                    datagrid('enableCellEditing').datagrid({
                        onEndEdit: function (rowIndex, row, changes) {
                            // get all changes
                            for (let name in changes) {
                                // Изменяем текствовое поле на  c id на name
                                let ed = table.datagrid('getEditor', {index: rowIndex, field: name});
                                row.name = $(ed.target).combotreegrid('getText');

                                // Автокалькуляция значений в строках
                                if (changes.cost) {
                                    // autosumm column   total = quantity * cost
                                    $(this).datagrid('updateRow', {
                                        index: rowIndex,
                                        row: {
                                            total: (row.cost * row.quantity).toFixed(2)
                                        }
                                    });
                                } else if (changes.quantity) {
                                    // alert(changes.quantity);
                                    // autosumm column   total = quantity * cost
                                    $(this).datagrid('updateRow', {
                                        index: rowIndex,
                                        row: {
                                            total: (row.cost * row.quantity).toFixed(2)
                                        }
                                    });
                                } else if (changes.total) {
                                    // alert(changes.total);
                                    // autosumm column   cost = total / quantity
                                    $(this).datagrid('updateRow', {
                                        index: rowIndex,
                                        row: {
                                            cost: (row.total / row.quantity).toFixed(2)
                                        }
                                    });
                                }
                            }
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
                    */

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

    function documentOpen(target, params) {
        let easydoc = $(target);
        easydoc.tabs('add', {
            //index: 1,  //params.index,
            //title: index,
            closable: true,
            selected: true
        });
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
            easydoc: target,
            journal: result
        };
    }

    /**
     * Функция создание иерархии каталога продукции на Фронтэнде
     * @param       rows        (Array)         Полученные данные
     * @returns     {Array}
     */
    function productLoadFilter(rows) {
        function exists(rows, parentId) {
            for (var i = 0; i < rows.length; i++) {
                if (rows[i].itemId == parentId) return true;
            }
            return false;
        }

        var nodes = [];
        // get the top level nodes
        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            if (!exists(rows, row.parentId)) {
                nodes.push({
                    itemId: row.itemId,
                    itemName: row.itemName,
                    state: row.state,
                    parentId: row.parentId
                    //добавить еще данные
                });
            }
        }
        var toDo = [];
        for (var i = 0; i < nodes.length; i++) {
            toDo.push(nodes[i]);
        }
        while (toDo.length) {
            var node = toDo.shift();    // the parent node
            // get the children nodes
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i];
                if (row.parentId == node.itemId) {
                    var child = {
                        itemId: row.itemId,
                        itemName: row.itemName,
                        state: row.state,
                        parentId: row.parentId
                    };
                    if (node.children) {
                        node.children.push(child);
                    } else {
                        node.children = [child];
                    }
                    toDo.push(child);
                }
            }
        }
        return nodes;
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
                documentOpen(this, params);
            });
        },
        edit: function (jq) {
            jq.each(function () {
                alert('edit');
            })
        },
        remove: function (jq) {
            jq.each(function () {
                alert('remove');
            });
        },
        copy: function (jq) {
            jq.each(function () {
                alert('copy');
            });
        },
        paste: function (jq) {
            jq.each(function () {
                alert('paste');
            });
        },
        dublicate: function (jq) {
            jq.each(function () {
                alert('dublicate');
            });
        },
        print: function (jq) {
            jq.each(function () {
                alert('print');
            });
        },
        reload: function (jq) {
            jq.each(function () {
                alert('reload');
            });
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
        formatter: 'formatDollar',

        /* Настройки локализации */
        title_create: 'Create',
        title_edit: 'Edit',
        title_remove: 'Remove',
        title_copy: 'Copy',
        title_paste: 'Paste',
        title_dublicate: 'Dublicate',
        title_print: 'Print',
        title_reload: 'Reload',
        title_dateTo: 'To',
        title_dateFrom: 'From',
        title_today: 'Today',
        title_close: 'Close',
        title_seller: 'Seller',
        title_buyer: 'Buyer',

        document_type: `all`,
        document_type_name: `document`,
        document_type_name_new: `a new document`,
        document_type_name_plural: `documents`,
        journal_title: 'documents\'s journal',


        title_field_document: '<p>Kind, number, date of document</p>',
        title_field_seller: '<p>Seller</p>',
        title_field_buyer: '<p>Buyer</p>',
        title_field_active: '<p>Active</p>',
        title_field_article: '<p>Article</p>',
        title_field_name: '<p>The name of goods, works, services</p>',
        title_field_measure: '<p>Measure <br> (pcs/kg)</p>',
        title_field_quantity: '<p>Quantity<br><em>(pcs)</em></p>',
        title_field_country: '<p>Country of<br>production</p>',
        title_field_cost: '<p>Cost of<br>piece</p>',
        title_field_tax: '<p>Tax</p>',
        title_field_total: '<p>Total</p>',


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

