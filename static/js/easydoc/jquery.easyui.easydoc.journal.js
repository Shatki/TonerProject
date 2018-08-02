/**
 * easyDoc for jQuery.EasyUI
 *
 * Copyright (c) 2016-2018 Seliverstov Dmitriy. All rights reserved.
 *
 * Licensed under the freeware license: http://www.-------.-----/--------
 * To use it on other terms please contact us: -----@-------.---
 *
 *      journal for easyDoc
 */

// Делаем замыкание
(function ($) {
    /**
     * Компонент journal из плагина EasyDoc
     * @param      target (jQuery) целевой элемент DOM
     * @param      options (object) параметры настройки плагина
     * @return             (object) содержит options, journal, table, toolbar, menu
     */

    /**
     * Динамическое создание меню для journal
     */
    function popupmenu(target, index, row) {
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
     * Активация компонента journal плагина EasyDoc на вкладке easyui-tabs
     */
    function init(target, options) {
        var journal = $(target);
        if (journal) {
            var table = journal.find('.easyui-datagrid');
            if (!table) {
                $.error('jQuery.easydoc.journal: can\'t find datagrid table');
                return false;
            } else {
                table.addClass('easydoc-journal-table')
            }
        } else {
            $.error('jQuery.easydoc.journal: can\'t find easydoc-journal');
            return false;
        }

        // Инициализацию функциональных элементов оформления придется описать каждый отдельно
        // Находим в "data-options" плагина datagrid элемент меню
        var menu = $(table.datagrid('options').popupmenu);
        if (menu.length !== 1) {
            $.error('jQuery.easydoc.journal: didn\'t find or multiple menu elements');
            return false;
        }
        // Находим в "data-options" плагина datagrid элемент toolbar
        var toolbar = $(table.datagrid('options').toolbar);
        if (toolbar.length !== 1) {
            $.error('jQuery.easydoc.journal: didn\'t find or multiple  toolbar elements');
            return false;
        }
        // Находим по тегам элементы дат начала и конца периода в journal
        var dateFrom = toolbar.find('input.journal-datefrom');
        if (dateFrom.length !== 1) {
            $.error('jQuery.easydoc.journal: didn\'t find or multiple  dateFrom elements');
            return false;
        }
        var dateTo = toolbar.find('input.journal-dateto');
        if (dateTo.length !== 1) {
            $.error('jQuery.easydoc.journal: didn\'t find or multiple dateTo elements');
            return false;
        }

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
        // Активный диапазон дат
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
     * Создание или редактирование документа, выделенного в journal datagrid
     */
    function openDoc(container, params) {
        // Извлекаем jQ объект таблицы
        var journal = $.data(container, 'journal');
        var opts = journal.options;
        var easydoc = opts.easydoc;

        var row = journal.table.datagrid('getSelected');
        if (row) {
            var add_params = {
                title: row.name,
                // url: opts.url + row.id + opts.edit_url,
                idDoc: row.id
            }
        }
        // Открываем
        easydoc('add', $.extend($.fn.journal.defaults.open_params, add_params));
        return this;


    }

    /**
     * Привязка событий
     */
    function bindEvents(target) {
        //var options = $.data(target, 'journal').options;
        // Извлекаем jQ объект тулбара
        var toolbar = $.data(target, 'journal').toolbar;
        $(document).unbind('.journal');
        toolbar.unbind('.journal');

        // Кнопка "Создать"
        var buttonCreate = $('#easydoc-createdoc');

        buttonCreate.bind('click.journal', function (e) {
                $(target).journal('new');
            }
        );

        // Кнопка "Редактировать"
        var buttonEdit = $('#easydoc-editdoc');
        buttonEdit.bind('click.journal', function (e) {
                $(target).journal('edit');
            }
        );

        // Кнопка "Удалить"
        var buttonRemove = $('#easydoc-removedoc');
        buttonRemove.bind('click.journal', function (e) {
                $(target).journal('remove');
            }
        );

    }

    $.fn.journal = function (options, params) {
        /**
         * Функция "точка" вызова компонента journal плагина EasyDoc
         * @param      options (string, необязательный) имя вызываемого метода
         * @param      params (object) параметры настройки плагина
         * @return     this (object) объект экземпляра для поддержки цепочки вызовов
         */
        if (typeof options === 'string') {
            var result = $.fn.journal.methods[options](this, params);
            if (result) {
                alert(result.toSource());
                return result(this, params);
            } else {
                $.error('The method with name:' + options + ' does not exist in jQuery.easydoc.journal');
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
                    options: $.extend($.fn.journal.defaults, options),
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

        ///// ???????
        add: function (jq, params) {
            return jq.each(function () {
                openDoc(this, params);
            })
        },
        new: function (jq) {
            return jq.each(function () {
                var date = $.fn.datebox.defaults.formatter(new Date());
                openDoc(this, {
                    action: 'new',
                    title: $.fn.journal.defaults.title_new + date
                });
            })
        },
        edit: function (jq) {
            return jq.each(function () {
                openDoc(this);
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
        test: 'journal-defaults',
        selector: '.easydoc-journal',
        journal: '#journal-table',
        title_new: 'Новая накладная от ',

        timedelta: 90,     // период журнала в днях
        dateto: null,
        datefrom: null,
        title: 'Documents\'s journal',
        open_params: {action: 'new'}

    };

})(jQuery);





