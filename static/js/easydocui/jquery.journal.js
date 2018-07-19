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
 * journal - EasyDocUI for jQuery
 *
 * Dependencies:
 *
 *
 *
 */
(function ($) {
    /**
     * Динамическое создание меню для journal
     */
    function popupmenu(target, index, row) {
        // var menu = $('<div id="journal-popupmenu" class="easyui-menu easydocui-popupmenu"></div>').appendTo(target);
        var menu = $.data(target, 'journal').menu;
        //alert(menu.html().toSource());
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
     * Функция открытия документа из journal datagrid в новой tab вкладки для редактирования
     */
    function openDoc(target, params) {
        var _easydocui = $(target).easydocui('journal');
        //alert(easydocui.tabs('tabs').toSource());
        alert(_easydocui.html().toSource());


        if (_easydocui.tabs('exists', params.title)) {
            // Если такой документ открыт, то переключимся на нее
            _easydocui.tabs('select', params.title);
        } else {
            alert(params.url);
            $.ajax({
                url: params.url,
                cache: true,
                success: function (html) {
                    //Найдем в полученом HTML id документа и добавим его в data-options к tabs
                    var idDoc = +($("<div/>", {"html": html}).find('#doc-id').html());
                    if (idDoc >= 0) {
                        _easydocui.tabs('add', {
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
    }

    /**
     * Редактирование документа, выделенного в journal datagrid
     */
    function editDoc(target) {
        var table = $.data(target, 'journal').table;
        //alert(table.html().toSource());
        var row = table.datagrid('getSelected');
        if (row) {
            openDoc(target, {
                title: row.name,
                url: '/document/consignment/' + row.id + '/edit/',
                idDoc: row.id
            });
        }
        return this;
    }

    /**
     * "Мягкое" удаление документа, выделенного в journal datagrid
     */
    function removeDoc(target) {
        var table = $.data(target, 'journal').table;
        var row = table.datagrid('getSelected');
        if (row) {
            $.ajax({
                method: 'POST',
                url: '/document/consignment/' + row.id + '/delete/',
                cache: false,
                success: function () {
                    table.datagrid('reload');
                }
            });
        }
        return this;
    }

    /**
     * Копирование документа, выделенного в journal datagrid в буфер cookie
     */
    function copyDoc(target) {
        var table = $.data(target, 'journal').table;
        var row = table.datagrid('getSelected');
        if (row) {
            //alert(row.toString());
            $.data(target, 'copiedDoc', row);
            //setCookie('copiedDoc', JSON.stringify(row));
        }
    }

    /**
     * Добавление документа, в journal datagrid из буфера
     */
    function pasteDoc(target) {
        var table = $.data(target, 'journal').table;
        //Вставляем в конец списка
        var rowIndex = table.datagrid('getRows').length;
        var row = $.data(target, 'copiedDoc');
        row.itemId = rowIndex;
        /*
        table.datagrid('insertRow', {
                index: rowIndex,
                row: row
            }
        );
        */
        $.ajax({
            url: '/document/consignment/' + row.id + '/item/paste/',
            method: 'POST',
            data: {'item': row},
            cache: false,
            success: function (data) {
                if (data === 'Ok') {
                    // Пока кокой-то деревянный способ
                    alert('Данные получены');
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

    /**
     * Создание дубликата документа, в journal datagrid
     */
    function dublicateDoc(target) {
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

    /**
     * Переименование панели документа, в journal tabs
     * */
    function renameDoc(target) {
        var doctabs = $('.journal-tabs');
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
        return false;
    }

    /**
     * Активация плагина journal на таблице datagrid
     */
    function init(target, options) {
        var journal = $(target);
        if (journal) {
            var table = journal.find('.easyui-datagrid');
            if (!table) {
                $.error('jQuery.journal: Не могу обнаружить datagrid table');
                return false;
            } else {
                table.addClass('easydocui-journal-table')
            }
        } else {
            $.error('jQuery.journal: Не могу обнаружить easydocui-journal');
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

    /**
     * Деакцивация плагина
     */
    function destroy(target) {
        var journal = $.data(target, 'journal').table;
        $(target).remove();
    }

    /**
     * Привязка событий
     */
    function bindEvents(target) {
        var opts = $.data(target, 'journal').options;
        var toolbar = $.data(target, 'journal').toolbar;
        //var panel = $.data(target, 'combo').panel;
        var buttonCreate = toolbar.find('a.easydocui-createdoc');
        var buttonEdit = toolbar.find('a.easydocui-editdoc');
        var buttonRemove = toolbar.find('a.easydocui-removedoc');

        $(document).unbind('.journal');
        toolbar.unbind('.journal');

        buttonCreate.bind('click.journal', function (e) {
            $(target).journal('new');
        });
        buttonEdit.bind('click.journal', function (e) {
            $(target).journal('edit');
        });
        buttonRemove.bind('click.journal', function (e) {
            $(target).journal('remove');
        });

    }

    $.fn.journal = function (options, param) {
        if (typeof options === 'string') {
            //alert('Строка');
            var result = $.fn.journal.methods[options];
            if (result) {
                return result(this, param);
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
                    //options: $.extend({}, $.fn.journal.defaults, parseOptions(this), options),
                    options: $.extend({}, $.fn.journal.defaults, options),
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
            bindEvents(this);
            //validate(this);
        });
    };

    $.fn.journal.methods = {
        options: function (jq) {
            return $.data(jq[0], 'journal').options;
        },
        table: function (jq) {
            return $.data(jq[0], 'journal').table;
        },
        journal: function (jq) {
            return $.data(jq[0], 'journal').journal;
        },
        destroy: function (jq) {
            return jq.each(function () {
                // Пока не работает
                destroy(this);
            });
        },
        add: function (jq, params) {
            return jq.each(function () {
                openDoc(this, params);
            })
        },
        new: function (jq) {
            return jq.each(function () {
                var date = $.fn.datebox.defaults.formatter(new Date());
                openDoc(this, {
                    title: 'Новая накладная от ' + date,
                    url: '/document/consignment/new/'
                });
            })
        },
        edit: function (jq) {
            return jq.each(function () {
                editDoc(this);
            })
        },
        remove: function (jq) {
            return jq.each(function () {
                removeDoc(this);
            })
        },
        copy: function (jq) {
            return jq.each(function () {
                copyDoc(this);
            })
        },
        paste: function (jq) {
            return jq.each(function () {
                pasteDoc(this);
            })
        },
        dublicate: function (jq) {

        },
        reload: function (jq) {
            return $.data(jq[0], 'journal').table.datagrid('reload');
        },
        print: function (jq) {
        },
        rename: function (jq) {
        }
    };

    $.fn.journal.defaults = {
        selector: '.easydocui-journal',
        url: '/document/'
    }
})(jQuery);