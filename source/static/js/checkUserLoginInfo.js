var LoginApp = angular.module('LoginApp', []);
LoginApp.controller('validateLoginCtrl',function($scope,$http){
    $scope.login={
        email:'',
        password:''
    }
    $scope.isUserNotRight=false
    $scope.isUserNotActive=false
    $scope.loginUser=function(){
        $http.post('users/login/',$scope.login).success(
            function(data){
                if(data['isSuccess']==true){
                    window.location.href='/'
                }else{
                    if(data['isNotActive']==false){
                        $scope.isUserNotRight=true
                        $scope.isUserNotActive=false
                    }else{
                        $scope.isUserNotActive=true
                        $scope.isUserNotRight=false
                    }

                }
            }
        )
    }
})