var scrollDelay
var loading = false

function resetPage(){
	history.replaceState({'page': 0, 'more': 1}, null, null)
}

function pageScroll(){
	if(document.documentElement.scrollTop + document.body.scrollTop == 0){
		clearTimeout(scrollDelay)
	}
	else{
		window.scrollBy(0, -70)
		scrollDelay = setTimeout(pageScroll, 10)
	}
}

function restore(){
	var target = 1
	if(history.state != null && history.state.page >= 1){
		target = history.state.page
	}
	resetPage()
	while(history.state.page < target && history.state.more == 1){
		loadMore(false)
	}
}

window.onload = restore
window.onbeforeunload = function(){ 
	if(document.documentElement.scrollTop + window.scrollY == 0){
		resetPage()
	}
}

function loadMore(async){
	
	if(loading == true) return
	else loading = true

	var xhr = new XMLHttpRequest()
	xhr.onreadystatechange = function(){
		if(xhr.readyState == 4){
			history.state.more = 0
			if(xhr.status == 200){
				var jsonBody= JSON.parse(xhr.responseText)
				history.state.page = history.state.page + 1

				if(jsonBody.length < 20){
					history.state.more = 0
					document.getElementById('loading').className = 'nomore'
				}
				else{
					history.state.more = 1
					document.getElementById('loading').className = 'goon'
				}
				jsonBody.forEach(buildCard)
			}
			history.replaceState(history.state, null, null)
			loading = 0
		}
	}

	xhr.open('GET','/api/feed/' + member + '?size=20&page=' + (history.state.page + 1), async)
	xhr.send()

}

function buildCard(item){
	var card = createElement('a', 'card')
	card.href = '/blog/' + item['fid']

	var info = createElement('div', 'info')

	if(member == 'all'){
		var avatar = info.appendChild(createElement('div', 'avatar'))
		avatar.style.backgroundImage = 'url(' + item.author.avatar + ')'
		info.appendChild(createElement('span', 'author',item.author.name))
	}

	info.appendChild(createElement('span', 'post', timeFriendly(item.post)))
	card.appendChild(info)
	card.appendChild(createElement('div', 'title', item.title))
	card.appendChild(createElement('div', 'snippet', item.snippet))
	document.getElementById('content').appendChild(card)
}

function createElement(tagName, className, innerHTML){
	var element = document.createElement(tagName)
	if(className) element.className = className
	if(innerHTML) element.innerHTML = innerHTML 
	return element
}

function fromNow(date){
	var now = new Date()
	var timeDelta = parseInt((Date.now() - date) / 1000)
	if(timeDelta < 2)
		return 'just now'
	else if (timeDelta < 60)
		return parseInt(timeDelta) + 'secs ago'
	else if (timeDelta < 120)
		return '1 min ago'
	else if (timeDelta < 3600)
		return parseInt(timeDelta / 60) + ' mins ago'
	else if (timeDelta < 7200)
		return '1 hour ago'
	else
		return parseInt(timeDelta / 3600) + ' hours ago'
}

function timeFormat(date){
	var year = date.getFullYear().toString()
	var month = (date.getMonth() + 1).toString()
	var day = date.getDate().toString()
	var hour = date.getHours().toString()
	var minute = date.getMinutes()
	minute = (minute < 10) ? '0'+minute.toString() : minute.toString()
	var timeinfo = year + '/' + month + '/' + day + ' ' + hour + ':' + minute
	return timeinfo
}

function timeFriendly(date){
	var post = new Date(date)
	var today = new Date()
	today.setHours(0, 0, 0, 0)
	if (post > today)
		return fromNow(post)
	else
		return timeFormat(post)
}

window.onscroll = function(){
	if (document.body.scrollHeight - 240 < window.scrollY + window.innerHeight && history.state.more == 1){
		loadMore(true)
	}
}


document.getElementById('topbar').onclick = function(){
	pageScroll()
}
if(document.getElementById('member') != null){
	document.getElementById('member').onclick = function(event){
		event.stopPropagation()
		window.location.href = '/group'
	}
}
if(document.getElementById('about') != null){
	document.getElementById('about').onclick = function(event){
		event.stopPropagation()
		window.location.href = '/about'
	}
}
if(document.getElementById('back') != null){
	document.getElementById('back').onclick = function(event){
		event.stopPropagation()
		history.back(-1) | window.close()
	}
}


if('serviceWorker' in navigator){
	navigator.serviceWorker.getRegistration().then(function(worker){
		if(worker) worker.unregister()
	})
}

// if('serviceWorker' in navigator) {
// 	navigator.serviceWorker.register('/sw.js', { scope: '/' }).then(function() {
// 		return navigator.serviceWorker.ready
// 	}).then(function(registration) {
// 		console.log('service worker ready')
// 		subscrible(registration)
// 	})
// }

// function setflag(){
// 	var date = new Date()
// 	var timestamp = date.getTime()
// 	date.setDate(date.getDate() + 1)
// 	document.cookie = 'LAST_SUBSCRIBE=' +escape(timestamp)+';expires='+date.toGMTString()
// }


// function checkflag(){
// 	var start_index = document.cookie.indexOf('LAST_SUBSCRIBE=')
// 	if (start_index == -1){return 0}
// 	var last_subscribe = unescape(document.cookie.substring(start_index + 15,start_index + 28))
// 	var date = new Date()
// 	var timestamp = date.getTime()
// 	// date.setTime(last_subscribe)
// 	// console.log(date)
// 	if ((timestamp - last_subscribe)< 1000 * 60 * 30){return 1}
// 	else{return 0}
// }


// function subscrible(registration){
// 	if(window.Notification && Notification.permission !== 'denied') {
// 		Notification.requestPermission(function(status) {
// 			if(status === 'granted') {
// 				registration.pushManager.getSubscription().then(function(subscribed) {
// 					registration.pushManager.subscribe({userVisibleOnly: true}).then(function(subscription) {
// 						var endpointSections = subscription.endpoint.split('/')
// 						var subscriptionId = endpointSections[endpointSections.length - 1]
// 						// console.log('subscriptionId:', subscriptionId)
// 						if (checkflag()==0||subscribed==null){
// 							fetch('/push/sub',
// 							{
// 								method: 'POST',
// 								credentials: 'include',
// 								headers: {'Content-Type': 'application/x-www-form-urlencoded'},
// 								body: 'subscriptionId=' + subscriptionId
// 							}).then(function(response) {
// 								if (response.ok) {
// 									console.log('server received')
// 									setflag()
// 									if (subscribed==null){return registration.showNotification('成功订阅推送服务', {body:'接收推送消息不一定要翻墙哦',icon:'/static/logo/144.png',badge:'/static/logo/badge.png'})}
// 								}
// 								else {console.log('server received failed');}
// 							})
// 						}
// 					}).catch(function(error) {
// 							console.log(error)
// 					})

// 				})
// 			}
// 		})
// 	}
// }


