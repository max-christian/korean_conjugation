//////////////////////////////////
//
//    JS IM Library
//        by Colspan (Miyoshi)
//         http://colspan.net/
//        License : MIT license
//
// depend jsim_common.js,jsim_keycode.js,jsim_caret.js


function JS_IM_setClassName( targetElement, className ){
  targetElement.className = className;
  if( targetElement.setAttribute ) targetElement.setAttribute( "class", className );
}

var JS_IM = Class.create();
JS_IM.prototype = {
  version : "20090813",
  author : "Colspan",
  isEnabled : false,// 有効か無効か
  methodObj : null,// JS_IM_Methodの形式のIMオブジェクト
  imeBox : null,// 乗っ取るelement( textarea or input )
  workingPhase : null,// 動作フェーズ
  inlineInputting : false,// インライン入力を有効にするか
  initialize : function(formObj,methodObj){
    var _this = this;
    this.imeBox = formObj;
    this.methodObj = new JS_IM_Method( methodObj );
    this.methodObj.JS_IM_Obj = this;
    var keyProcess = function(e){
      if( !JS_IM_Common.Browser.IE && !event ) var event = e;
      var status = _this.process( event );
      return !status;
    }

    this.imeBox.onblur = this.imeBox.onmousedown = function(){
      if( _this.isEnabled ) _this.accept();
    }

    ///// キー入力関連イベント取得 /////
    /*
      ** 連打対策 **
      Windows環境ではonkeydownによって長押しによる連打が可能
      Linux版Firefoxではonkeypressによって長押しによる連打が可能
    */
    if( JS_IM_Common.Browser.IE || JS_IM_Common.Browser.WebKit ){
        this.imeBox.onkeydown = keyProcess;
    }
    else if( JS_IM_Common.Browser.Gecko ){ // Gecko
        this.imeBox.onkeypress = keyProcess;
    }

    this.imeBox.onkeyup = function(e){ // Firefox on Linuxにおける問題を解決
      if( _this.isEnabled ) return false;
      return true;
    }

    // GUI 初期化

//    if( this.methodObj.params.listBox || ! this.methodObj.params.inlineInsertion ){
      this.GUI = new JS_IM_GUI( this );
//    }

    this.GUI.stateDisplay.init();
    if( this.methodObj.params.listBox ){
      this.GUI.list.init();
    }
    if( this.methodObj.params.inlineInsertion ){
      // do nothing
    }
    else{
      this.GUI.buffer.init();
    }

    // 起動
    this.enable();

  },
  selectAll : function(){
    this.imeAccept();
    this.imeBox.focus();
    this.imeBox.select();
  },
  clear : function(){
    this.combiningStr = ""
    this.imeBox.focus();
    this.imeBox.value = "";
  },
  enable : function(){
    this.isEnabled = true;
    this.combiningStr = "";
//    this.originalBackgroundColor = this.imeBox.style.background;
//   this.imeBox.style.background = "#FFF0F0";
    this.GUI.stateDisplay.show();
    this.imeBox.focus();
  },
  disable : function(){
    this.isEnabled = false;
    this.combiningStr = "";
//    this.imeBox.style.background = this.originalBackgroundColor;
    this.GUI.stateDisplay.hide();
    this.imeBox.focus();
  },
  // On Offを切り替える
  toggle : function (){
    if( this.isEnabled ) this.disable();
    else this.enable();
  },
  // 処理文字列を確定する
  accept :  function(){
    if( ! this.isEnabled ) return;
    if( this.methodObj.inlineBuffer != "" ){
      if( this.methodObj.params.inlineInsertion ) for( i=0; i<this.methodObj.inlineBuffer.length; i++ ) Caret.backSpace( this.imeBox );
      var outputStr = this.methodObj.accept();
      Caret.nowCaretPosPutWord( this.imeBox, outputStr );
    }
  },
  ///// IME処理関数 process /////
  /*
    返り値 : boolean
      IME処理を行った場合 : true
      IME処理を行わなかった場合 : false
  */
  process : function (e){

    // 起動制御
    if( this.methodObj == null ) return false; // methodが指定されていないとき

    // Methodに渡すキー情報オブジェクト
    var keyStatus = keyCode.getKeyStatus( e );

    // キーコードによる制御
    if( keyStatus.keyCode == 8 ){ // BackSpace
      return this.backspace();
    }
    else if( keyStatus.keyCode == 16 || keyStatus.keyCode == 17 ){ // Shift || Ctrl
      return false;
    }
    else if( keyStatus.keyCode == 224 ){ // Meta
      this.accept();
      return false;
    }
    else if( keyStatus.ctrlKey || keyStatus.altKey || keyStatus.metaKey ){ // 特殊キーが押されているとき
      if( keyCode.isAlphabet( keyStatus.inputCode ) ){
        //特殊キーと文字キーの組み合わせでは確定
        this.accept();
        return false;
      }
    }
    else if( keyStatus.inputCode == 32 && keyStatus.shiftKey ){ // Shift + Space なら toggle する
      this.accept();
      this.toggle();
      return true;
    }

    if( ! this.isEnabled ) return false;  // IMEが無効になっている場合

    // インライン入力 + 結合処理
    var lastInlineBufferLength = this.methodObj.inlineBuffer.length; // 結合前の文字数を記憶
    var outputStr = this.methodObj.process( keyStatus ); // 結合処理
    if( outputStr != null ){ // JS_IM_Methodから確定文字(空文字を含む)が返された
      if( this.methodObj.params.inlineInsertion ) for( i=0; i<lastInlineBufferLength; i++ ) Caret.backSpace( this.imeBox ); // テキストボックスからインライン文字列を取り除く
      Caret.nowCaretPosPutWord( this.imeBox, outputStr ); // テキストボックスに確定文字を挿入
      if( this.methodObj.params.inlineInsertion ) Caret.nowCaretPosPutWord( this.imeBox, this.methodObj.inlineBuffer ); // テキストボックスにインライン文字列を挿入
//      else this.GUI.buffer.update( this.methodObj.inlineBuffer );
      return true;
    }
    else{ // バッファ内容を確定
      this.accept();
      return false;
    }

  },
  backspace : function(){ // 後退処理
    // 起動制御
    if( this.methodObj == null ) return false; // methodが指定されていないとき
    if( !this.isEnabled ) return false;  // IMEが無効になっている場合

    var lastInlineBufferLength = this.methodObj.inlineBuffer.length;
    var returnValue = this.methodObj.backspace();
    if( this.methodObj.params.inlineInsertion ){
      for( i=0; i<lastInlineBufferLength; i++ ) Caret.backSpace( this.imeBox ); // テキストボックスからインライン文字列を取り除く
      Caret.nowCaretPosPutWord( this.imeBox, this.methodObj.inlineBuffer );//テキストボックスに挿入
    }
    return returnValue;
  }

}


var JS_IM_GUI = Class.create();
JS_IM_GUI.prototype = {
  version : "20081020",
  author : "Colspan",
  JS_IM_Obj : null,
  initialize : function( JS_IM_Obj ){
    this.stateDisplay = JS_IM_Common.cloneObj( JS_IM_GUI.prototype.stateDisplay );
    this.stateDisplay.JS_IM_Obj = this.buffer.JS_IM_Obj = this.list.JS_IM_Obj = this.JS_IM_Obj = JS_IM_Obj;
    this.stateDisplay.parentObj = this.buffer.parentObj = this.list.parentObj = this;
  },
    stateDisplay : {
      elem : null,
      elemId : null,
      init : function(){
        var imeBox = this.JS_IM_Obj.imeBox;
        var offset = JS_IM_Common.cumulativeOffset( imeBox );
        var stateDisplayElem = document.createElement( "div" );
        stateDisplayElem.style.fontSize = '12px';
        stateDisplayElem.style.textAlign = 'center';
        stateDisplayElem.style.width = '20px';
        stateDisplayElem.style.height = '20px';
        stateDisplayElem.style.border = 'solid 1px #000';
        stateDisplayElem.style.background = "#FFC";
        stateDisplayElem.style.position = 'absolute';
        stateDisplayElem.style.top = offset.top  + imeBox.offsetHeight - 20 + 'px';
        stateDisplayElem.style.left = offset.left + imeBox.offsetWidth - 20 + 'px';
        stateDisplayElem.style.visibility = "hidden";
        this.elem = stateDisplayElem;
        document.body.appendChild( this.elem );

        this.setString( this.JS_IM_Obj.methodObj.params.displayString );

      },
      show : function(){
        //this.elem.style.visibility = "visible";
      },
      hide : function(){
        this.elem.style.visibility = "hidden";
      },
      setString : function( string ){
        this.elem.innerHTML = string;
      }
    },
    buffer : {
      JS_IM_Obj : null,
      elem : null,
      init : function(){
        var bufferBoxElem = document.createElement("div");
        JS_IM_setClassName( bufferBoxElem, "jsim_bufferbox" );

        document.body.appendChild( bufferBoxElem );
        this.elem = bufferBoxElem;
      },
      update : function( bufferStr ){
        if( bufferStr == '' ){
          this.hide();
          return;
        }
        this.elem.innerHTML = bufferStr;
        this.elem.style.width = ( ( JS_IM_Common.stripTags(bufferStr).length * 11 ) + 15 ) + "px";
        this.flush();
      },
      flush : function(){
        //this.elem.style.visibility = "visible";
      },
      hide : function(){
        this.elem.style.visibility = "hidden";
      },
      setPosition : function( left, top ){
        this.elem.style.top = top + "px";
        this.elem.style.left = left + "px";
      }
    },
    list : {
      JS_IM_Obj : null,
      elem : null,
      candidateElems : null,
      selectedCandidateNum : 0,
      init : function(){
        var listBoxElem = document.createElement("ul");
        JS_IM_setClassName( listBoxElem, "jsim_listbox" );

        var imeBoxPosition = JS_IM_Common.cumulativeOffset(this.JS_IM_Obj.imeBox);
        listBoxElem.style.top = imeBoxPosition.top + 30 + "px";
        listBoxElem.style.left = imeBoxPosition.left + this.JS_IM_Obj.imeBox.offsetWidth + "px";

        listBoxElem.style.background = "#FFE";
        listBoxElem.style.listStyleType = "none";
        listBoxElem.style.listStylePosition = "inside";
        listBoxElem.style.visibility = "hidden";
        listBoxElem.style.border = "solid 1px #333";
        listBoxElem.style.padding = "0 3px 3px 3px";
        listBoxElem.style.margin = "0";
        listBoxElem.style.position = "absolute";
        listBoxElem.style.width = "200px";

        document.body.appendChild( listBoxElem );
        this.elem = listBoxElem;
        this.candidateElems = new Array();
      },
      next : function(){
        this.selectedCandidateNum += 1 + this.candidateElems.length;
        this.selectedCandidateNum %= this.candidateElems.length;
        this.flush(); // 背景色再描画
      },
      prev : function(){
        this.selectedCandidateNum += -1 + this.candidateElems.length;
        this.selectedCandidateNum %= this.candidateElems.length;
        this.flush(); // 背景色再描画
      },
      update : function(listArray){ // 配列書き換え
        var i,length;
        length = this.candidateElems.length;
        for(i=0;i<length;i++){
          this.elem.removeChild( this.candidateElems[i] );
        }
        this.candidateElems = new Array();
        if( typeof listArray == 'string' ){
          var candidate = document.createElement("li");
          candidate.innerHTML = listArray;
          this.elem.appendChild( candidate );
          this.candidateElems[i] = candidate;
        }
        else{
          length = listArray.length;
          for(i=0;i<length;i++){
            var candidate = document.createElement("li");
            candidate.innerHTML = listArray[i];
            this.elem.appendChild( candidate );
            this.candidateElems[i] = candidate;
          }
        }
        this.selectedCandidateNum = 0;
        this.flush();
      },
      flush : function(){ // リスト描画
        //this.elem.style.visibility = "visible";
        var length = this.candidateElems.length;
        var pos = this.selectedCandidateNum;
        var color,background;
        for(i=0;i<length;i++) if( i == pos ) {
          JS_IM_setClassName( this.candidateElems[i], "jsim_listbox_li_selected" );
        }
        else{
          JS_IM_setClassName( this.candidateElems[i],  "" );
        }

        // 描画位置設定
        var bufferElem = this.JS_IM_Obj.GUI.buffer.elem;
        if( bufferElem ){
          var bufferElemPosition =  JS_IM_Common.cumulativeOffset( bufferElem );
          this.elem.style.left = bufferElemPosition.left + "px";
          this.elem.style.top = bufferElemPosition.top + bufferElem.offsetHeight + "px";
        }
      },
      hide : function(){
    //        this.update( new Array() );
        this.elem.style.visibility = "hidden";
      },
      setSelectedCandidateNum : function( num ){
        this.selectedCandidateNum = num;
        this.flush();
      },
      setPosition : function( top, left ){
        this.elem.style.top = top + "px";
        this.elem.style.left = left + "px";
      }
    }
};

var JS_IM_Method = Class.create();
JS_IM_Method.prototype = {
  methodName : "",
  version : "",
  language : "",
  author : "",
  inlineBuffer : "", // インライン入力作業文字列
  extension : { // 独自拡張領域
    methodObj : null
  },
  JS_IM_Obj : null, // 親オブジェクト
  phase : null,
  params : { // 親に渡す情報
    displayString : 'skelton',
    listBox : false,
    inlineInsertion : true
  },
  init : function(){// 初期化処理
  },
  callback : function(){// コールバック用
  },
  accept : function(){
    var outputStr = this.inlineBuffer;
    this.inlineBuffer = "";
    return outputStr;
  },
/*// process( keyStatus )
  入力値 キー入力情報
  返り値 outputStr
    結合処理ができる場合 文字列 (処理における確定文字がない場合は空文字を返す)
    結合処理ができない場合 null
*/
  process : function( keyStatus ){
    var outputStr = keyStatus.inputChar;
    return outputStr;
  },
  backspace : function(){
  },
  initialize : function(functionObj){
    var valueList = ["init","methodName","version","language","author","accept","process","backspace","extension","params","callback"];
    if( functionObj ){
      for( i=0;i<valueList.length;i++ ){
        switch( typeof functionObj[valueList[i]] ){
            case 'function' :
                this[valueList[i]] = functionObj[valueList[i]];
            break;
            case 'object' :
                this[valueList[i]] = JS_IM_Common.cloneObj( functionObj[valueList[i]] );
            break;
        }
      }
      this.init();
    }
    this.extension.methodObj = this;
  }
}

// JS_IM Method Sample
var JS_IM_toUpperCase = {
  methodName : "toUpperCase",
  version : "20080123",
  language : "English",
  author : "Colspan",
  process : function( keyStatus ){
    var outputStr = keyStatus.inputChar.toUpperCase();
    return outputStr;
  }
}
