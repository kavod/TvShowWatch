<html><body>
<form method="POST" action="upload.php" enctype="multipart/form-data">
	<h1>Tracker</h1>
	Tracker provider: <select name="tracker_id"><option value="t411">T411</option></select><br />
	Username : <input type="text" name="tracker_username" /></br >
	Password : <input type="password" name="tracker_password" /><br />
	Defaults keywords: <input type="text" name="tracker_keywords" /><br />

	<h1>Transmission</h1>
	Transmission server: <input type="text" name="trans_server" /></br >
	Transmission port: <input type="text" name="trans_port" /></br >
	Transmission Username : <input type="text" name="trans_username" /></br >
	Transmission Password : <input type="password" name="trans_password" /><br />
	Transmission maximum slots: <select name="trans_slotNumber"><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6" selected="selected">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option></select><br />
	Transfer Local directory (keep empty for disable) : <input type="text" name="trans_folder" /></br >

	<h1>Email notification</h1>
	Enable: <select name="smtp_enable"><option value="0" selected="selected">No</option><option value="1">Yes</option></select><br />
	SMTP server: <input type="text" name="smtp_server" /></br ><br />
	SMTP port: <input type="text" name="smtp_port" /></br ><br />
	SSL/TLS encryption: <select name="smtp_ssltls"><option value="0" selected="selected">No</option><option value="1">Yes</option></select><br />
	Authentification Username : <input type="text" name="smtp_username" /></br >
	Authentification Password : <input type="password" name="smtp_password" /><br />
	Sender Email: <input type="text" name="smtp_emailSender" /></br ><br />

	TvShow file: <input type="file" name="config" /><br />
	
	<input type="submit" name="envoyer" value="Envoyer le fichier">
</form>
</body></html>
