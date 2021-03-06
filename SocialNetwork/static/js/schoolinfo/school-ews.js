// Utility function to get csrf-token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('td[contenteditable=true]').on('click', function(){
    document.execCommand('selectAll',false,null);
})

$('#convert-table').click( function() {
    var table = $('#table').tableToJSON({
        ignoreRows: [0,1],  // To Ignore the first two rows consisting of table heading

        headings: [
            'class_name',
            'boys_1','girls_1',  // Array of Column Header names
            'boys_2','girls_2',
            'boys_3','girls_3',
            'boys_4','girls_4',    
        ]
    }); // Convert the table into a javascript object
    // console.log(JSON.stringify(table));
    // console.log(table);
    
    let response = {
        table,
        academic_year: $('#year').text()
    }
    ac_year=$('#year').text()
    console.log(ac_year)
    response = JSON.stringify(response).replace(/-/g, '')

    fetch(`${window.location.origin}/schoolinfo/school-ews/${ac_year}/save`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json'
        },
        body: response
        })
        .then((res) => res.json())
        .then(function(data) {
            if (data['err'] == undefined) {
                window.location.reload()
            }
        })
})