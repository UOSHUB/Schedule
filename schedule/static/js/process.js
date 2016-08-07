// Switch on season db value according to it's string name
var seasons = {"FALL": 10, "Fall": 10, "Spring": 20, "Summer": 30};
// Switch on day column number according to day's first letter
var switchDay = {'U': 0, 'M': 1, 'T': 2, 'W': 3, 'R': 4, 'F': 5, 'S': 6};
// Initialize schedule padding and column width
var topShift = 5, leftShift = 5, columnWidth = 19;
// Declare schedule frequently used variables
var maxTime, minTime, hoursCount, rowHeight;
// Declare colors to be included in courses
var colors = ["red", "teal", "green", "orange",
              "purple", "light-blue", "brown",
              "yellow", "deep-orange", "blue"];
// Returns semesters as [digit value, beautified string]
function getSemestersData(semesters) {
    // Loop through semesters from array
    for(var data = {}, i = 0; i < semesters.length; i++) {
        // Add spaces around the '-' to beautify string
        var string = semesters[i].replace('-', " - ");
        // Split string on first two spaces
        var array = string.split(' ', 2);
        // Add to output the digit value and the string
        data[array[1] + seasons[array[0]]] = string;
    }
    return data;
}
// Main method that returns schedule drawing data from courses
function getCoursesData(courses) {
    initialProcessing(courses);
    // Loop through courses
    for(var id in courses) {
        var course = courses[id];
        // Declare points array in course
        course.points = [];
        // Calculate [x, y] coordinates then store them in array
        var y = topShift + rowHeight * (course.minutes[0] - minTime) / 60;
        for(var i = 0; i < course.days.length; i++)
            course.points.push([leftShift + switchDay[course.days[i]] * columnWidth, y]);
        // Calculate length of course
        course.length = (course.minutes[1] - course.minutes[0]) / 60;
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
    Object.keys(courses).forEach(function(id, index) {
        var course = courses[id];
        colorAndTime(course, index);
        // If course has a lab, separate it
        if("lab" in course) {
            // Make a copy of course
            var copy = jQuery.extend(true, {}, course); // TODO: TRY SHALLOW COPYING
            // Loop through lab's properties
            for(var key in copy.lab)
                // Replace them with original course ones
                copy[key] = copy.lab[key];
            // If lab doesn't have a name, then add " Lab" to course name
            if(!("name" in copy.lab) || copy.lab.name.indexOf("Lab") < 0)
                copy.name += " Lab";
            // delete lab property
            delete copy.lab;
            colorAndTime(copy, index);
            // Store resulted course as "id + lab"
            courses[id + "-lab"] = copy;
            // Flag original course lab as true
            course.lab = true;
        }
    });
    // Add 30 minutes margin to schedule
    maxTime += 30; minTime -= 30;
    // Number of hours in schedule
    hoursCount = (maxTime - minTime) / 60;
    // Height of a row in schedule
    rowHeight = (100 - topShift) / hoursCount;
}
// Sets course color and finds min and max times in schedule
function colorAndTime(course, index) {
    // Calculate minutes from start / end time
    for (var minutes = [], i = 0; i < 2; i++)
        minutes.push(toMinutes(course.time[i].replace(':', ' ').split(' ')));
    // Compare course time to other courses
    if(minutes[0] < minTime) minTime = minutes[0];
    if(minutes[1] > maxTime) maxTime = minutes[1];
    // Store course color and calculated minutes
    course.color = colors[index];
    course.minutes = minutes;
}
// Converts time from string to minutes
function toMinutes(time) {
    // Calculate minutes from time and if it's "PM" then add 12 * 60
    return Number(time[0]) * 60 + Number(time[1]) + (time[2] == "PM" && time[0] != "12" ? 720 : 0);
}
// Returns whole hours string labels in the schedule
function hoursLabels() {
    // Adding (60 - weekBottom() % 60) will round up week bottom hour
    var beginning = (minTime + 60 - minTime % 60) / 60;
    // Subtracting (weekTop() % 60) will round down week top hour
    var end = (maxTime - maxTime % 60) / 60;
    // It's morning if hour < 12, otherwise it's noon
    var hour, period = (beginning < 12 ? "AM" : "PM");
    // Loop through hours between week top and bottom
    for(var labels = [], i = beginning; i <= end; i++) {
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
    // If there's an extra half an hour add -1
    if(remaining % 1 > 0.5) fractions.push(-1);
    return fractions;
}
// Returns an array of weekday dates: ["MM/DD"]
function dates() {
    // Define needed date variables
    var date = new Date();
    var month = date.getMonth();
    var year = date.getFullYear();
    // Weekday => start this week, Weekend => start next week (+7)
    var startDay = date.getDate() - date.getDay() + (date.getDay() < 5 ? 0 : 7);
    // Loop five times and return formatted days array
    for (var dates = [], i = 0; i < 5; i++)
        dates.push(new Date(year, month, startDay + i).toLocaleDateString().slice(0,-5));
    return dates;
}
// Returns beautified string of semester id
function toString(semester, array) {
    var year = semester.slice(2, 4);
    array[semester] = {"10": "Fall", "20": "Spring", "30": "Summer"}[semester.slice(4)]
                      + " 20" + year + " - 20" + (Number(year) + 1);
    return array;
}
