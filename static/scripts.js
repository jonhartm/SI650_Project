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
      // Clear the div og any existing content
      $(".account_results").empty();
      // Iterate through the results and add a div for each
      for (var i = 0; i < response.length; i++) {
        $(".account_results").append(
          $("<div>")
            .addClass("account_info")
            .append(
              $("<p>")
                .addClass("account_user_name")
                .text(response[i].name)
            )
            .append(
              $("<a>")
                .addClass("account_twitter_link")
                .attr("href", 'https://twitter.com/'+response[i].screen_name)
                .text('@'+response[i].screen_name)
            )
            .append(
              $("<img>")
                .addClass("account_profile_image")
                .attr("src", response[i].profile_image)
            )
            .append(
              $("<input>")
                .addClass("account_id")
                .attr("type", "hidden")
                .val(response[i].id)
            )
        );
      }
    },
    error: function(error) {
      console.log("uh oh");
      console.log(error);
    }
  })
})
