// В стадии разработки для созданияя плагина 'document'
(function ($) {
    var methods = {
        'add': function (doc_id) {
            var doc = $(doc_id);
            var rowIndex = doc.datagrid('getRows').length;
            doc.datagrid('insertRow', {
                    index: rowIndex,
                    row: {
                        itemId: 'ITM-' + rowIndex + 1,
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
            // autoedit 'item' field added's row
            param = doc.datagrid('cell');
            if (param) {
                doc.datagrid('gotoCell', param).datagrid('editCell', param);
            }
        },
        'edit': function (doc_id, param) {
            //alert(doc_id);
            var doc = $(doc_id);
            if (!param) {
                param = doc.datagrid('cell');
                if (param) {
                    doc.datagrid('gotoCell', param).datagrid('editCell', param);
                }
            }
        },
        'copy': function (doc_id) {
            var doc = $(doc_id);
            var rowIndex = doc.datagrid('cell').index;
            //var row = doc.datagrid('getRows')[rowIndex];
            setCookie('bufferItem', rowIndex);
        },
        'paste': function (doc_id) {
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
        },
        'dublicate': function (doc_id) {
            var doc = $(doc_id);
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
            $.error('Метод с именем ' + method + ' не существует для jQuery.tooltip');
        }
    };
})(jQuery);



// Tab functions
function addTab(title, url) {
    if ($('#doc-tab').tabs('exists', title)) {
        $('#doc-tab').tabs('select', title);
    } else {
        $.ajax({
            url: url,
            cache: true,
            success: function (html) {
                $('#doc-tab').tabs('add', {
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
    var jqtab = $('#doc-tab');
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
function renameDocTab() {
    $('#common-tab').title()
}

// Document functions
// Активация cell-editing функции, а также запуск дополнительных возможностей datagrid
function enableDoc(doc_id) {
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
        },
        onRowContextMenu: function (e, index, row) {
            e.preventDefault();
            $('#mm').menu('show', {
                left: e.pageX,
                top: e.pageY
            });
            if (index >= 0) {
                //($(this).datagrid('cell'));
                //console.log(index);
            } else {
                alert(row.toSource());
            }
        }

    });
}


function newDoc(date) {
    addTab('Новая накладная от ' + date, '../consignment/new/');
}

function editDoc() {
    var row = $('#common-tab').datagrid('getSelected');
    if (row) {
        addTab(row.name, '/document/consignment/' + row.id + '/edit/');
    }
}

function closeDoc() {
    var jqtab = $('#doc-tab');
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
    var row = $('#common-tab').datagrid('getSelected');
    if (row) {
        $.ajax({
            method: 'POST',
            url: '/document/consignment/' + row.id + '/delete/',
            cache: false,
            success: function () {
                $('#common-tab').datagrid('reload');
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
    var rowIndex = doc.datagrid('getRows').length;
    doc.datagrid('insertRow', {
            index: rowIndex,
            row: {
                itemId: 'ITM-' + rowIndex + 1,
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
    // Сделать чтоб idшник сам находился #item-table-consignment-
    var tab = $('#doc-tab');
    var selected = tab.tabs('getSelected');
    var tabIndex = tab.tabs('getTabIndex', selected);
    //alert(tabIndex);
    if (tabIndex) {
        // Действия в документе
        switch (action) {
            case 'add':
                addItem($("<div/>",
                    {"html": selected.panel('options').content}).find('#doc-id').html());
                break;
            case 'edit':
                editItem('#item-table-consignment-' + $("<div/>",
                        {"html": selected.panel('options').content}).find('#doc-id').html());
                break;
            case 'remove':
                deleteItem('#item-table-consignment-' + $("<div/>",
                        {"html": selected.panel('options').content}).find('#doc-id').html());
                break;
            case 'copy':
                copyItem('#item-table-consignment-' + $("<div/>",
                        {"html": selected.panel('options').content}).find('#doc-id').html());
                break;
            case 'paste':
                pasteItem('#item-table-consignment-' + $("<div/>",
                        {"html": selected.panel('options').content}).find('#doc-id').html());
                break;
            case 'dublicate':
                dublicateItem('#item-table-consignment-' + $("<div/>",
                        {"html": selected.panel('options').content}).find('#doc-id').html());
                break;
            case 'reload':
                var doc_id = $("<div/>",
                    {"html": selected.panel('options').content}).find('#doc-id').html();
                $(doc_id).datagrid('reload');    // reload the data table
                break;
            case 'save':
                saveDoc($("<div/>",
                    {"html": selected.panel('options').content}).find('#doc-id').html());
                break;
            default:
                break;
        }
    } else {
        switch (action) {
            case 'add':
                newDoc();
                break;
            case 'edit':
                editDoc();
                break;
            case 'remove':
                destroyDoc();
                break;
            case 'reload':
                $('#common-tab').datagrid('reload');
                break;
            default:
                break;
        }
    }
}

// EASYUI переименование tabs без перезагрузки
// Предотвращение выбора категории в combotreegrid
$.extend(
    $.fn.combotreegrid.defaults.onBeforeSelect = function (row) {
        // Запрет выбора таких ID
        if (row.itemId.substring(0, 3) == 'DIR') {
            return false;
        }
    },
    $.fn.tabs.methods, {
        updateTitle: function (jq, param) {
            return jq.each(function () {
                var t = $(param.tab);
                var opts = t.panel('options');
                opts.title = param.title;
                opts.tab.find('.tabs-title').html(param.title);
            })
        }
    },
    $.fn.tabs.methods, {
        updateTitle: function (jq, param) {
            return jq.each(function () {
                var t = $(param.tab);
                var opts = t.panel('options');
                opts.title = param.title;
                opts.tab.find('.tabs-title').html(param.title);
            })
        }
    },
    // Методы для управления выводом datebox
    $.fn.datebox.defaults.parser = function (s) {
        var dateParts = s.split("/", 3);
        if (dateParts[0] != s) {
            return new Date(dateParts[2], (dateParts[1] - 1), dateParts[0]);
        } else {
            return new Date();
        }
    },
    $.fn.datebox.defaults.formatter = function (date) {
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        var d = date.getDate();
        return d + '/' + m + '/' + y;
    }
);

$(document).ready(function () {
    if (!navigator.cookieEnabled) {
        alert('Включите cookie для комфортной работы с этим сайтом');
    }
});
;


