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

function process(index) {
	var dict = {"index": index, "table": text};
    $.ajax({
        url: "/api/set_table/" + index,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(dict),
        success: function (data) {
			const div_table = document.getElementById("table");
			div_table.innerHTML = "";
            div_table.insertAdjacentHTML("beforeend", data["csv_table"]);

			const div_column_menu = document.getElementById("table_columns");
			div_column_menu.innerHTML = ""; 

			var select_column_menu = document.createElement("select");
			select_column_menu.setAttribute("id", "col_menu");
			select_column_menu.setAttribute("class", "select-menu");
			select_column_menu.setAttribute("multiple", "multiple")

			var options = data["columns"];

			for (var i = 0; i < options.length; i++) {
				var optionElement = document.createElement("option");
				optionElement.value = options[i];
				optionElement.text = options[i];
				select_column_menu.appendChild(optionElement);
			}
			
			select_column_menu.size = data["columns"].length

			div_column_menu.appendChild(select_column_menu);
        },
    });
}

function get_select_values(select) {
	var result = [];
	var options = select && select.options;
	var opt;

	for (var i = 0, length = options.length; i < length; i++) {
		opt = options[i];

		if (opt.selected) {
			result.push(opt.value || opt.text);
		}
	}
	return result;
}

function reload_table(index) {
	const col_menu = document.getElementById("col_menu");
	
	if (col_menu) {
		const sel_columns = get_select_values(col_menu);
		var dict = {"table": text, "sel_columns": sel_columns};
	}

	$.ajax({
		url: "/api/update_table/" + index,
		type: "POST",
		contentType: "application/json",
		data: JSON.stringify(dict),
		success: function (data) {
			const div_table = document.getElementById("table");
			div_table.innerHTML = "";
            div_table.insertAdjacentHTML("beforeend", data["csv_table"]);
		},
	});
}

