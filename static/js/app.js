var app = angular.module("UOSHUB", ["ngMaterial", "ngRoute", "ngMessages", "LocalStorageModule"]);
app.config(function($interpolateProvider, $compileProvider, $routeProvider, $controllerProvider) { //$locationProvider) {
    // Replace angular start symbol from "{{" to "{$"
    $interpolateProvider.startSymbol("{$");
    // Same with end symbol (to prevent conflict with jinja2 symbols)
    $interpolateProvider.endSymbol("$}");
    // Disable info debugging for faster performance
    $compileProvider.debugInfoEnabled(false);

    $routeProvider.when("/schedule", {
        templateUrl: function() {
            jQuery.getScript(js.schedule);
            return "/schedule";
        },
        controller: "scheduleHandler"
    }).otherwise({ redirectTo: '/' });
    //$locationProvider.html5Mode(true);
    app.controller = function(name, constructor) {
        $controllerProvider.register(name, constructor);
        return(this);
    };
});
app.factory("accountVariables", function($http, $timeout) {
    var student = { status: "loggedOut", remember: false };
    return {
        student: student,
        login: function(form) {
            if(form.$invalid) {
                form.sid.$setTouched();
                form.pin.$setTouched();
            } else {
                $timeout(function() {
                    student.status = "waiting";
                }, 400);
                waitAnimation();
                $http.post("/login", student).then(
                    function(response) {
                        jQuery.extend(student, response.data);
                        student.status = "loggedIn";
                        doneAnimation();
                    },function(response) {
                });
            }
        },
        logout: function() {
            $timeout(function() {
                student.status = "switching";
            }, 400);
            waitAnimation();
            var start = new Date().getTime();
            $http.post("/logout").then(
                function(response) {
                    $timeout(function() {
                        student.status = "loggedOut";
                        doneAnimation();
                    }, 520 - new Date().getTime() + start);
                },function(response) {
            });
        }
    };
}).controller("accountHandler", function($scope, accountVariables) {
    jQuery.extend($scope, accountVariables);
});
app.controller("accountButton", function($scope, $mdPanel) {
    var panelConfigs = {
        templateUrl: "account-panel.html",
        panelClass: "account-panel md-whiteframe-3dp",
        clickOutsideToClose: true,
        animation: $mdPanel.newPanelAnimation()
            .openFrom("#loginButton")
            .withAnimation($mdPanel.animation.SCALE),
        position: $mdPanel.newPanelPosition()
            .relativeTo("#loginButton")
            .addPanelPosition($mdPanel.xPosition.ALIGN_END,
                              $mdPanel.yPosition.ALIGN_TOPS)
    };
    $scope.showPanel = function() {
        $mdPanel.open(panelConfigs);
    };
});
