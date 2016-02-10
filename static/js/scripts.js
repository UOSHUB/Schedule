$(document).ready(function(){	
	$('.modal-trigger').leanModal({
		dismissible: true,
		opacity: 0.2,
		in_duration: 350,
		out_duration: 250
    });
    
    $('.button-collapse').sideNav({
        menuWidth: 200,
        edge: 'right',
        closeOnClick: true
        }
    );
});