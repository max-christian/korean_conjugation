//////////////////////////////////
//
//    JS_IM_Caret
//        by Colspan (Miyoshi)
//         http://colspan.net/
//
// depend jsim_common.js
/*
==============
based on caret.js var 0.24
 by sonozaki sion
　Webと文字 http://d.hatena.ne.jp/project_the_tower2/
*/


var Caret = {
  version : "20090813",
  author : "Colspan",
	getCaretPos: function (element){
//		element = JS_IM_Common.$(element);
		element.focus();
		if(JS_IM_Common.Browser.IE) {
			var sel=document.selection.createRange();
			var sel_length = sel.text.length;
			var r=element.createTextRange();
			var all=r.text.length;
			r.moveToPoint(sel.offsetLeft,sel.offsetTop);
			r.moveEnd("textedit");
			var end_length=r.text.length;
			var start_length=all-end_length;
			return start_length;
		}else if( JS_IM_Common.Browser.Opera || JS_IM_Common.Browser.Gecko  || JS_IM_Common.Browser.WebKit){
			return element.selectionStart;
		}
	},
	getSelectionPos:function(element){
//		element = JS_IM_Common.$(element);
		element.focus();
		if(JS_IM_Common.Browser.IE) {
			var sel=document.selection.createRange();
			var sel_length = sel.text.length;
			var r=element.createTextRange();
			var all=r.text.length;
			r.moveToPoint(sel.offsetLeft,sel.offsetTop);
			r.moveEnd("textedit");
			var end_length=r.text.length;
			var start_length=all-end_length;
			return new Array(start_length,sel_length);
		}else if( JS_IM_Common.Browser.Opera || JS_IM_Common.Browser.Gecko  || JS_IM_Common.Browser.WebKit){
			return new Array(element.selectionStart,element.selectionEnd - element.selectionStart);
		}
	},
	atachCaretPos:function(element,ln){
//		element = JS_IM_Common.$(element);
		element.focus();
		if(JS_IM_Common.Browser.IE){
			var e=element.createTextRange();
			var tx=element.value.substr(0, ln);
			var pl=tx.split(/\n/);
			e.collapse(true);
			e.moveStart("character",ln-pl.length+1);
			e.text=e.text+"";
			e.collapse(false);
			e.select();
		}else if(JS_IM_Common.Browser.Opera || JS_IM_Common.Browser.Gecko  || JS_IM_Common.Browser.WebKit){
			element.setSelectionRange(ln,ln);
		}
	},
	getSelectionText:function (element){
//		element = JS_IM_Common.$(element);
		element.focus();
		var sel = element.getSelectionPos();
		return element.value.substr(sel[0],sel[1]);
	},
	nowCaretPosPutWord:function(element,word){
//		element = JS_IM_Common.$(element);
		element.focus();
		if(JS_IM_Common.Browser.IE){
			var ieRegion = document.selection.createRange();
			ieRegion.text = word;
			ieRegion.select();
		}else if(JS_IM_Common.Browser.Opera || JS_IM_Common.Browser.Gecko  || JS_IM_Common.Browser.WebKit){
			// 挿入時に、selectionEndを使って後半を結合するように変更
			var str=element.value;
			var selected_range = Caret.getSelectionPos( element );
			var click_s=str.substr(0, selected_range[0]);
			var click_e=str.substr(selected_range[0] + selected_range[1], element.value.length);
			element.value = click_s + word + click_e;
			Caret.atachCaretPos( element, selected_range[0]+word.length);
			/*
			var str=element.value;
			var start_length = element.getCaretPos();
			var click_s=str.substr(0, start_length);
			var click_e=str.substr(start_length, element.value.length);
			element.value = click_s + word + click_e;
			element.atachCaretPos(start_length+word.length);
			*/
		}
	},
	setCaretPosPurWord:function(element,word,pos){
//		element = JS_IM_Common.$(element);
		element.focus();
		var s = element.getCaretPos();
		element.atachCaretPos(pos);
		element.nowCaretPosPutWord(word);
		//element.atachCaretPos(s);
	},
	setSelectionPos:function(element,range){
//		element = JS_IM_Common.$(element);
		element.focus();
		if(JS_IM_Common.Browser.IE){
			var rng = document.selection.createRange();
			if(range>0){
				rng.moveEnd("character", range);
			}else if(range<0){
				rng.moveStart("character", range);
			}
			rng.select();
		}else if(JS_IM_Common.Browser.Opera || JS_IM_Common.Browser.Gecko || JS_IM_Common.Browser.WebKit){
			var pos = element.getCaretPos();
			if(range>0){
				element.setSelectionRange(pos,pos + range);
			}else if(range<0){
				element.setSelectionRange(pos + range,pos);
			}
		}
	},

	getCaretXY:function(element,repaint){
//		element = JS_IM_Common.$(element);
		if(JS_IM_Common.Browser.IE){
			return function(element){
				var xy0 =JS_IM_Common.cumulativeOffset(element);
				element.focus();
				var caretPos = document.selection.createRange();

//				var x = xy0[0] + caretPos.offsetLeft + element.scrollLeft;
//				var y = xy0[1] + caretPos.offsetTop + element.scrollTop;
				var x = caretPos.boundingLeft + document.body.scrollLeft;
				var y = caretPos.boundingTop + document.body.scrollTop;
				return new Array(x,y);
			}
		}else if(JS_IM_Common.Browser.Opera || JS_IM_Common.Browser.Gecko  || JS_IM_Common.Browser.WebKit){
			var elmCursor = document.createElement('span');
			elmCursor.innerHTML = '|';
			return function(element,repaint){
//				element = document.getElementById(element);
				element.focus();

				var elmClone = Caret.__cloning( element, repaint);
				var caretPos = Caret.getCaretPos( element );
				var value = element.value;
				elmClone.innerHTML = '';
				elmClone.appendChild(document.createTextNode(value.substr(0,caretPos)));
				elmClone.appendChild(elmCursor);
				elmClone.appendChild(document.createTextNode(value.substr(caretPos)));



				//////ブラウザ別処理///////
				var xy0 =JS_IM_Common.cumulativeOffset(element);
				if(JS_IM_Common.Browser.Gecko  || JS_IM_Common.Browser.WebKit ||(parseFloat(opera.version()) >= 9.5)){
					var x = xy0.left + elmCursor.offsetLeft  - element.scrollLeft;
					var y = xy0.top + elmCursor.offsetTop  - element.scrollTop;
				}else	if((parseFloat(opera.version()) < 9.5)){
					var x = xy0.left + elmCursor.offsetLeft;
					var y = xy0.top + elmCursor.offsetTop;
				}
				return new Array(x,y);
			}
		}
	}(),
	__cloning:function(element,repaint){
//		element = JS_IM_Common.$(element);
		var elmClone = document.createElement('pre');
		var flag = false;
		var copyProps = [
			'width','height',
			'margin-top','margin-bottom','margin-left','margin-right',
			'padding-left', 'padding-right', 'padding-top', 'padding-bottom', 
			'border-left-style', 'border-right-style','border-top-style','border-bottom-style', 
			'border-left-width', 'border-right-width','border-top-width','border-bottom-width', 
			'font-family','font-size','line-height', 'letter-spacing', 'word-spacing'
		];
		var setElmStyle = function (element){
			for(var i=0;copyProps.length>i;i++){
				elmClone.style[ JS_IM_Common.camelize( copyProps[i] )] = JS_IM_Common.getStyle(element, copyProps[i]);
			}

			elmClone.style.visibility="hidden"; 
			elmClone.style.position = "absolute";
			elmClone.style.textAlign = "left";
			//elmClone.scrollLeft = element.scrollLeft;
			//elmClone.scrollTop = element.scrollTop;
			//ブラウザ別処理

			var dx,dy;
			if(JS_IM_Common.Browser.Gecko){
				dx =0;
				dy = -1;
				elmClone.style.whiteSpace = "-moz-pre-wrap";
			}else if(JS_IM_Common.Browser.Opera){
				elmClone.style.whiteSpace = "-o-pre-wrap";
				dx =2;
				dy = 2;
				if((parseFloat(opera.version())) < 9.5) elmClone.style.lineHeight = "15px";
			}else if(JS_IM_Common.Browser.WebKit){
				elmClone.style.whiteSpace = "pre-wrap";
				dx = 2;
				dy = - 2;
			}else{
				elmClone.style.whiteSpace = "normal";
				dx = dy =0;

			}

			var xy0 =JS_IM_Common.cumulativeOffset(element);
			elmClone.style.left = xy0.left + dx + 'px';
			elmClone.style.top = xy0.top + dy +'px';


		}
		return function(element,repaint){
			if(!flag || repaint) {
				setElmStyle(element);
				document.getElementsByTagName("body").item(0).appendChild(elmClone);
				flag = true;
			}
			return elmClone;
		}
	}(),

/*	getTextWidth:function(element,word){
		var pre1 = new Element('pre');
		var span1 = new Element('span');
		pre1.style.visibility = "hidden";
		return function(element,word){
			element = JS_IM_Common.$(element);
			span1.innerHTML = word;
			pre1.appendChild(span1);
			document.getElementsByTagName("body").item(0).appendChild(pre1);

			return span1.offsetWidth;
		}
	}(),*/

	backSpace : function (textElement){ // 文字列後退
		//IE support
		if (document.selection) {
			textElement.focus();
			sel = document.selection.createRange();
			if( sel.text == "") sel.moveStart("character",-1);
			sel.text = "";
			sel.move("character",0);
			sel.select();
		}else if(textElement.selectionStart || textElement.selectionStart == '0') {
			var startPos = textElement.selectionStart;
			var endPos = textElement.selectionEnd;
			var temp = textElement.value;
			if( startPos != endPos ){
				textElement.value = textElement.value.substring(0, startPos ) + textElement.value.substring(endPos , textElement.value.length);
				textElement.selectionStart = textElement.selectionEnd = startPos -1;
			}else{
				textElement.value = textElement.value.substring(0, startPos - 1) + textElement.value.substring(endPos , textElement.value.length);
				textElement.selectionStart = textElement.selectionEnd = startPos - 1;
			}
		}else{
			textElement.value = textElement.value.substring(0, textElement.value.length-1);
		}
	}
}
