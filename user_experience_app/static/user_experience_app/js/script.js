$('body').on('click','.like',function(e){

// $('.like').click(function(e){
    e.preventDefault();        
    console.log('like/un-like has been clicked');
    let movie_id = $(this).attr('movie_id');
    $.ajax({
        url: `/stream-bunny/user_experience/like/${movie_id}/main_page`,                         
        success: serverResponse => {
            $(`#like_count_${movie_id}`).text(serverResponse)

            console.log($(this).text())
            if ($(this).text() == "like") {
                $(this).text("un-like");
            } else {
                $(this).text("like");
            }    
        }
    })
});
