(function(){
	var body_width,body_height;
	var size = function(){
		body_width = $(document.body).width();
		body_height = $(document.body).height();
		$(".bigbox").css({
			"margin-top" : (body_height - 640)/2,
		});
	};
	$(function() {
		size();
		$(window).bind("resize", function () {
			size();
		});
		Y.wheel(
			function (n) {
				var  x = $(".app-box").scrollLeft();
				$(".app-box").scrollLeft(x + (n * 100));
				//alert(x + (n * 100));
			},
			function(e,dom){
				if($(dom).parents(".app-box").length)
					return true;
				else
					return false;
			}
		);

		$(".box > ul > li").bind("click", function () {
			if($(this).attr("_url"))
			{
				$("#iframe").attr({src : $(this).attr("_url")});
				$(".detail").css({
					"height" : ((body_height + 100) - 100),
					"width" : Math.floor((body_height - 200)/0.618),
					"top" : 50,
					"left" : 50
				});
				$(".detail > .close")
				.css({
					"margin-left" : Math.floor((body_height - 200)/0.618 - 40),
					"margin-top" : 10
				})
				.bind("click", function () {
					$(".cover").fadeOut(200);
				});

				$(".cover").css({opacity : 1});
				$(".cover").fadeIn(200);
			}
		});
	});
})();