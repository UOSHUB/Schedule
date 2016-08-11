// jQuery: When page is loaded
$(document).ready(function(){
    // A for each loop through class-modal divs to add common classes
    $("#class-modal .modal-content > div").each(function(index, div) {
        // Add "col s6" classes to all divs
        $(div).addClass("col s6");
        // Add "tooltipped" class to all spans in all divs
        $(div).children("span").addClass("tooltipped");
    });
    // Initialize "tooltipped" class with some configs
    $(".tooltipped").tooltip({
        delay: 100, // Delay 100 msec before tooltip appears
        position: "right" // Make tooltip appear to the right
    });
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
    // When closing class-modal modal through click the x button
    $("#class-modal .fa-times").click(function() {
        // Close class-modal with some configs
        $("#class-modal").closeModal({
            out_duration: 100, // Fast Transition out duration
            starting_top: "15%", // Start animation from 15% of screen
            ending_top: "25%" // Stop animation at 25% of screen
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
