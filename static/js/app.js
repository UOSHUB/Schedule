angular.module("main", ["ngMaterial", "ngMessages"])
    .config(function($interpolateProvider, $compileProvider) {
        // Replace angular start symbol from "{{" to "{$"
        $interpolateProvider.startSymbol("{$");
        // Same with end symbol (to prevent conflict with jinja2 symbols)
        $interpolateProvider.endSymbol("$}");
        // Disable info debugging for faster performance
        $compileProvider.debugInfoEnabled(false);
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
    }).run(function($rootScope, $http) {
        $rootScope.login = function(form, student) {
            if(form.$invalid) {
                form.sid.$setTouched();
                form.pin.$setTouched();
            } else {
                $rootScope.status = "waiting";
                $http.post("/login", student).then(
                    function(response) {
                        $rootScope.status = "loggedIn";
                        $rootScope.student = response.data;
                        $rootScope.student.sid = student.sid;
                    },function(response) {
                });
            }
        };
        $rootScope.logout = function() {
            $rootScope.status = "waiting";
            $http.post("/logout").then(
                function(response) {
                    $rootScope.status = "loggedOut";
                },function(response) {
            });
        };
    });
