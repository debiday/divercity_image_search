"use strict";

console.log("i am saving image results!");

function saveImages(evt) {
    console.log('hello save image function');

    evt.preventDefault();

    let today = new Date();
    let date_saved = (today.getMonth()+1)+'-'+today.getDate()+'-'+today.getFullYear();

    let user_id = $('#user-id').text();

    let url = "/save-images";

    let savedData = {
                    //  'user_id': user_id,
                     'city': $('#user-city').val(),
                     'user_id': user_id,
                     'date_saved': date_saved,
                     'notes': $('#user-city').val(),
                    //  'email': email
                    };
    console.log("*******");
    console.log(savedData['user_id']);

    $.post(url, savedData, (response) => {


        alert(response);

    });
}

// This is happening after the elements are loaded on the page in returnResult.js
// $("#image-form").on("submit", saveImages);
