/**
 * EasyDocUI for jQuery.EasyUI
 *
 * Copyright (c) 2016-2018 Seliverstov Dmitriy. All rights reserved.
 *
 * Licensed under the freeware license: http://www.-------.-----/--------
 * To use it on other terms please contact us: -----@-------.---
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
    $.fn.classes = function (callback) {
        var classes = [];
        $.each(this, function (i, v) {
            var splitClassName = v.className.split(/\s+/);
            for (var j = 0; j < splitClassName.length; j++) {
                var className = splitClassName[j];
                if (-1 === classes.indexOf(className)) {
                    classes.push(className);
                }
            }
        });
        if ('function' === typeof callback) {
            for (var i in classes) {
                callback(classes[i]);
            }
        }
        return classes;
    };
})(jQuery);



(function ($) {
    function init(target, options) {
        // Находим easyui tabs и вешаем на него плагин
        var easydocui = $(target);
        //alert(easydoc.hasClass('easyui-tabs'));
        if (!easydocui || !easydocui.hasClass('easyui-tabs')) {
            $.error('jQuery.easydoc: Не могу обнаружить easyui-tabs или easydoc');
            return this;
        }
        // Инициализируем Tabs
        easydocui.tabs({
            onLoad: function (panel) {
                // Первая вкладка всегда journal с индексом 0
                var indexTab = panel.panel('options').index;
                var tab = easydocui.tabs('getTab', indexTab);
                //alert(tab.find('div').classes().toSource());
                if (indexTab === 0) {
                    tab.addClass('easydoc-journal');
                    tab.journal(options);
                } else if (indexTab > 0) {
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
        //var journal = easydoc.tabs('getTab',0);
        //alert(journal.classes().toSource());
        return {
            options: options,
            easydocui: easydocui,
            journal: easydocui.tabs('getTab', 0)
        };
    }

    $.fn.easydocui = function (options, params) {
        if (typeof options === 'string') {
            //alert(params.toSource());
            alert(options.toSource());
            var result = $.fn.easydocui.methods[options];
            if (result) {
                return result(this, params);
            } else {
                $.error('Метод с именем ' + options + ' не существует для jQuery.easydocui');
                return this;
            }
        }
        options = options || {};
        //alert($(this).html().toSource());
        return this.each(function () {
            // Делаем инициализацию
            var state = $.data(this, 'easydocui');
            if (state) {
                $.extend(state.options, options);
            } else {
                var r = init(this, options);
                $.data(this, 'easydocui', {
                    //options: $.extend({}, $.fn.journal.defaults, parseOptions(this), options),
                    options: $.extend({}, $.fn.document.defaults, options),
                    easydocui: r.easydocui,
                    journal: r.journal
                });
                $(this).removeAttr('disabled');
            }
            //setDisabled(this, state.options.disabled);
            //Активация кнопок
            //bindEvents(this);
            //validate(this);
        });
    };

    $.fn.easydocui.methods = {
        options: function (jq) {
            return $.data(jq[0], 'easydocui').options;
        },
        tabs: function (jq) {
            return $.data(jq[0], 'easydocui').tabs;
        },
        journal: function (jq) {
            return $.data(jq[0], 'easydocui').journal;
        },
        close: function (jq, params) {
            return jq.each(function () {
                // Пока не работает
                close(this);
            });
        },
        add: function (jq, params) {
            return jq.each(function () {
                addTab(this, params);
            })
        }
    };

    $.fn.easydocui.defaults = {};
})(jQuery);
