var app = angular.module("schedule", ["LocalStorageModule"]);

app.config(["$interpolateProvider", function($interpolateProvider) {
    $interpolateProvider.startSymbol("{$");
    $interpolateProvider.endSymbol("$}");
}]);

app.controller("ctrl", function($scope, $http, localStorageService) {
    var lss = localStorageService;
    $scope.days = ["Sun", "Mon", "Tue", "Wed", "Thu"];
    $scope.colors = ["red", "teal", "green", "orange",
                     "purple", "light-blue", "teal",
                     "yellow", "deep-orange", "blue"];

    $scope.updateColor = function(index) {
        $scope.color = $scope.colors[index];
    };

    $scope.initialize = function() {
        $scope.semester = lss.get("semester");
        $scope.grabSchedule($scope.semester);
    }

    $scope.grabSchedule = function(semester) {
        if(lss.keys().indexOf(semester) > -1) {
            Materialize.toast("Schedule already selected", 2000);
            if(!(angular.isDefined($scope.courses) && $scope.semester === lss.get("semester"))) {
                extractData(lss.get(semester));
                lss.set("semester", semester);
            }
        } else getSchedule(semester);
    };

    function getSchedule(semester) {
        $http.post("/schedule/getter", semester).then(function(response) {
            $scope.semester = response.data[0];
            var courses = response.data[1];
            lss.set("semester", $scope.semester);
            lss.set($scope.semester, courses);
            extractData(courses);
        }, function(response) {
            Materialize.toast("Couldn't get schedule!", 2000);
        });
    }

    function extractData(courses) {
        var data = getData(courses);
        $scope.courses = courses;
        $scope.height = data.height;
        $scope.labels = data.labels;
        $scope.fractions = data.fractions;
        $scope.dates = data.dates;
    }
});
