var currentYearElement = null;
var currentMonthElement = null;
var scrollButton = null;
var monthNames = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
var weekdayNames = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
var streamers;

function load() {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() { if (this.readyState == 4 && this.status == 200) {streamers = JSON.parse(this.responseText); populate();}};
    req.open("GET", "https://streaming.ensmann.de/streamers.json", true);
    req.send();
}

function populate() {
    scrollButton = document.getElementById("scrollButton");
    window.onscroll = scrollFunction;
    var contentElement = document.getElementById("content");

    var streamersDiv = document.createElement("div");
    streamersDiv.style.width = "100%";
    var streamersButton = document.createElement("button");
    streamersButton.innerHTML = "Streamerliste";
    streamersButton.classList.add("collapsible", "streamerlist");
    streamersButton.onclick = function() { openCollapsibleEvent(this); };
    streamersDiv.appendChild(streamersButton);
    var streamersContent = document.createElement("div");
    streamersContent.classList.add("content");
    for (var streamer in streamers["crew"]) {
        addStreamer(streamer, "crew", streamersContent);
    }
    var nLines = 3;
    for (var i = 0; i < nLines; ++i) {
        var line = document.createElement("hr");
        line.style.height = "1px";
        line.style.color = "#F0F0FF";
        line.style.backgroundColor = "#F0F0FF";
        line.style.borderWidth = "0px";
        line.style.margin = "0px";
        if (i == 0) {
            line.style.marginTop = "7px";
        }
        if (i < nLines - 1) {
            line.style.marginBottom = "2px";
        }
        else {
            line.style.marginBottom = "7px";
        }
        streamersContent.appendChild(line);
    }
    for (var streamer in streamers["friends"]) {
        addStreamer(streamer, "friends", streamersContent);
    }
    streamersDiv.appendChild(streamersContent);
    contentElement.appendChild(streamersDiv);

    var currentDate = new Date();
    var minYear = 2019;
    var maxYear = currentDate.getFullYear();
    var i, j;
    for (i = maxYear; i >= minYear; --i) {
        var yearDiv = createYearElements(currentDate, i)
        for (j = (i < maxYear ? 11 : currentDate.getMonth()); j >= 0; --j) {
            yearDiv.childNodes[1].appendChild(createMonthElements(currentDate, i, j));
        }
        contentElement.appendChild(yearDiv);
    }
    getEventData(currentDate.getFullYear(), currentDate.getMonth()+1, true);
}

function createYearElements(currentDate, i) {
    var yearDiv = document.createElement("div");
    yearDiv.style.width = "100%";
    var yearButton = document.createElement("button");
    yearButton.innerHTML = "" + i;
    yearButton.classList.add("collapsible", "year");
    yearButton.id = "" + i;
    if (currentDate.getFullYear() == i) {
        yearButton.classList.add("currentYear");
        currentYearElement = yearButton;
    }
    yearButton.onclick = function() { openCollapsibleEvent(this); };
    yearDiv.appendChild(yearButton);
    var monthContent = document.createElement("div");
    monthContent.classList.add("content");
    yearDiv.appendChild(monthContent);
    return yearDiv;
}

function createMonthElements(currentDate, i, j) {
    var monthDiv = document.createElement("div");
    var monthButton = document.createElement("button");
    monthButton.innerHTML = monthNames[j];
    monthButton.classList.add("collapsible", "month");
    monthButton.id = ("" + i) + (j < 10 ? "0" + j : j);
    if (currentDate.getFullYear() == i && currentDate.getMonth() == j) {
        monthButton.classList.add("currentMonth");
        currentMonthElement = monthButton;
    }
    monthButton.onclick = function() { openMonthEvent(this); };
    monthDiv.appendChild(monthButton);
    var monthEvents = document.createElement("div");
    monthEvents.classList.add("content");
    monthEvents.innerHTML = "Loading...";
    monthDiv.appendChild(monthEvents);
    return monthDiv;
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function darkenColor(color, percentage) {
    var c = hexToRgb(color);
    var perc = 1 - percentage;
    c.r = Math.floor(perc * c.r);
    c.g = Math.floor(perc * c.g);
    c.b = Math.floor(perc * c.b);
    return rgbToHex(c.r, c.g, c.b);
}

function addStreamer(streamer, type, streamersContent) {
    var streamerContainer = document.createElement("div");
    streamerContainer.classList.add("streamer");
    var link = document.createElement("a");
    link.href = "https:\\\\twitch.tv\\" + streamer;
    link.target = "_blank";
    var imageContainer = document.createElement("img");
    imageContainer.classList.add("profile");
    imageContainer.src = streamers[type][streamer]["pic"];
    link.appendChild(imageContainer);
    var nameContainer = document.createElement("span");
    nameContainer.classList.add("streamername");
    nameContainer.innerHTML = streamers[type][streamer]["dis"];
    streamerContainer.appendChild(link);
    streamerContainer.appendChild(nameContainer);
    streamerContainer.style.backgroundColor = darkenColor(streamers[type][streamer]["bg"], 0.1);
    streamerContainer.style.color = streamers[type][streamer]["font"];
    streamersContent.appendChild(streamerContainer);
}

function setFinalHeight(obj, content) {
    content.style.maxHeight = content.scrollHeight + "px";
    if (obj.classList.contains("month")) {
        content.parentNode.parentNode.style.maxHeight = content.scrollHeight + content.parentNode.parentNode.scrollHeight + "px";
    }
}

function openCollapsibleEvent(obj) {
    obj.classList.toggle("active");
    var content = obj.nextElementSibling;
    if (content.style.maxHeight) {
        content.style.maxHeight = null;
    } else {
        setFinalHeight(obj, content);
    }
}

function openMonthEvent(obj) {
    openCollapsibleEvent(obj);
    if (!obj.classList.contains("hasLoaded")) {
        obj.classList.add("hasLoaded");
        var year = parseInt(obj.id.substring(0, 4));
        var month = parseInt(obj.id.substring(4));
        getEventData(year, month+1);
    }
}

function openCurrentDate() {
    if (currentYearElement !== null) {
        currentYearElement.click();
    }
    if (currentMonthElement !== null) {
        currentMonthElement.click();
    }
}

function getDateFormat(date) {
    return weekdayNames[date.getDay()] + ", " + date.getDate() + ". " + monthNames[date.getMonth()] + " um " + date.getHours() +
    (date.getMinutes() != 0 ? (":" + (date.getMinutes() < 10 ? "0" : "") + date.getMinutes()) : "") + " Uhr";
}

function createEventContainer(item, nextEvent=false, today=new Date()) {
    var eventContainer = document.createElement("div");
    eventContainer.classList.add("event");
    if (nextEvent) {
        var headline = document.createElement("div");
        headline.style.fontSize = "1.17em";
        headline.style.fontWeight = "bold";
        headline.innerHTML = "Next up:";
        eventContainer.appendChild(headline);
    }
    if (nextEvent && item == null) {
        eventContainer.classList.add("past");
        var container = document.createElement("div");
        container.innerHTML = "Es gibt noch keinen weiteren Termin...";
        container.classList.add("name");
        eventContainer.appendChild(container);
    }
    else {
        var nameContainer = document.createElement("div");
        nameContainer.innerHTML = item["summary"];
        nameContainer.classList.add("name");
        eventContainer.appendChild(nameContainer);
        var descriptionContainer = document.createElement("div");
        descriptionContainer.innerHTML = item["description"];
        descriptionContainer.classList.add("description");
        eventContainer.appendChild(descriptionContainer);
        var timeContainer = document.createElement("div");
        var startDate = new Date(item["start"]["dateTime"]);
        var endDate = new Date(item["end"]["dateTime"]);
        if (endDate < today) {
            eventContainer.classList.add("past");
        }
        timeContainer.innerHTML = getDateFormat(startDate);
        timeContainer.classList.add("time");
        eventContainer.appendChild(timeContainer);
        if (item["location"] !== undefined) {
            var regex = new RegExp(/[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/gi);
            var locationContainer = document.createElement("div");
            locationContainer.classList.add("location");
            if (item["location"].match(regex)) {
                var linkContainer = document.createElement("a");
                linkContainer.innerHTML = item["location"];
                linkContainer.href = item["location"];
                linkContainer.target = "_blank";
                locationContainer.appendChild(linkContainer);
            }
            else {
                locationContainer.innerHTML = item["location"];
            }
            eventContainer.appendChild(locationContainer);
        }
    }
    return eventContainer;
}

function compareFunction(first, second, today) {
    if (first.hasOwnProperty("start") && second.hasOwnProperty("start") && first.hasOwnProperty("end") && second.hasOwnProperty("end")) {
        firstStart = new Date(first["start"]["dateTime"]);
        firstEnd = new Date(first["end"]["dateTime"]);
        secondStart = new Date(second["start"]["dateTime"]);
        secondEnd = new Date(second["end"]["dateTime"]);
        if ((firstEnd > today && secondEnd > today) || (firstEnd < today && secondEnd < today)) {
            if (firstStart > secondStart) {
                return -1;
            }
            else if (secondStart > firstStart) {
                return 1;
            }
            else {
                return first["summary"].localCompare(second["summary"])
            }
        }
        else if (firstEnd > today) {
            return 1;
        }
        else {
            return -1;
        }
    }
    else if (first.hasOwnProperty("start") && first.hasOwnProperty("end")) {
        return 1;
    }
    else if (second.hasOwnProperty("start") && second.hasOwnProperty("end")) {
        return -1;
    }
    else {
        return 0;
    }
}

function populateMonth(year, month, eventList, open=true) {
    var monthButton = document.getElementById(year + ((month-1) < 10 ? "0" : "") + (month-1));
    var monthContainer = monthButton.nextElementSibling;
    var eventContainerList = [];
    var today = new Date();
    monthContainer.innerHTML = "";
    eventList["items"].sort((a, b) => compareFunction(a, b, today))
    for (var i = 0; i < eventList["items"].length; ++i) {
        var item = eventList["items"][i];
        if (item.hasOwnProperty("summary") && item.hasOwnProperty("description") && item.hasOwnProperty("start") && item.hasOwnProperty("end")) {
            eventContainerList.push(createEventContainer(item, false, today));
        }
    }
    if (eventContainerList.length == 0) {
        var noElementsContainer = document.createElement("div");
        noElementsContainer.classList.add("event");
        if (year > today.getFullYear() || (year == today.getFullYear() && today.getMonth() <= month-1)) {
            noElementsContainer.innerHTML = "In diesem Monat gibt es noch keine Streams...";
        }
        else {
            noElementsContainer.innerHTML = "In diesem Monat gab es keine Streams...";
            noElementsContainer.classList.add("past");
        }
        monthContainer.appendChild(noElementsContainer);
    }
    else {
        for (var i = eventContainerList.length - 1; i >= 0; --i) {
            monthContainer.appendChild(eventContainerList[i]);
        }
    }
    if (open) {
        setTimeout(function() {setFinalHeight(monthButton, monthContainer);}, 50);
    }
    else {
        monthButton.classList.add("hasLoaded");
    }
}

function readyStateChange(e, year, month) {
    if (e.currentTarget.readyState == 4 && e.currentTarget.status == 200) {
        var response = JSON.parse(e.currentTarget.response);
        populateMonth(year, month, response);
    }
}

function appendLaterMonths(e, year, month) {
    if (e.currentTarget.readyState == 4 && e.currentTarget.status == 200) {
        var response = JSON.parse(e.currentTarget.response);
        var subresponses = {};
        var sortedYears = [];
        var today = new Date();
        var nextEvent = null;
        for (var i = 0; i < response["items"].length; ++i) {
            var item = response["items"][i];
            var d = new Date(item["start"]["dateTime"]);
            var endtime = new Date(item["end"]["dateTime"]);
            if (nextEvent === null && today < endtime) {
                nextEvent = item;
            }
            else if (nextEvent !== null && today < endtime && d < new Date(nextEvent["start"]["dateTime"])) {
                nextEvent = item;
            }
            var fullYear = d.getFullYear();
            var fullMonth = d.getMonth();
            if (!sortedYears.includes(fullYear)) {
                sortedYears.push(fullYear);
                subresponses[fullYear] = {"months" : [], "data": {}};
            }
            if (!subresponses[fullYear]["months"].includes(fullMonth)) {
                subresponses[fullYear]["months"].push(fullMonth);
                subresponses[fullYear]["data"][fullMonth] = {"items": []};
            }
            subresponses[fullYear]["data"][fullMonth]["items"].push(item);
        }
        var contentElement = document.getElementById("content");
        var currentDate = new Date();
        for (var i = 0; i < sortedYears.length; ++i) {
            var currentYear = sortedYears[i];
            var yearDiv = document.getElementById("" + currentYear);
            if (yearDiv === null) {
                yearDiv = createYearElements(currentDate, currentYear);
                contentElement.insertBefore(yearDiv, contentElement.childNodes[1]);
            }
            else {
                yearDiv = yearDiv.parentElement;
            }
            var monthContent = yearDiv.childNodes[1];
            for (var j = 0; j < subresponses[currentYear]["months"].length; ++j) {
                var currentMonth = subresponses[currentYear]["months"][j];
                var monthDiv = document.getElementById(("" + currentYear) + (currentMonth < 10 ? "0" + currentMonth : currentMonth));
                if (monthDiv === null) {
                    monthDiv = createMonthElements(currentDate, currentYear, currentMonth);
                    if (monthContent.childNodes.length > 0) {
                        monthContent.insertBefore(monthDiv, monthContent.childNodes[0]);
                    }
                    else {
                        monthContent.appendChild(monthDiv);
                    }
                }
                populateMonth(currentYear, currentMonth+1, subresponses[currentYear]["data"][currentMonth], false);
            }
        }
        var nextEvent = createEventContainer(nextEvent, true, today);
        document.body.insertBefore(nextEvent, document.getElementById("content"));
        setTimeout(openCurrentDate, 200);
    }
}

function getEventData(year, month, untilToday=false) {
    var lastDay = (new Date(year, month, 0)).getDate();
    var timeMin = encodeURIComponent(year + "-" + (month < 10 ? "0" + month : month) + "-01T00:00:00+01:00");
    var timeMax = encodeURIComponent(year + "-" + (month < 10 ? "0" + month : month) + "-" + lastDay + "T23:59:59+01:00");
    var fields = "items(summary%2Cdescription%2Cstart%2Cend,location)"
    var url = "https://www.googleapis.com/calendar/v3/calendars/" + calendar_id + "/events?key=" + api_key + "&timeMin=" + timeMin + (untilToday ? "" : ("&timeMax=" + timeMax)) + "&fields=" + fields + "&singleEvents=true&orderBy=startTime";
    var request = new XMLHttpRequest();
    request.open("GET", url, true);
    if (!untilToday) {
        request.onreadystatechange = function(e) { readyStateChange(e, year, month); };
    }
    else {
        request.onreadystatechange = function(e) { appendLaterMonths(e, year, month); };
    }
    request.send();
}

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        if (scrollButton.style.display != "block") {
            scrollButton.style.display = "block";
            setTimeout(function() {scrollButton.style.opacity = "1.0";}, 100);
        }
    }
    else {
        if (scrollButton.style.display == "block") {
            scrollButton.style.opacity = "0.0";
            setTimeout(function() {scrollButton.style.display = "none";}, 210);
        }
    }
}

function scrollToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

window.onload = load;