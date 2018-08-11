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
        let menu = $.data(target, 'journal').menu;
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
        }).menu('options').onClick = function (action) {
            $(target).journal(action.name)
        };
        return menu;
    }

    /**
     * Активация компонента journal плагина EasyDoc на вкладке easyui-tabs
     */
    function init(target, options) {
        let journal = $(target);
        let table = journal.find('.easyui-datagrid');

        if (journal) {
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
        let menu = $(table.datagrid('options').popupmenu);
        if (menu.length !== 1) {
            $.error('jQuery.easydoc.journal: didn\'t find or multiple menu elements');
            return false;
        }
        // Находим в "data-options" плагина datagrid элемент toolbar
        let toolbar = $(table.datagrid('options').toolbar);
        if (toolbar.length !== 1) {
            $.error('jQuery.easydoc.journal: didn\'t find or multiple  toolbar elements');
            return false;
        }
        // Находим по тегам элементы дат начала и конца периода в journal
        let dateFrom = toolbar.find('input.journal-datefrom');
        if (dateFrom.length !== 1) {
            $.error('jQuery.easydoc.journal: didn\'t find or multiple  dateFrom elements');
            return false;
        }
        let dateTo = toolbar.find('input.journal-dateto');
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
     * Редактирование документа, выделенного в journal datagrid
     */
    function editDoc(container) {
        // Извлекаем jQ объект таблицы
        let journal = $.data(container, 'journal');
        let easydoc = $(journal.easydoc);
        let row = journal.table.datagrid('getSelected');
        if (row) {
            letadd_params = {
                title: row.name,
                // url: opts.url + row.id + opts.edit_url,
                idDoc: row.id
            };
            easydoc.easydoc('edit', $.extend($.fn.journal.defaults.open_params, add_params));
        } else {
            $.error('easyDoc.journal.editDoc: row\'s choice error')
        }
        // Открываем
        return this;
    }

    /**
     * Создание нового документа, в journal datagrid
     */
    function newDoc(container) {
        // Извлекаем jQ объект таблицы
        let journal = $.data(container, 'journal');
        let easydoc = $(journal.easydoc);
        //letopts = journal.options;
        easydoc.easydoc('new');
        return this;
    }



    /**
     * Привязка событий
     */
    function bindEvents(target) {
        //letoptions = $.data(target, 'journal').options;
        // Извлекаем jQ объект тулбара
        let toolbar = $.data(target, 'journal').toolbar;
        $(document).unbind('.journal');
        toolbar.unbind('.journal');

        // Кнопка "Создать"
        let buttonCreate = $('#easydoc-createdoc');

        buttonCreate.bind('click.journal', function (e) {
                $(target).journal('new');
            }
        );

        // Кнопка "Редактировать"
        let buttonEdit = $('#easydoc-editdoc');
        buttonEdit.bind('click.journal', function (e) {
                $(target).journal('edit');
            }
        );

        // Кнопка "Удалить"
        let buttonRemove = $('#easydoc-removedoc');
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
            let result = $.fn.journal.methods[options](this, params);
            if (result) {
                //alert(result.toSource());
                return result;
            } else {
                $.error('jQuery.easydoc.journal: The method with name:' + options + ' does not exist');
                return this;
            }
        }

        options = options || {};
        //alert($(this).html().toSource());
        return this.each(function () {
            // Делаем инициализацию
            let state = $.data(this, 'journal');
            if (state) {
                $.extend(state.options, options);
            } else {
                let r = init(this, options);
                //alert(r.toSource());
                $.data(this, 'journal', {
                    options: $.extend({}, $.fn.journal.defaults, options),
                    easydoc: options.easydoc,
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
        easydoc: function (jq) {
            return $.data(jq[0], 'journal').easydoc;
        },
        destroy: function (jq) {
            return jq.each(function () {
                // Пока не работает
                destroy(this);
            });
        },
        new: function (jq) {
            return jq.each(function () {
                newDoc(this);
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
        journal: '#journal-table',
        journal_title: 'Documents\'s journal',
        selector: '.easydoc-journal',

        timedelta: 90,     // период журнала в днях
        dateto: null,
        datefrom: null,

        open_params: {action: 'new'}

    };

})(jQuery);





