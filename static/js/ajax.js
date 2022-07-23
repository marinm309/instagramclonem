$('.like').click(function(e){
    e.preventDefault()
    var this_ = $(this)
    var likeUrl = this_.attr('href')
    $.ajax({
        url: likeUrl,
        method: 'GET',
        data: {},
        success: function(request){
            $(request.indf).text(request.likes)
            $("#" + request.basic_indf + '6969').load(location.href + ' ' + "#" + request.basic_indf + '6969');
        }
    });
});

$('.comment-btn').click(function(f){
    f.preventDefault()
    var comment = $(this)
    var commentUrl = comment.attr('data-href')
    var csrf = $('input[name=csrfmiddlewaretoken]').val()
    var elements = comment.attr('data-id');

    $.ajax({
        url: commentUrl,
        method: 'POST',
        data: {csrfmiddlewaretoken: csrf, comment_text: $('#' + elements).val()},
        success: function(request){
            $(request.indf_comment).text(request.comments)
            $('.type-comments').val('')
        }
    });
});

$('.single-comment-btn').click(function(z){
    z.preventDefault()
    var single_comment = $(this)
    var single_commentURL = single_comment.attr('data-href')
    var csrf = $('input[name=csrfmiddlewaretoken]').val()
    var single_elements = single_comment.attr('data-id');
    var comment_the_comment = $('#hidden-comment-id').text()


    $.ajax({
        url: single_commentURL,
        method: 'POST',
        data: {csrfmiddlewaretoken: csrf, comment_text: $('#' + single_elements).val(), reply_comment: comment_the_comment},
        success: function(request){
            $('.type-comments').val('')
            location.reload()
        }
    });
});

$('.single-post-comment-like-btn').click(function(m){
    m.preventDefault()
    var single_like = $(this)
    var single_likeURL = single_like.attr('href')

    $.ajax({
        url: single_likeURL,
        method: '',
        data: {},
        success: function(request){
            $(request.indf).text(request.likes)
            $("#" + request.basic_indf + '1234').load(location.href + ' ' + "#" + request.basic_indf + '1234');
        }
    });
});

$('.delete-single-comment').click(function(l){
    l.preventDefault()
    var single_delete_comment = $(this)
    var single_delete_commentURL = single_delete_comment.attr('href')

    $.ajax({
        url: single_delete_commentURL,
        method: '',
        data: {},
        success: function(request){
            $(request.basic_indf).remove();
        }
    });
});

$('.user-follow-btn').click(function(u){
    u.preventDefault()
    var follow_user = $(this)
    var follow_userURL = follow_user.attr('href')

    $.ajax({
        url: follow_userURL,
        method: '',
        data: {},
        success: function(request){
            var follow_txt = $('#' + request.basic_indf).text()
            if(follow_txt == 'Follow'){
                $('.' + request.basic_indf).text('Unfollow')
                $('.' + request.basic_indf).css('color', 'red')
            }else{
                $('.' + request.basic_indf).text('Follow')
                $('.' + request.basic_indf).css('color', 'blue')
            }
            $('#' + request.basic_indf + '123').text(request.profile_followers)
            $('#' + request.basic_indf + '321').text(request.profile_followings)
            $('#' + request.basic_indf + '456').text(request.profile_followers)
            $('#' + request.basic_indf + '654').text(request.profile_followings)
        }
    });
});

$('.reply-btn').click(function(j){
    j.preventDefault()
    var reply_user = $(this)
    var reply_userURL = reply_user.attr('href')

    $.ajax({
        url: reply_userURL,
        method: '',
        data: {},
        success: function(request){
            $('.type-comments').val(request.reply_key_word + ' ')
            $('#hidden-comment-id').text(request.comment)
        }
    });
});

$('.view-replies-btn').click(function(p){
    p.preventDefault()
    var current_comment = $(this)
    var current_commentURL = current_comment.attr('href')

    $.ajax({
        url: current_commentURL,
        method: '',
        data: {},
        success: function(request){
            reply = document.getElementById(request.indf + '007')
            if (reply.style.display == 'block'){
                reply.style.display = "none";
            } else {
                reply.style.display = "block";
            }
            
        }
    });
});

$('.delete-reply-btn').click(function(w){
    w.preventDefault()
    var delete_reply = $(this)
    var delete_replyURL = delete_reply.attr('href')

    $.ajax({
        url: delete_replyURL,
        method: '',
        data: {},
        success: function(request){
            $(request.indf).remove();
            $('.view-replies-btn').load(' .view-replies-btn')
        }
    });
});


$('.friend-btn').click(function(h){
    h.preventDefault()
    var friend = $(this)
    var friendURL = friend.attr('href')

    $.ajax({
        url: friendURL,
        method: '',
        data: {},
        success: function(request){
            hide_element = document.getElementById('to_be_hidden')
            hide_element.style.display = 'none'
            show_element = document.getElementById('to_be_shown')
            show_element.style.display = 'block'
            $('#js-username').text(request.chat_with)
            document.getElementById("js-img").src = request.other_user_img
            $('#js-status').text(request.other_user_activity)
            var mLen = request.merged_messages.length
            for (var i = 0; i < mLen; i++) {
                if(mLen - 1 == i){
                    if(request.merged_users[i] == request.user){
                        $('.test-mess').append('<div class="right-bubble-wrapper" id="last">' + '<div class="right-bubble">' + '<li class="right-text">' + request.merged_messages[i] + '</li>' + '</div>' + '</div>') 
                    }
                    else{
                        $('.test-mess').append('<div class="left-bubble-wrapper" id="last">' + '<div class="left-bubble">' + '<li class="left-text">' + request.merged_messages[i] + '</li>' + '</div>' + '</div>')
                    }
                }
                else if(request.merged_users[i] == request.user){
                    $('.test-mess').append('<div class="right-bubble-wrapper">' + '<div class="right-bubble">' + '<li class="right-text">' + request.merged_messages[i] + '</li>' + '</div>' + '</div>')
                }
                else{
                    $('.test-mess').append('<div class="left-bubble-wrapper">' + '<div class="left-bubble">' + '<li class="left-text">' + request.merged_messages[i] + '</li>' + '</div>' + '</div>')
                }
              }
                var element = document.getElementById("last")
                element.scrollIntoView()

                var intervalId = window.setInterval(function(){
                    
                  }, 2000);
        }
    });
});


$('.send-message-btn').click(function(y){
    y.preventDefault()
    var send_message = $('.send-message-form')
    var send_messageURL = send_message.attr('data-href')
    var csrf = $('input[name=csrfmiddlewaretoken]').val()
    var message = $('.message-field').val()
    var other_user = $('#js-username').text()

    $.ajax({
        url: send_messageURL,
        method: 'POST', 
        data: {csrfmiddlewaretoken: csrf, other_user: other_user, message: message},
        success: function(request){
            $('.message-field').val('')
            if(message.length > 0){
                $('.test-mess').append('<div class="right-bubble-wrapper" id="last">' + '<div class="right-bubble">' + '<li class="right-text">' + message + '</li>' + '</div>' + '</div>')
            }
            var element = document.getElementById("last")
            element.scrollIntoView()
        }
    });
});

$('#chat_search_word').click(function(g){
    g.preventDefault()
    var key_word_field = document.getElementById('chat_search_word')
    var chatUrl = $('#chat-form-id').attr('data-href')
    key_word_field.addEventListener('keyup', (e) => {
        var chat_search_word = $(this).val()
        $.ajax({
            url: chatUrl,
            method: 'GET',
            data: {chat_search_word: chat_search_word},
            success: function(request){
                lstLen = request.all_in_chat.length
                for (var i = 0; i < lstLen; i++){
                    var current_username = request.all_in_chat[i]
                    var current_username_div = document.getElementById(current_username)
                    if(current_username in request.matches){
                        current_username_div.style.display = 'block'
                    }
                    else{
                        current_username_div.style.display = 'none'
                    }
                }
            }
        });
    });
});

$('select').click(function(){
    var selected_time = $(this).val()
    if(selected_time == '0'){
        var regular_time_field = document.getElementById('regular_time')
        regular_time_field.style.display = 'none'
        var custom_time_field = document.getElementById('custom_time')
        custom_time_field.style.display = 'block'
    }
});

function loadlink(){ 
        $('.friend-btn').trigger('click');
}
