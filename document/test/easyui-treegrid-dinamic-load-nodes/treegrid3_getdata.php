<?php
$id = isset($_POST['id']) ? intval($_POST['id']) : 0;

include 'conn.php';
$result = array();
$rs = mysql_query("select * from products where parentId=$id");
while($row = mysql_fetch_array($rs)){
	$row['state'] = has_child($row['id']) ? 'closed' : 'open';
	$row['total'] = $row['price']*$row['quantity'];
	array_push($result, $row);
}

echo json_encode($result);

function has_child($id){
	$rs = mysql_query("select count(*) from products where parentId=$id");
	$row = mysql_fetch_array($rs);
	return $row[0] > 0 ? true : false;
}

?>
