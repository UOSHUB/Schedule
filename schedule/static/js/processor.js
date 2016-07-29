// Switch on day column number according to day's first letter
var switchDay = {"U": 0, "M": 1, "T": 2, "W": 3, "R": 4, "F": 5, "S": 6};
// Initialize schedule padding and column width
var topShift = 5, leftShift = 5, columnWidth = 19;
// Declare schedule frequently used variables
var maxTime, minTime, hoursCount, rowHeight;
// Main method that returns schedule drawing data from courses
function getData(courses) {
    initialProcessing(courses);
    // Loop through courses
    for(var id in courses) {
        var course = courses[id];
        // Declare points array in course
        course.points = [];
        // Calculate [x, y] coordinates then store them in array
        var y = topShift + rowHeight * (course.time[0] - minTime) / 60;
        for(var i = 0; i < course.days.length; i++)
            course.points.push([leftShift + switchDay[course.days[i]] * columnWidth, y]);
        // Calculate length of course
        course.length = (course.time[1] - course.time[0]) / 60;
    }
    // Return processed data as a dictionary
    return {
        "height": rowHeight,
        "labels": hoursLabels(),
        "fractions": hoursFractions(),
        "dates": dates()
    };
}
// Separates labs and finds min and max
function initialProcessing(courses) {
    // Initial max and min values
    maxTime = 0; minTime = 24 * 60;
    // Loop through courses again!
    for(var id in courses) {
        var course = courses[id];
        findMinMax(course.time);
        // If course has a lab, separate it
        if("lab" in course) {
            // Make a copy of course
            var copy = jQuery.extend(true, {}, course); // TODO: TRY SHALLOW COPYING
            // Loop through lab's properties
            for(var key in copy.lab)
                // Replace them with original course ones
                copy[key] = copy.lab[key];
            if(!("name" in copy.lab)) copy.name += " Lab";
            if(!("short_name" in copy.lab)) copy.short_name += " Lab";
            // delete lab property
            delete copy.lab;
            findMinMax(copy.time);
            // Store resulted course as "id + lab"
            courses[id + "-lab"] = copy;
            // Flag original course lab as true
            course.lab = true;
        }
    }
    // Add 30 minutes margin to schedule
    maxTime += 30; minTime -= 30;
    // Number of hours in schedule
    hoursCount = (maxTime - minTime) / 60;
    // Height of a row in schedule
    rowHeight = (100 - topShift) / hoursCount;
}
// Finds min and max course times in schedule
function findMinMax(time) {
    if(time[0] < minTime) minTime = time[0];
    if(time[1] > maxTime) maxTime = time[1];
}
// Returns whole hours string labels in the schedule
function hoursLabels() {
    var labels = [];
    // Adding (60 - weekBottom() % 60) will round up week bottom hour
    var beginning = (minTime + 60 - minTime % 60) / 60;
    // Subtracting (weekTop() % 60) will round down week top hour
    var end = (maxTime - maxTime % 60) / 60;
    // It's morning if hour < 12, otherwise it's noon
    var hour, period = (beginning < 12 ? "AM" : "PM");
    // Loop through hours between week top and bottom
    for(var i = beginning; i <= end; i++) {
        // When it reaches 12, switch time period
        if(i == 12) {
            period = (period == "PM" ? "AM" : "PM");
            hour = 12;
        // Otherwise, calculate hour e.g. (13 -> 1)
        } else hour = i % 12;
        // Add hour and period to array
        labels.push([hour, period]);
    }
    return labels;
}
// Returns hour by hour representing count array for the schedule
function hoursFractions() {
    var fractions = [];
    // subHour is the fractions before the first whole hour
    var subHour = minTime % 60 / 60;
    // First bit is either a fraction or a whole hour
    var firstBit = (subHour > 0 ? subHour : 1);
    // Add first bit to the array
    fractions.push(firstBit);
    // The remaining hours after subtracting first bit
    var remaining = hoursCount - firstBit;
    // Add the remaining hours cumulatively
    for(var i = 1; i < remaining; i++)
        fractions.push(1 + fractions.slice(-1)[0]);
    return fractions;
}
// Returns an array of weekday dates: ["MM/DD"]
function dates() {
    // Define needed date variables
    var dates = [], date = new Date();
    var month = date.getMonth();
    var year = date.getFullYear();
    // Weekday => start this week, Weekend => start next week (+7)
    var startDay = date.getDate() - date.getDay() + (date.getDay() < 5 ? 0 : 7);
    // Loop five times and return formatted days array
    for (var i = 0; i < 5; i++)
        dates.push(new Date(year, month, startDay + i).toLocaleDateString().slice(0,-5));
    return dates;
}
