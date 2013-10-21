$(document).ready(function() { 

function processInput() {
$.ajax({
cache: false,
url: "/ajax/processinput",
type: "POST",
contentType: "application/json",
dataType: "json",
data: JSON.stringify({ "input": $("#typehere").val() })
}).done(function(json) {
$("#ajax-processedinput").html(json.processed);
}).error(function(json) {
$("#ajax-processedinput").html("connection to server lost...");
});
}

$("#typehere").change(function () {
processInput();
});
});

