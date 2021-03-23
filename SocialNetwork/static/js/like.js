$('.like-form').submit(function(e){
    e.preventDefault()
    // ssconsole.log("helo");
    const post_id = $(this).attr('id');
    const url = $(this).attr('action');
    console.log("helo");
    console.log(url);
    const icon = this.querySelector('i');
    console.log(icon)
    const like_count = this.querySelector('ins');
    // console.log(like_count.innerHTML );

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'post_id':post_id,
        },
        success : function(response){

            if(icon.classList.contains('fas fa-thumbs-up like')) {
                
                $('#like{{post.id}}').html($('<i/>',{class:'fas fa-thumbs-down dislike'})) ;
                // like_count.innerHTML = parseInt(like_count.innerHTML)+1;
                // console.log(like_count.innerHTML );
                // console.log("IF");

               
            } else {
                   $('#like{{post.id}}').html($('<i/>',{class:'fas fa-thumbs-up like'}));
                //   like_count.innerHTML = parseInt(like_count.innerHTML)-1;
                // //   console.log(like_count.innerHTML);
                // console.log("Else");
                 
            }
            console.log("hi");
                 
            },
            error : function(rs, e){
                console.log(rs.responseText);
            },
    })

})