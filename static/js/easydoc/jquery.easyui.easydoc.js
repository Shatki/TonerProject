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
     * Функция создает на нулевой вкладке журнал,
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
     * Функция инициализатор плагина easyDoc,
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
     */
    function documentOpen(target, params) {
        alert(target.options.toSource());

        let easydoc = $.data(target, 'easydoc').easydoc;
        let options = $.data(target, 'easydoc').options;



        //let date = $.fn.datebox.defaults.formatter(new Date());

        // Получим название вкладки документа согласно полученым параметрам
        let title = options.getTitle(params);
        alert(params.title);

        // Получим url запроса документа согласно полученым параметрам
        let url = easydoc.options.getUrl(params);

        alert(url);

        // Переработать для открытия через easyDoc
        if (easydoc.tabs('exists', params.title)) {
            // Если такой документ открыт, то переключимся на нее
            easydoc.tabs('select', params.title);
        } else {
            alert(params.url);
            $.ajax({
                url: params.url,
                cache: true,
                success: function (html) {
                    //Найдем в полученом HTML id документа и добавим его в data-options к tabs
                    let idDoc = +($("<div/>", {"html": html}).find('#doc-id').html());
                    if (idDoc >= 0) {
                        easydoc.tabs('add', {
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
        return this;
    }

    function documentClose(container, param) {

    }

    $.fn.easydoc = function (options, params) {
        /*  Функция "точка" вызова плагина easyDoc
            @param      options (string, необязательный) имя вызываемого метода
            @param      params (object) параметры настройки плагина
            @return     this (object) объект экземпляра для поддержки цепочки вызовов
            */
        // Если пришло имя функции то string
        if (typeof options === 'string') {
            return $.fn.easydoc.methods[options](this, params);
        }
        // Пришел объект с данными

        options = options || {};
        // Отобразим this для отладки

        return this.each(function () {
            // Ищем в data уже существующий компонент
            let state = $.data(this, 'easydoc');
            if (state) {
                // Если уже создан, расширим опции
                $.extend(state.options, options);
            } else {
                // Инициализируем объект с требуемыми опциями
                let result = init(this, options);
                // Получим созданный объект с элементами easydoc и journal
                // с нашими настройками и сохраним их в data
                $.data(this, 'easydoc', {
                    // Сохраним jQuery объект нашего элемента DOM
                    easydoc: result.easydoc,
                    // Берем для EasyDoc настройки по-умолчанию и дополняем их полученными
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
        tabs: function (jq) {
            return $.data(jq[0], 'easydoc').tabs;
        },

        close: function (jq, params) {
            return jq.each(function () {
                documentClose(this, params);
            });
        },

        new: function (jq, params) {
            return jq.each(function () {
                documentOpen(this, params);
            })
        }

    };
    $.fn.easydoc.defaults = {
        document_type: `consignment`,               // Потом поменять на 'all'
        document_type_name: `накладная`,
        document_date: `31/10/1985`,

        option: null,                       // Url параметр запроса {json, ...}

        common_url: `/all/`,
        edit_url: `/edit/`,
        new_url: `/new/`,

        getTitle: function (params) {
            params = params || {};
            // Если не пришла дата, то возьмем ее из delaults
            // params.date = $.fn.datebox.defaults.formatter(new Date());
            // Если не пришли параметры, то создадим новый документ
            return `Новая ${params.document_type} от ${params.document_date ? params.document_date : this.document_date }`;
        },

        getUrl: function (params) {
            return `/document/${params.document_type}/${params.target}/${params.option}`;
        }

    };
})(jQuery);

