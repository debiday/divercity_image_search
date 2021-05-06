"use strict";

console.log("i am saving input!");

function saveInput(evt) {
    console.log('hello input function');

    evt.preventDefault();

    // //Get email
    // let email = $('#user-email').text()

    // //Get user_id
    // let user_id = $('#user-id').text()


    let url = "/save-city";
    let response = "hello response"
    //saves values from the front end and sends it to server
    let savedData = {
                    //  'user_id': user_id,
                     'city': $('#user-city').val()
                    //  'email': email
                    };

    $.post(url, savedData, (response) => {

        console.log("post reponse from server");

        let city = response;

        let url_front = "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=4f2a9c7f2ea592f840664a1486e37348&text=%22";
        let url_back = "+people%22&per_page=100&format=json&nojsoncallback=1";
        let final_url = url_front.concat(city, url_back);


        let settings = {
        "async": true,
        "crossDomain": true,
        "url": final_url,
        //   "url": "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=4f2a9c7f2ea592f840664a1486e37348&text=%22london+people%22&per_page=100&format=json&nojsoncallback=1",
        "method": "GET",
        "headers": {}
        }


        $.ajax(settings).done(function (data) {
        console.log(data);


        //add a jquery to replace "place with user input" 
        $("#galleryTitle").append(response+" ");
                $.each( data.photos.photo, function( i, gp ) {

        let farmId = gp.farm;
        let serverId = gp.server;
        let id = gp.id;
        let secret = gp.secret;
        // let button_html = "<input type="radio" value="email">"


        console.log(farmId + ", " + serverId + ", " + id + ", " + secret);
        //  https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg

        //https://farm' + farmId + '.staticflickr.com/' + serverId + '/' + id + '_' + secret + '.jpg
        //https://www.flickr.com/photos/155854489@N04/51154725669/


        $("#flickr").append('<a href="https://www.flickr.com/photo.gne?id=' + id + '/" target="_blank"><img src="https://farm' + farmId + '.staticflickr.com/' + serverId + '/' + id + '_' + secret + '.jpg"/></a><input style="display:inline-block; height:20%; "type="radio" value="id">');
        // $("#results").append('<p><a href="'+myresult_size.url+'" target="_blank"><img src="'+myresult_size.source+'"/></a></p>');
        //'<p><span id="{child.child_id}" class="child_bio">{child.fname} {child.lname}
        });
        });

        });
}

$("#city-form").on("submit", saveInput);
// $("#city-form").reload(true);
