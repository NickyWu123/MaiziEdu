var UpdateApp = angular.module('UpdateApp', []);

UpdateApp.controller('validateUpdateCtrl', function($scope,$http,$location) {
    $scope.password=''
    $scope.passwordConfirm=''

    $scope.submitUpdateInfo=function(){
        $scope.updateInfo={
            password:$scope.passwordConfirm
        }
        $http.post('http://'+$location.host()+':'+$location.port()+'/users/update_user_password/',$scope.updateInfo).success(function(data){
             if(data['isSuccess']==true){
                    window.location.href='/'
             }else{
                 alert('服务端异常修改失败')
             }
        })
    }

})
