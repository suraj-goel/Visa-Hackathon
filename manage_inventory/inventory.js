$(document).ready(function() {
  $("#formButton").click(function() {
    $("#form1").toggle();
  });
});

function checkvalue(val)
{
    if(val==="others")
       document.getElementById('category').style.display='block';
    else
       document.getElementById('category').style.display='none';
}

function validate(id) {
        var element = document.getElementById(id);
        if (parseInt(element.value) <= 0) {
            alert(id +" value should be greater than 0");
            element.value = "1";
            element.focus();
    }
}


$(document).ready(function() {
    var ua = navigator.userAgent,
        event = (ua.match(/iPad/i)) ? "touchstart" : "click";
    if ($('.table').length > 0) {
        $('.table .header').on(event, function() {
            $(this).toggleClass("active", "").nextUntil('.header').css('display', function(i, v) {
                return this.style.display === 'table-row' ? 'none' : 'table-row';
            });
        });
    }
})