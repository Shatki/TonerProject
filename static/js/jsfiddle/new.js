/**
 * Created by Shatki on 13.09.2017.
 */
var data = {
    "total": 3,
    "rows": [{
        "productid": "PRT-15-031",
        "itemid": "EST-1",
        "productname": "Epson WorkForce 845",
        "quantity": 69,
        "price": 121.29,
        "measure": "pcs",
        "attr1": "retail"
    }, {
        "productid": "PRT-DL-044",
        "itemid": "EST-10",
        "productname": "Canon PIXMA MG5320",
        "quantity": 12,
        "price": 110.50,
        "measure": "pcs",
        "attr1": "retail"
    }, {
        "productid": "PRT-SN-201",
        "itemid": "EST-11",
        "productname": "HP Deskjet 1000 Printer",
        "quantity": 63,
        "price": 33.95,
        "measure": "pcs",
        "attr1": "retail"
    }]
};

var measure = [{
    "id": 1,
    "name": "pcs"
}, {
    "id": 2,
    "name": "wth"
}, {
    "id": 3,
    "name": "vol"
}];

var response = [{
    'id': 'DIR-0',
    'name': "Printers",
    'iconCls': "printer",
    'children': [{
        "id": 'DIR-1',
        "name": "Laser",
        "children": [{
            "id": 'DIR-1-1',
            "name": "HP",
            "state": "closed",
            "children": [{
                "id": 'EST-1-1-1',
                'iconCls': 'icon-print',
                'price': 86.3,
                'attr2': 'retail',
                "name": "LaserJet 1020"
            }, {
                "id": 'EST-1-1-2',
                'iconCls': 'icon-print',
                'price': 126.2,
                'attr2': 'retail',
                "name": "LaserJet P1005"
            }, {
                'id': 'EST-1-1-4',
                'iconCls': 'icon-print',
                'price': 209.7,
                'attr2': 'retail',
                'name': 'LaserJet M402dn'
            }, {
                'id': 'EST-1-1-5',
                'iconCls': 'icon-print',
                'price': 183.1,
                'attr2': 'retail',
                'name': 'LaserJet 4050dn'
            }]
        }, {
            "id": 'DIR-1-2',
            "name": "Canon",
            "state": "closed",
            "children": [{
                'iconCls': 'icon-print',
                'id': 'EST-1-2-3',
                'price': 125.5,
                'attr2': 'retail',
                'name': 'i-SENSYS LBP2900'
            }]
        }]
    }, {
        "id": 'DIR-2',
        "name": "Cartridge",
        "state": "closed",
        "children": [{
            "id": 'EST-2-1',
            "name": "Q2512A",
            'price': 45.00,
            'attr2': 'retail'
        }, {
            "id": 'EST-2-2',
            "name": "CE505A",
            'price': 95.00,
            'attr2': 'retail'
        }, {
            "id": 'EST-2-3',
            "name": "Cartridge 703",
            'price': 51.00,
            'attr2': 'retail'
        }]
    }]
}];

$(function () {
    $('#dg').datagrid({
        data: data,
        clickToEdit: false,
        dblclickToEdit: true
    }).datagrid('enableCellEditing').datagrid('gotoCell', {
        index: 0,
        field: 'productid'
    });
});
