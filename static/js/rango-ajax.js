$(document).ready(function(){
    $('#likes').click(function(){
        var catid;
        console.log("here in jquery!");
        catid = $(this).attr("data-catid");
        $.get('/rango/like_category/', {category_id: catid}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        }); 
    });

    $('#suggestion').keyup(function(){
        var query, all;
        query = $(this).val();
        if(query == '' || query == ' '){
            all = true;
        }else{
            all = false;
        }
        $.get('/rango/suggest_category/', {suggestion: query, flag: all}, function(data){
            $('#cats').html(data);
        }); 
    });

    $('.add_page').click(function(){
        var category, title, url;
        title = $(this).attr('data-title');
        url = $(this).attr('data-url');
        category = $(this).attr('data-cat');

        $(this).attr('disabled', 'true');
        $(this).addClass('btn-success');
        $(this).text('Added');

        if(title == '' ){
            title = 'No title!'
        }

        $.get('/rango/insert_page/', {'title': title, 'url': url, 'category': category}, function(data){
            if(data != 'Success'){
                alert(data);
                $('.add_page').attr('disabled', 'false');
                $('.add_page').removeClass('btn-success');
                $('.add_page').text('Add Page');
            }
        });
    });
        
});