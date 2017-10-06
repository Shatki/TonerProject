(function ($) {
    // Расширение редакторов
    $.extend($.fn.datagrid.defaults.editors, {
        itemcombotreegrid: {
            init: function (container, options) {
                var input = container;
                input.combotreegrid(options);
                //$('#dlg-consignment').dialog('open');
                //$('product-tg-consignment').datagrid('reload');
                return input
            },
            destroy: function (target) {
                //$('#dlg-consignment').dialog('close');
                $(target).combotreegrid('destroy');
            },
            getValue: function (target) {
                //alert($(target).combotreegrid('getValue').toSource());
                //var g = $(target).combotreegrid('grid');	// get treegrid object
                //var value = g.treegrid('getSelected');
                //if (value){return value.name;}
                return $(target).combotreegrid('getValue');
            },
            setValue: function (target, value) {
                $(target).combotreegrid('setValue', value);
            },
            resize: function (target, width) {
                $(target).combotreegrid('resize', width);
            }
        }
    });

    // Предотвращение выбора категории в combotreegrid
    $.fn.combotreegrid.defaults.onBeforeSelect = function (row) {
        // Запрет выбора таких ID
        if (row.id.substring(0, 3) == 'DIR') {
            return false;
        } //else {
          //alert(row.toSource());
        //}
    };

})(jQuery);
