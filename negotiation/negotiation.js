$(document).ready(function () {
    $("#buyerTab").click(function () {
        $("#createReqTab").toggle();
    });
});

function showThis(ii) {
    document.getElementById("thisDiv1").style.display = "none";
    document.getElementById("thisDiv2").style.display = "none";
    document.getElementById("thisDiv" + ii).style.display = "block";
}