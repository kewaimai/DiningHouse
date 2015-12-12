function operated(obj) {
	var temparray = SaveClass(obj);

	obj.on({
		"mousemove": function (){
			var currentCount=0;
	        currentCount = obj.index($(this)[0]);
	        obj.each(function(i, e){
	        	if(i<=currentCount) {
		            $(this).removeClass();
		            $(this).addClass("on");
	         	} else {
		           $(this).removeClass();
		           $(this).addClass("off");
		        }
	    	});
		},
		"mouseout": function (){
			$.each(obj, function (i, e){
				$(this).removeClass();
				$(this).addClass(temparray[i]);
			});
		},
		"click": function (){
			temparray = SaveClass(obj);
            console.log(temparray);
		}
	});

	function SaveClass(obj) {
	  	var temClassArry = [];
		$.each(obj, function(e, i) {
			temClassArry.push($(this).attr("class"));
		});

	  	return temClassArry;
	}
}