// Предотвращение выбора категории в combotreegrid
$.extend($.fn.combotreegrid.defaults.onBeforeSelect = function (row) {
    // Запрет выбора таких ID
    if (row.itemId.substring(0, 3) == 'DIR') {
        return false;
    }
});


// Активация cell-editing функции, а также запуск дополнительных возможностей datagrid
function enableDoc(doc_id) {
    $(doc_id).datagrid({
        clickToEdit: false,
        dblclickToEdit: true
    }).datagrid('enableCellEditing').datagrid('gotoCell', {
        index: 0,
        field: 'name'
    }).datagrid({
        onEndEdit: function (rowIndex, row, changes) {
            // get all changes
            for (var k in changes) {
                // Изменяем текствовое поле на  c id на name
                var ed = $(this).datagrid('getEditor', {index: rowIndex, field: k});
                row[k] = $(ed.target).combotreegrid('getText');

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
                name: row.name,
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
                    name: row.name,
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

function copyItem(doc_id) {
    setCookie('copyItem', $("#item-table-consignment-" + doc_id).datagrid('getSelected').id);
}

// Вставка скопированного элемента из буфера
function pasteItem(doc_id) {
    $.ajax({
        url: '/document/consignment/' + doc_id + '/item/paste/',
        method: 'POST',
        data: {'item': getCookie('copyItem')},
        cache: false,
        success: function (data) {
            if (data == 'Ok') {
                // Пока кокой-то деревянный способ
                // alert('Данные получены');
                $('#item-table-consignment-' + doc_id).datagrid('reload');    // reload the data table
            } else {
                alert(data);
                // Данные получены кривые
                // location.href = "#";
                // location.reload();
            }
        }
    });
}

// Дубликация элемента в документе
function dublicateItem(doc_id) {
}