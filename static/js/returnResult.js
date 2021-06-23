"use strict";

console.log("i am saving input!");

function returnResults(evt) {

    evt.preventDefault();


    let url = "/save-city";

    let savedData = {
                     'city': $('#user-city').val(),
                    };


    $.post(url, savedData, (response) => {


        let final_url = response;


        let settings = {
                        "async": true,
                        "crossDomain": true,
                        "url": final_url,
                        "method": "GET",
                        "headers": {}
                        }


        $.ajax(settings).done(function (data) {


        document.getElementById('flickr').replaceChildren();
        $("#galleryTitle").html("<span>You have searched for people in </span>" + savedData["city"]+"."+ 
                                "<h5>Select images on the top right then click 'Save to Account'<h5>");
        $("#instructions").html("<p class='notbold'>Click the top right hand corner to select pictures.</p>");
        document.getElementById('flickr').scrollIntoView({ block: 'start',  behavior: 'smooth' });
        $("#ending").html("<br><h2 style='margin-top:10vh;'>Log in to save these images to your account</h2><p><b>Demo Account:</b> demo@demo &nbsp;<b>Password:</b> demo</p>");

        $.each( data.photos.photo, function( i, gp ) {

                let farmId = gp.farm;
                let serverId = gp.server;
                let id = gp.id;
                let secret = gp.secret;
        
        $("#flickr").append('<a href="https://www.flickr.com/photo.gne?id=' + id + '/" target="_blank"><img src="https://farm' + farmId + '.staticflickr.com/' + serverId + '/' + id + '_' + secret + '.jpg"/></a><input class="form-check-input" type="checkbox" name="selected" value="https://farm' + farmId + '.staticflickr.com/' + serverId + '/' + id + '_' + secret + '.jpg">');

        });
        });
        $("#image-form").on("submit", saveImages);
        });
}

$("#city-form").on("submit", returnResults);


// $("#city-form").reload(true);