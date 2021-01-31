var page = $("#pageID").html();

document.querySelector("#pageLink").innerHTML = window.location.href + "page?page="+page;

var sectionTypes = ["reading", "free", "video"];


$(function() {
	$(".sections").on("change", "select.type", function() {
		let typ = $("option:selected", this).val();
		
		
		let $section = $(this).parent(".section");
		let i;
		for (i = 0; i < sectionTypes.length; i++) {
			if (typ == sectionTypes[i]) {
				
				if (!$section.hasClass(typ)) {
					let classes = $section.attr('class').split(/\s+/);
					
					classes.splice(classes.indexOf("section"), 1);
					
					$section.removeClass(classes[0]);
					$section.addClass(typ);
				}
				break;
			}
		}
		
		$.get('/changeSection', 
			{
				pageID: page,
				i: $section.index(),
				type	: typ
			}).done(function( data ) {
				$section.find(".content").html(data);
		});

		return false;
	});
});


$(function() {
	$(".sections").on("click", "button.contentSave", function() {
	
		
		let $section = $(this).parent(".content").parent(".section");
		
		
		let typ = $("option:selected", $section).val();
		
		let cont = {};
		
		
		let catCont = {
			"reading": ["title", "text"],
			
			"free": ["text"],
			"video": ["link"]
		};
		
		catCont[typ].forEach(function (item, index) {
			cont[item] = $section.find(".contentInput."+typ+"."+item).val();
		});
		
		
		$.get('/saveSection', 
			{
				pageID: page,
				i: $section.index(),
				type: typ,
				content	: cont
				
			});
		
	});
});
