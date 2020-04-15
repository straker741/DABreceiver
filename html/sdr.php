<?php
    $channels = array(
        "174928000" => "5A",
        "176640000" => "5B",
        "178352000" => "5C",
        "180064000" => "5D",
        "181936000" => "6A",
        "183648000" => "6B",
        "185360000" => "6C",
        "187072000" => "6D",
        "188928000" => "7A",
        "190640000" => "7B",
        "192352000" => "7C",
        "194064000" => "7D",
        "195936000" => "8A",
        "197648000" => "8B",
        "199360000" => "8C",
        "201072000" => "8D",
        "202928000" => "9A",
        "204640000" => "9B",
        "206352000" => "9C",
        "208064000" => "9D",
        "209936000" => "10A",
        "211648000" => "10B",
        "213360000" => "10C",
        "215072000" => "10D",
        "216928000" => "11A",
        "218640000" => "11B",
        "220352000" => "11C",
        "222064000" => "11D",
        "223936000" => "12A",
        "225648000" => "12B",
        "227360000" => "12C",
        "229072000" => "12D",
        "230784000" => "13A",
        "232496000" => "13B",
        "234208000" => "13C",
        "235776000" => "13D",
        "237488000" => "13E",
        "239200000" => "13F",
    );
    
    function getFrequency() {		
		global $channels;
        $myfile = fopen("/var/www/html/config.txt", "r") or die("Unable to open file!");
        $freq = trim(fgets($myfile));    
        fclose($myfile);
        if (isset($channels[$freq])) {
            return $freq / 1000;
        }
		else {
            return "Nepodarilo sa načítať frekvenciu!";	
        }
	}
    
	function setConfig() {
        global $channels;
        $setConfig = FALSE;
        if (isset($_GET['freq']) and isset($_GET['mode'])) {	
			if (is_numeric($_GET['freq'])) {			
				if (isset($channels[$_GET['freq'] * 1000])) {                  
                    $freq = $_GET['freq'] * 1000;
                    $setConfig = TRUE;

                    if ($_GET['mode'] == "analyze" or $_GET['mode'] == "search") {
                        $mode = $_GET['mode'];
                    }
                    else {
                        $mode = "search";
                    }     
				}
			}
		}
        if($setConfig) {
			$myfile = fopen("/var/www/html/config.txt", "w") or die("Unable to open file!");
			settype($freq, "string");			
			fwrite($myfile, $freq . "\n" . $mode . "\n");
            fclose($myfile);
            // Start shell command
            //$error = shell_exec('/usr/bin/nohup /usr/bin/python3 /var/www/html/python/eventHandler.py >/dev/null 2>&1 &');
            
            $error = shell_exec('python3 ~/DABreceiver/python/eventHandler.py');
            $myfile = fopen("~/DABreceiver/python/test.txt", "w") or die("Unable to open file!");
            fwrite($myfile, $error . "\n");
            fclose($myfile);
		}
	}
	setConfig();
?>

<!DOCTYPE html>

<html lang="sk">
<head>
    <meta charset="utf-8" />
    <title>Raspberry pi</title>
    <link rel="stylesheet" type="text/CSS" href="bakalarka.css">
    <link rel="shortcut icon" href="obrazky/favicon.ico">
    <meta author="Jakub Švajka" />
    <script type="text/javascript" src="js/navbox.js"></script>
    <script type="text/javascript" src="js/updateImage.js"></script>
    <script type="text/javascript" src="js/config.js"></script>
</head>
<body>
    <header>
        <div class="container">
            <a href="https://www.fei.stuba.sk/">
                <img src="obrazky/logo_fei.png" alt="Slovenská Technická Univerzita Fakulta Elektrotechniky a Informatiky" />
            </a>
        </div>
        <nav id="nav">
            <ul class="container">
                <li><a href="index.html">DOMOV</a></li>
                <li><a href="sdr.php">SDR</a></li>
                <li><a href="teplota.html">TEPLOTA</a></li>
                <li><a href="dokumentacia.html">DOKUMENTÁCIA</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="container" id="box">
            <div class="block_container">
                <div class="block_header">Softvérovo definované rádio</div>
                <div class="block_body">
                    <table>
                        <tbody>
                            <tr>
                                <td>Nastavená frekvencia [kHz]:</td>
                                <td>
                                    <?php
                                       echo getFrequency();								
                                    ?>
                                </td>
                            </tr>
                            <form>
                                <tr>								
                                    <td><label for="freq">Centrálna frekvencia [kHz]:</label></td>
                                    <td>
                                        <input type="text" id="freq" name="freq" placeholder="Frekvencia [kHz]">
                                    </td>								
                                </tr>
                                <tr>								
                                    <td><label for="mode">Zvoľte pracovný mód:</label></td>
                                    <td>                                     
                                        <select name="mode" id="mode">
                                            <option value="search">Search</option>
                                            <option value="analyze">Analyze</option>
                                        </select>                                                                       
                                    </td>
                                    							
                                </tr>
                                <tr>
                                    <td>
                                    </td>
                                    <td>
                                        <input type="submit" onclick="return clickButton();">    
                                    </td>
                                </tr>
                            </form>					
                        </tbody>				
                    </table>                            
                    <p>Tuner Fitipower FC0012 je schopný fungovať len v pásme Band III.</p>
                    <br />
                    <hr />
                    <img id="image_psd" src="obrazky/power_spectral_density.png" alt="Power spectral density">
                </div>
            </div>
        </div>
    </main>

    <!-- END OF MAIN -->
    <div class="validator">
        Slovenská Technická Univerzita &copy; Jakub Švajka
    </div>
</body>
</html>
