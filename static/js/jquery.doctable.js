// В стадии разработки для созданияя плагина 'document'
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

$(document).ready(function () {
    if (!navigator.cookieEnabled) {
        alert('Включите cookie для комфортной работы с этим сайтом');
    }
});

(function ($) {
    var methods = {
        init: function (options) {
            //alert('enable');
            return this.each(function() {
                var table = $(this);
                var popupmenu = $(table.datagrid('options').popupmenu);
                var dateFrom = $(table.datagrid('options').toolbar).find('input.doctable-datefrom');
                var dateTo = $(table.datagrid('options').toolbar).find('input.doctable-dateto');
                var buttonAdd = $(table.datagrid('options').toolbar).find('a.doctable-newdoc');

                table.
                datagrid({
                    clickToEdit: false,
                    dblclickToEdit: true
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
    $.fn.doctable = function (method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Метод с именем ' + method + ' не существует для jQuery.doctable');
        }
    };
    $.fn.doctable.defaults = {
        selector: '.doctable',
        url: null
    }
})(jQuery);

$(document).ready(function () {
    $(function () {
        table=$('.doctable');
        table.doctable();
    });
});