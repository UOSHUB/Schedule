// Declare main schedule page angular app module
var app = angular.module("schedule", ["LocalStorageModule"]);

// Configure angular app
app.config(function($interpolateProvider, $compileProvider) {
    // Replace angular start symbol from "{{" to "{$"
    $interpolateProvider.startSymbol("{$");
    // Same with end symbol (to prevent conflict with jinja2 symbols)
    $interpolateProvider.endSymbol("$}");
    // Disable info debugging for faster performance
    $compileProvider.debugInfoEnabled(false);
});

// Create unified controller for the whole page logic (for now!)
app.controller("ctrl", function($scope, $http, localStorageService) {
    // Shorten localStorageService to lss as it's going to be used a lot
    var lss = localStorageService;  // TODO: identify data with user id
    // Declare a dynamic variable for http requesting status
    $scope.requesting = false;
    // Declare a static variable that holds week days shortened strings
    $scope.days = ["Sun", "Mon", "Tue", "Wed", "Thu"];
    // A scope method to be called when page first loads
    $scope.initialize = function() {
        // Assign selected semester from storage to scope
        $scope.semester = lss.get("semester");
        // Grab schedule of whatever semester is selected
        $scope.grabSchedule($scope.semester);
        // If semesters are in storage
        if($scope.isStored("semesters"))
            // Assign semesters from storage to scope
            $scope.semesters = lss.get("semesters");
    }
    // A scope method for selectively getting the schedule from server or storage
    $scope.grabSchedule = function(semester) {
        // If schedule of requested semester is in storage
        if($scope.isStored(semester))
            // If it's not the case that courses are in scope and semester hasn't changed
            if(!(angular.isDefined($scope.courses) && $scope.semester === semester))
                // Then extract semester from storage to scope
                extractData(semester, lss.get(semester));
            // Otherwise just notify that schedule is already selected
            else Materialize.toast("Schedule already selected", 2000);
        // If schedule isn't in storage and nothing is being requested
        else if(!$scope.requesting)
            // Get schedule from server
            getSchedule(semester);
        // If schedule isn't in storage but something is being requested, notify about it
        else Materialize.toast("Still processing, Please wait!", 2000);
    };
    // A non-scope method to directly get schedule from server
    function getSchedule(semester) {
        // Flag requesting state with requested semester
        $scope.requesting = semester;
        // Sent an HTTP POST request to server with requested semester to get it
        $http.post("/schedule/get_schedule", semester).then(
        // On request success
        function(response) {
            // If semester isn't known (as it initially would be)
            if(semester == null) {
                // Assign semester from server response
                semester = response.data["semester"];
                // Temporarily store current semester in as scope semesters
                $scope.semesters = toString(semester, {});
                // Temporarily store current semester in as storage semesters
                lss.set("semesters", $scope.semesters);
            }
            // Store preprocessed schedule courses from response in storage
            lss.set(semester, response.data["courses"]);
            // Extract drawing data from schedule courses
            extractData(semester, response.data["courses"]);
            // After processing is done, flag requesting state as false
            $scope.requesting = false;
        // On request failure
        }, function(response) {
            // Notify that server couldn't return schedule
            Materialize.toast("Couldn't get schedule!", 2000);
            // Because request failed, it's not requesting anymore
            $scope.requesting = false;
        });
    }
    // A non-scope method to extract drawing related data from raw schedule data
    function extractData(semester, courses) {
        // Process raw courses data
        var data = getCoursesData(courses);
        // Extract returned data to corresponding scope variables
        $scope.courses = courses;
        $scope.height = data.height;
        $scope.labels = data.labels;
        $scope.fractions = data.fractions;
        $scope.dates = data.dates;
        // Update requested semeter in scope
        $scope.semester = semester;
        // Update requested semeter in storage
        lss.set("semester", semester);
        // Highlight requested (selected) semester in side-bar
        highlight(semester);
    }
    // A scope method for selectively getting available semesters from server or storage
    $scope.grabSemesters = function() {
        // If "Switch Semesters" is not clicked already
        if($("#semesters").is(":hidden")) {
            // If all semesters are already in storage
            if(Object.keys(lss.get("semesters")).length > 1) {
                // If semesters aren't in scope
                if(!(angular.isDefined($scope.semesters)))
                    // Store semesters from storage to scope
                    $scope.semesters = lss.get("semesters");
            // If not all semesters are in storage and nothing is being requested
            } else if(!$scope.requesting)
                // Get semesters from server
                getSemesters();
            // If not all semesters are in storage but something is being requested, notify about it
            else Materialize.toast("Still processing, Please wait!", 2000);
        }
    };
    // A non-scope method to directly get semesters from server
    function getSemesters() {
        // Flag requesting state with "semesters" as it's being requested
        $scope.requesting = "semesters";
        // Show the semesters loading element to indicate loading state
        $("#semesters .loading").show();
        // Sent an HTTP POST request to server to get semesters
        $http.post("/schedule/get_semesters").then(
        // On request success
        function(response) {
            // Flag requesting state as false to indicate success directly
            $scope.requesting = false;
            // Hide the semesters loading element
            $("#semesters .loading").hide();
            // Process semesters and store the result in scope
            $scope.semesters = getSemestersData(response.data);
            // Store preprocessed semesters from response in storage
            lss.set("semesters", $scope.semesters);
            // On request failure
        }, function(response) {
            // Notify that server couldn't return semesters
            Materialize.toast("Couldn't get semesters!", 2000);
            // Because request failed, it's not requesting anymore
            $scope.requesting = false;
        });
    }
    // Returns whether key is stored in storage or not
    $scope.isStored = function(key) {
        // If key index in keys array is 0 or more return true
        return lss.keys().indexOf(key) > -1;
    }
    // Shows class detailed modal
    $scope.showClass = function(id, x) {
        // Store specific course by id as class in scope
        $scope.class = $scope.courses[id];
        // Store courses's id in that same class scope
        $scope.class.id = id;
        // Store day number from class's x point
        $scope.class.day = dayFromX(x);
        // Open the modal to show the data stored in class scope
        $("#class-modal").modal("open");
    };
});
