var app = angular.module("supplieriqApp");

app.controller("VendorController",['$scope', '$http','$compile','$rootScope','GetVendorList', 
    function($scope, $http,$compile, $rootScope, GetVendorList) {
	$scope.vendor_list = [];
	$scope.current_tab = '';
	$scope.load_section = function(value, app) {
		$scope.current_tab =  value;
		$scope.vendor_list = GetVendorList.list();
//		var ele = angular.element($("#siq_main_body")).scope();
		$scope.vendor_list.$promise.then(function() {			
			$rootScope.vendor_list = $scope.vendor_list.serializer;
		});
//		ele.append($scope.current_tab);
//		$compile(ele.contents())($scope);
    }
	$scope.get_vendor_list = function(){
		$scope.vendor_list = $rootScope.vendor_list;
	}
}]);
