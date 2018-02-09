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
        var menu = $(target).empty();
        menu.menu('appendItem', {
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
            name: 'edit',
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
            $(this).journal(item.name)
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
     * Функция создания и открытия документа из journal datagrid в новой tab вкладки для редактирования
     */
    function addDoc(target, params) {
        var doctabs = $('.journal-tabs');
        //alert(this.html().toSource());
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
        //alert(journal.toSource());
        //var journal = $(this).data('journal');
        //alert(journal.html().toSource());
        var row = journal.datagrid('getSelected');
        if (row) {
            methods.add({
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
        var table = $('.easydocui-journal');
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
        var doc = $(this);
        var rowIndex = doc.datagrid('cell').index;
        //var row = doc.datagrid('getRows')[rowIndex];
        alert(rowIndex);
        setCookie('bufferItem', rowIndex);
    }

    /**
     * Добавление документа, в journal datagrid из буфера cookie
     */
    function pasteDoc(target) {
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
        var tab = $(target);
        var journal = tab.find('table');

        alert(journal.html().toSource());
        var menuid = journal.datagrid('options').popupmenu;
        var toolbar = $(journal.datagrid('options').toolbar);
        var dateFrom = toolbar.find('input.journal-datefrom');
        var dateTo = toolbar.find('input.journal-dateto');

        var buttonAdd = toolbar.find('a.easydocui-adddoc');
        var buttonEdit = toolbar.find('a.easydocui-editdoc');
        var buttonRemove = toolbar.find('a.easydocui-removedoc');

        //buttonAdd.on( "click", $.proxy(methods.new.bind(this)));
        //buttonEdit.on( "click", $.proxy(methods.edit.bind(this)));
        //buttonRemove.on( "click", $.proxy(methods.remove.bind(this)));

        journal.datagrid({
            clickToEdit: false,
            dblclickToEdit: true
        }).datagrid({
            onRowContextMenu: function (e, index, row) {
                e.preventDefault();
                // Включаем контекстное меню для редактирования таблицы документов
                popupmenu(menuid, index, row).menu('show', {
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
                    journal.datagrid({
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
                    journal.datagrid({
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
            table: journal,
            tab: tab
        };
    }

    /**
     * Деакцивация плагина
     */
    function destroy(target) {
        var journal = $.data(target, 'journal').table;
        $(target).remove();
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
                var r = init(this);
                //alert(r.toSource());
                $.data(this, 'journal', {
                    //$.extend({}, $.fn.journal.defaults, options);
                    //options: $.extend({}, $.fn.journal.defaults, parseOptions(this), options),
                    table: r.table,
                    tab: r.tab
                });
                $(this).removeAttr('disabled');
            }
            //$('input.combo-text', state.combo).attr('readonly', !state.options.editable);
            //setDisabled(this, state.options.disabled);
            //setSize(this);
            //bindEvents(this);
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
        tab: function (jq) {
            return $.data(jq[0], 'journal').tab;
        },
        destroy: function (jq) {
            return jq.each(function () {
                // Пока не работает
                destroy(this);
            });
        },
        add: function (jq, params) {
            return jq.each(function () {
                addDoc(this, params);
            })
        },
        new: function (jq) {
            return jq.each(function () {
                var date = this.datebox.defaults.formatter(new Date());
                addDoc(this, {
                    title: 'Новая накладная от ' + date,
                    url: '/document/consignment/new/'
                });
            })
        },
        edit: function (jq) {
        },
        remove: function (jq) {
        },
        copy: function (jq) {
        },
        paste: function (jq) {
        },
        dublicate: function (jq) {

        },
        reload: function (jq) {
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
            name: 'Журнал накладных'
        });

    });

    if (!navigator.cookieEnabled) {
        alert('Включите cookie для комфортной работы с этим сайтом');
    }
});
