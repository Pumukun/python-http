/*var e = document.getElementById("select-menu");
if (e !== null) {
	var value = e.value;
	var text = e.options[e.selectedIndex].text;
}*/

var text;

const selectElement = document.querySelector('#select-menu');
	selectElement.addEventListener('change', (event) => {
		text = event.target[event.target.selectedIndex].text;
});

document.querySelector("#reload_btn").addEventListener('click', async function() {
	try {
		let text_data = await downloadFile();
		document.querySelector("#preview-text").textContent = text_data;
	}
	catch(e) {
		alert(e.message);
	}
});

async function downloadFile() {
	let	response = await fetch("static/tmp_upload/" + text);
		
	if(response.status != 200) {
		throw new Error("Server Error");
	}
		
	let text_data = await response.text();

	return text_data;
}

