var scrollDelay
buildText(0)
buildText(1)

if(history.state != null && history.state.view == 'cn')
	focus(1)
else
	focus(0)

function focus(type){
	var textJP = document.getElementsByClassName('text')[0]
	var textCN = document.getElementsByClassName('text')[1]
	if(type == 0){
		textJP.className = 'text focus'
		textCN.className = 'text unfocus'
		history.replaceState({'view': 'jp'}, null, null)
	}
	else if(type == 1){
		textJP.className = 'text unfocus'
		textCN.className = 'text focus'
		history.replaceState({'view': 'cn'}, null, null)
	}	
}

function viewSwitch(){
	var textJP = document.getElementsByClassName('text')[0]
	var textCN = document.getElementsByClassName('text')[1]
	if(textCN.className == 'text unfocus')
		focus(1)
	else if(textJP.className == 'text unfocus')
		focus(0)
}


function render(text){
	var article = document.createDocumentFragment()
	text = text.split('\n')
	var detector = /\!\[[^\]]*\]\([^\)]+\)/g
	text.forEach(function(line){
		if(line == ''){
			var paragraph = article.appendChild(document.createElement('p'))
			paragraph.appendChild(document.createElement('br'))
		}
		else if(!detector.test(line)){
			var paragraph = article.appendChild(document.createElement('p'))
			paragraph.innerHTML = line
		}
		else{
			var images = line.match(detector)
			var parts = line.split(detector)
			var paragraph = document.createElement('p')
			parts.slice(0, -1).forEach(function(part, index){
				paragraph.innerHTML += part
				var source = images[index].match(/\(([^\)]+)\)/)[1]
				var size = images[index].match(/\[([^\]]*)\]/)[1].split('x')
				// if(size[0] >= 500 || size[1] >= 500){
				if(size[0] >= 200){
					article.appendChild(paragraph)
					var image = article.appendChild(document.createElement('img'))
					image.src = source
					image.className = 'wide'
					paragraph = document.createElement('p')
				}
				else{
					var image = paragraph.appendChild(document.createElement('img'))
					image.src = source
				}
			})
			paragraph.innerHTML += parts.slice(-1)
			if (paragraph.innerHTML != ''){
				article.appendChild(paragraph)
			}
		}
	})
	return article
}

function timeFriendly(type){
	var post = new Date(shareData['post'])

	var month = post.getMonth() + 1
	var day = post.getDate()
	var hour = post.getHours()
	var minute = post.getMinutes()
	month = (month < 10) ? '0'+month.toString() : month.toString()
	day = (day < 10) ? '0'+day.toString() : day.toString()
	hour = (hour < 10) ? '0'+hour.toString() : hour.toString()
	minute = (minute < 10) ? '0'+minute.toString() : minute.toString()
	
	var time = hour + ':' + minute
	var date = month + '/' + day + ' ' + time

	var today = new Date()
	today.setHours(0, 0, 0, 0)
	var yesterday = new Date(today.getTime() - 86400 * 1000)

	if(post < yesterday){
		return date
	}
	else if(post < today){
		if (type == 0)
			return '昨日 ' + time
		else if (type == 1)
			return '昨天 ' + time
	}
	else{
		if (type == 0)
			return '今日 ' + time
		else if (type == 1)
			return '今天 ' + time
	}
}

function groupName(){
	return ['NOGI', 'KEYAKI', 'HINATA'][shareData.author.mid[0]]
}

function createElement(tagName, className, innerHTML){
	var element = document.createElement(tagName)
	if(className) element.className = className
	if(innerHTML) element.innerHTML = innerHTML 
	return element
}

function buildText(type){

	var header = createElement('header', 'header')
	var avatar = header.appendChild(createElement('div', 'avatar'))
	avatar.style.backgroundImage = 'url(' + shareData.author.avatar + ')'
	
	header.appendChild(createElement('div', 'title', shareData.title[type]))
	header.appendChild(createElement('div', 'info', shareData.author.name + ' · ' + groupName()+ ' · ' + timeFriendly(type)))
	header.appendChild(createElement('div', 'separator', '————    ~    ————'))

	var text = createElement('div', 'text unfocus')
	text.appendChild(header)
	var article = text.appendChild(createElement('article', 'article'))
	article.appendChild(render(shareData.article[type]))
	text.appendChild(createElement('footer', 'footer'))
	
	document.body.appendChild(text)

}

function pageScroll(){
	if(document.documentElement.scrollTop + document.body.scrollTop == 0){
		clearTimeout(scrollDelay)
	}
	else{
		window.scrollBy(0, -50)
		scrollDelay = setTimeout(pageScroll, 10)
	}
}

document.getElementById('topbar').onclick = function(){
	pageScroll()
}
document.getElementById('back').onclick = function(event){
	event.stopPropagation()
	history.back(-1) | window.close()
}
document.getElementById('link').onclick = function(event){
	event.stopPropagation()
	window.location.href = shareData['link']
}

document.getElementById('translate').onclick = function(even){
	event.stopPropagation()
	if(shareData.article[1] != '') viewSwitch()
}


