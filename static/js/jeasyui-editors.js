(function ($) {
    var lastIndex;
    $('#tt').datagrid({
        onClickRow: function (rowIndex) {
            if (lastIndex != rowIndex) {
                $(this).datagrid('endEdit', lastIndex);
                $(this).datagrid('beginEdit', rowIndex);
            }
            lastIndex = rowIndex;
        },
        onBeginEdit: function (rowIndex) {
            var editors = $('#tt').datagrid('getEditors', rowIndex);
            var n1 = $(editors[0].target);
            var n2 = $(editors[1].target);
            var n3 = $(editors[2].target);
            n1.add(n2).numberbox({
                onChange: function () {
                    var cost = n1.numberbox('getValue') * n2.numberbox('getValue');
                    n3.numberbox('setValue', cost);
                }
            })
        }
    });

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
                $(target).numberbox('destroy');
            },
            getValue: function (target) {
                //alert('get');
                //var value = $(target).numberbox('getValue');


                //var table = $(target).parent('table');
                //var rows = table.datagrid('getRows');

                //alert(rows);

                //var v2 = n1.numberbox('getValue');
                //var cell = dg.datagrid('cell');  // current cell
                //var row = dg.datagrid('getRows')[cell.index];  // current row
                //alert(rows);
                //var cell = dg.datagrid('cell');
                //var row = dg.datagrid('getRows')[cell.index];
                //alert($(target).datagrid('getRows')[5]);
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
