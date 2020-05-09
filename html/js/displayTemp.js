var data_url = "../getTemperature.php?limit=10";
var lastDateTime = "";
var numberOfElements = 10;
var changeOccurred = true;

function clickedButton(element) {  
    switch (element.id) {
        case "btn_temp_10":
            numberOfElements = 10;
            break;
        case "btn_temp_50":
            numberOfElements = 50;
            break;
        case "btn_temp_all":
            numberOfElements = "all";
            break;
        default:
            numberOfElements = 10;
            break;
    }
    changeOccurred = true;
    lastDateTime = "";
    data_url = "../getTemperature.php?limit=" + numberOfElements;
    return false;
}

window.onload = function () {
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
        if (lastDateTime === "") {
            full_url = data_url;
        }
        else {
            full_url = data_url + "&dt=" + lastDateTime;
        }

        $.ajax({
            url: full_url,
            type: "GET",
            success: function (data) {
                if (!(data.length === 0)) {
                    if (changeOccurred === true) {
                        // True when change of limit occures
                        myLineChart.data.datasets[0].data = [];
                        myLineChart.data.labels = [];
                        for (var j in data) {
                            myLineChart.data.datasets[0].data.push(data[j].temp);
                            myLineChart.data.labels.push(data[j].datetime);
                        }
                        changeOccurred = false;
                    }
                    else {
                        if (numberOfElements === "all") {
                            // True when all data are being shown
                            for (var j in data) {
                                myLineChart.data.datasets[0].data.push(data[j].temp);
                                myLineChart.data.labels.push(data[j].datetime);
                            }
                        }
                        else if (numberOfElements > myLineChart.data.datasets[0].data.length) {
                            for (var j in data) {
                                myLineChart.data.datasets[0].data.push(data[j].temp);
                                myLineChart.data.labels.push(data[j].datetime);
                            }
                        }
                        else {
                            for (var j in data) {
                                myLineChart.data.datasets[0].data.shift();
                                myLineChart.data.datasets[0].data.push(data[j].temp);
                                myLineChart.data.labels.shift();
                                myLineChart.data.labels.push(data[j].datetime);
                            }
                        }
                    }
                    
                    lastDateTime = data[data.length - 1].datetime;
                    lastDateTime = lastDateTime.replace(/:/g, "-");
                    lastDateTime = encodeURIComponent(lastDateTime);
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
