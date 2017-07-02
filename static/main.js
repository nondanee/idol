var scrolldelay;

$(document).ready(
function (){
	if(history.state!=null){
		var target = history.state.page
		history.state.more = 1
		history.state.page = 1
		history.replaceState(history.state, null, null);
		while(history.state.page < target&&history.state.more==1)
		{
			$.ajax({
				url:"?page=" + (history.state.page + 1),
				type:"get",
				data: false,
				async: false,
				processData:false,
				contentType:false,
				success:function(jsonback){
					history.state.page = history.state.page + 1
					history.state.more = jsonback.more
					history.replaceState(history.state, null, null);
					$("#content").append(jsonback.content);
					if(jsonback.more==0){$("#loading").css("display","none")}
				}
			});
		}
	}
	else{
		var state = {}
		state.page = 1
		state.more = 1
		history.replaceState(state, null, null);
	}

	if(navigator.userAgent.match("iPhone")!=null)
	{
		document.getElementById("app").style.top="0px";
	}
});


$(window).scroll(function()
{
	if ($("html").height()==$(window).scrollTop()+$(window).height()&&history.state.more==1) {

		$.ajax({
			url:"?page=" + (history.state.page + 1),
			type:"get",
			data: false,
			async: false,
			processData:false,
			contentType:false,
			success:function(jsonback){
				history.state.page = history.state.page + 1
				history.state.more = jsonback.more
				history.replaceState(history.state, null, null);
				$("#content").append(jsonback.content);
				if(jsonback.more==0){$("#loading").css("display","none")}
			}
		});
	}  
});

function pageScroll(){
	if(document.documentElement.scrollTop+document.body.scrollTop==0){
		clearTimeout(scrolldelay);
	}
	else{
		window.scrollBy(0,-70);
		scrolldelay=setTimeout('pageScroll()',10);
	}
}

function Refresh(){
	if($(window).scrollTop()==0)
	{
		history.replaceState(null, null, null);
		location.replace(location.origin);
	}
}