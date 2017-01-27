var app = angular.module("supplieriqApp");

app.controller("VendorController",['$scope', '$http','$compile','$rootScope',
    function($scope, $http,$compile, $rootScope) {
	$(".vendor_name").click(function() {
		var vendor_id = $(this).parent().find("td:first").text();	
		window.location.replace('/vendors/?id='+vendor_id);	
		
	});
	$(".item_name").click(function() {
		var item_id = $(this).parent().find("td:first").text();	
		window.location.replace('/items/?id='+item_id);	
		
	});
}]);
