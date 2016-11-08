var RetrieveApp = angular.module('RetrieveApp', []);

RetrieveApp.controller('validateRetrieveCtrl',function($scope,$http){
    $scope.retrieveEmail=''
    $scope.noEmail=false
    $scope.submitRetrieveEmail=function(){
        $scope.retrieveInfo={
            email:$scope.retrieveEmail
        }
        $http.post('users/email_retrieve/',$scope.retrieveInfo).success(function(data){
            if(data['isSuccess']==true){
                window.location.href='/users/registerorretrieve_sucess/retrieve/'+  $scope.retrieveEmail
            }else{
                $scope.noEmail=true
            }
        })
    }

})

angular.bootstrap(document.getElementById("RetrievePasswordForm"),['RetrieveApp'])