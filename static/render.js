var len = $('.section').length;
var i = 0;

$(".section").hide();

$(".section:nth-child("+(i+1)+")").show();

console.log(len);

if (len == 0)
	$("#next").hide();
else if(len == 1)
	$("#next").html("submit");



$("#next").click(function(){
	
	$("video").each(function() {
		$(this).get(0).pause();
	});
	
	++i;
	
	$(".section:nth-child("+i+")").hide();
	$(".section:nth-child("+(i+1)+")").show();
	
	console.log(i);
	
	
	if ( i == len-1)
		$("#next").html("submit");

	if (i == len)
		$("body").html("<h1>Thank You!</h1>");

});
