Globals = {}
Globals.shapeCounter = 0;

function init() {
	add_row()
}

function add_row() {
	Globals.shapeCounter++;
	var name = "Shape_" + Globals.shapeCounter;
	var weight = 10;

	var col0 = $("<td>");
	col0.append("<table width='200'>");
	col0.append("<tr><td>Name:</td><td><input class='name_input' type='text' value='" + name +"'/></td></tr>")
	col0.append("<tr><td>Weight:</td><td><input class='weight_input' type='text' value='" + weight + "'/></td></tr>")
	col0.append("</table>")

	var col1 = $("<td>")
	col1.append("<textarea class='shape_textbox' resizable='false'></textarea>")

	var col2 = $("<table class='transform_table'>");
	var heading_row = $("<tr>")
	heading_row.append("<td>")
	heading_row.append("<td>Default</td>")
	heading_row.append("<td>90\xB0</td>")
	heading_row.append("<td>180\xB0</td>")
	heading_row.append("<td>270\xB0</td>")
	col2.append(heading_row)
	for (var y=0; y<2; y++) {
		var check_row = $("<tr>");
		if (y == 0) {
			check_row.append("<td style='text-align: left'>Default</td>");
		} else {
			check_row.append("<td style='text-align: left'>Flip X</td>");
		}
		for (var x=0; x<4; x++) {
			var cell = $("<td width='35' height='25'></td>");
			var checker = $("<input class='transform_checkbox' type='checkbox'>");
			if (x == 0 && y == 0) {
				checker.attr("checked", "true");
				checker.click(function() { return false; });
			}
			cell.append(checker);
			check_row.append(cell);
		}
		col2.append(check_row);
	}

	var col3 = $("<td width='30'>");

	var col4 = $("<td>");
	var remove_button = $("<a href='#'>Remove</a>");
	remove_button.click(delete_row)
	col4.append(remove_button)

	// col4.append("<a href='#' onclick='delete_row'>Remove</a>");
	// var delete_col = $("<tr><td colspan='2'></td></tr>")
	// col4.append("<a href='#' onclick='delete_row'>Remove</a></td></tr>");

	var row = $("<tr class='shape_row'>");
	row.append(col1, col0, col2, col3, col4);
	$("#shape_table").append(row, "<tr height='15'/>");
}

function delete_row(ev) {
	$(ev.target).closest(".shape_row").remove()
}

function generate_code() {
	result = [];
	errors = []
	$("#shape_table").find(".shape_row").each(function(i, row) {
		console.log(row);
		shape = {}
		shape['name'] = $(row).find('.name_input').val();
		shape['weight'] = $(row).find('.weight_input').val();
		shape['mask'] = $(row).find('.shape_textbox').val();

		shape['transforms'] = []
		mapping = {
			0: "0,0",
			1: "90,0",
			2: "180,0",
			3: "270,0",
			4: "0,1",
			5: "90,1",
			6: "180,1",
			7: "270,1"
		};
		$(row).find(".transform_checkbox").each(function(i, elem) {
			if (elem.checked) {
				shape['transforms'].push(mapping[i]);
			}
		});

		result.push(shape);
		response = validate(i, shape);
		if (response != null) {
			errors.push(response);
		}
	});

	if (errors.length > 0) {
		t = "Code Generation Failed\n\n";
		t += errors.join("\n\n");
		$("#codebox").val(t);
		$("#codebox").css("color", "red");
	} else {
		$("#codebox").val(JSON.stringify(result, null, 4))
		$("#codebox").css("color", "black");
	}
}

function validate(i, shape) {
	name = shape['name']
	if (name == "") {
		return "Entry #" + (i+1) + " is missing a Name!";
	}

	if (shape['weight'] == "") {
		return "\"" + name + "\" is missing a Weight!";
	}

	if (isNaN(shape['weight'])) {
		return "\"" + name + "\" has an invalid Weight!";
	}

	mask = shape['mask'];
	rows = mask.split('\n');

	if (mask == "") {
		return "\"" + name + "\" has an empty mask!";
	}

	// check for valid characters
	validChars = [
		'x', '-', '\n'
	]
	for (var i=0; i<mask.length; i++) {
		if (validChars.indexOf(mask[i]) === -1) {
			return "\"" + name + "\" has an invalid mask!\nInvalid character '" + mask[i] + "'";
		}
	}

	maxDim = rows.length;
	for (var i=0; i<rows.length; i++) {
		maxDim = Math.max(maxDim, rows[i].length);
	}
	if (maxDim > 4) {
		return "\"" + name + "\" has an invalid mask!\nOnly blocks up to 4x4 are supported.";
	}

	for (var i=1; i<rows.length; i++) {
		if (rows[i].length != rows[i-1].length) {
			return "\"" + name + "\" has an invalid mask!\nMasks must be rectangular.";
		}
	}
}
