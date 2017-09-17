(function ($) {
    $.extend($.fn.datagrid.defaults, {
        clickToEdit: false,
        dblclickToEdit: true,
        navHandler: {
            '37': function (e) {
                var opts = $(this).datagrid('options');
                return navHandler.call(this, e, opts.isRtl ? 'right' : 'left');
            },
            '39': function (e) {
                var opts = $(this).datagrid('options');
                return navHandler.call(this, e, opts.isRtl ? 'left' : 'right');
            },
            '38': function (e) {
                return navHandler.call(this, e, 'up');
            },
            '40': function (e) {
                return navHandler.call(this, e, 'down');
            },
            '13': function (e) {
                return enterHandler.call(this, e);
            },
            '27': function (e) {
                return escHandler.call(this, e);
            },
            '8': function (e) {
                return clearHandler.call(this, e);
            },
            '46': function (e) {
                return clearHandler.call(this, e);
            },
            'keypress': function (e) {
                if (e.metaKey || e.ctrlKey) {
                    return;
                }
                var dg = $(this);
                var param = dg.datagrid('cell');	// current cell information
                if (!param) {
                    return;
                }
                var input = dg.datagrid('input', param);
                if (!input) {
                    var tmp = $('<span></span>');
                    tmp.html(String.fromCharCode(e.which));
                    var c = tmp.text();
                    tmp.remove();
                    if (c) {
                        dg.datagrid('editCell', {
                            index: param.index,
                            field: param.field,
                            value: c
                        });
                        return false;
                    }
                }
            }
        },
        onBeforeCellEdit: function (index, field) {
        },
        onCellEdit: function (index, field, value) {
            alert('Не работает!');
            var dg = $(this);
            //var cell = dg.datagrid('cell');  // current cell
            //var row = dg.datagrid('getRows')[cell.index];  // current row
            var input = dg.datagrid('input', {index: index, field: field}).bind('focusout', function (e) {
                // Добавка при отмене редактирования
                dg.datagrid('endEdit', index);
            });

            if (input) {
                if (value != undefined) {
                    input.val(value);
                }
            }
        },
        onSelectCell: function (index, field) {
        },
        onUnselectCell: function (index, field) {
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
                $('#tg').treegrid({
                    data: response
                }).treegrid('enableCellEditing').treegrid('gotoCell', {
                    index: 0,
                    field: 'id'
                });
                $('#dd').dialog('open');
                $('tg').treegrid('reload');
                return input
            },
            destroy: function (target) {
                $('#dd').dialog('close');
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
        }
    });
})(jQuery);

var data = {
    "total": 3, "rows": [
        {
            "productid": "PRT-15-031",
            "itemid": "EST-1",
            "productname": "Epson WorkForce 845",
            "quantity": 69,
            "price": 121.29,
            "measure": "pcs",
            "attr1": "retail"
        },
        {
            "productid": "PRT-DL-044",
            "itemid": "EST-10",
            "productname": "Canon PIXMA MG5320",
            "quantity": 12,
            "price": 110.50,
            "measure": "pcs",
            "attr1": "retail"
        },
        {
            "productid": "PRT-SN-201",
            "itemid": "EST-11",
            "productname": "HP Deskjet 1000 Printer",
            "quantity": 63,
            "price": 33.95,
            "measure": "pcs",
            "attr1": "retail"
        }
    ]
};

var measure = [
    {"id": 1, "name": "pcs"},
    {"id": 2, "name": "wth"},
    {"id": 3, "name": "vol"}
];

var response = [{
    'id': 'DIR-0',
    'name': "Parts",
    'iconCls': "icon-save",
    'children': [{
        "id": 'DIR-1',
        "name": "MotherBoards",
        "children": [{
            "id": 'DIR-1-1',
            "name": "Asus",
            "state": "closed",
            "children": [{
                "id": 'EST-1-1-1',
                'price': 56.3,
                'count': 3,
                "name": "M2N-E"
            }, {
                "id": 'EST-1-1-2',
                'price': 66.2,
                'count': 10,
                "name": "M5N-LE"
            }, {
                'id': 'EST-1-1-4',
                'iconCls': 'icon-print',
                'price': 49.7,
                'count': 13,
                'name': 'M5A78L-M LX3, SocketAM3+, mATX'
            }, {
                'id': 'EST-1-1-5',
                'iconCls': 'icon-print',
                'price': 53.1,
                'count': 11,
                'name': 'M5A97 LE R2.0, SocketAM3+, mATX'
            }]
        }, {
            "id": 'DIR-1-2',
            "name": "ASRock",
            "state": "closed",
            "children": [{
                'iconCls': 'icon-print',
                'id': 'EST-1-2-3',
                'price': 45.5,
                'count': 5,
                'name': 'ASRock N68-GS4 FX, SocketAM3+, mATX'
            }]
        }]
    }, {
        "id": 'DIR-2',
        "name": "CPU",
        "state": "closed",
        "children": [{
            "id": 'EST-2-1',
            "name": "i3",
            'price': 145.00,
            'count': 9
        }, {
            "id": 'EST-2-2',
            "name": "i5",
            'price': 195.00,
            'count': 5
        }, {
            "id": 'EST-2-3',
            "name": "i7",
            'price': 255.00,
            'count': 2
        }]
    }]
}];

$(function () {
    $('#dg').datagrid({
        data: data
    }).datagrid('enableCellEditing').datagrid('gotoCell', {
        index: 0,
        field: 'productid'
    });
});