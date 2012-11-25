<html>
<head>
<script>
	function login() {
		alert();
	    var username = document.getElementById("username").value;
	    var password = document.getElementById("password").value;
	
	    xhr = new XMLHttpRequest();
	    xhr.open("POST", "http://localhost/login.php", false, username, password);
	    xhr.send(null);
	
	    return xhr.status == 200;
	}
</script>
</head>
<body>
	<div style="margin: 10% 0 0 40%">
		<!-- <form method="post" onsubmit="return login();"> -->
		<form method="post">
			username: <input type="text" name="username" /><br/>
			password: <input type="password" name="password" /><br/>
			<input type="submit" />
			%if False:
			<p style="color: red">
				Login failed, please inpout correctly and try again.
			</p>
			%endif
		</form>
	</div>
</body>
</html>