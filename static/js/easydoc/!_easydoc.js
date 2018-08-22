/**
 * pop up menu плагина EasyDoc
 * @param      target   (object DOM)
 * @param      index    (number)
 * @param      row      (number)
 * @return              (object) Объект меню
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
        $(target).easydoc(action.name)
    };
    return menu;
}

/**
 * Активация компонента journal плагина easyDoc на вкладке easyui-tabs
 * @param      target   (object DOM) целевой элемент DOM
 * @param      tab      (object) настройки для активации компонента
 * @return              (object) содержит options, journal, table, toolbar, menu
 */
function createJournal(target, tab) {
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
}

/**
 * Редактирование документа, выделенного в journal datagrid
 * @param      target   (object DOM) элемент DOM
 */
function editDoc(target) {
    // Из data получаем объект данных привязанных journal
    let journal = $.data(target, 'journal');
    // Создаем jQuery объект
    let $this = journal.easydoc;

    let row = journal.table.datagrid('getSelected');
    if (row) {
        // Открываем
        $this.easydoc('edit', {
            document_type: journal.options.document_type,
            document_type_name: row.name,
            document_date: $.fn.datebox.defaults.formatter(new Date()),
            target: row.id,
            idDoc: row.id,
            index: row.id
            //target:
        });
    } else {
        $.error('easyDoc.journal.editDoc: row\'s choice error')
    }
}

/**
 * Создание нового документа, в journal datagrid
 * @param      target   (object DOM) элемент DOM, datagrid журнала
 */
function newDoc(target) {
    // target - datagrid у журнала
    // Извлекаем jQ объект таблицы
    let journal = $.data(target, 'journal');
    let $this = journal.easydoc;
    //alert(journal.document_type_name.toSource());
    $this.easydoc('new', {
        document_type: journal.options.document_type,
        document_type_name: journal.options.document_type_name,
        document_date: $.fn.datebox.defaults.formatter(new Date()),
        index: 0
        //target:
    });
}

/**
 * Функция открывает или создает документ на новой вкладке
 * @param      easydoc  (object DOM)    Объект jQuery.easydoc
 * @param      options  (object)    Объект с настройками плагина
 * @return              (object)    Инициализированный объект jQuery.easyui.document
 */
function documentOpen(easydoc, options) {
}

/**
 * Функция инициализатор плагина easyDoc
 * @param      target   (object DOM)    Объект DOM класса easyui-tabs  для активации на нем плагина easyDoc
 * @param      options  (object)    Объект с настройками плагина
 * @return              (object)    Объект содержащий {настройки, ициализированные jQuery.easydoc, jQuery.journal}
 */
function init(target, options) {
    // Если options === undefined, сделаем ее просто пустой
    options = options || {};
    // Обернем DOM объект в jQuery функционал
    let easydoc = $(target);
    // Полученый target должен быть класса easyui-tabs
    if (!easydoc || !easydoc.hasClass('easyui-tabs')) {
        $.error('jQuery.easydoc: can\'t find easyui-tabs or easydoc');
        return this;
    }

    alert(options.toSource());
    // Инициализируем Tabs
    easydoc.tabs({
        onLoad: function (panel) {
            // Первая вкладка всегда journal с индексом 0
            let indexTab = panel.panel('options').index;
            let tab = easydoc.tabs('getTab', indexTab);
            //alert(tab.find('div').classes().toSource());
            if (indexTab === 0) {
                // Тут журнал
                tab.addClass('easydoc-journal');
                // Инициализация журнала
                easydoc.easydoc('addTab', {
                    type: 'journal',
                    tab: tab
                });
            } else if (indexTab > 0) {
                // Тут документ
                tab.addClass('easydoc-document');
                alert(tab.classes().toSource());
                easydoc.easydoc('addTab', {
                    type: 'document',
                    tab: tab
                });
            } else {
                $.error('jQuery.easydoc: index of tab error');
            }
        }
    }).tabs('add', {
        //Принудительно делаем индекс журнала 0
        index: 0,
        href: options.url,
        method: 'POST',
        title: options.title,
        closable: false,
        selected: true
    });
    // let journal = easydoc.tabs('getTab',0);
    // Вернем журнал

    return {
        options: options,
        easydoc: easydoc,
        journal: easydoc.tabs('getTab', 0)
    };
}

/**
 * Функция открытия документа из journal datagrid или создание нового документа
 * в новой tab вкладки для редактирования
 * @param      target   (string)
 * @param      params   (object)    Объект с настройками для открытия документа
 * @return              (object)
 */
function open(target, params) {
    //alert(target.options.toSource());
    let easydoc = $.data(target, 'easydoc');
    //let options = easydoc.options;
    let $this = $(target);

    // Получим название вкладки документа согласно полученым параметрам
    let title = easydoc.options.getTitle(params);
    alert(title);

    // Получим url запроса документа согласно полученым параметрам
    let url = easydoc.options.getUrl(params);

    // Переработать для открытия через easyDoc
    if ($this.tabs('exists', title)) {
        // Если такой документ открыт, то переключимся на нее
        $this.tabs('select', title);
    } else {
        $.ajax({
            url: url,
            method: 'POST',
            cache: true,
            success: function (html) {
                // Найдем в полученом HTML id документа и добавим его в data-options к tabs
                let idDoc = +($("<div/>", {"html": html}).find('#doc-id').html());
                if (idDoc >= 0) {
                    $this.tabs('add', {
                        //index: idDoc,
                        idDoc: idDoc,
                        title: title,
                        content: html,
                        closable: true,
                        selected: true
                    });
                }
            }
        });
    }
    return $this;
}


function documentClose(container, param) {
}

/**
 * Функция "точка" вызова плагина easyDoc
 * @param      options  (string, необязательный) имя вызываемого метода
 * @param      params   (object) параметры настройки плагина
 * @return     this     (object) объект экземпляра для поддержки цепочки вызовов
 * */
$.fn.easydoc = function (options, params) {
    // Если пришло имя функции то string
    if (typeof options === 'string') {
        // Передаем в метод контекст и настройки
        return $.fn.easydoc.methods[options](this, params);
    }

    // Пришел объект с данными
    options = options || {};
    // Для поддержания цепочки вызовов вернем для каждого контекста результат индивидуально
    return this.each(function () {
        // Ищем в data уже существующий компонент
        let state = $.data(this, 'easydoc');
        if (state) {
            // Если уже создан, расширим опции
            $.extend(state.options, options);
        } else {
            // Инициализируем объект с требуемыми опциями
            // Возвращается объект с options/easydoc/journal
            let result = init(this, $.extend({}, $.fn.easydoc.defaults, options));
            // Сохраним созданный объект с элементами easydoc и journal
            // с нашими настройками для данного контекста в data
            $.data(this, 'easydoc', {
                // Сохраним jQuery объект нашего элемента DOM
                easydoc: result.easydoc,
                // Берем для easyDoc настройки по-умолчанию и дополняем их полученными
                options: result.options,
                // При инициализации создается и журнал, сохраним его jQuery объект
                journal: result.journal
            });
            $(this).removeAttr('disabled');
        }
        /*  Тут алгоритм активации функций EasyDoc */
        //setDisabled(this, state.options.disabled);
        //Активация кнопок
        //bindEvents(this);
        //validate(this);
    });
};

$.fn.easydoc.methods = {
    options: function (jq) {
        return $.data(jq[0], 'easydoc').options;
    },
    easydoc: function (jq) {
        return $.data(jq[0], 'easydoc').easydoc;
    },
    journal: function (jq) {
        return $.data(jq[0], 'easydoc').journal;
    },
    addTab: function (jq, params) {
        return jq.each(function () {
            if (params.type === 'journal') {
                createJournal(this, params.tab);
            }
            if (params.type === 'document') {
                documentOpen(this, params.tab);
            }
        });
    },
    close: function (jq, params) {
        return jq.each(function () {
            documentClose(this, params);
        });
    },
    edit: function (jq, params) {
        return jq.each(function () {
            open(this, params);
        })
    },
    new: function (jq, params) {
        return jq.each(function () {
            open(this, params);
        })
    }

};

$.fn.easydoc.defaults = {
    option: null,                       // Url параметр запроса {json, ...}
    common: `all`,
    edit: `edit/`,
    new: ``,
    target: `new`,

    document_type: `consignment`,               // Потом поменять на 'all'
    document_type_name: `накладная`,            // Потом 'все'
    document_date: `31/10/1985`,


    journal: '#journal-table',
    journal_title: 'Documents\'s journal',
    //title:         `Журнал документов`,
    selector: '.easydoc-journal',

    timedelta: 90,     // период журнала в днях
    dateto: null,
    datefrom: null,

    getTitle: function (params) {
        params = params || {};
        // Если не пришла дата, то возьмем ее из defaults
        // params.date = $.fn.datebox.defaults.formatter(new Date());
        // Если не пришли параметры, то создадим новый документ
        return params.index ?
            params.document_type_name :
            `Новая ${params.document_type_name} от ${params.document_date ? params.document_date : this.document_date }`;
    },

    getUrl: function (params) {
        // Доделать!!!
        let type = params.document_type;
        let target = params.target ? params.target : this.target;   // all or number
        let option = params.index > 0 ? this.edit : this.option;             // json or null
        return `/document/${type}/${target}/${option}`;
    }

};