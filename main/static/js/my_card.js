$(function(){

    $(".myblog-card").each(function(i, el)
		{
			var $el          	= $(el),
				$nav            = $el.find('.my-nav a'),
				$status_list    = $el.find('.xe-comment p'),
				index           = $status_list.filter('.post_show').index(),
				auto_switch     = attrDefault($el, 'auto-switch', 3),
				as_interval		= 0;
				
			if(auto_switch > 0)
			{
				as_interval = setInterval(function()
				{
					goTo(1);
					
				}, auto_switch * 1000);
				
				$el.hover(function()
				{
					window.clearInterval(as_interval);
				},
				function()
				{
					as_interval = setInterval(function()
					{
						goTo(1);
						
					}, auto_switch * 1000);;
				});
			}
			
			function goTo(plus_one)
			{
				index = (index + plus_one) % $status_list.length;
				
				if(index < 0)
					index = $status_list.length - 1;
				
				var $to_hide = $status_list.filter('.post_show'),
					$to_show = $status_list.eq(index);
				
                $to_hide.removeClass('post_show');
                $to_hide.css('display','none')
                $to_show.addClass('post_show').fadeTo(0,0).fadeTo(320,1);
                $to_show.css('display','block')
			}
			
			$nav.on('click', function(ev)
			{
				ev.preventDefault();
				
				var plus_one = $(this).hasClass('xe-prev') ? -1 : 1;
				
				goTo(plus_one);
			});
		});
})