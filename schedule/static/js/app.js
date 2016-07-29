var app = angular.module("schedule", []);

app.config(["$interpolateProvider", function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}]);

app.controller("ctrl", function($scope, $http) {
    $scope.days = ["Sun", "Mon", "Tue", "Wed", "Thu"];
    $scope.colors = ['red', 'teal', 'green', 'orange',
                     'purple', 'light-blue', 'teal',
                     'yellow', 'deep-orange', 'blue'];

    $scope.updateColor = function(index) {
        $scope.color = $scope.colors[index];
    };

    $scope.getSchedule = function(semester) {
        $http.post("/schedule/getter", semester).then(function(response) {
            $scope.courses = response.data;
            var data = getData($scope.courses);
            $scope.height = data["height"];
            $scope.labels = data["labels"];
            $scope.fractions = data["fractions"];
            $scope.dates = data["dates"];
        }, function(response) {
            Materialize.toast("Couldn't get schedule!", 2000);
        });
    };
});
