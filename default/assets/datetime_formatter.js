var shortDateTags = document.getElementsByClassName("short-datetime");

var todayStart = new Date()
todayStart.setHours(0, 0, 0, 0)
var todayStartTimestamp = todayStart.getTime()
var yesterdayStartTimestamp = todayStart.setDate(todayStart - 1)
for (var i = 0; i < shortDateTags.length; i++) {
	var date = new Date(shortDateTags[i].textContent)
	var timestamp = date.getTime()

	var text;
	if (timestamp >= todayStartTimestamp) {
		text = 'today';
	} else if (timestamp >= yesterdayStartTimestamp) {
		text = 'yesterday';
	} else {
		text = date.toDateString()
	}
	
	shortDateTags[i].textContent = text;
}
