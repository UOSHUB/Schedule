$(document).ready(function(){
    $("#side-bar").hover(function() {
        $(this).animate({width: "240px"}, 300);
    }, function() {
        $(this).animate({width: "60px"}, 300);
    });
});
