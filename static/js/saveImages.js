"use strict";

console.log("i am saving image results!");

function saveImages(evt) {
    console.log('hello save image function');

    evt.preventDefault();

    let today = new Date();
    let date_saved = today.getMonth()+'-'+today.getDate()+'-'+today.getFullYear();
    let user_id = $('#user-id').text();

    let arr = [];

    $('input.form-check-input:checkbox:checked').each(function () {
        arr.push($(this).val());
    });

    let urls = arr.join(", ");

    let url = "/save-images";

    let city = $('#user-city').val();
    let notes = city.charAt(0).toUpperCase() + city.slice(1)


    let savedData = {
                    //  'user_id': user_id,
                     'city': $('#user-city').val(),
                     'user_id': user_id,
                     'date_saved': date_saved,
                     'notes': notes,
                     'urls': urls,
                    //  'email': email
                    };

    $.post(url, savedData, (response) => {

        alert(response);
        location.reload();

    });
}

// This is happening after the elements are loaded on the page in returnResult.js
// $("#image-form").on("submit", saveImages);
