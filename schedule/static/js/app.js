var app = angular.module("schedule", ["LocalStorageModule"]);

app.config(function($interpolateProvider, $compileProvider) {
    $interpolateProvider.startSymbol("{$");
    $interpolateProvider.endSymbol("$}");
    $compileProvider.debugInfoEnabled(false);
});

app.controller("ctrl", function($scope, $http, localStorageService) {
    var lss = localStorageService;  // TODO: identify data with user id

    $scope.requesting = false;
    $scope.days = ["Sun", "Mon", "Tue", "Wed", "Thu"];

    $scope.initialize = function() {
        $scope.semester = lss.get("semester");
        $scope.grabSchedule($scope.semester);
        if($scope.isStored("semesters"))
            $scope.semesters = lss.get("semesters");
    }

    $scope.grabSchedule = function(semester) {
        if($scope.isStored(semester))
            if(!(angular.isDefined($scope.courses) && $scope.semester === semester))
                extractData(semester, lss.get(semester));
            else Materialize.toast("Schedule already selected", 2000);
        else if(!$scope.requesting)
            getSchedule(semester);
        else Materialize.toast("Still processing, Please wait!", 2000);
    };

    function getSchedule(semester) {
        $scope.requesting = semester;
        $http.post("/schedule/get_schedule", semester).then(function(response) {
            if(semester == null) {
                semester = response.data["semester"];
                $scope.semesters = toString(semester, {});
                lss.set("semesters", $scope.semesters);
            }
            lss.set(semester, response.data["courses"]);
            extractData(semester, response.data["courses"]);
            $scope.requesting = false;
        }, function(response) {
            Materialize.toast("Couldn't get schedule!", 2000);
            $scope.requesting = false;
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
            if(Object.keys(lss.get("semesters")).length > 1) {
                if(!(angular.isDefined($scope.semesters)))
                    $scope.semesters = lss.get("semesters");
            } else if(!$scope.requesting)
                getSemesters();
            else Materialize.toast("Still processing, Please wait!", 2000);
        }
    };

    function getSemesters() {
        $scope.requesting = "semesters";
        $("#semesters .loading").show();
        $http.post("/schedule/get_semesters").then(function(response) {
            $scope.requesting = false;
            $("#semesters .loading").hide();
            $scope.semesters = getSemestersData(response.data);
            lss.set("semesters", $scope.semesters);
        }, function(response) {
            Materialize.toast("Couldn't get semesters!", 2000);
            $scope.requesting = false;
        });
    }

    $scope.isStored = function(key) {
        return lss.keys().indexOf(key) > -1;
    }

    $scope.showClass = function(id, x) {
        $scope.class = $scope.courses[id];
        $scope.class.id = id;
        $scope.class.day = dayFromX(x);
        $("#class-modal").openModal({
            opacity: .2,
            in_duration: 200,
            out_duration: 100,
            starting_top: "35%",
            ending_top: "25%"
        });
    };
});
