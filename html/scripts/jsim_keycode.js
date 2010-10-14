//////////////////////////////////
//
//    keyCode
//        by Colspan (Miyoshi)
//         http://colspan.net/
//        License : MIT license
//
// depend prototype.js

// キー入力管理 ///////////////
var keyCode = {
  version : "20090813",
  author : "Colspan",
  specialKeys : {
    8:  'Backspace',
    9:  'Tab',
    10: 'Enter',
    13: 'Enter',
    16: 'Shift',
    17: 'Control',
    27: 'ESC',
    32: 'Space',
    33: 'PageUp',
    34: 'PageDown',
    35: 'End',
    36: 'Home',
    37: 'Left',
    38: 'Up',
    39: 'Right',
    40: 'Down',
    45: 'Insert',
    46: 'Delete',
    112: 'F1',
    113: 'F2',
    114: 'F3',
    115: 'F4',
    116: 'F5',
    117: 'F6',
    118: 'F7',
    119: 'F8',
    120: 'F9',
    121: 'F10',
    122: 'F11',
    123: 'F12',
    224: 'Meta'
  },
  isAlphabet : function(code){
		return ( code >= 0x41 && code <= 0x5a ) || ( code >= 0x61 && code <= 0x7a );
	},
  isAlphabetLower : function(code){
    return ( code >= 0x61 && code <= 0x7a );
  },
  isAlphabetUpper : function(code){
    return ( code >= 0x41 && code <= 0x5a );
  },
	isSymbol : function(code){
    return code >= 186 && code <= 191 || code >= 219 && code <= 222;
	},
  isNumeric : function(code){
    return code >= 0x30 && code <= 0x39;
  },
  isInputtable : function(code){
    return this.isAlphabet(code) || this.isSymbol(code) || this.isNumeric(code);
  },
  isSpecialKey : function(code){
    return this.specialKeys[code] != undefined;
  },
  getKeyStatus : function( e ){
    var inputChar = '',inputCode = null;
    if( JS_IM_Common.Browser.IE ) e = event; // IEの場合

    // 入力文字取得
    if( JS_IM_Common.Browser.IE ){ // onkeydownからやってくる
      inputCode = e.keyCode;//( JS_IM_Common.Browser.IE ? e.keyCode : e.charCode ); // IEだとkeyCode
      if( this.isAlphabetUpper( inputCode ) ){
        inputChar = String.fromCharCode(inputCode);
        inputChar = e.shiftKey ? inputChar.toUpperCase() : inputChar.toLowerCase(); // IE対策
      }
      else if( inputCode >= 188 && inputCode <= 191 ){  // ,./\
        inputCode -= e.shiftKey ? 128 : 144;
        inputChar = String.fromCharCode(inputCode);
      }
      else inputChar = null;
    }
    else if( JS_IM_Common.Browser.Gecko ){// Firefox onkeypressからやってくる
      if( e.keyCode == 0 && e.charCode != 32 ){
        inputCode = e.charCode;
        inputChar = String.fromCharCode(inputCode);
      }
      else{
        inputCode = e.keyCode ? e.keyCode : e.charCode;
        inputChar = null;
      }
    }
    else if( JS_IM_Common.Browser.WebKit ){ // Webkit
      inputCode = e.keyCode;
      if( this.isAlphabetUpper( inputCode ) ){
        inputChar = String.fromCharCode(inputCode);
        inputChar = e.shiftKey ? inputChar.toUpperCase() : inputChar.toLowerCase();
      }
      else if( inputCode >= 188 && inputCode <= 191 ){  // ,./\
        inputCode -= e.shiftKey ? 128 : 144;
        inputChar = String.fromCharCode(inputCode);
      }
    }
    else if( JS_IM_Common.Browser.Opera ){
        alert( "未実装です" );
    }
    else{
        return null;
    }

    // Methodに渡すキー情報オブジェクト
    var keyStatus = {
      ctrlKey : e.ctrlKey,
      altKey : e.altKey,
      metaKey : e.metaKey,
      shiftKey : e.shiftKey,
      keyCode : e.keyCode,
      charCode : e.charCode,
      inputChar : inputChar,
      inputCode : inputCode
    };

    return keyStatus;
  }
}
