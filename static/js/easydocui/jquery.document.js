/**
 * EasyDocUI for jQuery.EasyUI
 *
 * Copyright (c) 2016-2018 Seliverstov Dmitriy. All rights reserved.
 *
 * Licensed under the freeware license: http://www.-------.-----/--------
 * To use it on other terms please contact us: -----@-------.---
 *
 */
/**
 * document - EasyDocUI for jQuery
 *
 * Dependencies:
 *
 *
 *
 */

$.extend(
    // Предотвращение выбора категории в combotreegrid
    $.fn.combotreegrid.defaults.onBeforeSelect = function (row) {
        // Запрет выбора таких ID
        if (row.itemId.substring(0, 3) == 'DIR') {
            return false;
        }
    }
);

(function ($) {
    /**
     * Динамическое создание меню для document
     */
    function popupmenu(target, index, row) {
        var menu = $.data(target, 'document').menu;
        menu.empty().menu('appendItem', {
            text: 'Создать',
            name: 'new',
            iconCls: 'icon-add'
        }).menu('appendItem', {
            text: 'Редактировать',
            name: 'edit',
            iconCls: 'icon-edit'
        }).menu('appendItem', {
            text: 'Удалить',
            name: 'remove',
            iconCls: 'icon-remove'
        }).menu('appendItem', {
            separator: true
        }).menu('appendItem', {
            text: 'Копировать',
            name: 'copy',
            iconCls: 'icon-copy'
        }).menu('appendItem', {
            text: 'Вставить',
            name: 'paste',
            iconCls: 'icon-paste'
        }).menu('appendItem', {
            text: 'Дублировать',
            name: 'remove',
            iconCls: 'icon-paste'
        }).menu('appendItem', {
            separator: true
        }).menu('appendItem', {
            text: 'Обновить',
            name: 'reload',
            iconCls: 'icon-reload'
        }).menu('appendItem', {
            text: 'Печать',
            name: 'print',
            iconCls: 'icon-print'
        }).menu('options').onClick = function (item) {
            $(target).journal(item.name)
        };
        return menu;
    }

    /**
     * Функция создание иерархии каталога продукции на Фронтэнде
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
     * Активация плагина document на таблице datagrid
     */
    function init(target, options) {
        var document = $(target);
        if (document) {
            var table = document.find(options.table);
            if (!document) {
                $.error('jQuery.document: Не могу обнаружить datagrid table');
                return false;
            }
            ///////
        } else {
            $.error('jQuery.document: Не могу обнаружить easydocui-document');
            return false;
        }

        //alert(journal.html().toSource());
        var menu = $(table.datagrid('options').menu);
        var toolbar = $(table.datagrid('options').toolbar);

        table.datagrid({
            clickToEdit: false,
            dblclickToEdit: true
        }).// Активация cell-editing функции, а также запуск дополнительных возможностей datagrid
        datagrid('enableCellEditing').datagrid({
            onEndEdit: function (rowIndex, row, changes) {
                // get all changes
                for (var name in changes) {
                    // Изменяем текствовое поле на  c id на name
                    var ed = table.datagrid('getEditor', {index: rowIndex, field: name});
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
            }
        }).datagrid({
            onRowContextMenu: function (e, index, row) {
                e.preventDefault();
                // Включаем контекстное меню для редактирования таблицы документов
                popupmenu.menu('show', {
                    left: e.pageX,
                    top: e.pageY
                });
            }
        });
        return {
            options: options,
            document: document,
            table: table,
            toolbar: toolbar,
            menu: menu
        };
    }

    /**
     * Привязка событий
     */
    function bindEvents(target) {
        return false
    }

    $.fn.document = function (options, param) {
        if (typeof options === 'string') {
            //alert('Строка');
            var result = $.fn.document.methods[options];
            if (result) {
                return result(this, param);
            } else {
                $.error('Метод с именем ' + options + ' не существует для jQuery.document');
                return this;
            }
        }
        options = options || {};
        //alert($(this).html().toSource());
        return this.each(function () {
            // Делаем инициализацию
            var state = $.data(this, 'document');
            if (state) {
                $.extend(state.options, options);
            } else {
                var r = init(this, options);
                alert(r.toSource());
                $.data(this, 'document', {
                    //options: $.extend({}, $.fn.journal.defaults, parseOptions(this), options),
                    options: $.extend({}, $.fn.document.defaults, options),
                    document: r.document,
                    table: r.table,
                    toolbar: r.toolbar,
                    menu: r.menu
                });
                $(this).removeAttr('disabled');
            }
            //$('input.combo-text', state.combo).attr('readonly', !state.options.editable);
            //setDisabled(this, state.options.disabled);
            //setSize(this);
            // Активация кнопок
            bindEvents(this);
            //validate(this);
        });
    };

    $.fn.document.methods = {
        options: function (jq) {
            return $.data(jq[0], 'document').options;
        },
        table: function (jq) {
            return $.data(jq[0], 'document').table;
        },
        document: function (jq) {
            return $.data(jq[0], 'document').document;
        },
        reload: function (jq) {
            return $.data(jq[0], 'document').table.datagrid('reload');
        }
    };

    $.fn.document.defaults = {
        selector: '.easydocui-document',
        url: '/document/'
    };
})(jQuery);


/*
// Tab functions
function addTab(title, url) {
    var doctabs = $('#doc-tabs');
    if (doctabs.tabs('exists', title)) {
        doctabs.tabs('select', title);
    } else {
        $.ajax({
            url: url,
            cache: true,
            success: function (html) {
                doctabs.tabs('add', {
                    //id: doc_id.substring(1),
                    title: title,
                    content: html,
                    closable: true
                });
            }
        });
    }
}

function renameTab(number, date) {
    var jqtab = $('#doc-tabs');
    var t = jqtab.tabs('getSelected');
    var titleParts = t.panel('options').title.split(" ", 5);

    if (!number) {
        number = titleParts[2];
    }
    if (titleParts[4]) {
        // Наименование будет из 5  частей
        if (!date) {
            date = titleParts[4];
        }
    } else {
        // Наименование будет из 4  частей
        if (!date) {
            date = titleParts[3];
        }
    }

    var title = 'Накладная № ' + number + ' от ' + date;

    jqtab.tabs('updateTitle', {
        tab: t,
        title: title
    });
}

// Смена наименования панели
// Возможно устрело --- СДЕЛАТЬ смена даты на панели журнала накладных
function docTabFilter(table_id, datefrom_id, dateto_id) {
    var dateFrom = $(datefrom_id);
    var dateTo = $(dateto_id);
    $(table_id).datagrid({
        loadFilter: function (data) {
            dateFrom.datetimebox('setValue', data.date_from);
            dateTo.datetimebox('setValue', data.date_to);
            return data;
        }
    });
}
*/
// Document functions
/*
function enablePopupMenu(doc_id, menu_id) {
    $(doc_id).datagrid({
        onRowContextMenu: function (e, index, row) {
            e.preventDefault();
            // Включаем контекстное меню для редактирования таблицы документов
            $(menu_id).menu('show', {
                left: e.pageX,
                top: e.pageY
            });
        }
    })
}


function enableDocTabLoader(url, table_id, datefrom_id, dateto_id) {
    var table = $(table_id);
    var dateFrom = $(datefrom_id);
    var dateTo = $(dateto_id);

    table.datagrid({
        loadFilter: function (data) {
            dateFrom.datetimebox('setValue', data.date_from);
            dateTo.datetimebox('setValue', data.date_to);
            return data;
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
    table.datagrid({url: url, method: 'post'});
}

function enableDoc(doc_id, popupmenu_id) {
    $(doc_id).datagrid({
        clickToEdit: false,
        dblclickToEdit: true
    }).datagrid('enableCellEditing').datagrid({
        onEndEdit: function (rowIndex, row, changes) {
            // get all changes
            for (var name in changes) {
                // Изменяем текствовое поле на  c id на name
                var ed = $(this).datagrid('getEditor', {index: rowIndex, field: name});
                row[name] = $(ed.target).combotreegrid('getText');

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
                    //alert(changes.quantity);
                    // autosumm column   total = quantity * cost
                    $(this).datagrid('updateRow', {
                        index: rowIndex,
                        row: {
                            total: (row.cost * row.quantity).toFixed(2)
                        }
                    });
                } else if (changes.total) {
                    //alert(changes.total);
                    // autosumm column   cost = total / quantity
                    $(this).datagrid('updateRow', {
                        index: rowIndex,
                        row: {
                            cost: (row.total / row.quantity).toFixed(2)
                        }
                    });
                }
            }
        }
    });
    if (popupmenu_id) {
        enablePopupMenu(doc_id, popupmenu_id);
    }
}

function newDoc(date) {
    addTab('Новая накладная от ' + date, '/document/consignment/new/');
}
*/

