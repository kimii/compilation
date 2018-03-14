/*
$(document).ready(function(){
  var head = ['#','<a style=cursor:pointer>IP<span class="glyphicon glyphicon-menu-down"></span></a>','icon','<a style=cursor:pointer>ASN<span class="glyphicon glyphicon-menu-down"></span></a>','neighbours','topology'];
  var body = [
    ['202.118.224.100','CN','4538','details','details'],
    ['202.118.224.101','CN','4538','details','details'],
    ['202.118.224.103','CN','4538','details','details']
  ];
  var data = {
    'head': head, 
    'body': body
  };
  
  var options = {}
  var container = document.getElementById('table_div');
  
  var table = new mylib.myTable(container, data, options);
});
*/

/*
$(document).ready(function(){
  var options = {}
  var container = document.getElementById('table_div');
  
  var table = new mylib.myTableOnline(container, request, options);

  //todo: tbl.pager_front, tbl.page_size, tbl.refresh to request data and refresh table.//
  function request(tbl){
    console.log(tbl.pager_front, tbl.page_size);
    $.ajax("/public/data.json", {
      type: 'GET',
      async: false,
      success: function(d){
        tbl.refresh(d); //important!! remember to manually refresh the tbl.
      },
      error: function (jqXhr, textStatus, errorMessage) {console.log('Error' + errorMessage);}
    });
  };
  
  $.ajax("/public/small.json", {
    type: 'GET',
    async: false,
    success: function(data){
      var container = document.getElementById('graph_div');
      var graph = new mylib.myVisjsGraph(container, data);
    },
    error: function (jqXhr, textStatus, errorMessage) {console.log('Error' + errorMessage);}
  });
});
*/

$(document).ready(function(){
  var options = {}
  var container = document.getElementById('table_div');
  
  var table = new mylib.myTableOnline(container, request, options);

  function request(tbl){
    console.log(tbl.pager_front, tbl.page_size);
    $.ajax("/public/data.json", {
      type: 'GET',
      async: false,
      success: function(d){
        tbl.refresh(d); //important!! remember to manually refresh the tbl.
      },
      error: function (jqXhr, textStatus, errorMessage) {console.log('Error' + errorMessage);}
    });
  };

  $.ajax("/public/huge.json", {
    type: 'GET',
    async: false,
    success: function(data){
      var container = document.getElementById('graph_div');
      var graph = new mylib.myD3Graph(container, data, {});
    },
    error: function (jqXhr, textStatus, errorMessage) {console.log('Error' + errorMessage);}
  });
});
