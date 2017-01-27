(function() {
    var app;

    app = angular.module('supplieriqApp');

    var actions = {        
        'get' : {
            method : 'GET',           
            isArray : false
        },
        'save' : {
            method : 'POST',
            isArray : false
        },
        'query' : {
            method : 'GET',
            transformResponse : function(data) {
                jdata = JSON.parse(data);
                if (jdata['results']){
                    jdata = jdata.results;
                }
                return jdata;
            },
            isArray : true
        },
        'remove' : {
            method : 'DELETE'
        },
        'delete' : {
            method : 'DELETE'
        },

        'list' : {
            method : 'GET',
            isArray : false
        },


    };

    app.factory('GetVendorList', ['$resource',
        function($resource) {
            return $resource('/vendors/ ', {}, actions);
        }]);
    app.factory('GetVendorDetails', ['$resource',function($resource) {
          return $resource('/vendors/?id=:id', {id:'@id'}, actions);
      }]);
    

}).call(this);
