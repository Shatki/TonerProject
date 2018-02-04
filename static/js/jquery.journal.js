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
            + ' ' +formatNumber(h)+':'+formatNumber(M)+':'+formatNumber(s);
    },
    $.fn.datetimebox.defaults.parser = function (s) {
        if ($.trim(s) == '') {
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
    function popupmenu(menuid, index, row) {
        var menu = $(menuid).empty();
        menu.
        menu('appendItem', {
            text: 'Создать',
            name: 'new',
            iconCls: 'icon-add'}).
        menu('appendItem', {
            text: 'Редактировать',
            name: 'edit',
            iconCls: 'icon-edit'}).
        menu('appendItem', {
            text: 'Удалить',
            name: 'remove',
            iconCls: 'icon-remove'}).
        menu('appendItem', {
                separator: true}).
        menu('appendItem', {
            text: 'Копировать',
            name: 'copy',
            iconCls: 'icon-copy'}).
        menu('appendItem', {
            text: 'Вставить',
            name: 'edit',
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
            iconCls: 'icon-print'
        }).
        menu('options').onClick = function (item) {
            $(this).journal(item.name)};
        return menu;
    }

    function activate(table) {


    }

    var methods = {
        init: function (options) {
            // Создаем настройки из дефолтных
            // актуальные настройки, будут индивидуальными при каждом запуске
            options = options || {};
            var opts = $.extend({}, $.fn.journal.defaults, options);

            return this.each(function() {
                //var data = journal.data('journal');
                var journal = $(this);
                var state = journal.data('journal');
                if (state) {
                    return this;
                } else {
                    var menuid = journal.datagrid('options').popupmenu;
                    var toolbar = $(journal.datagrid('options').toolbar);
                    var dateFrom = toolbar.find('input.journal-datefrom');
                    var dateTo = toolbar.find('input.journal-dateto');

                    var buttonAdd = toolbar.find('a.easydocui-adddoc');
                    var buttonEdit = toolbar.find('a.easydocui-editdoc');
                    var buttonRemove = toolbar.find('a.easydocui-removedoc');

                    buttonAdd.on( "click", $.proxy(methods.new.bind(this)));
                    buttonEdit.on( "click", $.proxy(methods.edit.bind(this)));
                    buttonRemove.on( "click", $.proxy(methods.remove.bind(this)));


                    journal.
                    datagrid({
                        clickToEdit: false,
                        dblclickToEdit: true
                    }).
                    datagrid({
                        onRowContextMenu: function (e, index, row) {
                            e.preventDefault();
                            // Включаем контекстное меню для редактирования таблицы документов
                            popupmenu(menuid, index, row).menu('show', {
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
                    // Устанавливаем флаг проинициализированности
                    $(this).data('journal', this);
                }
            });
        },
        destroy: function () {
            return $(this).each(function () {
                $(window).unbind('.journal');
            })
        },
        add: function (params) {
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
            return this;
        },
        new: function () {
            var table = $(this);
            //alert($(".journal-tabs").html().toSource());
            //var row = table.datagrid('getSelected');
            //alert(row);
            var date = table.datebox.defaults.formatter(new Date());
            methods.add({
                title: 'Новая накладная от ' + date,
                url: '/document/consignment/new/'
            });
            return this
        },
        edit: function () {
            var journal = $(this);
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
        },
        remove: function () {
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
        },
        copy: function () {
            var doc = this;
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
        },
        rename: function () {
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
        },
        reload: function () {
            //tab
            return this;
        },
        popupmenu: function (action) {
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
        },
        print: function () {
            //
            alert('Печать из журнала');
            return this;
        }
    };
    $.fn.journal = function (method) {
        if (methods[method]) {
            // если запрашиваемый метод существует, мы его вызываем
            // все параметры, кроме имени метода прийдут в метод
            // this так же перекочует в метод
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            // если первым параметром идет объект, либо совсем пусто
            // выполняем метод init
            return methods.init.apply(this, arguments);
        } else {
            // если ничего не получилось
            $.error('Метод с именем ' + method + ' не существует для jQuery.journal');
        }
    };
    $.fn.journal.defaults = {
        selector: '.easydocui-journal',
        url: '/document/'
    }
})(jQuery);

$(document).ready(function () {
    $(function () {
        $('table.easydocui-journal').journal();

    });

    if (!navigator.cookieEnabled) {
        alert('Включите cookie для комфортной работы с этим сайтом');
    }
});