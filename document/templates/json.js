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