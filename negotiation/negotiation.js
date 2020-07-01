$(document).ready(function () {
    //Fixing jQuery Click Events for the iPad
    var ua = navigator.userAgent,
        event = (ua.match(/iPad/i)) ? "touchstart" : "click";
    if ($('.table').length > 0) {
        $('.table .header').on(event, function () {
            $(this).toggleClass("active", "").nextUntil('.header').css('display', function (i, v) {
                return this.style.display === 'table-row' ? 'none' : 'table-row';
            });
        });
    }

    $("#buyerTab").click(function () {
        $("#createReqTab").toggle();
    });
});

(() => {
    let customSelects = document.querySelectorAll(".custom-dropdown__select");
    customSelects.forEach(el => {
        if (el.disabled)
            el.parentNode.classList.add("custom-dropdown--disabled");
    })
})();

function showThis(ii) {
    document.getElementById("thisDiv1").style.display = "none";
    document.getElementById("thisDiv2").style.display = "none";
    document.getElementById("thisDiv" + ii).style.display = "block";
}

function validateForm() {
    var x = document.forms["requirementForm"]["title"].value;
    var x2 = document.forms["requirementForm"]["Quantity"].value;
    if (x == "") {
        alert("Error in Creating Request. Fill all Information Carefully");
        return false;
    }
    if (parseInt(x2) <= 0) {
        alert("Error in Creating Request. Fill all Information Carefully");
        return false;
    }
}