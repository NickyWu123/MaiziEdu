
var RegisterApp = angular.module('RegApp', []);

RegisterApp.controller('validateRegCtrl', function($scope,$http) {
    //邮箱是否唯一
    $scope.isEmailNotOnly=false
    //验证码是否正确
    $scope.isCodeNotRight=false
    $scope.register={
         registerEmail:'',
         registerPassword : '',
         registerCode:''
    }
     //验证邮箱
     $scope.validateEmail=function(){
         if(typeof($scope.register.registerEmail)=='undefined') {
             return false
         }
        $scope.postRegister= {
            email: $scope.register.registerEmail
        }
        $http.post("users/validate_email/",$scope.postRegister).success(
            function(data){
               if(data['is_only']=='NotOnly'){
                   $scope.isEmailNotOnly=true
               }else if(data['is_only']=='Only'){
                   $scope.isEmailNotOnly=false
               }
                if(data['error']==true){
                    alert('系统异常无法验证')
                }
            }
        ).error(
            function(error){
                alert('error')
            }
        );
    }


   //验证验证码
    $scope.validateCode=function(){
        if($scope.register.registerCode.length==0){
            $scope.register.registerCode=''
        }
        $scope.postRegister= {
            verification_code: $scope.register.registerCode
        }
        $http.post("users/validate_verification_code/",$scope.postRegister).success(
            function(data){
                if(data['is_verification_right']==true){
                    $scope.isCodeNotRight=false
                }else{
                    $scope.isCodeNotRight=true
                }
                if(data['error']==true){
                    alert('系统异常无法验证')
                }
            }
        ).error(
            function(error){
                alert('error')
            }
        );
    }
    //注册提交
    $scope.submitUserfunction=function(){
        if( $scope.isEmailNotOnly||$scope.isCodeNotRight){
            return
        }
        $http.post("users/register/",$scope.register).success(
            function(data){
                if(data['isSuccess']==true){
                    window.location.href='/users/registerorretrieve_sucess/register/'+ $scope.register.registerEmail
                }else{
                    alert('服务端异常,注册失败')
                }
            }
        )
    }



});
angular.bootstrap(document.getElementById("RegForm"),['RegApp'])
