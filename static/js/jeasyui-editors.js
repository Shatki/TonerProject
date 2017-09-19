(function ($) {
    $.extend($.fn.datagrid.defaults.editors, {
        product: {
            init: function (container, options) {
                var input = container;
                input.textbox(options);
                //$('#dd').dialog({
                //    title: 'My Dialog',
                //    width: 400,
                //    height: 200,
                //    closed: false,
                //    cache: false,
                //    href: '\\',
                //    modal: true
                //});

                $('#dlg-consignment').dialog('open');
                $('product-tg-consignment').datagrid('reload');
                return input
            },
            destroy: function (target) {
                $('#dlg-consignment').dialog('close');
                $(target).textbox('destroy');
            },
            getValue: function (target) {
                //var g = $(target).combotreegrid('grid');	// get treegrid object
                //var value = g.treegrid('getSelected');
                //if (value){return value.name;}
                return $(target).textbox('getValue');
            },
            setValue: function (target, value) {
                $(target).textbox('setValue', value);
            },
            resize: function (target, width) {
                $(target).textbox('resize', width);
            }
        },

        calcnumberbox: {
            init: function (container, options) {
                var input = $('<input type="text" class="datagrid-editable-input">').appendTo(container);
                input.numberbox(options);
                return input;
            },
            destroy: function (target) {
                // Убирает бокс редактирования

                //var dg = $(target);
                //var cell = dg.datagrid('cell');  // current cell
                //var row = dg.datagrid('getRows')[cell.index];  // current row
                //alert('des');
                //var cell = dg.datagrid('cell');
                //var row = dg.datagrid('getRows')[cell.index];
                //alert($(target).datagrid('getRows')[5]);
                $(target).numberbox('destroy');
            },
            getValue: function (target) {
                //alert('get');
                return $(target).numberbox('getValue');
            },
            setValue: function (target, value) {
                //alert('set');
                $(target).numberbox('setValue', value);
            },
            resize: function (target, width) {
                $(target).numberbox('resize', width);
            }
        }
    });
})(jQuery);
