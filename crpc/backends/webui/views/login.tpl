<html>
<head>
</head>
<body>
	<div style="margin: 10% 0 0 40%">
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