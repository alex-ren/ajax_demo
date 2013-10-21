
$(document).ready(function() { 

function updateDateTime() {
$.ajax({
cache: false,
url: "/ajax/time",
type: "GET",
contentType: "application/json",
}).done(function(json) {
$("#ajax-datetime").html(json.time);
});
}

setInterval(updateDateTime, (3 * 1000));
});

