$(function() {
    $('button').click(function() {
        $.ajax({
            url: '/draw_number',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                console.log(data);
                var drawn_number;
                var json = $.parseJSON(data);
                    $(json).each(function(i,val){
                        $.each(val,function(k,v){
			     console.log(k+" : "+ v);     
                	      if (k === 'drawn_number')  {
				  document.getElementById("draw_number").innerHTML = v
			          $('#drawn_number').append(v+" ");
			      }
                	      if (k === 'winning_table')  {
				  document.getElementById("winning_table").innerHTML = v
			      }
                	      if (k === 'winner_1_name')  {
				  document.getElementById("winner_1_name").innerHTML = v
			      }
                	      if (k === 'winner_2_name')  {
				  document.getElementById("winner_2_name").innerHTML = v
			      }
                	      if (k === 'winner_1_table')  {
				  document.getElementById("winner_1_table").innerHTML = v
			      }
                	      if (k === 'winner_2_table')  {
				  document.getElementById("winner_2_table").innerHTML = v
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
