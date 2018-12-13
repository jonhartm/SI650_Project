$('#btn_search').click(function() {
  var term = $('#search_term').val();
  console.log("Searching for " + term);

  // Clear the div of any existing content and add a spinner
  $(".account_results").empty();
  $(".account_results").append(
    $("<img>")
      .attr("src", '/static/ajax-loader.gif')
  );

  $(".tweet_results").empty();
  $("#on_the_issues").empty();
  $("#related_terms").empty();

  $.ajax({
    contentType: "application/json",
    datatype: "json",
    data:JSON.stringify({"search_term":term}),
    type:"POST",
    url:'/get_account',
    success: function(response) {
      console.log(response);

      // Related terms will always be the last item in the response.
      // Pop it off and display it in the proper div
      related_terms = response.pop()['related_terms'];
      $("#related_terms").html("<b>Related Terms</b>: " + related_terms.join(', '));

      // Clear the div of any existing content
      $(".account_results").empty();
      // Iterate through the results and add a div for each
      for (var i = 0; i < response.length; i++) {
        $(".account_results").append(
          $("<div>")
            .addClass("account_info")
            .append(
              $("<div>")
                .addClass("account_image_container")
                  .append(
                    $("<img>")
                      .addClass("account_profile_image")
                      .attr("src", response[i].profile_image.replace('normal', 'bigger'))
                  )
            )
            .append(
              $("<div>")
                .addClass("account_detail_container")
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

  // remove the active class from all other account detail divs
  $(".account_info").removeClass("active");

  $(this).addClass("active");

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
      $(".tweet_results").empty();
      for (var i = 0; i < response.length; i++) {
        if ("id_str" in response[i]) {
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
      }
    },
    error: function(error) {
      console.log("uh oh");
      console.log(error);
    }
  })

  $.ajax({
    contentType: "application/json",
    datatype: "json",
    data:JSON.stringify({
      "id":user_id,
      "topic":$("#search_term option:selected").text()
    }),
    type:"POST",
    url:'/get_OTI_json_by_account',
    success: function(response) {
      $("#on_the_issues").empty();
      $("#on_the_issues").text("Results from On The Issues...");
      var issues_list = $("<ul>");
      for (var i = 0; i < response.length; i++) {
        // console.log(response[i]);
        issues_list.append(
          $("<div>")
            .append(
              $("<li>")
                .text(response[i][0] + " " + response[i][1])
            )
        );
      }
      $("#on_the_issues").append(issues_list);
    },
    error: function(error) {
      console.log("uh oh");
      console.log(error);
    }
  })
});
