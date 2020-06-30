
var check = false;
function save(event) {

    if (check == true) {
        event.preventDefault();
    }
    check = true;
}

function negotiate(dP) {
    check = true;
    var tprice = dP;
    var negprice = prompt("Please enter the amount you want", tprice);
    console.log(tprice, negprice);
    var priceSent = tprice;
    if (parseInt(negprice) < parseInt(tprice) && parseInt(negprice) >= 0) {
        priceSent = negprice;
        alert("Negotiated price (" + priceSent + ") sent to merchant");
    } else if (parseInt(negprice) >= parseInt(tprice) || parseInt(negprice) < 0) {
        priceSent = tprice;
        alert("Negotiated Price should be greater than 0 and less than Discount price(" + tprice + ")");
        alert("Discount price (" + priceSent + ") sent to merchant");
    }
    document.getElementById("Negotiated").value = parseInt(priceSent);
}

function payment() {
    check = true;
    return alert("you want to proceed for payment? Once Proceed you will not able to edit your cart.");
}

function goBack() {
    return window.history.back();
}

function showDetails() {
    document.getElementById("contact").style.display = "block";

}

function hideDetails() {
    document.getElementById("contact").style.display = "none";
}

function addItems() {
    var x = document.getElementById("emptyCart").name;
    return window.location = x;
}