    let friendName = document.querySelector('.friendName').id;
    let currentRoom = 'nitu_sharma_22'
    console.log(friendName);
    var user= document.getElementById("userid").value;
    console.log(user);
    let chatInput = $('#chat-input');
    let chatButton = $('#btn-send');
    let messageList = $('#messages');

    let socket = new WebSocket(
            'ws://' + window.location.host +
            '/ws/communications/' + currentRoom + '/');

    console.log(socket);
   
    socket.onopen = (function(e){
            chatInput.keypress(function (e) {
                if (e.keyCode == 13)
                    chatButton.click();
            });
            
            chatButton.click(function () {
                if (chatInput.val().length > 0) {
                    sendMessage(user,friendName, chatInput.val());
                    chatInput.val('');
                }
            });

            function sendMessage(user,recipient, body) {
                console.log(user,recipient,body)   
                  socket.send(JSON.stringify({
                    'author':user,
                    'friend': recipient,
                    'message': body
                }));
            }
    });
    
        
    socket.onmessage = function (e) {
        console.log("e",typeof(e.data),e.data)
        const data = JSON.parse(e.data);
        console.log('data',data);
        drawMessage(data) ;
       
    };
    
    function drawMessage(message) {
        console.log("mess",message)
        let position = 'left';
        console.log(message.author)
        let date = new Date(message.timestamp);
        if (message.author === user) position = 'right';
        const messageItem = `
            <li class="message ${position}">
                 <div class="avatar">${message.friend}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.message}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
            console.log("type",typeof(messageItem));
            $(messageItem).appendTo('#messages');
            
 
 }
    socket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

