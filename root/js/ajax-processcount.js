$(document).ready(function() { 

function updateProcessCount() {
$.ajax({
cache: false,
url: "/ajax/processcount",
type: "GET",
contentType: "application/json",
}).done(function(json) {
$("#ajax-processcount").html(json.processcount);
}).error(function(json) {
$("#ajax-processcount").html("connection to server lost...");
});
}

setInterval(updateProcessCount, (5 * 1000));
});

