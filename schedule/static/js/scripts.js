$(document).ready(function(){
    $("#side-bar").hover(function() {
        $(this).animate({width: "240px"}, 300);
    }, function() {
        $(this).animate({width: "60px"}, 300);
        $("#side-bar .collapsible").each(function(index, item) {
            if($(item).find($(".collapsible-body")).is(":visible"))
                $(item).find($(".collapsible-header")).click();
        });
    });
});

function highlight(semester) {
    $("#semesters li > a.selected").each(function(index, option) {
        $(option).removeClass("selected");
    });
    $("#" + semester).addClass("selected");
}
