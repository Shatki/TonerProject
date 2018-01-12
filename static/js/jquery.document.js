// EASYUI переименование tabs без перезагрузки
// Предотвращение выбора категории в combotreegrid
$.extend(
    $.fn.combotreegrid.defaults.onBeforeSelect = function (row) {
        // Запрет выбора таких ID
        if (row.itemId.substring(0, 3) == 'DIR') {
            return false;
        }
    }
);

(function ($) {
    var methods = {
        init: function (options) {
            //alert('enable');
            return this.each(function() {
                var table = $(this);
                var popupmenu = $(table.datagrid('options').popupmenu);
                var buttonAdd = $(table.datagrid('options').toolbar).find('a.document-newdoc');
                table.
                datagrid({
                    clickToEdit: false,
                    dblclickToEdit: true
                }).
                datagrid('enableCellEditing').
                datagrid({
                    onEndEdit: function (rowIndex, row, changes) {
                        // get all changes
                        for (var name in changes) {
                            // Изменяем текствовое поле на  c id на name
                            var ed = $(this).datagrid('getEditor', {index: rowIndex, field: name});
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
                }).
                datagrid({
                    onRowContextMenu: function (e, index, row) {
                        e.preventDefault();
                        // Включаем контекстное меню для редактирования таблицы документов
                        popupmenu.menu('show', {
                            left: e.pageX,
                            top: e.pageY
                        });
                    }
                });

                buttonAdd.bind('click.doctable', methods.new);
            });

        },
        destroy: function () {
            return this.each(function () {
                $(window).unbind('.doctable');
            })
        },
        add: function (params) {
            var doctabs = $('.doctable-tabs');
            //alert(params.title);
            if (doctabs.tabs('exists', params.title)) {
                doctabs.tabs('select', params.title);
            } else {
                $.ajax({
                    url: params.url,
                    cache: true,
                    success: function (html) {
                        doctabs.tabs('add', {
                            //id: doc_id.substring(1),
                            title: params.title,
                            content: html,
                            closable: true
                        });
                    }
                });
            }
            return false;
        },
        new: function () {
            var date = table.datebox.defaults.formatter(new Date());
            methods.add({
                title: 'Новая накладная от ' + date,
                url: '/document/consignment/new/'
            });
            return false;
        },
        rename: function () {
            var doctabs = $('.doctable-tabs');
            var t = doctabs.tabs('getSelected');
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
            doctabs.tabs('updateTitle', {
                tab: t,
                title: title
            });
        },
        edit: function (param) {
            //alert(doc_id);
            var doc = $(this);
            if (!param) {
                param = doc.datagrid('cell');
                if (param) {
                    doc.datagrid('gotoCell', param).datagrid('editCell', param);
                }
            }
        },
        copy: function () {
            var doc = $(this);
            var rowIndex = doc.datagrid('cell').index;
            //var row = doc.datagrid('getRows')[rowIndex];
            setCookie('bufferItem', rowIndex);
        },
        paste: function () {
            var doc = $(this);
            //Вставляем в конец списка
            var rowIndex = doc.datagrid('getRows').length;
            var row = doc.datagrid('getRows')[getCookie('bufferItem')];
            row.itemId = rowIndex;
            doc.datagrid('insertRow', {
                    index: rowIndex,
                    row: row
                }
            );
            //$.ajax({
            //    url: '/document/consignment/' + doc_id + '/item/paste/',
            //    method: 'POST',
            //    data: {'item': getCookie('copyItem')},
            //    cache: false,
            //    success: function (data) {
            //        if (data == 'Ok') {
            //            // Пока кокой-то деревянный способ
            //            // alert('Данные получены');
            //            $('#item-table-consignment-' + doc_id).datagrid('reload');    // reload the data table
            //        } else {
            //            alert(data);
            //            // Данные получены кривые
            //            // location.href = "#";
            //            // location.reload();
            //        }
            //    }
            //});
        },
        dublicate: function () {
            var doc = $(this);
            var rowIndex = doc.datagrid('cell').index;
            var row = doc.datagrid('getRows')[rowIndex];
            row.itemId = rowIndex;
            doc.datagrid('insertRow', {
                    index: rowIndex,
                    row: row
                }
            );
        }
    };
    $.fn.document = function (method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Метод с именем ' + method + ' не существует для jQuery.document');
        }
    };
    $.fn.document.defaults = {
        selector: '.document',
        url: null
    }
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
// Активация cell-editing функции, а также запуск дополнительных возможностей datagrid
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
function editDoc() {
    var row = $('#docs').datagrid('getSelected');
    if (row) {
        addTab(row.name, '/document/consignment/' + row.id + '/edit/');
    }
}

function closeDoc() {
    var jqtab = $('#doc-tabs');
    var t = jqtab.tabs('getSelected');
    var index = jqtab.tabs('getTabIndex', t);
    // Общий журнал не закрывается
    if (index) {
        jqtab.tabs('close', index);
    }
}

function printDoc(doc_id) {
    window.open('/form/consignment/' + doc_id + '/print/pdf/', '_blank');
    //location.href='/form/consignment/' + doc_id +'/print/pdf/';
}

function destroyDoc() {
    var maintab = $('#docs');
    var row = maintab.datagrid('getSelected');
    if (row) {
        $.ajax({
            method: 'POST',
            url: '/document/consignment/' + row.id + '/delete/',
            cache: false,
            success: function () {
                maintab.datagrid('reload');
            }
        });
    }
}

// Скрипты для главного меню документа
function saveDoc(doc_id) {
    var doc_form = $('#doc-req-fm-consignment-' + doc_id);
    // Записываем в том случае, если есть хотя бы одна позиция в таблице продукции
    //alert($("#item-table-consignment-" + doc_id).datagrid('getData').total);
    if ($("#item-table-consignment-" + doc_id).datagrid('getData').total > 0) {
        if (doc_form.form('validate')) {
            var data = doc_form.serialize();
            $.ajax({
                url: '/document/consignment/' + doc_id + '/save/',
                method: 'POST',
                data: data,
                cache: false,
                success: function (data) {
                    if (data == 'Ok') {
                        // Пока кокой-то деревянный способ
                        alert(' Документ успешно сохранен');
                        //$('#item-add-dlg-consignment-' + doc_id).dialog('close');      // close the dialog
                        //$('#item-table-consignment-' + doc_id).datagrid('reload');    // reload the data table
                    } else {
                        alert(data);
                        // Данные получены кривые

                    }
                }
            });

        }
    } else {
        alert('Заполните таблицу товаров!');
    }
}

// Функция создание иерархии каталога продукции на Фронтэнде
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

function formatDollar(value) {
    if (value) {
        return '$' + value;
    } else {
        return '';
    }
}

function formatRouble(value) {
    if (value) {
        return 'P' + value;
    } else {
        return '';
    }
}

function editItem(doc_id, param) {
    //alert(doc_id);
    var doc = $(doc_id);
    if (!param) {
        param = doc.datagrid('cell');
        if (param) {
            doc.datagrid('gotoCell', param).datagrid('editCell', param);
        }
    }
}

function addItem(doc_id) {
    var doc = $(doc_id);
    var rowIndex = doc.datagrid('getRows').length + 1;
    doc.datagrid('insertRow', {
            index: rowIndex,
            row: {
                id: rowIndex,
                itemId: 'ITM-' + rowIndex,
                itemName: 'Не выбран',
                measure: '-',   //Переделать
                country: '-',
                cost: '0.00',
                quantity: '0.00',
                tax: '0.00',
                total: '0.00'
            }
        }
    );

    editItem(doc_id, {
        index: rowIndex,
        field: 'itemName'
    });
}

function copyItem(doc_id) {
    var doc = $(doc_id);
    var rowIndex = doc.datagrid('cell').index;
    //var row = doc.datagrid('getRows')[rowIndex];
    setCookie('bufferItem', rowIndex);
    //alert(row.toSource());
}

// Вставка скопированного элемента из буфера
function pasteItem(doc_id) {
    var doc = $(doc_id);
    //Вставляем в конец списка
    var rowIndex = doc.datagrid('getRows').length;
    var row = doc.datagrid('getRows')[getCookie('bufferItem')];
    row.itemId = rowIndex;
    doc.datagrid('insertRow', {
            index: rowIndex,
            row: row
        }
    );
    //$.ajax({
    //    url: '/document/consignment/' + doc_id + '/item/paste/',
    //    method: 'POST',
    //    data: {'item': getCookie('copyItem')},
    //    cache: false,
    //    success: function (data) {
    //        if (data == 'Ok') {
    //            // Пока кокой-то деревянный способ
    //            // alert('Данные получены');
    //            $('#item-table-consignment-' + doc_id).datagrid('reload');    // reload the data table
    //        } else {
    //            alert(data);
    //            // Данные получены кривые
    //            // location.href = "#";
    //            // location.reload();
    //        }
    //    }
    //});
}

// Дубликация элемента в документе без записи в буффер
function dublicateItem(doc_id) {
    var doc = $(doc_id);
    var rowIndex = doc.datagrid('cell').index;
    var rows = doc.datagrid('getRows');
    var row = rows[rowIndex];
    row.itemId = rows.length;
    doc.datagrid('insertRow', {
            index: row.itemId,
            row: row
        }
    );
}

// Дубликация элемента в документе
function deleteItem(doc_id) {
    // Доработать функционал выделения и удаления, возможно множественного удаления
    var doc = $(doc_id);
    rowIndex = doc.datagrid('cell').index;
    //checkedIndex = doc.datagrid('getChecked');
    //alert(checkedIndex);
    if (rowIndex) {
        doc.datagrid('deleteRow', rowIndex);
    }
    //if(checkedIndex){
    //    doc.datagrid('deleteRow', checkedIndex);
    //}else{
    //    doc.datagrid('deleteRow', rowIndex);
    //}
}

// Activate pop-up context menu in documents
function popupMenuDispatcher(action) {
    // находим общий журнал документов
    var tab = $('#doc-tabs');
    // выбираем соответствующую tab панель
    var selected = tab.tabs('getSelected');
    // узнаем его индекс  панели в таблице
    var tabIndex = tab.tabs('getTabIndex', selected);
    //alert(tabIndex);
    if (tabIndex) {
        // Действия в документе
        var table_id = '#document-item-table-' + $("<div/>",
            {"html": selected.panel('options').content}).find('#doc-id').html();
        switch (action) {
            case 'add':
                addItem(table_id);
                break;
            case 'edit':
                editItem(table_id);
                break;
            case 'remove':
                deleteItem(table_id);
                break;
            case 'copy':
                copyItem(table_id);
                break;
            case 'paste':
                pasteItem(table_id);
                break;
            case 'dublicate':
                dublicateItem(table_id);
                break;
            case 'reload':
                $(table_id).datagrid('reload');    // reload the data table
                break;
            case 'save':
                saveDoc(table_id);
                break;
            default:
                break;
        }
    } else {
        switch (action) {
            case 'add':
                var date = new Date();
                var y = date.getFullYear();
                var m = date.getMonth() + 1;
                var d = date.getDate();
                newDoc(d + '/' + m + '/' + y);
                break;
            case 'edit':
                editDoc();
                break;
            case 'remove':
                destroyDoc();
                break;
            case 'reload':
                $('#docs').datagrid('reload');
                break;
            default:
                break;
        }
    }
}

// В стадии разработки для созданияя плагина 'document'
