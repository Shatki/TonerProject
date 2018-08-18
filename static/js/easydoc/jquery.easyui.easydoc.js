/**
 * easyDoc for jQuery.EasyUI
 *
 * Copyright (c) 2016-2018 Seliverstov Dmitriy. All rights reserved.
 *
 * Licensed under the freeware license: http://www.-------.-----/--------
 * To use it on other terms please contact us: -----@-------.---
 *
 */

// Делаем замыкание
(function ($) {
    /**
     * Функция создает на нулевой вкладке журнал
     * @param      easydoc  (object)    Объект jQuery.easydoc для инициализации плагина jQuery.easyui.easydoc.journal
     * @param      options  (object)    Объект с настройками плагина
     * @return              (object)    Инициализированный объект jQuery.easyui.journal
     */
    function journalCreate(easydoc, options) {
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
                    tab.journal({easydoc: easydoc});
                } else if (indexTab > 0) {
                    // Тут документ
                    tab.addClass('easydoc-document');
                    alert(tab.classes().toSource());
                    tab.document(options);
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
        //let journal = easydoc.tabs('getTab',0);
        //  Вернем журнал
        return easydoc.tabs('getTab', 0);
    }

    /**
     * Функция инициализатор плагина easyDoc
     * @param      target   (object)    Объект DOM класса easyui-tabs  для активации на нем плагина easyDoc
     * @param      options  (object)    Объект с настройками плагина
     * @return              (object)    Объект содержащий {настройки, ициализированные jQuery.easydoc, jQuery.journal}
     */
    function init(target, options) {
        /*  Функция инициализации плагина EasyDoc
            @param      target  (jQuery) целевой элемент DOM
            @param      options (object) параметры настройки плагина
            @return             (object) содержит options, easydoc, journal
            */

        // Если options === undefined, сделаем ее просто пустой
        options = options || {};
        // Получаем target для поиска элемента на который вешаем плагин
        let container = $(target);
        // Полученый target должен быть класса easyui-tabs
        if (!container || !container.hasClass('easyui-tabs')) {
            $.error('jQuery.easydoc: can\'t find easyui-tabs or easydoc');
            return this;
        }
        return {
            options: options,
            easydoc: container.easydoc,
            journal: journalCreate(container, options)
        };
    }

    /**
     * Функция открытия документа из journal datagrid или создание нового документа
     * в новой tab вкладки для редактирования
     * @param      target   (string)
     * @param      params   (object)    Объект с настройками для открытия документа
     * @return              (object)
     */
    function documentOpen(target, params) {
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
                    //Найдем в полученом HTML id документа и добавим его в data-options к tabs
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

    /** Функция "точка" вызова плагина easyDoc
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
                let result = init(this, options);
                // Сохраним созданный объект с элементами easydoc и journal
                // с нашими настройками для данного контекста в data
                $.data(this, 'easydoc', {
                    // Сохраним jQuery объект нашего элемента DOM
                    easydoc: result.easydoc,
                    // Берем для easyDoc настройки по-умолчанию и дополняем их полученными
                    options: $.extend({}, $.fn.easydoc.defaults, options),
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
        close: function (jq, params) {
            return jq.each(function () {
                documentClose(this, params);
            });
        },
        edit: function (jq, params) {
            return jq.each(function () {
                documentOpen(this, params);
            })
        },
        new: function (jq, params) {
            return jq.each(function () {
                documentOpen(this, params);
            })
        }

    };

    $.fn.easydoc.defaults = {
        option: null,                       // Url параметр запроса {json, ...}
        common: `all`,
        edit: `edit/`,
        new: ``,
        target: `new`,

        getTitle: function (params) {
            params = params || {};
            // Если не пришла дата, то возьмем ее из delaults
            // params.date = $.fn.datebox.defaults.formatter(new Date());
            // Если не пришли параметры, то создадим новый документ
            return `Новая ${params.document_type_name} от ${params.document_date ? params.document_date : this.document_date }`;
        },

        getUrl: function (params) {
            return `/document/${params.document_type}/${params.target ? params.target : this.target}/${params.index > 0 ? this.edit : ``}`;
        }

    };
})(jQuery);

