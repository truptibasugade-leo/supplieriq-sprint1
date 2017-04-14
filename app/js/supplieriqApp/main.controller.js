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
	$(".po_item").click(function() {
		
		var po_id = $(this).data('po-id');	
		window.location.replace('/purchase_order/?id='+po_id);	
		
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
	
	$(".send_quote").on('click',function(e){
		var vendor_id = $(this).data('vendor-id');
		var item_id = $(this).data('item-id');
		var action = "open modal";
		$.ajax({
          type: 'get',
          url: '/quote/',
          data: {"vendorid":vendor_id, "itemid" :item_id, "action" :action},
          success: function (data) {
        	  $("#link").val(data.serializer);
        	  $(".copy").attr('data-clipboard-text',data.serializer)
        	  $(".send_mail").attr('data-vendor-id',vendor_id)
        	  $(".send_mail").attr('data-item-id',item_id)
        	  $('#send_quote_popup').modal({
	      	        show: true
	      	    });
          }
		});
	});
	$(".send_mail").on('click',function(e){
		var vendor_id = $(this).data('vendor-id');
		var item_id = $(this).data('item-id');
		var action = "send mail";
		$.ajax({
          type: 'get',
          url: '/quote/',
          data: {"vendorid":vendor_id, "itemid" :item_id, "action" :action},
          success: function (data) {
        	  $('#send_quote_popup').modal('toggle');
        	  $("#result").html('<div class="alert alert-success"><button type="button" class="close">&nbsp;×</button>'+data.serializer+'</div>');
              window.setTimeout(function() {
                    $(".alert").fadeTo(500, 0).slideUp(500, function(){
                        $(this).remove(); 
                    });
                }, 5000);
              $('.alert .close').on("click", function(e){
                    $(this).parent().fadeTo(500, 0).slideUp(500);
                 });
          }
		});
	});
	$('.price_col').on('click', function (e) {
        e.preventDefault();
        var iv = $(this).data('itemvendor-id');        
        var q = $(this).data('quantity');
        $.ajax({
          type: 'get',
          url: '/runmatch/',
          data: {'itemvendor':iv,'quantity':q},
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
	
	$('.edit_fix_cost').on('click', function (e) {
        e.preventDefault();
        var id = $(this).data('id');
        var cost = $(this).data('cost');
		var cost_type = $(this).data('cost-type');
		$('#edit_fixed_cost input[name="price_type"]').val(cost_type);
		$('#edit_fixed_cost input[name="price"]').val(cost);
		
		$("#edit_fixed_cost").attr('data-fixedcost-id',id);
		
        $('#edit_fixed_cost').modal({
	        show: true
	    });
	});
	$('.edit_var_cost').on('click', function (e) {
        e.preventDefault();
        var id = $(this).data('id');
        var qty = $(this).data('quantity');
		var cost = $(this).data('cost');
		$('#edit_variable_cost input[name="quantity"]').val(qty);
		$('#edit_variable_cost input[name="price"]').val(cost);
		
		$("#edit_variable_cost").attr('data-variablecost-id',id);
        
		$('#edit_variable_cost').modal({
	        show: true
	    });
	});
	
	$('#update_f_c').on('submit', function (e) {
        e.preventDefault();
        var id = $("#edit_fixed_cost").data('fixedcost-id');
        var data = $(this).serializeArray();
        data.push({ name:'fixedcost_id', value:id });
        $.ajax({
        	
          type: 'post',
          url: '/cost/',
          data: data,
          success: function (data) {
        	  x=JSON.parse(data);
    		  $("input[name='price_type']").next('span').html("");
    		  $("input[name='price']").next('span').html("");
    		  if(x.status == "error"){
    				if(x.price){
    					$("input[name='price']").next('span').html(x.price);
    				}
    				if(x.non_field_errors){
    					$("input[name='price_type']").next('span').html(x.non_field_errors)
    				}
    			}
    		  else{   
		        	  $('#edit_fixed_cost').modal('toggle');
		              
		        	  $("#result").html('<div class="alert alert-success"><button type="button" class="close">&nbsp;×</button>Data Updated Successfully..</div>');
		        	  window.setTimeout(function() {
		                    $(".alert").fadeTo(500, 0).slideUp(500, function(){
		                        $(this).remove(); 
		                    });
		                }, 5000);
		              $('.alert .close').on("click", function(e){
		                    $(this).parent().fadeTo(500, 0).slideUp(500);
		                 });
		              location.reload(); 
    		  }
        	}
        });
	});
	
	$('#update_v_c').on('submit', function (e) {
		e.preventDefault();
		var id = $("#edit_variable_cost").data('variablecost-id');
        var data = $(this).serializeArray();
        data.push({ name:'variablecost_id', value:id });
        $.ajax({
        	
          type: 'post',
          url: '/cost/',
          data: data,
          success: function (data) {
        	  x=JSON.parse(data);
    		  $("input[name='quantity']").next('span').html("");
    		  $("input[name='price']").next('span').html("");
    		  if(x.status == "error"){
    				if(x.price){
    					$("input[name='price']").next('span').html(x.price);
    				}
    				if(x.non_field_errors){
    					$("input[name='quantity']").next('span').html(x.non_field_errors)
    				}
    			}
    		  else{   
		        	  $('#edit_variable_cost').modal('toggle');
		        	  
		        	  $("#result").html('<div class="alert alert-success"><button type="button" class="close">&nbsp;×</button>Data Updated Successfully..</div>');
		              window.setTimeout(function() {
		                    $(".alert").fadeTo(500, 0).slideUp(500, function(){
		                        $(this).remove(); 
		                    });
		                }, 5000);
		              $('.alert .close').on("click", function(e){
		                    $(this).parent().fadeTo(500, 0).slideUp(500);
		                 });
		              location.reload();
    		  }
        	 }
        });
	});
	$('#add_f_c').on('click', function (e) {
		e.preventDefault();
		$('#add_fixed_cost').modal({
	        show: true
	    });
	});
	$('#add_v_c').on('click', function (e) {
		e.preventDefault();        
		$('#add_variable_cost').modal({
	        show: true
	    });
	});
	$('#add_f_price_form').on('submit', function (e) {
        e.preventDefault();
        var i_id = $("#hidden_field_fixed").data('item-id');
		var v_id = $("#hidden_field_fixed").data('vendor-id');
        var data = $('#add_f_price_form').serializeArray();
        data.push({ name:'vendor_id', value:v_id });
        data.push({ name:'item_id',value:i_id });
        $.ajax({
          type: 'post',
          url: '/cost/',
          data: data,
          success: function (data) {     
        	  
        		  x=JSON.parse(data);
        		  $("input[name='price_type']").next('span').html("");
        		  $("input[name='price']").next('span').html("");
        		  if(x.status == "error"){
        				if(x.price){
        					$("input[name='price']").next('span').html(x.price);
        				}
        				if(x.non_field_errors){
        					$("input[name='price_type']").next('span').html(x.non_field_errors)
        				}
        			}
        		  else{        			  
        			  $('#add_fixed_cost').modal('toggle');
                	  $("#result").html('<div class="alert alert-success"><button type="button" class="close">&nbsp;×</button>Data Added Successfully..</div>');
                      window.setTimeout(function() {
                            $(".alert").fadeTo(500, 0).slideUp(500, function(){
                                $(this).remove(); 
                            });
                        }, 5000);
                      $('.alert .close').on("click", function(e){
                            $(this).parent().fadeTo(500, 0).slideUp(500);
                         });
                      location.reload();
        		  }      	   
          }
        });
	});
	$('#add_v_price_form').on('submit', function (e) {
        e.preventDefault();
        var i_id = $("#hidden_field_variable").data('item-id');
		var v_id = $("#hidden_field_variable").data('vendor-id');
        var data = $('#add_v_price_form').serializeArray();
        data.push({ name:'vendor_id', value:v_id });
        data.push({ name:'item_id',value:i_id });
        $.ajax({
          type: 'post',
          url: '/cost/',
          data: data,
          success: function (data) {
        	  
        		  x=JSON.parse(data);
        		  $("input[name='quantity']").next('span').html("");
        		  $("input[name='price']").next('span').html("");
        		  if(x.status == "error"){
        				if(x.price){
        					$("input[name='price']").next('span').html(x.price);
        				}
        				if(x.non_field_errors){
        					$("input[name='quantity']").next('span').html(x.non_field_errors)
        				}
        			}
        		  else{
        			  $('#add_variable_cost').modal('toggle');
    	        	  $("#result").html('<div class="alert alert-success"><button type="button" class="close">&nbsp;×</button>Data Added Successfully..</div>');
    	              window.setTimeout(function() {
    	                    $(".alert").fadeTo(500, 0).slideUp(500, function(){
    	                        $(this).remove(); 
    	                    });
    	                }, 5000);
    	              $('.alert .close').on("click", function(e){
    	                    $(this).parent().fadeTo(500, 0).slideUp(500);
    	                 });
    	              location.reload();  
        		  }	        	  
	          }          
        });
	});
	$('.delete_fix_cost').on('click', function (e) {
		e.preventDefault();
		var data = $(this).data('id');
		$("#hidden_id_fix").attr('data-fixedcost-id',data);
		$("#hidden_id_fix").val(data);
		$('#delete_fixedcost').modal({
	        show: true
	    });
	});
	$('.delete_var_cost').on('click', function (e) {
		e.preventDefault();
		var data = $(this).data('id');
		$("#hidden_id_var").attr('data-variablecost-id',data);
		$("#hidden_id_var").val(data);
		$('#delete_variablecost').modal({
	        show: true
	    });
	});
	
	$('#del_fixedcost').on('submit', function (e) {
		var h =$("#hidden_id_fix").val();
		$.ajax({
          type: 'delete',
          url: '/cost/',
          data: {"fixedcost_id":h},
          success: function (data) {
        	  $('#delete_fixedcost').modal('toggle');
        	  
        	  $("#result").html('<div class="alert alert-success"><button type="button" class="close">&nbsp;×</button>Data has been deleted successfully..</div>');
              window.setTimeout(function() {
                    $(".alert").fadeTo(500, 0).slideUp(500, function(){
                        $(this).remove(); 
                    });
                }, 5000);
              $('.alert .close').on("click", function(e){
                    $(this).parent().fadeTo(500, 0).slideUp(500);
                 });
              location.reload();
          }
		});
	});
	
	$('#del_variablecost').on('submit', function (e) {
		var h =$("#hidden_id_var").val();
		$.ajax({
		  type: 'delete',
          url: '/cost/',
          data: {"variablecost_id":h},
          success: function (data) {
        	  $('#delete_variablecost').modal('toggle');        	  
        	  $("#result").html('<div class="alert alert-success"><button type="button" class="close">&nbsp;×</button>Data has been deleted successfully..</div>');
              window.setTimeout(function() {
                    $(".alert").fadeTo(500, 0).slideUp(500, function(){
                        $(this).remove(); 
                    });
                }, 5000);
              $('.alert .close').on("click", function(e){
                    $(this).parent().fadeTo(500, 0).slideUp(500);
                 });
              location.reload();
	       }
		});
	});
	
	
}]);
