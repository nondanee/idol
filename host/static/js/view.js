const createElement = (tagName, className, innerHTML) => {
	let element = document.createElement(tagName)
	if(className) element.className = className
	if(innerHTML) element.innerHTML = innerHTML
	return element
}

const parse = text => {
	let article = document.createDocumentFragment()
	text = text.split('\n')
	const detector = /\!\[[^\]]*\]\([^\)]+\)/g
	text.forEach(line => {
		if(line == ''){
			let paragraph = article.appendChild(createElement('p'))
			paragraph.appendChild(createElement('br'))
		}
		else if(!detector.test(line)){
			let paragraph = article.appendChild(createElement('p'))
			paragraph.innerHTML = line
		}
		else{
			let images = line.match(detector)
			let parts = line.split(detector)
			let paragraph = createElement('p')
			parts.slice(0, -1).forEach((part, index) => {
				paragraph.innerHTML += part
				let source = images[index].match(/\(([^\)]+)\)/)[1]
				let size = images[index].match(/\[([^\]]*)\]/)[1].split('x')
				// if(size[0] >= 500 || size[1] >= 500){
				if(size[0] >= 200){
					article.appendChild(paragraph)
					let image = article.appendChild(createElement('img'))
					image.src = source
					image.className = 'wide'
					paragraph = createElement('p')
				}
				else{
					let image = paragraph.appendChild(createElement('img'))
					image.src = source
				}
			})
			paragraph.innerHTML += parts.slice(-1)
			if(paragraph.innerHTML != ''){
				article.appendChild(paragraph)
			}
		}
	})
	return article
}

const timeFormat = type => {
	const stringify = number => ('0' + number).slice(-2)
	let post = new Date(shareData.post)
	
	let time = stringify(post.getHours()) + ':' + stringify(post.getMinutes())
	let date = stringify(post.getMonth() + 1) + '/' + stringify(post.getDate()) + ' ' + time

	let today = new Date()
	today.setHours(0, 0, 0, 0)
	let yesterday = new Date(today.getTime() - 86400 * 1000)

	if(post < yesterday)
		return date
	else if(post < today)
		return (type == 0 ? '昨日' : '昨天') + ' ' + time
	else
		return (type == 0 ? '今日' : '今天') + ' ' + time
}

const render = type => {
	let header = createElement('header', 'header')
	let avatar = header.appendChild(createElement('div', 'avatar'))
	avatar.style.backgroundImage = 'url(' + shareData.author.avatar + ')'
	
	header.appendChild(createElement('div', 'title', shareData.title[type]))
	header.appendChild(createElement('div', 'info', shareData.author.name + ' · ' + ['NOGI', 'KEYAKI', 'HINATA'][shareData.author.mid[0]] + ' · ' + timeFormat(type)))
	header.appendChild(createElement('div', 'separator', '————    ~    ————'))

	let text = createElement('div', 'text unfocus')
	text.appendChild(header)
	let article = text.appendChild(createElement('article', 'article'))
	article.appendChild(parse(shareData.article[type]))
	text.appendChild(createElement('footer', 'footer'))
	
	document.body.appendChild(text)
}

let scrollDelay
const scrollTop = () => {
	if(document.documentElement.scrollTop + document.body.scrollTop == 0){
		clearTimeout(scrollDelay)
	}
	else{
		window.scrollBy(0, -50)
		scrollDelay = setTimeout(scrollTop, 10)
	}
}

const focus = type =>
	Array.from(document.getElementsByClassName('text')).forEach((element, index) => {
		element.className = 'text' + ' ' + (index === type ? 'focus' : 'unfocus')
		history.replaceState({view: ['jp', 'cn'][type]}, null, null)
	})

const turn = () => {
	let elements = Array.from(document.getElementsByClassName('text'))
	focus((elements.findIndex(element => element.classList.contains('focus')) + 1) % elements.length)
}

document.getElementById('topbar').onclick = scrollTop
document.getElementById('back').onclick = event => {
	event.stopPropagation()
	history.back(-1) | window.close()
}
document.getElementById('link').onclick = event => {
	event.stopPropagation()
	window.location.href = shareData.link
}
document.getElementById('translate').onclick = event => {
	event.stopPropagation()
	if(shareData.article[1] != '') turn()
}

render(0)
render(1)
focus((history.state != null && history.state.view == 'cn') ? 1 : 0)