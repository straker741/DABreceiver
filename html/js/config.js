function clickButton() {
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
    return false;
}