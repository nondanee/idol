var scrolldelay;

moment.relativeTimeThreshold('s', 60);
moment.relativeTimeThreshold('m', 60);
moment.relativeTimeThreshold('h', 24);
moment.locale('en', {
	relativeTime : {
		future: "in %s",
		past:   "%s ago",
		s:  "secs",
		m:  "1 min",
		mm: "%d mins",
		h:  "1 hour",
		hh: "%d hours",
		d:  "a day",
		dd: "%d days",
		M:  "a month",
		MM: "%d months",
		y:  "a year",
		yy: "%d years"
	}
});

function runfirst(){
	if(history.state!=null){
		var target = history.state.page
		history.state.more = 1
		history.state.page = 1
		history.replaceState(history.state, null, null);
		while(history.state.page < target&&history.state.more==1){
			loadmore()
		}
	}
	else{
		history.replaceState({"page":1,"more":1}, null, null);
	}
	timefriendly()
};


window.addEventListener("scroll", function() {
	if (document.body.scrollHeight - 120 < document.body.scrollTop+window.screen.height&&history.state.more==1) {
		loadmore()
	}
});

function pagescroll(){
	if(document.documentElement.scrollTop+document.body.scrollTop==0){
		clearTimeout(scrolldelay);
	}
	else{
		window.scrollBy(0,-70);
		scrolldelay=setTimeout('pagescroll()',10);
	}
}

function timefriendly(){
	var allposts = document.getElementsByClassName("post")
	var today = moment(0, "HH")
	for (var i=0; i<allposts.length; i++){
		var post = moment(allposts[i].getAttribute("data-post"))
		if (post.isBefore(today))
			var timeinfo = post.format('YYYY/M/D H:mm')
		else
			var timeinfo = post.fromNow()
		allposts[i].innerHTML = timeinfo
	}
}


function loadmore(){
	var xhr = new XMLHttpRequest();
	xhr.open('GET',"?page="+(history.state.page + 1),false);
	xhr.send();
	var jsonback = JSON.parse(xhr.responseText)
	history.state.page = history.state.page + 1
	history.state.more = jsonback.more
	history.replaceState(history.state, null, null);
	document.getElementById("content").innerHTML += jsonback.content;
	if(jsonback.more==0){document.body.removeChild(document.getElementById("loading"))}
	timefriendly()

	// fetch("?page="+(history.state.page + 1),{credentials: 'include'}).then(function(response) {
	// 	return response.json()}).then(function(jsonback){
	// 		history.state.page = history.state.page + 1
	// 		history.state.more = jsonback.more
	// 		history.replaceState(history.state, null, null);
	// 		document.getElementById("content").innerHTML += jsonback.content;
	// 		if(jsonback.more==0){document.body.removeChild(document.getElementById("loading"))}
	// 		timefriendly()
	// 	}).catch(function(error) {
	// 	console.log(error);
	// })
}

function docready(cb) {
	if (document.readyState != 'loading') {cb();} 
	else {document.addEventListener('DOMContentLoaded', cb);}
}

docready(runfirst);

if('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js', { scope: '/' }).then(function() {
      return navigator.serviceWorker.ready;
    }).then(function(registration) {
      if(window.Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function(status) {
          if(status === 'granted') {
            registration.pushManager.getSubscription().then(function(subscribed) {
              registration.pushManager.subscribe({userVisibleOnly: true}).then(function(subscription) {
              var endpointSections = subscription.endpoint.split('/');
              var subscriptionId = endpointSections[endpointSections.length - 1];
              console.log('subscriptionId:', subscriptionId);
              fetch("/push/sub",
              {
                  method: "POST",
                  credentials: 'include',
                  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                  body: "subscriptionId=" + subscriptionId
              }).then(function(response) {
                  if (response.ok) {
                    console.log("server received");
                    if (!subscribed){return registration.showNotification('成功订阅推送服务', {body:'接收推送消息不一定要翻墙哦',icon:'/static/logo/144.png'});}
                  }
                  else {console.log("server received failed");}
              });
              }).catch(function(error) {
                console.log(error);
              })
            })
          }
        });
      }
    });
  navigator.serviceWorker.ready.then(function(registration) {
    console.log('service worker ready');
  });
}