angular.module("main", ["ngMaterial", "ngMessages"])
    .config(function($interpolateProvider, $compileProvider) {
        // Replace angular start symbol from "{{" to "{$"
        $interpolateProvider.startSymbol("{$");
        // Same with end symbol (to prevent conflict with jinja2 symbols)
        $interpolateProvider.endSymbol("$}");
        // Disable info debugging for faster performance
        $compileProvider.debugInfoEnabled(false);
    }).controller("accountButton", function($mdPanel) {
        this.showDialog = function() {
            $mdPanel.open({
                templateUrl: "loginForm.html",
                panelClass: "account-dialog md-whiteframe-3dp",
                clickOutsideToClose: true,
                animation: $mdPanel.newPanelAnimation()
                    .openFrom("#loginButton")
                    .withAnimation($mdPanel.animation.SCALE),
                position: $mdPanel.newPanelPosition()
                    .relativeTo("#loginButton")
                    .addPanelPosition($mdPanel.xPosition.ALIGN_END,
                                      $mdPanel.yPosition.ALIGN_TOPS)
            });
        }
    }).controller("loginForm", function($scope) {
        $scope.login = function(form) {
            if(form.$invalid) {
                form.sid.$setTouched();
                form.pin.$setTouched();
            }
        };
    });
