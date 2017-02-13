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
        	  var x = JSON.parse(data);
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
        	  var x = JSON.parse(data);
        	  $("<div class='col-sm-6'>"+x.quantity+"</div>"+"<div class='col-sm-6'>"+x.price+"</div>").insertAfter("#v_c");
          }
        });
	});
	
	$('#run_match_form').on('submit', function (e) {
        e.preventDefault();
        var data = $('#run_match_form').serializeArray();
        $.ajax({
          type: 'get',
          url: '/runmatch/',
          data: data,
          success: function (data) {
        	  $("#f_c_cal").empty();
        	  $("#v_c_cal").empty();
        	  $("#tot_c_cal").empty();
        	  try{
        		  var x = JSON.parse(data);
	        	  $.each(x, function(i, item) {
	        		  
	        		if(i == 'Variable Price' || i == 'Price (per unit)' || i == 'Total' || i == 'Fixed Price' || i == 'Quantity'){
	        			if(i== 'Quantity' || i== 'Price (per unit)'){
	        				$("#v_c_cal").append("<div class='col-sm-6'>"+ i +" : </div><div class='col-sm-6'>"+ item +"</div><br/>");
	        				
	        			}
	        			if(i=='Total'){
	        				$("#tot_c_cal").append("<div class='col-sm-2'>"+ i +" : </div><div class='col-sm-2'> Fixed Price  </div><div class='col-sm-1'>+</div><div class='col-sm-3'>Variable Price</div><br/>");
	        				$("#tot_c_cal").append("<div class='col-sm-2'>"+ i +" : </div><div class='col-sm-2'>"+ x["Fixed Price"] +"</div><div class='col-sm-1'>+</div><div class='col-sm-3'>"+ x["Variable Price"] +"</div><br/>");
	        				$("#tot_c_cal").append("<div class='col-sm-12'> ------------------------------------------------------------------------------------------ </div><br/>");
	        				$("#tot_c_cal").append("<div class='col-sm-2'>"+ i +" : </div><div class='col-sm-2'>"+ item +"</div><br/>");
	        			}
	        			
	        		}else{
	        			$("#f_c_cal").append("<div class='col-sm-6'>"+ i +" : </div><div class='col-sm-6'>"+ item +"</div><br/>");
	    				
	        		}          		
	        		
	        	  });
	        	$("#v_c_cal").append("<div class='col-sm-12'> ------------------------------------------------------------------------------------------ </div><br/>");
				$("#v_c_cal").append("<div class='col-sm-6'>Variable Price : </div><div class='col-sm-6'>"+ x["Variable Price"] +"</div><br/>");
	      		$("#f_c_cal").append("<div class='col-sm-12'> ------------------------------------------------------------------------------------------ </div><br/>");
	  			$("#f_c_cal").append("<div class='col-sm-6'> Fixed Price: </div><div class='col-sm-6'>"+ x["Fixed Price"] +"</div><br/>");
        	  }
		catch(e){
			$("#f_c_cal").append("<div class='col-sm-12'> No data Available </div><br/>");
			$("#v_c_cal").append("<div class='col-sm-12'>  No data Available  </div><br/>");
			$("#tot_c_cal").append("<div class='col-sm-12'>  No data Available  </div><br/>");
		      }
          }
        });
        $('#cost_runmatch').modal({
	        show: true
	    });
	});
	
}]);
