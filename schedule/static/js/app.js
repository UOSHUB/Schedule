var app = angular.module("schedule", []);

app.config(["$interpolateProvider", function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}]);

app.controller("ctrl", function($scope, $http) {
    $scope.colors = ['red', 'teal', 'green', 'orange',
                     'purple', 'light-blue', 'teal',
                     'yellow', 'deep-orange', 'blue'];
    
    $scope.updateColor = function(index) {
        $scope.color = $scope.colors[index];
    };
    
    $scope.days = ["Sun", "Mon", "Tue", "Wed", "Thu"];
    
    $scope.getSchedule = function(semester) {
        $http.post("/schedule/getter", semester).then(function(response) {
            var data = response.data;
            $scope.height = data["height"];
            $scope.labels = data["labels"];
            $scope.fractions = data["fractions"];
            $scope.dates = data["dates"];
            $scope.bottom = data["bottom"];
            $scope.courses = processData(data["courses"]);
        }, function(response) {
            Materialize.toast("Couldn't get schedule!", 2000);
        });
    };
    
    function processData(courses) {
        for(var id in courses) {
            calcPoints(courses[id]);
            if("lab" in courses[id]) {
                var course = jQuery.extend(true, {}, courses[id]);
                for(var key in course.lab)
                    course[key] = course.lab[key];
                delete course.lab;
                calcPoints(course);
                courses[id + "-lab"] = course;
                courses[id].lab = true;
            }
        }
        return courses;
    }
    
    // Calculate [x, y] coordinates then store them
    function calcPoints(course) {
        course["points"] = [];
        var y = 5 + $scope.height * (course.time[0] - $scope.bottom) / 60;
        for(var i = 0; i < course.days.length; i++)
            course["points"].push([5 + switchDay[course.days[i]] * 19, y]);
        course["length"] = (course.time[1] - course.time[0]) / 60;
    }
    // Switch on day column number according to day's first letter
    var switchDay = {"U": 0, "M": 1, "T": 2, "W": 3, "R": 4, "F": 5, "S": 6};
});