$(document).ready(function(){
    // Initialize login modal
	$('.modal-trigger').leanModal({
		dismissible: true,
		opacity: 0.2,
		in_duration: 350,
		out_duration: 250
    });
    // Initialize sidebar for small screens
    $('.button-collapse').sideNav({
        menuWidth: 200,
        edge: 'right',
        closeOnClick: true
        }
    );
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
            $('.button-collapse').sideNav('hide')
            // Set visibility to false
            visible = false;
        }
    // When screen is small set sidebar as visible
    } else if (!visible) visible = true;
});