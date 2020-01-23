$(() => {
	$('#signup-form div.txtb input').focus(function () {
		$(this).addClass('focus');
	});

	$('#signup-form div.txtb input').focusout(function () {
		if ($(this).val() == '') {
			$(this).removeClass('focus');
		}
	});
});