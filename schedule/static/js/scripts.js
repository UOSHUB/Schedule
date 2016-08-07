$(document).ready(function(){
    $("#class-modal .modal-content > div").each(function(index, div) {
        $(div).addClass("col s6");
        $(div).children("span").addClass("tooltipped");
    });
    $(".tooltipped").tooltip({
        delay: 50,
        position: "right"
    });
    $("#side-bar").hover(function() {
        if($(this).width() < 61)
            $(this).animate({width: "240px"}, 300)
    }, function() {
        $(this).animate({width: "60px"}, 300, "swing");
        $("#side-bar .collapsible").each(function(index, item) {
            if($(item).find($(".collapsible-header")).hasClass("active"))
                $(item).find($(".collapsible-header")).click();
        });
    });
    $("#class-modal .fa-times").click(function() {
        $("#class-modal").closeModal({
            out_duration: 100,
            starting_top: "15%",
            ending_top: "25%"
        });
    });
});

function highlight(semester) {
    $("#semesters li > a.selected").each(function(index, option) {
        $(option).removeClass("selected");
    });
    $("#" + semester).addClass("selected");
}
