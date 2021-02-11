var len = $('.section').length;
var i = 0;

//show first section
$(".section").hide();
$(".section:nth-child(1)").show();

//button based on number of sections 
//0 - no button, 1 - submit, otherwise - next
if (len == 0)
    $("#next").hide();
else if (len == 1)
    $("#next").html("submit");

//button click
$("#next").click(function() {
	
	//pause videos
    $("video").each(function() {
        $(this).get(0).pause();
    });

    ++i;
	
	//show next section
    $(".section:nth-child(" + i + ")").hide();
    $(".section:nth-child(" + (i + 1) + ")").show();

	//last page
    if (i == len - 1)
        $("#next").html("submit");
	
	//done
    if (i == len)
        $("body").html("<h1>Thank You!</h1>");

});