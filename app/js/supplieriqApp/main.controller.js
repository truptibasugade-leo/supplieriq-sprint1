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
	$('.price').click(function(){
		var data = $(this).data('id');
		var item_id = $(this).data('item-id');
		var vendor_id = $(this).data('vendor-id');
		$("#hidden_field").attr('data-vendor-id',vendor_id);
		$("#hidden_field").attr('data-item-id',item_id);
		$("#f_c").nextAll('div').remove();
		$("#v_c").nextAll('div').remove();
		
		if (data[0].fixed_cost){
			$.each(data[0].fixed_cost[0], function(i, item) {
//			    console.log(i + ":" +item);
			    $("<div class='col-sm-6'>"+i+"</div>"+"<div class='col-sm-6'>"+item+"</div>").insertAfter("#f_c");
			});
		}else{
			
		}
		if (data[1].variable_cost){
			$.each(data[1].variable_cost[0], function(i,item) {
				$.each(item, function(x, y) {
//				    console.log(x + ":" +y);
				    $("<div class='col-sm-6'>"+y+"</div>").insertAfter("#v_c");
				});
			});
		}else{
			
		}
		$('#myModal').modal({
	        show: true
	    });
	});
	
	$('#f_price_form').on('submit', function (e) {
        e.preventDefault();
        var i_id = $("#hidden_field").data('item-id');
		var v_id = $("#hidden_field").data('vendor-id');
        var data = $('#f_price_form').serializeArray();
        data.push({ name:'vendor_id', value:v_id });
        data.push({ name:'item_id',value:i_id });
        $.ajax({
          type: 'post',
          url: '/cost/',
          data: data,
          success: function (data) {
        	  var x = JSON.Parse(data);
        	  $("<div class='col-sm-6'>"+x.price_type+"</div>"+"<div class='col-sm-6'>"+x.price+"</div>").insertAfter("#f_c");
          }
        });
	});
	
	$('#v_price_form').on('submit', function (e) {
        e.preventDefault();
        var i_id = $("#hidden_field").data('item-id');
		var v_id = $("#hidden_field").data('vendor-id');
        var data = $('#v_price_form').serializeArray();
        data.push({ name:'vendor_id', value:v_id });
        data.push({ name:'item_id',value:i_id });
        $.ajax({
          type: 'post',
          url: '/cost/',
          data: data,
          success: function (data) {
        	  var x = JSON.Parse(data);
        	  $("<div class='col-sm-6'>"+x.quantity+"</div>"+"<div class='col-sm-6'>"+x.price+"</div>").insertAfter("#v_c");
          }
        });
	});
	
}]);
