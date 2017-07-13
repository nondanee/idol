var scrolldelay;
function viewSwitch(){
	var text_cn = document.getElementById("zh-cn")
	var text_jp = document.getElementById("ja-jp")
	if(text_cn.getAttribute("class") == "text unfocus"){
		text_cn.setAttribute("class","text focus")
		text_jp.setAttribute("class","text unfocus")
		history.replaceState({"view":"cn"}, null, null);
	}
	else{
		text_cn.setAttribute("class","text unfocus")
		text_jp.setAttribute("class","text focus")
		history.replaceState({"view":"jp"}, null, null);
	}
};
function statusCheck() {
	if(history.state!=null){
		if(history.state.view=="jp"){
			document.getElementById("zh-cn").setAttribute("class","text unfocus")
			document.getElementById("ja-jp").setAttribute("class","text focus")
		}
		else if(history.state.view="cn"){
			document.getElementById("zh-cn").setAttribute("class","text focus")
			document.getElementById("ja-jp").setAttribute("class","text unfocus")
		}
	}
	else{
		history.replaceState({"view":"jp"}, null, null);
	}
}
function pageScroll(){
	if(document.documentElement.scrollTop+document.body.scrollTop==0){
		clearTimeout(scrolldelay);
	}
	else{
		window.scrollBy(0,-50);
		scrolldelay=setTimeout('pageScroll()',10);
	}
}
function docReady(cb) {
	if (document.readyState != 'loading') {cb();} 
	else {document.addEventListener('DOMContentLoaded', cb);}
}
docReady(statusCheck);