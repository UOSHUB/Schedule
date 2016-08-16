// Configure Materialize components
$(document).ready(function(){
    // Initialize sidebar for small screens
    $('.button-collapse').sideNav({
        menuWidth: 200,
        edge: 'right',
        closeOnClick: true
    });
    $('.dropdown-button').dropdown({
        inDuration: 300,
        outDuration: 225,
        constrain_width: false, // Does not change width of dropdown to that of the activator
        hover: true, // Activate on hover
        gutter: 0, // Spacing from edge
        belowOrigin: false, // Displays dropdown below the button
        alignment: 'left' // Displays dropdown with edge aligned to the left of button
    });
});

/* This method hides the sidebar when
 * the screen becomes wider than 992px
 * It's executed whenever the screen size
 * changes, but it's guaranteed to run only
 * when needed.
 */
// Initialize sidebar visibility flag as true
var visible = true;
// Run on screen resize event
$(window).resize(function() {
    // Check if screen is wider than 992px
    if (window.innerWidth > 992) {
        // Only execute when sidebar is visible
        if (visible) {
            // Hide sidebar
            $('.button-collapse').sideNav('hide');
            // Set visibility to false
            visible = false;
        }
    // When screen is small set sidebar as visible
    } else if (!visible) visible = true;
});

// Display progress to user while waiting, it'll
function loggingIn() {
    // Check if fields aren't empty
    if(pin.value != '' && sid.value != '') {
        // Display Loading for 5 sec
        Materialize.toast('<i class=\"fa fa-spinner fa-pulse fa-2x\"></i>&nbsp;&nbsp;&nbsp;Loading...', 7500);
        // Display Almost done for the next 5 sec
        setTimeout("Materialize.toast('<i class=\"fa fa-spinner fa-pulse fa-2x\"></i>&nbsp;&nbsp;&nbsp;Almost done....', 7500)", 7600);
        // Display Preparing your dashboard for the next 5 sec
        setTimeout("Materialize.toast('<i class=\"fa fa-spinner fa-pulse fa-2x\"></i>&nbsp;&nbsp;&nbsp;Preparing your dashboard...', 7500)", 15200);
        // Display Something went wrong for the next 5 sec
        setTimeout("Materialize.toast('<i class=\"fa fa-spinner fa-pulse fa-2x\"></i>&nbsp;&nbsp;&nbsp;Something went wrong!..', 7500)", 22800);
        // Finally if it took all this time, display Please refresh the page for the next 20 sec
        setTimeout("Materialize.toast('<i class=\"fa fa-exclamation-triangle fa-2x\"></i>&nbsp;&nbsp;&nbsp;Please refresh the page!!', 30000)", 30400);
    }
}
