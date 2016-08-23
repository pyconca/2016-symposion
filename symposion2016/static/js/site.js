$(document).ready(function () {
	var $backgroundPattern1 = $('#background-pattern-1');
	// Entry of the background pattern on the home page
	$('<img />')
		.on('load', function() {
			$backgroundPattern1.animate({
				opacity: 0.8,
				top: '-200px',
				left: '-80px'
			}, 500);
		})
		.attr('src', $backgroundPattern1.find('img').attr('src'));
});
