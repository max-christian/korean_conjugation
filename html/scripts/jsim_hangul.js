//////////////////////////////////
//
//    JS IM Hangul
//        by Colspan (Miyoshi)
//         http://colspan.net/
//        License : MIT license
//
// depend JSIM.js,johab.js,prototype.js

var JS_IM_hangul = {
  methodName : "Hangul",
  version : "20080123",
  language : "Korean",
  author : "Colspan",
  params : {
    displayString : '한',
    listBox : false,
    inlineInsertion : true
  },
  process : function( keyStatus ){
    var outputStr="";

    if( ! keyCode.isAlphabet( keyStatus.inputCode ) ){//アルファベットではない場合は処理しない
      outputStr = null;
      return outputStr;
    }

		//Shiftキーの状態による母音と子音の処理
    var noShiftCharacterSet = "abcdfghijklmnsuvxyz";
		inputChar = ( keyStatus.shiftKey && ( noShiftCharacterSet.indexOf( keyStatus.inputChar.toLowerCase() ) == -1 ) ?
      keyStatus.inputChar.toUpperCase() :
		  keyStatus.inputChar.toLowerCase()
    );

		//変換開始
		if( isJasoKey( inputChar ) ){ // 作業文字列に入力文字を演算
			this.inlineBuffer = strPlusJasoKey( this.inlineBuffer, inputChar );
		}
    if( this.inlineBuffer.length == 2 ){ //文字が確定した
      outputStr = this.inlineBuffer.substring(0, 1);
      this.inlineBuffer = this.inlineBuffer.substring(1,2);
    }
		return outputStr;
  },
	backspace : function(){
    if( this.inlineBuffer.length == 0 ) return false;
	  this.inlineBuffer = strDeleteOneJaso( this.inlineBuffer );
    return true;
  }
}

