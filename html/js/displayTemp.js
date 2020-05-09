var data_url = "../getTemperature.php?limit=10";

function clickedButton(element) {
    switch (element.id) {
        case "btn_temp_last_10":
            data_url = "../getTemperature.php?limit=lastTen";
            break;
        case "btn_temp_last_50":
            data_url = "../getTemperature.php?limit=lastFifty";
            break;
        case "btn_temp_10":
            data_url = "../getTemperature.php?limit=10";
            break;
        case "btn_temp_50":
            data_url = "../getTemperature.php?limit=50";
            break;
        case "btn_temp_all":
            data_url = "../getTemperature.php?limit=all";
            break;
        default:
            data_url = "../getTemperature.php?limit=10";
            break;
    }
    return false;
}

window.onload = function () {
    document.getElementById("btn_temp_last_10").addEventListener("click", function() {
        clickedButton(document.getElementById("btn_temp_last_10"));
    }, false);
    document.getElementById("btn_temp_last_50").addEventListener("click", function() {
        clickedButton(document.getElementById("btn_temp_last_50"));
    }, false);
    document.getElementById("btn_temp_10").addEventListener("click", function() {
        clickedButton(document.getElementById("btn_temp_10"));
    }, false);
    document.getElementById("btn_temp_50").addEventListener("click", function() {
        clickedButton(document.getElementById("btn_temp_50"));
    }, false);
    document.getElementById("btn_temp_all").addEventListener("click", function() {
        clickedButton(document.getElementById("btn_temp_all"));
    }, false);
}

document.addEventListener("DOMContentLoaded", function() {
    var updateInterval = 1000;  //1000ms
    var ctx = document.getElementById("myChart");

    // chart setup
    var chartdata = {
        labels: [],
        datasets: [
            {
                label: 'Temperature [' + String.fromCharCode(176) + 'C]',
                backgroundColor: 'firebrick',
                borderColor: 'firebrick',
                lineTension: '0',
                fill: false,
                pointHoverBackgroundColor: "rgba(59, 89, 152, 1)",
                pointHoverBorderColor: "rgba(59, 89, 152, 1)",
                data: []
            },
        ]
    };

    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: chartdata,
        options: {
            responsive: true,
            animation: {
                duration: 1000 // general animation time default=1000
            },
            hover: {
                animationDuration: 400 // duration of animations when hovering an item default=400
            },
            responsiveAnimationDuration: 0, // animation duration after a resize
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: { display: true, labelString: 'Present time' }
                }],
                yAxes: [{
                    display: true,
                    ticks: { beginAtZero: true },   //graf bude vzdy zacinat od priamky y=0
                    scaleLabel: { display: true, labelString: 'Temperature [' + String.fromCharCode(176) + 'C]' }
                }]
            },
            legend: {
                display: false
            },
            tooltips: { mode: 'index', intersect: false, },
            hover: { mode: 'nearest', intersect: true }
        }
    });

    // chart update
    var updateChart = function () {
        // ../getTemperature.php?limit=all
        $.ajax({
            url: data_url,
            type: "GET",
            success: function (data) {
                
                myLineChart.data.datasets[0].data = [];
                myLineChart.data.labels = [];

                for (var j in data) {
                    myLineChart.data.datasets[0].data.push(data[j].temp);
                    myLineChart.data.labels.push(data[j].datetime);
                }

                myLineChart.update();
            },
            error: function (data) {
                console.log("Could not fetch data.");
            }
        });
    }

    setInterval(function () { updateChart() }, updateInterval); //updatne iba jednu hodnotu kazdych updateInterval
});
