/**
 * EasyDocUI for jQuery
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
$.extend(
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
    $.fn.datebox.defaults.formatter = function (date) {
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        var d = date.getDate();

        function formatNumber(value) {
            return (value < 10 ? '0' : '') + value;
        }

        return formatNumber(d) + '/' + formatNumber(m) + '/' + y;
    },
    $.fn.datetimebox.defaults.formatter = function (date) {
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        var d = date.getDate();
        var h = date.getHours();
        var M = date.getMinutes();
        var s = date.getSeconds();

        function formatNumber(value) {
            return (value < 10 ? '0' : '') + value;
        }

        return formatNumber(d) + '/' + formatNumber(m) + '/' + y
            + ' ' + formatNumber(h) + ':' + formatNumber(M) + ':' + formatNumber(s);
    },
    $.fn.datetimebox.defaults.parser = function (s) {
        if ($.trim(s) === '') {
            return new Date();
        }
        var dt = s.split(' ');
        var ss = dt[0].split('/');
        var d = parseInt(ss[0], 10);
        var m = parseInt(ss[1], 10) - 1;
        var y = parseInt(ss[2], 10);
        if (dt.length >= 2) {
            var tt = dt[1].split(':');
            var hour = parseInt(tt[0], 10) || 0;
            var minute = parseInt(tt[1], 10) || 0;
            var second = parseInt(tt[2], 10) || 0;
        } else {
            var hour = 0;
            var minute = 0;
            var second = 0;
        }
        return new Date(y, m, d, hour, minute, second);
    }
);

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

(function ($) {
    /**
     * Динамическое создание меню для journal
     */
    function popupmenu(target, index, row) {
        var menu = $.data(target, 'journal').menu;
        menu.empty().
        menu('appendItem', {
            text: 'Создать',
            name: 'new',
            iconCls: 'icon-add'}).
        menu('appendItem', {
            text: 'Редактировать',
            name: 'edit',
            iconCls: 'icon-edit'
        }).
        menu('appendItem', {
            text: 'Удалить',
            name: 'remove',
            iconCls: 'icon-remove'}).
        menu('appendItem', {
            separator: true
        }).
        menu('appendItem', {
            text: 'Копировать',
            name: 'copy',
            iconCls: 'icon-copy'}).
        menu('appendItem', {
            text: 'Вставить',
            name: 'paste',
            iconCls: 'icon-paste'}).
        menu('appendItem', {
            text: 'Дублировать',
            name: 'remove',
            iconCls: 'icon-paste'}).
        menu('appendItem', {
            separator: true}).
        menu('appendItem', {
            text: 'Обновить',
            name: 'reload',
            iconCls: 'icon-reload'}).
        menu('appendItem', {
            text: 'Печать',
            name: 'print',
            iconCls: 'icon-print'}).
        menu('options').
            onClick = function (item) {
            $(target).journal(item.name)
        };
        return menu;
    }

    function showMenu(target, action) {
        // УСТАРЕВШАЯ
        // находим общий журнал документов
        var tab = $('.easydocui-journal');
        // выбираем соответствующую tab панель
        var selected = tab.tabs('getSelected');
        // узнаем его индекс  панели в таблице
        var tabIndex = tab.tabs('getTabIndex', selected);
        //alert(tabIndex);
        alert(selected.panel('options').idDoc);

        if (tabIndex) {
            // Действия в документе
            //var doc_id = '#document-item-table-' + $("<div/>",
            //    {"html": selected.panel('options').content}).find('#doc-id').html();

            alert(selected.panel('options').content);
            $(this).document(action);

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

    /**
     * Функция открытия документа из journal datagrid в новой tab вкладки для редактирования
     */
    function openDoc(target, params) {
        var doctabs = $(target);
        if (doctabs.tabs('exists', params.title)) {
            doctabs.tabs('select', params.title);
        } else {
            $.ajax({
                url: params.url,
                cache: true,
                success: function (html) {
                    //Найдем в полученом HTML id документа и добавим его в data-options к tabs
                    var idDoc = $("<div/>", {"html": html}).find('#doc-id').html();

                    doctabs.tabs('add', {
                        idDoc: idDoc,
                        title: params.title,
                        content: html,
                        closable: true
                    });
                    // Инициализируем все документы
                    $('.easydocui-document').document();
                    //var tabs = document.datagrid('options').idDoc;
                    //alert(idDoc);
                    //document.document();
                    //$(html).document();
                    // enableDoc('#document-item-table-' + '{{ consignment.id }}', '#item-table-popup-menu');
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
        if(row){
            //alert(row.toString());
            $.data(target, 'copiedDoc', row);
            //setCookie('copiedDoc', JSON.stringify(row));
        }
    }

    /**
     * Добавление документа, в journal datagrid из буфера cookie
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
            data: {'item':row},
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
        if (journal){
            var table = journal.find(options.table);
            if (!journal){
                $.error('jQuery.journal: Не могу обнаружить datagrid table');
                return false;
            }
        }else {
            $.error('jQuery.journal: Не могу обнаружить easydocui-journal');
            return false;
        }

        //alert(journal.html().toSource());
        var menu = $(table.datagrid('options').popupmenu);
        var toolbar = $(table.datagrid('options').toolbar);
        var dateFrom = toolbar.find('input.journal-datefrom');
        var dateTo = toolbar.find('input.journal-dateto');

        table.
        datagrid({
            clickToEdit: false,
            dblclickToEdit: true
        }).
        datagrid({
            onRowContextMenu: function (e, index, row) {
                e.preventDefault();
                // Включаем контекстное меню для редактирования таблицы документов
                popupmenu(target, index, row).menu('show', {
                    left: e.pageX,
                    top: e.pageY
                });
            }
        }).
        datagrid({
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
            return $.data(jq[0],'journal').table.datagrid('reload');
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

$(document).ready(function () {
    $(function () {
        $('.easydocui-journal').journal({
            type: 'consignment',
            name: 'Журнал накладных',
            table: '#journal-table'
        });

    });

    if (!navigator.cookieEnabled) {
        alert('Включите cookie для комфортной работы с этим сайтом');
    }
});
