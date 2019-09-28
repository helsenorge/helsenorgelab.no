function selectSearchBox() {
	setTimeout(() => {
		const nS = $('#navbarSearch');
		nS.is(':visible') && nS.focus();
	}, 400)
}