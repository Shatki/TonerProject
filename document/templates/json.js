/**
 * Created by Shatki on 26.01.17.
 */
var url;
function newDocument() {
    $('#dlg').dialog('open').dialog('setTitle', 'Новая накладная');
    $('#fm').form('clear');
    url = 'save_user.php';
}

function savedocument() {
    $('#fm').form('submit', {
        url: url,
        onSubmit: function () {
            return $(this).form('validate');
        },
        success: function (result) {
            var result = eval('(' + result + ')');
            if (result.errorMsg) {
                $.messager.show({
                    title: 'Error',
                    msg: result.errorMsg
                });
            } else {
                $('#dlg').dialog('close');		// close the dialog
                $('#dg').datagrid('reload');	// reload the user data
            }
        }
    });
}
function destroyDocument() {
    var row = $('#dg').datagrid('getSelected');
    if (row) {
        $.messager.confirm('Confirm', 'Вы действительно хотели бы удалить этот документ?', function (r) {
            if (r) {
                $.post('destroy_user.php', {id: row.id}, function (result) {
                    if (result.success) {
                        $('#dg').datagrid('reload');	// reload the user data
                    } else {
                        $.messager.show({	// show error message
                            title: 'Error',
                            msg: result.errorMsg
                        });
                    }
                }, 'json');
            }
        });
    }
}


function saveItem() {
    var data = $('#item-info-fm').serialize();
    $.ajax({
        url: '../item/add/',
        method: 'POST',
        data: data,
        cache: false,
        //beforeSend: function (xhr) {
        //    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        //    return $('#item-info-fm').form('validate');
        //},
        success: function (data) {
            if (data == 'Ok') {
                // Пока кокой-то деревянный способ
                // alert('Данные получены');
                //location.href = "#";
                //location.reload();
                $('#item-add-dlg').dialog('close');      // close the dialog
                $('#item-table').datagrid('reload');    // reload the data table
            } else {
                // Данные получены кривые
                return $('#item-info-fm').form('validate');
                // location.href = "#";
                // location.reload();
            }
        }
    });
}


function saveItem() {
    var data = $('#item-info-fm').serialize();
    $('#item-info-fm').form({
        url: '../item/add/',
        method: 'POST',
        //data: data,
        cache: false,
        onSubmit: function () {
            return $(this).form('validate');
        },
        success: function (data) {
            if (data == 'Ok') {
                // Пока кокой-то деревянный способ
                alert('Данные получены');
                //location.href = "#";
                //location.reload();
                $('#item-add-dlg').dialog('close');      // close the dialog
                $('#item-table').datagrid('reload');    // reload the data table
            } else {
                alert(data);
                // location.href = "#";
                // location.reload();
            }
        }
    });
}


var data = {'item_id': $('#item-table').datagrid('getSelected').id};
$.ajax({
    url: '../item/json/',
    method: 'POST',
    data: data,
    cache: false,
    success: function (data) {
        if (data.status == 'Ok') {
            $('#product-tg').treegrid('select', data.product_id);
            $('#serial-number').textbox('setValue', data.serial_number);
            $('#warranty').textbox('setValue', data.warranty);
            $('#country').combobox('setValue', data.warranty);

            //$('#item-add-dlg').dialog('close');      // close the dialog
            //$('#item-table').datagrid('reload');    // reload the data table
        } else {
            // alert(data);
            // Данные получены кривые, закрываемся
            $('#item-add-dlg').dialog('close');      // close the dialog
            $('#item-table').datagrid('reload');    // reload the data table
        }
    }
});
$('#product-tg').treegrid('reload');