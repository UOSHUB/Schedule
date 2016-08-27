// jQuery: When page is loaded
$(document).ready(function(){
    // On side-bar hover logic
    $("#side-bar").hover(function() {
        // Only if side-bar is at resting state
        if($(this).width() < 61)
            // Animate extending the width to 240px
            $(this).animate({width: "240px"}, 300)
    // When mouse isn't hovering in side-bar
    }, function() {
        // Animate shrinking the width to 60px
        $(this).animate({width: "60px"}, 300);
        // As side-bar closes, loop through each collapsible list
        $("#side-bar .collapsible").each(function(index, item) {
            // If collapsible list is open
            if($(item).find($(".collapsible-header")).hasClass("active"))
                // Click it to close it
                $(item).find($(".collapsible-header")).click();
        });
    });
});
// Highlights selected semester
function highlight(semester) {
    // Loop through each "a" element in semesters list items
    $("#semesters li > a.selected").each(function(index, option) {
        // Remove the "selected" class (to prevent multi-selection)
        $(option).removeClass("selected");
    });
    // Add "selected" class to the selected semester
    $("#" + semester).addClass("selected");
}
