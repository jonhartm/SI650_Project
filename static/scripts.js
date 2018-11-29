$('#btn_search').click(function() {
  var term = $('#search_term').val();
  console.log("Searching for " + term);

  // Clear the div of any existing content and add a spinner
  $(".account_results").empty();
  $(".account_results").append(
    $("<img>")
      .attr("src", '/static/ajax-loader.gif')
  );

  $.ajax({
    contentType: "application/json",
    datatype: "json",
    data:JSON.stringify({"search_term":term}),
    type:"POST",
    url:'/get_account',
    success: function(response) {
      console.log("ok");
      // Clear the div of any existing content
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

$(document).on("click", ".account_info", function(event) {
  var user_id = $(this).find(".account_id").val();
  var search_term = $('#search_term').val();

  // Clear the div of any existing content and add a spinner
  $(".tweet_results").empty();
  $(".tweet_results").append(
    $("<img>")
      .attr("src", '/static/ajax-loader.gif')
  );

  $.ajax({
    contentType: "application/json",
    datatype: "json",
    data:JSON.stringify({
      "id":user_id,
      "search_term":search_term
    }),
    type:"POST",
    url:'/get_tweets_by_account',
    success: function(response) {
      console.log("ok");

      $(".tweet_results").empty();
      for (var i = 0; i < response.length; i++) {
        $(".tweet_results").append(
          $("<div>")
            .addClass("tweet_info")
            .append(
              $("<p>")
                .addClass("tweet_text")
                .text(
                  "@"+response[i].user+": "+response[i].text
                )
            )
            .append(
              $("<a>")
                .addClass("tweet_link")
                .attr("href", 'https://twitter.com/i/web/status/'+response[i].id_str)
                .text("Link to Tweet")
            )
        );
      }
    },
    error: function(error) {
      console.log("uh oh");
      console.log(error);
    }
  })
});
