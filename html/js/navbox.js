window.onscroll = function () {
    var nav = document.getElementById('nav');
    var box = document.getElementById('box');

    window.onscroll = function () {
        if (window.pageYOffset > 78.2) {        //velkost loga skoly - prveho .head
            nav.style.position = "fixed";
            nav.style.top = 0;                  //podobne ako margin
            box.style.marginTop = "54.2px";     //velkost navbaru o ktory sa musi text posunut
        } else {
            // nav.style.position = "absolute";
            nav.style.position = "relative"; //fixed
            nav.style.top = 0;
            box.style.marginTop = "0px";
        }
    }
}