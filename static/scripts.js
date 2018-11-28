$('#btn_search').click(function() {
  var term = $('#search_term').val();
  console.log("Searching for " + term);

  $.ajax({
    contentType: "application/json",
    datatype: "json",
    data:JSON.stringify({"search_term":term}),
    type:"POST",
    url:'/get_account',
    success: function(response) {
      console.log("ok");
      console.log(response);
    },
    error: function(error) {
      console.log("uh oh");
      console.log(error);
    }
  })
})
