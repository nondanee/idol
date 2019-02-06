'use strict'

var avaterCache = "portrait_20180601"
var staticCache = "static_78"

self.addEventListener('install', function(event){
	console.log("[Service Worker] install")
	event.waitUntil(self.skipWaiting())
})

self.addEventListener('activate', function(event){
	console.log('[Service Worker] activate')
	event.waitUntil(
		caches.keys().then(function(keys){
			return Promise.all(keys.map(function(key){
				// if (key !== "dynamic" && key !== avaterCache && key !== staticCache){
				// if (key !== avaterCache && key !== staticCache){
					// console.log('[ServiceWorker] removing old cache', key) 
					return caches.delete(key)
				// }
			}))
		})
	)
})


self.addEventListener('fetch', function(event){
	// console.log(event.request.url)
	var requestURL = new URL(event.request.url)

	// Routing for local URLs
	if (requestURL.origin == location.origin){
		// Handle article URLs
		// if (/^\/$/.test(requestURL.pathname)){
		//	 event.respondWith(
		//		 caches.open('dynamic').then(function(cache){
		//			 return cache.match(event.request).then(function(fromcache){
		//				 return fetch(event.request).then(function(latest){
		//					 cache.put(event.request, latest.clone())
		//					 return latest
		//				 }).catch(function(error){
		//						// console.log(error)
		//						return fromcache
		//				 })
		//				 // var fetchPromise = fetch(event.request).then(function(networkResponse){
		//				 //	 cache.put(event.request, networkResponse.clone())
		//				 //	 return networkResponse
		//				 // })
		//				 // return response || fetchPromise
		//			 })
		//		 })
		//	 )
		// }

		// if (/^\/$/.test(requestURL.pathname)){
		// 	event.respondWith(
		// 		caches.open(staticCache).then(function(cache){
		// 			return cache.match(event.request).then(function (response){
		// 				return response || fetch(event.request).then(function(response){
		// 					cache.put(event.request, response.clone())
		// 					console.log("static file update")
		// 					return response
		// 				})
		// 			})
		// 		})
		// 	)
		// }

		if (/\/static\//.test(requestURL.pathname)){
			event.respondWith(
				caches.open(staticCache).then(function(cache){
					return cache.match(event.request).then(function (response){
						return response || fetch(event.request).then(function(response){
							cache.put(event.request, response.clone())
							console.log("static file update")
							return response
						})
					})
				})
			)
		}

		if (/^\/avatar\//.test(requestURL.pathname)){
			event.respondWith(
				caches.open(avaterCache).then(function(cache){
					return cache.match(event.request).then(function (response){
						return response || fetch(event.request).then(function(response){
							cache.put(event.request, response.clone())
							console.log("avatar update")
							return response
						})
					})
				})
			)
		}

		// if (/\.webp$/.test(requestURL.pathname)){
		//	 event.respondWith(/* some other combination of patterns */)
		//	 return
		// }
	}


})

// self.addEventListener('push', function(event){
// 	// console.log("[Service Worker] update test")
// 	console.log('[Service Worker] push received')
// 	const pushInfoPromise = fetch("/push/get",{credentials:'include'}).then(function(res){
// 			return res.json()
// 			}).then(function(data){
// 					var promises = []
// 					//for (var i = 0i < data.lengthi++){
// 					for (var i = data.length-1; i > -1; i--){
// 						promises.push(self.registration.showNotification(data[i]["title"], {data:data[i]["data"],icon:data[i]["icon"],body:data[i]["body"],badge:'/static/logo/badge.png'}))
// 					}
// 					return Promise.all(promises)
// 			}).catch(function(error){
// 			 console.log(error)
// 		})
// 	event.waitUntil(pushInfoPromise)
// })


// self.addEventListener('notificationclick', function(event){
// 		event.notification.close()
// 		if(event.notification.data != null)
// 			event.waitUntil(clients.openWindow(event.notification.data))
// })

// self.addEventListener('pushsubscriptionchange',function(){
// 	self.registration.pushManager.getSubscription()
// 		.then(function (subscription){
// 				if (!subscription){
// 				} else {
// 						subscription.unsubscribe().then(function (){
// 								self.registration.pushManager.subscribe({ userVisibleOnly: true })
// 										.then(function (subscription){
// 												var endpointSections = subscription.endpoint.split('/')
// 												var subscriptionId = endpointSections[endpointSections.length - 1]
// 												fetch("/push/sub",
// 												{
// 														method: "POST",
// 														credentials: 'include',
// 														headers: {'Content-Type': 'application/x-www-form-urlencoded'},
// 														body: "subscriptionId=" + subscriptionId
// 												})
// 										})
// 						})
// 					}
// 		})
// })
