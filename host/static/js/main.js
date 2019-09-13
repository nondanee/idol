const createElement = (tagName, className, innerHTML) => {
	let element = document.createElement(tagName)
	if(className) element.className = className
	if(innerHTML) element.innerHTML = innerHTML
	return element
}

let scrollDelay
const scrollTop = () => {
	if(document.documentElement.scrollTop + document.body.scrollTop == 0){
		clearTimeout(scrollDelay)
	}
	else{
		window.scrollBy(0, -70)
		scrollDelay = setTimeout(scrollTop, 10)
	}
}

let loading = false
const loadMore = async => {
	if(loading == true) return
	else loading = true

	const xhr = new XMLHttpRequest()
	xhr.onreadystatechange = () => {
		if(xhr.readyState == 4){
			history.state.more = false
			if(xhr.status == 200){
				let jsonBody= JSON.parse(xhr.responseText)
				history.state.page += 1
				history.state.more = jsonBody.length === 20
				document.getElementById('loading').className = history.state.more ? 'goon' : 'nomore'
				jsonBody.forEach(cardify)
			}
			history.replaceState(history.state, null, null)
			loading = 0
		}
	}

	xhr.open('GET', `/api/v3/feed/${member}?size=20&page=${history.state.page + 1}`, async)
	xhr.send()
}

const cardify = item => {
	let card = createElement('a', 'card')
	card.href = '/blog/' + item.fid

	let info = createElement('div', 'info')

	if(member == 'all'){
		let avatar = info.appendChild(createElement('div', 'avatar'))
		avatar.style.backgroundImage = 'url(' + item.author.avatar + ')'
		info.appendChild(createElement('span', 'author', item.author.name))
	}

	info.appendChild(createElement('span', 'post', timeFormat(item.post)))
	card.appendChild(info)
	card.appendChild(createElement('div', 'title', item.title))
	card.appendChild(createElement('div', 'snippet', item.snippet))
	document.getElementById('content').appendChild(card)
}


const timeFormat = date => {
	let post = new Date(date)
	let today = new Date()
	today.setHours(0, 0, 0, 0)

	const interval = date => {
		let delta = parseInt((Date.now() - date) / 1000)
		if(delta < 2)
			return 'just now'
		else if (delta < 60)
			return parseInt(delta) + 'secs ago'
		else if (delta < 120)
			return '1 min ago'
		else if (delta < 3600)
			return parseInt(delta / 60) + ' mins ago'
		else if (delta < 7200)
			return '1 hour ago'
		else
			return parseInt(delta / 3600) + ' hours ago'
	}

	const time = date => {
		const stringify = number => ('0' + number).slice(-2)
		return date.getFullYear() + '/' + (date.getMonth() + 1) + '/' + date.getDate() + ' ' + date.getHours() + ':' + stringify(date.getMinutes())
	}

	return post > today ? interval(post) : time(post)
}

window.onscroll = () => {
	if (document.body.scrollHeight - 240 < window.scrollY + window.innerHeight && history.state.more == 1){
		loadMore(true)
	}
}

document.getElementById('topbar').onclick = scrollTop
if(document.getElementById('member')){
	document.getElementById('member').onclick = event => {
		event.stopPropagation()
		window.location.href = '/group'
	}
}
if(document.getElementById('about')){
	document.getElementById('about').onclick = event => {
		event.stopPropagation()
		window.location.href = '/about'
	}
}
if(document.getElementById('back')){
	document.getElementById('back').onclick = event => {
		event.stopPropagation()
		history.back(-1) | window.close()
	}
}

window.onload = () => {
	let target = (history.state || {}).page >= 1 ? history.state.page : 1
	history.replaceState({page: 0, more: true}, null, null)
	while(history.state.page < target && history.state.more){
		loadMore(false)
	}
}
window.onbeforeunload = () => {
	if(document.documentElement.scrollTop + window.scrollY == 0) history.replaceState(null, null, null)
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
// 	let date = new Date()
// 	let timestamp = date.getTime()
// 	date.setDate(date.getDate() + 1)
// 	document.cookie = 'LAST_SUBSCRIBE=' +escape(timestamp)+';expires='+date.toGMTString()
// }


// function checkflag(){
// 	let start_index = document.cookie.indexOf('LAST_SUBSCRIBE=')
// 	if (start_index == -1){return 0}
// 	let last_subscribe = unescape(document.cookie.substring(start_index + 15,start_index + 28))
// 	let date = new Date()
// 	let timestamp = date.getTime()
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
// 						let endpointSections = subscription.endpoint.split('/')
// 						let subscriptionId = endpointSections[endpointSections.length - 1]
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


