//////////////////////////////////
//
//    JS IM Common Library
//        by Colspan (Miyoshi)
//         http://colspan.net/
//
// ported from prototype.js

var JS_IM_Common = {
  version : "20090813",
  author : "Colspan",
  Browser: {
	IE:     !!(window.attachEvent && !window.opera),
	Opera:  !!window.opera,
	WebKit: navigator.userAgent.indexOf('AppleWebKit/') > -1,
	Gecko:  navigator.userAgent.indexOf('Gecko') > -1 && navigator.userAgent.indexOf('KHTML') == -1,
	MobileSafari: !!navigator.userAgent.match(/Apple.*Mobile.*Safari/)
  },
  $: function( element ){
	element = document.getElementById(element);
	return element;
  },
  cloneObj: function(source) {
	destination = {};
	for (var property in source)
	destination[property] = source[property];
	return destination;
  },
  cumulativeOffset: function(element) {
	var valueT = 0, valueL = 0;
	do {
	  valueT += element.offsetTop  || 0;
	  valueL += element.offsetLeft || 0;
	  element = element.offsetParent;
	} while (element);
	return { left:valueL, top:valueT };
  },
  camelize: function( targetString ) {
	var parts = targetString.split('-'), len = parts.length;
	if (len == 1) return parts[0];

	var camelized = targetString.charAt(0) == '-'
	  ? parts[0].charAt(0).toUpperCase() + parts[0].substring(1)
	  : parts[0];

	for (var i = 1; i < len; i++)
	  camelized += parts[i].charAt(0).toUpperCase() + parts[i].substring(1);

	return camelized;
  },
  getStyle: function(element, style) {
	style = style == 'float' ? 'cssFloat' : JS_IM_Common.camelize(style);
	var value = element.style[style];
	if (!value) {
	  var css = document.defaultView.getComputedStyle(element, null);
	  value = css ? css[style] : null;
	}
	if (style == 'opacity') return value ? parseFloat(value) : 1.0;
	return value == 'auto' ? null : value;
  },
  stripTags: function(targetString) {
	return targetString.replace(/<\/?[^>]+>/gi, '');
  }

};
var Class = {
  create: function() {
	return function () {
	  this.initialize.apply(this, arguments);
	};
  }
};

