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
            $scope.courses = separateLabs(data["courses"]);
            $scope.height = data["height"];
            $scope.labels = data["labels"];
            $scope.fractions = data["fractions"];
            $scope.dates = data["dates"];
        }, function(response) {
            Materialize.toast("Couldn't get schedule!", 2000);
        });
    };
});

function separateLabs(courses) {
    for(var key in courses)
        if(courses[key].lab !== null) {
            courses[key + "-lab"] = courses[key].lab;
            courses[key].lab = true;
        }
    return courses;
}