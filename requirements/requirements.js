$(document).ready(function () {
    $("#buyerTab").click(function () {
        $("#createReqTab").toggle();
    });
});




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
    return alert("Post Requirement?");
}