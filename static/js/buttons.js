

var apiurl,myresult,apiurl_size,selected_size;
apiurl = "https://api.flickr.com/services/rest/?method=flickr.photos.getRecent&api_key=ca370d51a054836007519a00ff4ce59e&per_page=10&format=json&nojsoncallback=1";

$(document).ready(function(){
$("#sq").click(function(){
selected_size=75;
})
});

$(document).ready(function(){
$("#lg-sq").click(function(){
selected_size=150;
})
});

$(document).ready(function(){
$("#thumb").click(function(){
selected_size=100;
})
});

$(document).ready(function(){
$("#small").click(function(){
selected_size=240;
})
});

$(document).ready(function(){
$("#mid").click(function(){
selected_size=500;
})
});

$(document).ready(function(){
$("#ori").click(function(){
selected_size=640;
})
});

$(document).ready(function(){
$('#button').click(function(){
$.getJSON(apiurl,function(json){
$.each(json.photos.photo,function(i,myresult){
apiurl_size = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=ca370d51a054836007519a00ff4ce59e&photo_id="+myresult.id+"&format=json&nojsoncallback=1";
$.getJSON(apiurl_size,function(size){
$.each(size.sizes.size,function(i,myresult_size){
if(myresult_size.width==selected_size){
$("#results").append('<p><a href="'+myresult_size.url+'" target="_blank"><img src="'+myresult_size.source+'"/></a></p>');
}
})
})
});
});
});
});


cityurl = https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=53578c5fcf2a1f0472f8492fe0ced3d0&text=%22singapore+people%22&format=json&nojsoncallback=1&auth_token=72157719079408853-9f15a2de6ac531a6&api_sig=0158d4d1f26aee753c406ba0cfdfb4f0
https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=53578c5fcf2a1f0472f8492fe0ced3d0&text=%22california+people%22&format=json&nojsoncallback=1&auth_token=72157719079408853-9f15a2de6ac531a6&api_sig=3ddf843481a9a549dba00b79f614d149
texturl = "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=53578c5fcf2a1f0472f8492fe0ced3d0&text=singapore+and+people&format=json&nojsoncallback=1&auth_token=72157719079408853-9f15a2de6ac531a6&api_sig=602e9cc434b548edcdf74231ba05285f";

 