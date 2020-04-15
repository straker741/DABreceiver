
function updateImage() {
    document.getElementById("image_psd").src = "obrazky/power_spectral_density.png?rand=" + Math.random();
}
setInterval(function () { updateImage() }, 4500);
