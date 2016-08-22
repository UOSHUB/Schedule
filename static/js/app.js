angular.module("main", ["ngMaterial", "ngMessages"])
    .config(function($interpolateProvider, $compileProvider) {
        // Replace angular start symbol from "{{" to "{$"
        $interpolateProvider.startSymbol("{$");
        // Same with end symbol (to prevent conflict with jinja2 symbols)
        $interpolateProvider.endSymbol("$}");
        // Disable info debugging for faster performance
        $compileProvider.debugInfoEnabled(false);
    }).factory("accountMethods", function($http, $timeout) {
        console.log("hi");
        var student = {status: "loggedOut"};
        var login = function(form, sid) {
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
                        student.sid = sid;
                        doneAnimation();
                    },function(response) {
                });
            }
        };
        var logout = function() {
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
        };
        return {
            student: student,
            login: login,
            logout: logout
        };
    }).controller("accountHandler", function($scope, accountMethods) {
        jQuery.extend($scope, accountMethods);
    }).controller("accountButton", function($scope, $mdPanel) {
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
