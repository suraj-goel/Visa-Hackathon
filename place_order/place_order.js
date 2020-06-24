// Validate all the input fields to get the no of products
function validate() {
    var n = document.getElementById("tableID").rows.length - 1;
    for (var i = 0; i < n; i++) {
        var quantity = document.getElementById("quantity" + i);
        var totalQuantity = document.getElementById("tquantity" + i);

        if (quantity.value == "" || quantity.value.length < 0 || quantity.value == null) {
            quantity.value = "0";
        }
        if (parseInt(quantity.value) > parseInt(totalQuantity.innerText)) {
            alert("Sorry !! \nWe have only " + totalQuantity.innerText + " units in our Stock.");
            quantity.value = totalQuantity.innerText;
        } else if (parseInt(quantity.value) < 0) {
            alert("Sorry !! \nMinimum amount to order is 0");
            quantity.value = "0";
        } else if (parseInt(quantity.value) >= 0 && parseInt(quantity.value) < parseInt(totalQuantity.innerText)) {
            quantity.value = parseInt(quantity.value);
        } else {
            quantity.value = totalQuantity.innerText;
        }
    }
    updateTotalPrice();
}

// Update the total price the the customer needs to give
function updateTotalPrice() {
    var n = document.getElementById("tableID").rows.length - 1;
    for (var i = 0; i < n; i++) {
        var pppID = "price" + i;
        var qrID = "quantity" + i;
        var disID = "offerOptions" + i;
        var tpID = "tprice" + i;
        var dpID = "dprice" + i;

        var price = document.getElementById(pppID).innerText;
        var qty = document.getElementById(qrID).value;
        var tprice = document.getElementById(tpID);
        tprice.innerText = price * qty;
        updateDiscount(qrID, disID, tpID, dpID);
    }
}

// Update the discounted price that the customer needs to give
function updateDiscount(qrID, disID, tpID, dpID) {
    var qty = document.getElementById(qrID).value;
    var discount = document.getElementById(disID);
    var cost = document.getElementById(tpID);
    var fcost = document.getElementById(dpID);
    var qID = String(qrID).charAt(String(qrID).length - 1);

    // for saving offers
    if (discount != null) {

        var v1 = document.getElementById("off" + qID);
        for (var i = 0, len = discount.options.length; i < len; i++) {
            if (discount.options[i].selected == true) {
                if (v1 != null)
                    v1.value = discount.options[i].text;
                break;
            }

        }
    }


    if (discount != null && cost != null) {
        disc = discount.value.split(" ")[0];

        if (parseInt(qty) >= parseInt(discount.value.split(" ")[1])) {
            fcost.innerText = cost.innerText - (cost.innerText * (disc / 100));
        } else {
            fcost.innerText = cost.innerText;
        }
    } else {
        fcost.innerText = cost.innerText;
    }
    var v2 = document.getElementById("dis" + qID);
    if (v2 != null)
        v2.value = fcost.innerText;
    findCartPrice();
}

// Show total price before discount and after discount
function findCartPrice() {
    var cp1 = document.getElementById("finalPrice");
    var cp2 = document.getElementById("CartPrice");

    if (cp1 != null && cp2 != null) {
        var n = document.getElementById("tableID").rows.length - 1;
        var res1 = 0;
        var res2 = 0;

        for (var i = 0; i < n; i++) {
            res1 += parseInt(document.getElementById("tprice" + i).innerText);
            res2 += parseInt(document.getElementById("dprice" + i).innerText);
        }
        cp1.innerHTML = res1;
        cp2.innerHTML = res2;
        var finalPrice = res1;
        var discountPrice = res2;
        sessionStorage.setItem("finalPrice", finalPrice);
        sessionStorage.setItem("discountPrice", discountPrice);
    }

}

// // Prevent Enter key from performing any function/event
// $(document).ready(function() {
//     $(window).keydown(function(event) {
//         if (event.keyCode == 13) {
//             event.preventDefault();
//             return false;
//         }
//     });
// });