var app = angular.module("schedule", ["LocalStorageModule"]);

app.config(["$interpolateProvider", function($interpolateProvider) {
    $interpolateProvider.startSymbol("{$");
    $interpolateProvider.endSymbol("$}");
}]);

app.controller("ctrl", function($scope, $http, localStorageService) {
    var lss = localStorageService;  // TODO: identify data with user id
    var requesting = false;

    $scope.days = ["Sun", "Mon", "Tue", "Wed", "Thu"];

    $scope.initialize = function() {
        $scope.semester = lss.get("semester");
        $scope.grabSchedule($scope.semester);
    }

    $scope.grabSchedule = function(semester) {
        if(lss.keys().indexOf(semester) > -1)
            if(!(angular.isDefined($scope.courses) && $scope.semester === semester))
                extractData(semester, lss.get(semester));
            else Materialize.toast("Schedule already selected", 2000);
        else if(!requesting)
            getSchedule(semester);
        else Materialize.toast("Still processing, Please wait!", 2000);
    };

    function getSchedule(semester) {
        requesting = true;
        $http.post("/schedule/get_schedule", semester).then(function(response) {
            lss.set(response.data[0], response.data[1]);
            extractData(response.data[0], response.data[1]);
            requesting = false;
        }, function(response) {
            Materialize.toast("Couldn't get schedule!", 2000);
            requesting = false;
        });
    }

    function extractData(semester, courses) {
        var data = getCoursesData(courses);
        $scope.courses = courses;
        $scope.height = data.height;
        $scope.labels = data.labels;
        $scope.fractions = data.fractions;
        $scope.dates = data.dates;
        $scope.semester = semester;
        lss.set("semester", semester);
        highlight(semester);
    }

    $scope.grabSemesters = function() {
        if($("#semesters").is(":hidden")) {
            if(lss.keys().indexOf("semesters") > -1) {
                if(!(angular.isDefined($scope.semesters)))
                    $scope.semesters = lss.get("semesters");
            } else if(!requesting)
                getSemesters();
            else Materialize.toast("Still processing, Please wait!", 2000);
        }
    };

    function getSemesters() {
        requesting = true;
        $("#semesters .loading").show();
        $http.post("/schedule/get_semesters").then(function(response) {
            requesting = false;
            $("#semesters .loading").hide();
            $scope.semesters = getSemestersData(response.data);
            lss.set("semesters", $scope.semesters);
        }, function(response) {
            Materialize.toast("Couldn't get semesters!", 2000);
            requesting = false;
        });
    }
});
