(function() {
	function startGame(ai_1_strength, ai_2_strength, code) {
		$('#board').empty();

		var game = new C4({
			ai_1_strength: ai_1_strength,
			ai_2_strength: ai_2_strength,
			container: '#board',
			code: code,
		});
	}

	$("#yellow_select").on('change', function(ev) {
		var codebox = $("#yellow_player").find(".enter_code");
		if ($("#yellow_select").val() == 0) {
			// Human
			codebox.css("display", "none");
			codebox.find("textarea").val("");
		} else {
			// AI
			codebox.css("display", "block");
		}
	});

	$("#red_select").on('change', function(ev) {
		var codebox = $("#red_player").find(".enter_code");
		if ($("#red_select").val() == 0) {
			// Human
			codebox.css("display", "none");
			codebox.find("textarea").val("");
		} else {
			// AI
			codebox.css("display", "block");
		}
	});

	$('#starter').on('click', function() {
		var yellow = $("#yellow_select").val()
		var yellow_code = $("#yellow_player")
			.find(".enter_code")
			.find("textarea").val()

		var red = $("#red_select").val()
		var red_code = $("#red_player")
			.find(".enter_code")
			.find("textarea").val()

		startGame(
			yellow == 0 ? 0 : 5,
			red == 0 ? 0 : 5,
			{"yellow": yellow_code, "red": red_code}
		)

		// $.post("http://localhost:5000/init_game", {
		// 	yellow_code: yellow_code,
		// 	red_code: red_code,
		// }, function(res) {
		// 	startGame(
		// 		res,
		// 		yellow == 0 ? 0 : 5,
		// 		red == 0 ? 0 : 5
		// 	);
		// }).fail(function() {
		// 	alert("Can't connect to server!")
		// });
	}).trigger('click');
})();
