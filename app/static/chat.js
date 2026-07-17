function escapeHtml(text) {
	var div = document.createElement("div");
	div.appendChild(document.createTextNode(text));
	return div.innerHTML;
}

function getBotResponse() {
	var rawText = $("#textInput").val();
	if (!rawText) {
		return;
	}
	var userHtml = '<p class="userText"><span>' + escapeHtml(rawText) + "</span></p>";
	$("#textInput").val("");
	$("#chatbox").append(userHtml);
	$("#chatbox").animate({ scrollTop: $("#chatbox").prop("scrollHeight") }, 700);
	$.get("/get", { msg: rawText }).done(function (data) {
		var botHtml = '<p class="botText"><span>' + escapeHtml(data) + "</span></p>";
		$("#chatbox").append(botHtml);
		$("#chatbox").animate({ scrollTop: $("#chatbox").prop("scrollHeight") }, 700);
	});
}

$(function () {
	$("#textInput").keypress(function (e) {
		if (e.which === 13) {
			getBotResponse();
		}
	});
	$("#buttonInput").click(function () {
		getBotResponse();
	});
});
