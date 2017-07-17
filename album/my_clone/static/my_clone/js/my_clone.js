document.addEventListener("DOMContentLoaded", function(){
    var likeButton = $('.like');
//    likeButton.prop('clickCounter', 0);
//    console.log(likeButton);

    $(likeButton).each(function(){
        var clickCount = 0;
        var clickDisplay = $(this).next('.counter');

        $(this).on('click', function(){
            clickCount += 1;
            $(clickDisplay).text(clickCount)
            console.log(clickDisplay);
        });
    });
});

