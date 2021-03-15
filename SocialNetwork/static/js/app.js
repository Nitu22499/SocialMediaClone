$("#searchfriend").keyup(function () {
    var user = $(this).val();
    const search_icon = $('#search-icon')
    const search_div = $('#browsers')

    $.ajax({
      url: '/ajax-search/',
      data: {
        'user': user
      },
      dataType: 'json',
      
      success: function (data) {
          console.log(data);
          search_div.html(data['html_from_view'])
        }
    });

  });
  