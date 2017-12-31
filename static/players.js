$(function() {
    $('button').click(function() {
        $.ajax({
            url: '/players',
            type: 'GET',
            success: function(data) {
                console.log(data);
                var json = $.parseJSON(data);
                    $(json).each(function(i,val){
                        $.each(val,function(k,v){
                	      if (k === 'players_list')  {
			           $('#players_list').append(v);
			      }
                    });
                });
		},
            error: function(error) {
                console.log(error);
            }
        });
    });
});
