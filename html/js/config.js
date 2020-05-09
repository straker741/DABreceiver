document.getElementById("sdr").addEventListener("click", function() {
    clickedButton(document.getElementById("sdr"));
}, false);

function clickedButton(element) {
    switch (element.id) {
        case "sdr":
            var freq = document.getElementById('freq').value;
            var mode = document.getElementById('mode').value;

            $.ajax({
                type: "get",
                url: "sdr.php",
                data:
                {
                    'freq': freq,
                    'mode': mode
                },
                cache: false,
                success: function () {
                    //alert('Data Send');           
                }
            });
            break;
        default:
            break;
    }
    return true;
}