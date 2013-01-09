/*! jQuery v1.7.2 jquery.com | jquery.org/license */
(function(a,b){function cy(a){return f.isWindow(a)?a:a.nodeType===9?a.defaultView||a.parentWindow:!1}function cu(a){if(!cj[a]){var b=c.body,d=f("<"+a+">").appendTo(b),e=d.css("display");d.remove();if(e==="none"||e===""){ck||(ck=c.createElement("iframe"),ck.frameBorder=ck.width=ck.height=0),b.appendChild(ck);if(!cl||!ck.createElement)cl=(ck.contentWindow||ck.contentDocument).document,cl.write((f.support.boxModel?"<!doctype html>":"")+"<html><body>"),cl.close();d=cl.createElement(a),cl.body.appendChild(d),e=f.css(d,"display"),b.removeChild(ck)}cj[a]=e}return cj[a]}function ct(a,b){var c={};f.each(cp.concat.apply([],cp.slice(0,b)),function(){c[this]=a});return c}function cs(){cq=b}function cr(){setTimeout(cs,0);return cq=f.now()}function ci(){try{return new a.ActiveXObject("Microsoft.XMLHTTP")}catch(b){}}function ch(){try{return new a.XMLHttpRequest}catch(b){}}function cb(a,c){a.dataFilter&&(c=a.dataFilter(c,a.dataType));var d=a.dataTypes,e={},g,h,i=d.length,j,k=d[0],l,m,n,o,p;for(g=1;g<i;g++){if(g===1)for(h in a.converters)typeof h=="string"&&(e[h.toLowerCase()]=a.converters[h]);l=k,k=d[g];if(k==="*")k=l;else if(l!=="*"&&l!==k){m=l+" "+k,n=e[m]||e["* "+k];if(!n){p=b;for(o in e){j=o.split(" ");if(j[0]===l||j[0]==="*"){p=e[j[1]+" "+k];if(p){o=e[o],o===!0?n=p:p===!0&&(n=o);break}}}}!n&&!p&&f.error("No conversion from "+m.replace(" "," to ")),n!==!0&&(c=n?n(c):p(o(c)))}}return c}function ca(a,c,d){var e=a.contents,f=a.dataTypes,g=a.responseFields,h,i,j,k;for(i in g)i in d&&(c[g[i]]=d[i]);while(f[0]==="*")f.shift(),h===b&&(h=a.mimeType||c.getResponseHeader("content-type"));if(h)for(i in e)if(e[i]&&e[i].test(h)){f.unshift(i);break}if(f[0]in d)j=f[0];else{for(i in d){if(!f[0]||a.converters[i+" "+f[0]]){j=i;break}k||(k=i)}j=j||k}if(j){j!==f[0]&&f.unshift(j);return d[j]}}function b_(a,b,c,d){if(f.isArray(b))f.each(b,function(b,e){c||bD.test(a)?d(a,e):b_(a+"["+(typeof e=="object"?b:"")+"]",e,c,d)});else if(!c&&f.type(b)==="object")for(var e in b)b_(a+"["+e+"]",b[e],c,d);else d(a,b)}function b$(a,c){var d,e,g=f.ajaxSettings.flatOptions||{};for(d in c)c[d]!==b&&((g[d]?a:e||(e={}))[d]=c[d]);e&&f.extend(!0,a,e)}function bZ(a,c,d,e,f,g){f=f||c.dataTypes[0],g=g||{},g[f]=!0;var h=a[f],i=0,j=h?h.length:0,k=a===bS,l;for(;i<j&&(k||!l);i++)l=h[i](c,d,e),typeof l=="string"&&(!k||g[l]?l=b:(c.dataTypes.unshift(l),l=bZ(a,c,d,e,l,g)));(k||!l)&&!g["*"]&&(l=bZ(a,c,d,e,"*",g));return l}function bY(a){return function(b,c){typeof b!="string"&&(c=b,b="*");if(f.isFunction(c)){var d=b.toLowerCase().split(bO),e=0,g=d.length,h,i,j;for(;e<g;e++)h=d[e],j=/^\+/.test(h),j&&(h=h.substr(1)||"*"),i=a[h]=a[h]||[],i[j?"unshift":"push"](c)}}}function bB(a,b,c){var d=b==="width"?a.offsetWidth:a.offsetHeight,e=b==="width"?1:0,g=4;if(d>0){if(c!=="border")for(;e<g;e+=2)c||(d-=parseFloat(f.css(a,"padding"+bx[e]))||0),c==="margin"?d+=parseFloat(f.css(a,c+bx[e]))||0:d-=parseFloat(f.css(a,"border"+bx[e]+"Width"))||0;return d+"px"}d=by(a,b);if(d<0||d==null)d=a.style[b];if(bt.test(d))return d;d=parseFloat(d)||0;if(c)for(;e<g;e+=2)d+=parseFloat(f.css(a,"padding"+bx[e]))||0,c!=="padding"&&(d+=parseFloat(f.css(a,"border"+bx[e]+"Width"))||0),c==="margin"&&(d+=parseFloat(f.css(a,c+bx[e]))||0);return d+"px"}function bo(a){var b=c.createElement("div");bh.appendChild(b),b.innerHTML=a.outerHTML;return b.firstChild}function bn(a){var b=(a.nodeName||"").toLowerCase();b==="input"?bm(a):b!=="script"&&typeof a.getElementsByTagName!="undefined"&&f.grep(a.getElementsByTagName("input"),bm)}function bm(a){if(a.type==="checkbox"||a.type==="radio")a.defaultChecked=a.checked}function bl(a){return typeof a.getElementsByTagName!="undefined"?a.getElementsByTagName("*"):typeof a.querySelectorAll!="undefined"?a.querySelectorAll("*"):[]}function bk(a,b){var c;b.nodeType===1&&(b.clearAttributes&&b.clearAttributes(),b.mergeAttributes&&b.mergeAttributes(a),c=b.nodeName.toLowerCase(),c==="object"?b.outerHTML=a.outerHTML:c!=="input"||a.type!=="checkbox"&&a.type!=="radio"?c==="option"?b.selected=a.defaultSelected:c==="input"||c==="textarea"?b.defaultValue=a.defaultValue:c==="script"&&b.text!==a.text&&(b.text=a.text):(a.checked&&(b.defaultChecked=b.checked=a.checked),b.value!==a.value&&(b.value=a.value)),b.removeAttribute(f.expando),b.removeAttribute("_submit_attached"),b.removeAttribute("_change_attached"))}function bj(a,b){if(b.nodeType===1&&!!f.hasData(a)){var c,d,e,g=f._data(a),h=f._data(b,g),i=g.events;if(i){delete h.handle,h.events={};for(c in i)for(d=0,e=i[c].length;d<e;d++)f.event.add(b,c,i[c][d])}h.data&&(h.data=f.extend({},h.data))}}function bi(a,b){return f.nodeName(a,"table")?a.getElementsByTagName("tbody")[0]||a.appendChild(a.ownerDocument.createElement("tbody")):a}function U(a){var b=V.split("|"),c=a.createDocumentFragment();if(c.createElement)while(b.length)c.createElement(b.pop());return c}function T(a,b,c){b=b||0;if(f.isFunction(b))return f.grep(a,function(a,d){var e=!!b.call(a,d,a);return e===c});if(b.nodeType)return f.grep(a,function(a,d){return a===b===c});if(typeof b=="string"){var d=f.grep(a,function(a){return a.nodeType===1});if(O.test(b))return f.filter(b,d,!c);b=f.filter(b,d)}return f.grep(a,function(a,d){return f.inArray(a,b)>=0===c})}function S(a){return!a||!a.parentNode||a.parentNode.nodeType===11}function K(){return!0}function J(){return!1}function n(a,b,c){var d=b+"defer",e=b+"queue",g=b+"mark",h=f._data(a,d);h&&(c==="queue"||!f._data(a,e))&&(c==="mark"||!f._data(a,g))&&setTimeout(function(){!f._data(a,e)&&!f._data(a,g)&&(f.removeData(a,d,!0),h.fire())},0)}function m(a){for(var b in a){if(b==="data"&&f.isEmptyObject(a[b]))continue;if(b!=="toJSON")return!1}return!0}function l(a,c,d){if(d===b&&a.nodeType===1){var e="data-"+c.replace(k,"-$1").toLowerCase();d=a.getAttribute(e);if(typeof d=="string"){try{d=d==="true"?!0:d==="false"?!1:d==="null"?null:f.isNumeric(d)?+d:j.test(d)?f.parseJSON(d):d}catch(g){}f.data(a,c,d)}else d=b}return d}function h(a){var b=g[a]={},c,d;a=a.split(/\s+/);for(c=0,d=a.length;c<d;c++)b[a[c]]=!0;return b}var c=a.document,d=a.navigator,e=a.location,f=function(){function J(){if(!e.isReady){try{c.documentElement.doScroll("left")}catch(a){setTimeout(J,1);return}e.ready()}}var e=function(a,b){return new e.fn.init(a,b,h)},f=a.jQuery,g=a.$,h,i=/^(?:[^#<]*(<[\w\W]+>)[^>]*$|#([\w\-]*)$)/,j=/\S/,k=/^\s+/,l=/\s+$/,m=/^<(\w+)\s*\/?>(?:<\/\1>)?$/,n=/^[\],:{}\s]*$/,o=/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,p=/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,q=/(?:^|:|,)(?:\s*\[)+/g,r=/(webkit)[ \/]([\w.]+)/,s=/(opera)(?:.*version)?[ \/]([\w.]+)/,t=/(msie) ([\w.]+)/,u=/(mozilla)(?:.*? rv:([\w.]+))?/,v=/-([a-z]|[0-9])/ig,w=/^-ms-/,x=function(a,b){return(b+"").toUpperCase()},y=d.userAgent,z,A,B,C=Object.prototype.toString,D=Object.prototype.hasOwnProperty,E=Array.prototype.push,F=Array.prototype.slice,G=String.prototype.trim,H=Array.prototype.indexOf,I={};e.fn=e.prototype={constructor:e,init:function(a,d,f){var g,h,j,k;if(!a)return this;if(a.nodeType){this.context=this[0]=a,this.length=1;return this}if(a==="body"&&!d&&c.body){this.context=c,this[0]=c.body,this.selector=a,this.length=1;return this}if(typeof a=="string"){a.charAt(0)!=="<"||a.charAt(a.length-1)!==">"||a.length<3?g=i.exec(a):g=[null,a,null];if(g&&(g[1]||!d)){if(g[1]){d=d instanceof e?d[0]:d,k=d?d.ownerDocument||d:c,j=m.exec(a),j?e.isPlainObject(d)?(a=[c.createElement(j[1])],e.fn.attr.call(a,d,!0)):a=[k.createElement(j[1])]:(j=e.buildFragment([g[1]],[k]),a=(j.cacheable?e.clone(j.fragment):j.fragment).childNodes);return e.merge(this,a)}h=c.getElementById(g[2]);if(h&&h.parentNode){if(h.id!==g[2])return f.find(a);this.length=1,this[0]=h}this.context=c,this.selector=a;return this}return!d||d.jquery?(d||f).find(a):this.constructor(d).find(a)}if(e.isFunction(a))return f.ready(a);a.selector!==b&&(this.selector=a.selector,this.context=a.context);return e.makeArray(a,this)},selector:"",jquery:"1.7.2",length:0,size:function(){return this.length},toArray:function(){return F.call(this,0)},get:function(a){return a==null?this.toArray():a<0?this[this.length+a]:this[a]},pushStack:function(a,b,c){var d=this.constructor();e.isArray(a)?E.apply(d,a):e.merge(d,a),d.prevObject=this,d.context=this.context,b==="find"?d.selector=this.selector+(this.selector?" ":"")+c:b&&(d.selector=this.selector+"."+b+"("+c+")");return d},each:function(a,b){return e.each(this,a,b)},ready:function(a){e.bindReady(),A.add(a);return this},eq:function(a){a=+a;return a===-1?this.slice(a):this.slice(a,a+1)},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},slice:function(){return this.pushStack(F.apply(this,arguments),"slice",F.call(arguments).join(","))},map:function(a){return this.pushStack(e.map(this,function(b,c){return a.call(b,c,b)}))},end:function(){return this.prevObject||this.constructor(null)},push:E,sort:[].sort,splice:[].splice},e.fn.init.prototype=e.fn,e.extend=e.fn.extend=function(){var a,c,d,f,g,h,i=arguments[0]||{},j=1,k=arguments.length,l=!1;typeof i=="boolean"&&(l=i,i=arguments[1]||{},j=2),typeof i!="object"&&!e.isFunction(i)&&(i={}),k===j&&(i=this,--j);for(;j<k;j++)if((a=arguments[j])!=null)for(c in a){d=i[c],f=a[c];if(i===f)continue;l&&f&&(e.isPlainObject(f)||(g=e.isArray(f)))?(g?(g=!1,h=d&&e.isArray(d)?d:[]):h=d&&e.isPlainObject(d)?d:{},i[c]=e.extend(l,h,f)):f!==b&&(i[c]=f)}return i},e.extend({noConflict:function(b){a.$===e&&(a.$=g),b&&a.jQuery===e&&(a.jQuery=f);return e},isReady:!1,readyWait:1,holdReady:function(a){a?e.readyWait++:e.ready(!0)},ready:function(a){if(a===!0&&!--e.readyWait||a!==!0&&!e.isReady){if(!c.body)return setTimeout(e.ready,1);e.isReady=!0;if(a!==!0&&--e.readyWait>0)return;A.fireWith(c,[e]),e.fn.trigger&&e(c).trigger("ready").off("ready")}},bindReady:function(){if(!A){A=e.Callbacks("once memory");if(c.readyState==="complete")return setTimeout(e.ready,1);if(c.addEventListener)c.addEventListener("DOMContentLoaded",B,!1),a.addEventListener("load",e.ready,!1);else if(c.attachEvent){c.attachEvent("onreadystatechange",B),a.attachEvent("onload",e.ready);var b=!1;try{b=a.frameElement==null}catch(d){}c.documentElement.doScroll&&b&&J()}}},isFunction:function(a){return e.type(a)==="function"},isArray:Array.isArray||function(a){return e.type(a)==="array"},isWindow:function(a){return a!=null&&a==a.window},isNumeric:function(a){return!isNaN(parseFloat(a))&&isFinite(a)},type:function(a){return a==null?String(a):I[C.call(a)]||"object"},isPlainObject:function(a){if(!a||e.type(a)!=="object"||a.nodeType||e.isWindow(a))return!1;try{if(a.constructor&&!D.call(a,"constructor")&&!D.call(a.constructor.prototype,"isPrototypeOf"))return!1}catch(c){return!1}var d;for(d in a);return d===b||D.call(a,d)},isEmptyObject:function(a){for(var b in a)return!1;return!0},error:function(a){throw new Error(a)},parseJSON:function(b){if(typeof b!="string"||!b)return null;b=e.trim(b);if(a.JSON&&a.JSON.parse)return a.JSON.parse(b);if(n.test(b.replace(o,"@").replace(p,"]").replace(q,"")))return(new Function("return "+b))();e.error("Invalid JSON: "+b)},parseXML:function(c){if(typeof c!="string"||!c)return null;var d,f;try{a.DOMParser?(f=new DOMParser,d=f.parseFromString(c,"text/xml")):(d=new ActiveXObject("Microsoft.XMLDOM"),d.async="false",d.loadXML(c))}catch(g){d=b}(!d||!d.documentElement||d.getElementsByTagName("parsererror").length)&&e.error("Invalid XML: "+c);return d},noop:function(){},globalEval:function(b){b&&j.test(b)&&(a.execScript||function(b){a.eval.call(a,b)})(b)},camelCase:function(a){return a.replace(w,"ms-").replace(v,x)},nodeName:function(a,b){return a.nodeName&&a.nodeName.toUpperCase()===b.toUpperCase()},each:function(a,c,d){var f,g=0,h=a.length,i=h===b||e.isFunction(a);if(d){if(i){for(f in a)if(c.apply(a[f],d)===!1)break}else for(;g<h;)if(c.apply(a[g++],d)===!1)break}else if(i){for(f in a)if(c.call(a[f],f,a[f])===!1)break}else for(;g<h;)if(c.call(a[g],g,a[g++])===!1)break;return a},trim:G?function(a){return a==null?"":G.call(a)}:function(a){return a==null?"":(a+"").replace(k,"").replace(l,"")},makeArray:function(a,b){var c=b||[];if(a!=null){var d=e.type(a);a.length==null||d==="string"||d==="function"||d==="regexp"||e.isWindow(a)?E.call(c,a):e.merge(c,a)}return c},inArray:function(a,b,c){var d;if(b){if(H)return H.call(b,a,c);d=b.length,c=c?c<0?Math.max(0,d+c):c:0;for(;c<d;c++)if(c in b&&b[c]===a)return c}return-1},merge:function(a,c){var d=a.length,e=0;if(typeof c.length=="number")for(var f=c.length;e<f;e++)a[d++]=c[e];else while(c[e]!==b)a[d++]=c[e++];a.length=d;return a},grep:function(a,b,c){var d=[],e;c=!!c;for(var f=0,g=a.length;f<g;f++)e=!!b(a[f],f),c!==e&&d.push(a[f]);return d},map:function(a,c,d){var f,g,h=[],i=0,j=a.length,k=a instanceof e||j!==b&&typeof j=="number"&&(j>0&&a[0]&&a[j-1]||j===0||e.isArray(a));if(k)for(;i<j;i++)f=c(a[i],i,d),f!=null&&(h[h.length]=f);else for(g in a)f=c(a[g],g,d),f!=null&&(h[h.length]=f);return h.concat.apply([],h)},guid:1,proxy:function(a,c){if(typeof c=="string"){var d=a[c];c=a,a=d}if(!e.isFunction(a))return b;var f=F.call(arguments,2),g=function(){return a.apply(c,f.concat(F.call(arguments)))};g.guid=a.guid=a.guid||g.guid||e.guid++;return g},access:function(a,c,d,f,g,h,i){var j,k=d==null,l=0,m=a.length;if(d&&typeof d=="object"){for(l in d)e.access(a,c,l,d[l],1,h,f);g=1}else if(f!==b){j=i===b&&e.isFunction(f),k&&(j?(j=c,c=function(a,b,c){return j.call(e(a),c)}):(c.call(a,f),c=null));if(c)for(;l<m;l++)c(a[l],d,j?f.call(a[l],l,c(a[l],d)):f,i);g=1}return g?a:k?c.call(a):m?c(a[0],d):h},now:function(){return(new Date).getTime()},uaMatch:function(a){a=a.toLowerCase();var b=r.exec(a)||s.exec(a)||t.exec(a)||a.indexOf("compatible")<0&&u.exec(a)||[];return{browser:b[1]||"",version:b[2]||"0"}},sub:function(){function a(b,c){return new a.fn.init(b,c)}e.extend(!0,a,this),a.superclass=this,a.fn=a.prototype=this(),a.fn.constructor=a,a.sub=this.sub,a.fn.init=function(d,f){f&&f instanceof e&&!(f instanceof a)&&(f=a(f));return e.fn.init.call(this,d,f,b)},a.fn.init.prototype=a.fn;var b=a(c);return a},browser:{}}),e.each("Boolean Number String Function Array Date RegExp Object".split(" "),function(a,b){I["[object "+b+"]"]=b.toLowerCase()}),z=e.uaMatch(y),z.browser&&(e.browser[z.browser]=!0,e.browser.version=z.version),e.browser.webkit&&(e.browser.safari=!0),j.test(" ")&&(k=/^[\s\xA0]+/,l=/[\s\xA0]+$/),h=e(c),c.addEventListener?B=function(){c.removeEventListener("DOMContentLoaded",B,!1),e.ready()}:c.attachEvent&&(B=function(){c.readyState==="complete"&&(c.detachEvent("onreadystatechange",B),e.ready())});return e}(),g={};f.Callbacks=function(a){a=a?g[a]||h(a):{};var c=[],d=[],e,i,j,k,l,m,n=function(b){var d,e,g,h,i;for(d=0,e=b.length;d<e;d++)g=b[d],h=f.type(g),h==="array"?n(g):h==="function"&&(!a.unique||!p.has(g))&&c.push(g)},o=function(b,f){f=f||[],e=!a.memory||[b,f],i=!0,j=!0,m=k||0,k=0,l=c.length;for(;c&&m<l;m++)if(c[m].apply(b,f)===!1&&a.stopOnFalse){e=!0;break}j=!1,c&&(a.once?e===!0?p.disable():c=[]:d&&d.length&&(e=d.shift(),p.fireWith(e[0],e[1])))},p={add:function(){if(c){var a=c.length;n(arguments),j?l=c.length:e&&e!==!0&&(k=a,o(e[0],e[1]))}return this},remove:function(){if(c){var b=arguments,d=0,e=b.length;for(;d<e;d++)for(var f=0;f<c.length;f++)if(b[d]===c[f]){j&&f<=l&&(l--,f<=m&&m--),c.splice(f--,1);if(a.unique)break}}return this},has:function(a){if(c){var b=0,d=c.length;for(;b<d;b++)if(a===c[b])return!0}return!1},empty:function(){c=[];return this},disable:function(){c=d=e=b;return this},disabled:function(){return!c},lock:function(){d=b,(!e||e===!0)&&p.disable();return this},locked:function(){return!d},fireWith:function(b,c){d&&(j?a.once||d.push([b,c]):(!a.once||!e)&&o(b,c));return this},fire:function(){p.fireWith(this,arguments);return this},fired:function(){return!!i}};return p};var i=[].slice;f.extend({Deferred:function(a){var b=f.Callbacks("once memory"),c=f.Callbacks("once memory"),d=f.Callbacks("memory"),e="pending",g={resolve:b,reject:c,notify:d},h={done:b.add,fail:c.add,progress:d.add,state:function(){return e},isResolved:b.fired,isRejected:c.fired,then:function(a,b,c){i.done(a).fail(b).progress(c);return this},always:function(){i.done.apply(i,arguments).fail.apply(i,arguments);return this},pipe:function(a,b,c){return f.Deferred(function(d){f.each({done:[a,"resolve"],fail:[b,"reject"],progress:[c,"notify"]},function(a,b){var c=b[0],e=b[1],g;f.isFunction(c)?i[a](function(){g=c.apply(this,arguments),g&&f.isFunction(g.promise)?g.promise().then(d.resolve,d.reject,d.notify):d[e+"With"](this===i?d:this,[g])}):i[a](d[e])})}).promise()},promise:function(a){if(a==null)a=h;else for(var b in h)a[b]=h[b];return a}},i=h.promise({}),j;for(j in g)i[j]=g[j].fire,i[j+"With"]=g[j].fireWith;i.done(function(){e="resolved"},c.disable,d.lock).fail(function(){e="rejected"},b.disable,d.lock),a&&a.call(i,i);return i},when:function(a){function m(a){return function(b){e[a]=arguments.length>1?i.call(arguments,0):b,j.notifyWith(k,e)}}function l(a){return function(c){b[a]=arguments.length>1?i.call(arguments,0):c,--g||j.resolveWith(j,b)}}var b=i.call(arguments,0),c=0,d=b.length,e=Array(d),g=d,h=d,j=d<=1&&a&&f.isFunction(a.promise)?a:f.Deferred(),k=j.promise();if(d>1){for(;c<d;c++)b[c]&&b[c].promise&&f.isFunction(b[c].promise)?b[c].promise().then(l(c),j.reject,m(c)):--g;g||j.resolveWith(j,b)}else j!==a&&j.resolveWith(j,d?[a]:[]);return k}}),f.support=function(){var b,d,e,g,h,i,j,k,l,m,n,o,p=c.createElement("div"),q=c.documentElement;p.setAttribute("className","t"),p.innerHTML="   <link/><table></table><a href='/a' style='top:1px;float:left;opacity:.55;'>a</a><input type='checkbox'/>",d=p.getElementsByTagName("*"),e=p.getElementsByTagName("a")[0];if(!d||!d.length||!e)return{};g=c.createElement("select"),h=g.appendChild(c.createElement("option")),i=p.getElementsByTagName("input")[0],b={leadingWhitespace:p.firstChild.nodeType===3,tbody:!p.getElementsByTagName("tbody").length,htmlSerialize:!!p.getElementsByTagName("link").length,style:/top/.test(e.getAttribute("style")),hrefNormalized:e.getAttribute("href")==="/a",opacity:/^0.55/.test(e.style.opacity),cssFloat:!!e.style.cssFloat,checkOn:i.value==="on",optSelected:h.selected,getSetAttribute:p.className!=="t",enctype:!!c.createElement("form").enctype,html5Clone:c.createElement("nav").cloneNode(!0).outerHTML!=="<:nav></:nav>",submitBubbles:!0,changeBubbles:!0,focusinBubbles:!1,deleteExpando:!0,noCloneEvent:!0,inlineBlockNeedsLayout:!1,shrinkWrapBlocks:!1,reliableMarginRight:!0,pixelMargin:!0},f.boxModel=b.boxModel=c.compatMode==="CSS1Compat",i.checked=!0,b.noCloneChecked=i.cloneNode(!0).checked,g.disabled=!0,b.optDisabled=!h.disabled;try{delete p.test}catch(r){b.deleteExpando=!1}!p.addEventListener&&p.attachEvent&&p.fireEvent&&(p.attachEvent("onclick",function(){b.noCloneEvent=!1}),p.cloneNode(!0).fireEvent("onclick")),i=c.createElement("input"),i.value="t",i.setAttribute("type","radio"),b.radioValue=i.value==="t",i.setAttribute("checked","checked"),i.setAttribute("name","t"),p.appendChild(i),j=c.createDocumentFragment(),j.appendChild(p.lastChild),b.checkClone=j.cloneNode(!0).cloneNode(!0).lastChild.checked,b.appendChecked=i.checked,j.removeChild(i),j.appendChild(p);if(p.attachEvent)for(n in{submit:1,change:1,focusin:1})m="on"+n,o=m in p,o||(p.setAttribute(m,"return;"),o=typeof p[m]=="function"),b[n+"Bubbles"]=o;j.removeChild(p),j=g=h=p=i=null,f(function(){var d,e,g,h,i,j,l,m,n,q,r,s,t,u=c.getElementsByTagName("body")[0];!u||(m=1,t="padding:0;margin:0;border:",r="position:absolute;top:0;left:0;width:1px;height:1px;",s=t+"0;visibility:hidden;",n="style='"+r+t+"5px solid #000;",q="<div "+n+"display:block;'><div style='"+t+"0;display:block;overflow:hidden;'></div></div>"+"<table "+n+"' cellpadding='0' cellspacing='0'>"+"<tr><td></td></tr></table>",d=c.createElement("div"),d.style.cssText=s+"width:0;height:0;position:static;top:0;margin-top:"+m+"px",u.insertBefore(d,u.firstChild),p=c.createElement("div"),d.appendChild(p),p.innerHTML="<table><tr><td style='"+t+"0;display:none'></td><td>t</td></tr></table>",k=p.getElementsByTagName("td"),o=k[0].offsetHeight===0,k[0].style.display="",k[1].style.display="none",b.reliableHiddenOffsets=o&&k[0].offsetHeight===0,a.getComputedStyle&&(p.innerHTML="",l=c.createElement("div"),l.style.width="0",l.style.marginRight="0",p.style.width="2px",p.appendChild(l),b.reliableMarginRight=(parseInt((a.getComputedStyle(l,null)||{marginRight:0}).marginRight,10)||0)===0),typeof p.style.zoom!="undefined"&&(p.innerHTML="",p.style.width=p.style.padding="1px",p.style.border=0,p.style.overflow="hidden",p.style.display="inline",p.style.zoom=1,b.inlineBlockNeedsLayout=p.offsetWidth===3,p.style.display="block",p.style.overflow="visible",p.innerHTML="<div style='width:5px;'></div>",b.shrinkWrapBlocks=p.offsetWidth!==3),p.style.cssText=r+s,p.innerHTML=q,e=p.firstChild,g=e.firstChild,i=e.nextSibling.firstChild.firstChild,j={doesNotAddBorder:g.offsetTop!==5,doesAddBorderForTableAndCells:i.offsetTop===5},g.style.position="fixed",g.style.top="20px",j.fixedPosition=g.offsetTop===20||g.offsetTop===15,g.style.position=g.style.top="",e.style.overflow="hidden",e.style.position="relative",j.subtractsBorderForOverflowNotVisible=g.offsetTop===-5,j.doesNotIncludeMarginInBodyOffset=u.offsetTop!==m,a.getComputedStyle&&(p.style.marginTop="1%",b.pixelMargin=(a.getComputedStyle(p,null)||{marginTop:0}).marginTop!=="1%"),typeof d.style.zoom!="undefined"&&(d.style.zoom=1),u.removeChild(d),l=p=d=null,f.extend(b,j))});return b}();var j=/^(?:\{.*\}|\[.*\])$/,k=/([A-Z])/g;f.extend({cache:{},uuid:0,expando:"jQuery"+(f.fn.jquery+Math.random()).replace(/\D/g,""),noData:{embed:!0,object:"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",applet:!0},hasData:function(a){a=a.nodeType?f.cache[a[f.expando]]:a[f.expando];return!!a&&!m(a)},data:function(a,c,d,e){if(!!f.acceptData(a)){var g,h,i,j=f.expando,k=typeof c=="string",l=a.nodeType,m=l?f.cache:a,n=l?a[j]:a[j]&&j,o=c==="events";if((!n||!m[n]||!o&&!e&&!m[n].data)&&k&&d===b)return;n||(l?a[j]=n=++f.uuid:n=j),m[n]||(m[n]={},l||(m[n].toJSON=f.noop));if(typeof c=="object"||typeof c=="function")e?m[n]=f.extend(m[n],c):m[n].data=f.extend(m[n].data,c);g=h=m[n],e||(h.data||(h.data={}),h=h.data),d!==b&&(h[f.camelCase(c)]=d);if(o&&!h[c])return g.events;k?(i=h[c],i==null&&(i=h[f.camelCase(c)])):i=h;return i}},removeData:function(a,b,c){if(!!f.acceptData(a)){var d,e,g,h=f.expando,i=a.nodeType,j=i?f.cache:a,k=i?a[h]:h;if(!j[k])return;if(b){d=c?j[k]:j[k].data;if(d){f.isArray(b)||(b in d?b=[b]:(b=f.camelCase(b),b in d?b=[b]:b=b.split(" ")));for(e=0,g=b.length;e<g;e++)delete d[b[e]];if(!(c?m:f.isEmptyObject)(d))return}}if(!c){delete j[k].data;if(!m(j[k]))return}f.support.deleteExpando||!j.setInterval?delete j[k]:j[k]=null,i&&(f.support.deleteExpando?delete a[h]:a.removeAttribute?a.removeAttribute(h):a[h]=null)}},_data:function(a,b,c){return f.data(a,b,c,!0)},acceptData:function(a){if(a.nodeName){var b=f.noData[a.nodeName.toLowerCase()];if(b)return b!==!0&&a.getAttribute("classid")===b}return!0}}),f.fn.extend({data:function(a,c){var d,e,g,h,i,j=this[0],k=0,m=null;if(a===b){if(this.length){m=f.data(j);if(j.nodeType===1&&!f._data(j,"parsedAttrs")){g=j.attributes;for(i=g.length;k<i;k++)h=g[k].name,h.indexOf("data-")===0&&(h=f.camelCase(h.substring(5)),l(j,h,m[h]));f._data(j,"parsedAttrs",!0)}}return m}if(typeof a=="object")return this.each(function(){f.data(this,a)});d=a.split(".",2),d[1]=d[1]?"."+d[1]:"",e=d[1]+"!";return f.access(this,function(c){if(c===b){m=this.triggerHandler("getData"+e,[d[0]]),m===b&&j&&(m=f.data(j,a),m=l(j,a,m));return m===b&&d[1]?this.data(d[0]):m}d[1]=c,this.each(function(){var b=f(this);b.triggerHandler("setData"+e,d),f.data(this,a,c),b.triggerHandler("changeData"+e,d)})},null,c,arguments.length>1,null,!1)},removeData:function(a){return this.each(function(){f.removeData(this,a)})}}),f.extend({_mark:function(a,b){a&&(b=(b||"fx")+"mark",f._data(a,b,(f._data(a,b)||0)+1))},_unmark:function(a,b,c){a!==!0&&(c=b,b=a,a=!1);if(b){c=c||"fx";var d=c+"mark",e=a?0:(f._data(b,d)||1)-1;e?f._data(b,d,e):(f.removeData(b,d,!0),n(b,c,"mark"))}},queue:function(a,b,c){var d;if(a){b=(b||"fx")+"queue",d=f._data(a,b),c&&(!d||f.isArray(c)?d=f._data(a,b,f.makeArray(c)):d.push(c));return d||[]}},dequeue:function(a,b){b=b||"fx";var c=f.queue(a,b),d=c.shift(),e={};d==="inprogress"&&(d=c.shift()),d&&(b==="fx"&&c.unshift("inprogress"),f._data(a,b+".run",e),d.call(a,function(){f.dequeue(a,b)},e)),c.length||(f.removeData(a,b+"queue "+b+".run",!0),n(a,b,"queue"))}}),f.fn.extend({queue:function(a,c){var d=2;typeof a!="string"&&(c=a,a="fx",d--);if(arguments.length<d)return f.queue(this[0],a);return c===b?this:this.each(function(){var b=f.queue(this,a,c);a==="fx"&&b[0]!=="inprogress"&&f.dequeue(this,a)})},dequeue:function(a){return this.each(function(){f.dequeue(this,a)})},delay:function(a,b){a=f.fx?f.fx.speeds[a]||a:a,b=b||"fx";return this.queue(b,function(b,c){var d=setTimeout(b,a);c.stop=function(){clearTimeout(d)}})},clearQueue:function(a){return this.queue(a||"fx",[])},promise:function(a,c){function m(){--h||d.resolveWith(e,[e])}typeof a!="string"&&(c=a,a=b),a=a||"fx";var d=f.Deferred(),e=this,g=e.length,h=1,i=a+"defer",j=a+"queue",k=a+"mark",l;while(g--)if(l=f.data(e[g],i,b,!0)||(f.data(e[g],j,b,!0)||f.data(e[g],k,b,!0))&&f.data(e[g],i,f.Callbacks("once memory"),!0))h++,l.add(m);m();return d.promise(c)}});var o=/[\n\t\r]/g,p=/\s+/,q=/\r/g,r=/^(?:button|input)$/i,s=/^(?:button|input|object|select|textarea)$/i,t=/^a(?:rea)?$/i,u=/^(?:autofocus|autoplay|async|checked|controls|defer|disabled|hidden|loop|multiple|open|readonly|required|scoped|selected)$/i,v=f.support.getSetAttribute,w,x,y;f.fn.extend({attr:function(a,b){return f.access(this,f.attr,a,b,arguments.length>1)},removeAttr:function(a){return this.each(function(){f.removeAttr(this,a)})},prop:function(a,b){return f.access(this,f.prop,a,b,arguments.length>1)},removeProp:function(a){a=f.propFix[a]||a;return this.each(function(){try{this[a]=b,delete this[a]}catch(c){}})},addClass:function(a){var b,c,d,e,g,h,i;if(f.isFunction(a))return this.each(function(b){f(this).addClass(a.call(this,b,this.className))});if(a&&typeof a=="string"){b=a.split(p);for(c=0,d=this.length;c<d;c++){e=this[c];if(e.nodeType===1)if(!e.className&&b.length===1)e.className=a;else{g=" "+e.className+" ";for(h=0,i=b.length;h<i;h++)~g.indexOf(" "+b[h]+" ")||(g+=b[h]+" ");e.className=f.trim(g)}}}return this},removeClass:function(a){var c,d,e,g,h,i,j;if(f.isFunction(a))return this.each(function(b){f(this).removeClass(a.call(this,b,this.className))});if(a&&typeof a=="string"||a===b){c=(a||"").split(p);for(d=0,e=this.length;d<e;d++){g=this[d];if(g.nodeType===1&&g.className)if(a){h=(" "+g.className+" ").replace(o," ");for(i=0,j=c.length;i<j;i++)h=h.replace(" "+c[i]+" "," ");g.className=f.trim(h)}else g.className=""}}return this},toggleClass:function(a,b){var c=typeof a,d=typeof b=="boolean";if(f.isFunction(a))return this.each(function(c){f(this).toggleClass(a.call(this,c,this.className,b),b)});return this.each(function(){if(c==="string"){var e,g=0,h=f(this),i=b,j=a.split(p);while(e=j[g++])i=d?i:!h.hasClass(e),h[i?"addClass":"removeClass"](e)}else if(c==="undefined"||c==="boolean")this.className&&f._data(this,"__className__",this.className),this.className=this.className||a===!1?"":f._data(this,"__className__")||""})},hasClass:function(a){var b=" "+a+" ",c=0,d=this.length;for(;c<d;c++)if(this[c].nodeType===1&&(" "+this[c].className+" ").replace(o," ").indexOf(b)>-1)return!0;return!1},val:function(a){var c,d,e,g=this[0];{if(!!arguments.length){e=f.isFunction(a);return this.each(function(d){var g=f(this),h;if(this.nodeType===1){e?h=a.call(this,d,g.val()):h=a,h==null?h="":typeof h=="number"?h+="":f.isArray(h)&&(h=f.map(h,function(a){return a==null?"":a+""})),c=f.valHooks[this.type]||f.valHooks[this.nodeName.toLowerCase()];if(!c||!("set"in c)||c.set(this,h,"value")===b)this.value=h}})}if(g){c=f.valHooks[g.type]||f.valHooks[g.nodeName.toLowerCase()];if(c&&"get"in c&&(d=c.get(g,"value"))!==b)return d;d=g.value;return typeof d=="string"?d.replace(q,""):d==null?"":d}}}}),f.extend({valHooks:{option:{get:function(a){var b=a.attributes.value;return!b||b.specified?a.value:a.text}},select:{get:function(a){var b,c,d,e,g=a.selectedIndex,h=[],i=a.options,j=a.type==="select-one";if(g<0)return null;c=j?g:0,d=j?g+1:i.length;for(;c<d;c++){e=i[c];if(e.selected&&(f.support.optDisabled?!e.disabled:e.getAttribute("disabled")===null)&&(!e.parentNode.disabled||!f.nodeName(e.parentNode,"optgroup"))){b=f(e).val();if(j)return b;h.push(b)}}if(j&&!h.length&&i.length)return f(i[g]).val();return h},set:function(a,b){var c=f.makeArray(b);f(a).find("option").each(function(){this.selected=f.inArray(f(this).val(),c)>=0}),c.length||(a.selectedIndex=-1);return c}}},attrFn:{val:!0,css:!0,html:!0,text:!0,data:!0,width:!0,height:!0,offset:!0},attr:function(a,c,d,e){var g,h,i,j=a.nodeType;if(!!a&&j!==3&&j!==8&&j!==2){if(e&&c in f.attrFn)return f(a)[c](d);if(typeof a.getAttribute=="undefined")return f.prop(a,c,d);i=j!==1||!f.isXMLDoc(a),i&&(c=c.toLowerCase(),h=f.attrHooks[c]||(u.test(c)?x:w));if(d!==b){if(d===null){f.removeAttr(a,c);return}if(h&&"set"in h&&i&&(g=h.set(a,d,c))!==b)return g;a.setAttribute(c,""+d);return d}if(h&&"get"in h&&i&&(g=h.get(a,c))!==null)return g;g=a.getAttribute(c);return g===null?b:g}},removeAttr:function(a,b){var c,d,e,g,h,i=0;if(b&&a.nodeType===1){d=b.toLowerCase().split(p),g=d.length;for(;i<g;i++)e=d[i],e&&(c=f.propFix[e]||e,h=u.test(e),h||f.attr(a,e,""),a.removeAttribute(v?e:c),h&&c in a&&(a[c]=!1))}},attrHooks:{type:{set:function(a,b){if(r.test(a.nodeName)&&a.parentNode)f.error("type property can't be changed");else if(!f.support.radioValue&&b==="radio"&&f.nodeName(a,"input")){var c=a.value;a.setAttribute("type",b),c&&(a.value=c);return b}}},value:{get:function(a,b){if(w&&f.nodeName(a,"button"))return w.get(a,b);return b in a?a.value:null},set:function(a,b,c){if(w&&f.nodeName(a,"button"))return w.set(a,b,c);a.value=b}}},propFix:{tabindex:"tabIndex",readonly:"readOnly","for":"htmlFor","class":"className",maxlength:"maxLength",cellspacing:"cellSpacing",cellpadding:"cellPadding",rowspan:"rowSpan",colspan:"colSpan",usemap:"useMap",frameborder:"frameBorder",contenteditable:"contentEditable"},prop:function(a,c,d){var e,g,h,i=a.nodeType;if(!!a&&i!==3&&i!==8&&i!==2){h=i!==1||!f.isXMLDoc(a),h&&(c=f.propFix[c]||c,g=f.propHooks[c]);return d!==b?g&&"set"in g&&(e=g.set(a,d,c))!==b?e:a[c]=d:g&&"get"in g&&(e=g.get(a,c))!==null?e:a[c]}},propHooks:{tabIndex:{get:function(a){var c=a.getAttributeNode("tabindex");return c&&c.specified?parseInt(c.value,10):s.test(a.nodeName)||t.test(a.nodeName)&&a.href?0:b}}}}),f.attrHooks.tabindex=f.propHooks.tabIndex,x={get:function(a,c){var d,e=f.prop(a,c);return e===!0||typeof e!="boolean"&&(d=a.getAttributeNode(c))&&d.nodeValue!==!1?c.toLowerCase():b},set:function(a,b,c){var d;b===!1?f.removeAttr(a,c):(d=f.propFix[c]||c,d in a&&(a[d]=!0),a.setAttribute(c,c.toLowerCase()));return c}},v||(y={name:!0,id:!0,coords:!0},w=f.valHooks.button={get:function(a,c){var d;d=a.getAttributeNode(c);return d&&(y[c]?d.nodeValue!=="":d.specified)?d.nodeValue:b},set:function(a,b,d){var e=a.getAttributeNode(d);e||(e=c.createAttribute(d),a.setAttributeNode(e));return e.nodeValue=b+""}},f.attrHooks.tabindex.set=w.set,f.each(["width","height"],function(a,b){f.attrHooks[b]=f.extend(f.attrHooks[b],{set:function(a,c){if(c===""){a.setAttribute(b,"auto");return c}}})}),f.attrHooks.contenteditable={get:w.get,set:function(a,b,c){b===""&&(b="false"),w.set(a,b,c)}}),f.support.hrefNormalized||f.each(["href","src","width","height"],function(a,c){f.attrHooks[c]=f.extend(f.attrHooks[c],{get:function(a){var d=a.getAttribute(c,2);return d===null?b:d}})}),f.support.style||(f.attrHooks.style={get:function(a){return a.style.cssText.toLowerCase()||b},set:function(a,b){return a.style.cssText=""+b}}),f.support.optSelected||(f.propHooks.selected=f.extend(f.propHooks.selected,{get:function(a){var b=a.parentNode;b&&(b.selectedIndex,b.parentNode&&b.parentNode.selectedIndex);return null}})),f.support.enctype||(f.propFix.enctype="encoding"),f.support.checkOn||f.each(["radio","checkbox"],function(){f.valHooks[this]={get:function(a){return a.getAttribute("value")===null?"on":a.value}}}),f.each(["radio","checkbox"],function(){f.valHooks[this]=f.extend(f.valHooks[this],{set:function(a,b){if(f.isArray(b))return a.checked=f.inArray(f(a).val(),b)>=0}})});var z=/^(?:textarea|input|select)$/i,A=/^([^\.]*)?(?:\.(.+))?$/,B=/(?:^|\s)hover(\.\S+)?\b/,C=/^key/,D=/^(?:mouse|contextmenu)|click/,E=/^(?:focusinfocus|focusoutblur)$/,F=/^(\w*)(?:#([\w\-]+))?(?:\.([\w\-]+))?$/,G=function(
a){var b=F.exec(a);b&&(b[1]=(b[1]||"").toLowerCase(),b[3]=b[3]&&new RegExp("(?:^|\\s)"+b[3]+"(?:\\s|$)"));return b},H=function(a,b){var c=a.attributes||{};return(!b[1]||a.nodeName.toLowerCase()===b[1])&&(!b[2]||(c.id||{}).value===b[2])&&(!b[3]||b[3].test((c["class"]||{}).value))},I=function(a){return f.event.special.hover?a:a.replace(B,"mouseenter$1 mouseleave$1")};f.event={add:function(a,c,d,e,g){var h,i,j,k,l,m,n,o,p,q,r,s;if(!(a.nodeType===3||a.nodeType===8||!c||!d||!(h=f._data(a)))){d.handler&&(p=d,d=p.handler,g=p.selector),d.guid||(d.guid=f.guid++),j=h.events,j||(h.events=j={}),i=h.handle,i||(h.handle=i=function(a){return typeof f!="undefined"&&(!a||f.event.triggered!==a.type)?f.event.dispatch.apply(i.elem,arguments):b},i.elem=a),c=f.trim(I(c)).split(" ");for(k=0;k<c.length;k++){l=A.exec(c[k])||[],m=l[1],n=(l[2]||"").split(".").sort(),s=f.event.special[m]||{},m=(g?s.delegateType:s.bindType)||m,s=f.event.special[m]||{},o=f.extend({type:m,origType:l[1],data:e,handler:d,guid:d.guid,selector:g,quick:g&&G(g),namespace:n.join(".")},p),r=j[m];if(!r){r=j[m]=[],r.delegateCount=0;if(!s.setup||s.setup.call(a,e,n,i)===!1)a.addEventListener?a.addEventListener(m,i,!1):a.attachEvent&&a.attachEvent("on"+m,i)}s.add&&(s.add.call(a,o),o.handler.guid||(o.handler.guid=d.guid)),g?r.splice(r.delegateCount++,0,o):r.push(o),f.event.global[m]=!0}a=null}},global:{},remove:function(a,b,c,d,e){var g=f.hasData(a)&&f._data(a),h,i,j,k,l,m,n,o,p,q,r,s;if(!!g&&!!(o=g.events)){b=f.trim(I(b||"")).split(" ");for(h=0;h<b.length;h++){i=A.exec(b[h])||[],j=k=i[1],l=i[2];if(!j){for(j in o)f.event.remove(a,j+b[h],c,d,!0);continue}p=f.event.special[j]||{},j=(d?p.delegateType:p.bindType)||j,r=o[j]||[],m=r.length,l=l?new RegExp("(^|\\.)"+l.split(".").sort().join("\\.(?:.*\\.)?")+"(\\.|$)"):null;for(n=0;n<r.length;n++)s=r[n],(e||k===s.origType)&&(!c||c.guid===s.guid)&&(!l||l.test(s.namespace))&&(!d||d===s.selector||d==="**"&&s.selector)&&(r.splice(n--,1),s.selector&&r.delegateCount--,p.remove&&p.remove.call(a,s));r.length===0&&m!==r.length&&((!p.teardown||p.teardown.call(a,l)===!1)&&f.removeEvent(a,j,g.handle),delete o[j])}f.isEmptyObject(o)&&(q=g.handle,q&&(q.elem=null),f.removeData(a,["events","handle"],!0))}},customEvent:{getData:!0,setData:!0,changeData:!0},trigger:function(c,d,e,g){if(!e||e.nodeType!==3&&e.nodeType!==8){var h=c.type||c,i=[],j,k,l,m,n,o,p,q,r,s;if(E.test(h+f.event.triggered))return;h.indexOf("!")>=0&&(h=h.slice(0,-1),k=!0),h.indexOf(".")>=0&&(i=h.split("."),h=i.shift(),i.sort());if((!e||f.event.customEvent[h])&&!f.event.global[h])return;c=typeof c=="object"?c[f.expando]?c:new f.Event(h,c):new f.Event(h),c.type=h,c.isTrigger=!0,c.exclusive=k,c.namespace=i.join("."),c.namespace_re=c.namespace?new RegExp("(^|\\.)"+i.join("\\.(?:.*\\.)?")+"(\\.|$)"):null,o=h.indexOf(":")<0?"on"+h:"";if(!e){j=f.cache;for(l in j)j[l].events&&j[l].events[h]&&f.event.trigger(c,d,j[l].handle.elem,!0);return}c.result=b,c.target||(c.target=e),d=d!=null?f.makeArray(d):[],d.unshift(c),p=f.event.special[h]||{};if(p.trigger&&p.trigger.apply(e,d)===!1)return;r=[[e,p.bindType||h]];if(!g&&!p.noBubble&&!f.isWindow(e)){s=p.delegateType||h,m=E.test(s+h)?e:e.parentNode,n=null;for(;m;m=m.parentNode)r.push([m,s]),n=m;n&&n===e.ownerDocument&&r.push([n.defaultView||n.parentWindow||a,s])}for(l=0;l<r.length&&!c.isPropagationStopped();l++)m=r[l][0],c.type=r[l][1],q=(f._data(m,"events")||{})[c.type]&&f._data(m,"handle"),q&&q.apply(m,d),q=o&&m[o],q&&f.acceptData(m)&&q.apply(m,d)===!1&&c.preventDefault();c.type=h,!g&&!c.isDefaultPrevented()&&(!p._default||p._default.apply(e.ownerDocument,d)===!1)&&(h!=="click"||!f.nodeName(e,"a"))&&f.acceptData(e)&&o&&e[h]&&(h!=="focus"&&h!=="blur"||c.target.offsetWidth!==0)&&!f.isWindow(e)&&(n=e[o],n&&(e[o]=null),f.event.triggered=h,e[h](),f.event.triggered=b,n&&(e[o]=n));return c.result}},dispatch:function(c){c=f.event.fix(c||a.event);var d=(f._data(this,"events")||{})[c.type]||[],e=d.delegateCount,g=[].slice.call(arguments,0),h=!c.exclusive&&!c.namespace,i=f.event.special[c.type]||{},j=[],k,l,m,n,o,p,q,r,s,t,u;g[0]=c,c.delegateTarget=this;if(!i.preDispatch||i.preDispatch.call(this,c)!==!1){if(e&&(!c.button||c.type!=="click")){n=f(this),n.context=this.ownerDocument||this;for(m=c.target;m!=this;m=m.parentNode||this)if(m.disabled!==!0){p={},r=[],n[0]=m;for(k=0;k<e;k++)s=d[k],t=s.selector,p[t]===b&&(p[t]=s.quick?H(m,s.quick):n.is(t)),p[t]&&r.push(s);r.length&&j.push({elem:m,matches:r})}}d.length>e&&j.push({elem:this,matches:d.slice(e)});for(k=0;k<j.length&&!c.isPropagationStopped();k++){q=j[k],c.currentTarget=q.elem;for(l=0;l<q.matches.length&&!c.isImmediatePropagationStopped();l++){s=q.matches[l];if(h||!c.namespace&&!s.namespace||c.namespace_re&&c.namespace_re.test(s.namespace))c.data=s.data,c.handleObj=s,o=((f.event.special[s.origType]||{}).handle||s.handler).apply(q.elem,g),o!==b&&(c.result=o,o===!1&&(c.preventDefault(),c.stopPropagation()))}}i.postDispatch&&i.postDispatch.call(this,c);return c.result}},props:"attrChange attrName relatedNode srcElement altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),fixHooks:{},keyHooks:{props:"char charCode key keyCode".split(" "),filter:function(a,b){a.which==null&&(a.which=b.charCode!=null?b.charCode:b.keyCode);return a}},mouseHooks:{props:"button buttons clientX clientY fromElement offsetX offsetY pageX pageY screenX screenY toElement".split(" "),filter:function(a,d){var e,f,g,h=d.button,i=d.fromElement;a.pageX==null&&d.clientX!=null&&(e=a.target.ownerDocument||c,f=e.documentElement,g=e.body,a.pageX=d.clientX+(f&&f.scrollLeft||g&&g.scrollLeft||0)-(f&&f.clientLeft||g&&g.clientLeft||0),a.pageY=d.clientY+(f&&f.scrollTop||g&&g.scrollTop||0)-(f&&f.clientTop||g&&g.clientTop||0)),!a.relatedTarget&&i&&(a.relatedTarget=i===a.target?d.toElement:i),!a.which&&h!==b&&(a.which=h&1?1:h&2?3:h&4?2:0);return a}},fix:function(a){if(a[f.expando])return a;var d,e,g=a,h=f.event.fixHooks[a.type]||{},i=h.props?this.props.concat(h.props):this.props;a=f.Event(g);for(d=i.length;d;)e=i[--d],a[e]=g[e];a.target||(a.target=g.srcElement||c),a.target.nodeType===3&&(a.target=a.target.parentNode),a.metaKey===b&&(a.metaKey=a.ctrlKey);return h.filter?h.filter(a,g):a},special:{ready:{setup:f.bindReady},load:{noBubble:!0},focus:{delegateType:"focusin"},blur:{delegateType:"focusout"},beforeunload:{setup:function(a,b,c){f.isWindow(this)&&(this.onbeforeunload=c)},teardown:function(a,b){this.onbeforeunload===b&&(this.onbeforeunload=null)}}},simulate:function(a,b,c,d){var e=f.extend(new f.Event,c,{type:a,isSimulated:!0,originalEvent:{}});d?f.event.trigger(e,null,b):f.event.dispatch.call(b,e),e.isDefaultPrevented()&&c.preventDefault()}},f.event.handle=f.event.dispatch,f.removeEvent=c.removeEventListener?function(a,b,c){a.removeEventListener&&a.removeEventListener(b,c,!1)}:function(a,b,c){a.detachEvent&&a.detachEvent("on"+b,c)},f.Event=function(a,b){if(!(this instanceof f.Event))return new f.Event(a,b);a&&a.type?(this.originalEvent=a,this.type=a.type,this.isDefaultPrevented=a.defaultPrevented||a.returnValue===!1||a.getPreventDefault&&a.getPreventDefault()?K:J):this.type=a,b&&f.extend(this,b),this.timeStamp=a&&a.timeStamp||f.now(),this[f.expando]=!0},f.Event.prototype={preventDefault:function(){this.isDefaultPrevented=K;var a=this.originalEvent;!a||(a.preventDefault?a.preventDefault():a.returnValue=!1)},stopPropagation:function(){this.isPropagationStopped=K;var a=this.originalEvent;!a||(a.stopPropagation&&a.stopPropagation(),a.cancelBubble=!0)},stopImmediatePropagation:function(){this.isImmediatePropagationStopped=K,this.stopPropagation()},isDefaultPrevented:J,isPropagationStopped:J,isImmediatePropagationStopped:J},f.each({mouseenter:"mouseover",mouseleave:"mouseout"},function(a,b){f.event.special[a]={delegateType:b,bindType:b,handle:function(a){var c=this,d=a.relatedTarget,e=a.handleObj,g=e.selector,h;if(!d||d!==c&&!f.contains(c,d))a.type=e.origType,h=e.handler.apply(this,arguments),a.type=b;return h}}}),f.support.submitBubbles||(f.event.special.submit={setup:function(){if(f.nodeName(this,"form"))return!1;f.event.add(this,"click._submit keypress._submit",function(a){var c=a.target,d=f.nodeName(c,"input")||f.nodeName(c,"button")?c.form:b;d&&!d._submit_attached&&(f.event.add(d,"submit._submit",function(a){a._submit_bubble=!0}),d._submit_attached=!0)})},postDispatch:function(a){a._submit_bubble&&(delete a._submit_bubble,this.parentNode&&!a.isTrigger&&f.event.simulate("submit",this.parentNode,a,!0))},teardown:function(){if(f.nodeName(this,"form"))return!1;f.event.remove(this,"._submit")}}),f.support.changeBubbles||(f.event.special.change={setup:function(){if(z.test(this.nodeName)){if(this.type==="checkbox"||this.type==="radio")f.event.add(this,"propertychange._change",function(a){a.originalEvent.propertyName==="checked"&&(this._just_changed=!0)}),f.event.add(this,"click._change",function(a){this._just_changed&&!a.isTrigger&&(this._just_changed=!1,f.event.simulate("change",this,a,!0))});return!1}f.event.add(this,"beforeactivate._change",function(a){var b=a.target;z.test(b.nodeName)&&!b._change_attached&&(f.event.add(b,"change._change",function(a){this.parentNode&&!a.isSimulated&&!a.isTrigger&&f.event.simulate("change",this.parentNode,a,!0)}),b._change_attached=!0)})},handle:function(a){var b=a.target;if(this!==b||a.isSimulated||a.isTrigger||b.type!=="radio"&&b.type!=="checkbox")return a.handleObj.handler.apply(this,arguments)},teardown:function(){f.event.remove(this,"._change");return z.test(this.nodeName)}}),f.support.focusinBubbles||f.each({focus:"focusin",blur:"focusout"},function(a,b){var d=0,e=function(a){f.event.simulate(b,a.target,f.event.fix(a),!0)};f.event.special[b]={setup:function(){d++===0&&c.addEventListener(a,e,!0)},teardown:function(){--d===0&&c.removeEventListener(a,e,!0)}}}),f.fn.extend({on:function(a,c,d,e,g){var h,i;if(typeof a=="object"){typeof c!="string"&&(d=d||c,c=b);for(i in a)this.on(i,c,d,a[i],g);return this}d==null&&e==null?(e=c,d=c=b):e==null&&(typeof c=="string"?(e=d,d=b):(e=d,d=c,c=b));if(e===!1)e=J;else if(!e)return this;g===1&&(h=e,e=function(a){f().off(a);return h.apply(this,arguments)},e.guid=h.guid||(h.guid=f.guid++));return this.each(function(){f.event.add(this,a,e,d,c)})},one:function(a,b,c,d){return this.on(a,b,c,d,1)},off:function(a,c,d){if(a&&a.preventDefault&&a.handleObj){var e=a.handleObj;f(a.delegateTarget).off(e.namespace?e.origType+"."+e.namespace:e.origType,e.selector,e.handler);return this}if(typeof a=="object"){for(var g in a)this.off(g,c,a[g]);return this}if(c===!1||typeof c=="function")d=c,c=b;d===!1&&(d=J);return this.each(function(){f.event.remove(this,a,d,c)})},bind:function(a,b,c){return this.on(a,null,b,c)},unbind:function(a,b){return this.off(a,null,b)},live:function(a,b,c){f(this.context).on(a,this.selector,b,c);return this},die:function(a,b){f(this.context).off(a,this.selector||"**",b);return this},delegate:function(a,b,c,d){return this.on(b,a,c,d)},undelegate:function(a,b,c){return arguments.length==1?this.off(a,"**"):this.off(b,a,c)},trigger:function(a,b){return this.each(function(){f.event.trigger(a,b,this)})},triggerHandler:function(a,b){if(this[0])return f.event.trigger(a,b,this[0],!0)},toggle:function(a){var b=arguments,c=a.guid||f.guid++,d=0,e=function(c){var e=(f._data(this,"lastToggle"+a.guid)||0)%d;f._data(this,"lastToggle"+a.guid,e+1),c.preventDefault();return b[e].apply(this,arguments)||!1};e.guid=c;while(d<b.length)b[d++].guid=c;return this.click(e)},hover:function(a,b){return this.mouseenter(a).mouseleave(b||a)}}),f.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error contextmenu".split(" "),function(a,b){f.fn[b]=function(a,c){c==null&&(c=a,a=null);return arguments.length>0?this.on(b,null,a,c):this.trigger(b)},f.attrFn&&(f.attrFn[b]=!0),C.test(b)&&(f.event.fixHooks[b]=f.event.keyHooks),D.test(b)&&(f.event.fixHooks[b]=f.event.mouseHooks)}),function(){function x(a,b,c,e,f,g){for(var h=0,i=e.length;h<i;h++){var j=e[h];if(j){var k=!1;j=j[a];while(j){if(j[d]===c){k=e[j.sizset];break}if(j.nodeType===1){g||(j[d]=c,j.sizset=h);if(typeof b!="string"){if(j===b){k=!0;break}}else if(m.filter(b,[j]).length>0){k=j;break}}j=j[a]}e[h]=k}}}function w(a,b,c,e,f,g){for(var h=0,i=e.length;h<i;h++){var j=e[h];if(j){var k=!1;j=j[a];while(j){if(j[d]===c){k=e[j.sizset];break}j.nodeType===1&&!g&&(j[d]=c,j.sizset=h);if(j.nodeName.toLowerCase()===b){k=j;break}j=j[a]}e[h]=k}}}var a=/((?:\((?:\([^()]+\)|[^()]+)+\)|\[(?:\[[^\[\]]*\]|['"][^'"]*['"]|[^\[\]'"]+)+\]|\\.|[^ >+~,(\[\\]+)+|[>+~])(\s*,\s*)?((?:.|\r|\n)*)/g,d="sizcache"+(Math.random()+"").replace(".",""),e=0,g=Object.prototype.toString,h=!1,i=!0,j=/\\/g,k=/\r\n/g,l=/\W/;[0,0].sort(function(){i=!1;return 0});var m=function(b,d,e,f){e=e||[],d=d||c;var h=d;if(d.nodeType!==1&&d.nodeType!==9)return[];if(!b||typeof b!="string")return e;var i,j,k,l,n,q,r,t,u=!0,v=m.isXML(d),w=[],x=b;do{a.exec(""),i=a.exec(x);if(i){x=i[3],w.push(i[1]);if(i[2]){l=i[3];break}}}while(i);if(w.length>1&&p.exec(b))if(w.length===2&&o.relative[w[0]])j=y(w[0]+w[1],d,f);else{j=o.relative[w[0]]?[d]:m(w.shift(),d);while(w.length)b=w.shift(),o.relative[b]&&(b+=w.shift()),j=y(b,j,f)}else{!f&&w.length>1&&d.nodeType===9&&!v&&o.match.ID.test(w[0])&&!o.match.ID.test(w[w.length-1])&&(n=m.find(w.shift(),d,v),d=n.expr?m.filter(n.expr,n.set)[0]:n.set[0]);if(d){n=f?{expr:w.pop(),set:s(f)}:m.find(w.pop(),w.length===1&&(w[0]==="~"||w[0]==="+")&&d.parentNode?d.parentNode:d,v),j=n.expr?m.filter(n.expr,n.set):n.set,w.length>0?k=s(j):u=!1;while(w.length)q=w.pop(),r=q,o.relative[q]?r=w.pop():q="",r==null&&(r=d),o.relative[q](k,r,v)}else k=w=[]}k||(k=j),k||m.error(q||b);if(g.call(k)==="[object Array]")if(!u)e.push.apply(e,k);else if(d&&d.nodeType===1)for(t=0;k[t]!=null;t++)k[t]&&(k[t]===!0||k[t].nodeType===1&&m.contains(d,k[t]))&&e.push(j[t]);else for(t=0;k[t]!=null;t++)k[t]&&k[t].nodeType===1&&e.push(j[t]);else s(k,e);l&&(m(l,h,e,f),m.uniqueSort(e));return e};m.uniqueSort=function(a){if(u){h=i,a.sort(u);if(h)for(var b=1;b<a.length;b++)a[b]===a[b-1]&&a.splice(b--,1)}return a},m.matches=function(a,b){return m(a,null,null,b)},m.matchesSelector=function(a,b){return m(b,null,null,[a]).length>0},m.find=function(a,b,c){var d,e,f,g,h,i;if(!a)return[];for(e=0,f=o.order.length;e<f;e++){h=o.order[e];if(g=o.leftMatch[h].exec(a)){i=g[1],g.splice(1,1);if(i.substr(i.length-1)!=="\\"){g[1]=(g[1]||"").replace(j,""),d=o.find[h](g,b,c);if(d!=null){a=a.replace(o.match[h],"");break}}}}d||(d=typeof b.getElementsByTagName!="undefined"?b.getElementsByTagName("*"):[]);return{set:d,expr:a}},m.filter=function(a,c,d,e){var f,g,h,i,j,k,l,n,p,q=a,r=[],s=c,t=c&&c[0]&&m.isXML(c[0]);while(a&&c.length){for(h in o.filter)if((f=o.leftMatch[h].exec(a))!=null&&f[2]){k=o.filter[h],l=f[1],g=!1,f.splice(1,1);if(l.substr(l.length-1)==="\\")continue;s===r&&(r=[]);if(o.preFilter[h]){f=o.preFilter[h](f,s,d,r,e,t);if(!f)g=i=!0;else if(f===!0)continue}if(f)for(n=0;(j=s[n])!=null;n++)j&&(i=k(j,f,n,s),p=e^i,d&&i!=null?p?g=!0:s[n]=!1:p&&(r.push(j),g=!0));if(i!==b){d||(s=r),a=a.replace(o.match[h],"");if(!g)return[];break}}if(a===q)if(g==null)m.error(a);else break;q=a}return s},m.error=function(a){throw new Error("Syntax error, unrecognized expression: "+a)};var n=m.getText=function(a){var b,c,d=a.nodeType,e="";if(d){if(d===1||d===9||d===11){if(typeof a.textContent=="string")return a.textContent;if(typeof a.innerText=="string")return a.innerText.replace(k,"");for(a=a.firstChild;a;a=a.nextSibling)e+=n(a)}else if(d===3||d===4)return a.nodeValue}else for(b=0;c=a[b];b++)c.nodeType!==8&&(e+=n(c));return e},o=m.selectors={order:["ID","NAME","TAG"],match:{ID:/#((?:[\w\u00c0-\uFFFF\-]|\\.)+)/,CLASS:/\.((?:[\w\u00c0-\uFFFF\-]|\\.)+)/,NAME:/\[name=['"]*((?:[\w\u00c0-\uFFFF\-]|\\.)+)['"]*\]/,ATTR:/\[\s*((?:[\w\u00c0-\uFFFF\-]|\\.)+)\s*(?:(\S?=)\s*(?:(['"])(.*?)\3|(#?(?:[\w\u00c0-\uFFFF\-]|\\.)*)|)|)\s*\]/,TAG:/^((?:[\w\u00c0-\uFFFF\*\-]|\\.)+)/,CHILD:/:(only|nth|last|first)-child(?:\(\s*(even|odd|(?:[+\-]?\d+|(?:[+\-]?\d*)?n\s*(?:[+\-]\s*\d+)?))\s*\))?/,POS:/:(nth|eq|gt|lt|first|last|even|odd)(?:\((\d*)\))?(?=[^\-]|$)/,PSEUDO:/:((?:[\w\u00c0-\uFFFF\-]|\\.)+)(?:\((['"]?)((?:\([^\)]+\)|[^\(\)]*)+)\2\))?/},leftMatch:{},attrMap:{"class":"className","for":"htmlFor"},attrHandle:{href:function(a){return a.getAttribute("href")},type:function(a){return a.getAttribute("type")}},relative:{"+":function(a,b){var c=typeof b=="string",d=c&&!l.test(b),e=c&&!d;d&&(b=b.toLowerCase());for(var f=0,g=a.length,h;f<g;f++)if(h=a[f]){while((h=h.previousSibling)&&h.nodeType!==1);a[f]=e||h&&h.nodeName.toLowerCase()===b?h||!1:h===b}e&&m.filter(b,a,!0)},">":function(a,b){var c,d=typeof b=="string",e=0,f=a.length;if(d&&!l.test(b)){b=b.toLowerCase();for(;e<f;e++){c=a[e];if(c){var g=c.parentNode;a[e]=g.nodeName.toLowerCase()===b?g:!1}}}else{for(;e<f;e++)c=a[e],c&&(a[e]=d?c.parentNode:c.parentNode===b);d&&m.filter(b,a,!0)}},"":function(a,b,c){var d,f=e++,g=x;typeof b=="string"&&!l.test(b)&&(b=b.toLowerCase(),d=b,g=w),g("parentNode",b,f,a,d,c)},"~":function(a,b,c){var d,f=e++,g=x;typeof b=="string"&&!l.test(b)&&(b=b.toLowerCase(),d=b,g=w),g("previousSibling",b,f,a,d,c)}},find:{ID:function(a,b,c){if(typeof b.getElementById!="undefined"&&!c){var d=b.getElementById(a[1]);return d&&d.parentNode?[d]:[]}},NAME:function(a,b){if(typeof b.getElementsByName!="undefined"){var c=[],d=b.getElementsByName(a[1]);for(var e=0,f=d.length;e<f;e++)d[e].getAttribute("name")===a[1]&&c.push(d[e]);return c.length===0?null:c}},TAG:function(a,b){if(typeof b.getElementsByTagName!="undefined")return b.getElementsByTagName(a[1])}},preFilter:{CLASS:function(a,b,c,d,e,f){a=" "+a[1].replace(j,"")+" ";if(f)return a;for(var g=0,h;(h=b[g])!=null;g++)h&&(e^(h.className&&(" "+h.className+" ").replace(/[\t\n\r]/g," ").indexOf(a)>=0)?c||d.push(h):c&&(b[g]=!1));return!1},ID:function(a){return a[1].replace(j,"")},TAG:function(a,b){return a[1].replace(j,"").toLowerCase()},CHILD:function(a){if(a[1]==="nth"){a[2]||m.error(a[0]),a[2]=a[2].replace(/^\+|\s*/g,"");var b=/(-?)(\d*)(?:n([+\-]?\d*))?/.exec(a[2]==="even"&&"2n"||a[2]==="odd"&&"2n+1"||!/\D/.test(a[2])&&"0n+"+a[2]||a[2]);a[2]=b[1]+(b[2]||1)-0,a[3]=b[3]-0}else a[2]&&m.error(a[0]);a[0]=e++;return a},ATTR:function(a,b,c,d,e,f){var g=a[1]=a[1].replace(j,"");!f&&o.attrMap[g]&&(a[1]=o.attrMap[g]),a[4]=(a[4]||a[5]||"").replace(j,""),a[2]==="~="&&(a[4]=" "+a[4]+" ");return a},PSEUDO:function(b,c,d,e,f){if(b[1]==="not")if((a.exec(b[3])||"").length>1||/^\w/.test(b[3]))b[3]=m(b[3],null,null,c);else{var g=m.filter(b[3],c,d,!0^f);d||e.push.apply(e,g);return!1}else if(o.match.POS.test(b[0])||o.match.CHILD.test(b[0]))return!0;return b},POS:function(a){a.unshift(!0);return a}},filters:{enabled:function(a){return a.disabled===!1&&a.type!=="hidden"},disabled:function(a){return a.disabled===!0},checked:function(a){return a.checked===!0},selected:function(a){a.parentNode&&a.parentNode.selectedIndex;return a.selected===!0},parent:function(a){return!!a.firstChild},empty:function(a){return!a.firstChild},has:function(a,b,c){return!!m(c[3],a).length},header:function(a){return/h\d/i.test(a.nodeName)},text:function(a){var b=a.getAttribute("type"),c=a.type;return a.nodeName.toLowerCase()==="input"&&"text"===c&&(b===c||b===null)},radio:function(a){return a.nodeName.toLowerCase()==="input"&&"radio"===a.type},checkbox:function(a){return a.nodeName.toLowerCase()==="input"&&"checkbox"===a.type},file:function(a){return a.nodeName.toLowerCase()==="input"&&"file"===a.type},password:function(a){return a.nodeName.toLowerCase()==="input"&&"password"===a.type},submit:function(a){var b=a.nodeName.toLowerCase();return(b==="input"||b==="button")&&"submit"===a.type},image:function(a){return a.nodeName.toLowerCase()==="input"&&"image"===a.type},reset:function(a){var b=a.nodeName.toLowerCase();return(b==="input"||b==="button")&&"reset"===a.type},button:function(a){var b=a.nodeName.toLowerCase();return b==="input"&&"button"===a.type||b==="button"},input:function(a){return/input|select|textarea|button/i.test(a.nodeName)},focus:function(a){return a===a.ownerDocument.activeElement}},setFilters:{first:function(a,b){return b===0},last:function(a,b,c,d){return b===d.length-1},even:function(a,b){return b%2===0},odd:function(a,b){return b%2===1},lt:function(a,b,c){return b<c[3]-0},gt:function(a,b,c){return b>c[3]-0},nth:function(a,b,c){return c[3]-0===b},eq:function(a,b,c){return c[3]-0===b}},filter:{PSEUDO:function(a,b,c,d){var e=b[1],f=o.filters[e];if(f)return f(a,c,b,d);if(e==="contains")return(a.textContent||a.innerText||n([a])||"").indexOf(b[3])>=0;if(e==="not"){var g=b[3];for(var h=0,i=g.length;h<i;h++)if(g[h]===a)return!1;return!0}m.error(e)},CHILD:function(a,b){var c,e,f,g,h,i,j,k=b[1],l=a;switch(k){case"only":case"first":while(l=l.previousSibling)if(l.nodeType===1)return!1;if(k==="first")return!0;l=a;case"last":while(l=l.nextSibling)if(l.nodeType===1)return!1;return!0;case"nth":c=b[2],e=b[3];if(c===1&&e===0)return!0;f=b[0],g=a.parentNode;if(g&&(g[d]!==f||!a.nodeIndex)){i=0;for(l=g.firstChild;l;l=l.nextSibling)l.nodeType===1&&(l.nodeIndex=++i);g[d]=f}j=a.nodeIndex-e;return c===0?j===0:j%c===0&&j/c>=0}},ID:function(a,b){return a.nodeType===1&&a.getAttribute("id")===b},TAG:function(a,b){return b==="*"&&a.nodeType===1||!!a.nodeName&&a.nodeName.toLowerCase()===b},CLASS:function(a,b){return(" "+(a.className||a.getAttribute("class"))+" ").indexOf(b)>-1},ATTR:function(a,b){var c=b[1],d=m.attr?m.attr(a,c):o.attrHandle[c]?o.attrHandle[c](a):a[c]!=null?a[c]:a.getAttribute(c),e=d+"",f=b[2],g=b[4];return d==null?f==="!=":!f&&m.attr?d!=null:f==="="?e===g:f==="*="?e.indexOf(g)>=0:f==="~="?(" "+e+" ").indexOf(g)>=0:g?f==="!="?e!==g:f==="^="?e.indexOf(g)===0:f==="$="?e.substr(e.length-g.length)===g:f==="|="?e===g||e.substr(0,g.length+1)===g+"-":!1:e&&d!==!1},POS:function(a,b,c,d){var e=b[2],f=o.setFilters[e];if(f)return f(a,c,b,d)}}},p=o.match.POS,q=function(a,b){return"\\"+(b-0+1)};for(var r in o.match)o.match[r]=new RegExp(o.match[r].source+/(?![^\[]*\])(?![^\(]*\))/.source),o.leftMatch[r]=new RegExp(/(^(?:.|\r|\n)*?)/.source+o.match[r].source.replace(/\\(\d+)/g,q));o.match.globalPOS=p;var s=function(a,b){a=Array.prototype.slice.call(a,0);if(b){b.push.apply(b,a);return b}return a};try{Array.prototype.slice.call(c.documentElement.childNodes,0)[0].nodeType}catch(t){s=function(a,b){var c=0,d=b||[];if(g.call(a)==="[object Array]")Array.prototype.push.apply(d,a);else if(typeof a.length=="number")for(var e=a.length;c<e;c++)d.push(a[c]);else for(;a[c];c++)d.push(a[c]);return d}}var u,v;c.documentElement.compareDocumentPosition?u=function(a,b){if(a===b){h=!0;return 0}if(!a.compareDocumentPosition||!b.compareDocumentPosition)return a.compareDocumentPosition?-1:1;return a.compareDocumentPosition(b)&4?-1:1}:(u=function(a,b){if(a===b){h=!0;return 0}if(a.sourceIndex&&b.sourceIndex)return a.sourceIndex-b.sourceIndex;var c,d,e=[],f=[],g=a.parentNode,i=b.parentNode,j=g;if(g===i)return v(a,b);if(!g)return-1;if(!i)return 1;while(j)e.unshift(j),j=j.parentNode;j=i;while(j)f.unshift(j),j=j.parentNode;c=e.length,d=f.length;for(var k=0;k<c&&k<d;k++)if(e[k]!==f[k])return v(e[k],f[k]);return k===c?v(a,f[k],-1):v(e[k],b,1)},v=function(a,b,c){if(a===b)return c;var d=a.nextSibling;while(d){if(d===b)return-1;d=d.nextSibling}return 1}),function(){var a=c.createElement("div"),d="script"+(new Date).getTime(),e=c.documentElement;a.innerHTML="<a name='"+d+"'/>",e.insertBefore(a,e.firstChild),c.getElementById(d)&&(o.find.ID=function(a,c,d){if(typeof c.getElementById!="undefined"&&!d){var e=c.getElementById(a[1]);return e?e.id===a[1]||typeof e.getAttributeNode!="undefined"&&e.getAttributeNode("id").nodeValue===a[1]?[e]:b:[]}},o.filter.ID=function(a,b){var c=typeof a.getAttributeNode!="undefined"&&a.getAttributeNode("id");return a.nodeType===1&&c&&c.nodeValue===b}),e.removeChild(a),e=a=null}(),function(){var a=c.createElement("div");a.appendChild(c.createComment("")),a.getElementsByTagName("*").length>0&&(o.find.TAG=function(a,b){var c=b.getElementsByTagName(a[1]);if(a[1]==="*"){var d=[];for(var e=0;c[e];e++)c[e].nodeType===1&&d.push(c[e]);c=d}return c}),a.innerHTML="<a href='#'></a>",a.firstChild&&typeof a.firstChild.getAttribute!="undefined"&&a.firstChild.getAttribute("href")!=="#"&&(o.attrHandle.href=function(a){return a.getAttribute("href",2)}),a=null}(),c.querySelectorAll&&function(){var a=m,b=c.createElement("div"),d="__sizzle__";b.innerHTML="<p class='TEST'></p>";if(!b.querySelectorAll||b.querySelectorAll(".TEST").length!==0){m=function(b,e,f,g){e=e||c;if(!g&&!m.isXML(e)){var h=/^(\w+$)|^\.([\w\-]+$)|^#([\w\-]+$)/.exec(b);if(h&&(e.nodeType===1||e.nodeType===9)){if(h[1])return s(e.getElementsByTagName(b),f);if(h[2]&&o.find.CLASS&&e.getElementsByClassName)return s(e.getElementsByClassName(h[2]),f)}if(e.nodeType===9){if(b==="body"&&e.body)return s([e.body],f);if(h&&h[3]){var i=e.getElementById(h[3]);if(!i||!i.parentNode)return s([],f);if(i.id===h[3])return s([i],f)}try{return s(e.querySelectorAll(b),f)}catch(j){}}else if(e.nodeType===1&&e.nodeName.toLowerCase()!=="object"){var k=e,l=e.getAttribute("id"),n=l||d,p=e.parentNode,q=/^\s*[+~]/.test(b);l?n=n.replace(/'/g,"\\$&"):e.setAttribute("id",n),q&&p&&(e=e.parentNode);try{if(!q||p)return s(e.querySelectorAll("[id='"+n+"'] "+b),f)}catch(r){}finally{l||k.removeAttribute("id")}}}return a(b,e,f,g)};for(var e in a)m[e]=a[e];b=null}}(),function(){var a=c.documentElement,b=a.matchesSelector||a.mozMatchesSelector||a.webkitMatchesSelector||a.msMatchesSelector;if(b){var d=!b.call(c.createElement("div"),"div"),e=!1;try{b.call(c.documentElement,"[test!='']:sizzle")}catch(f){e=!0}m.matchesSelector=function(a,c){c=c.replace(/\=\s*([^'"\]]*)\s*\]/g,"='$1']");if(!m.isXML(a))try{if(e||!o.match.PSEUDO.test(c)&&!/!=/.test(c)){var f=b.call(a,c);if(f||!d||a.document&&a.document.nodeType!==11)return f}}catch(g){}return m(c,null,null,[a]).length>0}}}(),function(){var a=c.createElement("div");a.innerHTML="<div class='test e'></div><div class='test'></div>";if(!!a.getElementsByClassName&&a.getElementsByClassName("e").length!==0){a.lastChild.className="e";if(a.getElementsByClassName("e").length===1)return;o.order.splice(1,0,"CLASS"),o.find.CLASS=function(a,b,c){if(typeof b.getElementsByClassName!="undefined"&&!c)return b.getElementsByClassName(a[1])},a=null}}(),c.documentElement.contains?m.contains=function(a,b){return a!==b&&(a.contains?a.contains(b):!0)}:c.documentElement.compareDocumentPosition?m.contains=function(a,b){return!!(a.compareDocumentPosition(b)&16)}:m.contains=function(){return!1},m.isXML=function(a){var b=(a?a.ownerDocument||a:0).documentElement;return b?b.nodeName!=="HTML":!1};var y=function(a,b,c){var d,e=[],f="",g=b.nodeType?[b]:b;while(d=o.match.PSEUDO.exec(a))f+=d[0],a=a.replace(o.match.PSEUDO,"");a=o.relative[a]?a+"*":a;for(var h=0,i=g.length;h<i;h++)m(a,g[h],e,c);return m.filter(f,e)};m.attr=f.attr,m.selectors.attrMap={},f.find=m,f.expr=m.selectors,f.expr[":"]=f.expr.filters,f.unique=m.uniqueSort,f.text=m.getText,f.isXMLDoc=m.isXML,f.contains=m.contains}();var L=/Until$/,M=/^(?:parents|prevUntil|prevAll)/,N=/,/,O=/^.[^:#\[\.,]*$/,P=Array.prototype.slice,Q=f.expr.match.globalPOS,R={children:!0,contents:!0,next:!0,prev:!0};f.fn.extend({find:function(a){var b=this,c,d;if(typeof a!="string")return f(a).filter(function(){for(c=0,d=b.length;c<d;c++)if(f.contains(b[c],this))return!0});var e=this.pushStack("","find",a),g,h,i;for(c=0,d=this.length;c<d;c++){g=e.length,f.find(a,this[c],e);if(c>0)for(h=g;h<e.length;h++)for(i=0;i<g;i++)if(e[i]===e[h]){e.splice(h--,1);break}}return e},has:function(a){var b=f(a);return this.filter(function(){for(var a=0,c=b.length;a<c;a++)if(f.contains(this,b[a]))return!0})},not:function(a){return this.pushStack(T(this,a,!1),"not",a)},filter:function(a){return this.pushStack(T(this,a,!0),"filter",a)},is:function(a){return!!a&&(typeof a=="string"?Q.test(a)?f(a,this.context).index(this[0])>=0:f.filter(a,this).length>0:this.filter(a).length>0)},closest:function(a,b){var c=[],d,e,g=this[0];if(f.isArray(a)){var h=1;while(g&&g.ownerDocument&&g!==b){for(d=0;d<a.length;d++)f(g).is(a[d])&&c.push({selector:a[d],elem:g,level:h});g=g.parentNode,h++}return c}var i=Q.test(a)||typeof a!="string"?f(a,b||this.context):0;for(d=0,e=this.length;d<e;d++){g=this[d];while(g){if(i?i.index(g)>-1:f.find.matchesSelector(g,a)){c.push(g);break}g=g.parentNode;if(!g||!g.ownerDocument||g===b||g.nodeType===11)break}}c=c.length>1?f.unique(c):c;return this.pushStack(c,"closest",a)},index:function(a){if(!a)return this[0]&&this[0].parentNode?this.prevAll().length:-1;if(typeof a=="string")return f.inArray(this[0],f(a));return f.inArray(a.jquery?a[0]:a,this)},add:function(a,b){var c=typeof a=="string"?f(a,b):f.makeArray(a&&a.nodeType?[a]:a),d=f.merge(this.get(),c);return this.pushStack(S(c[0])||S(d[0])?d:f.unique(d))},andSelf:function(){return this.add(this.prevObject)}}),f.each({parent:function(a){var b=a.parentNode;return b&&b.nodeType!==11?b:null},parents:function(a){return f.dir(a,"parentNode")},parentsUntil:function(a,b,c){return f.dir(a,"parentNode",c)},next:function(a){return f.nth(a,2,"nextSibling")},prev:function(a){return f.nth(a,2,"previousSibling")},nextAll:function(a){return f.dir(a,"nextSibling")},prevAll:function(a){return f.dir(a,"previousSibling")},nextUntil:function(a,b,c){return f.dir(a,"nextSibling",c)},prevUntil:function(a,b,c){return f.dir(a,"previousSibling",c)},siblings:function(a){return f.sibling((a.parentNode||{}).firstChild,a)},children:function(a){return f.sibling(a.firstChild)},contents:function(a){return f.nodeName(a,"iframe")?a.contentDocument||a.contentWindow.document:f.makeArray(a.childNodes)}},function(a,b){f.fn[a]=function(c,d){var e=f.map(this,b,c);L.test(a)||(d=c),d&&typeof d=="string"&&(e=f.filter(d,e)),e=this.length>1&&!R[a]?f.unique(e):e,(this.length>1||N.test(d))&&M.test(a)&&(e=e.reverse());return this.pushStack(e,a,P.call(arguments).join(","))}}),f.extend({filter:function(a,b,c){c&&(a=":not("+a+")");return b.length===1?f.find.matchesSelector(b[0],a)?[b[0]]:[]:f.find.matches(a,b)},dir:function(a,c,d){var e=[],g=a[c];while(g&&g.nodeType!==9&&(d===b||g.nodeType!==1||!f(g).is(d)))g.nodeType===1&&e.push(g),g=g[c];return e},nth:function(a,b,c,d){b=b||1;var e=0;for(;a;a=a[c])if(a.nodeType===1&&++e===b)break;return a},sibling:function(a,b){var c=[];for(;a;a=a.nextSibling)a.nodeType===1&&a!==b&&c.push(a);return c}});var V="abbr|article|aside|audio|bdi|canvas|data|datalist|details|figcaption|figure|footer|header|hgroup|mark|meter|nav|output|progress|section|summary|time|video",W=/ jQuery\d+="(?:\d+|null)"/g,X=/^\s+/,Y=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/ig,Z=/<([\w:]+)/,$=/<tbody/i,_=/<|&#?\w+;/,ba=/<(?:script|style)/i,bb=/<(?:script|object|embed|option|style)/i,bc=new RegExp("<(?:"+V+")[\\s/>]","i"),bd=/checked\s*(?:[^=]|=\s*.checked.)/i,be=/\/(java|ecma)script/i,bf=/^\s*<!(?:\[CDATA\[|\-\-)/,bg={option:[1,"<select multiple='multiple'>","</select>"],legend:[1,"<fieldset>","</fieldset>"],thead:[1,"<table>","</table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],col:[2,"<table><tbody></tbody><colgroup>","</colgroup></table>"],area:[1,"<map>","</map>"],_default:[0,"",""]},bh=U(c);bg.optgroup=bg.option,bg.tbody=bg.tfoot=bg.colgroup=bg.caption=bg.thead,bg.th=bg.td,f.support.htmlSerialize||(bg._default=[1,"div<div>","</div>"]),f.fn.extend({text:function(a){return f.access(this,function(a){return a===b?f.text(this):this.empty().append((this[0]&&this[0].ownerDocument||c).createTextNode(a))},null,a,arguments.length)},wrapAll:function(a){if(f.isFunction(a))return this.each(function(b){f(this).wrapAll(a.call(this,b))});if(this[0]){var b=f(a,this[0].ownerDocument).eq(0).clone(!0);this[0].parentNode&&b.insertBefore(this[0]),b.map(function(){var a=this;while(a.firstChild&&a.firstChild.nodeType===1)a=a.firstChild;return a}).append(this)}return this},wrapInner:function(a){if(f.isFunction(a))return this.each(function(b){f(this).wrapInner(a.call(this,b))});return this.each(function(){var b=f(this),c=b.contents();c.length?c.wrapAll(a):b.append(a)})},wrap:function(a){var b=f.isFunction(a);return this.each(function(c){f(this).wrapAll(b?a.call(this,c):a)})},unwrap:function(){return this.parent().each(function(){f.nodeName(this,"body")||f(this).replaceWith(this.childNodes)}).end()},append:function(){return this.domManip(arguments,!0,function(a){this.nodeType===1&&this.appendChild(a)})},prepend:function(){return this.domManip(arguments,!0,function(a){this.nodeType===1&&this.insertBefore(a,this.firstChild)})},before:function(){if(this[0]&&this[0].parentNode)return this.domManip(arguments,!1,function(a){this.parentNode.insertBefore(a,this)});if(arguments.length){var a=f
.clean(arguments);a.push.apply(a,this.toArray());return this.pushStack(a,"before",arguments)}},after:function(){if(this[0]&&this[0].parentNode)return this.domManip(arguments,!1,function(a){this.parentNode.insertBefore(a,this.nextSibling)});if(arguments.length){var a=this.pushStack(this,"after",arguments);a.push.apply(a,f.clean(arguments));return a}},remove:function(a,b){for(var c=0,d;(d=this[c])!=null;c++)if(!a||f.filter(a,[d]).length)!b&&d.nodeType===1&&(f.cleanData(d.getElementsByTagName("*")),f.cleanData([d])),d.parentNode&&d.parentNode.removeChild(d);return this},empty:function(){for(var a=0,b;(b=this[a])!=null;a++){b.nodeType===1&&f.cleanData(b.getElementsByTagName("*"));while(b.firstChild)b.removeChild(b.firstChild)}return this},clone:function(a,b){a=a==null?!1:a,b=b==null?a:b;return this.map(function(){return f.clone(this,a,b)})},html:function(a){return f.access(this,function(a){var c=this[0]||{},d=0,e=this.length;if(a===b)return c.nodeType===1?c.innerHTML.replace(W,""):null;if(typeof a=="string"&&!ba.test(a)&&(f.support.leadingWhitespace||!X.test(a))&&!bg[(Z.exec(a)||["",""])[1].toLowerCase()]){a=a.replace(Y,"<$1></$2>");try{for(;d<e;d++)c=this[d]||{},c.nodeType===1&&(f.cleanData(c.getElementsByTagName("*")),c.innerHTML=a);c=0}catch(g){}}c&&this.empty().append(a)},null,a,arguments.length)},replaceWith:function(a){if(this[0]&&this[0].parentNode){if(f.isFunction(a))return this.each(function(b){var c=f(this),d=c.html();c.replaceWith(a.call(this,b,d))});typeof a!="string"&&(a=f(a).detach());return this.each(function(){var b=this.nextSibling,c=this.parentNode;f(this).remove(),b?f(b).before(a):f(c).append(a)})}return this.length?this.pushStack(f(f.isFunction(a)?a():a),"replaceWith",a):this},detach:function(a){return this.remove(a,!0)},domManip:function(a,c,d){var e,g,h,i,j=a[0],k=[];if(!f.support.checkClone&&arguments.length===3&&typeof j=="string"&&bd.test(j))return this.each(function(){f(this).domManip(a,c,d,!0)});if(f.isFunction(j))return this.each(function(e){var g=f(this);a[0]=j.call(this,e,c?g.html():b),g.domManip(a,c,d)});if(this[0]){i=j&&j.parentNode,f.support.parentNode&&i&&i.nodeType===11&&i.childNodes.length===this.length?e={fragment:i}:e=f.buildFragment(a,this,k),h=e.fragment,h.childNodes.length===1?g=h=h.firstChild:g=h.firstChild;if(g){c=c&&f.nodeName(g,"tr");for(var l=0,m=this.length,n=m-1;l<m;l++)d.call(c?bi(this[l],g):this[l],e.cacheable||m>1&&l<n?f.clone(h,!0,!0):h)}k.length&&f.each(k,function(a,b){b.src?f.ajax({type:"GET",global:!1,url:b.src,async:!1,dataType:"script"}):f.globalEval((b.text||b.textContent||b.innerHTML||"").replace(bf,"/*$0*/")),b.parentNode&&b.parentNode.removeChild(b)})}return this}}),f.buildFragment=function(a,b,d){var e,g,h,i,j=a[0];b&&b[0]&&(i=b[0].ownerDocument||b[0]),i.createDocumentFragment||(i=c),a.length===1&&typeof j=="string"&&j.length<512&&i===c&&j.charAt(0)==="<"&&!bb.test(j)&&(f.support.checkClone||!bd.test(j))&&(f.support.html5Clone||!bc.test(j))&&(g=!0,h=f.fragments[j],h&&h!==1&&(e=h)),e||(e=i.createDocumentFragment(),f.clean(a,i,e,d)),g&&(f.fragments[j]=h?e:1);return{fragment:e,cacheable:g}},f.fragments={},f.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(a,b){f.fn[a]=function(c){var d=[],e=f(c),g=this.length===1&&this[0].parentNode;if(g&&g.nodeType===11&&g.childNodes.length===1&&e.length===1){e[b](this[0]);return this}for(var h=0,i=e.length;h<i;h++){var j=(h>0?this.clone(!0):this).get();f(e[h])[b](j),d=d.concat(j)}return this.pushStack(d,a,e.selector)}}),f.extend({clone:function(a,b,c){var d,e,g,h=f.support.html5Clone||f.isXMLDoc(a)||!bc.test("<"+a.nodeName+">")?a.cloneNode(!0):bo(a);if((!f.support.noCloneEvent||!f.support.noCloneChecked)&&(a.nodeType===1||a.nodeType===11)&&!f.isXMLDoc(a)){bk(a,h),d=bl(a),e=bl(h);for(g=0;d[g];++g)e[g]&&bk(d[g],e[g])}if(b){bj(a,h);if(c){d=bl(a),e=bl(h);for(g=0;d[g];++g)bj(d[g],e[g])}}d=e=null;return h},clean:function(a,b,d,e){var g,h,i,j=[];b=b||c,typeof b.createElement=="undefined"&&(b=b.ownerDocument||b[0]&&b[0].ownerDocument||c);for(var k=0,l;(l=a[k])!=null;k++){typeof l=="number"&&(l+="");if(!l)continue;if(typeof l=="string")if(!_.test(l))l=b.createTextNode(l);else{l=l.replace(Y,"<$1></$2>");var m=(Z.exec(l)||["",""])[1].toLowerCase(),n=bg[m]||bg._default,o=n[0],p=b.createElement("div"),q=bh.childNodes,r;b===c?bh.appendChild(p):U(b).appendChild(p),p.innerHTML=n[1]+l+n[2];while(o--)p=p.lastChild;if(!f.support.tbody){var s=$.test(l),t=m==="table"&&!s?p.firstChild&&p.firstChild.childNodes:n[1]==="<table>"&&!s?p.childNodes:[];for(i=t.length-1;i>=0;--i)f.nodeName(t[i],"tbody")&&!t[i].childNodes.length&&t[i].parentNode.removeChild(t[i])}!f.support.leadingWhitespace&&X.test(l)&&p.insertBefore(b.createTextNode(X.exec(l)[0]),p.firstChild),l=p.childNodes,p&&(p.parentNode.removeChild(p),q.length>0&&(r=q[q.length-1],r&&r.parentNode&&r.parentNode.removeChild(r)))}var u;if(!f.support.appendChecked)if(l[0]&&typeof (u=l.length)=="number")for(i=0;i<u;i++)bn(l[i]);else bn(l);l.nodeType?j.push(l):j=f.merge(j,l)}if(d){g=function(a){return!a.type||be.test(a.type)};for(k=0;j[k];k++){h=j[k];if(e&&f.nodeName(h,"script")&&(!h.type||be.test(h.type)))e.push(h.parentNode?h.parentNode.removeChild(h):h);else{if(h.nodeType===1){var v=f.grep(h.getElementsByTagName("script"),g);j.splice.apply(j,[k+1,0].concat(v))}d.appendChild(h)}}}return j},cleanData:function(a){var b,c,d=f.cache,e=f.event.special,g=f.support.deleteExpando;for(var h=0,i;(i=a[h])!=null;h++){if(i.nodeName&&f.noData[i.nodeName.toLowerCase()])continue;c=i[f.expando];if(c){b=d[c];if(b&&b.events){for(var j in b.events)e[j]?f.event.remove(i,j):f.removeEvent(i,j,b.handle);b.handle&&(b.handle.elem=null)}g?delete i[f.expando]:i.removeAttribute&&i.removeAttribute(f.expando),delete d[c]}}}});var bp=/alpha\([^)]*\)/i,bq=/opacity=([^)]*)/,br=/([A-Z]|^ms)/g,bs=/^[\-+]?(?:\d*\.)?\d+$/i,bt=/^-?(?:\d*\.)?\d+(?!px)[^\d\s]+$/i,bu=/^([\-+])=([\-+.\de]+)/,bv=/^margin/,bw={position:"absolute",visibility:"hidden",display:"block"},bx=["Top","Right","Bottom","Left"],by,bz,bA;f.fn.css=function(a,c){return f.access(this,function(a,c,d){return d!==b?f.style(a,c,d):f.css(a,c)},a,c,arguments.length>1)},f.extend({cssHooks:{opacity:{get:function(a,b){if(b){var c=by(a,"opacity");return c===""?"1":c}return a.style.opacity}}},cssNumber:{fillOpacity:!0,fontWeight:!0,lineHeight:!0,opacity:!0,orphans:!0,widows:!0,zIndex:!0,zoom:!0},cssProps:{"float":f.support.cssFloat?"cssFloat":"styleFloat"},style:function(a,c,d,e){if(!!a&&a.nodeType!==3&&a.nodeType!==8&&!!a.style){var g,h,i=f.camelCase(c),j=a.style,k=f.cssHooks[i];c=f.cssProps[i]||i;if(d===b){if(k&&"get"in k&&(g=k.get(a,!1,e))!==b)return g;return j[c]}h=typeof d,h==="string"&&(g=bu.exec(d))&&(d=+(g[1]+1)*+g[2]+parseFloat(f.css(a,c)),h="number");if(d==null||h==="number"&&isNaN(d))return;h==="number"&&!f.cssNumber[i]&&(d+="px");if(!k||!("set"in k)||(d=k.set(a,d))!==b)try{j[c]=d}catch(l){}}},css:function(a,c,d){var e,g;c=f.camelCase(c),g=f.cssHooks[c],c=f.cssProps[c]||c,c==="cssFloat"&&(c="float");if(g&&"get"in g&&(e=g.get(a,!0,d))!==b)return e;if(by)return by(a,c)},swap:function(a,b,c){var d={},e,f;for(f in b)d[f]=a.style[f],a.style[f]=b[f];e=c.call(a);for(f in b)a.style[f]=d[f];return e}}),f.curCSS=f.css,c.defaultView&&c.defaultView.getComputedStyle&&(bz=function(a,b){var c,d,e,g,h=a.style;b=b.replace(br,"-$1").toLowerCase(),(d=a.ownerDocument.defaultView)&&(e=d.getComputedStyle(a,null))&&(c=e.getPropertyValue(b),c===""&&!f.contains(a.ownerDocument.documentElement,a)&&(c=f.style(a,b))),!f.support.pixelMargin&&e&&bv.test(b)&&bt.test(c)&&(g=h.width,h.width=c,c=e.width,h.width=g);return c}),c.documentElement.currentStyle&&(bA=function(a,b){var c,d,e,f=a.currentStyle&&a.currentStyle[b],g=a.style;f==null&&g&&(e=g[b])&&(f=e),bt.test(f)&&(c=g.left,d=a.runtimeStyle&&a.runtimeStyle.left,d&&(a.runtimeStyle.left=a.currentStyle.left),g.left=b==="fontSize"?"1em":f,f=g.pixelLeft+"px",g.left=c,d&&(a.runtimeStyle.left=d));return f===""?"auto":f}),by=bz||bA,f.each(["height","width"],function(a,b){f.cssHooks[b]={get:function(a,c,d){if(c)return a.offsetWidth!==0?bB(a,b,d):f.swap(a,bw,function(){return bB(a,b,d)})},set:function(a,b){return bs.test(b)?b+"px":b}}}),f.support.opacity||(f.cssHooks.opacity={get:function(a,b){return bq.test((b&&a.currentStyle?a.currentStyle.filter:a.style.filter)||"")?parseFloat(RegExp.$1)/100+"":b?"1":""},set:function(a,b){var c=a.style,d=a.currentStyle,e=f.isNumeric(b)?"alpha(opacity="+b*100+")":"",g=d&&d.filter||c.filter||"";c.zoom=1;if(b>=1&&f.trim(g.replace(bp,""))===""){c.removeAttribute("filter");if(d&&!d.filter)return}c.filter=bp.test(g)?g.replace(bp,e):g+" "+e}}),f(function(){f.support.reliableMarginRight||(f.cssHooks.marginRight={get:function(a,b){return f.swap(a,{display:"inline-block"},function(){return b?by(a,"margin-right"):a.style.marginRight})}})}),f.expr&&f.expr.filters&&(f.expr.filters.hidden=function(a){var b=a.offsetWidth,c=a.offsetHeight;return b===0&&c===0||!f.support.reliableHiddenOffsets&&(a.style&&a.style.display||f.css(a,"display"))==="none"},f.expr.filters.visible=function(a){return!f.expr.filters.hidden(a)}),f.each({margin:"",padding:"",border:"Width"},function(a,b){f.cssHooks[a+b]={expand:function(c){var d,e=typeof c=="string"?c.split(" "):[c],f={};for(d=0;d<4;d++)f[a+bx[d]+b]=e[d]||e[d-2]||e[0];return f}}});var bC=/%20/g,bD=/\[\]$/,bE=/\r?\n/g,bF=/#.*$/,bG=/^(.*?):[ \t]*([^\r\n]*)\r?$/mg,bH=/^(?:color|date|datetime|datetime-local|email|hidden|month|number|password|range|search|tel|text|time|url|week)$/i,bI=/^(?:about|app|app\-storage|.+\-extension|file|res|widget):$/,bJ=/^(?:GET|HEAD)$/,bK=/^\/\//,bL=/\?/,bM=/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,bN=/^(?:select|textarea)/i,bO=/\s+/,bP=/([?&])_=[^&]*/,bQ=/^([\w\+\.\-]+:)(?:\/\/([^\/?#:]*)(?::(\d+))?)?/,bR=f.fn.load,bS={},bT={},bU,bV,bW=["*/"]+["*"];try{bU=e.href}catch(bX){bU=c.createElement("a"),bU.href="",bU=bU.href}bV=bQ.exec(bU.toLowerCase())||[],f.fn.extend({load:function(a,c,d){if(typeof a!="string"&&bR)return bR.apply(this,arguments);if(!this.length)return this;var e=a.indexOf(" ");if(e>=0){var g=a.slice(e,a.length);a=a.slice(0,e)}var h="GET";c&&(f.isFunction(c)?(d=c,c=b):typeof c=="object"&&(c=f.param(c,f.ajaxSettings.traditional),h="POST"));var i=this;f.ajax({url:a,type:h,dataType:"html",data:c,complete:function(a,b,c){c=a.responseText,a.isResolved()&&(a.done(function(a){c=a}),i.html(g?f("<div>").append(c.replace(bM,"")).find(g):c)),d&&i.each(d,[c,b,a])}});return this},serialize:function(){return f.param(this.serializeArray())},serializeArray:function(){return this.map(function(){return this.elements?f.makeArray(this.elements):this}).filter(function(){return this.name&&!this.disabled&&(this.checked||bN.test(this.nodeName)||bH.test(this.type))}).map(function(a,b){var c=f(this).val();return c==null?null:f.isArray(c)?f.map(c,function(a,c){return{name:b.name,value:a.replace(bE,"\r\n")}}):{name:b.name,value:c.replace(bE,"\r\n")}}).get()}}),f.each("ajaxStart ajaxStop ajaxComplete ajaxError ajaxSuccess ajaxSend".split(" "),function(a,b){f.fn[b]=function(a){return this.on(b,a)}}),f.each(["get","post"],function(a,c){f[c]=function(a,d,e,g){f.isFunction(d)&&(g=g||e,e=d,d=b);return f.ajax({type:c,url:a,data:d,success:e,dataType:g})}}),f.extend({getScript:function(a,c){return f.get(a,b,c,"script")},getJSON:function(a,b,c){return f.get(a,b,c,"json")},ajaxSetup:function(a,b){b?b$(a,f.ajaxSettings):(b=a,a=f.ajaxSettings),b$(a,b);return a},ajaxSettings:{url:bU,isLocal:bI.test(bV[1]),global:!0,type:"GET",contentType:"application/x-www-form-urlencoded; charset=UTF-8",processData:!0,async:!0,accepts:{xml:"application/xml, text/xml",html:"text/html",text:"text/plain",json:"application/json, text/javascript","*":bW},contents:{xml:/xml/,html:/html/,json:/json/},responseFields:{xml:"responseXML",text:"responseText"},converters:{"* text":a.String,"text html":!0,"text json":f.parseJSON,"text xml":f.parseXML},flatOptions:{context:!0,url:!0}},ajaxPrefilter:bY(bS),ajaxTransport:bY(bT),ajax:function(a,c){function w(a,c,l,m){if(s!==2){s=2,q&&clearTimeout(q),p=b,n=m||"",v.readyState=a>0?4:0;var o,r,u,w=c,x=l?ca(d,v,l):b,y,z;if(a>=200&&a<300||a===304){if(d.ifModified){if(y=v.getResponseHeader("Last-Modified"))f.lastModified[k]=y;if(z=v.getResponseHeader("Etag"))f.etag[k]=z}if(a===304)w="notmodified",o=!0;else try{r=cb(d,x),w="success",o=!0}catch(A){w="parsererror",u=A}}else{u=w;if(!w||a)w="error",a<0&&(a=0)}v.status=a,v.statusText=""+(c||w),o?h.resolveWith(e,[r,w,v]):h.rejectWith(e,[v,w,u]),v.statusCode(j),j=b,t&&g.trigger("ajax"+(o?"Success":"Error"),[v,d,o?r:u]),i.fireWith(e,[v,w]),t&&(g.trigger("ajaxComplete",[v,d]),--f.active||f.event.trigger("ajaxStop"))}}typeof a=="object"&&(c=a,a=b),c=c||{};var d=f.ajaxSetup({},c),e=d.context||d,g=e!==d&&(e.nodeType||e instanceof f)?f(e):f.event,h=f.Deferred(),i=f.Callbacks("once memory"),j=d.statusCode||{},k,l={},m={},n,o,p,q,r,s=0,t,u,v={readyState:0,setRequestHeader:function(a,b){if(!s){var c=a.toLowerCase();a=m[c]=m[c]||a,l[a]=b}return this},getAllResponseHeaders:function(){return s===2?n:null},getResponseHeader:function(a){var c;if(s===2){if(!o){o={};while(c=bG.exec(n))o[c[1].toLowerCase()]=c[2]}c=o[a.toLowerCase()]}return c===b?null:c},overrideMimeType:function(a){s||(d.mimeType=a);return this},abort:function(a){a=a||"abort",p&&p.abort(a),w(0,a);return this}};h.promise(v),v.success=v.done,v.error=v.fail,v.complete=i.add,v.statusCode=function(a){if(a){var b;if(s<2)for(b in a)j[b]=[j[b],a[b]];else b=a[v.status],v.then(b,b)}return this},d.url=((a||d.url)+"").replace(bF,"").replace(bK,bV[1]+"//"),d.dataTypes=f.trim(d.dataType||"*").toLowerCase().split(bO),d.crossDomain==null&&(r=bQ.exec(d.url.toLowerCase()),d.crossDomain=!(!r||r[1]==bV[1]&&r[2]==bV[2]&&(r[3]||(r[1]==="http:"?80:443))==(bV[3]||(bV[1]==="http:"?80:443)))),d.data&&d.processData&&typeof d.data!="string"&&(d.data=f.param(d.data,d.traditional)),bZ(bS,d,c,v);if(s===2)return!1;t=d.global,d.type=d.type.toUpperCase(),d.hasContent=!bJ.test(d.type),t&&f.active++===0&&f.event.trigger("ajaxStart");if(!d.hasContent){d.data&&(d.url+=(bL.test(d.url)?"&":"?")+d.data,delete d.data),k=d.url;if(d.cache===!1){var x=f.now(),y=d.url.replace(bP,"$1_="+x);d.url=y+(y===d.url?(bL.test(d.url)?"&":"?")+"_="+x:"")}}(d.data&&d.hasContent&&d.contentType!==!1||c.contentType)&&v.setRequestHeader("Content-Type",d.contentType),d.ifModified&&(k=k||d.url,f.lastModified[k]&&v.setRequestHeader("If-Modified-Since",f.lastModified[k]),f.etag[k]&&v.setRequestHeader("If-None-Match",f.etag[k])),v.setRequestHeader("Accept",d.dataTypes[0]&&d.accepts[d.dataTypes[0]]?d.accepts[d.dataTypes[0]]+(d.dataTypes[0]!=="*"?", "+bW+"; q=0.01":""):d.accepts["*"]);for(u in d.headers)v.setRequestHeader(u,d.headers[u]);if(d.beforeSend&&(d.beforeSend.call(e,v,d)===!1||s===2)){v.abort();return!1}for(u in{success:1,error:1,complete:1})v[u](d[u]);p=bZ(bT,d,c,v);if(!p)w(-1,"No Transport");else{v.readyState=1,t&&g.trigger("ajaxSend",[v,d]),d.async&&d.timeout>0&&(q=setTimeout(function(){v.abort("timeout")},d.timeout));try{s=1,p.send(l,w)}catch(z){if(s<2)w(-1,z);else throw z}}return v},param:function(a,c){var d=[],e=function(a,b){b=f.isFunction(b)?b():b,d[d.length]=encodeURIComponent(a)+"="+encodeURIComponent(b)};c===b&&(c=f.ajaxSettings.traditional);if(f.isArray(a)||a.jquery&&!f.isPlainObject(a))f.each(a,function(){e(this.name,this.value)});else for(var g in a)b_(g,a[g],c,e);return d.join("&").replace(bC,"+")}}),f.extend({active:0,lastModified:{},etag:{}});var cc=f.now(),cd=/(\=)\?(&|$)|\?\?/i;f.ajaxSetup({jsonp:"callback",jsonpCallback:function(){return f.expando+"_"+cc++}}),f.ajaxPrefilter("json jsonp",function(b,c,d){var e=typeof b.data=="string"&&/^application\/x\-www\-form\-urlencoded/.test(b.contentType);if(b.dataTypes[0]==="jsonp"||b.jsonp!==!1&&(cd.test(b.url)||e&&cd.test(b.data))){var g,h=b.jsonpCallback=f.isFunction(b.jsonpCallback)?b.jsonpCallback():b.jsonpCallback,i=a[h],j=b.url,k=b.data,l="$1"+h+"$2";b.jsonp!==!1&&(j=j.replace(cd,l),b.url===j&&(e&&(k=k.replace(cd,l)),b.data===k&&(j+=(/\?/.test(j)?"&":"?")+b.jsonp+"="+h))),b.url=j,b.data=k,a[h]=function(a){g=[a]},d.always(function(){a[h]=i,g&&f.isFunction(i)&&a[h](g[0])}),b.converters["script json"]=function(){g||f.error(h+" was not called");return g[0]},b.dataTypes[0]="json";return"script"}}),f.ajaxSetup({accepts:{script:"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},contents:{script:/javascript|ecmascript/},converters:{"text script":function(a){f.globalEval(a);return a}}}),f.ajaxPrefilter("script",function(a){a.cache===b&&(a.cache=!1),a.crossDomain&&(a.type="GET",a.global=!1)}),f.ajaxTransport("script",function(a){if(a.crossDomain){var d,e=c.head||c.getElementsByTagName("head")[0]||c.documentElement;return{send:function(f,g){d=c.createElement("script"),d.async="async",a.scriptCharset&&(d.charset=a.scriptCharset),d.src=a.url,d.onload=d.onreadystatechange=function(a,c){if(c||!d.readyState||/loaded|complete/.test(d.readyState))d.onload=d.onreadystatechange=null,e&&d.parentNode&&e.removeChild(d),d=b,c||g(200,"success")},e.insertBefore(d,e.firstChild)},abort:function(){d&&d.onload(0,1)}}}});var ce=a.ActiveXObject?function(){for(var a in cg)cg[a](0,1)}:!1,cf=0,cg;f.ajaxSettings.xhr=a.ActiveXObject?function(){return!this.isLocal&&ch()||ci()}:ch,function(a){f.extend(f.support,{ajax:!!a,cors:!!a&&"withCredentials"in a})}(f.ajaxSettings.xhr()),f.support.ajax&&f.ajaxTransport(function(c){if(!c.crossDomain||f.support.cors){var d;return{send:function(e,g){var h=c.xhr(),i,j;c.username?h.open(c.type,c.url,c.async,c.username,c.password):h.open(c.type,c.url,c.async);if(c.xhrFields)for(j in c.xhrFields)h[j]=c.xhrFields[j];c.mimeType&&h.overrideMimeType&&h.overrideMimeType(c.mimeType),!c.crossDomain&&!e["X-Requested-With"]&&(e["X-Requested-With"]="XMLHttpRequest");try{for(j in e)h.setRequestHeader(j,e[j])}catch(k){}h.send(c.hasContent&&c.data||null),d=function(a,e){var j,k,l,m,n;try{if(d&&(e||h.readyState===4)){d=b,i&&(h.onreadystatechange=f.noop,ce&&delete cg[i]);if(e)h.readyState!==4&&h.abort();else{j=h.status,l=h.getAllResponseHeaders(),m={},n=h.responseXML,n&&n.documentElement&&(m.xml=n);try{m.text=h.responseText}catch(a){}try{k=h.statusText}catch(o){k=""}!j&&c.isLocal&&!c.crossDomain?j=m.text?200:404:j===1223&&(j=204)}}}catch(p){e||g(-1,p)}m&&g(j,k,m,l)},!c.async||h.readyState===4?d():(i=++cf,ce&&(cg||(cg={},f(a).unload(ce)),cg[i]=d),h.onreadystatechange=d)},abort:function(){d&&d(0,1)}}}});var cj={},ck,cl,cm=/^(?:toggle|show|hide)$/,cn=/^([+\-]=)?([\d+.\-]+)([a-z%]*)$/i,co,cp=[["height","marginTop","marginBottom","paddingTop","paddingBottom"],["width","marginLeft","marginRight","paddingLeft","paddingRight"],["opacity"]],cq;f.fn.extend({show:function(a,b,c){var d,e;if(a||a===0)return this.animate(ct("show",3),a,b,c);for(var g=0,h=this.length;g<h;g++)d=this[g],d.style&&(e=d.style.display,!f._data(d,"olddisplay")&&e==="none"&&(e=d.style.display=""),(e===""&&f.css(d,"display")==="none"||!f.contains(d.ownerDocument.documentElement,d))&&f._data(d,"olddisplay",cu(d.nodeName)));for(g=0;g<h;g++){d=this[g];if(d.style){e=d.style.display;if(e===""||e==="none")d.style.display=f._data(d,"olddisplay")||""}}return this},hide:function(a,b,c){if(a||a===0)return this.animate(ct("hide",3),a,b,c);var d,e,g=0,h=this.length;for(;g<h;g++)d=this[g],d.style&&(e=f.css(d,"display"),e!=="none"&&!f._data(d,"olddisplay")&&f._data(d,"olddisplay",e));for(g=0;g<h;g++)this[g].style&&(this[g].style.display="none");return this},_toggle:f.fn.toggle,toggle:function(a,b,c){var d=typeof a=="boolean";f.isFunction(a)&&f.isFunction(b)?this._toggle.apply(this,arguments):a==null||d?this.each(function(){var b=d?a:f(this).is(":hidden");f(this)[b?"show":"hide"]()}):this.animate(ct("toggle",3),a,b,c);return this},fadeTo:function(a,b,c,d){return this.filter(":hidden").css("opacity",0).show().end().animate({opacity:b},a,c,d)},animate:function(a,b,c,d){function g(){e.queue===!1&&f._mark(this);var b=f.extend({},e),c=this.nodeType===1,d=c&&f(this).is(":hidden"),g,h,i,j,k,l,m,n,o,p,q;b.animatedProperties={};for(i in a){g=f.camelCase(i),i!==g&&(a[g]=a[i],delete a[i]);if((k=f.cssHooks[g])&&"expand"in k){l=k.expand(a[g]),delete a[g];for(i in l)i in a||(a[i]=l[i])}}for(g in a){h=a[g],f.isArray(h)?(b.animatedProperties[g]=h[1],h=a[g]=h[0]):b.animatedProperties[g]=b.specialEasing&&b.specialEasing[g]||b.easing||"swing";if(h==="hide"&&d||h==="show"&&!d)return b.complete.call(this);c&&(g==="height"||g==="width")&&(b.overflow=[this.style.overflow,this.style.overflowX,this.style.overflowY],f.css(this,"display")==="inline"&&f.css(this,"float")==="none"&&(!f.support.inlineBlockNeedsLayout||cu(this.nodeName)==="inline"?this.style.display="inline-block":this.style.zoom=1))}b.overflow!=null&&(this.style.overflow="hidden");for(i in a)j=new f.fx(this,b,i),h=a[i],cm.test(h)?(q=f._data(this,"toggle"+i)||(h==="toggle"?d?"show":"hide":0),q?(f._data(this,"toggle"+i,q==="show"?"hide":"show"),j[q]()):j[h]()):(m=cn.exec(h),n=j.cur(),m?(o=parseFloat(m[2]),p=m[3]||(f.cssNumber[i]?"":"px"),p!=="px"&&(f.style(this,i,(o||1)+p),n=(o||1)/j.cur()*n,f.style(this,i,n+p)),m[1]&&(o=(m[1]==="-="?-1:1)*o+n),j.custom(n,o,p)):j.custom(n,h,""));return!0}var e=f.speed(b,c,d);if(f.isEmptyObject(a))return this.each(e.complete,[!1]);a=f.extend({},a);return e.queue===!1?this.each(g):this.queue(e.queue,g)},stop:function(a,c,d){typeof a!="string"&&(d=c,c=a,a=b),c&&a!==!1&&this.queue(a||"fx",[]);return this.each(function(){function h(a,b,c){var e=b[c];f.removeData(a,c,!0),e.stop(d)}var b,c=!1,e=f.timers,g=f._data(this);d||f._unmark(!0,this);if(a==null)for(b in g)g[b]&&g[b].stop&&b.indexOf(".run")===b.length-4&&h(this,g,b);else g[b=a+".run"]&&g[b].stop&&h(this,g,b);for(b=e.length;b--;)e[b].elem===this&&(a==null||e[b].queue===a)&&(d?e[b](!0):e[b].saveState(),c=!0,e.splice(b,1));(!d||!c)&&f.dequeue(this,a)})}}),f.each({slideDown:ct("show",1),slideUp:ct("hide",1),slideToggle:ct("toggle",1),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"},fadeToggle:{opacity:"toggle"}},function(a,b){f.fn[a]=function(a,c,d){return this.animate(b,a,c,d)}}),f.extend({speed:function(a,b,c){var d=a&&typeof a=="object"?f.extend({},a):{complete:c||!c&&b||f.isFunction(a)&&a,duration:a,easing:c&&b||b&&!f.isFunction(b)&&b};d.duration=f.fx.off?0:typeof d.duration=="number"?d.duration:d.duration in f.fx.speeds?f.fx.speeds[d.duration]:f.fx.speeds._default;if(d.queue==null||d.queue===!0)d.queue="fx";d.old=d.complete,d.complete=function(a){f.isFunction(d.old)&&d.old.call(this),d.queue?f.dequeue(this,d.queue):a!==!1&&f._unmark(this)};return d},easing:{linear:function(a){return a},swing:function(a){return-Math.cos(a*Math.PI)/2+.5}},timers:[],fx:function(a,b,c){this.options=b,this.elem=a,this.prop=c,b.orig=b.orig||{}}}),f.fx.prototype={update:function(){this.options.step&&this.options.step.call(this.elem,this.now,this),(f.fx.step[this.prop]||f.fx.step._default)(this)},cur:function(){if(this.elem[this.prop]!=null&&(!this.elem.style||this.elem.style[this.prop]==null))return this.elem[this.prop];var a,b=f.css(this.elem,this.prop);return isNaN(a=parseFloat(b))?!b||b==="auto"?0:b:a},custom:function(a,c,d){function h(a){return e.step(a)}var e=this,g=f.fx;this.startTime=cq||cr(),this.end=c,this.now=this.start=a,this.pos=this.state=0,this.unit=d||this.unit||(f.cssNumber[this.prop]?"":"px"),h.queue=this.options.queue,h.elem=this.elem,h.saveState=function(){f._data(e.elem,"fxshow"+e.prop)===b&&(e.options.hide?f._data(e.elem,"fxshow"+e.prop,e.start):e.options.show&&f._data(e.elem,"fxshow"+e.prop,e.end))},h()&&f.timers.push(h)&&!co&&(co=setInterval(g.tick,g.interval))},show:function(){var a=f._data(this.elem,"fxshow"+this.prop);this.options.orig[this.prop]=a||f.style(this.elem,this.prop),this.options.show=!0,a!==b?this.custom(this.cur(),a):this.custom(this.prop==="width"||this.prop==="height"?1:0,this.cur()),f(this.elem).show()},hide:function(){this.options.orig[this.prop]=f._data(this.elem,"fxshow"+this.prop)||f.style(this.elem,this.prop),this.options.hide=!0,this.custom(this.cur(),0)},step:function(a){var b,c,d,e=cq||cr(),g=!0,h=this.elem,i=this.options;if(a||e>=i.duration+this.startTime){this.now=this.end,this.pos=this.state=1,this.update(),i.animatedProperties[this.prop]=!0;for(b in i.animatedProperties)i.animatedProperties[b]!==!0&&(g=!1);if(g){i.overflow!=null&&!f.support.shrinkWrapBlocks&&f.each(["","X","Y"],function(a,b){h.style["overflow"+b]=i.overflow[a]}),i.hide&&f(h).hide();if(i.hide||i.show)for(b in i.animatedProperties)f.style(h,b,i.orig[b]),f.removeData(h,"fxshow"+b,!0),f.removeData(h,"toggle"+b,!0);d=i.complete,d&&(i.complete=!1,d.call(h))}return!1}i.duration==Infinity?this.now=e:(c=e-this.startTime,this.state=c/i.duration,this.pos=f.easing[i.animatedProperties[this.prop]](this.state,c,0,1,i.duration),this.now=this.start+(this.end-this.start)*this.pos),this.update();return!0}},f.extend(f.fx,{tick:function(){var a,b=f.timers,c=0;for(;c<b.length;c++)a=b[c],!a()&&b[c]===a&&b.splice(c--,1);b.length||f.fx.stop()},interval:13,stop:function(){clearInterval(co),co=null},speeds:{slow:600,fast:200,_default:400},step:{opacity:function(a){f.style(a.elem,"opacity",a.now)},_default:function(a){a.elem.style&&a.elem.style[a.prop]!=null?a.elem.style[a.prop]=a.now+a.unit:a.elem[a.prop]=a.now}}}),f.each(cp.concat.apply([],cp),function(a,b){b.indexOf("margin")&&(f.fx.step[b]=function(a){f.style(a.elem,b,Math.max(0,a.now)+a.unit)})}),f.expr&&f.expr.filters&&(f.expr.filters.animated=function(a){return f.grep(f.timers,function(b){return a===b.elem}).length});var cv,cw=/^t(?:able|d|h)$/i,cx=/^(?:body|html)$/i;"getBoundingClientRect"in c.documentElement?cv=function(a,b,c,d){try{d=a.getBoundingClientRect()}catch(e){}if(!d||!f.contains(c,a))return d?{top:d.top,left:d.left}:{top:0,left:0};var g=b.body,h=cy(b),i=c.clientTop||g.clientTop||0,j=c.clientLeft||g.clientLeft||0,k=h.pageYOffset||f.support.boxModel&&c.scrollTop||g.scrollTop,l=h.pageXOffset||f.support.boxModel&&c.scrollLeft||g.scrollLeft,m=d.top+k-i,n=d.left+l-j;return{top:m,left:n}}:cv=function(a,b,c){var d,e=a.offsetParent,g=a,h=b.body,i=b.defaultView,j=i?i.getComputedStyle(a,null):a.currentStyle,k=a.offsetTop,l=a.offsetLeft;while((a=a.parentNode)&&a!==h&&a!==c){if(f.support.fixedPosition&&j.position==="fixed")break;d=i?i.getComputedStyle(a,null):a.currentStyle,k-=a.scrollTop,l-=a.scrollLeft,a===e&&(k+=a.offsetTop,l+=a.offsetLeft,f.support.doesNotAddBorder&&(!f.support.doesAddBorderForTableAndCells||!cw.test(a.nodeName))&&(k+=parseFloat(d.borderTopWidth)||0,l+=parseFloat(d.borderLeftWidth)||0),g=e,e=a.offsetParent),f.support.subtractsBorderForOverflowNotVisible&&d.overflow!=="visible"&&(k+=parseFloat(d.borderTopWidth)||0,l+=parseFloat(d.borderLeftWidth)||0),j=d}if(j.position==="relative"||j.position==="static")k+=h.offsetTop,l+=h.offsetLeft;f.support.fixedPosition&&j.position==="fixed"&&(k+=Math.max(c.scrollTop,h.scrollTop),l+=Math.max(c.scrollLeft,h.scrollLeft));return{top:k,left:l}},f.fn.offset=function(a){if(arguments.length)return a===b?this:this.each(function(b){f.offset.setOffset(this,a,b)});var c=this[0],d=c&&c.ownerDocument;if(!d)return null;if(c===d.body)return f.offset.bodyOffset(c);return cv(c,d,d.documentElement)},f.offset={bodyOffset:function(a){var b=a.offsetTop,c=a.offsetLeft;f.support.doesNotIncludeMarginInBodyOffset&&(b+=parseFloat(f.css(a,"marginTop"))||0,c+=parseFloat(f.css(a,"marginLeft"))||0);return{top:b,left:c}},setOffset:function(a,b,c){var d=f.css(a,"position");d==="static"&&(a.style.position="relative");var e=f(a),g=e.offset(),h=f.css(a,"top"),i=f.css(a,"left"),j=(d==="absolute"||d==="fixed")&&f.inArray("auto",[h,i])>-1,k={},l={},m,n;j?(l=e.position(),m=l.top,n=l.left):(m=parseFloat(h)||0,n=parseFloat(i)||0),f.isFunction(b)&&(b=b.call(a,c,g)),b.top!=null&&(k.top=b.top-g.top+m),b.left!=null&&(k.left=b.left-g.left+n),"using"in b?b.using.call(a,k):e.css(k)}},f.fn.extend({position:function(){if(!this[0])return null;var a=this[0],b=this.offsetParent(),c=this.offset(),d=cx.test(b[0].nodeName)?{top:0,left:0}:b.offset();c.top-=parseFloat(f.css(a,"marginTop"))||0,c.left-=parseFloat(f.css(a,"marginLeft"))||0,d.top+=parseFloat(f.css(b[0],"borderTopWidth"))||0,d.left+=parseFloat(f.css(b[0],"borderLeftWidth"))||0;return{top:c.top-d.top,left:c.left-d.left}},offsetParent:function(){return this.map(function(){var a=this.offsetParent||c.body;while(a&&!cx.test(a.nodeName)&&f.css(a,"position")==="static")a=a.offsetParent;return a})}}),f.each({scrollLeft:"pageXOffset",scrollTop:"pageYOffset"},function(a,c){var d=/Y/.test(c);f.fn[a]=function(e){return f.access(this,function(a,e,g){var h=cy(a);if(g===b)return h?c in h?h[c]:f.support.boxModel&&h.document.documentElement[e]||h.document.body[e]:a[e];h?h.scrollTo(d?f(h).scrollLeft():g,d?g:f(h).scrollTop()):a[e]=g},a,e,arguments.length,null)}}),f.each({Height:"height",Width:"width"},function(a,c){var d="client"+a,e="scroll"+a,g="offset"+a;f.fn["inner"+a]=function(){var a=this[0];return a?a.style?parseFloat(f.css(a,c,"padding")):this[c]():null},f.fn["outer"+a]=function(a){var b=this[0];return b?b.style?parseFloat(f.css(b,c,a?"margin":"border")):this[c]():null},f.fn[c]=function(a){return f.access(this,function(a,c,h){var i,j,k,l;if(f.isWindow(a)){i=a.document,j=i.documentElement[d];return f.support.boxModel&&j||i.body&&i.body[d]||j}if(a.nodeType===9){i=a.documentElement;if(i[d]>=i[e])return i[d];return Math.max(a.body[e],i[e],a.body[g],i[g])}if(h===b){k=f.css(a,c),l=parseFloat(k);return f.isNumeric(l)?l:k}f(a).css(c,h)},c,a,arguments.length,null)}}),a.jQuery=a.$=f,typeof define=="function"&&define.amd&&define.amd.jQuery&&define("jquery",[],function(){return f})})(window);
/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.core.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){function c(b,c){var e=b.nodeName.toLowerCase();if("area"===e){var f=b.parentNode,g=f.name,h;return!b.href||!g||f.nodeName.toLowerCase()!=="map"?!1:(h=a("img[usemap=#"+g+"]")[0],!!h&&d(h))}return(/input|select|textarea|button|object/.test(e)?!b.disabled:"a"==e?b.href||c:c)&&d(b)}function d(b){return!a(b).parents().andSelf().filter(function(){return a.curCSS(this,"visibility")==="hidden"||a.expr.filters.hidden(this)}).length}a.ui=a.ui||{};if(a.ui.version)return;a.extend(a.ui,{version:"1.8.21",keyCode:{ALT:18,BACKSPACE:8,CAPS_LOCK:20,COMMA:188,COMMAND:91,COMMAND_LEFT:91,COMMAND_RIGHT:93,CONTROL:17,DELETE:46,DOWN:40,END:35,ENTER:13,ESCAPE:27,HOME:36,INSERT:45,LEFT:37,MENU:93,NUMPAD_ADD:107,NUMPAD_DECIMAL:110,NUMPAD_DIVIDE:111,NUMPAD_ENTER:108,NUMPAD_MULTIPLY:106,NUMPAD_SUBTRACT:109,PAGE_DOWN:34,PAGE_UP:33,PERIOD:190,RIGHT:39,SHIFT:16,SPACE:32,TAB:9,UP:38,WINDOWS:91}}),a.fn.extend({propAttr:a.fn.prop||a.fn.attr,_focus:a.fn.focus,focus:function(b,c){return typeof b=="number"?this.each(function(){var d=this;setTimeout(function(){a(d).focus(),c&&c.call(d)},b)}):this._focus.apply(this,arguments)},scrollParent:function(){var b;return a.browser.msie&&/(static|relative)/.test(this.css("position"))||/absolute/.test(this.css("position"))?b=this.parents().filter(function(){return/(relative|absolute|fixed)/.test(a.curCSS(this,"position",1))&&/(auto|scroll)/.test(a.curCSS(this,"overflow",1)+a.curCSS(this,"overflow-y",1)+a.curCSS(this,"overflow-x",1))}).eq(0):b=this.parents().filter(function(){return/(auto|scroll)/.test(a.curCSS(this,"overflow",1)+a.curCSS(this,"overflow-y",1)+a.curCSS(this,"overflow-x",1))}).eq(0),/fixed/.test(this.css("position"))||!b.length?a(document):b},zIndex:function(c){if(c!==b)return this.css("zIndex",c);if(this.length){var d=a(this[0]),e,f;while(d.length&&d[0]!==document){e=d.css("position");if(e==="absolute"||e==="relative"||e==="fixed"){f=parseInt(d.css("zIndex"),10);if(!isNaN(f)&&f!==0)return f}d=d.parent()}}return 0},disableSelection:function(){return this.bind((a.support.selectstart?"selectstart":"mousedown")+".ui-disableSelection",function(a){a.preventDefault()})},enableSelection:function(){return this.unbind(".ui-disableSelection")}}),a.each(["Width","Height"],function(c,d){function h(b,c,d,f){return a.each(e,function(){c-=parseFloat(a.curCSS(b,"padding"+this,!0))||0,d&&(c-=parseFloat(a.curCSS(b,"border"+this+"Width",!0))||0),f&&(c-=parseFloat(a.curCSS(b,"margin"+this,!0))||0)}),c}var e=d==="Width"?["Left","Right"]:["Top","Bottom"],f=d.toLowerCase(),g={innerWidth:a.fn.innerWidth,innerHeight:a.fn.innerHeight,outerWidth:a.fn.outerWidth,outerHeight:a.fn.outerHeight};a.fn["inner"+d]=function(c){return c===b?g["inner"+d].call(this):this.each(function(){a(this).css(f,h(this,c)+"px")})},a.fn["outer"+d]=function(b,c){return typeof b!="number"?g["outer"+d].call(this,b):this.each(function(){a(this).css(f,h(this,b,!0,c)+"px")})}}),a.extend(a.expr[":"],{data:function(b,c,d){return!!a.data(b,d[3])},focusable:function(b){return c(b,!isNaN(a.attr(b,"tabindex")))},tabbable:function(b){var d=a.attr(b,"tabindex"),e=isNaN(d);return(e||d>=0)&&c(b,!e)}}),a(function(){var b=document.body,c=b.appendChild(c=document.createElement("div"));c.offsetHeight,a.extend(c.style,{minHeight:"100px",height:"auto",padding:0,borderWidth:0}),a.support.minHeight=c.offsetHeight===100,a.support.selectstart="onselectstart"in c,b.removeChild(c).style.display="none"}),a.extend(a.ui,{plugin:{add:function(b,c,d){var e=a.ui[b].prototype;for(var f in d)e.plugins[f]=e.plugins[f]||[],e.plugins[f].push([c,d[f]])},call:function(a,b,c){var d=a.plugins[b];if(!d||!a.element[0].parentNode)return;for(var e=0;e<d.length;e++)a.options[d[e][0]]&&d[e][1].apply(a.element,c)}},contains:function(a,b){return document.compareDocumentPosition?a.compareDocumentPosition(b)&16:a!==b&&a.contains(b)},hasScroll:function(b,c){if(a(b).css("overflow")==="hidden")return!1;var d=c&&c==="left"?"scrollLeft":"scrollTop",e=!1;return b[d]>0?!0:(b[d]=1,e=b[d]>0,b[d]=0,e)},isOverAxis:function(a,b,c){return a>b&&a<b+c},isOver:function(b,c,d,e,f,g){return a.ui.isOverAxis(b,d,f)&&a.ui.isOverAxis(c,e,g)}})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.widget.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){if(a.cleanData){var c=a.cleanData;a.cleanData=function(b){for(var d=0,e;(e=b[d])!=null;d++)try{a(e).triggerHandler("remove")}catch(f){}c(b)}}else{var d=a.fn.remove;a.fn.remove=function(b,c){return this.each(function(){return c||(!b||a.filter(b,[this]).length)&&a("*",this).add([this]).each(function(){try{a(this).triggerHandler("remove")}catch(b){}}),d.call(a(this),b,c)})}}a.widget=function(b,c,d){var e=b.split(".")[0],f;b=b.split(".")[1],f=e+"-"+b,d||(d=c,c=a.Widget),a.expr[":"][f]=function(c){return!!a.data(c,b)},a[e]=a[e]||{},a[e][b]=function(a,b){arguments.length&&this._createWidget(a,b)};var g=new c;g.options=a.extend(!0,{},g.options),a[e][b].prototype=a.extend(!0,g,{namespace:e,widgetName:b,widgetEventPrefix:a[e][b].prototype.widgetEventPrefix||b,widgetBaseClass:f},d),a.widget.bridge(b,a[e][b])},a.widget.bridge=function(c,d){a.fn[c]=function(e){var f=typeof e=="string",g=Array.prototype.slice.call(arguments,1),h=this;return e=!f&&g.length?a.extend.apply(null,[!0,e].concat(g)):e,f&&e.charAt(0)==="_"?h:(f?this.each(function(){var d=a.data(this,c),f=d&&a.isFunction(d[e])?d[e].apply(d,g):d;if(f!==d&&f!==b)return h=f,!1}):this.each(function(){var b=a.data(this,c);b?b.option(e||{})._init():a.data(this,c,new d(e,this))}),h)}},a.Widget=function(a,b){arguments.length&&this._createWidget(a,b)},a.Widget.prototype={widgetName:"widget",widgetEventPrefix:"",options:{disabled:!1},_createWidget:function(b,c){a.data(c,this.widgetName,this),this.element=a(c),this.options=a.extend(!0,{},this.options,this._getCreateOptions(),b);var d=this;this.element.bind("remove."+this.widgetName,function(){d.destroy()}),this._create(),this._trigger("create"),this._init()},_getCreateOptions:function(){return a.metadata&&a.metadata.get(this.element[0])[this.widgetName]},_create:function(){},_init:function(){},destroy:function(){this.element.unbind("."+this.widgetName).removeData(this.widgetName),this.widget().unbind("."+this.widgetName).removeAttr("aria-disabled").removeClass(this.widgetBaseClass+"-disabled "+"ui-state-disabled")},widget:function(){return this.element},option:function(c,d){var e=c;if(arguments.length===0)return a.extend({},this.options);if(typeof c=="string"){if(d===b)return this.options[c];e={},e[c]=d}return this._setOptions(e),this},_setOptions:function(b){var c=this;return a.each(b,function(a,b){c._setOption(a,b)}),this},_setOption:function(a,b){return this.options[a]=b,a==="disabled"&&this.widget()[b?"addClass":"removeClass"](this.widgetBaseClass+"-disabled"+" "+"ui-state-disabled").attr("aria-disabled",b),this},enable:function(){return this._setOption("disabled",!1)},disable:function(){return this._setOption("disabled",!0)},_trigger:function(b,c,d){var e,f,g=this.options[b];d=d||{},c=a.Event(c),c.type=(b===this.widgetEventPrefix?b:this.widgetEventPrefix+b).toLowerCase(),c.target=this.element[0],f=c.originalEvent;if(f)for(e in f)e in c||(c[e]=f[e]);return this.element.trigger(c,d),!(a.isFunction(g)&&g.call(this.element[0],c,d)===!1||c.isDefaultPrevented())}}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.mouse.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){var c=!1;a(document).mouseup(function(a){c=!1}),a.widget("ui.mouse",{options:{cancel:":input,option",distance:1,delay:0},_mouseInit:function(){var b=this;this.element.bind("mousedown."+this.widgetName,function(a){return b._mouseDown(a)}).bind("click."+this.widgetName,function(c){if(!0===a.data(c.target,b.widgetName+".preventClickEvent"))return a.removeData(c.target,b.widgetName+".preventClickEvent"),c.stopImmediatePropagation(),!1}),this.started=!1},_mouseDestroy:function(){this.element.unbind("."+this.widgetName),a(document).unbind("mousemove."+this.widgetName,this._mouseMoveDelegate).unbind("mouseup."+this.widgetName,this._mouseUpDelegate)},_mouseDown:function(b){if(c)return;this._mouseStarted&&this._mouseUp(b),this._mouseDownEvent=b;var d=this,e=b.which==1,f=typeof this.options.cancel=="string"&&b.target.nodeName?a(b.target).closest(this.options.cancel).length:!1;if(!e||f||!this._mouseCapture(b))return!0;this.mouseDelayMet=!this.options.delay,this.mouseDelayMet||(this._mouseDelayTimer=setTimeout(function(){d.mouseDelayMet=!0},this.options.delay));if(this._mouseDistanceMet(b)&&this._mouseDelayMet(b)){this._mouseStarted=this._mouseStart(b)!==!1;if(!this._mouseStarted)return b.preventDefault(),!0}return!0===a.data(b.target,this.widgetName+".preventClickEvent")&&a.removeData(b.target,this.widgetName+".preventClickEvent"),this._mouseMoveDelegate=function(a){return d._mouseMove(a)},this._mouseUpDelegate=function(a){return d._mouseUp(a)},a(document).bind("mousemove."+this.widgetName,this._mouseMoveDelegate).bind("mouseup."+this.widgetName,this._mouseUpDelegate),b.preventDefault(),c=!0,!0},_mouseMove:function(b){return!a.browser.msie||document.documentMode>=9||!!b.button?this._mouseStarted?(this._mouseDrag(b),b.preventDefault()):(this._mouseDistanceMet(b)&&this._mouseDelayMet(b)&&(this._mouseStarted=this._mouseStart(this._mouseDownEvent,b)!==!1,this._mouseStarted?this._mouseDrag(b):this._mouseUp(b)),!this._mouseStarted):this._mouseUp(b)},_mouseUp:function(b){return a(document).unbind("mousemove."+this.widgetName,this._mouseMoveDelegate).unbind("mouseup."+this.widgetName,this._mouseUpDelegate),this._mouseStarted&&(this._mouseStarted=!1,b.target==this._mouseDownEvent.target&&a.data(b.target,this.widgetName+".preventClickEvent",!0),this._mouseStop(b)),!1},_mouseDistanceMet:function(a){return Math.max(Math.abs(this._mouseDownEvent.pageX-a.pageX),Math.abs(this._mouseDownEvent.pageY-a.pageY))>=this.options.distance},_mouseDelayMet:function(a){return this.mouseDelayMet},_mouseStart:function(a){},_mouseDrag:function(a){},_mouseStop:function(a){},_mouseCapture:function(a){return!0}})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.position.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.ui=a.ui||{};var c=/left|center|right/,d=/top|center|bottom/,e="center",f={},g=a.fn.position,h=a.fn.offset;a.fn.position=function(b){if(!b||!b.of)return g.apply(this,arguments);b=a.extend({},b);var h=a(b.of),i=h[0],j=(b.collision||"flip").split(" "),k=b.offset?b.offset.split(" "):[0,0],l,m,n;return i.nodeType===9?(l=h.width(),m=h.height(),n={top:0,left:0}):i.setTimeout?(l=h.width(),m=h.height(),n={top:h.scrollTop(),left:h.scrollLeft()}):i.preventDefault?(b.at="left top",l=m=0,n={top:b.of.pageY,left:b.of.pageX}):(l=h.outerWidth(),m=h.outerHeight(),n=h.offset()),a.each(["my","at"],function(){var a=(b[this]||"").split(" ");a.length===1&&(a=c.test(a[0])?a.concat([e]):d.test(a[0])?[e].concat(a):[e,e]),a[0]=c.test(a[0])?a[0]:e,a[1]=d.test(a[1])?a[1]:e,b[this]=a}),j.length===1&&(j[1]=j[0]),k[0]=parseInt(k[0],10)||0,k.length===1&&(k[1]=k[0]),k[1]=parseInt(k[1],10)||0,b.at[0]==="right"?n.left+=l:b.at[0]===e&&(n.left+=l/2),b.at[1]==="bottom"?n.top+=m:b.at[1]===e&&(n.top+=m/2),n.left+=k[0],n.top+=k[1],this.each(function(){var c=a(this),d=c.outerWidth(),g=c.outerHeight(),h=parseInt(a.curCSS(this,"marginLeft",!0))||0,i=parseInt(a.curCSS(this,"marginTop",!0))||0,o=d+h+(parseInt(a.curCSS(this,"marginRight",!0))||0),p=g+i+(parseInt(a.curCSS(this,"marginBottom",!0))||0),q=a.extend({},n),r;b.my[0]==="right"?q.left-=d:b.my[0]===e&&(q.left-=d/2),b.my[1]==="bottom"?q.top-=g:b.my[1]===e&&(q.top-=g/2),f.fractions||(q.left=Math.round(q.left),q.top=Math.round(q.top)),r={left:q.left-h,top:q.top-i},a.each(["left","top"],function(c,e){a.ui.position[j[c]]&&a.ui.position[j[c]][e](q,{targetWidth:l,targetHeight:m,elemWidth:d,elemHeight:g,collisionPosition:r,collisionWidth:o,collisionHeight:p,offset:k,my:b.my,at:b.at})}),a.fn.bgiframe&&c.bgiframe(),c.offset(a.extend(q,{using:b.using}))})},a.ui.position={fit:{left:function(b,c){var d=a(window),e=c.collisionPosition.left+c.collisionWidth-d.width()-d.scrollLeft();b.left=e>0?b.left-e:Math.max(b.left-c.collisionPosition.left,b.left)},top:function(b,c){var d=a(window),e=c.collisionPosition.top+c.collisionHeight-d.height()-d.scrollTop();b.top=e>0?b.top-e:Math.max(b.top-c.collisionPosition.top,b.top)}},flip:{left:function(b,c){if(c.at[0]===e)return;var d=a(window),f=c.collisionPosition.left+c.collisionWidth-d.width()-d.scrollLeft(),g=c.my[0]==="left"?-c.elemWidth:c.my[0]==="right"?c.elemWidth:0,h=c.at[0]==="left"?c.targetWidth:-c.targetWidth,i=-2*c.offset[0];b.left+=c.collisionPosition.left<0?g+h+i:f>0?g+h+i:0},top:function(b,c){if(c.at[1]===e)return;var d=a(window),f=c.collisionPosition.top+c.collisionHeight-d.height()-d.scrollTop(),g=c.my[1]==="top"?-c.elemHeight:c.my[1]==="bottom"?c.elemHeight:0,h=c.at[1]==="top"?c.targetHeight:-c.targetHeight,i=-2*c.offset[1];b.top+=c.collisionPosition.top<0?g+h+i:f>0?g+h+i:0}}},a.offset.setOffset||(a.offset.setOffset=function(b,c){/static/.test(a.curCSS(b,"position"))&&(b.style.position="relative");var d=a(b),e=d.offset(),f=parseInt(a.curCSS(b,"top",!0),10)||0,g=parseInt(a.curCSS(b,"left",!0),10)||0,h={top:c.top-e.top+f,left:c.left-e.left+g};"using"in c?c.using.call(b,h):d.css(h)},a.fn.offset=function(b){var c=this[0];return!c||!c.ownerDocument?null:b?a.isFunction(b)?this.each(function(c){a(this).offset(b.call(this,c,a(this).offset()))}):this.each(function(){a.offset.setOffset(this,b)}):h.call(this)}),function(){var b=document.getElementsByTagName("body")[0],c=document.createElement("div"),d,e,g,h,i;d=document.createElement(b?"div":"body"),g={visibility:"hidden",width:0,height:0,border:0,margin:0,background:"none"},b&&a.extend(g,{position:"absolute",left:"-1000px",top:"-1000px"});for(var j in g)d.style[j]=g[j];d.appendChild(c),e=b||document.documentElement,e.insertBefore(d,e.firstChild),c.style.cssText="position: absolute; left: 10.7432222px; top: 10.432325px; height: 30px; width: 201px;",h=a(c).offset(function(a,b){return b}).offset(),d.innerHTML="",e.removeChild(d),i=h.top+h.left+(b?2e3:0),f.fractions=i>21&&i<22}()})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.draggable.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.widget("ui.draggable",a.ui.mouse,{widgetEventPrefix:"drag",options:{addClasses:!0,appendTo:"parent",axis:!1,connectToSortable:!1,containment:!1,cursor:"auto",cursorAt:!1,grid:!1,handle:!1,helper:"original",iframeFix:!1,opacity:!1,refreshPositions:!1,revert:!1,revertDuration:500,scope:"default",scroll:!0,scrollSensitivity:20,scrollSpeed:20,snap:!1,snapMode:"both",snapTolerance:20,stack:!1,zIndex:!1},_create:function(){this.options.helper=="original"&&!/^(?:r|a|f)/.test(this.element.css("position"))&&(this.element[0].style.position="relative"),this.options.addClasses&&this.element.addClass("ui-draggable"),this.options.disabled&&this.element.addClass("ui-draggable-disabled"),this._mouseInit()},destroy:function(){if(!this.element.data("draggable"))return;return this.element.removeData("draggable").unbind(".draggable").removeClass("ui-draggable ui-draggable-dragging ui-draggable-disabled"),this._mouseDestroy(),this},_mouseCapture:function(b){var c=this.options;return this.helper||c.disabled||a(b.target).is(".ui-resizable-handle")?!1:(this.handle=this._getHandle(b),this.handle?(c.iframeFix&&a(c.iframeFix===!0?"iframe":c.iframeFix).each(function(){a('<div class="ui-draggable-iframeFix" style="background: #fff;"></div>').css({width:this.offsetWidth+"px",height:this.offsetHeight+"px",position:"absolute",opacity:"0.001",zIndex:1e3}).css(a(this).offset()).appendTo("body")}),!0):!1)},_mouseStart:function(b){var c=this.options;return this.helper=this._createHelper(b),this.helper.addClass("ui-draggable-dragging"),this._cacheHelperProportions(),a.ui.ddmanager&&(a.ui.ddmanager.current=this),this._cacheMargins(),this.cssPosition=this.helper.css("position"),this.scrollParent=this.helper.scrollParent(),this.offset=this.positionAbs=this.element.offset(),this.offset={top:this.offset.top-this.margins.top,left:this.offset.left-this.margins.left},a.extend(this.offset,{click:{left:b.pageX-this.offset.left,top:b.pageY-this.offset.top},parent:this._getParentOffset(),relative:this._getRelativeOffset()}),this.originalPosition=this.position=this._generatePosition(b),this.originalPageX=b.pageX,this.originalPageY=b.pageY,c.cursorAt&&this._adjustOffsetFromHelper(c.cursorAt),c.containment&&this._setContainment(),this._trigger("start",b)===!1?(this._clear(),!1):(this._cacheHelperProportions(),a.ui.ddmanager&&!c.dropBehaviour&&a.ui.ddmanager.prepareOffsets(this,b),this._mouseDrag(b,!0),a.ui.ddmanager&&a.ui.ddmanager.dragStart(this,b),!0)},_mouseDrag:function(b,c){this.position=this._generatePosition(b),this.positionAbs=this._convertPositionTo("absolute");if(!c){var d=this._uiHash();if(this._trigger("drag",b,d)===!1)return this._mouseUp({}),!1;this.position=d.position}if(!this.options.axis||this.options.axis!="y")this.helper[0].style.left=this.position.left+"px";if(!this.options.axis||this.options.axis!="x")this.helper[0].style.top=this.position.top+"px";return a.ui.ddmanager&&a.ui.ddmanager.drag(this,b),!1},_mouseStop:function(b){var c=!1;a.ui.ddmanager&&!this.options.dropBehaviour&&(c=a.ui.ddmanager.drop(this,b)),this.dropped&&(c=this.dropped,this.dropped=!1);var d=this.element[0],e=!1;while(d&&(d=d.parentNode))d==document&&(e=!0);if(!e&&this.options.helper==="original")return!1;if(this.options.revert=="invalid"&&!c||this.options.revert=="valid"&&c||this.options.revert===!0||a.isFunction(this.options.revert)&&this.options.revert.call(this.element,c)){var f=this;a(this.helper).animate(this.originalPosition,parseInt(this.options.revertDuration,10),function(){f._trigger("stop",b)!==!1&&f._clear()})}else this._trigger("stop",b)!==!1&&this._clear();return!1},_mouseUp:function(b){return this.options.iframeFix===!0&&a("div.ui-draggable-iframeFix").each(function(){this.parentNode.removeChild(this)}),a.ui.ddmanager&&a.ui.ddmanager.dragStop(this,b),a.ui.mouse.prototype._mouseUp.call(this,b)},cancel:function(){return this.helper.is(".ui-draggable-dragging")?this._mouseUp({}):this._clear(),this},_getHandle:function(b){var c=!this.options.handle||!a(this.options.handle,this.element).length?!0:!1;return a(this.options.handle,this.element).find("*").andSelf().each(function(){this==b.target&&(c=!0)}),c},_createHelper:function(b){var c=this.options,d=a.isFunction(c.helper)?a(c.helper.apply(this.element[0],[b])):c.helper=="clone"?this.element.clone().removeAttr("id"):this.element;return d.parents("body").length||d.appendTo(c.appendTo=="parent"?this.element[0].parentNode:c.appendTo),d[0]!=this.element[0]&&!/(fixed|absolute)/.test(d.css("position"))&&d.css("position","absolute"),d},_adjustOffsetFromHelper:function(b){typeof b=="string"&&(b=b.split(" ")),a.isArray(b)&&(b={left:+b[0],top:+b[1]||0}),"left"in b&&(this.offset.click.left=b.left+this.margins.left),"right"in b&&(this.offset.click.left=this.helperProportions.width-b.right+this.margins.left),"top"in b&&(this.offset.click.top=b.top+this.margins.top),"bottom"in b&&(this.offset.click.top=this.helperProportions.height-b.bottom+this.margins.top)},_getParentOffset:function(){this.offsetParent=this.helper.offsetParent();var b=this.offsetParent.offset();this.cssPosition=="absolute"&&this.scrollParent[0]!=document&&a.ui.contains(this.scrollParent[0],this.offsetParent[0])&&(b.left+=this.scrollParent.scrollLeft(),b.top+=this.scrollParent.scrollTop());if(this.offsetParent[0]==document.body||this.offsetParent[0].tagName&&this.offsetParent[0].tagName.toLowerCase()=="html"&&a.browser.msie)b={top:0,left:0};return{top:b.top+(parseInt(this.offsetParent.css("borderTopWidth"),10)||0),left:b.left+(parseInt(this.offsetParent.css("borderLeftWidth"),10)||0)}},_getRelativeOffset:function(){if(this.cssPosition=="relative"){var a=this.element.position();return{top:a.top-(parseInt(this.helper.css("top"),10)||0)+this.scrollParent.scrollTop(),left:a.left-(parseInt(this.helper.css("left"),10)||0)+this.scrollParent.scrollLeft()}}return{top:0,left:0}},_cacheMargins:function(){this.margins={left:parseInt(this.element.css("marginLeft"),10)||0,top:parseInt(this.element.css("marginTop"),10)||0,right:parseInt(this.element.css("marginRight"),10)||0,bottom:parseInt(this.element.css("marginBottom"),10)||0}},_cacheHelperProportions:function(){this.helperProportions={width:this.helper.outerWidth(),height:this.helper.outerHeight()}},_setContainment:function(){var b=this.options;b.containment=="parent"&&(b.containment=this.helper[0].parentNode);if(b.containment=="document"||b.containment=="window")this.containment=[b.containment=="document"?0:a(window).scrollLeft()-this.offset.relative.left-this.offset.parent.left,b.containment=="document"?0:a(window).scrollTop()-this.offset.relative.top-this.offset.parent.top,(b.containment=="document"?0:a(window).scrollLeft())+a(b.containment=="document"?document:window).width()-this.helperProportions.width-this.margins.left,(b.containment=="document"?0:a(window).scrollTop())+(a(b.containment=="document"?document:window).height()||document.body.parentNode.scrollHeight)-this.helperProportions.height-this.margins.top];if(!/^(document|window|parent)$/.test(b.containment)&&b.containment.constructor!=Array){var c=a(b.containment),d=c[0];if(!d)return;var e=c.offset(),f=a(d).css("overflow")!="hidden";this.containment=[(parseInt(a(d).css("borderLeftWidth"),10)||0)+(parseInt(a(d).css("paddingLeft"),10)||0),(parseInt(a(d).css("borderTopWidth"),10)||0)+(parseInt(a(d).css("paddingTop"),10)||0),(f?Math.max(d.scrollWidth,d.offsetWidth):d.offsetWidth)-(parseInt(a(d).css("borderLeftWidth"),10)||0)-(parseInt(a(d).css("paddingRight"),10)||0)-this.helperProportions.width-this.margins.left-this.margins.right,(f?Math.max(d.scrollHeight,d.offsetHeight):d.offsetHeight)-(parseInt(a(d).css("borderTopWidth"),10)||0)-(parseInt(a(d).css("paddingBottom"),10)||0)-this.helperProportions.height-this.margins.top-this.margins.bottom],this.relative_container=c}else b.containment.constructor==Array&&(this.containment=b.containment)},_convertPositionTo:function(b,c){c||(c=this.position);var d=b=="absolute"?1:-1,e=this.options,f=this.cssPosition=="absolute"&&(this.scrollParent[0]==document||!a.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,g=/(html|body)/i.test(f[0].tagName);return{top:c.top+this.offset.relative.top*d+this.offset.parent.top*d-(a.browser.safari&&a.browser.version<526&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollTop():g?0:f.scrollTop())*d),left:c.left+this.offset.relative.left*d+this.offset.parent.left*d-(a.browser.safari&&a.browser.version<526&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():g?0:f.scrollLeft())*d)}},_generatePosition:function(b){var c=this.options,d=this.cssPosition=="absolute"&&(this.scrollParent[0]==document||!a.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,e=/(html|body)/i.test(d[0].tagName),f=b.pageX,g=b.pageY;if(this.originalPosition){var h;if(this.containment){if(this.relative_container){var i=this.relative_container.offset();h=[this.containment[0]+i.left,this.containment[1]+i.top,this.containment[2]+i.left,this.containment[3]+i.top]}else h=this.containment;b.pageX-this.offset.click.left<h[0]&&(f=h[0]+this.offset.click.left),b.pageY-this.offset.click.top<h[1]&&(g=h[1]+this.offset.click.top),b.pageX-this.offset.click.left>h[2]&&(f=h[2]+this.offset.click.left),b.pageY-this.offset.click.top>h[3]&&(g=h[3]+this.offset.click.top)}if(c.grid){var j=c.grid[1]?this.originalPageY+Math.round((g-this.originalPageY)/c.grid[1])*c.grid[1]:this.originalPageY;g=h?j-this.offset.click.top<h[1]||j-this.offset.click.top>h[3]?j-this.offset.click.top<h[1]?j+c.grid[1]:j-c.grid[1]:j:j;var k=c.grid[0]?this.originalPageX+Math.round((f-this.originalPageX)/c.grid[0])*c.grid[0]:this.originalPageX;f=h?k-this.offset.click.left<h[0]||k-this.offset.click.left>h[2]?k-this.offset.click.left<h[0]?k+c.grid[0]:k-c.grid[0]:k:k}}return{top:g-this.offset.click.top-this.offset.relative.top-this.offset.parent.top+(a.browser.safari&&a.browser.version<526&&this.cssPosition=="fixed"?0:this.cssPosition=="fixed"?-this.scrollParent.scrollTop():e?0:d.scrollTop()),left:f-this.offset.click.left-this.offset.relative.left-this.offset.parent.left+(a.browser.safari&&a.browser.version<526&&this.cssPosition=="fixed"?0:this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():e?0:d.scrollLeft())}},_clear:function(){this.helper.removeClass("ui-draggable-dragging"),this.helper[0]!=this.element[0]&&!this.cancelHelperRemoval&&this.helper.remove(),this.helper=null,this.cancelHelperRemoval=!1},_trigger:function(b,c,d){return d=d||this._uiHash(),a.ui.plugin.call(this,b,[c,d]),b=="drag"&&(this.positionAbs=this._convertPositionTo("absolute")),a.Widget.prototype._trigger.call(this,b,c,d)},plugins:{},_uiHash:function(a){return{helper:this.helper,position:this.position,originalPosition:this.originalPosition,offset:this.positionAbs}}}),a.extend(a.ui.draggable,{version:"1.8.21"}),a.ui.plugin.add("draggable","connectToSortable",{start:function(b,c){var d=a(this).data("draggable"),e=d.options,f=a.extend({},c,{item:d.element});d.sortables=[],a(e.connectToSortable).each(function(){var c=a.data(this,"sortable");c&&!c.options.disabled&&(d.sortables.push({instance:c,shouldRevert:c.options.revert}),c.refreshPositions(),c._trigger("activate",b,f))})},stop:function(b,c){var d=a(this).data("draggable"),e=a.extend({},c,{item:d.element});a.each(d.sortables,function(){this.instance.isOver?(this.instance.isOver=0,d.cancelHelperRemoval=!0,this.instance.cancelHelperRemoval=!1,this.shouldRevert&&(this.instance.options.revert=!0),this.instance._mouseStop(b),this.instance.options.helper=this.instance.options._helper,d.options.helper=="original"&&this.instance.currentItem.css({top:"auto",left:"auto"})):(this.instance.cancelHelperRemoval=!1,this.instance._trigger("deactivate",b,e))})},drag:function(b,c){var d=a(this).data("draggable"),e=this,f=function(b){var c=this.offset.click.top,d=this.offset.click.left,e=this.positionAbs.top,f=this.positionAbs.left,g=b.height,h=b.width,i=b.top,j=b.left;return a.ui.isOver(e+c,f+d,i,j,g,h)};a.each(d.sortables,function(f){this.instance.positionAbs=d.positionAbs,this.instance.helperProportions=d.helperProportions,this.instance.offset.click=d.offset.click,this.instance._intersectsWith(this.instance.containerCache)?(this.instance.isOver||(this.instance.isOver=1,this.instance.currentItem=a(e).clone().removeAttr("id").appendTo(this.instance.element).data("sortable-item",!0),this.instance.options._helper=this.instance.options.helper,this.instance.options.helper=function(){return c.helper[0]},b.target=this.instance.currentItem[0],this.instance._mouseCapture(b,!0),this.instance._mouseStart(b,!0,!0),this.instance.offset.click.top=d.offset.click.top,this.instance.offset.click.left=d.offset.click.left,this.instance.offset.parent.left-=d.offset.parent.left-this.instance.offset.parent.left,this.instance.offset.parent.top-=d.offset.parent.top-this.instance.offset.parent.top,d._trigger("toSortable",b),d.dropped=this.instance.element,d.currentItem=d.element,this.instance.fromOutside=d),this.instance.currentItem&&this.instance._mouseDrag(b)):this.instance.isOver&&(this.instance.isOver=0,this.instance.cancelHelperRemoval=!0,this.instance.options.revert=!1,this.instance._trigger("out",b,this.instance._uiHash(this.instance)),this.instance._mouseStop(b,!0),this.instance.options.helper=this.instance.options._helper,this.instance.currentItem.remove(),this.instance.placeholder&&this.instance.placeholder.remove(),d._trigger("fromSortable",b),d.dropped=!1)})}}),a.ui.plugin.add("draggable","cursor",{start:function(b,c){var d=a("body"),e=a(this).data("draggable").options;d.css("cursor")&&(e._cursor=d.css("cursor")),d.css("cursor",e.cursor)},stop:function(b,c){var d=a(this).data("draggable").options;d._cursor&&a("body").css("cursor",d._cursor)}}),a.ui.plugin.add("draggable","opacity",{start:function(b,c){var d=a(c.helper),e=a(this).data("draggable").options;d.css("opacity")&&(e._opacity=d.css("opacity")),d.css("opacity",e.opacity)},stop:function(b,c){var d=a(this).data("draggable").options;d._opacity&&a(c.helper).css("opacity",d._opacity)}}),a.ui.plugin.add("draggable","scroll",{start:function(b,c){var d=a(this).data("draggable");d.scrollParent[0]!=document&&d.scrollParent[0].tagName!="HTML"&&(d.overflowOffset=d.scrollParent.offset())},drag:function(b,c){var d=a(this).data("draggable"),e=d.options,f=!1;if(d.scrollParent[0]!=document&&d.scrollParent[0].tagName!="HTML"){if(!e.axis||e.axis!="x")d.overflowOffset.top+d.scrollParent[0].offsetHeight-b.pageY<e.scrollSensitivity?d.scrollParent[0].scrollTop=f=d.scrollParent[0].scrollTop+e.scrollSpeed:b.pageY-d.overflowOffset.top<e.scrollSensitivity&&(d.scrollParent[0].scrollTop=f=d.scrollParent[0].scrollTop-e.scrollSpeed);if(!e.axis||e.axis!="y")d.overflowOffset.left+d.scrollParent[0].offsetWidth-b.pageX<e.scrollSensitivity?d.scrollParent[0].scrollLeft=f=d.scrollParent[0].scrollLeft+e.scrollSpeed:b.pageX-d.overflowOffset.left<e.scrollSensitivity&&(d.scrollParent[0].scrollLeft=f=d.scrollParent[0].scrollLeft-e.scrollSpeed)}else{if(!e.axis||e.axis!="x")b.pageY-a(document).scrollTop()<e.scrollSensitivity?f=a(document).scrollTop(a(document).scrollTop()-e.scrollSpeed):a(window).height()-(b.pageY-a(document).scrollTop())<e.scrollSensitivity&&(f=a(document).scrollTop(a(document).scrollTop()+e.scrollSpeed));if(!e.axis||e.axis!="y")b.pageX-a(document).scrollLeft()<e.scrollSensitivity?f=a(document).scrollLeft(a(document).scrollLeft()-e.scrollSpeed):a(window).width()-(b.pageX-a(document).scrollLeft())<e.scrollSensitivity&&(f=a(document).scrollLeft(a(document).scrollLeft()+e.scrollSpeed))}f!==!1&&a.ui.ddmanager&&!e.dropBehaviour&&a.ui.ddmanager.prepareOffsets(d,b)}}),a.ui.plugin.add("draggable","snap",{start:function(b,c){var d=a(this).data("draggable"),e=d.options;d.snapElements=[],a(e.snap.constructor!=String?e.snap.items||":data(draggable)":e.snap).each(function(){var b=a(this),c=b.offset();this!=d.element[0]&&d.snapElements.push({item:this,width:b.outerWidth(),height:b.outerHeight(),top:c.top,left:c.left})})},drag:function(b,c){var d=a(this).data("draggable"),e=d.options,f=e.snapTolerance,g=c.offset.left,h=g+d.helperProportions.width,i=c.offset.top,j=i+d.helperProportions.height;for(var k=d.snapElements.length-1;k>=0;k--){var l=d.snapElements[k].left,m=l+d.snapElements[k].width,n=d.snapElements[k].top,o=n+d.snapElements[k].height;if(!(l-f<g&&g<m+f&&n-f<i&&i<o+f||l-f<g&&g<m+f&&n-f<j&&j<o+f||l-f<h&&h<m+f&&n-f<i&&i<o+f||l-f<h&&h<m+f&&n-f<j&&j<o+f)){d.snapElements[k].snapping&&d.options.snap.release&&d.options.snap.release.call(d.element,b,a.extend(d._uiHash(),{snapItem:d.snapElements[k].item})),d.snapElements[k].snapping=!1;continue}if(e.snapMode!="inner"){var p=Math.abs(n-j)<=f,q=Math.abs(o-i)<=f,r=Math.abs(l-h)<=f,s=Math.abs(m-g)<=f;p&&(c.position.top=d._convertPositionTo("relative",{top:n-d.helperProportions.height,left:0}).top-d.margins.top),q&&(c.position.top=d._convertPositionTo("relative",{top:o,left:0}).top-d.margins.top),r&&(c.position.left=d._convertPositionTo("relative",{top:0,left:l-d.helperProportions.width}).left-d.margins.left),s&&(c.position.left=d._convertPositionTo("relative",{top:0,left:m}).left-d.margins.left)}var t=p||q||r||s;if(e.snapMode!="outer"){var p=Math.abs(n-i)<=f,q=Math.abs(o-j)<=f,r=Math.abs(l-g)<=f,s=Math.abs(m-h)<=f;p&&(c.position.top=d._convertPositionTo("relative",{top:n,left:0}).top-d.margins.top),q&&(c.position.top=d._convertPositionTo("relative",{top:o-d.helperProportions.height,left:0}).top-d.margins.top),r&&(c.position.left=d._convertPositionTo("relative",{top:0,left:l}).left-d.margins.left),s&&(c.position.left=d._convertPositionTo("relative",{top:0,left:m-d.helperProportions.width}).left-d.margins.left)}!d.snapElements[k].snapping&&(p||q||r||s||t)&&d.options.snap.snap&&d.options.snap.snap.call(d.element,b,a.extend(d._uiHash(),{snapItem:d.snapElements[k].item})),d.snapElements[k].snapping=p||q||r||s||t}}}),a.ui.plugin.add("draggable","stack",{start:function(b,c){var d=a(this).data("draggable").options,e=a.makeArray(a(d.stack)).sort(function(b,c){return(parseInt(a(b).css("zIndex"),10)||0)-(parseInt(a(c).css("zIndex"),10)||0)});if(!e.length)return;var f=parseInt(e[0].style.zIndex)||0;a(e).each(function(a){this.style.zIndex=f+a}),this[0].style.zIndex=f+e.length}}),a.ui.plugin.add("draggable","zIndex",{start:function(b,c){var d=a(c.helper),e=a(this).data("draggable").options;d.css("zIndex")&&(e._zIndex=d.css("zIndex")),d.css("zIndex",e.zIndex)},stop:function(b,c){var d=a(this).data("draggable").options;d._zIndex&&a(c.helper).css("zIndex",d._zIndex)}})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.droppable.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.widget("ui.droppable",{widgetEventPrefix:"drop",options:{accept:"*",activeClass:!1,addClasses:!0,greedy:!1,hoverClass:!1,scope:"default",tolerance:"intersect"},_create:function(){var b=this.options,c=b.accept;this.isover=0,this.isout=1,this.accept=a.isFunction(c)?c:function(a){return a.is(c)},this.proportions={width:this.element[0].offsetWidth,height:this.element[0].offsetHeight},a.ui.ddmanager.droppables[b.scope]=a.ui.ddmanager.droppables[b.scope]||[],a.ui.ddmanager.droppables[b.scope].push(this),b.addClasses&&this.element.addClass("ui-droppable")},destroy:function(){var b=a.ui.ddmanager.droppables[this.options.scope];for(var c=0;c<b.length;c++)b[c]==this&&b.splice(c,1);return this.element.removeClass("ui-droppable ui-droppable-disabled").removeData("droppable").unbind(".droppable"),this},_setOption:function(b,c){b=="accept"&&(this.accept=a.isFunction(c)?c:function(a){return a.is(c)}),a.Widget.prototype._setOption.apply(this,arguments)},_activate:function(b){var c=a.ui.ddmanager.current;this.options.activeClass&&this.element.addClass(this.options.activeClass),c&&this._trigger("activate",b,this.ui(c))},_deactivate:function(b){var c=a.ui.ddmanager.current;this.options.activeClass&&this.element.removeClass(this.options.activeClass),c&&this._trigger("deactivate",b,this.ui(c))},_over:function(b){var c=a.ui.ddmanager.current;if(!c||(c.currentItem||c.element)[0]==this.element[0])return;this.accept.call(this.element[0],c.currentItem||c.element)&&(this.options.hoverClass&&this.element.addClass(this.options.hoverClass),this._trigger("over",b,this.ui(c)))},_out:function(b){var c=a.ui.ddmanager.current;if(!c||(c.currentItem||c.element)[0]==this.element[0])return;this.accept.call(this.element[0],c.currentItem||c.element)&&(this.options.hoverClass&&this.element.removeClass(this.options.hoverClass),this._trigger("out",b,this.ui(c)))},_drop:function(b,c){var d=c||a.ui.ddmanager.current;if(!d||(d.currentItem||d.element)[0]==this.element[0])return!1;var e=!1;return this.element.find(":data(droppable)").not(".ui-draggable-dragging").each(function(){var b=a.data(this,"droppable");if(b.options.greedy&&!b.options.disabled&&b.options.scope==d.options.scope&&b.accept.call(b.element[0],d.currentItem||d.element)&&a.ui.intersect(d,a.extend(b,{offset:b.element.offset()}),b.options.tolerance))return e=!0,!1}),e?!1:this.accept.call(this.element[0],d.currentItem||d.element)?(this.options.activeClass&&this.element.removeClass(this.options.activeClass),this.options.hoverClass&&this.element.removeClass(this.options.hoverClass),this._trigger("drop",b,this.ui(d)),this.element):!1},ui:function(a){return{draggable:a.currentItem||a.element,helper:a.helper,position:a.position,offset:a.positionAbs}}}),a.extend(a.ui.droppable,{version:"1.8.21"}),a.ui.intersect=function(b,c,d){if(!c.offset)return!1;var e=(b.positionAbs||b.position.absolute).left,f=e+b.helperProportions.width,g=(b.positionAbs||b.position.absolute).top,h=g+b.helperProportions.height,i=c.offset.left,j=i+c.proportions.width,k=c.offset.top,l=k+c.proportions.height;switch(d){case"fit":return i<=e&&f<=j&&k<=g&&h<=l;case"intersect":return i<e+b.helperProportions.width/2&&f-b.helperProportions.width/2<j&&k<g+b.helperProportions.height/2&&h-b.helperProportions.height/2<l;case"pointer":var m=(b.positionAbs||b.position.absolute).left+(b.clickOffset||b.offset.click).left,n=(b.positionAbs||b.position.absolute).top+(b.clickOffset||b.offset.click).top,o=a.ui.isOver(n,m,k,i,c.proportions.height,c.proportions.width);return o;case"touch":return(g>=k&&g<=l||h>=k&&h<=l||g<k&&h>l)&&(e>=i&&e<=j||f>=i&&f<=j||e<i&&f>j);default:return!1}},a.ui.ddmanager={current:null,droppables:{"default":[]},prepareOffsets:function(b,c){var d=a.ui.ddmanager.droppables[b.options.scope]||[],e=c?c.type:null,f=(b.currentItem||b.element).find(":data(droppable)").andSelf();g:for(var h=0;h<d.length;h++){if(d[h].options.disabled||b&&!d[h].accept.call(d[h].element[0],b.currentItem||b.element))continue;for(var i=0;i<f.length;i++)if(f[i]==d[h].element[0]){d[h].proportions.height=0;continue g}d[h].visible=d[h].element.css("display")!="none";if(!d[h].visible)continue;e=="mousedown"&&d[h]._activate.call(d[h],c),d[h].offset=d[h].element.offset(),d[h].proportions={width:d[h].element[0].offsetWidth,height:d[h].element[0].offsetHeight}}},drop:function(b,c){var d=!1;return a.each(a.ui.ddmanager.droppables[b.options.scope]||[],function(){if(!this.options)return;!this.options.disabled&&this.visible&&a.ui.intersect(b,this,this.options.tolerance)&&(d=this._drop.call(this,c)||d),!this.options.disabled&&this.visible&&this.accept.call(this.element[0],b.currentItem||b.element)&&(this.isout=1,this.isover=0,this._deactivate.call(this,c))}),d},dragStart:function(b,c){b.element.parents(":not(body,html)").bind("scroll.droppable",function(){b.options.refreshPositions||a.ui.ddmanager.prepareOffsets(b,c)})},drag:function(b,c){b.options.refreshPositions&&a.ui.ddmanager.prepareOffsets(b,c),a.each(a.ui.ddmanager.droppables[b.options.scope]||[],function(){if(this.options.disabled||this.greedyChild||!this.visible)return;var d=a.ui.intersect(b,this,this.options.tolerance),e=!d&&this.isover==1?"isout":d&&this.isover==0?"isover":null;if(!e)return;var f;if(this.options.greedy){var g=this.element.parents(":data(droppable):eq(0)");g.length&&(f=a.data(g[0],"droppable"),f.greedyChild=e=="isover"?1:0)}f&&e=="isover"&&(f.isover=0,f.isout=1,f._out.call(f,c)),this[e]=1,this[e=="isout"?"isover":"isout"]=0,this[e=="isover"?"_over":"_out"].call(this,c),f&&e=="isout"&&(f.isout=0,f.isover=1,f._over.call(f,c))})},dragStop:function(b,c){b.element.parents(":not(body,html)").unbind("scroll.droppable"),b.options.refreshPositions||a.ui.ddmanager.prepareOffsets(b,c)}}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.resizable.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.widget("ui.resizable",a.ui.mouse,{widgetEventPrefix:"resize",options:{alsoResize:!1,animate:!1,animateDuration:"slow",animateEasing:"swing",aspectRatio:!1,autoHide:!1,containment:!1,ghost:!1,grid:!1,handles:"e,s,se",helper:!1,maxHeight:null,maxWidth:null,minHeight:10,minWidth:10,zIndex:1e3},_create:function(){var b=this,c=this.options;this.element.addClass("ui-resizable"),a.extend(this,{_aspectRatio:!!c.aspectRatio,aspectRatio:c.aspectRatio,originalElement:this.element,_proportionallyResizeElements:[],_helper:c.helper||c.ghost||c.animate?c.helper||"ui-resizable-helper":null}),this.element[0].nodeName.match(/canvas|textarea|input|select|button|img/i)&&(this.element.wrap(a('<div class="ui-wrapper" style="overflow: hidden;"></div>').css({position:this.element.css("position"),width:this.element.outerWidth(),height:this.element.outerHeight(),top:this.element.css("top"),left:this.element.css("left")})),this.element=this.element.parent().data("resizable",this.element.data("resizable")),this.elementIsWrapper=!0,this.element.css({marginLeft:this.originalElement.css("marginLeft"),marginTop:this.originalElement.css("marginTop"),marginRight:this.originalElement.css("marginRight"),marginBottom:this.originalElement.css("marginBottom")}),this.originalElement.css({marginLeft:0,marginTop:0,marginRight:0,marginBottom:0}),this.originalResizeStyle=this.originalElement.css("resize"),this.originalElement.css("resize","none"),this._proportionallyResizeElements.push(this.originalElement.css({position:"static",zoom:1,display:"block"})),this.originalElement.css({margin:this.originalElement.css("margin")}),this._proportionallyResize()),this.handles=c.handles||(a(".ui-resizable-handle",this.element).length?{n:".ui-resizable-n",e:".ui-resizable-e",s:".ui-resizable-s",w:".ui-resizable-w",se:".ui-resizable-se",sw:".ui-resizable-sw",ne:".ui-resizable-ne",nw:".ui-resizable-nw"}:"e,s,se");if(this.handles.constructor==String){this.handles=="all"&&(this.handles="n,e,s,w,se,sw,ne,nw");var d=this.handles.split(",");this.handles={};for(var e=0;e<d.length;e++){var f=a.trim(d[e]),g="ui-resizable-"+f,h=a('<div class="ui-resizable-handle '+g+'"></div>');h.css({zIndex:c.zIndex}),"se"==f&&h.addClass("ui-icon ui-icon-gripsmall-diagonal-se"),this.handles[f]=".ui-resizable-"+f,this.element.append(h)}}this._renderAxis=function(b){b=b||this.element;for(var c in this.handles){this.handles[c].constructor==String&&(this.handles[c]=a(this.handles[c],this.element).show());if(this.elementIsWrapper&&this.originalElement[0].nodeName.match(/textarea|input|select|button/i)){var d=a(this.handles[c],this.element),e=0;e=/sw|ne|nw|se|n|s/.test(c)?d.outerHeight():d.outerWidth();var f=["padding",/ne|nw|n/.test(c)?"Top":/se|sw|s/.test(c)?"Bottom":/^e$/.test(c)?"Right":"Left"].join("");b.css(f,e),this._proportionallyResize()}if(!a(this.handles[c]).length)continue}},this._renderAxis(this.element),this._handles=a(".ui-resizable-handle",this.element).disableSelection(),this._handles.mouseover(function(){if(!b.resizing){if(this.className)var a=this.className.match(/ui-resizable-(se|sw|ne|nw|n|e|s|w)/i);b.axis=a&&a[1]?a[1]:"se"}}),c.autoHide&&(this._handles.hide(),a(this.element).addClass("ui-resizable-autohide").hover(function(){if(c.disabled)return;a(this).removeClass("ui-resizable-autohide"),b._handles.show()},function(){if(c.disabled)return;b.resizing||(a(this).addClass("ui-resizable-autohide"),b._handles.hide())})),this._mouseInit()},destroy:function(){this._mouseDestroy();var b=function(b){a(b).removeClass("ui-resizable ui-resizable-disabled ui-resizable-resizing").removeData("resizable").unbind(".resizable").find(".ui-resizable-handle").remove()};if(this.elementIsWrapper){b(this.element);var c=this.element;c.after(this.originalElement.css({position:c.css("position"),width:c.outerWidth(),height:c.outerHeight(),top:c.css("top"),left:c.css("left")})).remove()}return this.originalElement.css("resize",this.originalResizeStyle),b(this.originalElement),this},_mouseCapture:function(b){var c=!1;for(var d in this.handles)a(this.handles[d])[0]==b.target&&(c=!0);return!this.options.disabled&&c},_mouseStart:function(b){var d=this.options,e=this.element.position(),f=this.element;this.resizing=!0,this.documentScroll={top:a(document).scrollTop(),left:a(document).scrollLeft()},(f.is(".ui-draggable")||/absolute/.test(f.css("position")))&&f.css({position:"absolute",top:e.top,left:e.left}),this._renderProxy();var g=c(this.helper.css("left")),h=c(this.helper.css("top"));d.containment&&(g+=a(d.containment).scrollLeft()||0,h+=a(d.containment).scrollTop()||0),this.offset=this.helper.offset(),this.position={left:g,top:h},this.size=this._helper?{width:f.outerWidth(),height:f.outerHeight()}:{width:f.width(),height:f.height()},this.originalSize=this._helper?{width:f.outerWidth(),height:f.outerHeight()}:{width:f.width(),height:f.height()},this.originalPosition={left:g,top:h},this.sizeDiff={width:f.outerWidth()-f.width(),height:f.outerHeight()-f.height()},this.originalMousePosition={left:b.pageX,top:b.pageY},this.aspectRatio=typeof d.aspectRatio=="number"?d.aspectRatio:this.originalSize.width/this.originalSize.height||1;var i=a(".ui-resizable-"+this.axis).css("cursor");return a("body").css("cursor",i=="auto"?this.axis+"-resize":i),f.addClass("ui-resizable-resizing"),this._propagate("start",b),!0},_mouseDrag:function(b){var c=this.helper,d=this.options,e={},f=this,g=this.originalMousePosition,h=this.axis,i=b.pageX-g.left||0,j=b.pageY-g.top||0,k=this._change[h];if(!k)return!1;var l=k.apply(this,[b,i,j]),m=a.browser.msie&&a.browser.version<7,n=this.sizeDiff;this._updateVirtualBoundaries(b.shiftKey);if(this._aspectRatio||b.shiftKey)l=this._updateRatio(l,b);return l=this._respectSize(l,b),this._propagate("resize",b),c.css({top:this.position.top+"px",left:this.position.left+"px",width:this.size.width+"px",height:this.size.height+"px"}),!this._helper&&this._proportionallyResizeElements.length&&this._proportionallyResize(),this._updateCache(l),this._trigger("resize",b,this.ui()),!1},_mouseStop:function(b){this.resizing=!1;var c=this.options,d=this;if(this._helper){var e=this._proportionallyResizeElements,f=e.length&&/textarea/i.test(e[0].nodeName),g=f&&a.ui.hasScroll(e[0],"left")?0:d.sizeDiff.height,h=f?0:d.sizeDiff.width,i={width:d.helper.width()-h,height:d.helper.height()-g},j=parseInt(d.element.css("left"),10)+(d.position.left-d.originalPosition.left)||null,k=parseInt(d.element.css("top"),10)+(d.position.top-d.originalPosition.top)||null;c.animate||this.element.css(a.extend(i,{top:k,left:j})),d.helper.height(d.size.height),d.helper.width(d.size.width),this._helper&&!c.animate&&this._proportionallyResize()}return a("body").css("cursor","auto"),this.element.removeClass("ui-resizable-resizing"),this._propagate("stop",b),this._helper&&this.helper.remove(),!1},_updateVirtualBoundaries:function(a){var b=this.options,c,e,f,g,h;h={minWidth:d(b.minWidth)?b.minWidth:0,maxWidth:d(b.maxWidth)?b.maxWidth:Infinity,minHeight:d(b.minHeight)?b.minHeight:0,maxHeight:d(b.maxHeight)?b.maxHeight:Infinity};if(this._aspectRatio||a)c=h.minHeight*this.aspectRatio,f=h.minWidth/this.aspectRatio,e=h.maxHeight*this.aspectRatio,g=h.maxWidth/this.aspectRatio,c>h.minWidth&&(h.minWidth=c),f>h.minHeight&&(h.minHeight=f),e<h.maxWidth&&(h.maxWidth=e),g<h.maxHeight&&(h.maxHeight=g);this._vBoundaries=h},_updateCache:function(a){var b=this.options;this.offset=this.helper.offset(),d(a.left)&&(this.position.left=a.left),d(a.top)&&(this.position.top=a.top),d(a.height)&&(this.size.height=a.height),d(a.width)&&(this.size.width=a.width)},_updateRatio:function(a,b){var c=this.options,e=this.position,f=this.size,g=this.axis;return d(a.height)?a.width=a.height*this.aspectRatio:d(a.width)&&(a.height=a.width/this.aspectRatio),g=="sw"&&(a.left=e.left+(f.width-a.width),a.top=null),g=="nw"&&(a.top=e.top+(f.height-a.height),a.left=e.left+(f.width-a.width)),a},_respectSize:function(a,b){var c=this.helper,e=this._vBoundaries,f=this._aspectRatio||b.shiftKey,g=this.axis,h=d(a.width)&&e.maxWidth&&e.maxWidth<a.width,i=d(a.height)&&e.maxHeight&&e.maxHeight<a.height,j=d(a.width)&&e.minWidth&&e.minWidth>a.width,k=d(a.height)&&e.minHeight&&e.minHeight>a.height;j&&(a.width=e.minWidth),k&&(a.height=e.minHeight),h&&(a.width=e.maxWidth),i&&(a.height=e.maxHeight);var l=this.originalPosition.left+this.originalSize.width,m=this.position.top+this.size.height,n=/sw|nw|w/.test(g),o=/nw|ne|n/.test(g);j&&n&&(a.left=l-e.minWidth),h&&n&&(a.left=l-e.maxWidth),k&&o&&(a.top=m-e.minHeight),i&&o&&(a.top=m-e.maxHeight);var p=!a.width&&!a.height;return p&&!a.left&&a.top?a.top=null:p&&!a.top&&a.left&&(a.left=null),a},_proportionallyResize:function(){var b=this.options;if(!this._proportionallyResizeElements.length)return;var c=this.helper||this.element;for(var d=0;d<this._proportionallyResizeElements.length;d++){var e=this._proportionallyResizeElements[d];if(!this.borderDif){var f=[e.css("borderTopWidth"),e.css("borderRightWidth"),e.css("borderBottomWidth"),e.css("borderLeftWidth")],g=[e.css("paddingTop"),e.css("paddingRight"),e.css("paddingBottom"),e.css("paddingLeft")];this.borderDif=a.map(f,function(a,b){var c=parseInt(a,10)||0,d=parseInt(g[b],10)||0;return c+d})}if(!a.browser.msie||!a(c).is(":hidden")&&!a(c).parents(":hidden").length)e.css({height:c.height()-this.borderDif[0]-this.borderDif[2]||0,width:c.width()-this.borderDif[1]-this.borderDif[3]||0});else continue}},_renderProxy:function(){var b=this.element,c=this.options;this.elementOffset=b.offset();if(this._helper){this.helper=this.helper||a('<div style="overflow:hidden;"></div>');var d=a.browser.msie&&a.browser.version<7,e=d?1:0,f=d?2:-1;this.helper.addClass(this._helper).css({width:this.element.outerWidth()+f,height:this.element.outerHeight()+f,position:"absolute",left:this.elementOffset.left-e+"px",top:this.elementOffset.top-e+"px",zIndex:++c.zIndex}),this.helper.appendTo("body").disableSelection()}else this.helper=this.element},_change:{e:function(a,b,c){return{width:this.originalSize.width+b}},w:function(a,b,c){var d=this.options,e=this.originalSize,f=this.originalPosition;return{left:f.left+b,width:e.width-b}},n:function(a,b,c){var d=this.options,e=this.originalSize,f=this.originalPosition;return{top:f.top+c,height:e.height-c}},s:function(a,b,c){return{height:this.originalSize.height+c}},se:function(b,c,d){return a.extend(this._change.s.apply(this,arguments),this._change.e.apply(this,[b,c,d]))},sw:function(b,c,d){return a.extend(this._change.s.apply(this,arguments),this._change.w.apply(this,[b,c,d]))},ne:function(b,c,d){return a.extend(this._change.n.apply(this,arguments),this._change.e.apply(this,[b,c,d]))},nw:function(b,c,d){return a.extend(this._change.n.apply(this,arguments),this._change.w.apply(this,[b,c,d]))}},_propagate:function(b,c){a.ui.plugin.call(this,b,[c,this.ui()]),b!="resize"&&this._trigger(b,c,this.ui())},plugins:{},ui:function(){return{originalElement:this.originalElement,element:this.element,helper:this.helper,position:this.position,size:this.size,originalSize:this.originalSize,originalPosition:this.originalPosition}}}),a.extend(a.ui.resizable,{version:"1.8.21"}),a.ui.plugin.add("resizable","alsoResize",{start:function(b,c){var d=a(this).data("resizable"),e=d.options,f=function(b){a(b).each(function(){var b=a(this);b.data("resizable-alsoresize",{width:parseInt(b.width(),10),height:parseInt(b.height(),10),left:parseInt(b.css("left"),10),top:parseInt(b.css("top"),10)})})};typeof e.alsoResize=="object"&&!e.alsoResize.parentNode?e.alsoResize.length?(e.alsoResize=e.alsoResize[0],f(e.alsoResize)):a.each(e.alsoResize,function(a){f(a)}):f(e.alsoResize)},resize:function(b,c){var d=a(this).data("resizable"),e=d.options,f=d.originalSize,g=d.originalPosition,h={height:d.size.height-f.height||0,width:d.size.width-f.width||0,top:d.position.top-g.top||0,left:d.position.left-g.left||0},i=function(b,d){a(b).each(function(){var b=a(this),e=a(this).data("resizable-alsoresize"),f={},g=d&&d.length?d:b.parents(c.originalElement[0]).length?["width","height"]:["width","height","top","left"];a.each(g,function(a,b){var c=(e[b]||0)+(h[b]||0);c&&c>=0&&(f[b]=c||null)}),b.css(f)})};typeof e.alsoResize=="object"&&!e.alsoResize.nodeType?a.each(e.alsoResize,function(a,b){i(a,b)}):i(e.alsoResize)},stop:function(b,c){a(this).removeData("resizable-alsoresize")}}),a.ui.plugin.add("resizable","animate",{stop:function(b,c){var d=a(this).data("resizable"),e=d.options,f=d._proportionallyResizeElements,g=f.length&&/textarea/i.test(f[0].nodeName),h=g&&a.ui.hasScroll(f[0],"left")?0:d.sizeDiff.height,i=g?0:d.sizeDiff.width,j={width:d.size.width-i,height:d.size.height-h},k=parseInt(d.element.css("left"),10)+(d.position.left-d.originalPosition.left)||null,l=parseInt(d.element.css("top"),10)+(d.position.top-d.originalPosition.top)||null;d.element.animate(a.extend(j,l&&k?{top:l,left:k}:{}),{duration:e.animateDuration,easing:e.animateEasing,step:function(){var c={width:parseInt(d.element.css("width"),10),height:parseInt(d.element.css("height"),10),top:parseInt(d.element.css("top"),10),left:parseInt(d.element.css("left"),10)};f&&f.length&&a(f[0]).css({width:c.width,height:c.height}),d._updateCache(c),d._propagate("resize",b)}})}}),a.ui.plugin.add("resizable","containment",{start:function(b,d){var e=a(this).data("resizable"),f=e.options,g=e.element,h=f.containment,i=h instanceof a?h.get(0):/parent/.test(h)?g.parent().get(0):h;if(!i)return;e.containerElement=a(i);if(/document/.test(h)||h==document)e.containerOffset={left:0,top:0},e.containerPosition={left:0,top:0},e.parentData={element:a(document),left:0,top:0,width:a(document).width(),height:a(document).height()||document.body.parentNode.scrollHeight};else{var j=a(i),k=[];a(["Top","Right","Left","Bottom"]).each(function(a,b){k[a]=c(j.css("padding"+b))}),e.containerOffset=j.offset(),e.containerPosition=j.position(),e.containerSize={height:j.innerHeight()-k[3],width:j.innerWidth()-k[1]};var l=e.containerOffset,m=e.containerSize.height,n=e.containerSize.width,o=a.ui.hasScroll(i,"left")?i.scrollWidth:n,p=a.ui.hasScroll(i)?i.scrollHeight:m;e.parentData={element:i,left:l.left,top:l.top,width:o,height:p}}},resize:function(b,c){var d=a(this).data("resizable"),e=d.options,f=d.containerSize,g=d.containerOffset,h=d.size,i=d.position,j=d._aspectRatio||b.shiftKey,k={top:0,left:0},l=d.containerElement;l[0]!=document&&/static/.test(l.css("position"))&&(k=g),i.left<(d._helper?g.left:0)&&(d.size.width=d.size.width+(d._helper?d.position.left-g.left:d.position.left-k.left),j&&(d.size.height=d.size.width/d.aspectRatio),d.position.left=e.helper?g.left:0),i.top<(d._helper?g.top:0)&&(d.size.height=d.size.height+(d._helper?d.position.top-g.top:d.position.top),j&&(d.size.width=d.size.height*d.aspectRatio),d.position.top=d._helper?g.top:0),d.offset.left=d.parentData.left+d.position.left,d.offset.top=d.parentData.top+d.position.top;var m=Math.abs((d._helper?d.offset.left-k.left:d.offset.left-k.left)+d.sizeDiff.width),n=Math.abs((d._helper?d.offset.top-k.top:d.offset.top-g.top)+d.sizeDiff.height),o=d.containerElement.get(0)==d.element.parent().get(0),p=/relative|absolute/.test(d.containerElement.css("position"));o&&p&&(m-=d.parentData.left),m+d.size.width>=d.parentData.width&&(d.size.width=d.parentData.width-m,j&&(d.size.height=d.size.width/d.aspectRatio)),n+d.size.height>=d.parentData.height&&(d.size.height=d.parentData.height-n,j&&(d.size.width=d.size.height*d.aspectRatio))},stop:function(b,c){var d=a(this).data("resizable"),e=d.options,f=d.position,g=d.containerOffset,h=d.containerPosition,i=d.containerElement,j=a(d.helper),k=j.offset(),l=j.outerWidth()-d.sizeDiff.width,m=j.outerHeight()-d.sizeDiff.height;d._helper&&!e.animate&&/relative/.test(i.css("position"))&&a(this).css({left:k.left-h.left-g.left,width:l,height:m}),d._helper&&!e.animate&&/static/.test(i.css("position"))&&a(this).css({left:k.left-h.left-g.left,width:l,height:m})}}),a.ui.plugin.add("resizable","ghost",{start:function(b,c){var d=a(this).data("resizable"),e=d.options,f=d.size;d.ghost=d.originalElement.clone(),d.ghost.css({opacity:.25,display:"block",position:"relative",height:f.height,width:f.width,margin:0,left:0,top:0}).addClass("ui-resizable-ghost").addClass(typeof e.ghost=="string"?e.ghost:""),d.ghost.appendTo(d.helper)},resize:function(b,c){var d=a(this).data("resizable"),e=d.options;d.ghost&&d.ghost.css({position:"relative",height:d.size.height,width:d.size.width})},stop:function(b,c){var d=a(this).data("resizable"),e=d.options;d.ghost&&d.helper&&d.helper.get(0).removeChild(d.ghost.get(0))}}),a.ui.plugin.add("resizable","grid",{resize:function(b,c){var d=a(this).data("resizable"),e=d.options,f=d.size,g=d.originalSize,h=d.originalPosition,i=d.axis,j=e._aspectRatio||b.shiftKey;e.grid=typeof e.grid=="number"?[e.grid,e.grid]:e.grid;var k=Math.round((f.width-g.width)/(e.grid[0]||1))*(e.grid[0]||1),l=Math.round((f.height-g.height)/(e.grid[1]||1))*(e.grid[1]||1);/^(se|s|e)$/.test(i)?(d.size.width=g.width+k,d.size.height=g.height+l):/^(ne)$/.test(i)?(d.size.width=g.width+k,d.size.height=g.height+l,d.position.top=h.top-l):/^(sw)$/.test(i)?(d.size.width=g.width+k,d.size.height=g.height+l,d.position.left=h.left-k):(d.size.width=g.width+k,d.size.height=g.height+l,d.position.top=h.top-l,d.position.left=h.left-k)}});var c=function(a){return parseInt(a,10)||0},d=function(a){return!isNaN(parseInt(a,10))}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.selectable.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.widget("ui.selectable",a.ui.mouse,{options:{appendTo:"body",autoRefresh:!0,distance:0,filter:"*",tolerance:"touch"},_create:function(){var b=this;this.element.addClass("ui-selectable"),this.dragged=!1;var c;this.refresh=function(){c=a(b.options.filter,b.element[0]),c.addClass("ui-selectee"),c.each(function(){var b=a(this),c=b.offset();a.data(this,"selectable-item",{element:this,$element:b,left:c.left,top:c.top,right:c.left+b.outerWidth(),bottom:c.top+b.outerHeight(),startselected:!1,selected:b.hasClass("ui-selected"),selecting:b.hasClass("ui-selecting"),unselecting:b.hasClass("ui-unselecting")})})},this.refresh(),this.selectees=c.addClass("ui-selectee"),this._mouseInit(),this.helper=a("<div class='ui-selectable-helper'></div>")},destroy:function(){return this.selectees.removeClass("ui-selectee").removeData("selectable-item"),this.element.removeClass("ui-selectable ui-selectable-disabled").removeData("selectable").unbind(".selectable"),this._mouseDestroy(),this},_mouseStart:function(b){var c=this;this.opos=[b.pageX,b.pageY];if(this.options.disabled)return;var d=this.options;this.selectees=a(d.filter,this.element[0]),this._trigger("start",b),a(d.appendTo).append(this.helper),this.helper.css({left:b.clientX,top:b.clientY,width:0,height:0}),d.autoRefresh&&this.refresh(),this.selectees.filter(".ui-selected").each(function(){var d=a.data(this,"selectable-item");d.startselected=!0,!b.metaKey&&!b.ctrlKey&&(d.$element.removeClass("ui-selected"),d.selected=!1,d.$element.addClass("ui-unselecting"),d.unselecting=!0,c._trigger("unselecting",b,{unselecting:d.element}))}),a(b.target).parents().andSelf().each(function(){var d=a.data(this,"selectable-item");if(d){var e=!b.metaKey&&!b.ctrlKey||!d.$element.hasClass("ui-selected");return d.$element.removeClass(e?"ui-unselecting":"ui-selected").addClass(e?"ui-selecting":"ui-unselecting"),d.unselecting=!e,d.selecting=e,d.selected=e,e?c._trigger("selecting",b,{selecting:d.element}):c._trigger("unselecting",b,{unselecting:d.element}),!1}})},_mouseDrag:function(b){var c=this;this.dragged=!0;if(this.options.disabled)return;var d=this.options,e=this.opos[0],f=this.opos[1],g=b.pageX,h=b.pageY;if(e>g){var i=g;g=e,e=i}if(f>h){var i=h;h=f,f=i}return this.helper.css({left:e,top:f,width:g-e,height:h-f}),this.selectees.each(function(){var i=a.data(this,"selectable-item");if(!i||i.element==c.element[0])return;var j=!1;d.tolerance=="touch"?j=!(i.left>g||i.right<e||i.top>h||i.bottom<f):d.tolerance=="fit"&&(j=i.left>e&&i.right<g&&i.top>f&&i.bottom<h),j?(i.selected&&(i.$element.removeClass("ui-selected"),i.selected=!1),i.unselecting&&(i.$element.removeClass("ui-unselecting"),i.unselecting=!1),i.selecting||(i.$element.addClass("ui-selecting"),i.selecting=!0,c._trigger("selecting",b,{selecting:i.element}))):(i.selecting&&((b.metaKey||b.ctrlKey)&&i.startselected?(i.$element.removeClass("ui-selecting"),i.selecting=!1,i.$element.addClass("ui-selected"),i.selected=!0):(i.$element.removeClass("ui-selecting"),i.selecting=!1,i.startselected&&(i.$element.addClass("ui-unselecting"),i.unselecting=!0),c._trigger("unselecting",b,{unselecting:i.element}))),i.selected&&!b.metaKey&&!b.ctrlKey&&!i.startselected&&(i.$element.removeClass("ui-selected"),i.selected=!1,i.$element.addClass("ui-unselecting"),i.unselecting=!0,c._trigger("unselecting",b,{unselecting:i.element})))}),!1},_mouseStop:function(b){var c=this;this.dragged=!1;var d=this.options;return a(".ui-unselecting",this.element[0]).each(function(){var d=a.data(this,"selectable-item");d.$element.removeClass("ui-unselecting"),d.unselecting=!1,d.startselected=!1,c._trigger("unselected",b,{unselected:d.element})}),a(".ui-selecting",this.element[0]).each(function(){var d=a.data(this,"selectable-item");d.$element.removeClass("ui-selecting").addClass("ui-selected"),d.selecting=!1,d.selected=!0,d.startselected=!0,c._trigger("selected",b,{selected:d.element})}),this._trigger("stop",b),this.helper.remove(),!1}}),a.extend(a.ui.selectable,{version:"1.8.21"})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.sortable.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.widget("ui.sortable",a.ui.mouse,{widgetEventPrefix:"sort",ready:!1,options:{appendTo:"parent",axis:!1,connectWith:!1,containment:!1,cursor:"auto",cursorAt:!1,dropOnEmpty:!0,forcePlaceholderSize:!1,forceHelperSize:!1,grid:!1,handle:!1,helper:"original",items:"> *",opacity:!1,placeholder:!1,revert:!1,scroll:!0,scrollSensitivity:20,scrollSpeed:20,scope:"default",tolerance:"intersect",zIndex:1e3},_create:function(){var a=this.options;this.containerCache={},this.element.addClass("ui-sortable"),this.refresh(),this.floating=this.items.length?a.axis==="x"||/left|right/.test(this.items[0].item.css("float"))||/inline|table-cell/.test(this.items[0].item.css("display")):!1,this.offset=this.element.offset(),this._mouseInit(),this.ready=!0},destroy:function(){a.Widget.prototype.destroy.call(this),this.element.removeClass("ui-sortable ui-sortable-disabled"),this._mouseDestroy();for(var b=this.items.length-1;b>=0;b--)this.items[b].item.removeData(this.widgetName+"-item");return this},_setOption:function(b,c){b==="disabled"?(this.options[b]=c,this.widget()[c?"addClass":"removeClass"]("ui-sortable-disabled")):a.Widget.prototype._setOption.apply(this,arguments)},_mouseCapture:function(b,c){var d=this;if(this.reverting)return!1;if(this.options.disabled||this.options.type=="static")return!1;this._refreshItems(b);var e=null,f=this,g=a(b.target).parents().each(function(){if(a.data(this,d.widgetName+"-item")==f)return e=a(this),!1});a.data(b.target,d.widgetName+"-item")==f&&(e=a(b.target));if(!e)return!1;if(this.options.handle&&!c){var h=!1;a(this.options.handle,e).find("*").andSelf().each(function(){this==b.target&&(h=!0)});if(!h)return!1}return this.currentItem=e,this._removeCurrentsFromItems(),!0},_mouseStart:function(b,c,d){var e=this.options,f=this;this.currentContainer=this,this.refreshPositions(),this.helper=this._createHelper(b),this._cacheHelperProportions(),this._cacheMargins(),this.scrollParent=this.helper.scrollParent(),this.offset=this.currentItem.offset(),this.offset={top:this.offset.top-this.margins.top,left:this.offset.left-this.margins.left},a.extend(this.offset,{click:{left:b.pageX-this.offset.left,top:b.pageY-this.offset.top},parent:this._getParentOffset(),relative:this._getRelativeOffset()}),this.helper.css("position","absolute"),this.cssPosition=this.helper.css("position"),this.originalPosition=this._generatePosition(b),this.originalPageX=b.pageX,this.originalPageY=b.pageY,e.cursorAt&&this._adjustOffsetFromHelper(e.cursorAt),this.domPosition={prev:this.currentItem.prev()[0],parent:this.currentItem.parent()[0]},this.helper[0]!=this.currentItem[0]&&this.currentItem.hide(),this._createPlaceholder(),e.containment&&this._setContainment(),e.cursor&&(a("body").css("cursor")&&(this._storedCursor=a("body").css("cursor")),a("body").css("cursor",e.cursor)),e.opacity&&(this.helper.css("opacity")&&(this._storedOpacity=this.helper.css("opacity")),this.helper.css("opacity",e.opacity)),e.zIndex&&(this.helper.css("zIndex")&&(this._storedZIndex=this.helper.css("zIndex")),this.helper.css("zIndex",e.zIndex)),this.scrollParent[0]!=document&&this.scrollParent[0].tagName!="HTML"&&(this.overflowOffset=this.scrollParent.offset()),this._trigger("start",b,this._uiHash()),this._preserveHelperProportions||this._cacheHelperProportions();if(!d)for(var g=this.containers.length-1;g>=0;g--)this.containers[g]._trigger("activate",b,f._uiHash(this));return a.ui.ddmanager&&(a.ui.ddmanager.current=this),a.ui.ddmanager&&!e.dropBehaviour&&a.ui.ddmanager.prepareOffsets(this,b),this.dragging=!0,this.helper.addClass("ui-sortable-helper"),this._mouseDrag(b),!0},_mouseDrag:function(b){this.position=this._generatePosition(b),this.positionAbs=this._convertPositionTo("absolute"),this.lastPositionAbs||(this.lastPositionAbs=this.positionAbs);if(this.options.scroll){var c=this.options,d=!1;this.scrollParent[0]!=document&&this.scrollParent[0].tagName!="HTML"?(this.overflowOffset.top+this.scrollParent[0].offsetHeight-b.pageY<c.scrollSensitivity?this.scrollParent[0].scrollTop=d=this.scrollParent[0].scrollTop+c.scrollSpeed:b.pageY-this.overflowOffset.top<c.scrollSensitivity&&(this.scrollParent[0].scrollTop=d=this.scrollParent[0].scrollTop-c.scrollSpeed),this.overflowOffset.left+this.scrollParent[0].offsetWidth-b.pageX<c.scrollSensitivity?this.scrollParent[0].scrollLeft=d=this.scrollParent[0].scrollLeft+c.scrollSpeed:b.pageX-this.overflowOffset.left<c.scrollSensitivity&&(this.scrollParent[0].scrollLeft=d=this.scrollParent[0].scrollLeft-c.scrollSpeed)):(b.pageY-a(document).scrollTop()<c.scrollSensitivity?d=a(document).scrollTop(a(document).scrollTop()-c.scrollSpeed):a(window).height()-(b.pageY-a(document).scrollTop())<c.scrollSensitivity&&(d=a(document).scrollTop(a(document).scrollTop()+c.scrollSpeed)),b.pageX-a(document).scrollLeft()<c.scrollSensitivity?d=a(document).scrollLeft(a(document).scrollLeft()-c.scrollSpeed):a(window).width()-(b.pageX-a(document).scrollLeft())<c.scrollSensitivity&&(d=a(document).scrollLeft(a(document).scrollLeft()+c.scrollSpeed))),d!==!1&&a.ui.ddmanager&&!c.dropBehaviour&&a.ui.ddmanager.prepareOffsets(this,b)}this.positionAbs=this._convertPositionTo("absolute");if(!this.options.axis||this.options.axis!="y")this.helper[0].style.left=this.position.left+"px";if(!this.options.axis||this.options.axis!="x")this.helper[0].style.top=this.position.top+"px";for(var e=this.items.length-1;e>=0;e--){var f=this.items[e],g=f.item[0],h=this._intersectsWithPointer(f);if(!h)continue;if(g!=this.currentItem[0]&&this.placeholder[h==1?"next":"prev"]()[0]!=g&&!a.ui.contains(this.placeholder[0],g)&&(this.options.type=="semi-dynamic"?!a.ui.contains(this.element[0],g):!0)){this.direction=h==1?"down":"up";if(this.options.tolerance=="pointer"||this._intersectsWithSides(f))this._rearrange(b,f);else break;this._trigger("change",b,this._uiHash());break}}return this._contactContainers(b),a.ui.ddmanager&&a.ui.ddmanager.drag(this,b),this._trigger("sort",b,this._uiHash()),this.lastPositionAbs=this.positionAbs,!1},_mouseStop:function(b,c){if(!b)return;a.ui.ddmanager&&!this.options.dropBehaviour&&a.ui.ddmanager.drop(this,b);if(this.options.revert){var d=this,e=d.placeholder.offset();d.reverting=!0,a(this.helper).animate({left:e.left-this.offset.parent.left-d.margins.left+(this.offsetParent[0]==document.body?0:this.offsetParent[0].scrollLeft),top:e.top-this.offset.parent.top-d.margins.top+(this.offsetParent[0]==document.body?0:this.offsetParent[0].scrollTop)},parseInt(this.options.revert,10)||500,function(){d._clear(b)})}else this._clear(b,c);return!1},cancel:function(){var b=this;if(this.dragging){this._mouseUp({target:null}),this.options.helper=="original"?this.currentItem.css(this._storedCSS).removeClass("ui-sortable-helper"):this.currentItem.show();for(var c=this.containers.length-1;c>=0;c--)this.containers[c]._trigger("deactivate",null,b._uiHash(this)),this.containers[c].containerCache.over&&(this.containers[c]._trigger("out",null,b._uiHash(this)),this.containers[c].containerCache.over=0)}return this.placeholder&&(this.placeholder[0].parentNode&&this.placeholder[0].parentNode.removeChild(this.placeholder[0]),this.options.helper!="original"&&this.helper&&this.helper[0].parentNode&&this.helper.remove(),a.extend(this,{helper:null,dragging:!1,reverting:!1,_noFinalSort:null}),this.domPosition.prev?a(this.domPosition.prev).after(this.currentItem):a(this.domPosition.parent).prepend(this.currentItem)),this},serialize:function(b){var c=this._getItemsAsjQuery(b&&b.connected),d=[];return b=b||{},a(c).each(function(){var c=(a(b.item||this).attr(b.attribute||"id")||"").match(b.expression||/(.+)[-=_](.+)/);c&&d.push((b.key||c[1]+"[]")+"="+(b.key&&b.expression?c[1]:c[2]))}),!d.length&&b.key&&d.push(b.key+"="),d.join("&")},toArray:function(b){var c=this._getItemsAsjQuery(b&&b.connected),d=[];return b=b||{},c.each(function(){d.push(a(b.item||this).attr(b.attribute||"id")||"")}),d},_intersectsWith:function(a){var b=this.positionAbs.left,c=b+this.helperProportions.width,d=this.positionAbs.top,e=d+this.helperProportions.height,f=a.left,g=f+a.width,h=a.top,i=h+a.height,j=this.offset.click.top,k=this.offset.click.left,l=d+j>h&&d+j<i&&b+k>f&&b+k<g;return this.options.tolerance=="pointer"||this.options.forcePointerForContainers||this.options.tolerance!="pointer"&&this.helperProportions[this.floating?"width":"height"]>a[this.floating?"width":"height"]?l:f<b+this.helperProportions.width/2&&c-this.helperProportions.width/2<g&&h<d+this.helperProportions.height/2&&e-this.helperProportions.height/2<i},_intersectsWithPointer:function(b){var c=this.options.axis==="x"||a.ui.isOverAxis(this.positionAbs.top+this.offset.click.top,b.top,b.height),d=this.options.axis==="y"||a.ui.isOverAxis(this.positionAbs.left+this.offset.click.left,b.left,b.width),e=c&&d,f=this._getDragVerticalDirection(),g=this._getDragHorizontalDirection();return e?this.floating?g&&g=="right"||f=="down"?2:1:f&&(f=="down"?2:1):!1},_intersectsWithSides:function(b){var c=a.ui.isOverAxis(this.positionAbs.top+this.offset.click.top,b.top+b.height/2,b.height),d=a.ui.isOverAxis(this.positionAbs.left+this.offset.click.left,b.left+b.width/2,b.width),e=this._getDragVerticalDirection(),f=this._getDragHorizontalDirection();return this.floating&&f?f=="right"&&d||f=="left"&&!d:e&&(e=="down"&&c||e=="up"&&!c)},_getDragVerticalDirection:function(){var a=this.positionAbs.top-this.lastPositionAbs.top;return a!=0&&(a>0?"down":"up")},_getDragHorizontalDirection:function(){var a=this.positionAbs.left-this.lastPositionAbs.left;return a!=0&&(a>0?"right":"left")},refresh:function(a){return this._refreshItems(a),this.refreshPositions(),this},_connectWith:function(){var a=this.options;return a.connectWith.constructor==String?[a.connectWith]:a.connectWith},_getItemsAsjQuery:function(b){var c=this,d=[],e=[],f=this._connectWith();if(f&&b)for(var g=f.length-1;g>=0;g--){var h=a(f[g]);for(var i=h.length-1;i>=0;i--){var j=a.data(h[i],this.widgetName);j&&j!=this&&!j.options.disabled&&e.push([a.isFunction(j.options.items)?j.options.items.call(j.element):a(j.options.items,j.element).not(".ui-sortable-helper").not(".ui-sortable-placeholder"),j])}}e.push([a.isFunction(this.options.items)?this.options.items.call(this.element,null,{options:this.options,item:this.currentItem}):a(this.options.items,this.element).not(".ui-sortable-helper").not(".ui-sortable-placeholder"),this]);for(var g=e.length-1;g>=0;g--)e[g][0].each(function(){d.push(this)});return a(d)},_removeCurrentsFromItems:function(){var a=this.currentItem.find(":data("+this.widgetName+"-item)");for(var b=0;b<this.items.length;b++)for(var c=0;c<a.length;c++)a[c]==this.items[b].item[0]&&this.items.splice(b,1)},_refreshItems:function(b){this.items=[],this.containers=[this];var c=this.items,d=this,e=[[a.isFunction(this.options.items)?this.options.items.call(this.element[0],b,{item:this.currentItem}):a(this.options.items,this.element),this]],f=this._connectWith();if(f&&this.ready)for(var g=f.length-1;g>=0;g--){var h=a(f[g]);for(var i=h.length-1;i>=0;i--){var j=a.data(h[i],this.widgetName);j&&j!=this&&!j.options.disabled&&(e.push([a.isFunction(j.options.items)?j.options.items.call(j.element[0],b,{item:this.currentItem}):a(j.options.items,j.element),j]),this.containers.push(j))}}for(var g=e.length-1;g>=0;g--){var k=e[g][1],l=e[g][0];for(var i=0,m=l.length;i<m;i++){var n=a(l[i]);n.data(this.widgetName+"-item",k),c.push({item:n,instance:k,width:0,height:0,left:0,top:0})}}},refreshPositions:function(b){this.offsetParent&&this.helper&&(this.offset.parent=this._getParentOffset());for(var c=this.items.length-1;c>=0;c--){var d=this.items[c];if(d.instance!=this.currentContainer&&this.currentContainer&&d.item[0]!=this.currentItem[0])continue;var e=this.options.toleranceElement?a(this.options.toleranceElement,d.item):d.item;b||(d.width=e.outerWidth(),d.height=e.outerHeight());var f=e.offset();d.left=f.left,d.top=f.top}if(this.options.custom&&this.options.custom.refreshContainers)this.options.custom.refreshContainers.call(this);else for(var c=this.containers.length-1;c>=0;c--){var f=this.containers[c].element.offset();this.containers[c].containerCache.left=f.left,this.containers[c].containerCache.top=f.top,this.containers[c].containerCache.width=this.containers[c].element.outerWidth(),this.containers[c].containerCache.height=this.containers[c].element.outerHeight()}return this},_createPlaceholder:function(b){var c=b||this,d=c.options;if(!d.placeholder||d.placeholder.constructor==String){var e=d.placeholder;d.placeholder={element:function(){var b=a(document.createElement(c.currentItem[0].nodeName)).addClass(e||c.currentItem[0].className+" ui-sortable-placeholder").removeClass("ui-sortable-helper")[0];return e||(b.style.visibility="hidden"),b},update:function(a,b){if(e&&!d.forcePlaceholderSize)return;b.height()||b.height(c.currentItem.innerHeight()-parseInt(c.currentItem.css("paddingTop")||0,10)-parseInt(c.currentItem.css("paddingBottom")||0,10)),b.width()||b.width(c.currentItem.innerWidth()-parseInt(c.currentItem.css("paddingLeft")||0,10)-parseInt(c.currentItem.css("paddingRight")||0,10))}}}c.placeholder=a(d.placeholder.element.call(c.element,c.currentItem)),c.currentItem.after(c.placeholder),d.placeholder.update(c,c.placeholder)},_contactContainers:function(b){var c=null,d=null;for(var e=this.containers.length-1;e>=0;e--){if(a.ui.contains(this.currentItem[0],this.containers[e].element[0]))continue;if(this._intersectsWith(this.containers[e].containerCache)){if(c&&a.ui.contains(this.containers[e].element[0],c.element[0]))continue;c=this.containers[e],d=e}else this.containers[e].containerCache.over&&(this.containers[e]._trigger("out",b,this._uiHash(this)),this.containers[e].containerCache.over=0)}if(!c)return;if(this.containers.length===1)this.containers[d]._trigger("over",b,this._uiHash(this)),this.containers[d].containerCache.over=1;else if(this.currentContainer!=this.containers[d]){var f=1e4,g=null,h=this.positionAbs[this.containers[d].floating?"left":"top"];for(var i=this.items.length-1;i>=0;i--){if(!a.ui.contains(this.containers[d].element[0],this.items[i].item[0]))continue;var j=this.containers[d].floating?this.items[i].item.offset().left:this.items[i].item.offset().top;Math.abs(j-h)<f&&(f=Math.abs(j-h),g=this.items[i],this.direction=j-h>0?"down":"up")}if(!g&&!this.options.dropOnEmpty)return;this.currentContainer=this.containers[d],g?this._rearrange(b,g,null,!0):this._rearrange(b,null,this.containers[d].element,!0),this._trigger("change",b,this._uiHash()),this.containers[d]._trigger("change",b,this._uiHash(this)),this.options.placeholder.update(this.currentContainer,this.placeholder),this.containers[d]._trigger("over",b,this._uiHash(this)),this.containers[d].containerCache.over=1}},_createHelper:function(b){var c=this.options,d=a.isFunction(c.helper)?a(c.helper.apply(this.element[0],[b,this.currentItem])):c.helper=="clone"?this.currentItem.clone():this.currentItem;return d.parents("body").length||a(c.appendTo!="parent"?c.appendTo:this.currentItem[0].parentNode)[0].appendChild(d[0]),d[0]==this.currentItem[0]&&(this._storedCSS={width:this.currentItem[0].style.width,height:this.currentItem[0].style.height,position:this.currentItem.css("position"),top:this.currentItem.css("top"),left:this.currentItem.css("left")}),(d[0].style.width==""||c.forceHelperSize)&&d.width(this.currentItem.width()),(d[0].style.height==""||c.forceHelperSize)&&d.height(this.currentItem.height()),d},_adjustOffsetFromHelper:function(b){typeof b=="string"&&(b=b.split(" ")),a.isArray(b)&&(b={left:+b[0],top:+b[1]||0}),"left"in b&&(this.offset.click.left=b.left+this.margins.left),"right"in b&&(this.offset.click.left=this.helperProportions.width-b.right+this.margins.left),"top"in b&&(this.offset.click.top=b.top+this.margins.top),"bottom"in b&&(this.offset.click.top=this.helperProportions.height-b.bottom+this.margins.top)},_getParentOffset:function(){this.offsetParent=this.helper.offsetParent();var b=this.offsetParent.offset();this.cssPosition=="absolute"&&this.scrollParent[0]!=document&&a.ui.contains(this.scrollParent[0],this.offsetParent[0])&&(b.left+=this.scrollParent.scrollLeft(),b.top+=this.scrollParent.scrollTop());if(this.offsetParent[0]==document.body||this.offsetParent[0].tagName&&this.offsetParent[0].tagName.toLowerCase()=="html"&&a.browser.msie)b={top:0,left:0};return{top:b.top+(parseInt(this.offsetParent.css("borderTopWidth"),10)||0),left:b.left+(parseInt(this.offsetParent.css("borderLeftWidth"),10)||0)}},_getRelativeOffset:function(){if(this.cssPosition=="relative"){var a=this.currentItem.position();return{top:a.top-(parseInt(this.helper.css("top"),10)||0)+this.scrollParent.scrollTop(),left:a.left-(parseInt(this.helper.css("left"),10)||0)+this.scrollParent.scrollLeft()}}return{top:0,left:0}},_cacheMargins:function(){this.margins={left:parseInt(this.currentItem.css("marginLeft"),10)||0,top:parseInt(this.currentItem.css("marginTop"),10)||0}},_cacheHelperProportions:function(){this.helperProportions={width:this.helper.outerWidth(),height:this.helper.outerHeight()}},_setContainment:function(){var b=this.options;b.containment=="parent"&&(b.containment=this.helper[0].parentNode);if(b.containment=="document"||b.containment=="window")this.containment=[0-this.offset.relative.left-this.offset.parent.left,0-this.offset.relative.top-this.offset.parent.top,a(b.containment=="document"?document:window).width()-this.helperProportions.width-this.margins.left,(a(b.containment=="document"?document:window).height()||document.body.parentNode.scrollHeight)-this.helperProportions.height-this.margins.top];if(!/^(document|window|parent)$/.test(b.containment)){var c=a(b.containment)[0],d=a(b.containment).offset(),e=a(c).css("overflow")!="hidden";this.containment=[d.left+(parseInt(a(c).css("borderLeftWidth"),10)||0)+(parseInt(a(c).css("paddingLeft"),10)||0)-this.margins.left,d.top+(parseInt(a(c).css("borderTopWidth"),10)||0)+(parseInt(a(c).css("paddingTop"),10)||0)-this.margins.top,d.left+(e?Math.max(c.scrollWidth,c.offsetWidth):c.offsetWidth)-(parseInt(a(c).css("borderLeftWidth"),10)||0)-(parseInt(a(c).css("paddingRight"),10)||0)-this.helperProportions.width-this.margins.left,d.top+(e?Math.max(c.scrollHeight,c.offsetHeight):c.offsetHeight)-(parseInt(a(c).css("borderTopWidth"),10)||0)-(parseInt(a(c).css("paddingBottom"),10)||0)-this.helperProportions.height-this.margins.top]}},_convertPositionTo:function(b,c){c||(c=this.position);var d=b=="absolute"?1:-1,e=this.options,f=this.cssPosition=="absolute"&&(this.scrollParent[0]==document||!a.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,g=/(html|body)/i.test(f[0].tagName);return{top:c.top+this.offset.relative.top*d+this.offset.parent.top*d-(a.browser.safari&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollTop():g?0:f.scrollTop())*d),left:c.left+this.offset.relative.left*d+this.offset.parent.left*d-(a.browser.safari&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():g?0:f.scrollLeft())*d)}},_generatePosition:function(b){var c=this.options,d=this.cssPosition=="absolute"&&(this.scrollParent[0]==document||!a.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,e=/(html|body)/i.test(d[0].tagName);this.cssPosition=="relative"&&(this.scrollParent[0]==document||this.scrollParent[0]==this.offsetParent[0])&&(this.offset.relative=this._getRelativeOffset());var f=b.pageX,g=b.pageY;if(this.originalPosition){this.containment&&(b.pageX-this.offset.click.left<this.containment[0]&&(f=this.containment[0]+this.offset.click.left),b.pageY-this.offset.click.top<this.containment[1]&&(g=this.containment[1]+this.offset.click.top),b.pageX-this.offset.click.left>this.containment[2]&&(f=this.containment[2]+this.offset.click.left),b.pageY-this.offset.click.top>this.containment[3]&&(g=this.containment[3]+this.offset.click.top));if(c.grid){var h=this.originalPageY+Math.round((g-this.originalPageY)/c.grid[1])*c.grid[1];g=this.containment?h-this.offset.click.top<this.containment[1]||h-this.offset.click.top>this.containment[3]?h-this.offset.click.top<this.containment[1]?h+c.grid[1]:h-c.grid[1]:h:h;var i=this.originalPageX+Math.round((f-this.originalPageX)/c.grid[0])*c.grid[0];f=this.containment?i-this.offset.click.left<this.containment[0]||i-this.offset.click.left>this.containment[2]?i-this.offset.click.left<this.containment[0]?i+c.grid[0]:i-c.grid[0]:i:i}}return{top:g-this.offset.click.top-this.offset.relative.top-this.offset.parent.top+(a.browser.safari&&this.cssPosition=="fixed"?0:this.cssPosition=="fixed"?-this.scrollParent.scrollTop():e?0:d.scrollTop()),left:f-this.offset.click.left-this.offset.relative.left-this.offset.parent.left+(a.browser.safari&&this.cssPosition=="fixed"?0:this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():e?0:d.scrollLeft())}},_rearrange:function(a,b,c,d){c?c[0].appendChild(this.placeholder[0]):b.item[0].parentNode.insertBefore(this.placeholder[0],this.direction=="down"?b.item[0]:b.item[0].nextSibling),this.counter=this.counter?++this.counter:1;var e=this,f=this.counter;window.setTimeout(function(){f==e.counter&&e.refreshPositions(!d)},0)},_clear:function(b,c){this.reverting=!1;var d=[],e=this;!this._noFinalSort&&this.currentItem.parent().length&&this.placeholder.before(this.currentItem),this._noFinalSort=null;if(this.helper[0]==this.currentItem[0]){for(var f in this._storedCSS)if(this._storedCSS[f]=="auto"||this._storedCSS[f]=="static")this._storedCSS[f]="";this.currentItem.css(this._storedCSS).removeClass("ui-sortable-helper")}else this.currentItem.show();this.fromOutside&&!c&&d.push(function(a){this._trigger("receive",a,this._uiHash(this.fromOutside))}),(this.fromOutside||this.domPosition.prev!=this.currentItem.prev().not(".ui-sortable-helper")[0]||this.domPosition.parent!=this.currentItem.parent()[0])&&!c&&d.push(function(a){this._trigger("update",a,this._uiHash())});if(!a.ui.contains(this.element[0],this.currentItem[0])){c||d.push(function(a){this._trigger("remove",a,this._uiHash())});for(var f=this.containers.length-1;f>=0;f--)a.ui.contains(this.containers[f].element[0],this.currentItem[0])&&!c&&(d.push(function(a){return function(b){a._trigger("receive",b,this._uiHash(this))}}.call(this,this.containers[f])),d.push(function(a){return function(b){a._trigger("update",b,this._uiHash(this))}}.call(this,this.containers[f])))}for(var f=this.containers.length-1;f>=0;f--)c||d.push(function(a){return function(b){a._trigger("deactivate",b,this._uiHash(this))}}.call(this,this.containers[f])),this.containers[f].containerCache.over&&(d.push(function(a){return function(b){a._trigger("out",b,this._uiHash(this))}}.call(this,this.containers[f])),this.containers[f].containerCache.over=0);this._storedCursor&&a("body").css("cursor",this._storedCursor),this._storedOpacity&&this.helper.css("opacity",this._storedOpacity),this._storedZIndex&&this.helper.css("zIndex",this._storedZIndex=="auto"?"":this._storedZIndex),this.dragging=!1;if(this.cancelHelperRemoval){if(!c){this._trigger("beforeStop",b,this._uiHash());for(var f=0;f<d.length;f++)d[f].call(this,b);this._trigger("stop",b,this._uiHash())}return!1}c||this._trigger("beforeStop",b,this._uiHash()),this.placeholder[0].parentNode.removeChild(this.placeholder[0]),this.helper[0]!=this.currentItem[0]&&this.helper.remove(),this.helper=null;if(!c){for(var f=0;f<d.length;f++)d[f].call(this,b);this._trigger("stop",b,this._uiHash())}return this.fromOutside=!1,!0},_trigger:function(){a.Widget.prototype._trigger.apply(this,arguments)===!1&&this.cancel()},_uiHash:function(b){var c=b||this;return{helper:c.helper,placeholder:c.placeholder||a([]),position:c.position,originalPosition:c.originalPosition,offset:c.positionAbs,item:c.currentItem,sender:b?b.element:null}}}),a.extend(a.ui.sortable,{version:"1.8.21"})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.accordion.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.widget("ui.accordion",{options:{active:0,animated:"slide",autoHeight:!0,clearStyle:!1,collapsible:!1,event:"click",fillSpace:!1,header:"> li > :first-child,> :not(li):even",icons:{header:"ui-icon-triangle-1-e",headerSelected:"ui-icon-triangle-1-s"},navigation:!1,navigationFilter:function(){return this.href.toLowerCase()===location.href.toLowerCase()}},_create:function(){var b=this,c=b.options;b.running=0,b.element.addClass("ui-accordion ui-widget ui-helper-reset").children("li").addClass("ui-accordion-li-fix"),b.headers=b.element.find(c.header).addClass("ui-accordion-header ui-helper-reset ui-state-default ui-corner-all").bind("mouseenter.accordion",function(){if(c.disabled)return;a(this).addClass("ui-state-hover")}).bind("mouseleave.accordion",function(){if(c.disabled)return;a(this).removeClass("ui-state-hover")}).bind("focus.accordion",function(){if(c.disabled)return;a(this).addClass("ui-state-focus")}).bind("blur.accordion",function(){if(c.disabled)return;a(this).removeClass("ui-state-focus")}),b.headers.next().addClass("ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom");if(c.navigation){var d=b.element.find("a").filter(c.navigationFilter).eq(0);if(d.length){var e=d.closest(".ui-accordion-header");e.length?b.active=e:b.active=d.closest(".ui-accordion-content").prev()}}b.active=b._findActive(b.active||c.active).addClass("ui-state-default ui-state-active").toggleClass("ui-corner-all").toggleClass("ui-corner-top"),b.active.next().addClass("ui-accordion-content-active"),b._createIcons(),b.resize(),b.element.attr("role","tablist"),b.headers.attr("role","tab").bind("keydown.accordion",function(a){return b._keydown(a)}).next().attr("role","tabpanel"),b.headers.not(b.active||"").attr({"aria-expanded":"false","aria-selected":"false",tabIndex:-1}).next().hide(),b.active.length?b.active.attr({"aria-expanded":"true","aria-selected":"true",tabIndex:0}):b.headers.eq(0).attr("tabIndex",0),a.browser.safari||b.headers.find("a").attr("tabIndex",-1),c.event&&b.headers.bind(c.event.split(" ").join(".accordion ")+".accordion",function(a){b._clickHandler.call(b,a,this),a.preventDefault()})},_createIcons:function(){var b=this.options;b.icons&&(a("<span></span>").addClass("ui-icon "+b.icons.header).prependTo(this.headers),this.active.children(".ui-icon").toggleClass(b.icons.header).toggleClass(b.icons.headerSelected),this.element.addClass("ui-accordion-icons"))},_destroyIcons:function(){this.headers.children(".ui-icon").remove(),this.element.removeClass("ui-accordion-icons")},destroy:function(){var b=this.options;this.element.removeClass("ui-accordion ui-widget ui-helper-reset").removeAttr("role"),this.headers.unbind(".accordion").removeClass("ui-accordion-header ui-accordion-disabled ui-helper-reset ui-state-default ui-corner-all ui-state-active ui-state-disabled ui-corner-top").removeAttr("role").removeAttr("aria-expanded").removeAttr("aria-selected").removeAttr("tabIndex"),this.headers.find("a").removeAttr("tabIndex"),this._destroyIcons();var c=this.headers.next().css("display","").removeAttr("role").removeClass("ui-helper-reset ui-widget-content ui-corner-bottom ui-accordion-content ui-accordion-content-active ui-accordion-disabled ui-state-disabled");return(b.autoHeight||b.fillHeight)&&c.css("height",""),a.Widget.prototype.destroy.call(this)},_setOption:function(b,c){a.Widget.prototype._setOption.apply(this,arguments),b=="active"&&this.activate(c),b=="icons"&&(this._destroyIcons(),c&&this._createIcons()),b=="disabled"&&this.headers.add(this.headers.next())[c?"addClass":"removeClass"]("ui-accordion-disabled ui-state-disabled")},_keydown:function(b){if(this.options.disabled||b.altKey||b.ctrlKey)return;var c=a.ui.keyCode,d=this.headers.length,e=this.headers.index(b.target),f=!1;switch(b.keyCode){case c.RIGHT:case c.DOWN:f=this.headers[(e+1)%d];break;case c.LEFT:case c.UP:f=this.headers[(e-1+d)%d];break;case c.SPACE:case c.ENTER:this._clickHandler({target:b.target},b.target),b.preventDefault()}return f?(a(b.target).attr("tabIndex",-1),a(f).attr("tabIndex",0),f.focus(),!1):!0},resize:function(){var b=this.options,c;if(b.fillSpace){if(a.browser.msie){var d=this.element.parent().css("overflow");this.element.parent().css("overflow","hidden")}c=this.element.parent().height(),a.browser.msie&&this.element.parent().css("overflow",d),this.headers.each(function(){c-=a(this).outerHeight(!0)}),this.headers.next().each(function(){a(this).height(Math.max(0,c-a(this).innerHeight()+a(this).height()))}).css("overflow","auto")}else b.autoHeight&&(c=0,this.headers.next().each(function(){c=Math.max(c,a(this).height("").height())}).height(c));return this},activate:function(a){this.options.active=a;var b=this._findActive(a)[0];return this._clickHandler({target:b},b),this},_findActive:function(b){return b?typeof b=="number"?this.headers.filter(":eq("+b+")"):this.headers.not(this.headers.not(b)):b===!1?a([]):this.headers.filter(":eq(0)")},_clickHandler:function(b,c){var d=this.options;if(d.disabled)return;if(!b.target){if(!d.collapsible)return;this.active.removeClass("ui-state-active ui-corner-top").addClass("ui-state-default ui-corner-all").children(".ui-icon").removeClass(d.icons.headerSelected).addClass(d.icons.header),this.active.next().addClass("ui-accordion-content-active");var e=this.active.next(),f={options:d,newHeader:a([]),oldHeader:d.active,newContent:a([]),oldContent:e},g=this.active=a([]);this._toggle(g,e,f);return}var h=a(b.currentTarget||c),i=h[0]===this.active[0];d.active=d.collapsible&&i?!1:this.headers.index(h);if(this.running||!d.collapsible&&i)return;var j=this.active,g=h.next(),e=this.active.next(),f={options:d,newHeader:i&&d.collapsible?a([]):h,oldHeader:this.active,newContent:i&&d.collapsible?a([]):g,oldContent:e},k=this.headers.index(this.active[0])>this.headers.index(h[0]);this.active=i?a([]):h,this._toggle(g,e,f,i,k),j.removeClass("ui-state-active ui-corner-top").addClass("ui-state-default ui-corner-all").children(".ui-icon").removeClass(d.icons.headerSelected).addClass(d.icons.header),i||(h.removeClass("ui-state-default ui-corner-all").addClass("ui-state-active ui-corner-top").children(".ui-icon").removeClass(d.icons.header).addClass(d.icons.headerSelected),h.next().addClass("ui-accordion-content-active"));return},_toggle:function(b,c,d,e,f){var g=this,h=g.options;g.toShow=b,g.toHide=c,g.data=d;var i=function(){if(!g)return;return g._completed.apply(g,arguments)};g._trigger("changestart",null,g.data),g.running=c.size()===0?b.size():c.size();if(h.animated){var j={};h.collapsible&&e?j={toShow:a([]),toHide:c,complete:i,down:f,autoHeight:h.autoHeight||h.fillSpace}:j={toShow:b,toHide:c,complete:i,down:f,autoHeight:h.autoHeight||h.fillSpace},h.proxied||(h.proxied=h.animated),h.proxiedDuration||(h.proxiedDuration=h.duration),h.animated=a.isFunction(h.proxied)?h.proxied(j):h.proxied,h.duration=a.isFunction(h.proxiedDuration)?h.proxiedDuration(j):h.proxiedDuration;var k=a.ui.accordion.animations,l=h.duration,m=h.animated;m&&!k[m]&&!a.easing[m]&&(m="slide"),k[m]||(k[m]=function(a){this.slide(a,{easing:m,duration:l||700})}),k[m](j)}else h.collapsible&&e?b.toggle():(c.hide(),b.show()),i(!0);c.prev().attr({"aria-expanded":"false","aria-selected":"false",tabIndex:-1}).blur(),b.prev().attr({"aria-expanded":"true","aria-selected":"true",tabIndex:0}).focus()},_completed:function(a){this.running=a?0:--this.running;if(this.running)return;this.options.clearStyle&&this.toShow.add(this.toHide).css({height:"",overflow:""}),this.toHide.removeClass("ui-accordion-content-active"),this.toHide.length&&(this.toHide.parent()[0].className=this.toHide.parent()[0].className),this._trigger("change",null,this.data)}}),a.extend(a.ui.accordion,{version:"1.8.21",animations:{slide:function(b,c){b=a.extend({easing:"swing",duration:300},b,c);if(!b.toHide.size()){b.toShow.animate({height:"show",paddingTop:"show",paddingBottom:"show"},b);return}if(!b.toShow.size()){b.toHide.animate({height:"hide",paddingTop:"hide",paddingBottom:"hide"},b);return}var d=b.toShow.css("overflow"),e=0,f={},g={},h=["height","paddingTop","paddingBottom"],i,j=b.toShow;i=j[0].style.width,j.width(j.parent().width()-parseFloat(j.css("paddingLeft"))-parseFloat(j.css("paddingRight"))-(parseFloat(j.css("borderLeftWidth"))||0)-(parseFloat(j.css("borderRightWidth"))||0)),a.each(h,function(c,d){g[d]="hide";var e=(""+a.css(b.toShow[0],d)).match(/^([\d+-.]+)(.*)$/);f[d]={value:e[1],unit:e[2]||"px"}}),b.toShow.css({height:0,overflow:"hidden"}).show(),b.toHide.filter(":hidden").each(b.complete).end().filter(":visible").animate(g,{step:function(a,c){c.prop=="height"&&(e=c.end-c.start===0?0:(c.now-c.start)/(c.end-c.start)),b.toShow[0].style[c.prop]=e*f[c.prop].value+f[c.prop].unit},duration:b.duration,easing:b.easing,complete:function(){b.autoHeight||b.toShow.css("height",""),b.toShow.css({width:i,overflow:d}),b.complete()}})},bounceslide:function(a){this.slide(a,{easing:a.down?"easeOutBounce":"swing",duration:a.down?1e3:200})}}})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.autocomplete.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){var c=0;a.widget("ui.autocomplete",{options:{appendTo:"body",autoFocus:!1,delay:300,minLength:1,position:{my:"left top",at:"left bottom",collision:"none"},source:null},pending:0,_create:function(){var b=this,c=this.element[0].ownerDocument,d;this.isMultiLine=this.element.is("textarea"),this.element.addClass("ui-autocomplete-input").attr("autocomplete","off").attr({role:"textbox","aria-autocomplete":"list","aria-haspopup":"true"}).bind("keydown.autocomplete",function(c){if(b.options.disabled||b.element.propAttr("readOnly"))return;d=!1;var e=a.ui.keyCode;switch(c.keyCode){case e.PAGE_UP:b._move("previousPage",c);break;case e.PAGE_DOWN:b._move("nextPage",c);break;case e.UP:b._keyEvent("previous",c);break;case e.DOWN:b._keyEvent("next",c);break;case e.ENTER:case e.NUMPAD_ENTER:b.menu.active&&(d=!0,c.preventDefault());case e.TAB:if(!b.menu.active)return;b.menu.select(c);break;case e.ESCAPE:b.element.val(b.term),b.close(c);break;default:clearTimeout(b.searching),b.searching=setTimeout(function(){b.term!=b.element.val()&&(b.selectedItem=null,b.search(null,c))},b.options.delay)}}).bind("keypress.autocomplete",function(a){d&&(d=!1,a.preventDefault())}).bind("focus.autocomplete",function(){if(b.options.disabled)return;b.selectedItem=null,b.previous=b.element.val()}).bind("blur.autocomplete",function(a){if(b.options.disabled)return;clearTimeout(b.searching),b.closing=setTimeout(function(){b.close(a),b._change(a)},150)}),this._initSource(),this.menu=a("<ul></ul>").addClass("ui-autocomplete").appendTo(a(this.options.appendTo||"body",c)[0]).mousedown(function(c){var d=b.menu.element[0];a(c.target).closest(".ui-menu-item").length||setTimeout(function(){a(document).one("mousedown",function(c){c.target!==b.element[0]&&c.target!==d&&!a.ui.contains(d,c.target)&&b.close()})},1),setTimeout(function(){clearTimeout(b.closing)},13)}).menu({focus:function(a,c){var d=c.item.data("item.autocomplete");!1!==b._trigger("focus",a,{item:d})&&/^key/.test(a.originalEvent.type)&&b.element.val(d.value)},selected:function(a,d){var e=d.item.data("item.autocomplete"),f=b.previous;b.element[0]!==c.activeElement&&(b.element.focus(),b.previous=f,setTimeout(function(){b.previous=f,b.selectedItem=e},1)),!1!==b._trigger("select",a,{item:e})&&b.element.val(e.value),b.term=b.element.val(),b.close(a),b.selectedItem=e},blur:function(a,c){b.menu.element.is(":visible")&&b.element.val()!==b.term&&b.element.val(b.term)}}).zIndex(this.element.zIndex()+1).css({top:0,left:0}).hide().data("menu"),a.fn.bgiframe&&this.menu.element.bgiframe(),b.beforeunloadHandler=function(){b.element.removeAttr("autocomplete")},a(window).bind("beforeunload",b.beforeunloadHandler)},destroy:function(){this.element.removeClass("ui-autocomplete-input").removeAttr("autocomplete").removeAttr("role").removeAttr("aria-autocomplete").removeAttr("aria-haspopup"),this.menu.element.remove(),a(window).unbind("beforeunload",this.beforeunloadHandler),a.Widget.prototype.destroy.call(this)},_setOption:function(b,c){a.Widget.prototype._setOption.apply(this,arguments),b==="source"&&this._initSource(),b==="appendTo"&&this.menu.element.appendTo(a(c||"body",this.element[0].ownerDocument)[0]),b==="disabled"&&c&&this.xhr&&this.xhr.abort()},_initSource:function(){var b=this,c,d;a.isArray(this.options.source)?(c=this.options.source,this.source=function(b,d){d(a.ui.autocomplete.filter(c,b.term))}):typeof this.options.source=="string"?(d=this.options.source,this.source=function(c,e){b.xhr&&b.xhr.abort(),b.xhr=a.ajax({url:d,data:c,dataType:"json",success:function(a,b){e(a)},error:function(){e([])}})}):this.source=this.options.source},search:function(a,b){a=a!=null?a:this.element.val(),this.term=this.element.val();if(a.length<this.options.minLength)return this.close(b);clearTimeout(this.closing);if(this._trigger("search",b)===!1)return;return this._search(a)},_search:function(a){this.pending++,this.element.addClass("ui-autocomplete-loading"),this.source({term:a},this._response())},_response:function(){var a=this,b=++c;return function(d){b===c&&a.__response(d),a.pending--,a.pending||a.element.removeClass("ui-autocomplete-loading")}},__response:function(a){!this.options.disabled&&a&&a.length?(a=this._normalize(a),this._suggest(a),this._trigger("open")):this.close()},close:function(a){clearTimeout(this.closing),this.menu.element.is(":visible")&&(this.menu.element.hide(),this.menu.deactivate(),this._trigger("close",a))},_change:function(a){this.previous!==this.element.val()&&this._trigger("change",a,{item:this.selectedItem})},_normalize:function(b){return b.length&&b[0].label&&b[0].value?b:a.map(b,function(b){return typeof b=="string"?{label:b,value:b}:a.extend({label:b.label||b.value,value:b.value||b.label},b)})},_suggest:function(b){var c=this.menu.element.empty().zIndex(this.element.zIndex()+1);this._renderMenu(c,b),this.menu.deactivate(),this.menu.refresh(),c.show(),this._resizeMenu(),c.position(a.extend({of:this.element},this.options.position)),this.options.autoFocus&&this.menu.next(new a.Event("mouseover"))},_resizeMenu:function(){var a=this.menu.element;a.outerWidth(Math.max(a.width("").outerWidth()+1,this.element.outerWidth()))},_renderMenu:function(b,c){var d=this;a.each(c,function(a,c){d._renderItem(b,c)})},_renderItem:function(b,c){return a("<li></li>").data("item.autocomplete",c).append(a("<a></a>").text(c.label)).appendTo(b)},_move:function(a,b){if(!this.menu.element.is(":visible")){this.search(null,b);return}if(this.menu.first()&&/^previous/.test(a)||this.menu.last()&&/^next/.test(a)){this.element.val(this.term),this.menu.deactivate();return}this.menu[a](b)},widget:function(){return this.menu.element},_keyEvent:function(a,b){if(!this.isMultiLine||this.menu.element.is(":visible"))this._move(a,b),b.preventDefault()}}),a.extend(a.ui.autocomplete,{escapeRegex:function(a){return a.replace(/[-[\]{}()*+?.,\\^$|#\s]/g,"\\$&")},filter:function(b,c){var d=new RegExp(a.ui.autocomplete.escapeRegex(c),"i");return a.grep(b,function(a){return d.test(a.label||a.value||a)})}})})(jQuery),function(a){a.widget("ui.menu",{_create:function(){var b=this;this.element.addClass("ui-menu ui-widget ui-widget-content ui-corner-all").attr({role:"listbox","aria-activedescendant":"ui-active-menuitem"}).click(function(c){if(!a(c.target).closest(".ui-menu-item a").length)return;c.preventDefault(),b.select(c)}),this.refresh()},refresh:function(){var b=this,c=this.element.children("li:not(.ui-menu-item):has(a)").addClass("ui-menu-item").attr("role","menuitem");c.children("a").addClass("ui-corner-all").attr("tabindex",-1).mouseenter(function(c){b.activate(c,a(this).parent())}).mouseleave(function(){b.deactivate()})},activate:function(a,b){this.deactivate();if(this.hasScroll()){var c=b.offset().top-this.element.offset().top,d=this.element.scrollTop(),e=this.element.height();c<0?this.element.scrollTop(d+c):c>=e&&this.element.scrollTop(d+c-e+b.height())}this.active=b.eq(0).children("a").addClass("ui-state-hover").attr("id","ui-active-menuitem").end(),this._trigger("focus",a,{item:b})},deactivate:function(){if(!this.active)return;this.active.children("a").removeClass("ui-state-hover").removeAttr("id"),this._trigger("blur"),this.active=null},next:function(a){this.move("next",".ui-menu-item:first",a)},previous:function(a){this.move("prev",".ui-menu-item:last",a)},first:function(){return this.active&&!this.active.prevAll(".ui-menu-item").length},last:function(){return this.active&&!this.active.nextAll(".ui-menu-item").length},move:function(a,b,c){if(!this.active){this.activate(c,this.element.children(b));return}var d=this.active[a+"All"](".ui-menu-item").eq(0);d.length?this.activate(c,d):this.activate(c,this.element.children(b))},nextPage:function(b){if(this.hasScroll()){if(!this.active||this.last()){this.activate(b,this.element.children(".ui-menu-item:first"));return}var c=this.active.offset().top,d=this.element.height(),e=this.element.children(".ui-menu-item").filter(function(){var b=a(this).offset().top-c-d+a(this).height();return b<10&&b>-10});e.length||(e=this.element.children(".ui-menu-item:last")),this.activate(b,e)}else this.activate(b,this.element.children(".ui-menu-item").filter(!this.active||this.last()?":first":":last"))},previousPage:function(b){if(this.hasScroll()){if(!this.active||this.first()){this.activate(b,this.element.children(".ui-menu-item:last"));return}var c=this.active.offset().top,d=this.element.height(),e=this.element.children(".ui-menu-item").filter(function(){var b=a(this).offset().top-c+d-a(this).height();return b<10&&b>-10});e.length||(e=this.element.children(".ui-menu-item:first")),this.activate(b,e)}else this.activate(b,this.element.children(".ui-menu-item").filter(!this.active||this.first()?":last":":first"))},hasScroll:function(){return this.element.height()<this.element[a.fn.prop?"prop":"attr"]("scrollHeight")},select:function(a){this._trigger("selected",a,{item:this.active})}})}(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.button.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){var c,d,e,f,g="ui-button ui-widget ui-state-default ui-corner-all",h="ui-state-hover ui-state-active ",i="ui-button-icons-only ui-button-icon-only ui-button-text-icons ui-button-text-icon-primary ui-button-text-icon-secondary ui-button-text-only",j=function(){var b=a(this).find(":ui-button");setTimeout(function(){b.button("refresh")},1)},k=function(b){var c=b.name,d=b.form,e=a([]);return c&&(d?e=a(d).find("[name='"+c+"']"):e=a("[name='"+c+"']",b.ownerDocument).filter(function(){return!this.form})),e};a.widget("ui.button",{options:{disabled:null,text:!0,label:null,icons:{primary:null,secondary:null}},_create:function(){this.element.closest("form").unbind("reset.button").bind("reset.button",j),typeof this.options.disabled!="boolean"?this.options.disabled=!!this.element.propAttr("disabled"):this.element.propAttr("disabled",this.options.disabled),this._determineButtonType(),this.hasTitle=!!this.buttonElement.attr("title");var b=this,h=this.options,i=this.type==="checkbox"||this.type==="radio",l="ui-state-hover"+(i?"":" ui-state-active"),m="ui-state-focus";h.label===null&&(h.label=this.buttonElement.html()),this.buttonElement.addClass(g).attr("role","button").bind("mouseenter.button",function(){if(h.disabled)return;a(this).addClass("ui-state-hover"),this===c&&a(this).addClass("ui-state-active")}).bind("mouseleave.button",function(){if(h.disabled)return;a(this).removeClass(l)}).bind("click.button",function(a){h.disabled&&(a.preventDefault(),a.stopImmediatePropagation())}),this.element.bind("focus.button",function(){b.buttonElement.addClass(m)}).bind("blur.button",function(){b.buttonElement.removeClass(m)}),i&&(this.element.bind("change.button",function(){if(f)return;b.refresh()}),this.buttonElement.bind("mousedown.button",function(a){if(h.disabled)return;f=!1,d=a.pageX,e=a.pageY}).bind("mouseup.button",function(a){if(h.disabled)return;if(d!==a.pageX||e!==a.pageY)f=!0})),this.type==="checkbox"?this.buttonElement.bind("click.button",function(){if(h.disabled||f)return!1;a(this).toggleClass("ui-state-active"),b.buttonElement.attr("aria-pressed",b.element[0].checked)}):this.type==="radio"?this.buttonElement.bind("click.button",function(){if(h.disabled||f)return!1;a(this).addClass("ui-state-active"),b.buttonElement.attr("aria-pressed","true");var c=b.element[0];k(c).not(c).map(function(){return a(this).button("widget")[0]}).removeClass("ui-state-active").attr("aria-pressed","false")}):(this.buttonElement.bind("mousedown.button",function(){if(h.disabled)return!1;a(this).addClass("ui-state-active"),c=this,a(document).one("mouseup",function(){c=null})}).bind("mouseup.button",function(){if(h.disabled)return!1;a(this).removeClass("ui-state-active")}).bind("keydown.button",function(b){if(h.disabled)return!1;(b.keyCode==a.ui.keyCode.SPACE||b.keyCode==a.ui.keyCode.ENTER)&&a(this).addClass("ui-state-active")}).bind("keyup.button",function(){a(this).removeClass("ui-state-active")}),this.buttonElement.is("a")&&this.buttonElement.keyup(function(b){b.keyCode===a.ui.keyCode.SPACE&&a(this).click()})),this._setOption("disabled",h.disabled),this._resetButton()},_determineButtonType:function(){this.element.is(":checkbox")?this.type="checkbox":this.element.is(":radio")?this.type="radio":this.element.is("input")?this.type="input":this.type="button";if(this.type==="checkbox"||this.type==="radio"){var a=this.element.parents().filter(":last"),b="label[for='"+this.element.attr("id")+"']";this.buttonElement=a.find(b),this.buttonElement.length||(a=a.length?a.siblings():this.element.siblings(),this.buttonElement=a.filter(b),this.buttonElement.length||(this.buttonElement=a.find(b))),this.element.addClass("ui-helper-hidden-accessible");var c=this.element.is(":checked");c&&this.buttonElement.addClass("ui-state-active"),this.buttonElement.attr("aria-pressed",c)}else this.buttonElement=this.element},widget:function(){return this.buttonElement},destroy:function(){this.element.removeClass("ui-helper-hidden-accessible"),this.buttonElement.removeClass(g+" "+h+" "+i).removeAttr("role").removeAttr("aria-pressed").html(this.buttonElement.find(".ui-button-text").html()),this.hasTitle||this.buttonElement.removeAttr("title"),a.Widget.prototype.destroy.call(this)},_setOption:function(b,c){a.Widget.prototype._setOption.apply(this,arguments);if(b==="disabled"){c?this.element.propAttr("disabled",!0):this.element.propAttr("disabled",!1);return}this._resetButton()},refresh:function(){var b=this.element.is(":disabled");b!==this.options.disabled&&this._setOption("disabled",b),this.type==="radio"?k(this.element[0]).each(function(){a(this).is(":checked")?a(this).button("widget").addClass("ui-state-active").attr("aria-pressed","true"):a(this).button("widget").removeClass("ui-state-active").attr("aria-pressed","false")}):this.type==="checkbox"&&(this.element.is(":checked")?this.buttonElement.addClass("ui-state-active").attr("aria-pressed","true"):this.buttonElement.removeClass("ui-state-active").attr("aria-pressed","false"))},_resetButton:function(){if(this.type==="input"){this.options.label&&this.element.val(this.options.label);return}var b=this.buttonElement.removeClass(i),c=a("<span></span>",this.element[0].ownerDocument).addClass("ui-button-text").html(this.options.label).appendTo(b.empty()).text(),d=this.options.icons,e=d.primary&&d.secondary,f=[];d.primary||d.secondary?(this.options.text&&f.push("ui-button-text-icon"+(e?"s":d.primary?"-primary":"-secondary")),d.primary&&b.prepend("<span class='ui-button-icon-primary ui-icon "+d.primary+"'></span>"),d.secondary&&b.append("<span class='ui-button-icon-secondary ui-icon "+d.secondary+"'></span>"),this.options.text||(f.push(e?"ui-button-icons-only":"ui-button-icon-only"),this.hasTitle||b.attr("title",c))):f.push("ui-button-text-only"),b.addClass(f.join(" "))}}),a.widget("ui.buttonset",{options:{items:":button, :submit, :reset, :checkbox, :radio, a, :data(button)"},_create:function(){this.element.addClass("ui-buttonset")},_init:function(){this.refresh()},_setOption:function(b,c){b==="disabled"&&this.buttons.button("option",b,c),a.Widget.prototype._setOption.apply(this,arguments)},refresh:function(){var b=this.element.css("direction")==="rtl";this.buttons=this.element.find(this.options.items).filter(":ui-button").button("refresh").end().not(":ui-button").button().end().map(function(){return a(this).button("widget")[0]}).removeClass("ui-corner-all ui-corner-left ui-corner-right").filter(":first").addClass(b?"ui-corner-right":"ui-corner-left").end().filter(":last").addClass(b?"ui-corner-left":"ui-corner-right").end().end()},destroy:function(){this.element.removeClass("ui-buttonset"),this.buttons.map(function(){return a(this).button("widget")[0]}).removeClass("ui-corner-left ui-corner-right").end().button("destroy"),a.Widget.prototype.destroy.call(this)}})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.dialog.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){var c="ui-dialog ui-widget ui-widget-content ui-corner-all ",d={buttons:!0,height:!0,maxHeight:!0,maxWidth:!0,minHeight:!0,minWidth:!0,width:!0},e={maxHeight:!0,maxWidth:!0,minHeight:!0,minWidth:!0},f=a.attrFn||{val:!0,css:!0,html:!0,text:!0,data:!0,width:!0,height:!0,offset:!0,click:!0};a.widget("ui.dialog",{options:{autoOpen:!0,buttons:{},closeOnEscape:!0,closeText:"close",dialogClass:"",draggable:!0,hide:null,height:"auto",maxHeight:!1,maxWidth:!1,minHeight:150,minWidth:150,modal:!1,position:{my:"center",at:"center",collision:"fit",using:function(b){var c=a(this).css(b).offset().top;c<0&&a(this).css("top",b.top-c)}},resizable:!0,show:null,stack:!0,title:"",width:300,zIndex:1e3},_create:function(){this.originalTitle=this.element.attr("title"),typeof this.originalTitle!="string"&&(this.originalTitle=""),this.options.title=this.options.title||this.originalTitle;var b=this,d=b.options,e=d.title||"&#160;",f=a.ui.dialog.getTitleId(b.element),g=(b.uiDialog=a("<div></div>")).appendTo(document.body).hide().addClass(c+d.dialogClass).css({zIndex:d.zIndex}).attr("tabIndex",-1).css("outline",0).keydown(function(c){d.closeOnEscape&&!c.isDefaultPrevented()&&c.keyCode&&c.keyCode===a.ui.keyCode.ESCAPE&&(b.close(c),c.preventDefault())}).attr({role:"dialog","aria-labelledby":f}).mousedown(function(a){b.moveToTop(!1,a)}),h=b.element.show().removeAttr("title").addClass("ui-dialog-content ui-widget-content").appendTo(g),i=(b.uiDialogTitlebar=a("<div></div>")).addClass("ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix").prependTo(g),j=a('<a href="#"></a>').addClass("ui-dialog-titlebar-close ui-corner-all").attr("role","button").hover(function(){j.addClass("ui-state-hover")},function(){j.removeClass("ui-state-hover")}).focus(function(){j.addClass("ui-state-focus")}).blur(function(){j.removeClass("ui-state-focus")}).click(function(a){return b.close(a),!1}).appendTo(i),k=(b.uiDialogTitlebarCloseText=a("<span></span>")).addClass("ui-icon ui-icon-closethick").text(d.closeText).appendTo(j),l=a("<span></span>").addClass("ui-dialog-title").attr("id",f).html(e).prependTo(i);a.isFunction(d.beforeclose)&&!a.isFunction(d.beforeClose)&&(d.beforeClose=d.beforeclose),i.find("*").add(i).disableSelection(),d.draggable&&a.fn.draggable&&b._makeDraggable(),d.resizable&&a.fn.resizable&&b._makeResizable(),b._createButtons(d.buttons),b._isOpen=!1,a.fn.bgiframe&&g.bgiframe()},_init:function(){this.options.autoOpen&&this.open()},destroy:function(){var a=this;return a.overlay&&a.overlay.destroy(),a.uiDialog.hide(),a.element.unbind(".dialog").removeData("dialog").removeClass("ui-dialog-content ui-widget-content").hide().appendTo("body"),a.uiDialog.remove(),a.originalTitle&&a.element.attr("title",a.originalTitle),a},widget:function(){return this.uiDialog},close:function(b){var c=this,d,e;if(!1===c._trigger("beforeClose",b))return;return c.overlay&&c.overlay.destroy(),c.uiDialog.unbind("keypress.ui-dialog"),c._isOpen=!1,c.options.hide?c.uiDialog.hide(c.options.hide,function(){c._trigger("close",b)}):(c.uiDialog.hide(),c._trigger("close",b)),a.ui.dialog.overlay.resize(),c.options.modal&&(d=0,a(".ui-dialog").each(function(){this!==c.uiDialog[0]&&(e=a(this).css("z-index"),isNaN(e)||(d=Math.max(d,e)))}),a.ui.dialog.maxZ=d),c},isOpen:function(){return this._isOpen},moveToTop:function(b,c){var d=this,e=d.options,f;return e.modal&&!b||!e.stack&&!e.modal?d._trigger("focus",c):(e.zIndex>a.ui.dialog.maxZ&&(a.ui.dialog.maxZ=e.zIndex),d.overlay&&(a.ui.dialog.maxZ+=1,d.overlay.$el.css("z-index",a.ui.dialog.overlay.maxZ=a.ui.dialog.maxZ)),f={scrollTop:d.element.scrollTop(),scrollLeft:d.element.scrollLeft()},a.ui.dialog.maxZ+=1,d.uiDialog.css("z-index",a.ui.dialog.maxZ),d.element.attr(f),d._trigger("focus",c),d)},open:function(){if(this._isOpen)return;var b=this,c=b.options,d=b.uiDialog;return b.overlay=c.modal?new a.ui.dialog.overlay(b):null,b._size(),b._position(c.position),d.show(c.show),b.moveToTop(!0),c.modal&&d.bind("keydown.ui-dialog",function(b){if(b.keyCode!==a.ui.keyCode.TAB)return;var c=a(":tabbable",this),d=c.filter(":first"),e=c.filter(":last");if(b.target===e[0]&&!b.shiftKey)return d.focus(1),!1;if(b.target===d[0]&&b.shiftKey)return e.focus(1),!1}),a(b.element.find(":tabbable").get().concat(d.find(".ui-dialog-buttonpane :tabbable").get().concat(d.get()))).eq(0).focus(),b._isOpen=!0,b._trigger("open"),b},_createButtons:function(b){var c=this,d=!1,e=a("<div></div>").addClass("ui-dialog-buttonpane ui-widget-content ui-helper-clearfix"),g=a("<div></div>").addClass("ui-dialog-buttonset").appendTo(e);c.uiDialog.find(".ui-dialog-buttonpane").remove(),typeof b=="object"&&b!==null&&a.each(b,function(){return!(d=!0)}),d&&(a.each(b,function(b,d){d=a.isFunction(d)?{click:d,text:b}:d;var e=a('<button type="button"></button>').click(function(){d.click.apply(c.element[0],arguments)}).appendTo(g);a.each(d,function(a,b){if(a==="click")return;a in f?e[a](b):e.attr(a,b)}),a.fn.button&&e.button()}),e.appendTo(c.uiDialog))},_makeDraggable:function(){function f(a){return{position:a.position,offset:a.offset}}var b=this,c=b.options,d=a(document),e;b.uiDialog.draggable({cancel:".ui-dialog-content, .ui-dialog-titlebar-close",handle:".ui-dialog-titlebar",containment:"document",start:function(d,g){e=c.height==="auto"?"auto":a(this).height(),a(this).height(a(this).height()).addClass("ui-dialog-dragging"),b._trigger("dragStart",d,f(g))},drag:function(a,c){b._trigger("drag",a,f(c))},stop:function(g,h){c.position=[h.position.left-d.scrollLeft(),h.position.top-d.scrollTop()],a(this).removeClass("ui-dialog-dragging").height(e),b._trigger("dragStop",g,f(h)),a.ui.dialog.overlay.resize()}})},_makeResizable:function(c){function h(a){return{originalPosition:a.originalPosition,originalSize:a.originalSize,position:a.position,size:a.size}}c=c===b?this.options.resizable:c;var d=this,e=d.options,f=d.uiDialog.css("position"),g=typeof c=="string"?c:"n,e,s,w,se,sw,ne,nw";d.uiDialog.resizable({cancel:".ui-dialog-content",containment:"document",alsoResize:d.element,maxWidth:e.maxWidth,maxHeight:e.maxHeight,minWidth:e.minWidth,minHeight:d._minHeight(),handles:g,start:function(b,c){a(this).addClass("ui-dialog-resizing"),d._trigger("resizeStart",b,h(c))},resize:function(a,b){d._trigger("resize",a,h(b))},stop:function(b,c){a(this).removeClass("ui-dialog-resizing"),e.height=a(this).height(),e.width=a(this).width(),d._trigger("resizeStop",b,h(c)),a.ui.dialog.overlay.resize()}}).css("position",f).find(".ui-resizable-se").addClass("ui-icon ui-icon-grip-diagonal-se")},_minHeight:function(){var a=this.options;return a.height==="auto"?a.minHeight:Math.min(a.minHeight,a.height)},_position:function(b){var c=[],d=[0,0],e;if(b){if(typeof b=="string"||typeof b=="object"&&"0"in b)c=b.split?b.split(" "):[b[0],b[1]],c.length===1&&(c[1]=c[0]),a.each(["left","top"],function(a,b){+c[a]===c[a]&&(d[a]=c[a],c[a]=b)}),b={my:c.join(" "),at:c.join(" "),offset:d.join(" ")};b=a.extend({},a.ui.dialog.prototype.options.position,b)}else b=a.ui.dialog.prototype.options.position;e=this.uiDialog.is(":visible"),e||this.uiDialog.show(),this.uiDialog.css({top:0,left:0}).position(a.extend({of:window},b)),e||this.uiDialog.hide()},_setOptions:function(b){var c=this,f={},g=!1;a.each(b,function(a,b){c._setOption(a,b),a in d&&(g=!0),a in e&&(f[a]=b)}),g&&this._size(),this.uiDialog.is(":data(resizable)")&&this.uiDialog.resizable("option",f)},_setOption:function(b,d){var e=this,f=e.uiDialog;switch(b){case"beforeclose":b="beforeClose";break;case"buttons":e._createButtons(d);break;case"closeText":e.uiDialogTitlebarCloseText.text(""+d);break;case"dialogClass":f.removeClass(e.options.dialogClass).addClass(c+d);break;case"disabled":d?f.addClass("ui-dialog-disabled"):f.removeClass("ui-dialog-disabled");break;case"draggable":var g=f.is(":data(draggable)");g&&!d&&f.draggable("destroy"),!g&&d&&e._makeDraggable();break;case"position":e._position(d);break;case"resizable":var h=f.is(":data(resizable)");h&&!d&&f.resizable("destroy"),h&&typeof d=="string"&&f.resizable("option","handles",d),!h&&d!==!1&&e._makeResizable(d);break;case"title":a(".ui-dialog-title",e.uiDialogTitlebar).html(""+(d||"&#160;"))}a.Widget.prototype._setOption.apply(e,arguments)},_size:function(){var b=this.options,c,d,e=this.uiDialog.is(":visible");this.element.show().css({width:"auto",minHeight:0,height:0}),b.minWidth>b.width&&(b.width=b.minWidth),c=this.uiDialog.css({height:"auto",width:b.width}).height(),d=Math.max(0,b.minHeight-c);if(b.height==="auto")if(a.support.minHeight)this.element.css({minHeight:d,height:"auto"});else{this.uiDialog.show();var f=this.element.css("height","auto").height();e||this.uiDialog.hide(),this.element.height(Math.max(f,d))}else this.element.height(Math.max(b.height-c,0));this.uiDialog.is(":data(resizable)")&&this.uiDialog.resizable("option","minHeight",this._minHeight())}}),a.extend(a.ui.dialog,{version:"1.8.21",uuid:0,maxZ:0,getTitleId:function(a){var b=a.attr("id");return b||(this.uuid+=1,b=this.uuid),"ui-dialog-title-"+b},overlay:function(b){this.$el=a.ui.dialog.overlay.create(b)}}),a.extend(a.ui.dialog.overlay,{instances:[],oldInstances:[],maxZ:0,events:a.map("focus,mousedown,mouseup,keydown,keypress,click".split(","),function(a){return a+".dialog-overlay"}).join(" "),create:function(b){this.instances.length===0&&(setTimeout(function(){a.ui.dialog.overlay.instances.length&&a(document).bind(a.ui.dialog.overlay.events,function(b){if(a(b.target).zIndex()<a.ui.dialog.overlay.maxZ)return!1})},1),a(document).bind("keydown.dialog-overlay",function(c){b.options.closeOnEscape&&!c.isDefaultPrevented()&&c.keyCode&&c.keyCode===a.ui.keyCode.ESCAPE&&(b.close(c),c.preventDefault())}),a(window).bind("resize.dialog-overlay",a.ui.dialog.overlay.resize));var c=(this.oldInstances.pop()||a("<div></div>").addClass("ui-widget-overlay")).appendTo(document.body).css({width:this.width(),height:this.height()});return a.fn.bgiframe&&c.bgiframe(),this.instances.push(c),c},destroy:function(b){var c=a.inArray(b,this.instances);c!=-1&&this.oldInstances.push(this.instances.splice(c,1)[0]),this.instances.length===0&&a([document,window]).unbind(".dialog-overlay"),b.remove();var d=0;a.each(this.instances,function(){d=Math.max(d,this.css("z-index"))}),this.maxZ=d},height:function(){var b,c;return a.browser.msie&&a.browser.version<7?(b=Math.max(document.documentElement.scrollHeight,document.body.scrollHeight),c=Math.max(document.documentElement.offsetHeight,document.body.offsetHeight),b<c?a(window).height()+"px":b+"px"):a(document).height()+"px"},width:function(){var b,c;return a.browser.msie?(b=Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),c=Math.max(document.documentElement.offsetWidth,document.body.offsetWidth),b<c?a(window).width()+"px":b+"px"):a(document).width()+"px"},resize:function(){var b=a([]);a.each(a.ui.dialog.overlay.instances,function(){b=b.add(this)}),b.css({width:0,height:0}).css({width:a.ui.dialog.overlay.width(),height:a.ui.dialog.overlay.height()})}}),a.extend(a.ui.dialog.overlay.prototype,{destroy:function(){a.ui.dialog.overlay.destroy(this.$el)}})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.slider.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){var c=5;a.widget("ui.slider",a.ui.mouse,{widgetEventPrefix:"slide",options:{animate:!1,distance:0,max:100,min:0,orientation:"horizontal",range:!1,step:1,value:0,values:null},_create:function(){var b=this,d=this.options,e=this.element.find(".ui-slider-handle").addClass("ui-state-default ui-corner-all"),f="<a class='ui-slider-handle ui-state-default ui-corner-all' href='#'></a>",g=d.values&&d.values.length||1,h=[];this._keySliding=!1,this._mouseSliding=!1,this._animateOff=!0,this._handleIndex=null,this._detectOrientation(),this._mouseInit(),this.element.addClass("ui-slider ui-slider-"+this.orientation+" ui-widget"+" ui-widget-content"+" ui-corner-all"+(d.disabled?" ui-slider-disabled ui-disabled":"")),this.range=a([]),d.range&&(d.range===!0&&(d.values||(d.values=[this._valueMin(),this._valueMin()]),d.values.length&&d.values.length!==2&&(d.values=[d.values[0],d.values[0]])),this.range=a("<div></div>").appendTo(this.element).addClass("ui-slider-range ui-widget-header"+(d.range==="min"||d.range==="max"?" ui-slider-range-"+d.range:"")));for(var i=e.length;i<g;i+=1)h.push(f);this.handles=e.add(a(h.join("")).appendTo(b.element)),this.handle=this.handles.eq(0),this.handles.add(this.range).filter("a").click(function(a){a.preventDefault()}).hover(function(){d.disabled||a(this).addClass("ui-state-hover")},function(){a(this).removeClass("ui-state-hover")}).focus(function(){d.disabled?a(this).blur():(a(".ui-slider .ui-state-focus").removeClass("ui-state-focus"),a(this).addClass("ui-state-focus"))}).blur(function(){a(this).removeClass("ui-state-focus")}),this.handles.each(function(b){a(this).data("index.ui-slider-handle",b)}),this.handles.keydown(function(d){var e=a(this).data("index.ui-slider-handle"),f,g,h,i;if(b.options.disabled)return;switch(d.keyCode){case a.ui.keyCode.HOME:case a.ui.keyCode.END:case a.ui.keyCode.PAGE_UP:case a.ui.keyCode.PAGE_DOWN:case a.ui.keyCode.UP:case a.ui.keyCode.RIGHT:case a.ui.keyCode.DOWN:case a.ui.keyCode.LEFT:d.preventDefault();if(!b._keySliding){b._keySliding=!0,a(this).addClass("ui-state-active"),f=b._start(d,e);if(f===!1)return}}i=b.options.step,b.options.values&&b.options.values.length?g=h=b.values(e):g=h=b.value();switch(d.keyCode){case a.ui.keyCode.HOME:h=b._valueMin();break;case a.ui.keyCode.END:h=b._valueMax();break;case a.ui.keyCode.PAGE_UP:h=b._trimAlignValue(g+(b._valueMax()-b._valueMin())/c);break;case a.ui.keyCode.PAGE_DOWN:h=b._trimAlignValue(g-(b._valueMax()-b._valueMin())/c);break;case a.ui.keyCode.UP:case a.ui.keyCode.RIGHT:if(g===b._valueMax())return;h=b._trimAlignValue(g+i);break;case a.ui.keyCode.DOWN:case a.ui.keyCode.LEFT:if(g===b._valueMin())return;h=b._trimAlignValue(g-i)}b._slide(d,e,h)}).keyup(function(c){var d=a(this).data("index.ui-slider-handle");b._keySliding&&(b._keySliding=!1,b._stop(c,d),b._change(c,d),a(this).removeClass("ui-state-active"))}),this._refreshValue(),this._animateOff=!1},destroy:function(){return this.handles.remove(),this.range.remove(),this.element.removeClass("ui-slider ui-slider-horizontal ui-slider-vertical ui-slider-disabled ui-widget ui-widget-content ui-corner-all").removeData("slider").unbind(".slider"),this._mouseDestroy(),this},_mouseCapture:function(b){var c=this.options,d,e,f,g,h,i,j,k,l;return c.disabled?!1:(this.elementSize={width:this.element.outerWidth(),height:this.element.outerHeight()},this.elementOffset=this.element.offset(),d={x:b.pageX,y:b.pageY},e=this._normValueFromMouse(d),f=this._valueMax()-this._valueMin()+1,h=this,this.handles.each(function(b){var c=Math.abs(e-h.values(b));f>c&&(f=c,g=a(this),i=b)}),c.range===!0&&this.values(1)===c.min&&(i+=1,g=a(this.handles[i])),j=this._start(b,i),j===!1?!1:(this._mouseSliding=!0,h._handleIndex=i,g.addClass("ui-state-active").focus(),k=g.offset(),l=!a(b.target).parents().andSelf().is(".ui-slider-handle"),this._clickOffset=l?{left:0,top:0}:{left:b.pageX-k.left-g.width()/2,top:b.pageY-k.top-g.height()/2-(parseInt(g.css("borderTopWidth"),10)||0)-(parseInt(g.css("borderBottomWidth"),10)||0)+(parseInt(g.css("marginTop"),10)||0)},this.handles.hasClass("ui-state-hover")||this._slide(b,i,e),this._animateOff=!0,!0))},_mouseStart:function(a){return!0},_mouseDrag:function(a){var b={x:a.pageX,y:a.pageY},c=this._normValueFromMouse(b);return this._slide(a,this._handleIndex,c),!1},_mouseStop:function(a){return this.handles.removeClass("ui-state-active"),this._mouseSliding=!1,this._stop(a,this._handleIndex),this._change(a,this._handleIndex),this._handleIndex=null,this._clickOffset=null,this._animateOff=!1,!1},_detectOrientation:function(){this.orientation=this.options.orientation==="vertical"?"vertical":"horizontal"},_normValueFromMouse:function(a){var b,c,d,e,f;return this.orientation==="horizontal"?(b=this.elementSize.width,c=a.x-this.elementOffset.left-(this._clickOffset?this._clickOffset.left:0)):(b=this.elementSize.height,c=a.y-this.elementOffset.top-(this._clickOffset?this._clickOffset.top:0)),d=c/b,d>1&&(d=1),d<0&&(d=0),this.orientation==="vertical"&&(d=1-d),e=this._valueMax()-this._valueMin(),f=this._valueMin()+d*e,this._trimAlignValue(f)},_start:function(a,b){var c={handle:this.handles[b],value:this.value()};return this.options.values&&this.options.values.length&&(c.value=this.values(b),c.values=this.values()),this._trigger("start",a,c)},_slide:function(a,b,c){var d,e,f;this.options.values&&this.options.values.length?(d=this.values(b?0:1),this.options.values.length===2&&this.options.range===!0&&(b===0&&c>d||b===1&&c<d)&&(c=d),c!==this.values(b)&&(e=this.values(),e[b]=c,f=this._trigger("slide",a,{handle:this.handles[b],value:c,values:e}),d=this.values(b?0:1),f!==!1&&this.values(b,c,!0))):c!==this.value()&&(f=this._trigger("slide",a,{handle:this.handles[b],value:c}),f!==!1&&this.value(c))},_stop:function(a,b){var c={handle:this.handles[b],value:this.value()};this.options.values&&this.options.values.length&&(c.value=this.values(b),c.values=this.values()),this._trigger("stop",a,c)},_change:function(a,b){if(!this._keySliding&&!this._mouseSliding){var c={handle:this.handles[b],value:this.value()};this.options.values&&this.options.values.length&&(c.value=this.values(b),c.values=this.values()),this._trigger("change",a,c)}},value:function(a){if(arguments.length){this.options.value=this._trimAlignValue(a),this._refreshValue(),this._change(null,0);return}return this._value()},values:function(b,c){var d,e,f;if(arguments.length>1){this.options.values[b]=this._trimAlignValue(c),this._refreshValue(),this._change(null,b);return}if(!arguments.length)return this._values();if(!a.isArray(arguments[0]))return this.options.values&&this.options.values.length?this._values(b):this.value();d=this.options.values,e=arguments[0];for(f=0;f<d.length;f+=1)d[f]=this._trimAlignValue(e[f]),this._change(null,f);this._refreshValue()},_setOption:function(b,c){var d,e=0;a.isArray(this.options.values)&&(e=this.options.values.length),a.Widget.prototype._setOption.apply(this,arguments);switch(b){case"disabled":c?(this.handles.filter(".ui-state-focus").blur(),this.handles.removeClass("ui-state-hover"),this.handles.propAttr("disabled",!0),this.element.addClass("ui-disabled")):(this.handles.propAttr("disabled",!1),this.element.removeClass("ui-disabled"));break;case"orientation":this._detectOrientation(),this.element.removeClass("ui-slider-horizontal ui-slider-vertical").addClass("ui-slider-"+this.orientation),this._refreshValue();break;case"value":this._animateOff=!0,this._refreshValue(),this._change(null,0),this._animateOff=!1;break;case"values":this._animateOff=!0,this._refreshValue();for(d=0;d<e;d+=1)this._change(null,d);this._animateOff=!1}},_value:function(){var a=this.options.value;return a=this._trimAlignValue(a),a},_values:function(a){var b,c,d;if(arguments.length)return b=this.options.values[a],b=this._trimAlignValue(b),b;c=this.options.values.slice();for(d=0;d<c.length;d+=1)c[d]=this._trimAlignValue(c[d]);return c},_trimAlignValue:function(a){if(a<=this._valueMin())return this._valueMin();if(a>=this._valueMax())return this._valueMax();var b=this.options.step>0?this.options.step:1,c=(a-this._valueMin())%b,d=a-c;return Math.abs(c)*2>=b&&(d+=c>0?b:-b),parseFloat(d.toFixed(5))},_valueMin:function(){return this.options.min},_valueMax:function(){return this.options.max},_refreshValue:function(){var b=this.options.range,c=this.options,d=this,e=this._animateOff?!1:c.animate,f,g={},h,i,j,k;this.options.values&&this.options.values.length?this.handles.each(function(b,i){f=(d.values(b)-d._valueMin())/(d._valueMax()-d._valueMin())*100,g[d.orientation==="horizontal"?"left":"bottom"]=f+"%",a(this).stop(1,1)[e?"animate":"css"](g,c.animate),d.options.range===!0&&(d.orientation==="horizontal"?(b===0&&d.range.stop(1,1)[e?"animate":"css"]({left:f+"%"},c.animate),b===1&&d.range[e?"animate":"css"]({width:f-h+"%"},{queue:!1,duration:c.animate})):(b===0&&d.range.stop(1,1)[e?"animate":"css"]({bottom:f+"%"},c.animate),b===1&&d.range[e?"animate":"css"]({height:f-h+"%"},{queue:!1,duration:c.animate}))),h=f}):(i=this.value(),j=this._valueMin(),k=this._valueMax(),f=k!==j?(i-j)/(k-j)*100:0,g[d.orientation==="horizontal"?"left":"bottom"]=f+"%",this.handle.stop(1,1)[e?"animate":"css"](g,c.animate),b==="min"&&this.orientation==="horizontal"&&this.range.stop(1,1)[e?"animate":"css"]({width:f+"%"},c.animate),b==="max"&&this.orientation==="horizontal"&&this.range[e?"animate":"css"]({width:100-f+"%"},{queue:!1,duration:c.animate}),b==="min"&&this.orientation==="vertical"&&this.range.stop(1,1)[e?"animate":"css"]({height:f+"%"},c.animate),b==="max"&&this.orientation==="vertical"&&this.range[e?"animate":"css"]({height:100-f+"%"},{queue:!1,duration:c.animate}))}}),a.extend(a.ui.slider,{version:"1.8.21"})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.tabs.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){function e(){return++c}function f(){return++d}var c=0,d=0;a.widget("ui.tabs",{options:{add:null,ajaxOptions:null,cache:!1,cookie:null,collapsible:!1,disable:null,disabled:[],enable:null,event:"click",fx:null,idPrefix:"ui-tabs-",load:null,panelTemplate:"<div></div>",remove:null,select:null,show:null,spinner:"<em>Loading&#8230;</em>",tabTemplate:"<li><a href='#{href}'><span>#{label}</span></a></li>"},_create:function(){this._tabify(!0)},_setOption:function(a,b){if(a=="selected"){if(this.options.collapsible&&b==this.options.selected)return;this.select(b)}else this.options[a]=b,this._tabify()},_tabId:function(a){return a.title&&a.title.replace(/\s/g,"_").replace(/[^\w\u00c0-\uFFFF-]/g,"")||this.options.idPrefix+e()},_sanitizeSelector:function(a){return a.replace(/:/g,"\\:")},_cookie:function(){var b=this.cookie||(this.cookie=this.options.cookie.name||"ui-tabs-"+f());return a.cookie.apply(null,[b].concat(a.makeArray(arguments)))},_ui:function(a,b){return{tab:a,panel:b,index:this.anchors.index(a)}},_cleanup:function(){this.lis.filter(".ui-state-processing").removeClass("ui-state-processing").find("span:data(label.tabs)").each(function(){var b=a(this);b.html(b.data("label.tabs")).removeData("label.tabs")})},_tabify:function(c){function m(b,c){b.css("display",""),!a.support.opacity&&c.opacity&&b[0].style.removeAttribute("filter")}var d=this,e=this.options,f=/^#.+/;this.list=this.element.find("ol,ul").eq(0),this.lis=a(" > li:has(a[href])",this.list),this.anchors=this.lis.map(function(){return a("a",this)[0]}),this.panels=a([]),this.anchors.each(function(b,c){var g=a(c).attr("href"),h=g.split("#")[0],i;h&&(h===location.toString().split("#")[0]||(i=a("base")[0])&&h===i.href)&&(g=c.hash,c.href=g);if(f.test(g))d.panels=d.panels.add(d.element.find(d._sanitizeSelector(g)));else if(g&&g!=="#"){a.data(c,"href.tabs",g),a.data(c,"load.tabs",g.replace(/#.*$/,""));var j=d._tabId(c);c.href="#"+j;var k=d.element.find("#"+j);k.length||(k=a(e.panelTemplate).attr("id",j).addClass("ui-tabs-panel ui-widget-content ui-corner-bottom").insertAfter(d.panels[b-1]||d.list),k.data("destroy.tabs",!0)),d.panels=d.panels.add(k)}else e.disabled.push(b)}),c?(this.element.addClass("ui-tabs ui-widget ui-widget-content ui-corner-all"),this.list.addClass("ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all"),this.lis.addClass("ui-state-default ui-corner-top"),this.panels.addClass("ui-tabs-panel ui-widget-content ui-corner-bottom"),e.selected===b?(location.hash&&this.anchors.each(function(a,b){if(b.hash==location.hash)return e.selected=a,!1}),typeof e.selected!="number"&&e.cookie&&(e.selected=parseInt(d._cookie(),10)),typeof e.selected!="number"&&this.lis.filter(".ui-tabs-selected").length&&(e.selected=this.lis.index(this.lis.filter(".ui-tabs-selected"))),e.selected=e.selected||(this.lis.length?0:-1)):e.selected===null&&(e.selected=-1),e.selected=e.selected>=0&&this.anchors[e.selected]||e.selected<0?e.selected:0,e.disabled=a.unique(e.disabled.concat(a.map(this.lis.filter(".ui-state-disabled"),function(a,b){return d.lis.index(a)}))).sort(),a.inArray(e.selected,e.disabled)!=-1&&e.disabled.splice(a.inArray(e.selected,e.disabled),1),this.panels.addClass("ui-tabs-hide"),this.lis.removeClass("ui-tabs-selected ui-state-active"),e.selected>=0&&this.anchors.length&&(d.element.find(d._sanitizeSelector(d.anchors[e.selected].hash)).removeClass("ui-tabs-hide"),this.lis.eq(e.selected).addClass("ui-tabs-selected ui-state-active"),d.element.queue("tabs",function(){d._trigger("show",null,d._ui(d.anchors[e.selected],d.element.find(d._sanitizeSelector(d.anchors[e.selected].hash))[0]))}),this.load(e.selected)),a(window).bind("unload",function(){d.lis.add(d.anchors).unbind(".tabs"),d.lis=d.anchors=d.panels=null})):e.selected=this.lis.index(this.lis.filter(".ui-tabs-selected")),this.element[e.collapsible?"addClass":"removeClass"]("ui-tabs-collapsible"),e.cookie&&this._cookie(e.selected,e.cookie);for(var g=0,h;h=this.lis[g];g++)a(h)[a.inArray(g,e.disabled)!=-1&&!a(h).hasClass("ui-tabs-selected")?"addClass":"removeClass"]("ui-state-disabled");e.cache===!1&&this.anchors.removeData("cache.tabs"),this.lis.add(this.anchors).unbind(".tabs");if(e.event!=="mouseover"){var i=function(a,b){b.is(":not(.ui-state-disabled)")&&b.addClass("ui-state-"+a)},j=function(a,b){b.removeClass("ui-state-"+a)};this.lis.bind("mouseover.tabs",function(){i("hover",a(this))}),this.lis.bind("mouseout.tabs",function(){j("hover",a(this))}),this.anchors.bind("focus.tabs",function(){i("focus",a(this).closest("li"))}),this.anchors.bind("blur.tabs",function(){j("focus",a(this).closest("li"))})}var k,l;e.fx&&(a.isArray(e.fx)?(k=e.fx[0],l=e.fx[1]):k=l=e.fx);var n=l?function(b,c){a(b).closest("li").addClass("ui-tabs-selected ui-state-active"),c.hide().removeClass("ui-tabs-hide").animate(l,l.duration||"normal",function(){m(c,l),d._trigger("show",null,d._ui(b,c[0]))})}:function(b,c){a(b).closest("li").addClass("ui-tabs-selected ui-state-active"),c.removeClass("ui-tabs-hide"),d._trigger("show",null,d._ui(b,c[0]))},o=k?function(a,b){b.animate(k,k.duration||"normal",function(){d.lis.removeClass("ui-tabs-selected ui-state-active"),b.addClass("ui-tabs-hide"),m(b,k),d.element.dequeue("tabs")})}:function(a,b,c){d.lis.removeClass("ui-tabs-selected ui-state-active"),b.addClass("ui-tabs-hide"),d.element.dequeue("tabs")};this.anchors.bind(e.event+".tabs",function(){var b=this,c=a(b).closest("li"),f=d.panels.filter(":not(.ui-tabs-hide)"),g=d.element.find(d._sanitizeSelector(b.hash));if(c.hasClass("ui-tabs-selected")&&!e.collapsible||c.hasClass("ui-state-disabled")||c.hasClass("ui-state-processing")||d.panels.filter(":animated").length||d._trigger("select",null,d._ui(this,g[0]))===!1)return this.blur(),!1;e.selected=d.anchors.index(this),d.abort();if(e.collapsible){if(c.hasClass("ui-tabs-selected"))return e.selected=-1,e.cookie&&d._cookie(e.selected,e.cookie),d.element.queue("tabs",function(){o(b,f)}).dequeue("tabs"),this.blur(),!1;if(!f.length)return e.cookie&&d._cookie(e.selected,e.cookie),d.element.queue("tabs",function(){n(b,g)}),d.load(d.anchors.index(this)),this.blur(),!1}e.cookie&&d._cookie(e.selected,e.cookie);if(g.length)f.length&&d.element.queue("tabs",function(){o(b,f)}),d.element.queue("tabs",function(){n(b,g)}),d.load(d.anchors.index(this));else throw"jQuery UI Tabs: Mismatching fragment identifier.";a.browser.msie&&this.blur()}),this.anchors.bind("click.tabs",function(){return!1})},_getIndex:function(a){return typeof a=="string"&&(a=this.anchors.index(this.anchors.filter("[href$='"+a+"']"))),a},destroy:function(){var b=this.options;return this.abort(),this.element.unbind(".tabs").removeClass("ui-tabs ui-widget ui-widget-content ui-corner-all ui-tabs-collapsible").removeData("tabs"),this.list.removeClass("ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all"),this.anchors.each(function(){var b=a.data(this,"href.tabs");b&&(this.href=b);var c=a(this).unbind(".tabs");a.each(["href","load","cache"],function(a,b){c.removeData(b+".tabs")})}),this.lis.unbind(".tabs").add(this.panels).each(function(){a.data(this,"destroy.tabs")?a(this).remove():a(this).removeClass(["ui-state-default","ui-corner-top","ui-tabs-selected","ui-state-active","ui-state-hover","ui-state-focus","ui-state-disabled","ui-tabs-panel","ui-widget-content","ui-corner-bottom","ui-tabs-hide"].join(" "))}),b.cookie&&this._cookie(null,b.cookie),this},add:function(c,d,e){e===b&&(e=this.anchors.length);var f=this,g=this.options,h=a(g.tabTemplate.replace(/#\{href\}/g,c).replace(/#\{label\}/g,d)),i=c.indexOf("#")?this._tabId(a("a",h)[0]):c.replace("#","");h.addClass("ui-state-default ui-corner-top").data("destroy.tabs",!0);var j=f.element.find("#"+i);return j.length||(j=a(g.panelTemplate).attr("id",i).data("destroy.tabs",!0)),j.addClass("ui-tabs-panel ui-widget-content ui-corner-bottom ui-tabs-hide"),e>=this.lis.length?(h.appendTo(this.list),j.appendTo(this.list[0].parentNode)):(h.insertBefore(this.lis[e]),j.insertBefore(this.panels[e])),g.disabled=a.map(g.disabled,function(a,b){return a>=e?++a:a}),this._tabify(),this.anchors.length==1&&(g.selected=0,h.addClass("ui-tabs-selected ui-state-active"),j.removeClass("ui-tabs-hide"),this.element.queue("tabs",function(){f._trigger("show",null,f._ui(f.anchors[0],f.panels[0]))}),this.load(0)),this._trigger("add",null,this._ui(this.anchors[e],this.panels[e])),this},remove:function(b){b=this._getIndex(b);var c=this.options,d=this.lis.eq(b).remove(),e=this.panels.eq(b).remove();return d.hasClass("ui-tabs-selected")&&this.anchors.length>1&&this.select(b+(b+1<this.anchors.length?1:-1)),c.disabled=a.map(a.grep(c.disabled,function(a,c){return a!=b}),function(a,c){return a>=b?--a:a}),this._tabify(),this._trigger("remove",null,this._ui(d.find("a")[0],e[0])),this},enable:function(b){b=this._getIndex(b);var c=this.options;if(a.inArray(b,c.disabled)==-1)return;return this.lis.eq(b).removeClass("ui-state-disabled"),c.disabled=a.grep(c.disabled,function(a,c){return a!=b}),this._trigger("enable",null,this._ui(this.anchors[b],this.panels[b])),this},disable:function(a){a=this._getIndex(a);var b=this,c=this.options;return a!=c.selected&&(this.lis.eq(a).addClass("ui-state-disabled"),c.disabled.push(a),c.disabled.sort(),this._trigger("disable",null,this._ui(this.anchors[a],this.panels[a]))),this},select:function(a){a=this._getIndex(a);if(a==-1)if(this.options.collapsible&&this.options.selected!=-1)a=this.options.selected;else return this;return this.anchors.eq(a).trigger(this.options.event+".tabs"),this},load:function(b){b=this._getIndex(b);var c=this,d=this.options,e=this.anchors.eq(b)[0],f=a.data(e,"load.tabs");this.abort();if(!f||this.element.queue("tabs").length!==0&&a.data(e,"cache.tabs")){this.element.dequeue("tabs");return}this.lis.eq(b).addClass("ui-state-processing");if(d.spinner){var g=a("span",e);g.data("label.tabs",g.html()).html(d.spinner)}return this.xhr=a.ajax(a.extend({},d.ajaxOptions,{url:f,success:function(f,g){c.element.find(c._sanitizeSelector(e.hash)).html(f),c._cleanup(),d.cache&&a.data(e,"cache.tabs",!0),c._trigger("load",null,c._ui(c.anchors[b],c.panels[b]));try{d.ajaxOptions.success(f,g)}catch(h){}},error:function(a,f,g){c._cleanup(),c._trigger("load",null,c._ui(c.anchors[b],c.panels[b]));try{d.ajaxOptions.error(a,f,b,e)}catch(g){}}})),c.element.dequeue("tabs"),this},abort:function(){return this.element.queue([]),this.panels.stop(!1,!0),this.element.queue("tabs",this.element.queue("tabs").splice(-2,2)),this.xhr&&(this.xhr.abort(),delete this.xhr),this._cleanup(),this},url:function(a,b){return this.anchors.eq(a).removeData("cache.tabs").data("load.tabs",b),this},length:function(){return this.anchors.length}}),a.extend(a.ui.tabs,{version:"1.8.21"}),a.extend(a.ui.tabs.prototype,{rotation:null,rotate:function(a,b){var c=this,d=this.options,e=c._rotate||(c._rotate=function(b){clearTimeout(c.rotation),c.rotation=setTimeout(function(){var a=d.selected;c.select(++a<c.anchors.length?a:0)},a),b&&b.stopPropagation()}),f=c._unrotate||(c._unrotate=b?function(a){e()}:function(a){a.clientX&&c.rotate(null)});return a?(this.element.bind("tabsshow",e),this.anchors.bind(d.event+".tabs",f),e()):(clearTimeout(c.rotation),this.element.unbind("tabsshow",e),this.anchors.unbind(d.event+".tabs",f),delete this._rotate,delete this._unrotate),this}})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.datepicker.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function($,undefined){function Datepicker(){this.debug=!1,this._curInst=null,this._keyEvent=!1,this._disabledInputs=[],this._datepickerShowing=!1,this._inDialog=!1,this._mainDivId="ui-datepicker-div",this._inlineClass="ui-datepicker-inline",this._appendClass="ui-datepicker-append",this._triggerClass="ui-datepicker-trigger",this._dialogClass="ui-datepicker-dialog",this._disableClass="ui-datepicker-disabled",this._unselectableClass="ui-datepicker-unselectable",this._currentClass="ui-datepicker-current-day",this._dayOverClass="ui-datepicker-days-cell-over",this.regional=[],this.regional[""]={closeText:"Done",prevText:"Prev",nextText:"Next",currentText:"Today",monthNames:["January","February","March","April","May","June","July","August","September","October","November","December"],monthNamesShort:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],dayNames:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],dayNamesShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],dayNamesMin:["Su","Mo","Tu","We","Th","Fr","Sa"],weekHeader:"Wk",dateFormat:"mm/dd/yy",firstDay:0,isRTL:!1,showMonthAfterYear:!1,yearSuffix:""},this._defaults={showOn:"focus",showAnim:"fadeIn",showOptions:{},defaultDate:null,appendText:"",buttonText:"...",buttonImage:"",buttonImageOnly:!1,hideIfNoPrevNext:!1,navigationAsDateFormat:!1,gotoCurrent:!1,changeMonth:!1,changeYear:!1,yearRange:"c-10:c+10",showOtherMonths:!1,selectOtherMonths:!1,showWeek:!1,calculateWeek:this.iso8601Week,shortYearCutoff:"+10",minDate:null,maxDate:null,duration:"fast",beforeShowDay:null,beforeShow:null,onSelect:null,onChangeMonthYear:null,onClose:null,numberOfMonths:1,showCurrentAtPos:0,stepMonths:1,stepBigMonths:12,altField:"",altFormat:"",constrainInput:!0,showButtonPanel:!1,autoSize:!1,disabled:!1},$.extend(this._defaults,this.regional[""]),this.dpDiv=bindHover($('<div id="'+this._mainDivId+'" class="ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all"></div>'))}function bindHover(a){var b="button, .ui-datepicker-prev, .ui-datepicker-next, .ui-datepicker-calendar td a";return a.bind("mouseout",function(a){var c=$(a.target).closest(b);if(!c.length)return;c.removeClass("ui-state-hover ui-datepicker-prev-hover ui-datepicker-next-hover")}).bind("mouseover",function(c){var d=$(c.target).closest(b);if($.datepicker._isDisabledDatepicker(instActive.inline?a.parent()[0]:instActive.input[0])||!d.length)return;d.parents(".ui-datepicker-calendar").find("a").removeClass("ui-state-hover"),d.addClass("ui-state-hover"),d.hasClass("ui-datepicker-prev")&&d.addClass("ui-datepicker-prev-hover"),d.hasClass("ui-datepicker-next")&&d.addClass("ui-datepicker-next-hover")})}function extendRemove(a,b){$.extend(a,b);for(var c in b)if(b[c]==null||b[c]==undefined)a[c]=b[c];return a}function isArray(a){return a&&($.browser.safari&&typeof a=="object"&&a.length||a.constructor&&a.constructor.toString().match(/\Array\(\)/))}$.extend($.ui,{datepicker:{version:"1.8.21"}});var PROP_NAME="datepicker",dpuuid=(new Date).getTime(),instActive;$.extend(Datepicker.prototype,{markerClassName:"hasDatepicker",maxRows:4,log:function(){this.debug&&console.log.apply("",arguments)},_widgetDatepicker:function(){return this.dpDiv},setDefaults:function(a){return extendRemove(this._defaults,a||{}),this},_attachDatepicker:function(target,settings){var inlineSettings=null;for(var attrName in this._defaults){var attrValue=target.getAttribute("date:"+attrName);if(attrValue){inlineSettings=inlineSettings||{};try{inlineSettings[attrName]=eval(attrValue)}catch(err){inlineSettings[attrName]=attrValue}}}var nodeName=target.nodeName.toLowerCase(),inline=nodeName=="div"||nodeName=="span";target.id||(this.uuid+=1,target.id="dp"+this.uuid);var inst=this._newInst($(target),inline);inst.settings=$.extend({},settings||{},inlineSettings||{}),nodeName=="input"?this._connectDatepicker(target,inst):inline&&this._inlineDatepicker(target,inst)},_newInst:function(a,b){var c=a[0].id.replace(/([^A-Za-z0-9_-])/g,"\\\\$1");return{id:c,input:a,selectedDay:0,selectedMonth:0,selectedYear:0,drawMonth:0,drawYear:0,inline:b,dpDiv:b?bindHover($('<div class="'+this._inlineClass+' ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all"></div>')):this.dpDiv}},_connectDatepicker:function(a,b){var c=$(a);b.append=$([]),b.trigger=$([]);if(c.hasClass(this.markerClassName))return;this._attachments(c,b),c.addClass(this.markerClassName).keydown(this._doKeyDown).keypress(this._doKeyPress).keyup(this._doKeyUp).bind("setData.datepicker",function(a,c,d){b.settings[c]=d}).bind("getData.datepicker",function(a,c){return this._get(b,c)}),this._autoSize(b),$.data(a,PROP_NAME,b),b.settings.disabled&&this._disableDatepicker(a)},_attachments:function(a,b){var c=this._get(b,"appendText"),d=this._get(b,"isRTL");b.append&&b.append.remove(),c&&(b.append=$('<span class="'+this._appendClass+'">'+c+"</span>"),a[d?"before":"after"](b.append)),a.unbind("focus",this._showDatepicker),b.trigger&&b.trigger.remove();var e=this._get(b,"showOn");(e=="focus"||e=="both")&&a.focus(this._showDatepicker);if(e=="button"||e=="both"){var f=this._get(b,"buttonText"),g=this._get(b,"buttonImage");b.trigger=$(this._get(b,"buttonImageOnly")?$("<img/>").addClass(this._triggerClass).attr({src:g,alt:f,title:f}):$('<button type="button"></button>').addClass(this._triggerClass).html(g==""?f:$("<img/>").attr({src:g,alt:f,title:f}))),a[d?"before":"after"](b.trigger),b.trigger.click(function(){return $.datepicker._datepickerShowing&&$.datepicker._lastInput==a[0]?$.datepicker._hideDatepicker():$.datepicker._datepickerShowing&&$.datepicker._lastInput!=a[0]?($.datepicker._hideDatepicker(),$.datepicker._showDatepicker(a[0])):$.datepicker._showDatepicker(a[0]),!1})}},_autoSize:function(a){if(this._get(a,"autoSize")&&!a.inline){var b=new Date(2009,11,20),c=this._get(a,"dateFormat");if(c.match(/[DM]/)){var d=function(a){var b=0,c=0;for(var d=0;d<a.length;d++)a[d].length>b&&(b=a[d].length,c=d);return c};b.setMonth(d(this._get(a,c.match(/MM/)?"monthNames":"monthNamesShort"))),b.setDate(d(this._get(a,c.match(/DD/)?"dayNames":"dayNamesShort"))+20-b.getDay())}a.input.attr("size",this._formatDate(a,b).length)}},_inlineDatepicker:function(a,b){var c=$(a);if(c.hasClass(this.markerClassName))return;c.addClass(this.markerClassName).append(b.dpDiv).bind("setData.datepicker",function(a,c,d){b.settings[c]=d}).bind("getData.datepicker",function(a,c){return this._get(b,c)}),$.data(a,PROP_NAME,b),this._setDate(b,this._getDefaultDate(b),!0),this._updateDatepicker(b),this._updateAlternate(b),b.settings.disabled&&this._disableDatepicker(a),b.dpDiv.css("display","block")},_dialogDatepicker:function(a,b,c,d,e){var f=this._dialogInst;if(!f){this.uuid+=1;var g="dp"+this.uuid;this._dialogInput=$('<input type="text" id="'+g+'" style="position: absolute; top: -100px; width: 0px; z-index: -10;"/>'),this._dialogInput.keydown(this._doKeyDown),$("body").append(this._dialogInput),f=this._dialogInst=this._newInst(this._dialogInput,!1),f.settings={},$.data(this._dialogInput[0],PROP_NAME,f)}extendRemove(f.settings,d||{}),b=b&&b.constructor==Date?this._formatDate(f,b):b,this._dialogInput.val(b),this._pos=e?e.length?e:[e.pageX,e.pageY]:null;if(!this._pos){var h=document.documentElement.clientWidth,i=document.documentElement.clientHeight,j=document.documentElement.scrollLeft||document.body.scrollLeft,k=document.documentElement.scrollTop||document.body.scrollTop;this._pos=[h/2-100+j,i/2-150+k]}return this._dialogInput.css("left",this._pos[0]+20+"px").css("top",this._pos[1]+"px"),f.settings.onSelect=c,this._inDialog=!0,this.dpDiv.addClass(this._dialogClass),this._showDatepicker(this._dialogInput[0]),$.blockUI&&$.blockUI(this.dpDiv),$.data(this._dialogInput[0],PROP_NAME,f),this},_destroyDatepicker:function(a){var b=$(a),c=$.data(a,PROP_NAME);if(!b.hasClass(this.markerClassName))return;var d=a.nodeName.toLowerCase();$.removeData(a,PROP_NAME),d=="input"?(c.append.remove(),c.trigger.remove(),b.removeClass(this.markerClassName).unbind("focus",this._showDatepicker).unbind("keydown",this._doKeyDown).unbind("keypress",this._doKeyPress).unbind("keyup",this._doKeyUp)):(d=="div"||d=="span")&&b.removeClass(this.markerClassName).empty()},_enableDatepicker:function(a){var b=$(a),c=$.data(a,PROP_NAME);if(!b.hasClass(this.markerClassName))return;var d=a.nodeName.toLowerCase();if(d=="input")a.disabled=!1,c.trigger.filter("button").each(function(){this.disabled=!1}).end().filter("img").css({opacity:"1.0",cursor:""});else if(d=="div"||d=="span"){var e=b.children("."+this._inlineClass);e.children().removeClass("ui-state-disabled"),e.find("select.ui-datepicker-month, select.ui-datepicker-year").removeAttr("disabled")}this._disabledInputs=$.map(this._disabledInputs,function(b){return b==a?null:b})},_disableDatepicker:function(a){var b=$(a),c=$.data(a,PROP_NAME);if(!b.hasClass(this.markerClassName))return;var d=a.nodeName.toLowerCase();if(d=="input")a.disabled=!0,c.trigger.filter("button").each(function(){this.disabled=!0}).end().filter("img").css({opacity:"0.5",cursor:"default"});else if(d=="div"||d=="span"){var e=b.children("."+this._inlineClass);e.children().addClass("ui-state-disabled"),e.find("select.ui-datepicker-month, select.ui-datepicker-year").attr("disabled","disabled")}this._disabledInputs=$.map(this._disabledInputs,function(b){return b==a?null:b}),this._disabledInputs[this._disabledInputs.length]=a},_isDisabledDatepicker:function(a){if(!a)return!1;for(var b=0;b<this._disabledInputs.length;b++)if(this._disabledInputs[b]==a)return!0;return!1},_getInst:function(a){try{return $.data(a,PROP_NAME)}catch(b){throw"Missing instance data for this datepicker"}},_optionDatepicker:function(a,b,c){var d=this._getInst(a);if(arguments.length==2&&typeof b=="string")return b=="defaults"?$.extend({},$.datepicker._defaults):d?b=="all"?$.extend({},d.settings):this._get(d,b):null;var e=b||{};typeof b=="string"&&(e={},e[b]=c);if(d){this._curInst==d&&this._hideDatepicker();var f=this._getDateDatepicker(a,!0),g=this._getMinMaxDate(d,"min"),h=this._getMinMaxDate(d,"max");extendRemove(d.settings,e),g!==null&&e.dateFormat!==undefined&&e.minDate===undefined&&(d.settings.minDate=this._formatDate(d,g)),h!==null&&e.dateFormat!==undefined&&e.maxDate===undefined&&(d.settings.maxDate=this._formatDate(d,h)),this._attachments($(a),d),this._autoSize(d),this._setDate(d,f),this._updateAlternate(d),this._updateDatepicker(d)}},_changeDatepicker:function(a,b,c){this._optionDatepicker(a,b,c)},_refreshDatepicker:function(a){var b=this._getInst(a);b&&this._updateDatepicker(b)},_setDateDatepicker:function(a,b){var c=this._getInst(a);c&&(this._setDate(c,b),this._updateDatepicker(c),this._updateAlternate(c))},_getDateDatepicker:function(a,b){var c=this._getInst(a);return c&&!c.inline&&this._setDateFromField(c,b),c?this._getDate(c):null},_doKeyDown:function(a){var b=$.datepicker._getInst(a.target),c=!0,d=b.dpDiv.is(".ui-datepicker-rtl");b._keyEvent=!0;if($.datepicker._datepickerShowing)switch(a.keyCode){case 9:$.datepicker._hideDatepicker(),c=!1;break;case 13:var e=$("td."+$.datepicker._dayOverClass+":not(."+$.datepicker._currentClass+")",b.dpDiv);e[0]&&$.datepicker._selectDay(a.target,b.selectedMonth,b.selectedYear,e[0]);var f=$.datepicker._get(b,"onSelect");if(f){var g=$.datepicker._formatDate(b);f.apply(b.input?b.input[0]:null,[g,b])}else $.datepicker._hideDatepicker();return!1;case 27:$.datepicker._hideDatepicker();break;case 33:$.datepicker._adjustDate(a.target,a.ctrlKey?-$.datepicker._get(b,"stepBigMonths"):-$.datepicker._get(b,"stepMonths"),"M");break;case 34:$.datepicker._adjustDate(a.target,a.ctrlKey?+$.datepicker._get(b,"stepBigMonths"):+$.datepicker._get(b,"stepMonths"),"M");break;case 35:(a.ctrlKey||a.metaKey)&&$.datepicker._clearDate(a.target),c=a.ctrlKey||a.metaKey;break;case 36:(a.ctrlKey||a.metaKey)&&$.datepicker._gotoToday(a.target),c=a.ctrlKey||a.metaKey;break;case 37:(a.ctrlKey||a.metaKey)&&$.datepicker._adjustDate(a.target,d?1:-1,"D"),c=a.ctrlKey||a.metaKey,a.originalEvent.altKey&&$.datepicker._adjustDate(a.target,a.ctrlKey?-$.datepicker._get(b,"stepBigMonths"):-$.datepicker._get(b,"stepMonths"),"M");break;case 38:(a.ctrlKey||a.metaKey)&&$.datepicker._adjustDate(a.target,-7,"D"),c=a.ctrlKey||a.metaKey;break;case 39:(a.ctrlKey||a.metaKey)&&$.datepicker._adjustDate(a.target,d?-1:1,"D"),c=a.ctrlKey||a.metaKey,a.originalEvent.altKey&&$.datepicker._adjustDate(a.target,a.ctrlKey?+$.datepicker._get(b,"stepBigMonths"):+$.datepicker._get(b,"stepMonths"),"M");break;case 40:(a.ctrlKey||a.metaKey)&&$.datepicker._adjustDate(a.target,7,"D"),c=a.ctrlKey||a.metaKey;break;default:c=!1}else a.keyCode==36&&a.ctrlKey?$.datepicker._showDatepicker(this):c=!1;c&&(a.preventDefault(),a.stopPropagation())},_doKeyPress:function(a){var b=$.datepicker._getInst(a.target);if($.datepicker._get(b,"constrainInput")){var c=$.datepicker._possibleChars($.datepicker._get(b,"dateFormat")),d=String.fromCharCode(a.charCode==undefined?a.keyCode:a.charCode);return a.ctrlKey||a.metaKey||d<" "||!c||c.indexOf(d)>-1}},_doKeyUp:function(a){var b=$.datepicker._getInst(a.target);if(b.input.val()!=b.lastVal)try{var c=$.datepicker.parseDate($.datepicker._get(b,"dateFormat"),b.input?b.input.val():null,$.datepicker._getFormatConfig(b));c&&($.datepicker._setDateFromField(b),$.datepicker._updateAlternate(b),$.datepicker._updateDatepicker(b))}catch(d){$.datepicker.log(d)}return!0},_showDatepicker:function(a){a=a.target||a,a.nodeName.toLowerCase()!="input"&&(a=$("input",a.parentNode)[0]);if($.datepicker._isDisabledDatepicker(a)||$.datepicker._lastInput==a)return;var b=$.datepicker._getInst(a);$.datepicker._curInst&&$.datepicker._curInst!=b&&($.datepicker._curInst.dpDiv.stop(!0,!0),b&&$.datepicker._datepickerShowing&&$.datepicker._hideDatepicker($.datepicker._curInst.input[0]));var c=$.datepicker._get(b,"beforeShow"),d=c?c.apply(a,[a,b]):{};if(d===!1)return;extendRemove(b.settings,d),b.lastVal=null,$.datepicker._lastInput=a,$.datepicker._setDateFromField(b),$.datepicker._inDialog&&(a.value=""),$.datepicker._pos||($.datepicker._pos=$.datepicker._findPos(a),$.datepicker._pos[1]+=a.offsetHeight);var e=!1;$(a).parents().each(function(){return e|=$(this).css("position")=="fixed",!e}),e&&$.browser.opera&&($.datepicker._pos[0]-=document.documentElement.scrollLeft,$.datepicker._pos[1]-=document.documentElement.scrollTop);var f={left:$.datepicker._pos[0],top:$.datepicker._pos[1]};$.datepicker._pos=null,b.dpDiv.empty(),b.dpDiv.css({position:"absolute",display:"block",top:"-1000px"}),$.datepicker._updateDatepicker(b),f=$.datepicker._checkOffset(b,f,e),b.dpDiv.css({position:$.datepicker._inDialog&&$.blockUI?"static":e?"fixed":"absolute",display:"none",left:f.left+"px",top:f.top+"px"});if(!b.inline){var g=$.datepicker._get(b,"showAnim"),h=$.datepicker._get(b,"duration"),i=function(){var a=b.dpDiv.find("iframe.ui-datepicker-cover");if(!!a.length){var c=$.datepicker._getBorders(b.dpDiv);a.css({left:-c[0],top:-c[1],width:b.dpDiv.outerWidth(),height:b.dpDiv.outerHeight()})}};b.dpDiv.zIndex($(a).zIndex()+1),$.datepicker._datepickerShowing=!0,$.effects&&$.effects[g]?b.dpDiv.show(g,$.datepicker._get(b,"showOptions"),h,i):b.dpDiv[g||"show"](g?h:null,i),(!g||!h)&&i(),b.input.is(":visible")&&!b.input.is(":disabled")&&b.input.focus(),$.datepicker._curInst=b}},_updateDatepicker:function(a){var b=this;b.maxRows=4;var c=$.datepicker._getBorders(a.dpDiv);instActive=a,a.dpDiv.empty().append(this._generateHTML(a));var d=a.dpDiv.find("iframe.ui-datepicker-cover");!d.length||d.css({left:-c[0],top:-c[1],width:a.dpDiv.outerWidth(),height:a.dpDiv.outerHeight()}),a.dpDiv.find("."+this._dayOverClass+" a").mouseover();var e=this._getNumberOfMonths(a),f=e[1],g=17;a.dpDiv.removeClass("ui-datepicker-multi-2 ui-datepicker-multi-3 ui-datepicker-multi-4").width(""),f>1&&a.dpDiv.addClass("ui-datepicker-multi-"+f).css("width",g*f+"em"),a.dpDiv[(e[0]!=1||e[1]!=1?"add":"remove")+"Class"]("ui-datepicker-multi"),a.dpDiv[(this._get(a,"isRTL")?"add":"remove")+"Class"]("ui-datepicker-rtl"),a==$.datepicker._curInst&&$.datepicker._datepickerShowing&&a.input&&a.input.is(":visible")&&!a.input.is(":disabled")&&a.input[0]!=document.activeElement&&a.input.focus();if(a.yearshtml){var h=a.yearshtml;setTimeout(function(){h===a.yearshtml&&a.yearshtml&&a.dpDiv.find("select.ui-datepicker-year:first").replaceWith(a.yearshtml),h=a.yearshtml=null},0)}},_getBorders:function(a){var b=function(a){return{thin:1,medium:2,thick:3}[a]||a};return[parseFloat(b(a.css("border-left-width"))),parseFloat(b(a.css("border-top-width")))]},_checkOffset:function(a,b,c){var d=a.dpDiv.outerWidth(),e=a.dpDiv.outerHeight(),f=a.input?a.input.outerWidth():0,g=a.input?a.input.outerHeight():0,h=document.documentElement.clientWidth+$(document).scrollLeft(),i=document.documentElement.clientHeight+$(document).scrollTop();return b.left-=this._get(a,"isRTL")?d-f:0,b.left-=c&&b.left==a.input.offset().left?$(document).scrollLeft():0,b.top-=c&&b.top==a.input.offset().top+g?$(document).scrollTop():0,b.left-=Math.min(b.left,b.left+d>h&&h>d?Math.abs(b.left+d-h):0),b.top-=Math.min(b.top,b.top+e>i&&i>e?Math.abs(e+g):0),b},_findPos:function(a){var b=this._getInst(a),c=this._get(b,"isRTL");while(a&&(a.type=="hidden"||a.nodeType!=1||$.expr.filters.hidden(a)))a=a[c?"previousSibling":"nextSibling"];var d=$(a).offset();return[d.left,d.top]},_hideDatepicker:function(a){var b=this._curInst;if(!b||a&&b!=$.data(a,PROP_NAME))return;if(this._datepickerShowing){var c=this._get(b,"showAnim"),d=this._get(b,"duration"),e=function(){$.datepicker._tidyDialog(b)};$.effects&&$.effects[c]?b.dpDiv.hide(c,$.datepicker._get(b,"showOptions"),d,e):b.dpDiv[c=="slideDown"?"slideUp":c=="fadeIn"?"fadeOut":"hide"](c?d:null,e),c||e(),this._datepickerShowing=!1;var f=this._get(b,"onClose");f&&f.apply(b.input?b.input[0]:null,[b.input?b.input.val():"",b]),this._lastInput=null,this._inDialog&&(this._dialogInput.css({position:"absolute",left:"0",top:"-100px"}),$.blockUI&&($.unblockUI(),$("body").append(this.dpDiv))),this._inDialog=!1}},_tidyDialog:function(a){a.dpDiv.removeClass(this._dialogClass).unbind(".ui-datepicker-calendar")},_checkExternalClick:function(a){if(!$.datepicker._curInst)return;var b=$(a.target),c=$.datepicker._getInst(b[0]);(b[0].id!=$.datepicker._mainDivId&&b.parents("#"+$.datepicker._mainDivId).length==0&&!b.hasClass($.datepicker.markerClassName)&&!b.closest("."+$.datepicker._triggerClass).length&&$.datepicker._datepickerShowing&&(!$.datepicker._inDialog||!$.blockUI)||b.hasClass($.datepicker.markerClassName)&&$.datepicker._curInst!=c)&&$.datepicker._hideDatepicker()},_adjustDate:function(a,b,c){var d=$(a),e=this._getInst(d[0]);if(this._isDisabledDatepicker(d[0]))return;this._adjustInstDate(e,b+(c=="M"?this._get(e,"showCurrentAtPos"):0),c),this._updateDatepicker(e)},_gotoToday:function(a){var b=$(a),c=this._getInst(b[0]);if(this._get(c,"gotoCurrent")&&c.currentDay)c.selectedDay=c.currentDay,c.drawMonth=c.selectedMonth=c.currentMonth,c.drawYear=c.selectedYear=c.currentYear;else{var d=new Date;c.selectedDay=d.getDate(),c.drawMonth=c.selectedMonth=d.getMonth(),c.drawYear=c.selectedYear=d.getFullYear()}this._notifyChange(c),this._adjustDate(b)},_selectMonthYear:function(a,b,c){var d=$(a),e=this._getInst(d[0]);e["selected"+(c=="M"?"Month":"Year")]=e["draw"+(c=="M"?"Month":"Year")]=parseInt(b.options[b.selectedIndex].value,10),this._notifyChange(e),this._adjustDate(d)},_selectDay:function(a,b,c,d){var e=$(a);if($(d).hasClass(this._unselectableClass)||this._isDisabledDatepicker(e[0]))return;var f=this._getInst(e[0]);f.selectedDay=f.currentDay=$("a",d).html(),f.selectedMonth=f.currentMonth=b,f.selectedYear=f.currentYear=c,this._selectDate(a,this._formatDate(f,f.currentDay,f.currentMonth,f.currentYear))},_clearDate:function(a){var b=$(a),c=this._getInst(b[0]);this._selectDate(b,"")},_selectDate:function(a,b){var c=$(a),d=this._getInst(c[0]);b=b!=null?b:this._formatDate(d),d.input&&d.input.val(b),this._updateAlternate(d);var e=this._get(d,"onSelect");e?e.apply(d.input?d.input[0]:null,[b,d]):d.input&&d.input.trigger("change"),d.inline?this._updateDatepicker(d):(this._hideDatepicker(),this._lastInput=d.input[0],typeof d.input[0]!="object"&&d.input.focus(),this._lastInput=null)},_updateAlternate:function(a){var b=this._get(a,"altField");if(b){var c=this._get(a,"altFormat")||this._get(a,"dateFormat"),d=this._getDate(a),e=this.formatDate(c,d,this._getFormatConfig(a));$(b).each(function(){$(this).val(e)})}},noWeekends:function(a){var b=a.getDay();return[b>0&&b<6,""]},iso8601Week:function(a){var b=new Date(a.getTime());b.setDate(b.getDate()+4-(b.getDay()||7));var c=b.getTime();return b.setMonth(0),b.setDate(1),Math.floor(Math.round((c-b)/864e5)/7)+1},parseDate:function(a,b,c){if(a==null||b==null)throw"Invalid arguments";b=typeof b=="object"?b.toString():b+"";if(b=="")return null;var d=(c?c.shortYearCutoff:null)||this._defaults.shortYearCutoff;d=typeof d!="string"?d:(new Date).getFullYear()%100+parseInt(d,10);var e=(c?c.dayNamesShort:null)||this._defaults.dayNamesShort,f=(c?c.dayNames:null)||this._defaults.dayNames,g=(c?c.monthNamesShort:null)||this._defaults.monthNamesShort,h=(c?c.monthNames:null)||this._defaults.monthNames,i=-1,j=-1,k=-1,l=-1,m=!1,n=function(b){var c=s+1<a.length&&a.charAt(s+1)==b;return c&&s++,c},o=function(a){var c=n(a),d=a=="@"?14:a=="!"?20:a=="y"&&c?4:a=="o"?3:2,e=new RegExp("^\\d{1,"+d+"}"),f=b.substring(r).match(e);if(!f)throw"Missing number at position "+r;return r+=f[0].length,parseInt(f[0],10)},p=function(a,c,d){var e=$.map(n(a)?d:c,function(a,b){return[[b,a]]}).sort(function(a,b){return-(a[1].length-b[1].length)}),f=-1;$.each(e,function(a,c){var d=c[1];if(b.substr(r,d.length).toLowerCase()==d.toLowerCase())return f=c[0],r+=d.length,!1});if(f!=-1)return f+1;throw"Unknown name at position "+r},q=function(){if(b.charAt(r)!=a.charAt(s))throw"Unexpected literal at position "+r;r++},r=0;for(var s=0;s<a.length;s++)if(m)a.charAt(s)=="'"&&!n("'")?m=!1:q();else switch(a.charAt(s)){case"d":k=o("d");break;case"D":p("D",e,f);break;case"o":l=o("o");break;case"m":j=o("m");break;case"M":j=p("M",g,h);break;case"y":i=o("y");break;case"@":var t=new Date(o("@"));i=t.getFullYear(),j=t.getMonth()+1,k=t.getDate();break;case"!":var t=new Date((o("!")-this._ticksTo1970)/1e4);i=t.getFullYear(),j=t.getMonth()+1,k=t.getDate();break;case"'":n("'")?q():m=!0;break;default:q()}if(r<b.length)throw"Extra/unparsed characters found in date: "+b.substring(r);i==-1?i=(new Date).getFullYear():i<100&&(i+=(new Date).getFullYear()-(new Date).getFullYear()%100+(i<=d?0:-100));if(l>-1){j=1,k=l;do{var u=this._getDaysInMonth(i,j-1);if(k<=u)break;j++,k-=u}while(!0)}var t=this._daylightSavingAdjust(new Date(i,j-1,k));if(t.getFullYear()!=i||t.getMonth()+1!=j||t.getDate()!=k)throw"Invalid date";return t},ATOM:"yy-mm-dd",COOKIE:"D, dd M yy",ISO_8601:"yy-mm-dd",RFC_822:"D, d M y",RFC_850:"DD, dd-M-y",RFC_1036:"D, d M y",RFC_1123:"D, d M yy",RFC_2822:"D, d M yy",RSS:"D, d M y",TICKS:"!",TIMESTAMP:"@",W3C:"yy-mm-dd",_ticksTo1970:(718685+Math.floor(492.5)-Math.floor(19.7)+Math.floor(4.925))*24*60*60*1e7,formatDate:function(a,b,c){if(!b)return"";var d=(c?c.dayNamesShort:null)||this._defaults.dayNamesShort,e=(c?c.dayNames:null)||this._defaults.dayNames,f=(c?c.monthNamesShort:null)||this._defaults.monthNamesShort,g=(c?c.monthNames:null)||this._defaults.monthNames,h=function(b){var c=m+1<a.length&&a.charAt(m+1)==b;return c&&m++,c},i=function(a,b,c){var d=""+b;if(h(a))while(d.length<c)d="0"+d;return d},j=function(a,b,c,d){return h(a)?d[b]:c[b]},k="",l=!1;if(b)for(var m=0;m<a.length;m++)if(l)a.charAt(m)=="'"&&!h("'")?l=!1:k+=a.charAt(m);else switch(a.charAt(m)){case"d":k+=i("d",b.getDate(),2);break;case"D":k+=j("D",b.getDay(),d,e);break;case"o":k+=i("o",Math.round(((new Date(b.getFullYear(),b.getMonth(),b.getDate())).getTime()-(new Date(b.getFullYear(),0,0)).getTime())/864e5),3);break;case"m":k+=i("m",b.getMonth()+1,2);break;case"M":k+=j("M",b.getMonth(),f,g);break;case"y":k+=h("y")?b.getFullYear():(b.getYear()%100<10?"0":"")+b.getYear()%100;break;case"@":k+=b.getTime();break;case"!":k+=b.getTime()*1e4+this._ticksTo1970;break;case"'":h("'")?k+="'":l=!0;break;default:k+=a.charAt(m)}return k},_possibleChars:function(a){var b="",c=!1,d=function(b){var c=e+1<a.length&&a.charAt(e+1)==b;return c&&e++,c};for(var e=0;e<a.length;e++)if(c)a.charAt(e)=="'"&&!d("'")?c=!1:b+=a.charAt(e);else switch(a.charAt(e)){case"d":case"m":case"y":case"@":b+="0123456789";break;case"D":case"M":return null;case"'":d("'")?b+="'":c=!0;break;default:b+=a.charAt(e)}return b},_get:function(a,b){return a.settings[b]!==undefined?a.settings[b]:this._defaults[b]},_setDateFromField:function(a,b){if(a.input.val()==a.lastVal)return;var c=this._get(a,"dateFormat"),d=a.lastVal=a.input?a.input.val():null,e,f;e=f=this._getDefaultDate(a);var g=this._getFormatConfig(a);try{e=this.parseDate(c,d,g)||f}catch(h){this.log(h),d=b?"":d}a.selectedDay=e.getDate(),a.drawMonth=a.selectedMonth=e.getMonth(),a.drawYear=a.selectedYear=e.getFullYear(),a.currentDay=d?e.getDate():0,a.currentMonth=d?e.getMonth():0,a.currentYear=d?e.getFullYear():0,this._adjustInstDate(a)},_getDefaultDate:function(a){return this._restrictMinMax(a,this._determineDate(a,this._get(a,"defaultDate"),new Date))},_determineDate:function(a,b,c){var d=function(a){var b=new Date;return b.setDate(b.getDate()+a),b},e=function(b){try{return $.datepicker.parseDate($.datepicker._get(a,"dateFormat"),b,$.datepicker._getFormatConfig(a))}catch(c){}var d=(b.toLowerCase().match(/^c/)?$.datepicker._getDate(a):null)||new Date,e=d.getFullYear(),f=d.getMonth(),g=d.getDate(),h=/([+-]?[0-9]+)\s*(d|D|w|W|m|M|y|Y)?/g,i=h.exec(b);while(i){switch(i[2]||"d"){case"d":case"D":g+=parseInt(i[1],10);break;case"w":case"W":g+=parseInt(i[1],10)*7;break;case"m":case"M":f+=parseInt(i[1],10),g=Math.min(g,$.datepicker._getDaysInMonth(e,f));break;case"y":case"Y":e+=parseInt(i[1],10),g=Math.min(g,$.datepicker._getDaysInMonth(e,f))}i=h.exec(b)}return new Date(e,f,g)},f=b==null||b===""?c:typeof b=="string"?e(b):typeof b=="number"?isNaN(b)?c:d(b):new Date(b.getTime());return f=f&&f.toString()=="Invalid Date"?c:f,f&&(f.setHours(0),f.setMinutes(0),f.setSeconds(0),f.setMilliseconds(0)),this._daylightSavingAdjust(f)},_daylightSavingAdjust:function(a){return a?(a.setHours(a.getHours()>12?a.getHours()+2:0),a):null},_setDate:function(a,b,c){var d=!b,e=a.selectedMonth,f=a.selectedYear,g=this._restrictMinMax(a,this._determineDate(a,b,new Date));a.selectedDay=a.currentDay=g.getDate(),a.drawMonth=a.selectedMonth=a.currentMonth=g.getMonth(),a.drawYear=a.selectedYear=a.currentYear=g.getFullYear(),(e!=a.selectedMonth||f!=a.selectedYear)&&!c&&this._notifyChange(a),this._adjustInstDate(a),a.input&&a.input.val(d?"":this._formatDate(a))},_getDate:function(a){var b=!a.currentYear||a.input&&a.input.val()==""?null:this._daylightSavingAdjust(new Date(a.currentYear,a.currentMonth,a.currentDay));return b},_generateHTML:function(a){var b=new Date;b=this._daylightSavingAdjust(new Date(b.getFullYear(),b.getMonth(),b.getDate()));var c=this._get(a,"isRTL"),d=this._get(a,"showButtonPanel"),e=this._get(a,"hideIfNoPrevNext"),f=this._get(a,"navigationAsDateFormat"),g=this._getNumberOfMonths(a),h=this._get(a,"showCurrentAtPos"),i=this._get(a,"stepMonths"),j=g[0]!=1||g[1]!=1,k=this._daylightSavingAdjust(a.currentDay?new Date(a.currentYear,a.currentMonth,a.currentDay):new Date(9999,9,9)),l=this._getMinMaxDate(a,"min"),m=this._getMinMaxDate(a,"max"),n=a.drawMonth-h,o=a.drawYear;n<0&&(n+=12,o--);if(m){var p=this._daylightSavingAdjust(new Date(m.getFullYear(),m.getMonth()-g[0]*g[1]+1,m.getDate()));p=l&&p<l?l:p;while(this._daylightSavingAdjust(new Date(o,n,1))>p)n--,n<0&&(n=11,o--)}a.drawMonth=n,a.drawYear=o;var q=this._get(a,"prevText");q=f?this.formatDate(q,this._daylightSavingAdjust(new Date(o,n-i,1)),this._getFormatConfig(a)):q;var r=this._canAdjustMonth(a,-1,o,n)?'<a class="ui-datepicker-prev ui-corner-all" onclick="DP_jQuery_'+dpuuid+".datepicker._adjustDate('#"+a.id+"', -"+i+", 'M');\""+' title="'+q+'"><span class="ui-icon ui-icon-circle-triangle-'+(c?"e":"w")+'">'+q+"</span></a>":e?"":'<a class="ui-datepicker-prev ui-corner-all ui-state-disabled" title="'+q+'"><span class="ui-icon ui-icon-circle-triangle-'+(c?"e":"w")+'">'+q+"</span></a>",s=this._get(a,"nextText");s=f?this.formatDate(s,this._daylightSavingAdjust(new Date(o,n+i,1)),this._getFormatConfig(a)):s;var t=this._canAdjustMonth(a,1,o,n)?'<a class="ui-datepicker-next ui-corner-all" onclick="DP_jQuery_'+dpuuid+".datepicker._adjustDate('#"+a.id+"', +"+i+", 'M');\""+' title="'+s+'"><span class="ui-icon ui-icon-circle-triangle-'+(c?"w":"e")+'">'+s+"</span></a>":e?"":'<a class="ui-datepicker-next ui-corner-all ui-state-disabled" title="'+s+'"><span class="ui-icon ui-icon-circle-triangle-'+(c?"w":"e")+'">'+s+"</span></a>",u=this._get(a,"currentText"),v=this._get(a,"gotoCurrent")&&a.currentDay?k:b;u=f?this.formatDate(u,v,this._getFormatConfig(a)):u;var w=a.inline?"":'<button type="button" class="ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all" onclick="DP_jQuery_'+dpuuid+'.datepicker._hideDatepicker();">'+this._get(a,"closeText")+"</button>",x=d?'<div class="ui-datepicker-buttonpane ui-widget-content">'+(c?w:"")+(this._isInRange(a,v)?'<button type="button" class="ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all" onclick="DP_jQuery_'+dpuuid+".datepicker._gotoToday('#"+a.id+"');\""+">"+u+"</button>":"")+(c?"":w)+"</div>":"",y=parseInt(this._get(a,"firstDay"),10);y=isNaN(y)?0:y;var z=this._get(a,"showWeek"),A=this._get(a,"dayNames"),B=this._get(a,"dayNamesShort"),C=this._get(a,"dayNamesMin"),D=this._get(a,"monthNames"),E=this._get(a,"monthNamesShort"),F=this._get(a,"beforeShowDay"),G=this._get(a,"showOtherMonths"),H=this._get(a,"selectOtherMonths"),I=this._get(a,"calculateWeek")||this.iso8601Week,J=this._getDefaultDate(a),K="";for(var L=0;L<g[0];L++){var M="";this.maxRows=4;for(var N=0;N<g[1];N++){var O=this._daylightSavingAdjust(new Date(o,n,a.selectedDay)),P=" ui-corner-all",Q="";if(j){Q+='<div class="ui-datepicker-group';if(g[1]>1)switch(N){case 0:Q+=" ui-datepicker-group-first",P=" ui-corner-"+(c?"right":"left");break;case g[1]-1:Q+=" ui-datepicker-group-last",P=" ui-corner-"+(c?"left":"right");break;default:Q+=" ui-datepicker-group-middle",P=""}Q+='">'}Q+='<div class="ui-datepicker-header ui-widget-header ui-helper-clearfix'+P+'">'+(/all|left/.test(P)&&L==0?c?t:r:"")+(/all|right/.test(P)&&L==0?c?r:t:"")+this._generateMonthYearHeader(a,n,o,l,m,L>0||N>0,D,E)+'</div><table class="ui-datepicker-calendar"><thead>'+"<tr>";var R=z?'<th class="ui-datepicker-week-col">'+this._get(a,"weekHeader")+"</th>":"";for(var S=0;S<7;S++){var T=(S+y)%7;R+="<th"+((S+y+6)%7>=5?' class="ui-datepicker-week-end"':"")+">"+'<span title="'+A[T]+'">'+C[T]+"</span></th>"}Q+=R+"</tr></thead><tbody>";var U=this._getDaysInMonth(o,n);o==a.selectedYear&&n==a.selectedMonth&&(a.selectedDay=Math.min(a.selectedDay,U));var V=(this._getFirstDayOfMonth(o,n)-y+7)%7,W=Math.ceil((V+U)/7),X=j?this.maxRows>W?this.maxRows:W:W;this.maxRows=X;var Y=this._daylightSavingAdjust(new Date(o,n,1-V));for(var Z=0;Z<X;Z++){Q+="<tr>";var _=z?'<td class="ui-datepicker-week-col">'+this._get(a,"calculateWeek")(Y)+"</td>":"";for(var S=0;S<7;S++){var ba=F?F.apply(a.input?a.input[0]:null,[Y]):[!0,""],bb=Y.getMonth()!=n,bc=bb&&!H||!ba[0]||l&&Y<l||m&&Y>m;_+='<td class="'+((S+y+6)%7>=5?" ui-datepicker-week-end":"")+(bb?" ui-datepicker-other-month":"")+(Y.getTime()==O.getTime()&&n==a.selectedMonth&&a._keyEvent||J.getTime()==Y.getTime()&&J.getTime()==O.getTime()?" "+this._dayOverClass:"")+(bc?" "+this._unselectableClass+" ui-state-disabled":"")+(bb&&!G?"":" "+ba[1]+(Y.getTime()==k.getTime()?" "+this._currentClass:"")+(Y.getTime()==b.getTime()?" ui-datepicker-today":""))+'"'+((!bb||G)&&ba[2]?' title="'+ba[2]+'"':"")+(bc?"":' onclick="DP_jQuery_'+dpuuid+".datepicker._selectDay('#"+a.id+"',"+Y.getMonth()+","+Y.getFullYear()+', this);return false;"')+">"+(bb&&!G?"&#xa0;":bc?'<span class="ui-state-default">'+Y.getDate()+"</span>":'<a class="ui-state-default'+(Y.getTime()==b.getTime()?" ui-state-highlight":"")+(Y.getTime()==k.getTime()?" ui-state-active":"")+(bb?" ui-priority-secondary":"")+'" href="#">'+Y.getDate()+"</a>")+"</td>",Y.setDate(Y.getDate()+1),Y=this._daylightSavingAdjust(Y)}Q+=_+"</tr>"}n++,n>11&&(n=0,o++),Q+="</tbody></table>"+(j?"</div>"+(g[0]>0&&N==g[1]-1?'<div class="ui-datepicker-row-break"></div>':""):""),M+=Q}K+=M}return K+=x+($.browser.msie&&parseInt($.browser.version,10)<7&&!a.inline?'<iframe src="javascript:false;" class="ui-datepicker-cover" frameborder="0"></iframe>':""),a._keyEvent=!1,K},_generateMonthYearHeader:function(a,b,c,d,e,f,g,h){var i=this._get(a,"changeMonth"),j=this._get(a,"changeYear"),k=this._get(a,"showMonthAfterYear"),l='<div class="ui-datepicker-title">',m="";if(f||!i)m+='<span class="ui-datepicker-month">'+g[b]+"</span>";else{var n=d&&d.getFullYear()==c,o=e&&e.getFullYear()==c;m+='<select class="ui-datepicker-month" onchange="DP_jQuery_'+dpuuid+".datepicker._selectMonthYear('#"+a.id+"', this, 'M');\" "+">";for(var p=0;p<12;p++)(!n||p>=d.getMonth())&&(!o||p<=e.getMonth())&&(m+='<option value="'+p+'"'+(p==b?' selected="selected"':"")+">"+h[p]+"</option>");m+="</select>"}k||(l+=m+(f||!i||!j?"&#xa0;":""));if(!a.yearshtml){a.yearshtml="";if(f||!j)l+='<span class="ui-datepicker-year">'+c+"</span>";else{var q=this._get(a,"yearRange").split(":"),r=(new Date).getFullYear(),s=function(a){var b=a.match(/c[+-].*/)?c+parseInt(a.substring(1),10):a.match(/[+-].*/)?r+parseInt(a,10):parseInt(a,10);return isNaN(b)?r:b},t=s(q[0]),u=Math.max(t,s(q[1]||""));t=d?Math.max(t,d.getFullYear()):t,u=e?Math.min(u,e.getFullYear()):u,a.yearshtml+='<select class="ui-datepicker-year" onchange="DP_jQuery_'+dpuuid+".datepicker._selectMonthYear('#"+a.id+"', this, 'Y');\" "+">";for(;t<=u;t++)a.yearshtml+='<option value="'+t+'"'+(t==c?' selected="selected"':"")+">"+t+"</option>";a.yearshtml+="</select>",l+=a.yearshtml,a.yearshtml=null}}return l+=this._get(a,"yearSuffix"),k&&(l+=(f||!i||!j?"&#xa0;":"")+m),l+="</div>",l},_adjustInstDate:function(a,b,c){var d=a.drawYear+(c=="Y"?b:0),e=a.drawMonth+(c=="M"?b:0),f=Math.min(a.selectedDay,this._getDaysInMonth(d,e))+(c=="D"?b:0),g=this._restrictMinMax(a,this._daylightSavingAdjust(new Date(d,e,f)));a.selectedDay=g.getDate(),a.drawMonth=a.selectedMonth=g.getMonth(),a.drawYear=a.selectedYear=g.getFullYear(),(c=="M"||c=="Y")&&this._notifyChange(a)},_restrictMinMax:function(a,b){var c=this._getMinMaxDate(a,"min"),d=this._getMinMaxDate(a,"max"),e=c&&b<c?c:b;return e=d&&e>d?d:e,e},_notifyChange:function(a){var b=this._get(a,"onChangeMonthYear");b&&b.apply(a.input?a.input[0]:null,[a.selectedYear,a.selectedMonth+1,a])},_getNumberOfMonths:function(a){var b=this._get(a,"numberOfMonths");return b==null?[1,1]:typeof b=="number"?[1,b]:b},_getMinMaxDate:function(a,b){return this._determineDate(a,this._get(a,b+"Date"),null)},_getDaysInMonth:function(a,b){return 32-this._daylightSavingAdjust(new Date(a,b,32)).getDate()},_getFirstDayOfMonth:function(a,b){return(new Date(a,b,1)).getDay()},_canAdjustMonth:function(a,b,c,d){var e=this._getNumberOfMonths(a),f=this._daylightSavingAdjust(new Date(c,d+(b<0?b:e[0]*e[1]),1));return b<0&&f.setDate(this._getDaysInMonth(f.getFullYear(),f.getMonth())),this._isInRange(a,f)},_isInRange:function(a,b){var c=this._getMinMaxDate(a,"min"),d=this._getMinMaxDate(a,"max");return(!c||b.getTime()>=c.getTime())&&(!d||b.getTime()<=d.getTime())},_getFormatConfig:function(a){var b=this._get(a,"shortYearCutoff");return b=typeof b!="string"?b:(new Date).getFullYear()%100+parseInt(b,10),{shortYearCutoff:b,dayNamesShort:this._get(a,"dayNamesShort"),dayNames:this._get(a,"dayNames"),monthNamesShort:this._get(a,"monthNamesShort"),monthNames:this._get(a,"monthNames")}},_formatDate:function(a,b,c,d){b||(a.currentDay=a.selectedDay,a.currentMonth=a.selectedMonth,a.currentYear=a.selectedYear);var e=b?typeof b=="object"?b:this._daylightSavingAdjust(new Date(d,c,b)):this._daylightSavingAdjust(new Date(a.currentYear,a.currentMonth,a.currentDay));return this.formatDate(this._get(a,"dateFormat"),e,this._getFormatConfig(a))}}),$.fn.datepicker=function(a){if(!this.length)return this;$.datepicker.initialized||($(document).mousedown($.datepicker._checkExternalClick).find("body").append($.datepicker.dpDiv),$.datepicker.initialized=!0);var b=Array.prototype.slice.call(arguments,1);return typeof a!="string"||a!="isDisabled"&&a!="getDate"&&a!="widget"?a=="option"&&arguments.length==2&&typeof arguments[1]=="string"?$.datepicker["_"+a+"Datepicker"].apply($.datepicker,[this[0]].concat(b)):this.each(function(){typeof a=="string"?$.datepicker["_"+a+"Datepicker"].apply($.datepicker,[this].concat(b)):$.datepicker._attachDatepicker(this,a)}):$.datepicker["_"+a+"Datepicker"].apply($.datepicker,[this[0]].concat(b))},$.datepicker=new Datepicker,$.datepicker.initialized=!1,$.datepicker.uuid=(new Date).getTime(),$.datepicker.version="1.8.21",window["DP_jQuery_"+dpuuid]=$})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.ui.progressbar.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.widget("ui.progressbar",{options:{value:0,max:100},min:0,_create:function(){this.element.addClass("ui-progressbar ui-widget ui-widget-content ui-corner-all").attr({role:"progressbar","aria-valuemin":this.min,"aria-valuemax":this.options.max,"aria-valuenow":this._value()}),this.valueDiv=a("<div class='ui-progressbar-value ui-widget-header ui-corner-left'></div>").appendTo(this.element),this.oldValue=this._value(),this._refreshValue()},destroy:function(){this.element.removeClass("ui-progressbar ui-widget ui-widget-content ui-corner-all").removeAttr("role").removeAttr("aria-valuemin").removeAttr("aria-valuemax").removeAttr("aria-valuenow"),this.valueDiv.remove(),a.Widget.prototype.destroy.apply(this,arguments)},value:function(a){return a===b?this._value():(this._setOption("value",a),this)},_setOption:function(b,c){b==="value"&&(this.options.value=c,this._refreshValue(),this._value()===this.options.max&&this._trigger("complete")),a.Widget.prototype._setOption.apply(this,arguments)},_value:function(){var a=this.options.value;return typeof a!="number"&&(a=0),Math.min(this.options.max,Math.max(this.min,a))},_percentage:function(){return 100*this._value()/this.options.max},_refreshValue:function(){var a=this.value(),b=this._percentage();this.oldValue!==a&&(this.oldValue=a,this._trigger("change")),this.valueDiv.toggle(a>this.min).toggleClass("ui-corner-right",a===this.options.max).width(b.toFixed(0)+"%"),this.element.attr("aria-valuenow",a)}}),a.extend(a.ui.progressbar,{version:"1.8.21"})})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.core.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
jQuery.effects||function(a,b){function c(b){var c;return b&&b.constructor==Array&&b.length==3?b:(c=/rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(b))?[parseInt(c[1],10),parseInt(c[2],10),parseInt(c[3],10)]:(c=/rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(b))?[parseFloat(c[1])*2.55,parseFloat(c[2])*2.55,parseFloat(c[3])*2.55]:(c=/#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(b))?[parseInt(c[1],16),parseInt(c[2],16),parseInt(c[3],16)]:(c=/#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(b))?[parseInt(c[1]+c[1],16),parseInt(c[2]+c[2],16),parseInt(c[3]+c[3],16)]:(c=/rgba\(0, 0, 0, 0\)/.exec(b))?e.transparent:e[a.trim(b).toLowerCase()]}function d(b,d){var e;do{e=a.curCSS(b,d);if(e!=""&&e!="transparent"||a.nodeName(b,"body"))break;d="backgroundColor"}while(b=b.parentNode);return c(e)}function h(){var a=document.defaultView?document.defaultView.getComputedStyle(this,null):this.currentStyle,b={},c,d;if(a&&a.length&&a[0]&&a[a[0]]){var e=a.length;while(e--)c=a[e],typeof a[c]=="string"&&(d=c.replace(/\-(\w)/g,function(a,b){return b.toUpperCase()}),b[d]=a[c])}else for(c in a)typeof a[c]=="string"&&(b[c]=a[c]);return b}function i(b){var c,d;for(c in b)d=b[c],(d==null||a.isFunction(d)||c in g||/scrollbar/.test(c)||!/color/i.test(c)&&isNaN(parseFloat(d)))&&delete b[c];return b}function j(a,b){var c={_:0},d;for(d in b)a[d]!=b[d]&&(c[d]=b[d]);return c}function k(b,c,d,e){typeof b=="object"&&(e=c,d=null,c=b,b=c.effect),a.isFunction(c)&&(e=c,d=null,c={});if(typeof c=="number"||a.fx.speeds[c])e=d,d=c,c={};return a.isFunction(d)&&(e=d,d=null),c=c||{},d=d||c.duration,d=a.fx.off?0:typeof d=="number"?d:d in a.fx.speeds?a.fx.speeds[d]:a.fx.speeds._default,e=e||c.complete,[b,c,d,e]}function l(b){return!b||typeof b=="number"||a.fx.speeds[b]?!0:typeof b=="string"&&!a.effects[b]?!0:!1}a.effects={},a.each(["backgroundColor","borderBottomColor","borderLeftColor","borderRightColor","borderTopColor","borderColor","color","outlineColor"],function(b,e){a.fx.step[e]=function(a){a.colorInit||(a.start=d(a.elem,e),a.end=c(a.end),a.colorInit=!0),a.elem.style[e]="rgb("+Math.max(Math.min(parseInt(a.pos*(a.end[0]-a.start[0])+a.start[0],10),255),0)+","+Math.max(Math.min(parseInt(a.pos*(a.end[1]-a.start[1])+a.start[1],10),255),0)+","+Math.max(Math.min(parseInt(a.pos*(a.end[2]-a.start[2])+a.start[2],10),255),0)+")"}});var e={aqua:[0,255,255],azure:[240,255,255],beige:[245,245,220],black:[0,0,0],blue:[0,0,255],brown:[165,42,42],cyan:[0,255,255],darkblue:[0,0,139],darkcyan:[0,139,139],darkgrey:[169,169,169],darkgreen:[0,100,0],darkkhaki:[189,183,107],darkmagenta:[139,0,139],darkolivegreen:[85,107,47],darkorange:[255,140,0],darkorchid:[153,50,204],darkred:[139,0,0],darksalmon:[233,150,122],darkviolet:[148,0,211],fuchsia:[255,0,255],gold:[255,215,0],green:[0,128,0],indigo:[75,0,130],khaki:[240,230,140],lightblue:[173,216,230],lightcyan:[224,255,255],lightgreen:[144,238,144],lightgrey:[211,211,211],lightpink:[255,182,193],lightyellow:[255,255,224],lime:[0,255,0],magenta:[255,0,255],maroon:[128,0,0],navy:[0,0,128],olive:[128,128,0],orange:[255,165,0],pink:[255,192,203],purple:[128,0,128],violet:[128,0,128],red:[255,0,0],silver:[192,192,192],white:[255,255,255],yellow:[255,255,0],transparent:[255,255,255]},f=["add","remove","toggle"],g={border:1,borderBottom:1,borderColor:1,borderLeft:1,borderRight:1,borderTop:1,borderWidth:1,margin:1,padding:1};a.effects.animateClass=function(b,c,d,e){return a.isFunction(d)&&(e=d,d=null),this.queue(function(){var g=a(this),k=g.attr("style")||" ",l=i(h.call(this)),m,n=g.attr("class")||"";a.each(f,function(a,c){b[c]&&g[c+"Class"](b[c])}),m=i(h.call(this)),g.attr("class",n),g.animate(j(l,m),{queue:!1,duration:c,easing:d,complete:function(){a.each(f,function(a,c){b[c]&&g[c+"Class"](b[c])}),typeof g.attr("style")=="object"?(g.attr("style").cssText="",g.attr("style").cssText=k):g.attr("style",k),e&&e.apply(this,arguments),a.dequeue(this)}})})},a.fn.extend({_addClass:a.fn.addClass,addClass:function(b,c,d,e){return c?a.effects.animateClass.apply(this,[{add:b},c,d,e]):this._addClass(b)},_removeClass:a.fn.removeClass,removeClass:function(b,c,d,e){return c?a.effects.animateClass.apply(this,[{remove:b},c,d,e]):this._removeClass(b)},_toggleClass:a.fn.toggleClass,toggleClass:function(c,d,e,f,g){return typeof d=="boolean"||d===b?e?a.effects.animateClass.apply(this,[d?{add:c}:{remove:c},e,f,g]):this._toggleClass(c,d):a.effects.animateClass.apply(this,[{toggle:c},d,e,f])},switchClass:function(b,c,d,e,f){return a.effects.animateClass.apply(this,[{add:c,remove:b},d,e,f])}}),a.extend(a.effects,{version:"1.8.21",save:function(a,b){for(var c=0;c<b.length;c++)b[c]!==null&&a.data("ec.storage."+b[c],a[0].style[b[c]])},restore:function(a,b){for(var c=0;c<b.length;c++)b[c]!==null&&a.css(b[c],a.data("ec.storage."+b[c]))},setMode:function(a,b){return b=="toggle"&&(b=a.is(":hidden")?"show":"hide"),b},getBaseline:function(a,b){var c,d;switch(a[0]){case"top":c=0;break;case"middle":c=.5;break;case"bottom":c=1;break;default:c=a[0]/b.height}switch(a[1]){case"left":d=0;break;case"center":d=.5;break;case"right":d=1;break;default:d=a[1]/b.width}return{x:d,y:c}},createWrapper:function(b){if(b.parent().is(".ui-effects-wrapper"))return b.parent();var c={width:b.outerWidth(!0),height:b.outerHeight(!0),"float":b.css("float")},d=a("<div></div>").addClass("ui-effects-wrapper").css({fontSize:"100%",background:"transparent",border:"none",margin:0,padding:0}),e=document.activeElement;try{e.id}catch(f){e=document.body}return b.wrap(d),(b[0]===e||a.contains(b[0],e))&&a(e).focus(),d=b.parent(),b.css("position")=="static"?(d.css({position:"relative"}),b.css({position:"relative"})):(a.extend(c,{position:b.css("position"),zIndex:b.css("z-index")}),a.each(["top","left","bottom","right"],function(a,d){c[d]=b.css(d),isNaN(parseInt(c[d],10))&&(c[d]="auto")}),b.css({position:"relative",top:0,left:0,right:"auto",bottom:"auto"})),d.css(c).show()},removeWrapper:function(b){var c,d=document.activeElement;return b.parent().is(".ui-effects-wrapper")?(c=b.parent().replaceWith(b),(b[0]===d||a.contains(b[0],d))&&a(d).focus(),c):b},setTransition:function(b,c,d,e){return e=e||{},a.each(c,function(a,c){var f=b.cssUnit(c);f[0]>0&&(e[c]=f[0]*d+f[1])}),e}}),a.fn.extend({effect:function(b,c,d,e){var f=k.apply(this,arguments),g={options:f[1],duration:f[2],callback:f[3]},h=g.options.mode,i=a.effects[b];return a.fx.off||!i?h?this[h](g.duration,g.callback):this.each(function(){g.callback&&g.callback.call(this)}):i.call(this,g)},_show:a.fn.show,show:function(a){if(l(a))return this._show.apply(this,arguments);var b=k.apply(this,arguments);return b[1].mode="show",this.effect.apply(this,b)},_hide:a.fn.hide,hide:function(a){if(l(a))return this._hide.apply(this,arguments);var b=k.apply(this,arguments);return b[1].mode="hide",this.effect.apply(this,b)},__toggle:a.fn.toggle,toggle:function(b){if(l(b)||typeof b=="boolean"||a.isFunction(b))return this.__toggle.apply(this,arguments);var c=k.apply(this,arguments);return c[1].mode="toggle",this.effect.apply(this,c)},cssUnit:function(b){var c=this.css(b),d=[];return a.each(["em","px","%","pt"],function(a,b){c.indexOf(b)>0&&(d=[parseFloat(c),b])}),d}}),a.easing.jswing=a.easing.swing,a.extend(a.easing,{def:"easeOutQuad",swing:function(b,c,d,e,f){return a.easing[a.easing.def](b,c,d,e,f)},easeInQuad:function(a,b,c,d,e){return d*(b/=e)*b+c},easeOutQuad:function(a,b,c,d,e){return-d*(b/=e)*(b-2)+c},easeInOutQuad:function(a,b,c,d,e){return(b/=e/2)<1?d/2*b*b+c:-d/2*(--b*(b-2)-1)+c},easeInCubic:function(a,b,c,d,e){return d*(b/=e)*b*b+c},easeOutCubic:function(a,b,c,d,e){return d*((b=b/e-1)*b*b+1)+c},easeInOutCubic:function(a,b,c,d,e){return(b/=e/2)<1?d/2*b*b*b+c:d/2*((b-=2)*b*b+2)+c},easeInQuart:function(a,b,c,d,e){return d*(b/=e)*b*b*b+c},easeOutQuart:function(a,b,c,d,e){return-d*((b=b/e-1)*b*b*b-1)+c},easeInOutQuart:function(a,b,c,d,e){return(b/=e/2)<1?d/2*b*b*b*b+c:-d/2*((b-=2)*b*b*b-2)+c},easeInQuint:function(a,b,c,d,e){return d*(b/=e)*b*b*b*b+c},easeOutQuint:function(a,b,c,d,e){return d*((b=b/e-1)*b*b*b*b+1)+c},easeInOutQuint:function(a,b,c,d,e){return(b/=e/2)<1?d/2*b*b*b*b*b+c:d/2*((b-=2)*b*b*b*b+2)+c},easeInSine:function(a,b,c,d,e){return-d*Math.cos(b/e*(Math.PI/2))+d+c},easeOutSine:function(a,b,c,d,e){return d*Math.sin(b/e*(Math.PI/2))+c},easeInOutSine:function(a,b,c,d,e){return-d/2*(Math.cos(Math.PI*b/e)-1)+c},easeInExpo:function(a,b,c,d,e){return b==0?c:d*Math.pow(2,10*(b/e-1))+c},easeOutExpo:function(a,b,c,d,e){return b==e?c+d:d*(-Math.pow(2,-10*b/e)+1)+c},easeInOutExpo:function(a,b,c,d,e){return b==0?c:b==e?c+d:(b/=e/2)<1?d/2*Math.pow(2,10*(b-1))+c:d/2*(-Math.pow(2,-10*--b)+2)+c},easeInCirc:function(a,b,c,d,e){return-d*(Math.sqrt(1-(b/=e)*b)-1)+c},easeOutCirc:function(a,b,c,d,e){return d*Math.sqrt(1-(b=b/e-1)*b)+c},easeInOutCirc:function(a,b,c,d,e){return(b/=e/2)<1?-d/2*(Math.sqrt(1-b*b)-1)+c:d/2*(Math.sqrt(1-(b-=2)*b)+1)+c},easeInElastic:function(a,b,c,d,e){var f=1.70158,g=0,h=d;if(b==0)return c;if((b/=e)==1)return c+d;g||(g=e*.3);if(h<Math.abs(d)){h=d;var f=g/4}else var f=g/(2*Math.PI)*Math.asin(d/h);return-(h*Math.pow(2,10*(b-=1))*Math.sin((b*e-f)*2*Math.PI/g))+c},easeOutElastic:function(a,b,c,d,e){var f=1.70158,g=0,h=d;if(b==0)return c;if((b/=e)==1)return c+d;g||(g=e*.3);if(h<Math.abs(d)){h=d;var f=g/4}else var f=g/(2*Math.PI)*Math.asin(d/h);return h*Math.pow(2,-10*b)*Math.sin((b*e-f)*2*Math.PI/g)+d+c},easeInOutElastic:function(a,b,c,d,e){var f=1.70158,g=0,h=d;if(b==0)return c;if((b/=e/2)==2)return c+d;g||(g=e*.3*1.5);if(h<Math.abs(d)){h=d;var f=g/4}else var f=g/(2*Math.PI)*Math.asin(d/h);return b<1?-0.5*h*Math.pow(2,10*(b-=1))*Math.sin((b*e-f)*2*Math.PI/g)+c:h*Math.pow(2,-10*(b-=1))*Math.sin((b*e-f)*2*Math.PI/g)*.5+d+c},easeInBack:function(a,c,d,e,f,g){return g==b&&(g=1.70158),e*(c/=f)*c*((g+1)*c-g)+d},easeOutBack:function(a,c,d,e,f,g){return g==b&&(g=1.70158),e*((c=c/f-1)*c*((g+1)*c+g)+1)+d},easeInOutBack:function(a,c,d,e,f,g){return g==b&&(g=1.70158),(c/=f/2)<1?e/2*c*c*(((g*=1.525)+1)*c-g)+d:e/2*((c-=2)*c*(((g*=1.525)+1)*c+g)+2)+d},easeInBounce:function(b,c,d,e,f){return e-a.easing.easeOutBounce(b,f-c,0,e,f)+d},easeOutBounce:function(a,b,c,d,e){return(b/=e)<1/2.75?d*7.5625*b*b+c:b<2/2.75?d*(7.5625*(b-=1.5/2.75)*b+.75)+c:b<2.5/2.75?d*(7.5625*(b-=2.25/2.75)*b+.9375)+c:d*(7.5625*(b-=2.625/2.75)*b+.984375)+c},easeInOutBounce:function(b,c,d,e,f){return c<f/2?a.easing.easeInBounce(b,c*2,0,e,f)*.5+d:a.easing.easeOutBounce(b,c*2-f,0,e,f)*.5+e*.5+d}})}(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.blind.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.blind=function(b){return this.queue(function(){var c=a(this),d=["position","top","bottom","left","right"],e=a.effects.setMode(c,b.options.mode||"hide"),f=b.options.direction||"vertical";a.effects.save(c,d),c.show();var g=a.effects.createWrapper(c).css({overflow:"hidden"}),h=f=="vertical"?"height":"width",i=f=="vertical"?g.height():g.width();e=="show"&&g.css(h,0);var j={};j[h]=e=="show"?i:0,g.animate(j,b.duration,b.options.easing,function(){e=="hide"&&c.hide(),a.effects.restore(c,d),a.effects.removeWrapper(c),b.callback&&b.callback.apply(c[0],arguments),c.dequeue()})})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.bounce.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.bounce=function(b){return this.queue(function(){var c=a(this),d=["position","top","bottom","left","right"],e=a.effects.setMode(c,b.options.mode||"effect"),f=b.options.direction||"up",g=b.options.distance||20,h=b.options.times||5,i=b.duration||250;/show|hide/.test(e)&&d.push("opacity"),a.effects.save(c,d),c.show(),a.effects.createWrapper(c);var j=f=="up"||f=="down"?"top":"left",k=f=="up"||f=="left"?"pos":"neg",g=b.options.distance||(j=="top"?c.outerHeight({margin:!0})/3:c.outerWidth({margin:!0})/3);e=="show"&&c.css("opacity",0).css(j,k=="pos"?-g:g),e=="hide"&&(g=g/(h*2)),e!="hide"&&h--;if(e=="show"){var l={opacity:1};l[j]=(k=="pos"?"+=":"-=")+g,c.animate(l,i/2,b.options.easing),g=g/2,h--}for(var m=0;m<h;m++){var n={},p={};n[j]=(k=="pos"?"-=":"+=")+g,p[j]=(k=="pos"?"+=":"-=")+g,c.animate(n,i/2,b.options.easing).animate(p,i/2,b.options.easing),g=e=="hide"?g*2:g/2}if(e=="hide"){var l={opacity:0};l[j]=(k=="pos"?"-=":"+=")+g,c.animate(l,i/2,b.options.easing,function(){c.hide(),a.effects.restore(c,d),a.effects.removeWrapper(c),b.callback&&b.callback.apply(this,arguments)})}else{var n={},p={};n[j]=(k=="pos"?"-=":"+=")+g,p[j]=(k=="pos"?"+=":"-=")+g,c.animate(n,i/2,b.options.easing).animate(p,i/2,b.options.easing,function(){a.effects.restore(c,d),a.effects.removeWrapper(c),b.callback&&b.callback.apply(this,arguments)})}c.queue("fx",function(){c.dequeue()}),c.dequeue()})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.clip.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.clip=function(b){return this.queue(function(){var c=a(this),d=["position","top","bottom","left","right","height","width"],e=a.effects.setMode(c,b.options.mode||"hide"),f=b.options.direction||"vertical";a.effects.save(c,d),c.show();var g=a.effects.createWrapper(c).css({overflow:"hidden"}),h=c[0].tagName=="IMG"?g:c,i={size:f=="vertical"?"height":"width",position:f=="vertical"?"top":"left"},j=f=="vertical"?h.height():h.width();e=="show"&&(h.css(i.size,0),h.css(i.position,j/2));var k={};k[i.size]=e=="show"?j:0,k[i.position]=e=="show"?0:j/2,h.animate(k,{queue:!1,duration:b.duration,easing:b.options.easing,complete:function(){e=="hide"&&c.hide(),a.effects.restore(c,d),a.effects.removeWrapper(c),b.callback&&b.callback.apply(c[0],arguments),c.dequeue()}})})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.drop.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.drop=function(b){return this.queue(function(){var c=a(this),d=["position","top","bottom","left","right","opacity"],e=a.effects.setMode(c,b.options.mode||"hide"),f=b.options.direction||"left";a.effects.save(c,d),c.show(),a.effects.createWrapper(c);var g=f=="up"||f=="down"?"top":"left",h=f=="up"||f=="left"?"pos":"neg",i=b.options.distance||(g=="top"?c.outerHeight({margin:!0})/2:c.outerWidth({margin:!0})/2);e=="show"&&c.css("opacity",0).css(g,h=="pos"?-i:i);var j={opacity:e=="show"?1:0};j[g]=(e=="show"?h=="pos"?"+=":"-=":h=="pos"?"-=":"+=")+i,c.animate(j,{queue:!1,duration:b.duration,easing:b.options.easing,complete:function(){e=="hide"&&c.hide(),a.effects.restore(c,d),a.effects.removeWrapper(c),b.callback&&b.callback.apply(this,arguments),c.dequeue()}})})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.explode.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.explode=function(b){return this.queue(function(){var c=b.options.pieces?Math.round(Math.sqrt(b.options.pieces)):3,d=b.options.pieces?Math.round(Math.sqrt(b.options.pieces)):3;b.options.mode=b.options.mode=="toggle"?a(this).is(":visible")?"hide":"show":b.options.mode;var e=a(this).show().css("visibility","hidden"),f=e.offset();f.top-=parseInt(e.css("marginTop"),10)||0,f.left-=parseInt(e.css("marginLeft"),10)||0;var g=e.outerWidth(!0),h=e.outerHeight(!0);for(var i=0;i<c;i++)for(var j=0;j<d;j++)e.clone().appendTo("body").wrap("<div></div>").css({position:"absolute",visibility:"visible",left:-j*(g/d),top:-i*(h/c)}).parent().addClass("ui-effects-explode").css({position:"absolute",overflow:"hidden",width:g/d,height:h/c,left:f.left+j*(g/d)+(b.options.mode=="show"?(j-Math.floor(d/2))*(g/d):0),top:f.top+i*(h/c)+(b.options.mode=="show"?(i-Math.floor(c/2))*(h/c):0),opacity:b.options.mode=="show"?0:1}).animate({left:f.left+j*(g/d)+(b.options.mode=="show"?0:(j-Math.floor(d/2))*(g/d)),top:f.top+i*(h/c)+(b.options.mode=="show"?0:(i-Math.floor(c/2))*(h/c)),opacity:b.options.mode=="show"?1:0},b.duration||500);setTimeout(function(){b.options.mode=="show"?e.css({visibility:"visible"}):e.css({visibility:"visible"}).hide(),b.callback&&b.callback.apply(e[0]),e.dequeue(),a("div.ui-effects-explode").remove()},b.duration||500)})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.fade.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.fade=function(b){return this.queue(function(){var c=a(this),d=a.effects.setMode(c,b.options.mode||"hide");c.animate({opacity:d},{queue:!1,duration:b.duration,easing:b.options.easing,complete:function(){b.callback&&b.callback.apply(this,arguments),c.dequeue()}})})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.fold.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.fold=function(b){return this.queue(function(){var c=a(this),d=["position","top","bottom","left","right"],e=a.effects.setMode(c,b.options.mode||"hide"),f=b.options.size||15,g=!!b.options.horizFirst,h=b.duration?b.duration/2:a.fx.speeds._default/2;a.effects.save(c,d),c.show();var i=a.effects.createWrapper(c).css({overflow:"hidden"}),j=e=="show"!=g,k=j?["width","height"]:["height","width"],l=j?[i.width(),i.height()]:[i.height(),i.width()],m=/([0-9]+)%/.exec(f);m&&(f=parseInt(m[1],10)/100*l[e=="hide"?0:1]),e=="show"&&i.css(g?{height:0,width:f}:{height:f,width:0});var n={},p={};n[k[0]]=e=="show"?l[0]:f,p[k[1]]=e=="show"?l[1]:0,i.animate(n,h,b.options.easing).animate(p,h,b.options.easing,function(){e=="hide"&&c.hide(),a.effects.restore(c,d),a.effects.removeWrapper(c),b.callback&&b.callback.apply(c[0],arguments),c.dequeue()})})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.highlight.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.highlight=function(b){return this.queue(function(){var c=a(this),d=["backgroundImage","backgroundColor","opacity"],e=a.effects.setMode(c,b.options.mode||"show"),f={backgroundColor:c.css("backgroundColor")};e=="hide"&&(f.opacity=0),a.effects.save(c,d),c.show().css({backgroundImage:"none",backgroundColor:b.options.color||"#ffff99"}).animate(f,{queue:!1,duration:b.duration,easing:b.options.easing,complete:function(){e=="hide"&&c.hide(),a.effects.restore(c,d),e=="show"&&!a.support.opacity&&this.style.removeAttribute("filter"),b.callback&&b.callback.apply(this,arguments),c.dequeue()}})})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.pulsate.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.pulsate=function(b){return this.queue(function(){var c=a(this),d=a.effects.setMode(c,b.options.mode||"show"),e=(b.options.times||5)*2-1,f=b.duration?b.duration/2:a.fx.speeds._default/2,g=c.is(":visible"),h=0;g||(c.css("opacity",0).show(),h=1),(d=="hide"&&g||d=="show"&&!g)&&e--;for(var i=0;i<e;i++)c.animate({opacity:h},f,b.options.easing),h=(h+1)%2;c.animate({opacity:h},f,b.options.easing,function(){h==0&&c.hide(),b.callback&&b.callback.apply(this,arguments)}),c.queue("fx",function(){c.dequeue()}).dequeue()})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.scale.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.puff=function(b){return this.queue(function(){var c=a(this),d=a.effects.setMode(c,b.options.mode||"hide"),e=parseInt(b.options.percent,10)||150,f=e/100,g={height:c.height(),width:c.width()};a.extend(b.options,{fade:!0,mode:d,percent:d=="hide"?e:100,from:d=="hide"?g:{height:g.height*f,width:g.width*f}}),c.effect("scale",b.options,b.duration,b.callback),c.dequeue()})},a.effects.scale=function(b){return this.queue(function(){var c=a(this),d=a.extend(!0,{},b.options),e=a.effects.setMode(c,b.options.mode||"effect"),f=parseInt(b.options.percent,10)||(parseInt(b.options.percent,10)==0?0:e=="hide"?0:100),g=b.options.direction||"both",h=b.options.origin;e!="effect"&&(d.origin=h||["middle","center"],d.restore=!0);var i={height:c.height(),width:c.width()};c.from=b.options.from||(e=="show"?{height:0,width:0}:i);var j={y:g!="horizontal"?f/100:1,x:g!="vertical"?f/100:1};c.to={height:i.height*j.y,width:i.width*j.x},b.options.fade&&(e=="show"&&(c.from.opacity=0,c.to.opacity=1),e=="hide"&&(c.from.opacity=1,c.to.opacity=0)),d.from=c.from,d.to=c.to,d.mode=e,c.effect("size",d,b.duration,b.callback),c.dequeue()})},a.effects.size=function(b){return this.queue(function(){var c=a(this),d=["position","top","bottom","left","right","width","height","overflow","opacity"],e=["position","top","bottom","left","right","overflow","opacity"],f=["width","height","overflow"],g=["fontSize"],h=["borderTopWidth","borderBottomWidth","paddingTop","paddingBottom"],i=["borderLeftWidth","borderRightWidth","paddingLeft","paddingRight"],j=a.effects.setMode(c,b.options.mode||"effect"),k=b.options.restore||!1,l=b.options.scale||"both",m=b.options.origin,n={height:c.height(),width:c.width()};c.from=b.options.from||n,c.to=b.options.to||n;if(m){var p=a.effects.getBaseline(m,n);c.from.top=(n.height-c.from.height)*p.y,c.from.left=(n.width-c.from.width)*p.x,c.to.top=(n.height-c.to.height)*p.y,c.to.left=(n.width-c.to.width)*p.x}var q={from:{y:c.from.height/n.height,x:c.from.width/n.width},to:{y:c.to.height/n.height,x:c.to.width/n.width}};if(l=="box"||l=="both")q.from.y!=q.to.y&&(d=d.concat(h),c.from=a.effects.setTransition(c,h,q.from.y,c.from),c.to=a.effects.setTransition(c,h,q.to.y,c.to)),q.from.x!=q.to.x&&(d=d.concat(i),c.from=a.effects.setTransition(c,i,q.from.x,c.from),c.to=a.effects.setTransition(c,i,q.to.x,c.to));(l=="content"||l=="both")&&q.from.y!=q.to.y&&(d=d.concat(g),c.from=a.effects.setTransition(c,g,q.from.y,c.from),c.to=a.effects.setTransition(c,g,q.to.y,c.to)),a.effects.save(c,k?d:e),c.show(),a.effects.createWrapper(c),c.css("overflow","hidden").css(c.from);if(l=="content"||l=="both")h=h.concat(["marginTop","marginBottom"]).concat(g),i=i.concat(["marginLeft","marginRight"]),f=d.concat(h).concat(i),c.find("*[width]").each(function(){var c=a(this);k&&a.effects.save(c,f);var d={height:c.height(),width:c.width()};c.from={height:d.height*q.from.y,width:d.width*q.from.x},c.to={height:d.height*q.to.y,width:d.width*q.to.x},q.from.y!=q.to.y&&(c.from=a.effects.setTransition(c,h,q.from.y,c.from),c.to=a.effects.setTransition(c,h,q.to.y,c.to)),q.from.x!=q.to.x&&(c.from=a.effects.setTransition(c,i,q.from.x,c.from),c.to=a.effects.setTransition(c,i,q.to.x,c.to)),c.css(c.from),c.animate(c.to,b.duration,b.options.easing,function(){k&&a.effects.restore(c,f)})});c.animate(c.to,{queue:!1,duration:b.duration,easing:b.options.easing,complete:function(){c.to.opacity===0&&c.css("opacity",c.from.opacity),j=="hide"&&c.hide(),a.effects.restore(c,k?d:e),a.effects.removeWrapper(c),b.callback&&b.callback.apply(this,arguments),c.dequeue()}})})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.shake.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.shake=function(b){return this.queue(function(){var c=a(this),d=["position","top","bottom","left","right"],e=a.effects.setMode(c,b.options.mode||"effect"),f=b.options.direction||"left",g=b.options.distance||20,h=b.options.times||3,i=b.duration||b.options.duration||140;a.effects.save(c,d),c.show(),a.effects.createWrapper(c);var j=f=="up"||f=="down"?"top":"left",k=f=="up"||f=="left"?"pos":"neg",l={},m={},n={};l[j]=(k=="pos"?"-=":"+=")+g,m[j]=(k=="pos"?"+=":"-=")+g*2,n[j]=(k=="pos"?"-=":"+=")+g*2,c.animate(l,i,b.options.easing);for(var p=1;p<h;p++)c.animate(m,i,b.options.easing).animate(n,i,b.options.easing);c.animate(m,i,b.options.easing).animate(l,i/2,b.options.easing,function(){a.effects.restore(c,d),a.effects.removeWrapper(c),b.callback&&b.callback.apply(this,arguments)}),c.queue("fx",function(){c.dequeue()}),c.dequeue()})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.slide.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.slide=function(b){return this.queue(function(){var c=a(this),d=["position","top","bottom","left","right"],e=a.effects.setMode(c,b.options.mode||"show"),f=b.options.direction||"left";a.effects.save(c,d),c.show(),a.effects.createWrapper(c).css({overflow:"hidden"});var g=f=="up"||f=="down"?"top":"left",h=f=="up"||f=="left"?"pos":"neg",i=b.options.distance||(g=="top"?c.outerHeight({margin:!0}):c.outerWidth({margin:!0}));e=="show"&&c.css(g,h=="pos"?isNaN(i)?"-"+i:-i:i);var j={};j[g]=(e=="show"?h=="pos"?"+=":"-=":h=="pos"?"-=":"+=")+i,c.animate(j,{queue:!1,duration:b.duration,easing:b.options.easing,complete:function(){e=="hide"&&c.hide(),a.effects.restore(c,d),a.effects.removeWrapper(c),b.callback&&b.callback.apply(this,arguments),c.dequeue()}})})}})(jQuery);;/*! jQuery UI - v1.8.21 - 2012-06-05
* https://github.com/jquery/jquery-ui
* Includes: jquery.effects.transfer.js
* Copyright (c) 2012 AUTHORS.txt; Licensed MIT, GPL */
(function(a,b){a.effects.transfer=function(b){return this.queue(function(){var c=a(this),d=a(b.options.to),e=d.offset(),f={top:e.top,left:e.left,height:d.innerHeight(),width:d.innerWidth()},g=c.offset(),h=a('<div class="ui-effects-transfer"></div>').appendTo(document.body).addClass(b.options.className).css({top:g.top,left:g.left,height:c.innerHeight(),width:c.innerWidth(),position:"absolute"}).animate(f,b.duration,b.options.easing,function(){h.remove(),b.callback&&b.callback.apply(c[0],arguments),c.dequeue()})})}})(jQuery);;
/* ===================================================
 * bootstrap-transition.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#transitions
 * ===================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================== */


!function ($) {

  $(function () {

    "use strict"; // jshint ;_;


    /* CSS TRANSITION SUPPORT (http://www.modernizr.com/)
     * ======================================================= */

    $.support.transition = (function () {

      var transitionEnd = (function () {

        var el = document.createElement('bootstrap')
          , transEndEventNames = {
               'WebkitTransition' : 'webkitTransitionEnd'
            ,  'MozTransition'    : 'transitionend'
            ,  'OTransition'      : 'oTransitionEnd'
            ,  'msTransition'     : 'MSTransitionEnd'
            ,  'transition'       : 'transitionend'
            }
          , name

        for (name in transEndEventNames){
          if (el.style[name] !== undefined) {
            return transEndEventNames[name]
          }
        }

      }())

      return transitionEnd && {
        end: transitionEnd
      }

    })()

  })

}(window.jQuery);
/* ==========================================================
 * bootstrap-alert.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#alerts
 * ==========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================== */


!function ($) {

  "use strict"; // jshint ;_;


 /* ALERT CLASS DEFINITION
  * ====================== */

  var dismiss = '[data-dismiss="alert"]'
    , Alert = function (el) {
        $(el).on('click', dismiss, this.close)
      }

  Alert.prototype.close = function (e) {
    var $this = $(this)
      , selector = $this.attr('data-target')
      , $parent

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') //strip for ie7
    }

    $parent = $(selector)

    e && e.preventDefault()

    $parent.length || ($parent = $this.hasClass('alert') ? $this : $this.parent())

    $parent.trigger(e = $.Event('close'))

    if (e.isDefaultPrevented()) return

    $parent.removeClass('in')

    function removeElement() {
      $parent
        .trigger('closed')
        .remove()
    }

    $.support.transition && $parent.hasClass('fade') ?
      $parent.on($.support.transition.end, removeElement) :
      removeElement()
  }


 /* ALERT PLUGIN DEFINITION
  * ======================= */

  $.fn.alert = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('alert')
      if (!data) $this.data('alert', (data = new Alert(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  $.fn.alert.Constructor = Alert


 /* ALERT DATA-API
  * ============== */

  $(function () {
    $('body').on('click.alert.data-api', dismiss, Alert.prototype.close)
  })

}(window.jQuery);
/* =========================================================
 * bootstrap-modal.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#modals
 * =========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================= */


!function ($) {

  "use strict"; // jshint ;_;


 /* MODAL CLASS DEFINITION
  * ====================== */

  var Modal = function (content, options) {
    this.options = options
    this.$element = $(content)
      .delegate('[data-dismiss="modal"]', 'click.dismiss.modal', $.proxy(this.hide, this))
  }

  Modal.prototype = {

      constructor: Modal

    , toggle: function () {
        return this[!this.isShown ? 'show' : 'hide']()
      }

    , show: function () {
        var that = this
          , e = $.Event('show')

        this.$element.trigger(e)

        if (this.isShown || e.isDefaultPrevented()) return

        $('body').addClass('modal-open')

        this.isShown = true

        escape.call(this)
        backdrop.call(this, function () {
          var transition = $.support.transition && that.$element.hasClass('fade')

          if (!that.$element.parent().length) {
            that.$element.appendTo(document.body) //don't move modals dom position
          }

          that.$element
            .show()

          if (transition) {
            that.$element[0].offsetWidth // force reflow
          }

          that.$element.addClass('in')

          transition ?
            that.$element.one($.support.transition.end, function () { that.$element.trigger('shown') }) :
            that.$element.trigger('shown')

        })
      }

    , hide: function (e) {
        e && e.preventDefault()

        var that = this

        e = $.Event('hide')

        this.$element.trigger(e)

        if (!this.isShown || e.isDefaultPrevented()) return

        this.isShown = false

        $('body').removeClass('modal-open')

        escape.call(this)

        this.$element.removeClass('in')

        $.support.transition && this.$element.hasClass('fade') ?
          hideWithTransition.call(this) :
          hideModal.call(this)
      }

  }


 /* MODAL PRIVATE METHODS
  * ===================== */

  function hideWithTransition() {
    var that = this
      , timeout = setTimeout(function () {
          that.$element.off($.support.transition.end)
          hideModal.call(that)
        }, 500)

    this.$element.one($.support.transition.end, function () {
      clearTimeout(timeout)
      hideModal.call(that)
    })
  }

  function hideModal(that) {
    this.$element
      .hide()
      .trigger('hidden')

    backdrop.call(this)
  }

  function backdrop(callback) {
    var that = this
      , animate = this.$element.hasClass('fade') ? 'fade' : ''

    if (this.isShown && this.options.backdrop) {
      var doAnimate = $.support.transition && animate

      this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />')
        .appendTo(document.body)

      if (this.options.backdrop != 'static') {
        this.$backdrop.click($.proxy(this.hide, this))
      }

      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow

      this.$backdrop.addClass('in')

      doAnimate ?
        this.$backdrop.one($.support.transition.end, callback) :
        callback()

    } else if (!this.isShown && this.$backdrop) {
      this.$backdrop.removeClass('in')

      $.support.transition && this.$element.hasClass('fade')?
        this.$backdrop.one($.support.transition.end, $.proxy(removeBackdrop, this)) :
        removeBackdrop.call(this)

    } else if (callback) {
      callback()
    }
  }

  function removeBackdrop() {
    this.$backdrop.remove()
    this.$backdrop = null
  }

  function escape() {
    var that = this
    if (this.isShown && this.options.keyboard) {
      $(document).on('keyup.dismiss.modal', function ( e ) {
        e.which == 27 && that.hide()
      })
    } else if (!this.isShown) {
      $(document).off('keyup.dismiss.modal')
    }
  }


 /* MODAL PLUGIN DEFINITION
  * ======================= */

  $.fn.modal = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('modal')
        , options = $.extend({}, $.fn.modal.defaults, $this.data(), typeof option == 'object' && option)
      if (!data) $this.data('modal', (data = new Modal(this, options)))
      if (typeof option == 'string') data[option]()
      else if (options.show) data.show()
    })
  }

  $.fn.modal.defaults = {
      backdrop: true
    , keyboard: true
    , show: true
  }

  $.fn.modal.Constructor = Modal


 /* MODAL DATA-API
  * ============== */

  $(function () {
    $('body').on('click.modal.data-api', '[data-toggle="modal"]', function ( e ) {
      var $this = $(this), href
        , $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) //strip for ie7
        , option = $target.data('modal') ? 'toggle' : $.extend({}, $target.data(), $this.data())

      e.preventDefault()
      $target.modal(option)
    })
  })

}(window.jQuery);
/* ============================================================
 * bootstrap-dropdown.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#dropdowns
 * ============================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================ */


!function ($) {

  "use strict"; // jshint ;_;


 /* DROPDOWN CLASS DEFINITION
  * ========================= */

  var toggle = '[data-toggle="dropdown"]'
    , Dropdown = function (element) {
        var $el = $(element).on('click.dropdown.data-api', this.toggle)
        $('html').on('click.dropdown.data-api', function () {
          $el.parent().removeClass('open')
        })
      }

  Dropdown.prototype = {

    constructor: Dropdown

  , toggle: function (e) {
      var $this = $(this)
        , $parent
        , selector
        , isActive

      if ($this.is('.disabled, :disabled')) return

      selector = $this.attr('data-target')

      if (!selector) {
        selector = $this.attr('href')
        selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') //strip for ie7
      }

      $parent = $(selector)
      $parent.length || ($parent = $this.parent())

      isActive = $parent.hasClass('open')

      clearMenus()

      if (!isActive) $parent.toggleClass('open')

      return false
    }

  }

  function clearMenus() {
    $(toggle).parent().removeClass('open')
  }


  /* DROPDOWN PLUGIN DEFINITION
   * ========================== */

  $.fn.dropdown = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('dropdown')
      if (!data) $this.data('dropdown', (data = new Dropdown(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  $.fn.dropdown.Constructor = Dropdown


  /* APPLY TO STANDARD DROPDOWN ELEMENTS
   * =================================== */

  $(function () {
    $('html').on('click.dropdown.data-api', clearMenus)
    $('body')
      .on('click.dropdown', '.dropdown form', function (e) { e.stopPropagation() })
      .on('click.dropdown.data-api', toggle, Dropdown.prototype.toggle)
  })

}(window.jQuery);
/* =============================================================
 * bootstrap-scrollspy.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#scrollspy
 * =============================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================== */


!function ($) {

  "use strict"; // jshint ;_;


  /* SCROLLSPY CLASS DEFINITION
   * ========================== */

  function ScrollSpy( element, options) {
    var process = $.proxy(this.process, this)
      , $element = $(element).is('body') ? $(window) : $(element)
      , href
    this.options = $.extend({}, $.fn.scrollspy.defaults, options)
    this.$scrollElement = $element.on('scroll.scroll.data-api', process)
    this.selector = (this.options.target
      || ((href = $(element).attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) //strip for ie7
      || '') + ' .nav li > a'
    this.$body = $('body')
    this.refresh()
    this.process()
  }

  ScrollSpy.prototype = {

      constructor: ScrollSpy

    , refresh: function () {
        var self = this
          , $targets

        this.offsets = $([])
        this.targets = $([])

        $targets = this.$body
          .find(this.selector)
          .map(function () {
            var $el = $(this)
              , href = $el.data('target') || $el.attr('href')
              , $href = /^#\w/.test(href) && $(href)
            return ( $href
              && href.length
              && [[ $href.position().top, href ]] ) || null
          })
          .sort(function (a, b) { return a[0] - b[0] })
          .each(function () {
            self.offsets.push(this[0])
            self.targets.push(this[1])
          })
      }

    , process: function () {
        var scrollTop = this.$scrollElement.scrollTop() + this.options.offset
          , scrollHeight = this.$scrollElement[0].scrollHeight || this.$body[0].scrollHeight
          , maxScroll = scrollHeight - this.$scrollElement.height()
          , offsets = this.offsets
          , targets = this.targets
          , activeTarget = this.activeTarget
          , i

        if (scrollTop >= maxScroll) {
          return activeTarget != (i = targets.last()[0])
            && this.activate ( i )
        }

        for (i = offsets.length; i--;) {
          activeTarget != targets[i]
            && scrollTop >= offsets[i]
            && (!offsets[i + 1] || scrollTop <= offsets[i + 1])
            && this.activate( targets[i] )
        }
      }

    , activate: function (target) {
        var active
          , selector

        this.activeTarget = target

        $(this.selector)
          .parent('.active')
          .removeClass('active')

        selector = this.selector
          + '[data-target="' + target + '"],'
          + this.selector + '[href="' + target + '"]'

        active = $(selector)
          .parent('li')
          .addClass('active')

        if (active.parent('.dropdown-menu'))  {
          active = active.closest('li.dropdown').addClass('active')
        }

        active.trigger('activate')
      }

  }


 /* SCROLLSPY PLUGIN DEFINITION
  * =========================== */

  $.fn.scrollspy = function ( option ) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('scrollspy')
        , options = typeof option == 'object' && option
      if (!data) $this.data('scrollspy', (data = new ScrollSpy(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.scrollspy.Constructor = ScrollSpy

  $.fn.scrollspy.defaults = {
    offset: 10
  }


 /* SCROLLSPY DATA-API
  * ================== */

  $(function () {
    $('[data-spy="scroll"]').each(function () {
      var $spy = $(this)
      $spy.scrollspy($spy.data())
    })
  })

}(window.jQuery);
/* ========================================================
 * bootstrap-tab.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#tabs
 * ========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ======================================================== */


!function ($) {

  "use strict"; // jshint ;_;


 /* TAB CLASS DEFINITION
  * ==================== */

  var Tab = function ( element ) {
    this.element = $(element)
  }

  Tab.prototype = {

    constructor: Tab

  , show: function () {
      var $this = this.element
        , $ul = $this.closest('ul:not(.dropdown-menu)')
        , selector = $this.attr('data-target')
        , previous
        , $target
        , e

      if (!selector) {
        selector = $this.attr('href')
        selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') //strip for ie7
      }

      if ( $this.parent('li').hasClass('active') ) return

      previous = $ul.find('.active a').last()[0]

      e = $.Event('show', {
        relatedTarget: previous
      })

      $this.trigger(e)

      if (e.isDefaultPrevented()) return

      $target = $(selector)

      this.activate($this.parent('li'), $ul)
      this.activate($target, $target.parent(), function () {
        $this.trigger({
          type: 'shown'
        , relatedTarget: previous
        })
      })
    }

  , activate: function ( element, container, callback) {
      var $active = container.find('> .active')
        , transition = callback
            && $.support.transition
            && $active.hasClass('fade')

      function next() {
        $active
          .removeClass('active')
          .find('> .dropdown-menu > .active')
          .removeClass('active')

        element.addClass('active')

        if (transition) {
          element[0].offsetWidth // reflow for transition
          element.addClass('in')
        } else {
          element.removeClass('fade')
        }

        if ( element.parent('.dropdown-menu') ) {
          element.closest('li.dropdown').addClass('active')
        }

        callback && callback()
      }

      transition ?
        $active.one($.support.transition.end, next) :
        next()

      $active.removeClass('in')
    }
  }


 /* TAB PLUGIN DEFINITION
  * ===================== */

  $.fn.tab = function ( option ) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('tab')
      if (!data) $this.data('tab', (data = new Tab(this)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.tab.Constructor = Tab


 /* TAB DATA-API
  * ============ */

  $(function () {
    $('body').on('click.tab.data-api', '[data-toggle="tab"], [data-toggle="pill"]', function (e) {
      e.preventDefault()
      $(this).tab('show')
    })
  })

}(window.jQuery);
/* ===========================================================
 * bootstrap-tooltip.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#tooltips
 * Inspired by the original jQuery.tipsy by Jason Frame
 * ===========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================== */


!function ($) {

  "use strict"; // jshint ;_;


 /* TOOLTIP PUBLIC CLASS DEFINITION
  * =============================== */

  var Tooltip = function (element, options) {
    this.init('tooltip', element, options)
  }

  Tooltip.prototype = {

    constructor: Tooltip

  , init: function (type, element, options) {
      var eventIn
        , eventOut

      this.type = type
      this.$element = $(element)
      this.options = this.getOptions(options)
      this.enabled = true

      if (this.options.trigger != 'manual') {
        eventIn  = this.options.trigger == 'hover' ? 'mouseenter' : 'focus'
        eventOut = this.options.trigger == 'hover' ? 'mouseleave' : 'blur'
        this.$element.on(eventIn, this.options.selector, $.proxy(this.enter, this))
        this.$element.on(eventOut, this.options.selector, $.proxy(this.leave, this))
      }

      this.options.selector ?
        (this._options = $.extend({}, this.options, { trigger: 'manual', selector: '' })) :
        this.fixTitle()
    }

  , getOptions: function (options) {
      options = $.extend({}, $.fn[this.type].defaults, options, this.$element.data())

      if (options.delay && typeof options.delay == 'number') {
        options.delay = {
          show: options.delay
        , hide: options.delay
        }
      }

      return options
    }

  , enter: function (e) {
      var self = $(e.currentTarget)[this.type](this._options).data(this.type)

      if (!self.options.delay || !self.options.delay.show) return self.show()

      clearTimeout(this.timeout)
      self.hoverState = 'in'
      this.timeout = setTimeout(function() {
        if (self.hoverState == 'in') self.show()
      }, self.options.delay.show)
    }

  , leave: function (e) {
      var self = $(e.currentTarget)[this.type](this._options).data(this.type)

      if (this.timeout) clearTimeout(this.timeout)
      if (!self.options.delay || !self.options.delay.hide) return self.hide()

      self.hoverState = 'out'
      this.timeout = setTimeout(function() {
        if (self.hoverState == 'out') self.hide()
      }, self.options.delay.hide)
    }

  , show: function () {
      var $tip
        , inside
        , pos
        , actualWidth
        , actualHeight
        , placement
        , tp

      if (this.hasContent() && this.enabled) {
        $tip = this.tip()
        this.setContent()

        if (this.options.animation) {
          $tip.addClass('fade')
        }

        placement = typeof this.options.placement == 'function' ?
          this.options.placement.call(this, $tip[0], this.$element[0]) :
          this.options.placement

        inside = /in/.test(placement)

        $tip
          .remove()
          .css({ top: 0, left: 0, display: 'block' })
          .appendTo(inside ? this.$element : document.body)

        pos = this.getPosition(inside)

        actualWidth = $tip[0].offsetWidth
        actualHeight = $tip[0].offsetHeight

        switch (inside ? placement.split(' ')[1] : placement) {
          case 'bottom':
            tp = {top: pos.top + pos.height, left: pos.left + pos.width / 2 - actualWidth / 2}
            break
          case 'top':
            tp = {top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2}
            break
          case 'left':
            tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth}
            break
          case 'right':
            tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width}
            break
        }

        $tip
          .css(tp)
          .addClass(placement)
          .addClass('in')
      }
    }

  , isHTML: function(text) {
      // html string detection logic adapted from jQuery
      return typeof text != 'string'
        || ( text.charAt(0) === "<"
          && text.charAt( text.length - 1 ) === ">"
          && text.length >= 3
        ) || /^(?:[^<]*<[\w\W]+>[^>]*$)/.exec(text)
    }

  , setContent: function () {
      var $tip = this.tip()
        , title = this.getTitle()

      $tip.find('.tooltip-inner')[this.isHTML(title) ? 'html' : 'text'](title)
      $tip.removeClass('fade in top bottom left right')
    }

  , hide: function () {
      var that = this
        , $tip = this.tip()

      $tip.removeClass('in')

      function removeWithAnimation() {
        var timeout = setTimeout(function () {
          $tip.off($.support.transition.end).remove()
        }, 500)

        $tip.one($.support.transition.end, function () {
          clearTimeout(timeout)
          $tip.remove()
        })
      }

      $.support.transition && this.$tip.hasClass('fade') ?
        removeWithAnimation() :
        $tip.remove()
    }

  , fixTitle: function () {
      var $e = this.$element
      if ($e.attr('title') || typeof($e.attr('data-original-title')) != 'string') {
        $e.attr('data-original-title', $e.attr('title') || '').removeAttr('title')
      }
    }

  , hasContent: function () {
      return this.getTitle()
    }

  , getPosition: function (inside) {
      return $.extend({}, (inside ? {top: 0, left: 0} : this.$element.offset()), {
        width: this.$element[0].offsetWidth
      , height: this.$element[0].offsetHeight
      })
    }

  , getTitle: function () {
      var title
        , $e = this.$element
        , o = this.options

      title = $e.attr('data-original-title')
        || (typeof o.title == 'function' ? o.title.call($e[0]) :  o.title)

      return title
    }

  , tip: function () {
      return this.$tip = this.$tip || $(this.options.template)
    }

  , validate: function () {
      if (!this.$element[0].parentNode) {
        this.hide()
        this.$element = null
        this.options = null
      }
    }

  , enable: function () {
      this.enabled = true
    }

  , disable: function () {
      this.enabled = false
    }

  , toggleEnabled: function () {
      this.enabled = !this.enabled
    }

  , toggle: function () {
      this[this.tip().hasClass('in') ? 'hide' : 'show']()
    }

  }


 /* TOOLTIP PLUGIN DEFINITION
  * ========================= */

  $.fn.tooltip = function ( option ) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('tooltip')
        , options = typeof option == 'object' && option
      if (!data) $this.data('tooltip', (data = new Tooltip(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.tooltip.Constructor = Tooltip

  $.fn.tooltip.defaults = {
    animation: true
  , placement: 'top'
  , selector: false
  , template: '<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
  , trigger: 'hover'
  , title: ''
  , delay: 0
  }

}(window.jQuery);

/* ===========================================================
 * bootstrap-popover.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#popovers
 * ===========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =========================================================== */


!function ($) {

  "use strict"; // jshint ;_;


 /* POPOVER PUBLIC CLASS DEFINITION
  * =============================== */

  var Popover = function ( element, options ) {
    this.init('popover', element, options)
  }


  /* NOTE: POPOVER EXTENDS BOOTSTRAP-TOOLTIP.js
     ========================================== */

  Popover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype, {

    constructor: Popover

  , setContent: function () {
      var $tip = this.tip()
        , title = this.getTitle()
        , content = this.getContent()

      $tip.find('.popover-title')[this.isHTML(title) ? 'html' : 'text'](title)
      $tip.find('.popover-content > *')[this.isHTML(content) ? 'html' : 'text'](content)

      $tip.removeClass('fade top bottom left right in')
    }

  , hasContent: function () {
      return this.getTitle() || this.getContent()
    }

  , getContent: function () {
      var content
        , $e = this.$element
        , o = this.options

      content = $e.attr('data-content')
        || (typeof o.content == 'function' ? o.content.call($e[0]) :  o.content)

      return content
    }

  , tip: function () {
      if (!this.$tip) {
        this.$tip = $(this.options.template)
      }
      return this.$tip
    }

  })


 /* POPOVER PLUGIN DEFINITION
  * ======================= */

  $.fn.popover = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('popover')
        , options = typeof option == 'object' && option
      if (!data) $this.data('popover', (data = new Popover(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.popover.Constructor = Popover

  $.fn.popover.defaults = $.extend({} , $.fn.tooltip.defaults, {
    placement: 'right'
  , content: ''
  , template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
  })

}(window.jQuery);
/* ============================================================
 * bootstrap-button.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#buttons
 * ============================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================ */


!function ($) {

  "use strict"; // jshint ;_;


 /* BUTTON PUBLIC CLASS DEFINITION
  * ============================== */

  var Button = function (element, options) {
    this.$element = $(element)
    this.options = $.extend({}, $.fn.button.defaults, options)
  }

  Button.prototype.setState = function (state) {
    var d = 'disabled'
      , $el = this.$element
      , data = $el.data()
      , val = $el.is('input') ? 'val' : 'html'

    state = state + 'Text'
    data.resetText || $el.data('resetText', $el[val]())

    $el[val](data[state] || this.options[state])

    // push to event loop to allow forms to submit
    setTimeout(function () {
      state == 'loadingText' ?
        $el.addClass(d).attr(d, d) :
        $el.removeClass(d).removeAttr(d)
    }, 0)
  }

  Button.prototype.toggle = function () {
    var $parent = this.$element.parent('[data-toggle="buttons-radio"]')

    $parent && $parent
      .find('.active')
      .removeClass('active')

    this.$element.toggleClass('active')
  }


 /* BUTTON PLUGIN DEFINITION
  * ======================== */

  $.fn.button = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('button')
        , options = typeof option == 'object' && option
      if (!data) $this.data('button', (data = new Button(this, options)))
      if (option == 'toggle') data.toggle()
      else if (option) data.setState(option)
    })
  }

  $.fn.button.defaults = {
    loadingText: 'loading...'
  }

  $.fn.button.Constructor = Button


 /* BUTTON DATA-API
  * =============== */

  $(function () {
    $('body').on('click.button.data-api', '[data-toggle^=button]', function ( e ) {
      var $btn = $(e.target)
      if (!$btn.hasClass('btn')) $btn = $btn.closest('.btn')
      $btn.button('toggle')
    })
  })

}(window.jQuery);
/* =============================================================
 * bootstrap-collapse.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#collapse
 * =============================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================ */


!function ($) {

  "use strict"; // jshint ;_;


 /* COLLAPSE PUBLIC CLASS DEFINITION
  * ================================ */

  var Collapse = function (element, options) {
    this.$element = $(element)
    this.options = $.extend({}, $.fn.collapse.defaults, options)

    if (this.options.parent) {
      this.$parent = $(this.options.parent)
    }

    this.options.toggle && this.toggle()
  }

  Collapse.prototype = {

    constructor: Collapse

  , dimension: function () {
      var hasWidth = this.$element.hasClass('width')
      return hasWidth ? 'width' : 'height'
    }

  , show: function () {
      var dimension
        , scroll
        , actives
        , hasData

      if (this.transitioning) return

      dimension = this.dimension()
      scroll = $.camelCase(['scroll', dimension].join('-'))
      actives = this.$parent && this.$parent.find('> .accordion-group > .in')

      if (actives && actives.length) {
        hasData = actives.data('collapse')
        if (hasData && hasData.transitioning) return
        actives.collapse('hide')
        hasData || actives.data('collapse', null)
      }

      this.$element[dimension](0)
      this.transition('addClass', $.Event('show'), 'shown')
      this.$element[dimension](this.$element[0][scroll])
    }

  , hide: function () {
      var dimension
      if (this.transitioning) return
      dimension = this.dimension()
      this.reset(this.$element[dimension]())
      this.transition('removeClass', $.Event('hide'), 'hidden')
      this.$element[dimension](0)
    }

  , reset: function (size) {
      var dimension = this.dimension()

      this.$element
        .removeClass('collapse')
        [dimension](size || 'auto')
        [0].offsetWidth

      this.$element[size !== null ? 'addClass' : 'removeClass']('collapse')

      return this
    }

  , transition: function (method, startEvent, completeEvent) {
      var that = this
        , complete = function () {
            if (startEvent.type == 'show') that.reset()
            that.transitioning = 0
            that.$element.trigger(completeEvent)
          }

      this.$element.trigger(startEvent)

      if (startEvent.isDefaultPrevented()) return

      this.transitioning = 1

      this.$element[method]('in')

      $.support.transition && this.$element.hasClass('collapse') ?
        this.$element.one($.support.transition.end, complete) :
        complete()
    }

  , toggle: function () {
      this[this.$element.hasClass('in') ? 'hide' : 'show']()
    }

  }


 /* COLLAPSIBLE PLUGIN DEFINITION
  * ============================== */

  $.fn.collapse = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('collapse')
        , options = typeof option == 'object' && option
      if (!data) $this.data('collapse', (data = new Collapse(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.collapse.defaults = {
    toggle: true
  }

  $.fn.collapse.Constructor = Collapse


 /* COLLAPSIBLE DATA-API
  * ==================== */

  $(function () {
    $('body').on('click.collapse.data-api', '[data-toggle=collapse]', function ( e ) {
      var $this = $(this), href
        , target = $this.attr('data-target')
          || e.preventDefault()
          || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') //strip for ie7
        , option = $(target).data('collapse') ? 'toggle' : $this.data()
      $(target).collapse(option)
    })
  })

}(window.jQuery);
/* ==========================================================
 * bootstrap-carousel.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#carousel
 * ==========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================== */


!function ($) {

  "use strict"; // jshint ;_;


 /* CAROUSEL CLASS DEFINITION
  * ========================= */

  var Carousel = function (element, options) {
    this.$element = $(element)
    this.options = options
    this.options.slide && this.slide(this.options.slide)
    this.options.pause == 'hover' && this.$element
      .on('mouseenter', $.proxy(this.pause, this))
      .on('mouseleave', $.proxy(this.cycle, this))
  }

  Carousel.prototype = {

    cycle: function (e) {
      if (!e) this.paused = false
      this.options.interval
        && !this.paused
        && (this.interval = setInterval($.proxy(this.next, this), this.options.interval))
      return this
    }

  , to: function (pos) {
      var $active = this.$element.find('.active')
        , children = $active.parent().children()
        , activePos = children.index($active)
        , that = this

      if (pos > (children.length - 1) || pos < 0) return

      if (this.sliding) {
        return this.$element.one('slid', function () {
          that.to(pos)
        })
      }

      if (activePos == pos) {
        return this.pause().cycle()
      }

      return this.slide(pos > activePos ? 'next' : 'prev', $(children[pos]))
    }

  , pause: function (e) {
      if (!e) this.paused = true
      clearInterval(this.interval)
      this.interval = null
      return this
    }

  , next: function () {
      if (this.sliding) return
      return this.slide('next')
    }

  , prev: function () {
      if (this.sliding) return
      return this.slide('prev')
    }

  , slide: function (type, next) {
      var $active = this.$element.find('.active')
        , $next = next || $active[type]()
        , isCycling = this.interval
        , direction = type == 'next' ? 'left' : 'right'
        , fallback  = type == 'next' ? 'first' : 'last'
        , that = this
        , e = $.Event('slide')

      this.sliding = true

      isCycling && this.pause()

      $next = $next.length ? $next : this.$element.find('.item')[fallback]()

      if ($next.hasClass('active')) return

      if ($.support.transition && this.$element.hasClass('slide')) {
        this.$element.trigger(e)
        if (e.isDefaultPrevented()) return
        $next.addClass(type)
        $next[0].offsetWidth // force reflow
        $active.addClass(direction)
        $next.addClass(direction)
        this.$element.one($.support.transition.end, function () {
          $next.removeClass([type, direction].join(' ')).addClass('active')
          $active.removeClass(['active', direction].join(' '))
          that.sliding = false
          setTimeout(function () { that.$element.trigger('slid') }, 0)
        })
      } else {
        this.$element.trigger(e)
        if (e.isDefaultPrevented()) return
        $active.removeClass('active')
        $next.addClass('active')
        this.sliding = false
        this.$element.trigger('slid')
      }

      isCycling && this.cycle()

      return this
    }

  }


 /* CAROUSEL PLUGIN DEFINITION
  * ========================== */

  $.fn.carousel = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('carousel')
        , options = $.extend({}, $.fn.carousel.defaults, typeof option == 'object' && option)
      if (!data) $this.data('carousel', (data = new Carousel(this, options)))
      if (typeof option == 'number') data.to(option)
      else if (typeof option == 'string' || (option = options.slide)) data[option]()
      else if (options.interval) data.cycle()
    })
  }

  $.fn.carousel.defaults = {
    interval: 5000
  , pause: 'hover'
  }

  $.fn.carousel.Constructor = Carousel


 /* CAROUSEL DATA-API
  * ================= */

  $(function () {
    $('body').on('click.carousel.data-api', '[data-slide]', function ( e ) {
      var $this = $(this), href
        , $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) //strip for ie7
        , options = !$target.data('modal') && $.extend({}, $target.data(), $this.data())
      $target.carousel(options)
      e.preventDefault()
    })
  })

}(window.jQuery);
/* =============================================================
 * bootstrap-typeahead.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#typeahead
 * =============================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================ */


!function($){

  "use strict"; // jshint ;_;


 /* TYPEAHEAD PUBLIC CLASS DEFINITION
  * ================================= */

  var Typeahead = function (element, options) {
    this.$element = $(element)
    this.options = $.extend({}, $.fn.typeahead.defaults, options)
    this.matcher = this.options.matcher || this.matcher
    this.sorter = this.options.sorter || this.sorter
    this.highlighter = this.options.highlighter || this.highlighter
    this.updater = this.options.updater || this.updater
    this.$menu = $(this.options.menu).appendTo('body')
    this.source = this.options.source
    this.shown = false
    this.listen()
  }

  Typeahead.prototype = {

    constructor: Typeahead

  , select: function () {
      var val = this.$menu.find('.active').attr('data-value')
      this.$element
        .val(this.updater(val))
        .change()
      return this.hide()
    }

  , updater: function (item) {
      return item
    }

  , show: function () {
      var pos = $.extend({}, this.$element.offset(), {
        height: this.$element[0].offsetHeight
      })

      this.$menu.css({
        top: pos.top + pos.height
      , left: pos.left
      })

      this.$menu.show()
      this.shown = true
      return this
    }

  , hide: function () {
      this.$menu.hide()
      this.shown = false
      return this
    }

  , lookup: function (event) {
      var that = this
        , items
        , q

      this.query = this.$element.val()

      if (!this.query) {
        return this.shown ? this.hide() : this
      }

      items = $.grep(this.source, function (item) {
        return that.matcher(item)
      })

      items = this.sorter(items)

      if (!items.length) {
        return this.shown ? this.hide() : this
      }

      return this.render(items.slice(0, this.options.items)).show()
    }

  , matcher: function (item) {
      return ~item.toLowerCase().indexOf(this.query.toLowerCase())
    }

  , sorter: function (items) {
      var beginswith = []
        , caseSensitive = []
        , caseInsensitive = []
        , item

      while (item = items.shift()) {
        if (!item.toLowerCase().indexOf(this.query.toLowerCase())) beginswith.push(item)
        else if (~item.indexOf(this.query)) caseSensitive.push(item)
        else caseInsensitive.push(item)
      }

      return beginswith.concat(caseSensitive, caseInsensitive)
    }

  , highlighter: function (item) {
      var query = this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, '\\$&')
      return item.replace(new RegExp('(' + query + ')', 'ig'), function ($1, match) {
        return '<strong>' + match + '</strong>'
      })
    }

  , render: function (items) {
      var that = this

      items = $(items).map(function (i, item) {
        i = $(that.options.item).attr('data-value', item)
        i.find('a').html(that.highlighter(item))
        return i[0]
      })

      items.first().addClass('active')
      this.$menu.html(items)
      return this
    }

  , next: function (event) {
      var active = this.$menu.find('.active').removeClass('active')
        , next = active.next()

      if (!next.length) {
        next = $(this.$menu.find('li')[0])
      }

      next.addClass('active')
    }

  , prev: function (event) {
      var active = this.$menu.find('.active').removeClass('active')
        , prev = active.prev()

      if (!prev.length) {
        prev = this.$menu.find('li').last()
      }

      prev.addClass('active')
    }

  , listen: function () {
      this.$element
        .on('blur',     $.proxy(this.blur, this))
        .on('keypress', $.proxy(this.keypress, this))
        .on('keyup',    $.proxy(this.keyup, this))

      if ($.browser.webkit || $.browser.msie) {
        this.$element.on('keydown', $.proxy(this.keypress, this))
      }

      this.$menu
        .on('click', $.proxy(this.click, this))
        .on('mouseenter', 'li', $.proxy(this.mouseenter, this))
    }

  , keyup: function (e) {
      switch(e.keyCode) {
        case 40: // down arrow
        case 38: // up arrow
          break

        case 9: // tab
        case 13: // enter
          if (!this.shown) return
          this.select()
          break

        case 27: // escape
          if (!this.shown) return
          this.hide()
          break

        default:
          this.lookup()
      }

      e.stopPropagation()
      e.preventDefault()
  }

  , keypress: function (e) {
      if (!this.shown) return

      switch(e.keyCode) {
        case 9: // tab
        case 13: // enter
        case 27: // escape
          e.preventDefault()
          break

        case 38: // up arrow
          if (e.type != 'keydown') break
          e.preventDefault()
          this.prev()
          break

        case 40: // down arrow
          if (e.type != 'keydown') break
          e.preventDefault()
          this.next()
          break
      }

      e.stopPropagation()
    }

  , blur: function (e) {
      var that = this
      setTimeout(function () { that.hide() }, 150)
    }

  , click: function (e) {
      e.stopPropagation()
      e.preventDefault()
      this.select()
    }

  , mouseenter: function (e) {
      this.$menu.find('.active').removeClass('active')
      $(e.currentTarget).addClass('active')
    }

  }


  /* TYPEAHEAD PLUGIN DEFINITION
   * =========================== */

  $.fn.typeahead = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('typeahead')
        , options = typeof option == 'object' && option
      if (!data) $this.data('typeahead', (data = new Typeahead(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.typeahead.defaults = {
    source: []
  , items: 8
  , menu: '<ul class="typeahead dropdown-menu"></ul>'
  , item: '<li><a href="#"></a></li>'
  }

  $.fn.typeahead.Constructor = Typeahead


 /* TYPEAHEAD DATA-API
  * ================== */

  $(function () {
    $('body').on('focus.typeahead.data-api', '[data-provide="typeahead"]', function (e) {
      var $this = $(this)
      if ($this.data('typeahead')) return
      e.preventDefault()
      $this.typeahead($this.data())
    })
  })

}(window.jQuery);
// Generated by CoffeeScript 1.3.3

/* ============================================================
# bootstrap-tour.js v0.1
# http://pushly.github.com/bootstrap-tour/
# ==============================================================
# Copyright 2012 Push.ly
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
*/


(function() {

  (function($, window) {
    var Tour, document;
    document = window.document;
    Tour = (function() {

      function Tour(options) {
        var _this = this;
        this._options = $.extend({
          afterSetState: function(key, value) {},
          afterGetState: function(key, value) {}
        }, options);
        this._steps = [];
        this.setCurrentStep();
        $(document).on("click", ".popover .next", function(e) {
          e.preventDefault();
          return _this.next();
        });
        $(document).on("click", ".popover .end", function(e) {
          e.preventDefault();
          return _this.end();
        });
      }

      Tour.prototype.setState = function(key, value) {
        $.cookie("tour_" + key, value, {
          expires: 36500,
          path: '/'
        });
        return this._options.afterSetState(key, value);
      };

      Tour.prototype.getState = function(key) {
        var value;
        value = $.cookie("tour_" + key);
        this._options.afterGetState(key, value);
        return value;
      };

      Tour.prototype.addStep = function(step) {
        return this._steps.push(step);
      };

      Tour.prototype.getStep = function(i) {
        return $.extend({
          path: "",
          placement: "right",
          title: "",
          content: "",
          next: i + 1,
          end: i === this._steps.length - 1,
          animation: true
        }, this._steps[i]);
      };

      Tour.prototype.start = function(force) {
        if (force == null) {
          force = false;
        }
        if (force || !this.ended()) {
          return this.showStep(this._current);
        }
      };

      Tour.prototype.next = function() {
        this.hideStep(this._current);
        return this.showNextStep();
      };

      Tour.prototype.end = function() {
        this.hideStep(this._current);
        return this.setState("end", "yes");
      };

      Tour.prototype.ended = function() {
        return !!this.getState("end");
      };

      Tour.prototype.restart = function() {
        this.setState("current_step", null);
        this.setState("end", null);
        this.setCurrentStep(0);
        return this.start();
      };

      Tour.prototype.hideStep = function(i) {
        var step;
        step = this.getStep(i);
        if (step.onHide != null) {
          step.onHide(this);
        }
        return $(step.element).popover("hide");
      };

      Tour.prototype.showStep = function(i) {
        var endOnClick, step,
          _this = this;
        step = this.getStep(i);
        if (step.element == null) {
          this.end;
          return;
        }
        this.setCurrentStep(i);
        if (step.path !== "" && document.location.pathname !== step.path && document.location.pathname.replace(/^.*[\\\/]/, '') !== step.path) {
          document.location.href = step.path;
          return;
        }
        if ($(step.element).is(":hidden")) {
          this.showNextStep();
          return;
        }
        endOnClick = step.endOnClick || step.element;
        $(endOnClick).one("click", function() {
          return _this.endCurrentStep();
        });
        if (step.onShow != null) {
          step.onShow(this);
        }
        return this._showPopover(step, i);
      };

      Tour.prototype.setCurrentStep = function(value) {
        if (value != null) {
          this._current = value;
          return this.setState("current_step", value);
        } else {
          this._current = this.getState("current_step");
          if (this._current === null || this._current === "null") {
            return this._current = 0;
          } else {
            return this._current = parseInt(this._current);
          }
        }
      };

      Tour.prototype.endCurrentStep = function() {
        var step;
        this.hideStep(this._current);
        step = this.getStep(this._current);
        return this.setCurrentStep(step.next);
      };

      Tour.prototype.showNextStep = function() {
        var step;
        step = this.getStep(this._current);
        return this.showStep(step.next);
      };

      Tour.prototype._showPopover = function(step, i) {
        var content, tip;
        content = "" + step.content + "<br /><p>";
        if (step.end) {
          content += "<a href='#' class='end'>End</a>";
        } else {
          content += "<a href='#" + step.next + "' class='next'>Next &raquo;</a>          <a href='#' class='pull-right end'>End tour</a></p>";
        }
        $(step.element).popover({
          placement: step.placement,
          trigger: "manual",
          title: step.title,
          content: content,
          animation: step.animation
        }).popover("show");
        tip = $(step.element).data("popover").tip();
        this._reposition(tip);
        return this._scrollIntoView(tip);
      };

      Tour.prototype._reposition = function(tip) {
        var offsetBottom, offsetRight, tipOffset;
        tipOffset = tip.offset();
        offsetBottom = $(document).outerHeight() - tipOffset.top - $(tip).outerHeight();
        if (offsetBottom < 0) {
          tipOffset.top = tipOffset.top + offsetBottom;
        }
        offsetRight = $(document).outerWidth() - tipOffset.left - $(tip).outerWidth();
        if (offsetRight < 0) {
          tipOffset.left = tipOffset.left + offsetRight;
        }
        if (tipOffset.top < 0) {
          tipOffset.top = 0;
        }
        if (tipOffset.left < 0) {
          tipOffset.left = 0;
        }
        return tip.offset(tipOffset);
      };

      Tour.prototype._scrollIntoView = function(tip) {
        var tipRect;
        tipRect = tip.get(0).getBoundingClientRect();
        if (!(tipRect.top > 0 && tipRect.bottom < $(window).height() && tipRect.left > 0 && tipRect.right < $(window).width())) {
          return tip.get(0).scrollIntoView(true);
        }
      };

      return Tour;

    })();
    return window.Tour = Tour;
  })(jQuery, window);

}).call(this);

/*!
 * jQuery Cookie Plugin
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2011, Klaus Hartl
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.opensource.org/licenses/GPL-2.0
 */
(function($) {
    $.cookie = function(key, value, options) {

        // key and at least value given, set cookie...
        if (arguments.length > 1 && (!/Object/.test(Object.prototype.toString.call(value)) || value === null || value === undefined)) {
            options = $.extend({}, options);

            if (value === null || value === undefined) {
                options.expires = -1;
            }

            if (typeof options.expires === 'number') {
                var days = options.expires, t = options.expires = new Date();
                t.setDate(t.getDate() + days);
            }

            value = String(value);

            return (document.cookie = [
                encodeURIComponent(key), '=', options.raw ? value : encodeURIComponent(value),
                options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
                options.path    ? '; path=' + options.path : '',
                options.domain  ? '; domain=' + options.domain : '',
                options.secure  ? '; secure' : ''
            ].join(''));
        }

        // key and possibly options given, get cookie...
        options = value || {};
        var decode = options.raw ? function(s) { return s; } : decodeURIComponent;

        var pairs = document.cookie.split('; ');
        for (var i = 0, pair; pair = pairs[i] && pairs[i].split('='); i++) {
            if (decode(pair[0]) === key) return decode(pair[1] || ''); // IE saves cookies with empty string as "c; ", e.g. without "=" as opposed to EOMB, thus pair[1] may be undefined
        }
        return null;
    };
})(jQuery);

/*

 FullCalendar v1.5.3
 http://arshaw.com/fullcalendar/

 Use fullcalendar.css for basic styling.
 For event drag & drop, requires jQuery UI draggable.
 For event resizing, requires jQuery UI resizable.

 Copyright (c) 2011 Adam Shaw
 Dual licensed under the MIT and GPL licenses, located in
 MIT-LICENSE.txt and GPL-LICENSE.txt respectively.

 Date: Mon Feb 6 22:40:40 2012 -0800

*/
(function(m,ma){function wb(a){m.extend(true,Ya,a)}function Yb(a,b,e){function d(k){if(E){u();q();na();S(k)}else f()}function f(){B=b.theme?"ui":"fc";a.addClass("fc");b.isRTL&&a.addClass("fc-rtl");b.theme&&a.addClass("ui-widget");E=m("<div class='fc-content' style='position:relative'/>").prependTo(a);C=new Zb(X,b);(P=C.render())&&a.prepend(P);y(b.defaultView);m(window).resize(oa);t()||g()}function g(){setTimeout(function(){!n.start&&t()&&S()},0)}function l(){m(window).unbind("resize",oa);C.destroy();
E.remove();a.removeClass("fc fc-rtl ui-widget")}function j(){return i.offsetWidth!==0}function t(){return m("body")[0].offsetWidth!==0}function y(k){if(!n||k!=n.name){F++;pa();var D=n,Z;if(D){(D.beforeHide||xb)();Za(E,E.height());D.element.hide()}else Za(E,1);E.css("overflow","hidden");if(n=Y[k])n.element.show();else n=Y[k]=new Ja[k](Z=s=m("<div class='fc-view fc-view-"+k+"' style='position:absolute'/>").appendTo(E),X);D&&C.deactivateButton(D.name);C.activateButton(k);S();E.css("overflow","");D&&
Za(E,1);Z||(n.afterShow||xb)();F--}}function S(k){if(j()){F++;pa();o===ma&&u();var D=false;if(!n.start||k||r<n.start||r>=n.end){n.render(r,k||0);fa(true);D=true}else if(n.sizeDirty){n.clearEvents();fa();D=true}else if(n.eventsDirty){n.clearEvents();D=true}n.sizeDirty=false;n.eventsDirty=false;ga(D);W=a.outerWidth();C.updateTitle(n.title);k=new Date;k>=n.start&&k<n.end?C.disableButton("today"):C.enableButton("today");F--;n.trigger("viewDisplay",i)}}function Q(){q();if(j()){u();fa();pa();n.clearEvents();
n.renderEvents(J);n.sizeDirty=false}}function q(){m.each(Y,function(k,D){D.sizeDirty=true})}function u(){o=b.contentHeight?b.contentHeight:b.height?b.height-(P?P.height():0)-Sa(E):Math.round(E.width()/Math.max(b.aspectRatio,0.5))}function fa(k){F++;n.setHeight(o,k);if(s){s.css("position","relative");s=null}n.setWidth(E.width(),k);F--}function oa(){if(!F)if(n.start){var k=++v;setTimeout(function(){if(k==v&&!F&&j())if(W!=(W=a.outerWidth())){F++;Q();n.trigger("windowResize",i);F--}},200)}else g()}function ga(k){if(!b.lazyFetching||
ya(n.visStart,n.visEnd))ra();else k&&da()}function ra(){K(n.visStart,n.visEnd)}function sa(k){J=k;da()}function ha(k){da(k)}function da(k){na();if(j()){n.clearEvents();n.renderEvents(J,k);n.eventsDirty=false}}function na(){m.each(Y,function(k,D){D.eventsDirty=true})}function ua(k,D,Z){n.select(k,D,Z===ma?true:Z)}function pa(){n&&n.unselect()}function U(){S(-1)}function ca(){S(1)}function ka(){gb(r,-1);S()}function qa(){gb(r,1);S()}function G(){r=new Date;S()}function p(k,D,Z){if(k instanceof Date)r=
N(k);else yb(r,k,D,Z);S()}function L(k,D,Z){k!==ma&&gb(r,k);D!==ma&&hb(r,D);Z!==ma&&ba(r,Z);S()}function c(){return N(r)}function z(){return n}function H(k,D){if(D===ma)return b[k];if(k=="height"||k=="contentHeight"||k=="aspectRatio"){b[k]=D;Q()}}function T(k,D){if(b[k])return b[k].apply(D||i,Array.prototype.slice.call(arguments,2))}var X=this;X.options=b;X.render=d;X.destroy=l;X.refetchEvents=ra;X.reportEvents=sa;X.reportEventChange=ha;X.rerenderEvents=da;X.changeView=y;X.select=ua;X.unselect=pa;
X.prev=U;X.next=ca;X.prevYear=ka;X.nextYear=qa;X.today=G;X.gotoDate=p;X.incrementDate=L;X.formatDate=function(k,D){return Oa(k,D,b)};X.formatDates=function(k,D,Z){return ib(k,D,Z,b)};X.getDate=c;X.getView=z;X.option=H;X.trigger=T;$b.call(X,b,e);var ya=X.isFetchNeeded,K=X.fetchEvents,i=a[0],C,P,E,B,n,Y={},W,o,s,v=0,F=0,r=new Date,J=[],M;yb(r,b.year,b.month,b.date);b.droppable&&m(document).bind("dragstart",function(k,D){var Z=k.target,ja=m(Z);if(!ja.parents(".fc").length){var ia=b.dropAccept;if(m.isFunction(ia)?
ia.call(Z,ja):ja.is(ia)){M=Z;n.dragStart(M,k,D)}}}).bind("dragstop",function(k,D){if(M){n.dragStop(M,k,D);M=null}})}function Zb(a,b){function e(){q=b.theme?"ui":"fc";if(b.header)return Q=m("<table class='fc-header' style='width:100%'/>").append(m("<tr/>").append(f("left")).append(f("center")).append(f("right")))}function d(){Q.remove()}function f(u){var fa=m("<td class='fc-header-"+u+"'/>");(u=b.header[u])&&m.each(u.split(" "),function(oa){oa>0&&fa.append("<span class='fc-header-space'/>");var ga;
m.each(this.split(","),function(ra,sa){if(sa=="title"){fa.append("<span class='fc-header-title'><h2>&nbsp;</h2></span>");ga&&ga.addClass(q+"-corner-right");ga=null}else{var ha;if(a[sa])ha=a[sa];else if(Ja[sa])ha=function(){na.removeClass(q+"-state-hover");a.changeView(sa)};if(ha){ra=b.theme?jb(b.buttonIcons,sa):null;var da=jb(b.buttonText,sa),na=m("<span class='fc-button fc-button-"+sa+" "+q+"-state-default'><span class='fc-button-inner'><span class='fc-button-content'>"+(ra?"<span class='fc-icon-wrap'><span class='ui-icon ui-icon-"+
ra+"'/></span>":da)+"</span><span class='fc-button-effect'><span></span></span></span></span>");if(na){na.click(function(){na.hasClass(q+"-state-disabled")||ha()}).mousedown(function(){na.not("."+q+"-state-active").not("."+q+"-state-disabled").addClass(q+"-state-down")}).mouseup(function(){na.removeClass(q+"-state-down")}).hover(function(){na.not("."+q+"-state-active").not("."+q+"-state-disabled").addClass(q+"-state-hover")},function(){na.removeClass(q+"-state-hover").removeClass(q+"-state-down")}).appendTo(fa);
ga||na.addClass(q+"-corner-left");ga=na}}}});ga&&ga.addClass(q+"-corner-right")});return fa}function g(u){Q.find("h2").html(u)}function l(u){Q.find("span.fc-button-"+u).addClass(q+"-state-active")}function j(u){Q.find("span.fc-button-"+u).removeClass(q+"-state-active")}function t(u){Q.find("span.fc-button-"+u).addClass(q+"-state-disabled")}function y(u){Q.find("span.fc-button-"+u).removeClass(q+"-state-disabled")}var S=this;S.render=e;S.destroy=d;S.updateTitle=g;S.activateButton=l;S.deactivateButton=
j;S.disableButton=t;S.enableButton=y;var Q=m([]),q}function $b(a,b){function e(c,z){return!ca||c<ca||z>ka}function d(c,z){ca=c;ka=z;L=[];c=++qa;G=z=U.length;for(var H=0;H<z;H++)f(U[H],c)}function f(c,z){g(c,function(H){if(z==qa){if(H){for(var T=0;T<H.length;T++){H[T].source=c;oa(H[T])}L=L.concat(H)}G--;G||ua(L)}})}function g(c,z){var H,T=Aa.sourceFetchers,X;for(H=0;H<T.length;H++){X=T[H](c,ca,ka,z);if(X===true)return;else if(typeof X=="object"){g(X,z);return}}if(H=c.events)if(m.isFunction(H)){u();
H(N(ca),N(ka),function(C){z(C);fa()})}else m.isArray(H)?z(H):z();else if(c.url){var ya=c.success,K=c.error,i=c.complete;H=m.extend({},c.data||{});T=Ta(c.startParam,a.startParam);X=Ta(c.endParam,a.endParam);if(T)H[T]=Math.round(+ca/1E3);if(X)H[X]=Math.round(+ka/1E3);u();m.ajax(m.extend({},ac,c,{data:H,success:function(C){C=C||[];var P=$a(ya,this,arguments);if(m.isArray(P))C=P;z(C)},error:function(){$a(K,this,arguments);z()},complete:function(){$a(i,this,arguments);fa()}}))}else z()}function l(c){if(c=
j(c)){G++;f(c,qa)}}function j(c){if(m.isFunction(c)||m.isArray(c))c={events:c};else if(typeof c=="string")c={url:c};if(typeof c=="object"){ga(c);U.push(c);return c}}function t(c){U=m.grep(U,function(z){return!ra(z,c)});L=m.grep(L,function(z){return!ra(z.source,c)});ua(L)}function y(c){var z,H=L.length,T,X=na().defaultEventEnd,ya=c.start-c._start,K=c.end?c.end-(c._end||X(c)):0;for(z=0;z<H;z++){T=L[z];if(T._id==c._id&&T!=c){T.start=new Date(+T.start+ya);T.end=c.end?T.end?new Date(+T.end+K):new Date(+X(T)+
K):null;T.title=c.title;T.url=c.url;T.allDay=c.allDay;T.className=c.className;T.editable=c.editable;T.color=c.color;T.backgroudColor=c.backgroudColor;T.borderColor=c.borderColor;T.textColor=c.textColor;oa(T)}}oa(c);ua(L)}function S(c,z){oa(c);if(!c.source){if(z){pa.events.push(c);c.source=pa}L.push(c)}ua(L)}function Q(c){if(c){if(!m.isFunction(c)){var z=c+"";c=function(T){return T._id==z}}L=m.grep(L,c,true);for(H=0;H<U.length;H++)if(m.isArray(U[H].events))U[H].events=m.grep(U[H].events,c,true)}else{L=
[];for(var H=0;H<U.length;H++)if(m.isArray(U[H].events))U[H].events=[]}ua(L)}function q(c){if(m.isFunction(c))return m.grep(L,c);else if(c){c+="";return m.grep(L,function(z){return z._id==c})}return L}function u(){p++||da("loading",null,true)}function fa(){--p||da("loading",null,false)}function oa(c){var z=c.source||{},H=Ta(z.ignoreTimezone,a.ignoreTimezone);c._id=c._id||(c.id===ma?"_fc"+bc++:c.id+"");if(c.date){if(!c.start)c.start=c.date;delete c.date}c._start=N(c.start=kb(c.start,H));c.end=kb(c.end,
H);if(c.end&&c.end<=c.start)c.end=null;c._end=c.end?N(c.end):null;if(c.allDay===ma)c.allDay=Ta(z.allDayDefault,a.allDayDefault);if(c.className){if(typeof c.className=="string")c.className=c.className.split(/\s+/)}else c.className=[]}function ga(c){if(c.className){if(typeof c.className=="string")c.className=c.className.split(/\s+/)}else c.className=[];for(var z=Aa.sourceNormalizers,H=0;H<z.length;H++)z[H](c)}function ra(c,z){return c&&z&&sa(c)==sa(z)}function sa(c){return(typeof c=="object"?c.events||
c.url:"")||c}var ha=this;ha.isFetchNeeded=e;ha.fetchEvents=d;ha.addEventSource=l;ha.removeEventSource=t;ha.updateEvent=y;ha.renderEvent=S;ha.removeEvents=Q;ha.clientEvents=q;ha.normalizeEvent=oa;var da=ha.trigger,na=ha.getView,ua=ha.reportEvents,pa={events:[]},U=[pa],ca,ka,qa=0,G=0,p=0,L=[];for(ha=0;ha<b.length;ha++)j(b[ha])}function gb(a,b,e){a.setFullYear(a.getFullYear()+b);e||Ka(a);return a}function hb(a,b,e){if(+a){b=a.getMonth()+b;var d=N(a);d.setDate(1);d.setMonth(b);a.setMonth(b);for(e||Ka(a);a.getMonth()!=
d.getMonth();)a.setDate(a.getDate()+(a<d?1:-1))}return a}function ba(a,b,e){if(+a){b=a.getDate()+b;var d=N(a);d.setHours(9);d.setDate(b);a.setDate(b);e||Ka(a);lb(a,d)}return a}function lb(a,b){if(+a)for(;a.getDate()!=b.getDate();)a.setTime(+a+(a<b?1:-1)*cc)}function xa(a,b){a.setMinutes(a.getMinutes()+b);return a}function Ka(a){a.setHours(0);a.setMinutes(0);a.setSeconds(0);a.setMilliseconds(0);return a}function N(a,b){if(b)return Ka(new Date(+a));return new Date(+a)}function zb(){var a=0,b;do b=new Date(1970,
a++,1);while(b.getHours());return b}function Fa(a,b,e){for(b=b||1;!a.getDay()||e&&a.getDay()==1||!e&&a.getDay()==6;)ba(a,b);return a}function Ca(a,b){return Math.round((N(a,true)-N(b,true))/Ab)}function yb(a,b,e,d){if(b!==ma&&b!=a.getFullYear()){a.setDate(1);a.setMonth(0);a.setFullYear(b)}if(e!==ma&&e!=a.getMonth()){a.setDate(1);a.setMonth(e)}d!==ma&&a.setDate(d)}function kb(a,b){if(typeof a=="object")return a;if(typeof a=="number")return new Date(a*1E3);if(typeof a=="string"){if(a.match(/^\d+(\.\d+)?$/))return new Date(parseFloat(a)*
1E3);if(b===ma)b=true;return Bb(a,b)||(a?new Date(a):null)}return null}function Bb(a,b){a=a.match(/^([0-9]{4})(-([0-9]{2})(-([0-9]{2})([T ]([0-9]{2}):([0-9]{2})(:([0-9]{2})(\.([0-9]+))?)?(Z|(([-+])([0-9]{2})(:?([0-9]{2}))?))?)?)?)?$/);if(!a)return null;var e=new Date(a[1],0,1);if(b||!a[13]){b=new Date(a[1],0,1,9,0);if(a[3]){e.setMonth(a[3]-1);b.setMonth(a[3]-1)}if(a[5]){e.setDate(a[5]);b.setDate(a[5])}lb(e,b);a[7]&&e.setHours(a[7]);a[8]&&e.setMinutes(a[8]);a[10]&&e.setSeconds(a[10]);a[12]&&e.setMilliseconds(Number("0."+
a[12])*1E3);lb(e,b)}else{e.setUTCFullYear(a[1],a[3]?a[3]-1:0,a[5]||1);e.setUTCHours(a[7]||0,a[8]||0,a[10]||0,a[12]?Number("0."+a[12])*1E3:0);if(a[14]){b=Number(a[16])*60+(a[18]?Number(a[18]):0);b*=a[15]=="-"?1:-1;e=new Date(+e+b*60*1E3)}}return e}function mb(a){if(typeof a=="number")return a*60;if(typeof a=="object")return a.getHours()*60+a.getMinutes();if(a=a.match(/(\d+)(?::(\d+))?\s*(\w+)?/)){var b=parseInt(a[1],10);if(a[3]){b%=12;if(a[3].toLowerCase().charAt(0)=="p")b+=12}return b*60+(a[2]?parseInt(a[2],
10):0)}}function Oa(a,b,e){return ib(a,null,b,e)}function ib(a,b,e,d){d=d||Ya;var f=a,g=b,l,j=e.length,t,y,S,Q="";for(l=0;l<j;l++){t=e.charAt(l);if(t=="'")for(y=l+1;y<j;y++){if(e.charAt(y)=="'"){if(f){Q+=y==l+1?"'":e.substring(l+1,y);l=y}break}}else if(t=="(")for(y=l+1;y<j;y++){if(e.charAt(y)==")"){l=Oa(f,e.substring(l+1,y),d);if(parseInt(l.replace(/\D/,""),10))Q+=l;l=y;break}}else if(t=="[")for(y=l+1;y<j;y++){if(e.charAt(y)=="]"){t=e.substring(l+1,y);l=Oa(f,t,d);if(l!=Oa(g,t,d))Q+=l;l=y;break}}else if(t==
"{"){f=b;g=a}else if(t=="}"){f=a;g=b}else{for(y=j;y>l;y--)if(S=dc[e.substring(l,y)]){if(f)Q+=S(f,d);l=y-1;break}if(y==l)if(f)Q+=t}}return Q}function Ua(a){return a.end?ec(a.end,a.allDay):ba(N(a.start),1)}function ec(a,b){a=N(a);return b||a.getHours()||a.getMinutes()?ba(a,1):Ka(a)}function fc(a,b){return(b.msLength-a.msLength)*100+(a.event.start-b.event.start)}function Cb(a,b){return a.end>b.start&&a.start<b.end}function nb(a,b,e,d){var f=[],g,l=a.length,j,t,y,S,Q;for(g=0;g<l;g++){j=a[g];t=j.start;
y=b[g];if(y>e&&t<d){if(t<e){t=N(e);S=false}else{t=t;S=true}if(y>d){y=N(d);Q=false}else{y=y;Q=true}f.push({event:j,start:t,end:y,isStart:S,isEnd:Q,msLength:y-t})}}return f.sort(fc)}function ob(a){var b=[],e,d=a.length,f,g,l,j;for(e=0;e<d;e++){f=a[e];for(g=0;;){l=false;if(b[g])for(j=0;j<b[g].length;j++)if(Cb(b[g][j],f)){l=true;break}if(l)g++;else break}if(b[g])b[g].push(f);else b[g]=[f]}return b}function Db(a,b,e){a.unbind("mouseover").mouseover(function(d){for(var f=d.target,g;f!=this;){g=f;f=f.parentNode}if((f=
g._fci)!==ma){g._fci=ma;g=b[f];e(g.event,g.element,g);m(d.target).trigger(d)}d.stopPropagation()})}function Va(a,b,e){for(var d=0,f;d<a.length;d++){f=m(a[d]);f.width(Math.max(0,b-pb(f,e)))}}function Eb(a,b,e){for(var d=0,f;d<a.length;d++){f=m(a[d]);f.height(Math.max(0,b-Sa(f,e)))}}function pb(a,b){return gc(a)+hc(a)+(b?ic(a):0)}function gc(a){return(parseFloat(m.curCSS(a[0],"paddingLeft",true))||0)+(parseFloat(m.curCSS(a[0],"paddingRight",true))||0)}function ic(a){return(parseFloat(m.curCSS(a[0],
"marginLeft",true))||0)+(parseFloat(m.curCSS(a[0],"marginRight",true))||0)}function hc(a){return(parseFloat(m.curCSS(a[0],"borderLeftWidth",true))||0)+(parseFloat(m.curCSS(a[0],"borderRightWidth",true))||0)}function Sa(a,b){return jc(a)+kc(a)+(b?Fb(a):0)}function jc(a){return(parseFloat(m.curCSS(a[0],"paddingTop",true))||0)+(parseFloat(m.curCSS(a[0],"paddingBottom",true))||0)}function Fb(a){return(parseFloat(m.curCSS(a[0],"marginTop",true))||0)+(parseFloat(m.curCSS(a[0],"marginBottom",true))||0)}
function kc(a){return(parseFloat(m.curCSS(a[0],"borderTopWidth",true))||0)+(parseFloat(m.curCSS(a[0],"borderBottomWidth",true))||0)}function Za(a,b){b=typeof b=="number"?b+"px":b;a.each(function(e,d){d.style.cssText+=";min-height:"+b+";_height:"+b})}function xb(){}function Gb(a,b){return a-b}function Hb(a){return Math.max.apply(Math,a)}function Pa(a){return(a<10?"0":"")+a}function jb(a,b){if(a[b]!==ma)return a[b];b=b.split(/(?=[A-Z])/);for(var e=b.length-1,d;e>=0;e--){d=a[b[e].toLowerCase()];if(d!==
ma)return d}return a[""]}function Qa(a){return a.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/'/g,"&#039;").replace(/"/g,"&quot;").replace(/\n/g,"<br />")}function Ib(a){return a.id+"/"+a.className+"/"+a.style.cssText.replace(/(^|;)\s*(top|left|width|height)\s*:[^;]*/ig,"")}function qb(a){a.attr("unselectable","on").css("MozUserSelect","none").bind("selectstart.ui",function(){return false})}function ab(a){a.children().removeClass("fc-first fc-last").filter(":first-child").addClass("fc-first").end().filter(":last-child").addClass("fc-last")}
function rb(a,b){a.each(function(e,d){d.className=d.className.replace(/^fc-\w*/,"fc-"+lc[b.getDay()])})}function Jb(a,b){var e=a.source||{},d=a.color,f=e.color,g=b("eventColor"),l=a.backgroundColor||d||e.backgroundColor||f||b("eventBackgroundColor")||g;d=a.borderColor||d||e.borderColor||f||b("eventBorderColor")||g;a=a.textColor||e.textColor||b("eventTextColor");b=[];l&&b.push("background-color:"+l);d&&b.push("border-color:"+d);a&&b.push("color:"+a);return b.join(";")}function $a(a,b,e){if(m.isFunction(a))a=
[a];if(a){var d,f;for(d=0;d<a.length;d++)f=a[d].apply(b,e)||f;return f}}function Ta(){for(var a=0;a<arguments.length;a++)if(arguments[a]!==ma)return arguments[a]}function mc(a,b){function e(j,t){if(t){hb(j,t);j.setDate(1)}j=N(j,true);j.setDate(1);t=hb(N(j),1);var y=N(j),S=N(t),Q=f("firstDay"),q=f("weekends")?0:1;if(q){Fa(y);Fa(S,-1,true)}ba(y,-((y.getDay()-Math.max(Q,q)+7)%7));ba(S,(7-S.getDay()+Math.max(Q,q))%7);Q=Math.round((S-y)/(Ab*7));if(f("weekMode")=="fixed"){ba(S,(6-Q)*7);Q=6}d.title=l(j,
f("titleFormat"));d.start=j;d.end=t;d.visStart=y;d.visEnd=S;g(6,Q,q?5:7,true)}var d=this;d.render=e;sb.call(d,a,b,"month");var f=d.opt,g=d.renderBasic,l=b.formatDate}function nc(a,b){function e(j,t){t&&ba(j,t*7);j=ba(N(j),-((j.getDay()-f("firstDay")+7)%7));t=ba(N(j),7);var y=N(j),S=N(t),Q=f("weekends");if(!Q){Fa(y);Fa(S,-1,true)}d.title=l(y,ba(N(S),-1),f("titleFormat"));d.start=j;d.end=t;d.visStart=y;d.visEnd=S;g(1,1,Q?7:5,false)}var d=this;d.render=e;sb.call(d,a,b,"basicWeek");var f=d.opt,g=d.renderBasic,
l=b.formatDates}function oc(a,b){function e(j,t){if(t){ba(j,t);f("weekends")||Fa(j,t<0?-1:1)}d.title=l(j,f("titleFormat"));d.start=d.visStart=N(j,true);d.end=d.visEnd=ba(N(d.start),1);g(1,1,1,false)}var d=this;d.render=e;sb.call(d,a,b,"basicDay");var f=d.opt,g=d.renderBasic,l=b.formatDate}function sb(a,b,e){function d(w,I,R,V){v=I;F=R;f();(I=!C)?g(w,V):z();l(I)}function f(){if(k=L("isRTL")){D=-1;Z=F-1}else{D=1;Z=0}ja=L("firstDay");ia=L("weekends")?0:1;la=L("theme")?"ui":"fc";$=L("columnFormat")}function g(w,
I){var R,V=la+"-widget-header",ea=la+"-widget-content",aa;R="<table class='fc-border-separate' style='width:100%' cellspacing='0'><thead><tr>";for(aa=0;aa<F;aa++)R+="<th class='fc- "+V+"'/>";R+="</tr></thead><tbody>";for(aa=0;aa<w;aa++){R+="<tr class='fc-week"+aa+"'>";for(V=0;V<F;V++)R+="<td class='fc- "+ea+" fc-day"+(aa*F+V)+"'><div>"+(I?"<div class='fc-day-number'/>":"")+"<div class='fc-day-content'><div style='position:relative'>&nbsp;</div></div></div></td>";R+="</tr>"}R+="</tbody></table>";w=
m(R).appendTo(a);K=w.find("thead");i=K.find("th");C=w.find("tbody");P=C.find("tr");E=C.find("td");B=E.filter(":first-child");n=P.eq(0).find("div.fc-day-content div");ab(K.add(K.find("tr")));ab(P);P.eq(0).addClass("fc-first");y(E);Y=m("<div style='position:absolute;z-index:8;top:0;left:0'/>").appendTo(a)}function l(w){var I=w||v==1,R=p.start.getMonth(),V=Ka(new Date),ea,aa,va;I&&i.each(function(wa,Ga){ea=m(Ga);aa=ca(wa);ea.html(ya(aa,$));rb(ea,aa)});E.each(function(wa,Ga){ea=m(Ga);aa=ca(wa);aa.getMonth()==
R?ea.removeClass("fc-other-month"):ea.addClass("fc-other-month");+aa==+V?ea.addClass(la+"-state-highlight fc-today"):ea.removeClass(la+"-state-highlight fc-today");ea.find("div.fc-day-number").text(aa.getDate());I&&rb(ea,aa)});P.each(function(wa,Ga){va=m(Ga);if(wa<v){va.show();wa==v-1?va.addClass("fc-last"):va.removeClass("fc-last")}else va.hide()})}function j(w){o=w;w=o-K.height();var I,R,V;if(L("weekMode")=="variable")I=R=Math.floor(w/(v==1?2:6));else{I=Math.floor(w/v);R=w-I*(v-1)}B.each(function(ea,
aa){if(ea<v){V=m(aa);Za(V.find("> div"),(ea==v-1?R:I)-Sa(V))}})}function t(w){W=w;M.clear();s=Math.floor(W/F);Va(i.slice(0,-1),s)}function y(w){w.click(S).mousedown(X)}function S(w){if(!L("selectable")){var I=parseInt(this.className.match(/fc\-day(\d+)/)[1]);I=ca(I);c("dayClick",this,I,true,w)}}function Q(w,I,R){R&&r.build();R=N(p.visStart);for(var V=ba(N(R),F),ea=0;ea<v;ea++){var aa=new Date(Math.max(R,w)),va=new Date(Math.min(V,I));if(aa<va){var wa;if(k){wa=Ca(va,R)*D+Z+1;aa=Ca(aa,R)*D+Z+1}else{wa=
Ca(aa,R);aa=Ca(va,R)}y(q(ea,wa,ea,aa-1))}ba(R,7);ba(V,7)}}function q(w,I,R,V){w=r.rect(w,I,R,V,a);return H(w,a)}function u(w){return N(w)}function fa(w,I){Q(w,ba(N(I),1),true)}function oa(){T()}function ga(w,I,R){var V=ua(w);c("dayClick",E[V.row*F+V.col],w,I,R)}function ra(w,I){J.start(function(R){T();R&&q(R.row,R.col,R.row,R.col)},I)}function sa(w,I,R){var V=J.stop();T();if(V){V=pa(V);c("drop",w,V,true,I,R)}}function ha(w){return N(w.start)}function da(w){return M.left(w)}function na(w){return M.right(w)}
function ua(w){return{row:Math.floor(Ca(w,p.visStart)/7),col:ka(w.getDay())}}function pa(w){return U(w.row,w.col)}function U(w,I){return ba(N(p.visStart),w*7+I*D+Z)}function ca(w){return U(Math.floor(w/F),w%F)}function ka(w){return(w-Math.max(ja,ia)+F)%F*D+Z}function qa(w){return P.eq(w)}function G(){return{left:0,right:W}}var p=this;p.renderBasic=d;p.setHeight=j;p.setWidth=t;p.renderDayOverlay=Q;p.defaultSelectionEnd=u;p.renderSelection=fa;p.clearSelection=oa;p.reportDayClick=ga;p.dragStart=ra;p.dragStop=
sa;p.defaultEventEnd=ha;p.getHoverListener=function(){return J};p.colContentLeft=da;p.colContentRight=na;p.dayOfWeekCol=ka;p.dateCell=ua;p.cellDate=pa;p.cellIsAllDay=function(){return true};p.allDayRow=qa;p.allDayBounds=G;p.getRowCnt=function(){return v};p.getColCnt=function(){return F};p.getColWidth=function(){return s};p.getDaySegmentContainer=function(){return Y};Kb.call(p,a,b,e);Lb.call(p);Mb.call(p);pc.call(p);var L=p.opt,c=p.trigger,z=p.clearEvents,H=p.renderOverlay,T=p.clearOverlays,X=p.daySelectionMousedown,
ya=b.formatDate,K,i,C,P,E,B,n,Y,W,o,s,v,F,r,J,M,k,D,Z,ja,ia,la,$;qb(a.addClass("fc-grid"));r=new Nb(function(w,I){var R,V,ea;i.each(function(aa,va){R=m(va);V=R.offset().left;if(aa)ea[1]=V;ea=[V];I[aa]=ea});ea[1]=V+R.outerWidth();P.each(function(aa,va){if(aa<v){R=m(va);V=R.offset().top;if(aa)ea[1]=V;ea=[V];w[aa]=ea}});ea[1]=V+R.outerHeight()});J=new Ob(r);M=new Pb(function(w){return n.eq(w)})}function pc(){function a(U,ca){S(U);ua(e(U),ca)}function b(){Q();ga().empty()}function e(U){var ca=da(),ka=
na(),qa=N(g.visStart);ka=ba(N(qa),ka);var G=m.map(U,Ua),p,L,c,z,H,T,X=[];for(p=0;p<ca;p++){L=ob(nb(U,G,qa,ka));for(c=0;c<L.length;c++){z=L[c];for(H=0;H<z.length;H++){T=z[H];T.row=p;T.level=c;X.push(T)}}ba(qa,7);ba(ka,7)}return X}function d(U,ca,ka){t(U)&&f(U,ca);ka.isEnd&&y(U)&&pa(U,ca,ka);q(U,ca)}function f(U,ca){var ka=ra(),qa;ca.draggable({zIndex:9,delay:50,opacity:l("dragOpacity"),revertDuration:l("dragRevertDuration"),start:function(G,p){j("eventDragStart",ca,U,G,p);fa(U,ca);ka.start(function(L,
c,z,H){ca.draggable("option","revert",!L||!z&&!H);ha();if(L){qa=z*7+H*(l("isRTL")?-1:1);sa(ba(N(U.start),qa),ba(Ua(U),qa))}else qa=0},G,"drag")},stop:function(G,p){ka.stop();ha();j("eventDragStop",ca,U,G,p);if(qa)oa(this,U,qa,0,U.allDay,G,p);else{ca.css("filter","");u(U,ca)}}})}var g=this;g.renderEvents=a;g.compileDaySegs=e;g.clearEvents=b;g.bindDaySeg=d;Qb.call(g);var l=g.opt,j=g.trigger,t=g.isEventDraggable,y=g.isEventResizable,S=g.reportEvents,Q=g.reportEventClear,q=g.eventElementHandlers,u=g.showEvents,
fa=g.hideEvents,oa=g.eventDrop,ga=g.getDaySegmentContainer,ra=g.getHoverListener,sa=g.renderDayOverlay,ha=g.clearOverlays,da=g.getRowCnt,na=g.getColCnt,ua=g.renderDaySegs,pa=g.resizableDayEvent}function qc(a,b){function e(j,t){t&&ba(j,t*7);j=ba(N(j),-((j.getDay()-f("firstDay")+7)%7));t=ba(N(j),7);var y=N(j),S=N(t),Q=f("weekends");if(!Q){Fa(y);Fa(S,-1,true)}d.title=l(y,ba(N(S),-1),f("titleFormat"));d.start=j;d.end=t;d.visStart=y;d.visEnd=S;g(Q?7:5)}var d=this;d.render=e;Rb.call(d,a,b,"agendaWeek");
var f=d.opt,g=d.renderAgenda,l=b.formatDates}function rc(a,b){function e(j,t){if(t){ba(j,t);f("weekends")||Fa(j,t<0?-1:1)}t=N(j,true);var y=ba(N(t),1);d.title=l(j,f("titleFormat"));d.start=d.visStart=t;d.end=d.visEnd=y;g(1)}var d=this;d.render=e;Rb.call(d,a,b,"agendaDay");var f=d.opt,g=d.renderAgenda,l=b.formatDate}function Rb(a,b,e){function d(h){Ba=h;f();v?P():g();l()}function f(){Wa=i("theme")?"ui":"fc";Sb=i("weekends")?0:1;Tb=i("firstDay");if(Ub=i("isRTL")){Ha=-1;Ia=Ba-1}else{Ha=1;Ia=0}La=mb(i("minTime"));
bb=mb(i("maxTime"));Vb=i("columnFormat")}function g(){var h=Wa+"-widget-header",O=Wa+"-widget-content",x,A,ta,za,Da,Ea=i("slotMinutes")%15==0;x="<table style='width:100%' class='fc-agenda-days fc-border-separate' cellspacing='0'><thead><tr><th class='fc-agenda-axis "+h+"'>&nbsp;</th>";for(A=0;A<Ba;A++)x+="<th class='fc- fc-col"+A+" "+h+"'/>";x+="<th class='fc-agenda-gutter "+h+"'>&nbsp;</th></tr></thead><tbody><tr><th class='fc-agenda-axis "+h+"'>&nbsp;</th>";for(A=0;A<Ba;A++)x+="<td class='fc- fc-col"+
A+" "+O+"'><div><div class='fc-day-content'><div style='position:relative'>&nbsp;</div></div></div></td>";x+="<td class='fc-agenda-gutter "+O+"'>&nbsp;</td></tr></tbody></table>";v=m(x).appendTo(a);F=v.find("thead");r=F.find("th").slice(1,-1);J=v.find("tbody");M=J.find("td").slice(0,-1);k=M.find("div.fc-day-content div");D=M.eq(0);Z=D.find("> div");ab(F.add(F.find("tr")));ab(J.add(J.find("tr")));aa=F.find("th:first");va=v.find(".fc-agenda-gutter");ja=m("<div style='position:absolute;z-index:2;left:0;width:100%'/>").appendTo(a);
if(i("allDaySlot")){ia=m("<div style='position:absolute;z-index:8;top:0;left:0'/>").appendTo(ja);x="<table style='width:100%' class='fc-agenda-allday' cellspacing='0'><tr><th class='"+h+" fc-agenda-axis'>"+i("allDayText")+"</th><td><div class='fc-day-content'><div style='position:relative'/></div></td><th class='"+h+" fc-agenda-gutter'>&nbsp;</th></tr></table>";la=m(x).appendTo(ja);$=la.find("tr");q($.find("td"));aa=aa.add(la.find("th:first"));va=va.add(la.find("th.fc-agenda-gutter"));ja.append("<div class='fc-agenda-divider "+
h+"'><div class='fc-agenda-divider-inner'/></div>")}else ia=m([]);w=m("<div style='position:absolute;width:100%;overflow-x:hidden;overflow-y:auto'/>").appendTo(ja);I=m("<div style='position:relative;width:100%;overflow:hidden'/>").appendTo(w);R=m("<div style='position:absolute;z-index:8;top:0;left:0'/>").appendTo(I);x="<table class='fc-agenda-slots' style='width:100%' cellspacing='0'><tbody>";ta=zb();za=xa(N(ta),bb);xa(ta,La);for(A=tb=0;ta<za;A++){Da=ta.getMinutes();x+="<tr class='fc-slot"+A+" "+
(!Da?"":"fc-minor")+"'><th class='fc-agenda-axis "+h+"'>"+(!Ea||!Da?s(ta,i("axisFormat")):"&nbsp;")+"</th><td class='"+O+"'><div style='position:relative'>&nbsp;</div></td></tr>";xa(ta,i("slotMinutes"));tb++}x+="</tbody></table>";V=m(x).appendTo(I);ea=V.find("div:first");u(V.find("td"));aa=aa.add(V.find("th:first"))}function l(){var h,O,x,A,ta=Ka(new Date);for(h=0;h<Ba;h++){A=ua(h);O=r.eq(h);O.html(s(A,Vb));x=M.eq(h);+A==+ta?x.addClass(Wa+"-state-highlight fc-today"):x.removeClass(Wa+"-state-highlight fc-today");
rb(O.add(x),A)}}function j(h,O){if(h===ma)h=Wb;Wb=h;ub={};var x=J.position().top,A=w.position().top;h=Math.min(h-x,V.height()+A+1);Z.height(h-Sa(D));ja.css("top",x);w.height(h-A-1);Xa=ea.height()+1;O&&y()}function t(h){Ga=h;cb.clear();Ma=0;Va(aa.width("").each(function(O,x){Ma=Math.max(Ma,m(x).outerWidth())}),Ma);h=w[0].clientWidth;if(vb=w.width()-h){Va(va,vb);va.show().prev().removeClass("fc-last")}else va.hide().prev().addClass("fc-last");db=Math.floor((h-Ma)/Ba);Va(r.slice(0,-1),db)}function y(){function h(){w.scrollTop(A)}
var O=zb(),x=N(O);x.setHours(i("firstHour"));var A=ca(O,x)+1;h();setTimeout(h,0)}function S(){Xb=w.scrollTop()}function Q(){w.scrollTop(Xb)}function q(h){h.click(fa).mousedown(W)}function u(h){h.click(fa).mousedown(H)}function fa(h){if(!i("selectable")){var O=Math.min(Ba-1,Math.floor((h.pageX-v.offset().left-Ma)/db)),x=ua(O),A=this.parentNode.className.match(/fc-slot(\d+)/);if(A){A=parseInt(A[1])*i("slotMinutes");var ta=Math.floor(A/60);x.setHours(ta);x.setMinutes(A%60+La);C("dayClick",M[O],x,false,
h)}else C("dayClick",M[O],x,true,h)}}function oa(h,O,x){x&&Na.build();var A=N(K.visStart);if(Ub){x=Ca(O,A)*Ha+Ia+1;h=Ca(h,A)*Ha+Ia+1}else{x=Ca(h,A);h=Ca(O,A)}x=Math.max(0,x);h=Math.min(Ba,h);x<h&&q(ga(0,x,0,h-1))}function ga(h,O,x,A){h=Na.rect(h,O,x,A,ja);return E(h,ja)}function ra(h,O){for(var x=N(K.visStart),A=ba(N(x),1),ta=0;ta<Ba;ta++){var za=new Date(Math.max(x,h)),Da=new Date(Math.min(A,O));if(za<Da){var Ea=ta*Ha+Ia;Ea=Na.rect(0,Ea,0,Ea,I);za=ca(x,za);Da=ca(x,Da);Ea.top=za;Ea.height=Da-za;u(E(Ea,
I))}ba(x,1);ba(A,1)}}function sa(h){return cb.left(h)}function ha(h){return cb.right(h)}function da(h){return{row:Math.floor(Ca(h,K.visStart)/7),col:U(h.getDay())}}function na(h){var O=ua(h.col);h=h.row;i("allDaySlot")&&h--;h>=0&&xa(O,La+h*i("slotMinutes"));return O}function ua(h){return ba(N(K.visStart),h*Ha+Ia)}function pa(h){return i("allDaySlot")&&!h.row}function U(h){return(h-Math.max(Tb,Sb)+Ba)%Ba*Ha+Ia}function ca(h,O){h=N(h,true);if(O<xa(N(h),La))return 0;if(O>=xa(N(h),bb))return V.height();
h=i("slotMinutes");O=O.getHours()*60+O.getMinutes()-La;var x=Math.floor(O/h),A=ub[x];if(A===ma)A=ub[x]=V.find("tr:eq("+x+") td div")[0].offsetTop;return Math.max(0,Math.round(A-1+Xa*(O%h/h)))}function ka(){return{left:Ma,right:Ga-vb}}function qa(){return $}function G(h){var O=N(h.start);if(h.allDay)return O;return xa(O,i("defaultEventMinutes"))}function p(h,O){if(O)return N(h);return xa(N(h),i("slotMinutes"))}function L(h,O,x){if(x)i("allDaySlot")&&oa(h,ba(N(O),1),true);else c(h,O)}function c(h,O){var x=
i("selectHelper");Na.build();if(x){var A=Ca(h,K.visStart)*Ha+Ia;if(A>=0&&A<Ba){A=Na.rect(0,A,0,A,I);var ta=ca(h,h),za=ca(h,O);if(za>ta){A.top=ta;A.height=za-ta;A.left+=2;A.width-=5;if(m.isFunction(x)){if(h=x(h,O)){A.position="absolute";A.zIndex=8;wa=m(h).css(A).appendTo(I)}}else{A.isStart=true;A.isEnd=true;wa=m(o({title:"",start:h,end:O,className:["fc-select-helper"],editable:false},A));wa.css("opacity",i("dragOpacity"))}if(wa){u(wa);I.append(wa);Va(wa,A.width,true);Eb(wa,A.height,true)}}}}else ra(h,
O)}function z(){B();if(wa){wa.remove();wa=null}}function H(h){if(h.which==1&&i("selectable")){Y(h);var O;Ra.start(function(x,A){z();if(x&&x.col==A.col&&!pa(x)){A=na(A);x=na(x);O=[A,xa(N(A),i("slotMinutes")),x,xa(N(x),i("slotMinutes"))].sort(Gb);c(O[0],O[3])}else O=null},h);m(document).one("mouseup",function(x){Ra.stop();if(O){+O[0]==+O[1]&&T(O[0],false,x);n(O[0],O[3],false,x)}})}}function T(h,O,x){C("dayClick",M[U(h.getDay())],h,O,x)}function X(h,O){Ra.start(function(x){B();if(x)if(pa(x))ga(x.row,
x.col,x.row,x.col);else{x=na(x);var A=xa(N(x),i("defaultEventMinutes"));ra(x,A)}},O)}function ya(h,O,x){var A=Ra.stop();B();A&&C("drop",h,na(A),pa(A),O,x)}var K=this;K.renderAgenda=d;K.setWidth=t;K.setHeight=j;K.beforeHide=S;K.afterShow=Q;K.defaultEventEnd=G;K.timePosition=ca;K.dayOfWeekCol=U;K.dateCell=da;K.cellDate=na;K.cellIsAllDay=pa;K.allDayRow=qa;K.allDayBounds=ka;K.getHoverListener=function(){return Ra};K.colContentLeft=sa;K.colContentRight=ha;K.getDaySegmentContainer=function(){return ia};
K.getSlotSegmentContainer=function(){return R};K.getMinMinute=function(){return La};K.getMaxMinute=function(){return bb};K.getBodyContent=function(){return I};K.getRowCnt=function(){return 1};K.getColCnt=function(){return Ba};K.getColWidth=function(){return db};K.getSlotHeight=function(){return Xa};K.defaultSelectionEnd=p;K.renderDayOverlay=oa;K.renderSelection=L;K.clearSelection=z;K.reportDayClick=T;K.dragStart=X;K.dragStop=ya;Kb.call(K,a,b,e);Lb.call(K);Mb.call(K);sc.call(K);var i=K.opt,C=K.trigger,
P=K.clearEvents,E=K.renderOverlay,B=K.clearOverlays,n=K.reportSelection,Y=K.unselect,W=K.daySelectionMousedown,o=K.slotSegHtml,s=b.formatDate,v,F,r,J,M,k,D,Z,ja,ia,la,$,w,I,R,V,ea,aa,va,wa,Ga,Wb,Ma,db,vb,Xa,Xb,Ba,tb,Na,Ra,cb,ub={},Wa,Tb,Sb,Ub,Ha,Ia,La,bb,Vb;qb(a.addClass("fc-agenda"));Na=new Nb(function(h,O){function x(eb){return Math.max(Ea,Math.min(tc,eb))}var A,ta,za;r.each(function(eb,uc){A=m(uc);ta=A.offset().left;if(eb)za[1]=ta;za=[ta];O[eb]=za});za[1]=ta+A.outerWidth();if(i("allDaySlot")){A=
$;ta=A.offset().top;h[0]=[ta,ta+A.outerHeight()]}for(var Da=I.offset().top,Ea=w.offset().top,tc=Ea+w.outerHeight(),fb=0;fb<tb;fb++)h.push([x(Da+Xa*fb),x(Da+Xa*(fb+1))])});Ra=new Ob(Na);cb=new Pb(function(h){return k.eq(h)})}function sc(){function a(o,s){sa(o);var v,F=o.length,r=[],J=[];for(v=0;v<F;v++)o[v].allDay?r.push(o[v]):J.push(o[v]);if(u("allDaySlot")){L(e(r),s);na()}g(d(J),s)}function b(){ha();ua().empty();pa().empty()}function e(o){o=ob(nb(o,m.map(o,Ua),q.visStart,q.visEnd));var s,v=o.length,
F,r,J,M=[];for(s=0;s<v;s++){F=o[s];for(r=0;r<F.length;r++){J=F[r];J.row=0;J.level=s;M.push(J)}}return M}function d(o){var s=z(),v=ka(),F=ca(),r=xa(N(q.visStart),v),J=m.map(o,f),M,k,D,Z,ja,ia,la=[];for(M=0;M<s;M++){k=ob(nb(o,J,r,xa(N(r),F-v)));vc(k);for(D=0;D<k.length;D++){Z=k[D];for(ja=0;ja<Z.length;ja++){ia=Z[ja];ia.col=M;ia.level=D;la.push(ia)}}ba(r,1,true)}return la}function f(o){return o.end?N(o.end):xa(N(o.start),u("defaultEventMinutes"))}function g(o,s){var v,F=o.length,r,J,M,k,D,Z,ja,ia,la,
$="",w,I,R={},V={},ea=pa(),aa;v=z();if(w=u("isRTL")){I=-1;aa=v-1}else{I=1;aa=0}for(v=0;v<F;v++){r=o[v];J=r.event;M=qa(r.start,r.start);k=qa(r.start,r.end);D=r.col;Z=r.level;ja=r.forward||0;ia=G(D*I+aa);la=p(D*I+aa)-ia;la=Math.min(la-6,la*0.95);D=Z?la/(Z+ja+1):ja?(la/(ja+1)-6)*2:la;Z=ia+la/(Z+ja+1)*Z*I+(w?la-D:0);r.top=M;r.left=Z;r.outerWidth=D;r.outerHeight=k-M;$+=l(J,r)}ea[0].innerHTML=$;w=ea.children();for(v=0;v<F;v++){r=o[v];J=r.event;$=m(w[v]);I=fa("eventRender",J,J,$);if(I===false)$.remove();
else{if(I&&I!==true){$.remove();$=m(I).css({position:"absolute",top:r.top,left:r.left}).appendTo(ea)}r.element=$;if(J._id===s)t(J,$,r);else $[0]._fci=v;ya(J,$)}}Db(ea,o,t);for(v=0;v<F;v++){r=o[v];if($=r.element){J=R[s=r.key=Ib($[0])];r.vsides=J===ma?(R[s]=Sa($,true)):J;J=V[s];r.hsides=J===ma?(V[s]=pb($,true)):J;s=$.find("div.fc-event-content");if(s.length)r.contentTop=s[0].offsetTop}}for(v=0;v<F;v++){r=o[v];if($=r.element){$[0].style.width=Math.max(0,r.outerWidth-r.hsides)+"px";R=Math.max(0,r.outerHeight-
r.vsides);$[0].style.height=R+"px";J=r.event;if(r.contentTop!==ma&&R-r.contentTop<10){$.find("div.fc-event-time").text(Y(J.start,u("timeFormat"))+" - "+J.title);$.find("div.fc-event-title").remove()}fa("eventAfterRender",J,J,$)}}}function l(o,s){var v="<",F=o.url,r=Jb(o,u),J=r?" style='"+r+"'":"",M=["fc-event","fc-event-skin","fc-event-vert"];oa(o)&&M.push("fc-event-draggable");s.isStart&&M.push("fc-corner-top");s.isEnd&&M.push("fc-corner-bottom");M=M.concat(o.className);if(o.source)M=M.concat(o.source.className||
[]);v+=F?"a href='"+Qa(o.url)+"'":"div";v+=" class='"+M.join(" ")+"' style='position:absolute;z-index:8;top:"+s.top+"px;left:"+s.left+"px;"+r+"'><div class='fc-event-inner fc-event-skin'"+J+"><div class='fc-event-head fc-event-skin'"+J+"><div class='fc-event-time'>"+Qa(W(o.start,o.end,u("timeFormat")))+"</div></div><div class='fc-event-content'><div class='fc-event-title'>"+Qa(o.title)+"</div></div><div class='fc-event-bg'></div></div>";if(s.isEnd&&ga(o))v+="<div class='ui-resizable-handle ui-resizable-s'>=</div>";
v+="</"+(F?"a":"div")+">";return v}function j(o,s,v){oa(o)&&y(o,s,v.isStart);v.isEnd&&ga(o)&&c(o,s,v);da(o,s)}function t(o,s,v){var F=s.find("div.fc-event-time");oa(o)&&S(o,s,F);v.isEnd&&ga(o)&&Q(o,s,F);da(o,s)}function y(o,s,v){function F(){if(!M){s.width(r).height("").draggable("option","grid",null);M=true}}var r,J,M=true,k,D=u("isRTL")?-1:1,Z=U(),ja=H(),ia=T(),la=ka();s.draggable({zIndex:9,opacity:u("dragOpacity","month"),revertDuration:u("dragRevertDuration"),start:function($,w){fa("eventDragStart",
s,o,$,w);i(o,s);r=s.width();Z.start(function(I,R,V,ea){B();if(I){J=false;k=ea*D;if(I.row)if(v){if(M){s.width(ja-10);Eb(s,ia*Math.round((o.end?(o.end-o.start)/wc:u("defaultEventMinutes"))/u("slotMinutes")));s.draggable("option","grid",[ja,1]);M=false}}else J=true;else{E(ba(N(o.start),k),ba(Ua(o),k));F()}J=J||M&&!k}else{F();J=true}s.draggable("option","revert",J)},$,"drag")},stop:function($,w){Z.stop();B();fa("eventDragStop",s,o,$,w);if(J){F();s.css("filter","");K(o,s)}else{var I=0;M||(I=Math.round((s.offset().top-
X().offset().top)/ia)*u("slotMinutes")+la-(o.start.getHours()*60+o.start.getMinutes()));C(this,o,k,I,M,$,w)}}})}function S(o,s,v){function F(I){var R=xa(N(o.start),I),V;if(o.end)V=xa(N(o.end),I);v.text(W(R,V,u("timeFormat")))}function r(){if(M){v.css("display","");s.draggable("option","grid",[$,w]);M=false}}var J,M=false,k,D,Z,ja=u("isRTL")?-1:1,ia=U(),la=z(),$=H(),w=T();s.draggable({zIndex:9,scroll:false,grid:[$,w],axis:la==1?"y":false,opacity:u("dragOpacity"),revertDuration:u("dragRevertDuration"),
start:function(I,R){fa("eventDragStart",s,o,I,R);i(o,s);J=s.position();D=Z=0;ia.start(function(V,ea,aa,va){s.draggable("option","revert",!V);B();if(V){k=va*ja;if(u("allDaySlot")&&!V.row){if(!M){M=true;v.hide();s.draggable("option","grid",null)}E(ba(N(o.start),k),ba(Ua(o),k))}else r()}},I,"drag")},drag:function(I,R){D=Math.round((R.position.top-J.top)/w)*u("slotMinutes");if(D!=Z){M||F(D);Z=D}},stop:function(I,R){var V=ia.stop();B();fa("eventDragStop",s,o,I,R);if(V&&(k||D||M))C(this,o,k,M?0:D,M,I,R);
else{r();s.css("filter","");s.css(J);F(0);K(o,s)}}})}function Q(o,s,v){var F,r,J=T();s.resizable({handles:{s:"div.ui-resizable-s"},grid:J,start:function(M,k){F=r=0;i(o,s);s.css("z-index",9);fa("eventResizeStart",this,o,M,k)},resize:function(M,k){F=Math.round((Math.max(J,s.height())-k.originalSize.height)/J);if(F!=r){v.text(W(o.start,!F&&!o.end?null:xa(ra(o),u("slotMinutes")*F),u("timeFormat")));r=F}},stop:function(M,k){fa("eventResizeStop",this,o,M,k);if(F)P(this,o,0,u("slotMinutes")*F,M,k);else{s.css("z-index",
8);K(o,s)}}})}var q=this;q.renderEvents=a;q.compileDaySegs=e;q.clearEvents=b;q.slotSegHtml=l;q.bindDaySeg=j;Qb.call(q);var u=q.opt,fa=q.trigger,oa=q.isEventDraggable,ga=q.isEventResizable,ra=q.eventEnd,sa=q.reportEvents,ha=q.reportEventClear,da=q.eventElementHandlers,na=q.setHeight,ua=q.getDaySegmentContainer,pa=q.getSlotSegmentContainer,U=q.getHoverListener,ca=q.getMaxMinute,ka=q.getMinMinute,qa=q.timePosition,G=q.colContentLeft,p=q.colContentRight,L=q.renderDaySegs,c=q.resizableDayEvent,z=q.getColCnt,
H=q.getColWidth,T=q.getSlotHeight,X=q.getBodyContent,ya=q.reportEventElement,K=q.showEvents,i=q.hideEvents,C=q.eventDrop,P=q.eventResize,E=q.renderDayOverlay,B=q.clearOverlays,n=q.calendar,Y=n.formatDate,W=n.formatDates}function vc(a){var b,e,d,f,g,l;for(b=a.length-1;b>0;b--){f=a[b];for(e=0;e<f.length;e++){g=f[e];for(d=0;d<a[b-1].length;d++){l=a[b-1][d];if(Cb(g,l))l.forward=Math.max(l.forward||0,(g.forward||0)+1)}}}}function Kb(a,b,e){function d(G,p){G=qa[G];if(typeof G=="object")return jb(G,p||e);
return G}function f(G,p){return b.trigger.apply(b,[G,p||da].concat(Array.prototype.slice.call(arguments,2),[da]))}function g(G){return j(G)&&!d("disableDragging")}function l(G){return j(G)&&!d("disableResizing")}function j(G){return Ta(G.editable,(G.source||{}).editable,d("editable"))}function t(G){U={};var p,L=G.length,c;for(p=0;p<L;p++){c=G[p];if(U[c._id])U[c._id].push(c);else U[c._id]=[c]}}function y(G){return G.end?N(G.end):na(G)}function S(G,p){ca.push(p);if(ka[G._id])ka[G._id].push(p);else ka[G._id]=
[p]}function Q(){ca=[];ka={}}function q(G,p){p.click(function(L){if(!p.hasClass("ui-draggable-dragging")&&!p.hasClass("ui-resizable-resizing"))return f("eventClick",this,G,L)}).hover(function(L){f("eventMouseover",this,G,L)},function(L){f("eventMouseout",this,G,L)})}function u(G,p){oa(G,p,"show")}function fa(G,p){oa(G,p,"hide")}function oa(G,p,L){G=ka[G._id];var c,z=G.length;for(c=0;c<z;c++)if(!p||G[c][0]!=p[0])G[c][L]()}function ga(G,p,L,c,z,H,T){var X=p.allDay,ya=p._id;sa(U[ya],L,c,z);f("eventDrop",
G,p,L,c,z,function(){sa(U[ya],-L,-c,X);pa(ya)},H,T);pa(ya)}function ra(G,p,L,c,z,H){var T=p._id;ha(U[T],L,c);f("eventResize",G,p,L,c,function(){ha(U[T],-L,-c);pa(T)},z,H);pa(T)}function sa(G,p,L,c){L=L||0;for(var z,H=G.length,T=0;T<H;T++){z=G[T];if(c!==ma)z.allDay=c;xa(ba(z.start,p,true),L);if(z.end)z.end=xa(ba(z.end,p,true),L);ua(z,qa)}}function ha(G,p,L){L=L||0;for(var c,z=G.length,H=0;H<z;H++){c=G[H];c.end=xa(ba(y(c),p,true),L);ua(c,qa)}}var da=this;da.element=a;da.calendar=b;da.name=e;da.opt=
d;da.trigger=f;da.isEventDraggable=g;da.isEventResizable=l;da.reportEvents=t;da.eventEnd=y;da.reportEventElement=S;da.reportEventClear=Q;da.eventElementHandlers=q;da.showEvents=u;da.hideEvents=fa;da.eventDrop=ga;da.eventResize=ra;var na=da.defaultEventEnd,ua=b.normalizeEvent,pa=b.reportEventChange,U={},ca=[],ka={},qa=b.options}function Qb(){function a(i,C){var P=z(),E=pa(),B=U(),n=0,Y,W,o=i.length,s,v;P[0].innerHTML=e(i);d(i,P.children());f(i);g(i,P,C);l(i);j(i);t(i);C=y();for(P=0;P<E;P++){Y=[];for(W=
0;W<B;W++)Y[W]=0;for(;n<o&&(s=i[n]).row==P;){W=Hb(Y.slice(s.startCol,s.endCol));s.top=W;W+=s.outerHeight;for(v=s.startCol;v<s.endCol;v++)Y[v]=W;n++}C[P].height(Hb(Y))}Q(i,S(C))}function b(i,C,P){var E=m("<div/>"),B=z(),n=i.length,Y;E[0].innerHTML=e(i);E=E.children();B.append(E);d(i,E);l(i);j(i);t(i);Q(i,S(y()));E=[];for(B=0;B<n;B++)if(Y=i[B].element){i[B].row===C&&Y.css("top",P);E.push(Y[0])}return m(E)}function e(i){var C=fa("isRTL"),P,E=i.length,B,n,Y,W;P=ka();var o=P.left,s=P.right,v,F,r,J,M,k=
"";for(P=0;P<E;P++){B=i[P];n=B.event;W=["fc-event","fc-event-skin","fc-event-hori"];ga(n)&&W.push("fc-event-draggable");if(C){B.isStart&&W.push("fc-corner-right");B.isEnd&&W.push("fc-corner-left");v=p(B.end.getDay()-1);F=p(B.start.getDay());r=B.isEnd?qa(v):o;J=B.isStart?G(F):s}else{B.isStart&&W.push("fc-corner-left");B.isEnd&&W.push("fc-corner-right");v=p(B.start.getDay());F=p(B.end.getDay()-1);r=B.isStart?qa(v):o;J=B.isEnd?G(F):s}W=W.concat(n.className);if(n.source)W=W.concat(n.source.className||
[]);Y=n.url;M=Jb(n,fa);k+=Y?"<a href='"+Qa(Y)+"'":"<div";k+=" class='"+W.join(" ")+"' style='position:absolute;z-index:8;left:"+r+"px;"+M+"'><div class='fc-event-inner fc-event-skin'"+(M?" style='"+M+"'":"")+">";if(!n.allDay&&B.isStart)k+="<span class='fc-event-time'>"+Qa(T(n.start,n.end,fa("timeFormat")))+"</span>";k+="<span class='fc-event-title'>"+Qa(n.title)+"</span></div>";if(B.isEnd&&ra(n))k+="<div class='ui-resizable-handle ui-resizable-"+(C?"w":"e")+"'>&nbsp;&nbsp;&nbsp;</div>";k+="</"+(Y?
"a":"div")+">";B.left=r;B.outerWidth=J-r;B.startCol=v;B.endCol=F+1}return k}function d(i,C){var P,E=i.length,B,n,Y;for(P=0;P<E;P++){B=i[P];n=B.event;Y=m(C[P]);n=oa("eventRender",n,n,Y);if(n===false)Y.remove();else{if(n&&n!==true){n=m(n).css({position:"absolute",left:B.left});Y.replaceWith(n);Y=n}B.element=Y}}}function f(i){var C,P=i.length,E,B;for(C=0;C<P;C++){E=i[C];(B=E.element)&&ha(E.event,B)}}function g(i,C,P){var E,B=i.length,n,Y,W;for(E=0;E<B;E++){n=i[E];if(Y=n.element){W=n.event;if(W._id===
P)H(W,Y,n);else Y[0]._fci=E}}Db(C,i,H)}function l(i){var C,P=i.length,E,B,n,Y,W={};for(C=0;C<P;C++){E=i[C];if(B=E.element){n=E.key=Ib(B[0]);Y=W[n];if(Y===ma)Y=W[n]=pb(B,true);E.hsides=Y}}}function j(i){var C,P=i.length,E,B;for(C=0;C<P;C++){E=i[C];if(B=E.element)B[0].style.width=Math.max(0,E.outerWidth-E.hsides)+"px"}}function t(i){var C,P=i.length,E,B,n,Y,W={};for(C=0;C<P;C++){E=i[C];if(B=E.element){n=E.key;Y=W[n];if(Y===ma)Y=W[n]=Fb(B);E.outerHeight=B[0].offsetHeight+Y}}}function y(){var i,C=pa(),
P=[];for(i=0;i<C;i++)P[i]=ca(i).find("td:first div.fc-day-content > div");return P}function S(i){var C,P=i.length,E=[];for(C=0;C<P;C++)E[C]=i[C][0].offsetTop;return E}function Q(i,C){var P,E=i.length,B,n;for(P=0;P<E;P++){B=i[P];if(n=B.element){n[0].style.top=C[B.row]+(B.top||0)+"px";B=B.event;oa("eventAfterRender",B,B,n)}}}function q(i,C,P){var E=fa("isRTL"),B=E?"w":"e",n=C.find("div.ui-resizable-"+B),Y=false;qb(C);C.mousedown(function(W){W.preventDefault()}).click(function(W){if(Y){W.preventDefault();
W.stopImmediatePropagation()}});n.mousedown(function(W){function o(ia){oa("eventResizeStop",this,i,ia);m("body").css("cursor","");s.stop();ya();k&&ua(this,i,k,0,ia);setTimeout(function(){Y=false},0)}if(W.which==1){Y=true;var s=u.getHoverListener(),v=pa(),F=U(),r=E?-1:1,J=E?F-1:0,M=C.css("top"),k,D,Z=m.extend({},i),ja=L(i.start);K();m("body").css("cursor",B+"-resize").one("mouseup",o);oa("eventResizeStart",this,i,W);s.start(function(ia,la){if(ia){var $=Math.max(ja.row,ia.row);ia=ia.col;if(v==1)$=0;
if($==ja.row)ia=E?Math.min(ja.col,ia):Math.max(ja.col,ia);k=$*7+ia*r+J-(la.row*7+la.col*r+J);la=ba(sa(i),k,true);if(k){Z.end=la;$=D;D=b(c([Z]),P.row,M);D.find("*").css("cursor",B+"-resize");$&&$.remove();na(i)}else if(D){da(i);D.remove();D=null}ya();X(i.start,ba(N(la),1))}},W)}})}var u=this;u.renderDaySegs=a;u.resizableDayEvent=q;var fa=u.opt,oa=u.trigger,ga=u.isEventDraggable,ra=u.isEventResizable,sa=u.eventEnd,ha=u.reportEventElement,da=u.showEvents,na=u.hideEvents,ua=u.eventResize,pa=u.getRowCnt,
U=u.getColCnt,ca=u.allDayRow,ka=u.allDayBounds,qa=u.colContentLeft,G=u.colContentRight,p=u.dayOfWeekCol,L=u.dateCell,c=u.compileDaySegs,z=u.getDaySegmentContainer,H=u.bindDaySeg,T=u.calendar.formatDates,X=u.renderDayOverlay,ya=u.clearOverlays,K=u.clearSelection}function Mb(){function a(Q,q,u){b();q||(q=j(Q,u));t(Q,q,u);e(Q,q,u)}function b(Q){if(S){S=false;y();l("unselect",null,Q)}}function e(Q,q,u,fa){S=true;l("select",null,Q,q,u,fa)}function d(Q){var q=f.cellDate,u=f.cellIsAllDay,fa=f.getHoverListener(),
oa=f.reportDayClick;if(Q.which==1&&g("selectable")){b(Q);var ga;fa.start(function(ra,sa){y();if(ra&&u(ra)){ga=[q(sa),q(ra)].sort(Gb);t(ga[0],ga[1],true)}else ga=null},Q);m(document).one("mouseup",function(ra){fa.stop();if(ga){+ga[0]==+ga[1]&&oa(ga[0],true,ra);e(ga[0],ga[1],true,ra)}})}}var f=this;f.select=a;f.unselect=b;f.reportSelection=e;f.daySelectionMousedown=d;var g=f.opt,l=f.trigger,j=f.defaultSelectionEnd,t=f.renderSelection,y=f.clearSelection,S=false;g("selectable")&&g("unselectAuto")&&m(document).mousedown(function(Q){var q=
g("unselectCancel");if(q)if(m(Q.target).parents(q).length)return;b(Q)})}function Lb(){function a(g,l){var j=f.shift();j||(j=m("<div class='fc-cell-overlay' style='position:absolute;z-index:3'/>"));j[0].parentNode!=l[0]&&j.appendTo(l);d.push(j.css(g).show());return j}function b(){for(var g;g=d.shift();)f.push(g.hide().unbind())}var e=this;e.renderOverlay=a;e.clearOverlays=b;var d=[],f=[]}function Nb(a){var b=this,e,d;b.build=function(){e=[];d=[];a(e,d)};b.cell=function(f,g){var l=e.length,j=d.length,
t,y=-1,S=-1;for(t=0;t<l;t++)if(g>=e[t][0]&&g<e[t][1]){y=t;break}for(t=0;t<j;t++)if(f>=d[t][0]&&f<d[t][1]){S=t;break}return y>=0&&S>=0?{row:y,col:S}:null};b.rect=function(f,g,l,j,t){t=t.offset();return{top:e[f][0]-t.top,left:d[g][0]-t.left,width:d[j][1]-d[g][0],height:e[l][1]-e[f][0]}}}function Ob(a){function b(j){xc(j);j=a.cell(j.pageX,j.pageY);if(!j!=!l||j&&(j.row!=l.row||j.col!=l.col)){if(j){g||(g=j);f(j,g,j.row-g.row,j.col-g.col)}else f(j,g);l=j}}var e=this,d,f,g,l;e.start=function(j,t,y){f=j;
g=l=null;a.build();b(t);d=y||"mousemove";m(document).bind(d,b)};e.stop=function(){m(document).unbind(d,b);return l}}function xc(a){if(a.pageX===ma){a.pageX=a.originalEvent.pageX;a.pageY=a.originalEvent.pageY}}function Pb(a){function b(l){return d[l]=d[l]||a(l)}var e=this,d={},f={},g={};e.left=function(l){return f[l]=f[l]===ma?b(l).position().left:f[l]};e.right=function(l){return g[l]=g[l]===ma?e.left(l)+b(l).width():g[l]};e.clear=function(){d={};f={};g={}}}var Ya={defaultView:"month",aspectRatio:1.35,
header:{left:"title",center:"",right:"today prev,next"},weekends:true,allDayDefault:true,ignoreTimezone:true,lazyFetching:true,startParam:"start",endParam:"end",titleFormat:{month:"MMMM yyyy",week:"MMM d[ yyyy]{ '&#8212;'[ MMM] d yyyy}",day:"dddd, MMM d, yyyy"},columnFormat:{month:"ddd",week:"ddd M/d",day:"dddd M/d"},timeFormat:{"":"h(:mm)t"},isRTL:false,firstDay:0,monthNames:["January","February","March","April","May","June","July","August","September","October","November","December"],monthNamesShort:["Jan",
"Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],dayNames:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],dayNamesShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],buttonText:{prev:"&nbsp;&#9668;&nbsp;",next:"&nbsp;&#9658;&nbsp;",prevYear:"&nbsp;&lt;&lt;&nbsp;",nextYear:"&nbsp;&gt;&gt;&nbsp;",today:"today",month:"month",week:"week",day:"day"},theme:false,buttonIcons:{prev:"circle-triangle-w",next:"circle-triangle-e"},unselectAuto:true,dropAccept:"*"},yc=
{header:{left:"next,prev today",center:"",right:"title"},buttonText:{prev:"&nbsp;&#9658;&nbsp;",next:"&nbsp;&#9668;&nbsp;",prevYear:"&nbsp;&gt;&gt;&nbsp;",nextYear:"&nbsp;&lt;&lt;&nbsp;"},buttonIcons:{prev:"circle-triangle-e",next:"circle-triangle-w"}},Aa=m.fullCalendar={version:"1.5.3"},Ja=Aa.views={};m.fn.fullCalendar=function(a){if(typeof a=="string"){var b=Array.prototype.slice.call(arguments,1),e;this.each(function(){var f=m.data(this,"fullCalendar");if(f&&m.isFunction(f[a])){f=f[a].apply(f,
b);if(e===ma)e=f;a=="destroy"&&m.removeData(this,"fullCalendar")}});if(e!==ma)return e;return this}var d=a.eventSources||[];delete a.eventSources;if(a.events){d.push(a.events);delete a.events}a=m.extend(true,{},Ya,a.isRTL||a.isRTL===ma&&Ya.isRTL?yc:{},a);this.each(function(f,g){f=m(g);g=new Yb(f,a,d);f.data("fullCalendar",g);g.render()});return this};Aa.sourceNormalizers=[];Aa.sourceFetchers=[];var ac={dataType:"json",cache:false},bc=1;Aa.addDays=ba;Aa.cloneDate=N;Aa.parseDate=kb;Aa.parseISO8601=
Bb;Aa.parseTime=mb;Aa.formatDate=Oa;Aa.formatDates=ib;var lc=["sun","mon","tue","wed","thu","fri","sat"],Ab=864E5,cc=36E5,wc=6E4,dc={s:function(a){return a.getSeconds()},ss:function(a){return Pa(a.getSeconds())},m:function(a){return a.getMinutes()},mm:function(a){return Pa(a.getMinutes())},h:function(a){return a.getHours()%12||12},hh:function(a){return Pa(a.getHours()%12||12)},H:function(a){return a.getHours()},HH:function(a){return Pa(a.getHours())},d:function(a){return a.getDate()},dd:function(a){return Pa(a.getDate())},
ddd:function(a,b){return b.dayNamesShort[a.getDay()]},dddd:function(a,b){return b.dayNames[a.getDay()]},M:function(a){return a.getMonth()+1},MM:function(a){return Pa(a.getMonth()+1)},MMM:function(a,b){return b.monthNamesShort[a.getMonth()]},MMMM:function(a,b){return b.monthNames[a.getMonth()]},yy:function(a){return(a.getFullYear()+"").substring(2)},yyyy:function(a){return a.getFullYear()},t:function(a){return a.getHours()<12?"a":"p"},tt:function(a){return a.getHours()<12?"am":"pm"},T:function(a){return a.getHours()<
12?"A":"P"},TT:function(a){return a.getHours()<12?"AM":"PM"},u:function(a){return Oa(a,"yyyy-MM-dd'T'HH:mm:ss'Z'")},S:function(a){a=a.getDate();if(a>10&&a<20)return"th";return["st","nd","rd"][a%10-1]||"th"}};Aa.applyAll=$a;Ja.month=mc;Ja.basicWeek=nc;Ja.basicDay=oc;wb({weekMode:"fixed"});Ja.agendaWeek=qc;Ja.agendaDay=rc;wb({allDaySlot:true,allDayText:"all-day",firstHour:6,slotMinutes:30,defaultEventMinutes:120,axisFormat:"h(:mm)tt",timeFormat:{agenda:"h:mm{ - h:mm}"},dragOpacity:{agenda:0.5},minTime:0,
maxTime:24})})(jQuery);

/*
 * File:        jquery.dataTables.min.js
 * Version:     1.9.2
 * Author:      Allan Jardine (www.sprymedia.co.uk)
 * Info:        www.datatables.net
 * 
 * Copyright 2008-2012 Allan Jardine, all rights reserved.
 *
 * This source file is free software, under either the GPL v2 license or a
 * BSD style license, available at:
 *   http://datatables.net/license_gpl2
 *   http://datatables.net/license_bsd
 * 
 * This source file is distributed in the hope that it will be useful, but 
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
 * or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
 */
(function(i,V,l,n){var j=function(e){function o(a,b){var c=j.defaults.columns,d=a.aoColumns.length,c=i.extend({},j.models.oColumn,c,{sSortingClass:a.oClasses.sSortable,sSortingClassJUI:a.oClasses.sSortJUI,nTh:b?b:l.createElement("th"),sTitle:c.sTitle?c.sTitle:b?b.innerHTML:"",aDataSort:c.aDataSort?c.aDataSort:[d],mDataProp:c.mDataProp?c.oDefaults:d});a.aoColumns.push(c);if(a.aoPreSearchCols[d]===n||null===a.aoPreSearchCols[d])a.aoPreSearchCols[d]=i.extend({},j.models.oSearch);else if(c=a.aoPreSearchCols[d],
c.bRegex===n&&(c.bRegex=!0),c.bSmart===n&&(c.bSmart=!0),c.bCaseInsensitive===n)c.bCaseInsensitive=!0;r(a,d,null)}function r(a,b,c){b=a.aoColumns[b];c!==n&&null!==c&&(c.sType!==n&&(b.sType=c.sType,b._bAutoType=!1),i.extend(b,c),p(b,c,"sWidth","sWidthOrig"),c.iDataSort!==n&&(b.aDataSort=[c.iDataSort]),p(b,c,"aDataSort"));b.fnGetData=W(b.mDataProp);b.fnSetData=ta(b.mDataProp);a.oFeatures.bSort||(b.bSortable=!1);!b.bSortable||-1==i.inArray("asc",b.asSorting)&&-1==i.inArray("desc",b.asSorting)?(b.sSortingClass=
a.oClasses.sSortableNone,b.sSortingClassJUI=""):b.bSortable||-1==i.inArray("asc",b.asSorting)&&-1==i.inArray("desc",b.asSorting)?(b.sSortingClass=a.oClasses.sSortable,b.sSortingClassJUI=a.oClasses.sSortJUI):-1!=i.inArray("asc",b.asSorting)&&-1==i.inArray("desc",b.asSorting)?(b.sSortingClass=a.oClasses.sSortableAsc,b.sSortingClassJUI=a.oClasses.sSortJUIAscAllowed):-1==i.inArray("asc",b.asSorting)&&-1!=i.inArray("desc",b.asSorting)&&(b.sSortingClass=a.oClasses.sSortableDesc,b.sSortingClassJUI=a.oClasses.sSortJUIDescAllowed)}
function k(a){if(!1===a.oFeatures.bAutoWidth)return!1;ba(a);for(var b=0,c=a.aoColumns.length;b<c;b++)a.aoColumns[b].nTh.style.width=a.aoColumns[b].sWidth}function G(a,b){for(var c=-1,d=0;d<a.aoColumns.length;d++)if(!0===a.aoColumns[d].bVisible&&c++,c==b)return d;return null}function t(a,b){for(var c=-1,d=0;d<a.aoColumns.length;d++)if(!0===a.aoColumns[d].bVisible&&c++,d==b)return!0===a.aoColumns[d].bVisible?c:null;return null}function v(a){for(var b=0,c=0;c<a.aoColumns.length;c++)!0===a.aoColumns[c].bVisible&&
b++;return b}function z(a){for(var b=j.ext.aTypes,c=b.length,d=0;d<c;d++){var g=b[d](a);if(null!==g)return g}return"string"}function D(a,b){for(var c=b.split(","),d=[],g=0,f=a.aoColumns.length;g<f;g++)for(var h=0;h<f;h++)if(a.aoColumns[g].sName==c[h]){d.push(h);break}return d}function x(a){for(var b="",c=0,d=a.aoColumns.length;c<d;c++)b+=a.aoColumns[c].sName+",";return b.length==d?"":b.slice(0,-1)}function J(a,b,c,d){var g,f,h,e,s;if(b)for(g=b.length-1;0<=g;g--){var m=b[g].aTargets;i.isArray(m)||
E(a,1,"aTargets must be an array of targets, not a "+typeof m);f=0;for(h=m.length;f<h;f++)if("number"===typeof m[f]&&0<=m[f]){for(;a.aoColumns.length<=m[f];)o(a);d(m[f],b[g])}else if("number"===typeof m[f]&&0>m[f])d(a.aoColumns.length+m[f],b[g]);else if("string"===typeof m[f]){e=0;for(s=a.aoColumns.length;e<s;e++)("_all"==m[f]||i(a.aoColumns[e].nTh).hasClass(m[f]))&&d(e,b[g])}}if(c){g=0;for(a=c.length;g<a;g++)d(g,c[g])}}function H(a,b){var c;c=i.isArray(b)?b.slice():i.extend(!0,{},b);var d=a.aoData.length,
g=i.extend(!0,{},j.models.oRow);g._aData=c;a.aoData.push(g);for(var f,g=0,h=a.aoColumns.length;g<h;g++)c=a.aoColumns[g],"function"===typeof c.fnRender&&c.bUseRendered&&null!==c.mDataProp?I(a,d,g,R(a,d,g)):I(a,d,g,w(a,d,g)),c._bAutoType&&"string"!=c.sType&&(f=w(a,d,g,"type"),null!==f&&""!==f&&(f=z(f),null===c.sType?c.sType=f:c.sType!=f&&"html"!=c.sType&&(c.sType="string")));a.aiDisplayMaster.push(d);a.oFeatures.bDeferRender||ca(a,d);return d}function ua(a){var b,c,d,g,f,h,e,s,m;if(a.bDeferLoading||
null===a.sAjaxSource){e=a.nTBody.childNodes;b=0;for(c=e.length;b<c;b++)if("TR"==e[b].nodeName.toUpperCase()){s=a.aoData.length;e[b]._DT_RowIndex=s;a.aoData.push(i.extend(!0,{},j.models.oRow,{nTr:e[b]}));a.aiDisplayMaster.push(s);h=e[b].childNodes;d=f=0;for(g=h.length;d<g;d++)if(m=h[d].nodeName.toUpperCase(),"TD"==m||"TH"==m)I(a,s,f,i.trim(h[d].innerHTML)),f++}}e=S(a);h=[];b=0;for(c=e.length;b<c;b++){d=0;for(g=e[b].childNodes.length;d<g;d++)f=e[b].childNodes[d],m=f.nodeName.toUpperCase(),("TD"==m||
"TH"==m)&&h.push(f)}g=0;for(e=a.aoColumns.length;g<e;g++){m=a.aoColumns[g];null===m.sTitle&&(m.sTitle=m.nTh.innerHTML);f=m._bAutoType;s="function"===typeof m.fnRender;var o=null!==m.sClass,k=m.bVisible,n,r;if(f||s||o||!k){b=0;for(c=a.aoData.length;b<c;b++)d=a.aoData[b],n=h[b*e+g],f&&"string"!=m.sType&&(r=w(a,b,g,"type"),""!==r&&(r=z(r),null===m.sType?m.sType=r:m.sType!=r&&"html"!=m.sType&&(m.sType="string"))),"function"===typeof m.mDataProp&&(n.innerHTML=w(a,b,g,"display")),s&&(r=R(a,b,g),n.innerHTML=
r,m.bUseRendered&&I(a,b,g,r)),o&&(n.className+=" "+m.sClass),k?d._anHidden[g]=null:(d._anHidden[g]=n,n.parentNode.removeChild(n)),m.fnCreatedCell&&m.fnCreatedCell.call(a.oInstance,n,w(a,b,g,"display"),d._aData,b,g)}}if(0!==a.aoRowCreatedCallback.length){b=0;for(c=a.aoData.length;b<c;b++)d=a.aoData[b],C(a,"aoRowCreatedCallback",null,[d.nTr,d._aData,b])}}function K(a,b){return b._DT_RowIndex!==n?b._DT_RowIndex:null}function da(a,b,c){for(var b=L(a,b),d=0,a=a.aoColumns.length;d<a;d++)if(b[d]===c)return d;
return-1}function X(a,b,c){for(var d=[],g=0,f=a.aoColumns.length;g<f;g++)d.push(w(a,b,g,c));return d}function w(a,b,c,d){var g=a.aoColumns[c];if((c=g.fnGetData(a.aoData[b]._aData,d))===n)return a.iDrawError!=a.iDraw&&null===g.sDefaultContent&&(E(a,0,"Requested unknown parameter "+("function"==typeof g.mDataProp?"{mDataprop function}":"'"+g.mDataProp+"'")+" from the data source for row "+b),a.iDrawError=a.iDraw),g.sDefaultContent;if(null===c&&null!==g.sDefaultContent)c=g.sDefaultContent;else if("function"===
typeof c)return c();return"display"==d&&null===c?"":c}function I(a,b,c,d){a.aoColumns[c].fnSetData(a.aoData[b]._aData,d)}function W(a){if(null===a)return function(){return null};if("function"===typeof a)return function(b,d){return a(b,d)};if("string"===typeof a&&-1!=a.indexOf(".")){var b=a.split(".");return function(a){for(var d=0,g=b.length;d<g;d++)if(a=a[b[d]],a===n)return n;return a}}return function(b){return b[a]}}function ta(a){if(null===a)return function(){};if("function"===typeof a)return function(b,
d){a(b,"set",d)};if("string"===typeof a&&-1!=a.indexOf(".")){var b=a.split(".");return function(a,d){for(var g=0,f=b.length-1;g<f;g++)a[b[g]]===n&&(a[b[g]]={}),a=a[b[g]];a[b[b.length-1]]=d}}return function(b,d){b[a]=d}}function Y(a){for(var b=[],c=a.aoData.length,d=0;d<c;d++)b.push(a.aoData[d]._aData);return b}function ea(a){a.aoData.splice(0,a.aoData.length);a.aiDisplayMaster.splice(0,a.aiDisplayMaster.length);a.aiDisplay.splice(0,a.aiDisplay.length);A(a)}function fa(a,b){for(var c=-1,d=0,g=a.length;d<
g;d++)a[d]==b?c=d:a[d]>b&&a[d]--; -1!=c&&a.splice(c,1)}function R(a,b,c){var d=a.aoColumns[c];return d.fnRender({iDataRow:b,iDataColumn:c,oSettings:a,aData:a.aoData[b]._aData,mDataProp:d.mDataProp},w(a,b,c,"display"))}function ca(a,b){var c=a.aoData[b],d;if(null===c.nTr){c.nTr=l.createElement("tr");c.nTr._DT_RowIndex=b;c._aData.DT_RowId&&(c.nTr.id=c._aData.DT_RowId);c._aData.DT_RowClass&&i(c.nTr).addClass(c._aData.DT_RowClass);for(var g=0,f=a.aoColumns.length;g<f;g++){var h=a.aoColumns[g];d=l.createElement(h.sCellType);
d.innerHTML="function"===typeof h.fnRender&&(!h.bUseRendered||null===h.mDataProp)?R(a,b,g):w(a,b,g,"display");null!==h.sClass&&(d.className=h.sClass);h.bVisible?(c.nTr.appendChild(d),c._anHidden[g]=null):c._anHidden[g]=d;h.fnCreatedCell&&h.fnCreatedCell.call(a.oInstance,d,w(a,b,g,"display"),c._aData,b,g)}C(a,"aoRowCreatedCallback",null,[c.nTr,c._aData,b])}}function va(a){var b,c,d;if(0!==a.nTHead.getElementsByTagName("th").length){b=0;for(d=a.aoColumns.length;b<d;b++)if(c=a.aoColumns[b].nTh,c.setAttribute("role",
"columnheader"),a.aoColumns[b].bSortable&&(c.setAttribute("tabindex",a.iTabIndex),c.setAttribute("aria-controls",a.sTableId)),null!==a.aoColumns[b].sClass&&i(c).addClass(a.aoColumns[b].sClass),a.aoColumns[b].sTitle!=c.innerHTML)c.innerHTML=a.aoColumns[b].sTitle}else{var g=l.createElement("tr");b=0;for(d=a.aoColumns.length;b<d;b++)c=a.aoColumns[b].nTh,c.innerHTML=a.aoColumns[b].sTitle,c.setAttribute("tabindex","0"),null!==a.aoColumns[b].sClass&&i(c).addClass(a.aoColumns[b].sClass),g.appendChild(c);
i(a.nTHead).html("")[0].appendChild(g);T(a.aoHeader,a.nTHead)}i(a.nTHead).children("tr").attr("role","row");if(a.bJUI){b=0;for(d=a.aoColumns.length;b<d;b++){c=a.aoColumns[b].nTh;g=l.createElement("div");g.className=a.oClasses.sSortJUIWrapper;i(c).contents().appendTo(g);var f=l.createElement("span");f.className=a.oClasses.sSortIcon;g.appendChild(f);c.appendChild(g)}}if(a.oFeatures.bSort)for(b=0;b<a.aoColumns.length;b++)!1!==a.aoColumns[b].bSortable?ga(a,a.aoColumns[b].nTh,b):i(a.aoColumns[b].nTh).addClass(a.oClasses.sSortableNone);
""!==a.oClasses.sFooterTH&&i(a.nTFoot).children("tr").children("th").addClass(a.oClasses.sFooterTH);if(null!==a.nTFoot){c=O(a,null,a.aoFooter);b=0;for(d=a.aoColumns.length;b<d;b++)c[b]&&(a.aoColumns[b].nTf=c[b],a.aoColumns[b].sClass&&i(c[b]).addClass(a.aoColumns[b].sClass))}}function U(a,b,c){var d,g,f,h=[],e=[],i=a.aoColumns.length,m;c===n&&(c=!1);d=0;for(g=b.length;d<g;d++){h[d]=b[d].slice();h[d].nTr=b[d].nTr;for(f=i-1;0<=f;f--)!a.aoColumns[f].bVisible&&!c&&h[d].splice(f,1);e.push([])}d=0;for(g=
h.length;d<g;d++){if(a=h[d].nTr)for(;f=a.firstChild;)a.removeChild(f);f=0;for(b=h[d].length;f<b;f++)if(m=i=1,e[d][f]===n){a.appendChild(h[d][f].cell);for(e[d][f]=1;h[d+i]!==n&&h[d][f].cell==h[d+i][f].cell;)e[d+i][f]=1,i++;for(;h[d][f+m]!==n&&h[d][f].cell==h[d][f+m].cell;){for(c=0;c<i;c++)e[d+c][f+m]=1;m++}h[d][f].cell.rowSpan=i;h[d][f].cell.colSpan=m}}}function y(a){var b=C(a,"aoPreDrawCallback","preDraw",[a]);if(-1!==i.inArray(!1,b))F(a,!1);else{var c,d,b=[],g=0,f=a.asStripeClasses.length;c=a.aoOpenRows.length;
a.bDrawing=!0;a.iInitDisplayStart!==n&&-1!=a.iInitDisplayStart&&(a._iDisplayStart=a.oFeatures.bServerSide?a.iInitDisplayStart:a.iInitDisplayStart>=a.fnRecordsDisplay()?0:a.iInitDisplayStart,a.iInitDisplayStart=-1,A(a));if(a.bDeferLoading)a.bDeferLoading=!1,a.iDraw++;else if(a.oFeatures.bServerSide){if(!a.bDestroying&&!wa(a))return}else a.iDraw++;if(0!==a.aiDisplay.length){var h=a._iDisplayStart;d=a._iDisplayEnd;a.oFeatures.bServerSide&&(h=0,d=a.aoData.length);for(;h<d;h++){var e=a.aoData[a.aiDisplay[h]];
null===e.nTr&&ca(a,a.aiDisplay[h]);var s=e.nTr;if(0!==f){var m=a.asStripeClasses[g%f];e._sRowStripe!=m&&(i(s).removeClass(e._sRowStripe).addClass(m),e._sRowStripe=m)}C(a,"aoRowCallback",null,[s,a.aoData[a.aiDisplay[h]]._aData,g,h]);b.push(s);g++;if(0!==c)for(e=0;e<c;e++)if(s==a.aoOpenRows[e].nParent){b.push(a.aoOpenRows[e].nTr);break}}}else b[0]=l.createElement("tr"),a.asStripeClasses[0]&&(b[0].className=a.asStripeClasses[0]),c=a.oLanguage,f=c.sZeroRecords,1==a.iDraw&&null!==a.sAjaxSource&&!a.oFeatures.bServerSide?
f=c.sLoadingRecords:c.sEmptyTable&&0===a.fnRecordsTotal()&&(f=c.sEmptyTable),c=l.createElement("td"),c.setAttribute("valign","top"),c.colSpan=v(a),c.className=a.oClasses.sRowEmpty,c.innerHTML=ha(a,f),b[g].appendChild(c);C(a,"aoHeaderCallback","header",[i(a.nTHead).children("tr")[0],Y(a),a._iDisplayStart,a.fnDisplayEnd(),a.aiDisplay]);C(a,"aoFooterCallback","footer",[i(a.nTFoot).children("tr")[0],Y(a),a._iDisplayStart,a.fnDisplayEnd(),a.aiDisplay]);g=l.createDocumentFragment();c=l.createDocumentFragment();
if(a.nTBody){f=a.nTBody.parentNode;c.appendChild(a.nTBody);if(!a.oScroll.bInfinite||!a._bInitComplete||a.bSorted||a.bFiltered)for(;c=a.nTBody.firstChild;)a.nTBody.removeChild(c);c=0;for(d=b.length;c<d;c++)g.appendChild(b[c]);a.nTBody.appendChild(g);null!==f&&f.appendChild(a.nTBody)}C(a,"aoDrawCallback","draw",[a]);a.bSorted=!1;a.bFiltered=!1;a.bDrawing=!1;a.oFeatures.bServerSide&&(F(a,!1),a._bInitComplete||Z(a))}}function $(a){a.oFeatures.bSort?P(a,a.oPreviousSearch):a.oFeatures.bFilter?M(a,a.oPreviousSearch):
(A(a),y(a))}function xa(a){var b=i("<div></div>")[0];a.nTable.parentNode.insertBefore(b,a.nTable);a.nTableWrapper=i('<div id="'+a.sTableId+'_wrapper" class="'+a.oClasses.sWrapper+'" role="grid"></div>')[0];a.nTableReinsertBefore=a.nTable.nextSibling;for(var c=a.nTableWrapper,d=a.sDom.split(""),g,f,h,e,s,m,o,k=0;k<d.length;k++){f=0;h=d[k];if("<"==h){e=i("<div></div>")[0];s=d[k+1];if("'"==s||'"'==s){m="";for(o=2;d[k+o]!=s;)m+=d[k+o],o++;"H"==m?m=a.oClasses.sJUIHeader:"F"==m&&(m=a.oClasses.sJUIFooter);
-1!=m.indexOf(".")?(s=m.split("."),e.id=s[0].substr(1,s[0].length-1),e.className=s[1]):"#"==m.charAt(0)?e.id=m.substr(1,m.length-1):e.className=m;k+=o}c.appendChild(e);c=e}else if(">"==h)c=c.parentNode;else if("l"==h&&a.oFeatures.bPaginate&&a.oFeatures.bLengthChange)g=ya(a),f=1;else if("f"==h&&a.oFeatures.bFilter)g=za(a),f=1;else if("r"==h&&a.oFeatures.bProcessing)g=Aa(a),f=1;else if("t"==h)g=Ba(a),f=1;else if("i"==h&&a.oFeatures.bInfo)g=Ca(a),f=1;else if("p"==h&&a.oFeatures.bPaginate)g=Da(a),f=1;
else if(0!==j.ext.aoFeatures.length){e=j.ext.aoFeatures;o=0;for(s=e.length;o<s;o++)if(h==e[o].cFeature){(g=e[o].fnInit(a))&&(f=1);break}}1==f&&null!==g&&("object"!==typeof a.aanFeatures[h]&&(a.aanFeatures[h]=[]),a.aanFeatures[h].push(g),c.appendChild(g))}b.parentNode.replaceChild(a.nTableWrapper,b)}function T(a,b){var c=i(b).children("tr"),d,g,f,h,e,s,m,j;a.splice(0,a.length);g=0;for(s=c.length;g<s;g++)a.push([]);g=0;for(s=c.length;g<s;g++){f=0;for(m=c[g].childNodes.length;f<m;f++)if(d=c[g].childNodes[f],
"TD"==d.nodeName.toUpperCase()||"TH"==d.nodeName.toUpperCase()){var o=1*d.getAttribute("colspan"),k=1*d.getAttribute("rowspan"),o=!o||0===o||1===o?1:o,k=!k||0===k||1===k?1:k;for(h=0;a[g][h];)h++;j=h;for(e=0;e<o;e++)for(h=0;h<k;h++)a[g+h][j+e]={cell:d,unique:1==o?!0:!1},a[g+h].nTr=c[g]}}}function O(a,b,c){var d=[];c||(c=a.aoHeader,b&&(c=[],T(c,b)));for(var b=0,g=c.length;b<g;b++)for(var f=0,h=c[b].length;f<h;f++)if(c[b][f].unique&&(!d[f]||!a.bSortCellsTop))d[f]=c[b][f].cell;return d}function wa(a){if(a.bAjaxDataGet){a.iDraw++;
F(a,!0);var b=Ea(a);ia(a,b);a.fnServerData.call(a.oInstance,a.sAjaxSource,b,function(b){Fa(a,b)},a);return!1}return!0}function Ea(a){var b=a.aoColumns.length,c=[],d,g,f,h;c.push({name:"sEcho",value:a.iDraw});c.push({name:"iColumns",value:b});c.push({name:"sColumns",value:x(a)});c.push({name:"iDisplayStart",value:a._iDisplayStart});c.push({name:"iDisplayLength",value:!1!==a.oFeatures.bPaginate?a._iDisplayLength:-1});for(f=0;f<b;f++)d=a.aoColumns[f].mDataProp,c.push({name:"mDataProp_"+f,value:"function"===
typeof d?"function":d});if(!1!==a.oFeatures.bFilter){c.push({name:"sSearch",value:a.oPreviousSearch.sSearch});c.push({name:"bRegex",value:a.oPreviousSearch.bRegex});for(f=0;f<b;f++)c.push({name:"sSearch_"+f,value:a.aoPreSearchCols[f].sSearch}),c.push({name:"bRegex_"+f,value:a.aoPreSearchCols[f].bRegex}),c.push({name:"bSearchable_"+f,value:a.aoColumns[f].bSearchable})}if(!1!==a.oFeatures.bSort){var e=0;d=null!==a.aaSortingFixed?a.aaSortingFixed.concat(a.aaSorting):a.aaSorting.slice();for(f=0;f<d.length;f++){g=
a.aoColumns[d[f][0]].aDataSort;for(h=0;h<g.length;h++)c.push({name:"iSortCol_"+e,value:g[h]}),c.push({name:"sSortDir_"+e,value:d[f][1]}),e++}c.push({name:"iSortingCols",value:e});for(f=0;f<b;f++)c.push({name:"bSortable_"+f,value:a.aoColumns[f].bSortable})}return c}function ia(a,b){C(a,"aoServerParams","serverParams",[b])}function Fa(a,b){if(b.sEcho!==n){if(1*b.sEcho<a.iDraw)return;a.iDraw=1*b.sEcho}(!a.oScroll.bInfinite||a.oScroll.bInfinite&&(a.bSorted||a.bFiltered))&&ea(a);a._iRecordsTotal=parseInt(b.iTotalRecords,
10);a._iRecordsDisplay=parseInt(b.iTotalDisplayRecords,10);var c=x(a),c=b.sColumns!==n&&""!==c&&b.sColumns!=c,d;c&&(d=D(a,b.sColumns));for(var g=W(a.sAjaxDataProp)(b),f=0,h=g.length;f<h;f++)if(c){for(var e=[],i=0,m=a.aoColumns.length;i<m;i++)e.push(g[f][d[i]]);H(a,e)}else H(a,g[f]);a.aiDisplay=a.aiDisplayMaster.slice();a.bAjaxDataGet=!1;y(a);a.bAjaxDataGet=!0;F(a,!1)}function za(a){var b=a.oPreviousSearch,c=a.oLanguage.sSearch,c=-1!==c.indexOf("_INPUT_")?c.replace("_INPUT_",'<input type="text" />'):
""===c?'<input type="text" />':c+' <input type="text" />',d=l.createElement("div");d.className=a.oClasses.sFilter;d.innerHTML="<label>"+c+"</label>";a.aanFeatures.f||(d.id=a.sTableId+"_filter");c=i('input[type="text"]',d);d._DT_Input=c[0];c.val(b.sSearch.replace('"',"&quot;"));c.bind("keyup.DT",function(){for(var c=a.aanFeatures.f,d=this.value===""?"":this.value,h=0,e=c.length;h<e;h++)c[h]!=i(this).parents("div.dataTables_filter")[0]&&i(c[h]._DT_Input).val(d);d!=b.sSearch&&M(a,{sSearch:d,bRegex:b.bRegex,
bSmart:b.bSmart,bCaseInsensitive:b.bCaseInsensitive})});c.attr("aria-controls",a.sTableId).bind("keypress.DT",function(a){if(a.keyCode==13)return false});return d}function M(a,b,c){var d=a.oPreviousSearch,g=a.aoPreSearchCols,f=function(a){d.sSearch=a.sSearch;d.bRegex=a.bRegex;d.bSmart=a.bSmart;d.bCaseInsensitive=a.bCaseInsensitive};if(a.oFeatures.bServerSide)f(b);else{Ga(a,b.sSearch,c,b.bRegex,b.bSmart,b.bCaseInsensitive);f(b);for(b=0;b<a.aoPreSearchCols.length;b++)Ha(a,g[b].sSearch,b,g[b].bRegex,
g[b].bSmart,g[b].bCaseInsensitive);Ia(a)}a.bFiltered=!0;i(a.oInstance).trigger("filter",a);a._iDisplayStart=0;A(a);y(a);ja(a,0)}function Ia(a){for(var b=j.ext.afnFiltering,c=0,d=b.length;c<d;c++)for(var g=0,f=0,h=a.aiDisplay.length;f<h;f++){var e=a.aiDisplay[f-g];b[c](a,X(a,e,"filter"),e)||(a.aiDisplay.splice(f-g,1),g++)}}function Ha(a,b,c,d,g,f){if(""!==b)for(var h=0,b=ka(b,d,g,f),d=a.aiDisplay.length-1;0<=d;d--)g=la(w(a,a.aiDisplay[d],c,"filter"),a.aoColumns[c].sType),b.test(g)||(a.aiDisplay.splice(d,
1),h++)}function Ga(a,b,c,d,g,f){d=ka(b,d,g,f);g=a.oPreviousSearch;c||(c=0);0!==j.ext.afnFiltering.length&&(c=1);if(0>=b.length)a.aiDisplay.splice(0,a.aiDisplay.length),a.aiDisplay=a.aiDisplayMaster.slice();else if(a.aiDisplay.length==a.aiDisplayMaster.length||g.sSearch.length>b.length||1==c||0!==b.indexOf(g.sSearch)){a.aiDisplay.splice(0,a.aiDisplay.length);ja(a,1);for(b=0;b<a.aiDisplayMaster.length;b++)d.test(a.asDataSearch[b])&&a.aiDisplay.push(a.aiDisplayMaster[b])}else for(b=c=0;b<a.asDataSearch.length;b++)d.test(a.asDataSearch[b])||
(a.aiDisplay.splice(b-c,1),c++)}function ja(a,b){if(!a.oFeatures.bServerSide){a.asDataSearch.splice(0,a.asDataSearch.length);for(var c=b&&1===b?a.aiDisplayMaster:a.aiDisplay,d=0,g=c.length;d<g;d++)a.asDataSearch[d]=ma(a,X(a,c[d],"filter"))}}function ma(a,b){var c="";a.__nTmpFilter===n&&(a.__nTmpFilter=l.createElement("div"));for(var d=a.__nTmpFilter,g=0,f=a.aoColumns.length;g<f;g++)a.aoColumns[g].bSearchable&&(c+=la(b[g],a.aoColumns[g].sType)+"  ");-1!==c.indexOf("&")&&(d.innerHTML=c,c=d.textContent?
d.textContent:d.innerText,c=c.replace(/\n/g," ").replace(/\r/g,""));return c}function ka(a,b,c,d){if(c)return a=b?a.split(" "):na(a).split(" "),a="^(?=.*?"+a.join(")(?=.*?")+").*$",RegExp(a,d?"i":"");a=b?a:na(a);return RegExp(a,d?"i":"")}function la(a,b){return"function"===typeof j.ext.ofnSearch[b]?j.ext.ofnSearch[b](a):null===a?"":"html"==b?a.replace(/[\r\n]/g," ").replace(/<.*?>/g,""):"string"===typeof a?a.replace(/[\r\n]/g," "):a}function na(a){return a.replace(RegExp("(\\/|\\.|\\*|\\+|\\?|\\||\\(|\\)|\\[|\\]|\\{|\\}|\\\\|\\$|\\^|\\-)",
"g"),"\\$1")}function Ca(a){var b=l.createElement("div");b.className=a.oClasses.sInfo;a.aanFeatures.i||(a.aoDrawCallback.push({fn:Ja,sName:"information"}),b.id=a.sTableId+"_info");a.nTable.setAttribute("aria-describedby",a.sTableId+"_info");return b}function Ja(a){if(a.oFeatures.bInfo&&0!==a.aanFeatures.i.length){var b=a.oLanguage,c=a._iDisplayStart+1,d=a.fnDisplayEnd(),g=a.fnRecordsTotal(),f=a.fnRecordsDisplay(),h;h=0===f&&f==g?b.sInfoEmpty:0===f?b.sInfoEmpty+" "+b.sInfoFiltered:f==g?b.sInfo:b.sInfo+
" "+b.sInfoFiltered;h+=b.sInfoPostFix;h=ha(a,h);null!==b.fnInfoCallback&&(h=b.fnInfoCallback.call(a.oInstance,a,c,d,g,f,h));a=a.aanFeatures.i;b=0;for(c=a.length;b<c;b++)i(a[b]).html(h)}}function ha(a,b){var c=a.fnFormatNumber(a._iDisplayStart+1),d=a.fnDisplayEnd(),d=a.fnFormatNumber(d),g=a.fnRecordsDisplay(),g=a.fnFormatNumber(g),f=a.fnRecordsTotal(),f=a.fnFormatNumber(f);a.oScroll.bInfinite&&(c=a.fnFormatNumber(1));return b.replace("_START_",c).replace("_END_",d).replace("_TOTAL_",g).replace("_MAX_",
f)}function aa(a){var b,c,d=a.iInitDisplayStart;if(!1===a.bInitialised)setTimeout(function(){aa(a)},200);else{xa(a);va(a);U(a,a.aoHeader);a.nTFoot&&U(a,a.aoFooter);F(a,!0);a.oFeatures.bAutoWidth&&ba(a);b=0;for(c=a.aoColumns.length;b<c;b++)null!==a.aoColumns[b].sWidth&&(a.aoColumns[b].nTh.style.width=q(a.aoColumns[b].sWidth));a.oFeatures.bSort?P(a):a.oFeatures.bFilter?M(a,a.oPreviousSearch):(a.aiDisplay=a.aiDisplayMaster.slice(),A(a),y(a));null!==a.sAjaxSource&&!a.oFeatures.bServerSide?(c=[],ia(a,
c),a.fnServerData.call(a.oInstance,a.sAjaxSource,c,function(c){var f=a.sAjaxDataProp!==""?W(a.sAjaxDataProp)(c):c;for(b=0;b<f.length;b++)H(a,f[b]);a.iInitDisplayStart=d;if(a.oFeatures.bSort)P(a);else{a.aiDisplay=a.aiDisplayMaster.slice();A(a);y(a)}F(a,false);Z(a,c)},a)):a.oFeatures.bServerSide||(F(a,!1),Z(a))}}function Z(a,b){a._bInitComplete=!0;C(a,"aoInitComplete","init",[a,b])}function oa(a){var b=j.defaults.oLanguage;!a.sEmptyTable&&(a.sZeroRecords&&"No data available in table"===b.sEmptyTable)&&
p(a,a,"sZeroRecords","sEmptyTable");!a.sLoadingRecords&&(a.sZeroRecords&&"Loading..."===b.sLoadingRecords)&&p(a,a,"sZeroRecords","sLoadingRecords")}function ya(a){if(a.oScroll.bInfinite)return null;var b='<select size="1" '+('name="'+a.sTableId+'_length"')+">",c,d,g=a.aLengthMenu;if(2==g.length&&"object"===typeof g[0]&&"object"===typeof g[1]){c=0;for(d=g[0].length;c<d;c++)b+='<option value="'+g[0][c]+'">'+g[1][c]+"</option>"}else{c=0;for(d=g.length;c<d;c++)b+='<option value="'+g[c]+'">'+g[c]+"</option>"}b+=
"</select>";g=l.createElement("div");a.aanFeatures.l||(g.id=a.sTableId+"_length");g.className=a.oClasses.sLength;g.innerHTML="<label>"+a.oLanguage.sLengthMenu.replace("_MENU_",b)+"</label>";i('select option[value="'+a._iDisplayLength+'"]',g).attr("selected",!0);i("select",g).bind("change.DT",function(){var b=i(this).val(),g=a.aanFeatures.l;c=0;for(d=g.length;c<d;c++)g[c]!=this.parentNode&&i("select",g[c]).val(b);a._iDisplayLength=parseInt(b,10);A(a);if(a.fnDisplayEnd()==a.fnRecordsDisplay()){a._iDisplayStart=
a.fnDisplayEnd()-a._iDisplayLength;if(a._iDisplayStart<0)a._iDisplayStart=0}if(a._iDisplayLength==-1)a._iDisplayStart=0;y(a)});i("select",g).attr("aria-controls",a.sTableId);return g}function A(a){a._iDisplayEnd=!1===a.oFeatures.bPaginate?a.aiDisplay.length:a._iDisplayStart+a._iDisplayLength>a.aiDisplay.length||-1==a._iDisplayLength?a.aiDisplay.length:a._iDisplayStart+a._iDisplayLength}function Da(a){if(a.oScroll.bInfinite)return null;var b=l.createElement("div");b.className=a.oClasses.sPaging+a.sPaginationType;
j.ext.oPagination[a.sPaginationType].fnInit(a,b,function(a){A(a);y(a)});a.aanFeatures.p||a.aoDrawCallback.push({fn:function(a){j.ext.oPagination[a.sPaginationType].fnUpdate(a,function(a){A(a);y(a)})},sName:"pagination"});return b}function pa(a,b){var c=a._iDisplayStart;if("number"===typeof b)a._iDisplayStart=b*a._iDisplayLength,a._iDisplayStart>a.fnRecordsDisplay()&&(a._iDisplayStart=0);else if("first"==b)a._iDisplayStart=0;else if("previous"==b)a._iDisplayStart=0<=a._iDisplayLength?a._iDisplayStart-
a._iDisplayLength:0,0>a._iDisplayStart&&(a._iDisplayStart=0);else if("next"==b)0<=a._iDisplayLength?a._iDisplayStart+a._iDisplayLength<a.fnRecordsDisplay()&&(a._iDisplayStart+=a._iDisplayLength):a._iDisplayStart=0;else if("last"==b)if(0<=a._iDisplayLength){var d=parseInt((a.fnRecordsDisplay()-1)/a._iDisplayLength,10)+1;a._iDisplayStart=(d-1)*a._iDisplayLength}else a._iDisplayStart=0;else E(a,0,"Unknown paging action: "+b);i(a.oInstance).trigger("page",a);return c!=a._iDisplayStart}function Aa(a){var b=
l.createElement("div");a.aanFeatures.r||(b.id=a.sTableId+"_processing");b.innerHTML=a.oLanguage.sProcessing;b.className=a.oClasses.sProcessing;a.nTable.parentNode.insertBefore(b,a.nTable);return b}function F(a,b){if(a.oFeatures.bProcessing)for(var c=a.aanFeatures.r,d=0,g=c.length;d<g;d++)c[d].style.visibility=b?"visible":"hidden";i(a.oInstance).trigger("processing",[a,b])}function Ba(a){if(""===a.oScroll.sX&&""===a.oScroll.sY)return a.nTable;var b=l.createElement("div"),c=l.createElement("div"),d=
l.createElement("div"),g=l.createElement("div"),f=l.createElement("div"),h=l.createElement("div"),e=a.nTable.cloneNode(!1),j=a.nTable.cloneNode(!1),m=a.nTable.getElementsByTagName("thead")[0],o=0===a.nTable.getElementsByTagName("tfoot").length?null:a.nTable.getElementsByTagName("tfoot")[0],k=a.oClasses;c.appendChild(d);f.appendChild(h);g.appendChild(a.nTable);b.appendChild(c);b.appendChild(g);d.appendChild(e);e.appendChild(m);null!==o&&(b.appendChild(f),h.appendChild(j),j.appendChild(o));b.className=
k.sScrollWrapper;c.className=k.sScrollHead;d.className=k.sScrollHeadInner;g.className=k.sScrollBody;f.className=k.sScrollFoot;h.className=k.sScrollFootInner;a.oScroll.bAutoCss&&(c.style.overflow="hidden",c.style.position="relative",f.style.overflow="hidden",g.style.overflow="auto");c.style.border="0";c.style.width="100%";f.style.border="0";d.style.width=""!==a.oScroll.sXInner?a.oScroll.sXInner:"100%";e.removeAttribute("id");e.style.marginLeft="0";a.nTable.style.marginLeft="0";null!==o&&(j.removeAttribute("id"),
j.style.marginLeft="0");d=i(a.nTable).children("caption");0<d.length&&(d=d[0],"top"===d._captionSide?e.appendChild(d):"bottom"===d._captionSide&&o&&j.appendChild(d));""!==a.oScroll.sX&&(c.style.width=q(a.oScroll.sX),g.style.width=q(a.oScroll.sX),null!==o&&(f.style.width=q(a.oScroll.sX)),i(g).scroll(function(){c.scrollLeft=this.scrollLeft;if(o!==null)f.scrollLeft=this.scrollLeft}));""!==a.oScroll.sY&&(g.style.height=q(a.oScroll.sY));a.aoDrawCallback.push({fn:Ka,sName:"scrolling"});a.oScroll.bInfinite&&
i(g).scroll(function(){if(!a.bDrawing&&i(this).scrollTop()!==0&&i(this).scrollTop()+i(this).height()>i(a.nTable).height()-a.oScroll.iLoadGap&&a.fnDisplayEnd()<a.fnRecordsDisplay()){pa(a,"next");A(a);y(a)}});a.nScrollHead=c;a.nScrollFoot=f;return b}function Ka(a){var b=a.nScrollHead.getElementsByTagName("div")[0],c=b.getElementsByTagName("table")[0],d=a.nTable.parentNode,g,f,h,e,j,m,o,k,n=[],r=null!==a.nTFoot?a.nScrollFoot.getElementsByTagName("div")[0]:null,p=null!==a.nTFoot?r.getElementsByTagName("table")[0]:
null,l=i.browser.msie&&7>=i.browser.version;i(a.nTable).children("thead, tfoot").remove();h=i(a.nTHead).clone()[0];a.nTable.insertBefore(h,a.nTable.childNodes[0]);null!==a.nTFoot&&(j=i(a.nTFoot).clone()[0],a.nTable.insertBefore(j,a.nTable.childNodes[1]));""===a.oScroll.sX&&(d.style.width="100%",b.parentNode.style.width="100%");var t=O(a,h);g=0;for(f=t.length;g<f;g++)o=G(a,g),t[g].style.width=a.aoColumns[o].sWidth;null!==a.nTFoot&&N(function(a){a.style.width=""},j.getElementsByTagName("tr"));a.oScroll.bCollapse&&
""!==a.oScroll.sY&&(d.style.height=d.offsetHeight+a.nTHead.offsetHeight+"px");g=i(a.nTable).outerWidth();if(""===a.oScroll.sX){if(a.nTable.style.width="100%",l&&(i("tbody",d).height()>d.offsetHeight||"scroll"==i(d).css("overflow-y")))a.nTable.style.width=q(i(a.nTable).outerWidth()-a.oScroll.iBarWidth)}else""!==a.oScroll.sXInner?a.nTable.style.width=q(a.oScroll.sXInner):g==i(d).width()&&i(d).height()<i(a.nTable).height()?(a.nTable.style.width=q(g-a.oScroll.iBarWidth),i(a.nTable).outerWidth()>g-a.oScroll.iBarWidth&&
(a.nTable.style.width=q(g))):a.nTable.style.width=q(g);g=i(a.nTable).outerWidth();f=a.nTHead.getElementsByTagName("tr");h=h.getElementsByTagName("tr");N(function(a,b){m=a.style;m.paddingTop="0";m.paddingBottom="0";m.borderTopWidth="0";m.borderBottomWidth="0";m.height=0;k=i(a).width();b.style.width=q(k);n.push(k)},h,f);i(h).height(0);null!==a.nTFoot&&(e=j.getElementsByTagName("tr"),j=a.nTFoot.getElementsByTagName("tr"),N(function(a,b){m=a.style;m.paddingTop="0";m.paddingBottom="0";m.borderTopWidth=
"0";m.borderBottomWidth="0";m.height=0;k=i(a).width();b.style.width=q(k);n.push(k)},e,j),i(e).height(0));N(function(a){a.innerHTML="";a.style.width=q(n.shift())},h);null!==a.nTFoot&&N(function(a){a.innerHTML="";a.style.width=q(n.shift())},e);if(i(a.nTable).outerWidth()<g){e=d.scrollHeight>d.offsetHeight||"scroll"==i(d).css("overflow-y")?g+a.oScroll.iBarWidth:g;if(l&&(d.scrollHeight>d.offsetHeight||"scroll"==i(d).css("overflow-y")))a.nTable.style.width=q(e-a.oScroll.iBarWidth);d.style.width=q(e);b.parentNode.style.width=
q(e);null!==a.nTFoot&&(r.parentNode.style.width=q(e));""===a.oScroll.sX?E(a,1,"The table cannot fit into the current element which will cause column misalignment. The table has been drawn at its minimum possible width."):""!==a.oScroll.sXInner&&E(a,1,"The table cannot fit into the current element which will cause column misalignment. Increase the sScrollXInner value or remove it to allow automatic calculation")}else d.style.width=q("100%"),b.parentNode.style.width=q("100%"),null!==a.nTFoot&&(r.parentNode.style.width=
q("100%"));""===a.oScroll.sY&&l&&(d.style.height=q(a.nTable.offsetHeight+a.oScroll.iBarWidth));""!==a.oScroll.sY&&a.oScroll.bCollapse&&(d.style.height=q(a.oScroll.sY),l=""!==a.oScroll.sX&&a.nTable.offsetWidth>d.offsetWidth?a.oScroll.iBarWidth:0,a.nTable.offsetHeight<d.offsetHeight&&(d.style.height=q(a.nTable.offsetHeight+l)));l=i(a.nTable).outerWidth();c.style.width=q(l);b.style.width=q(l);c=i(a.nTable).height()>d.clientHeight||"scroll"==i(d).css("overflow-y");b.style.paddingRight=c?a.oScroll.iBarWidth+
"px":"0px";null!==a.nTFoot&&(p.style.width=q(l),r.style.width=q(l),r.style.paddingRight=c?a.oScroll.iBarWidth+"px":"0px");i(d).scroll();if(a.bSorted||a.bFiltered)d.scrollTop=0}function N(a,b,c){for(var d=0,g=b.length;d<g;d++)for(var f=0,h=b[d].childNodes.length;f<h;f++)1==b[d].childNodes[f].nodeType&&(c?a(b[d].childNodes[f],c[d].childNodes[f]):a(b[d].childNodes[f]))}function La(a,b){if(!a||null===a||""===a)return 0;b||(b=l.getElementsByTagName("body")[0]);var c,d=l.createElement("div");d.style.width=
q(a);b.appendChild(d);c=d.offsetWidth;b.removeChild(d);return c}function ba(a){var b=0,c,d=0,g=a.aoColumns.length,f,h=i("th",a.nTHead),e=a.nTable.getAttribute("width");for(f=0;f<g;f++)a.aoColumns[f].bVisible&&(d++,null!==a.aoColumns[f].sWidth&&(c=La(a.aoColumns[f].sWidthOrig,a.nTable.parentNode),null!==c&&(a.aoColumns[f].sWidth=q(c)),b++));if(g==h.length&&0===b&&d==g&&""===a.oScroll.sX&&""===a.oScroll.sY)for(f=0;f<a.aoColumns.length;f++)c=i(h[f]).width(),null!==c&&(a.aoColumns[f].sWidth=q(c));else{b=
a.nTable.cloneNode(!1);f=a.nTHead.cloneNode(!0);d=l.createElement("tbody");c=l.createElement("tr");b.removeAttribute("id");b.appendChild(f);null!==a.nTFoot&&(b.appendChild(a.nTFoot.cloneNode(!0)),N(function(a){a.style.width=""},b.getElementsByTagName("tr")));b.appendChild(d);d.appendChild(c);d=i("thead th",b);0===d.length&&(d=i("tbody tr:eq(0)>td",b));h=O(a,f);for(f=d=0;f<g;f++){var j=a.aoColumns[f];j.bVisible&&null!==j.sWidthOrig&&""!==j.sWidthOrig?h[f-d].style.width=q(j.sWidthOrig):j.bVisible?h[f-
d].style.width="":d++}for(f=0;f<g;f++)a.aoColumns[f].bVisible&&(d=Ma(a,f),null!==d&&(d=d.cloneNode(!0),""!==a.aoColumns[f].sContentPadding&&(d.innerHTML+=a.aoColumns[f].sContentPadding),c.appendChild(d)));g=a.nTable.parentNode;g.appendChild(b);""!==a.oScroll.sX&&""!==a.oScroll.sXInner?b.style.width=q(a.oScroll.sXInner):""!==a.oScroll.sX?(b.style.width="",i(b).width()<g.offsetWidth&&(b.style.width=q(g.offsetWidth))):""!==a.oScroll.sY?b.style.width=q(g.offsetWidth):e&&(b.style.width=q(e));b.style.visibility=
"hidden";Na(a,b);g=i("tbody tr:eq(0)",b).children();0===g.length&&(g=O(a,i("thead",b)[0]));if(""!==a.oScroll.sX){for(f=d=c=0;f<a.aoColumns.length;f++)a.aoColumns[f].bVisible&&(c=null===a.aoColumns[f].sWidthOrig?c+i(g[d]).outerWidth():c+(parseInt(a.aoColumns[f].sWidth.replace("px",""),10)+(i(g[d]).outerWidth()-i(g[d]).width())),d++);b.style.width=q(c);a.nTable.style.width=q(c)}for(f=d=0;f<a.aoColumns.length;f++)a.aoColumns[f].bVisible&&(c=i(g[d]).width(),null!==c&&0<c&&(a.aoColumns[f].sWidth=q(c)),
d++);g=i(b).css("width");a.nTable.style.width=-1!==g.indexOf("%")?g:q(i(b).outerWidth());b.parentNode.removeChild(b)}e&&(a.nTable.style.width=q(e))}function Na(a,b){""===a.oScroll.sX&&""!==a.oScroll.sY?(i(b).width(),b.style.width=q(i(b).outerWidth()-a.oScroll.iBarWidth)):""!==a.oScroll.sX&&(b.style.width=q(i(b).outerWidth()))}function Ma(a,b){var c=Oa(a,b);if(0>c)return null;if(null===a.aoData[c].nTr){var d=l.createElement("td");d.innerHTML=w(a,c,b,"");return d}return L(a,c)[b]}function Oa(a,b){for(var c=
-1,d=-1,g=0;g<a.aoData.length;g++){var f=w(a,g,b,"display")+"",f=f.replace(/<.*?>/g,"");f.length>c&&(c=f.length,d=g)}return d}function q(a){if(null===a)return"0px";if("number"==typeof a)return 0>a?"0px":a+"px";var b=a.charCodeAt(a.length-1);return 48>b||57<b?a:a+"px"}function Pa(){var a=l.createElement("p"),b=a.style;b.width="100%";b.height="200px";b.padding="0px";var c=l.createElement("div"),b=c.style;b.position="absolute";b.top="0px";b.left="0px";b.visibility="hidden";b.width="200px";b.height="150px";
b.padding="0px";b.overflow="hidden";c.appendChild(a);l.body.appendChild(c);b=a.offsetWidth;c.style.overflow="scroll";a=a.offsetWidth;b==a&&(a=c.clientWidth);l.body.removeChild(c);return b-a}function P(a,b){var c,d,g,f,h,e,o=[],m=[],k=j.ext.oSort,r=a.aoData,l=a.aoColumns,p=a.oLanguage.oAria;if(!a.oFeatures.bServerSide&&(0!==a.aaSorting.length||null!==a.aaSortingFixed)){o=null!==a.aaSortingFixed?a.aaSortingFixed.concat(a.aaSorting):a.aaSorting.slice();for(c=0;c<o.length;c++)if(d=o[c][0],g=t(a,d),f=
a.aoColumns[d].sSortDataType,j.ext.afnSortData[f])if(h=j.ext.afnSortData[f].call(a.oInstance,a,d,g),h.length===r.length){g=0;for(f=r.length;g<f;g++)I(a,g,d,h[g])}else E(a,0,"Returned data sort array (col "+d+") is the wrong length");c=0;for(d=a.aiDisplayMaster.length;c<d;c++)m[a.aiDisplayMaster[c]]=c;var q=o.length,G;c=0;for(d=r.length;c<d;c++)for(g=0;g<q;g++){G=l[o[g][0]].aDataSort;h=0;for(e=G.length;h<e;h++)f=l[G[h]].sType,f=k[(f?f:"string")+"-pre"],r[c]._aSortData[G[h]]=f?f(w(a,c,G[h],"sort")):
w(a,c,G[h],"sort")}a.aiDisplayMaster.sort(function(a,b){var c,d,g,f,h;for(c=0;c<q;c++){h=l[o[c][0]].aDataSort;d=0;for(g=h.length;d<g;d++)if(f=l[h[d]].sType,f=k[(f?f:"string")+"-"+o[c][1]](r[a]._aSortData[h[d]],r[b]._aSortData[h[d]]),0!==f)return f}return k["numeric-asc"](m[a],m[b])})}(b===n||b)&&!a.oFeatures.bDeferRender&&Q(a);c=0;for(d=a.aoColumns.length;c<d;c++)f=l[c].sTitle.replace(/<.*?>/g,""),g=l[c].nTh,g.removeAttribute("aria-sort"),g.removeAttribute("aria-label"),l[c].bSortable?0<o.length&&
o[0][0]==c?(g.setAttribute("aria-sort","asc"==o[0][1]?"ascending":"descending"),g.setAttribute("aria-label",f+("asc"==(l[c].asSorting[o[0][2]+1]?l[c].asSorting[o[0][2]+1]:l[c].asSorting[0])?p.sSortAscending:p.sSortDescending))):g.setAttribute("aria-label",f+("asc"==l[c].asSorting[0]?p.sSortAscending:p.sSortDescending)):g.setAttribute("aria-label",f);a.bSorted=!0;i(a.oInstance).trigger("sort",a);a.oFeatures.bFilter?M(a,a.oPreviousSearch,1):(a.aiDisplay=a.aiDisplayMaster.slice(),a._iDisplayStart=0,
A(a),y(a))}function ga(a,b,c,d){Qa(b,{},function(b){if(!1!==a.aoColumns[c].bSortable){var f=function(){var d,f;if(b.shiftKey){for(var e=!1,i=0;i<a.aaSorting.length;i++)if(a.aaSorting[i][0]==c){e=!0;d=a.aaSorting[i][0];f=a.aaSorting[i][2]+1;a.aoColumns[d].asSorting[f]?(a.aaSorting[i][1]=a.aoColumns[d].asSorting[f],a.aaSorting[i][2]=f):a.aaSorting.splice(i,1);break}!1===e&&a.aaSorting.push([c,a.aoColumns[c].asSorting[0],0])}else 1==a.aaSorting.length&&a.aaSorting[0][0]==c?(d=a.aaSorting[0][0],f=a.aaSorting[0][2]+
1,a.aoColumns[d].asSorting[f]||(f=0),a.aaSorting[0][1]=a.aoColumns[d].asSorting[f],a.aaSorting[0][2]=f):(a.aaSorting.splice(0,a.aaSorting.length),a.aaSorting.push([c,a.aoColumns[c].asSorting[0],0]));P(a)};a.oFeatures.bProcessing?(F(a,!0),setTimeout(function(){f();a.oFeatures.bServerSide||F(a,!1)},0)):f();"function"==typeof d&&d(a)}})}function Q(a){var b,c,d,g,f,h=a.aoColumns.length,e=a.oClasses;for(b=0;b<h;b++)a.aoColumns[b].bSortable&&i(a.aoColumns[b].nTh).removeClass(e.sSortAsc+" "+e.sSortDesc+
" "+a.aoColumns[b].sSortingClass);g=null!==a.aaSortingFixed?a.aaSortingFixed.concat(a.aaSorting):a.aaSorting.slice();for(b=0;b<a.aoColumns.length;b++)if(a.aoColumns[b].bSortable){f=a.aoColumns[b].sSortingClass;d=-1;for(c=0;c<g.length;c++)if(g[c][0]==b){f="asc"==g[c][1]?e.sSortAsc:e.sSortDesc;d=c;break}i(a.aoColumns[b].nTh).addClass(f);a.bJUI&&(c=i("span."+e.sSortIcon,a.aoColumns[b].nTh),c.removeClass(e.sSortJUIAsc+" "+e.sSortJUIDesc+" "+e.sSortJUI+" "+e.sSortJUIAscAllowed+" "+e.sSortJUIDescAllowed),
c.addClass(-1==d?a.aoColumns[b].sSortingClassJUI:"asc"==g[d][1]?e.sSortJUIAsc:e.sSortJUIDesc))}else i(a.aoColumns[b].nTh).addClass(a.aoColumns[b].sSortingClass);f=e.sSortColumn;if(a.oFeatures.bSort&&a.oFeatures.bSortClasses){d=L(a);if(a.oFeatures.bDeferRender)i(d).removeClass(f+"1 "+f+"2 "+f+"3");else if(d.length>=h)for(b=0;b<h;b++)if(-1!=d[b].className.indexOf(f+"1")){c=0;for(a=d.length/h;c<a;c++)d[h*c+b].className=i.trim(d[h*c+b].className.replace(f+"1",""))}else if(-1!=d[b].className.indexOf(f+
"2")){c=0;for(a=d.length/h;c<a;c++)d[h*c+b].className=i.trim(d[h*c+b].className.replace(f+"2",""))}else if(-1!=d[b].className.indexOf(f+"3")){c=0;for(a=d.length/h;c<a;c++)d[h*c+b].className=i.trim(d[h*c+b].className.replace(" "+f+"3",""))}var e=1,j;for(b=0;b<g.length;b++){j=parseInt(g[b][0],10);c=0;for(a=d.length/h;c<a;c++)d[h*c+j].className+=" "+f+e;3>e&&e++}}}function qa(a){if(a.oFeatures.bStateSave&&!a.bDestroying){var b,c;b=a.oScroll.bInfinite;var d={iCreate:(new Date).getTime(),iStart:b?0:a._iDisplayStart,
iEnd:b?a._iDisplayLength:a._iDisplayEnd,iLength:a._iDisplayLength,aaSorting:i.extend(!0,[],a.aaSorting),oSearch:i.extend(!0,{},a.oPreviousSearch),aoSearchCols:i.extend(!0,[],a.aoPreSearchCols),abVisCols:[]};b=0;for(c=a.aoColumns.length;b<c;b++)d.abVisCols.push(a.aoColumns[b].bVisible);C(a,"aoStateSaveParams","stateSaveParams",[a,d]);a.fnStateSave.call(a.oInstance,a,d)}}function Ra(a,b){if(a.oFeatures.bStateSave){var c=a.fnStateLoad.call(a.oInstance,a);if(c){var d=C(a,"aoStateLoadParams","stateLoadParams",
[a,c]);if(-1===i.inArray(!1,d)){a.oLoadedState=i.extend(!0,{},c);a._iDisplayStart=c.iStart;a.iInitDisplayStart=c.iStart;a._iDisplayEnd=c.iEnd;a._iDisplayLength=c.iLength;a.aaSorting=c.aaSorting.slice();a.saved_aaSorting=c.aaSorting.slice();i.extend(a.oPreviousSearch,c.oSearch);i.extend(!0,a.aoPreSearchCols,c.aoSearchCols);b.saved_aoColumns=[];for(d=0;d<c.abVisCols.length;d++)b.saved_aoColumns[d]={},b.saved_aoColumns[d].bVisible=c.abVisCols[d];C(a,"aoStateLoaded","stateLoaded",[a,c])}}}}function Sa(a){for(var b=
V.location.pathname.split("/"),a=a+"_"+b[b.length-1].replace(/[\/:]/g,"").toLowerCase()+"=",b=l.cookie.split(";"),c=0;c<b.length;c++){for(var d=b[c];" "==d.charAt(0);)d=d.substring(1,d.length);if(0===d.indexOf(a))return decodeURIComponent(d.substring(a.length,d.length))}return null}function u(a){for(var b=0;b<j.settings.length;b++)if(j.settings[b].nTable===a)return j.settings[b];return null}function S(a){for(var b=[],a=a.aoData,c=0,d=a.length;c<d;c++)null!==a[c].nTr&&b.push(a[c].nTr);return b}function L(a,
b){var c=[],d,g,f,e,i,j;g=0;var o=a.aoData.length;b!==n&&(g=b,o=b+1);for(f=g;f<o;f++)if(j=a.aoData[f],null!==j.nTr){g=[];e=0;for(i=j.nTr.childNodes.length;e<i;e++)d=j.nTr.childNodes[e].nodeName.toLowerCase(),("td"==d||"th"==d)&&g.push(j.nTr.childNodes[e]);e=d=0;for(i=a.aoColumns.length;e<i;e++)a.aoColumns[e].bVisible?c.push(g[e-d]):(c.push(j._anHidden[e]),d++)}return c}function E(a,b,c){a=null===a?"DataTables warning: "+c:"DataTables warning (table id = '"+a.sTableId+"'): "+c;if(0===b)if("alert"==
j.ext.sErrMode)alert(a);else throw Error(a);else V.console&&console.log&&console.log(a)}function p(a,b,c,d){d===n&&(d=c);b[c]!==n&&(a[d]=b[c])}function Ta(a,b){for(var c in b)b.hasOwnProperty(c)&&("object"===typeof e[c]&&!1===i.isArray(b[c])?i.extend(!0,a[c],b[c]):a[c]=b[c]);return a}function Qa(a,b,c){i(a).bind("click.DT",b,function(b){a.blur();c(b)}).bind("keypress.DT",b,function(a){13===a.which&&c(a)}).bind("selectstart.DT",function(){return!1})}function B(a,b,c,d){c&&a[b].push({fn:c,sName:d})}
function C(a,b,c,d){for(var b=a[b],g=[],f=b.length-1;0<=f;f--)g.push(b[f].fn.apply(a.oInstance,d));null!==c&&i(a.oInstance).trigger(c,d);return g}function Ua(a){return function(){var b=[u(this[j.ext.iApiIndex])].concat(Array.prototype.slice.call(arguments));return j.ext.oApi[a].apply(this,b)}}var Va=V.JSON?JSON.stringify:function(a){var b=typeof a;if("object"!==b||null===a)return"string"===b&&(a='"'+a+'"'),a+"";var c,d,g=[],f=i.isArray(a);for(c in a)d=a[c],b=typeof d,"string"===b?d='"'+d+'"':"object"===
b&&null!==d&&(d=Va(d)),g.push((f?"":'"'+c+'":')+d);return(f?"[":"{")+g+(f?"]":"}")};this.$=function(a,b){var c,d,g=[],f;d=u(this[j.ext.iApiIndex]);var e=d.aoData,o=d.aiDisplay,k=d.aiDisplayMaster;b||(b={});b=i.extend({},{filter:"none",order:"current",page:"all"},b);if("current"==b.page){c=d._iDisplayStart;for(d=d.fnDisplayEnd();c<d;c++)(f=e[o[c]].nTr)&&g.push(f)}else if("current"==b.order&&"none"==b.filter){c=0;for(d=k.length;c<d;c++)(f=e[k[c]].nTr)&&g.push(f)}else if("current"==b.order&&"applied"==
b.filter){c=0;for(d=o.length;c<d;c++)(f=e[o[c]].nTr)&&g.push(f)}else if("original"==b.order&&"none"==b.filter){c=0;for(d=e.length;c<d;c++)(f=e[c].nTr)&&g.push(f)}else if("original"==b.order&&"applied"==b.filter){c=0;for(d=e.length;c<d;c++)f=e[c].nTr,-1!==i.inArray(c,o)&&f&&g.push(f)}else E(d,1,"Unknown selection options");g=i(g);c=g.filter(a);g=g.find(a);return i([].concat(i.makeArray(c),i.makeArray(g)))};this._=function(a,b){var c=[],d,g,e=this.$(a,b);d=0;for(g=e.length;d<g;d++)c.push(this.fnGetData(e[d]));
return c};this.fnAddData=function(a,b){if(0===a.length)return[];var c=[],d,g=u(this[j.ext.iApiIndex]);if("object"===typeof a[0]&&null!==a[0])for(var e=0;e<a.length;e++){d=H(g,a[e]);if(-1==d)return c;c.push(d)}else{d=H(g,a);if(-1==d)return c;c.push(d)}g.aiDisplay=g.aiDisplayMaster.slice();(b===n||b)&&$(g);return c};this.fnAdjustColumnSizing=function(a){var b=u(this[j.ext.iApiIndex]);k(b);a===n||a?this.fnDraw(!1):(""!==b.oScroll.sX||""!==b.oScroll.sY)&&this.oApi._fnScrollDraw(b)};this.fnClearTable=
function(a){var b=u(this[j.ext.iApiIndex]);ea(b);(a===n||a)&&y(b)};this.fnClose=function(a){for(var b=u(this[j.ext.iApiIndex]),c=0;c<b.aoOpenRows.length;c++)if(b.aoOpenRows[c].nParent==a)return(a=b.aoOpenRows[c].nTr.parentNode)&&a.removeChild(b.aoOpenRows[c].nTr),b.aoOpenRows.splice(c,1),0;return 1};this.fnDeleteRow=function(a,b,c){var d=u(this[j.ext.iApiIndex]),g,e,a="object"===typeof a?K(d,a):a,h=d.aoData.splice(a,1);g=0;for(e=d.aoData.length;g<e;g++)null!==d.aoData[g].nTr&&(d.aoData[g].nTr._DT_RowIndex=
g);g=i.inArray(a,d.aiDisplay);d.asDataSearch.splice(g,1);fa(d.aiDisplayMaster,a);fa(d.aiDisplay,a);"function"===typeof b&&b.call(this,d,h);d._iDisplayStart>=d.fnRecordsDisplay()&&(d._iDisplayStart-=d._iDisplayLength,0>d._iDisplayStart&&(d._iDisplayStart=0));if(c===n||c)A(d),y(d);return h};this.fnDestroy=function(a){var b=u(this[j.ext.iApiIndex]),c=b.nTableWrapper.parentNode,d=b.nTBody,g,e,a=a===n?!1:!0;b.bDestroying=!0;C(b,"aoDestroyCallback","destroy",[b]);g=0;for(e=b.aoColumns.length;g<e;g++)!1===
b.aoColumns[g].bVisible&&this.fnSetColumnVis(g,!0);i(b.nTableWrapper).find("*").andSelf().unbind(".DT");i("tbody>tr>td."+b.oClasses.sRowEmpty,b.nTable).parent().remove();b.nTable!=b.nTHead.parentNode&&(i(b.nTable).children("thead").remove(),b.nTable.appendChild(b.nTHead));b.nTFoot&&b.nTable!=b.nTFoot.parentNode&&(i(b.nTable).children("tfoot").remove(),b.nTable.appendChild(b.nTFoot));b.nTable.parentNode.removeChild(b.nTable);i(b.nTableWrapper).remove();b.aaSorting=[];b.aaSortingFixed=[];Q(b);i(S(b)).removeClass(b.asStripeClasses.join(" "));
i("th, td",b.nTHead).removeClass([b.oClasses.sSortable,b.oClasses.sSortableAsc,b.oClasses.sSortableDesc,b.oClasses.sSortableNone].join(" "));b.bJUI&&(i("th span."+b.oClasses.sSortIcon+", td span."+b.oClasses.sSortIcon,b.nTHead).remove(),i("th, td",b.nTHead).each(function(){var a=i("div."+b.oClasses.sSortJUIWrapper,this),c=a.contents();i(this).append(c);a.remove()}));!a&&b.nTableReinsertBefore?c.insertBefore(b.nTable,b.nTableReinsertBefore):a||c.appendChild(b.nTable);g=0;for(e=b.aoData.length;g<e;g++)null!==
b.aoData[g].nTr&&d.appendChild(b.aoData[g].nTr);!0===b.oFeatures.bAutoWidth&&(b.nTable.style.width=q(b.sDestroyWidth));i(d).children("tr:even").addClass(b.asDestroyStripes[0]);i(d).children("tr:odd").addClass(b.asDestroyStripes[1]);g=0;for(e=j.settings.length;g<e;g++)j.settings[g]==b&&j.settings.splice(g,1);b=null};this.fnDraw=function(a){var b=u(this[j.ext.iApiIndex]);!1===a?(A(b),y(b)):$(b)};this.fnFilter=function(a,b,c,d,e,f){var h=u(this[j.ext.iApiIndex]);if(h.oFeatures.bFilter){if(c===n||null===
c)c=!1;if(d===n||null===d)d=!0;if(e===n||null===e)e=!0;if(f===n||null===f)f=!0;if(b===n||null===b){if(M(h,{sSearch:a+"",bRegex:c,bSmart:d,bCaseInsensitive:f},1),e&&h.aanFeatures.f){b=h.aanFeatures.f;c=0;for(d=b.length;c<d;c++)i(b[c]._DT_Input).val(a)}}else i.extend(h.aoPreSearchCols[b],{sSearch:a+"",bRegex:c,bSmart:d,bCaseInsensitive:f}),M(h,h.oPreviousSearch,1)}};this.fnGetData=function(a,b){var c=u(this[j.ext.iApiIndex]);if(a!==n){var d=a;if("object"===typeof a){var e=a.nodeName.toLowerCase();"tr"===
e?d=K(c,a):"td"===e&&(d=K(c,a.parentNode),b=da(c,d,a))}return b!==n?w(c,d,b,""):c.aoData[d]!==n?c.aoData[d]._aData:null}return Y(c)};this.fnGetNodes=function(a){var b=u(this[j.ext.iApiIndex]);return a!==n?b.aoData[a]!==n?b.aoData[a].nTr:null:S(b)};this.fnGetPosition=function(a){var b=u(this[j.ext.iApiIndex]),c=a.nodeName.toUpperCase();return"TR"==c?K(b,a):"TD"==c||"TH"==c?(c=K(b,a.parentNode),a=da(b,c,a),[c,t(b,a),a]):null};this.fnIsOpen=function(a){for(var b=u(this[j.ext.iApiIndex]),c=0;c<b.aoOpenRows.length;c++)if(b.aoOpenRows[c].nParent==
a)return!0;return!1};this.fnOpen=function(a,b,c){var d=u(this[j.ext.iApiIndex]),e=S(d);if(-1!==i.inArray(a,e)){this.fnClose(a);var e=l.createElement("tr"),f=l.createElement("td");e.appendChild(f);f.className=c;f.colSpan=v(d);"string"===typeof b?f.innerHTML=b:i(f).html(b);b=i("tr",d.nTBody);-1!=i.inArray(a,b)&&i(e).insertAfter(a);d.aoOpenRows.push({nTr:e,nParent:a});return e}};this.fnPageChange=function(a,b){var c=u(this[j.ext.iApiIndex]);pa(c,a);A(c);(b===n||b)&&y(c)};this.fnSetColumnVis=function(a,
b,c){var d=u(this[j.ext.iApiIndex]),e,f,h=d.aoColumns,i=d.aoData,o,m;if(h[a].bVisible!=b){if(b){for(e=f=0;e<a;e++)h[e].bVisible&&f++;m=f>=v(d);if(!m)for(e=a;e<h.length;e++)if(h[e].bVisible){o=e;break}e=0;for(f=i.length;e<f;e++)null!==i[e].nTr&&(m?i[e].nTr.appendChild(i[e]._anHidden[a]):i[e].nTr.insertBefore(i[e]._anHidden[a],L(d,e)[o]))}else{e=0;for(f=i.length;e<f;e++)null!==i[e].nTr&&(o=L(d,e)[a],i[e]._anHidden[a]=o,o.parentNode.removeChild(o))}h[a].bVisible=b;U(d,d.aoHeader);d.nTFoot&&U(d,d.aoFooter);
e=0;for(f=d.aoOpenRows.length;e<f;e++)d.aoOpenRows[e].nTr.colSpan=v(d);if(c===n||c)k(d),y(d);qa(d)}};this.fnSettings=function(){return u(this[j.ext.iApiIndex])};this.fnSort=function(a){var b=u(this[j.ext.iApiIndex]);b.aaSorting=a;P(b)};this.fnSortListener=function(a,b,c){ga(u(this[j.ext.iApiIndex]),a,b,c)};this.fnUpdate=function(a,b,c,d,e){var f=u(this[j.ext.iApiIndex]),b="object"===typeof b?K(f,b):b;if(f.__fnUpdateDeep===n&&i.isArray(a)&&"object"===typeof a){f.aoData[b]._aData=a.slice();f.__fnUpdateDeep=
!0;for(c=0;c<f.aoColumns.length;c++)this.fnUpdate(w(f,b,c),b,c,!1,!1);f.__fnUpdateDeep=n}else if(f.__fnUpdateDeep===n&&null!==a&&"object"===typeof a){f.aoData[b]._aData=i.extend(!0,{},a);f.__fnUpdateDeep=!0;for(c=0;c<f.aoColumns.length;c++)this.fnUpdate(w(f,b,c),b,c,!1,!1);f.__fnUpdateDeep=n}else{I(f,b,c,a);var a=w(f,b,c,"display"),h=f.aoColumns[c];null!==h.fnRender&&(a=R(f,b,c),h.bUseRendered&&I(f,b,c,a));null!==f.aoData[b].nTr&&(L(f,b)[c].innerHTML=a)}c=i.inArray(b,f.aiDisplay);f.asDataSearch[c]=
ma(f,X(f,b,"filter"));(e===n||e)&&k(f);(d===n||d)&&$(f);return 0};this.fnVersionCheck=j.ext.fnVersionCheck;this.oApi={_fnExternApiFunc:Ua,_fnInitialise:aa,_fnInitComplete:Z,_fnLanguageCompat:oa,_fnAddColumn:o,_fnColumnOptions:r,_fnAddData:H,_fnCreateTr:ca,_fnGatherData:ua,_fnBuildHead:va,_fnDrawHead:U,_fnDraw:y,_fnReDraw:$,_fnAjaxUpdate:wa,_fnAjaxParameters:Ea,_fnAjaxUpdateDraw:Fa,_fnServerParams:ia,_fnAddOptionsHtml:xa,_fnFeatureHtmlTable:Ba,_fnScrollDraw:Ka,_fnAdjustColumnSizing:k,_fnFeatureHtmlFilter:za,
_fnFilterComplete:M,_fnFilterCustom:Ia,_fnFilterColumn:Ha,_fnFilter:Ga,_fnBuildSearchArray:ja,_fnBuildSearchRow:ma,_fnFilterCreateSearch:ka,_fnDataToSearch:la,_fnSort:P,_fnSortAttachListener:ga,_fnSortingClasses:Q,_fnFeatureHtmlPaginate:Da,_fnPageChange:pa,_fnFeatureHtmlInfo:Ca,_fnUpdateInfo:Ja,_fnFeatureHtmlLength:ya,_fnFeatureHtmlProcessing:Aa,_fnProcessingDisplay:F,_fnVisibleToColumnIndex:G,_fnColumnIndexToVisible:t,_fnNodeToDataIndex:K,_fnVisbleColumns:v,_fnCalculateEnd:A,_fnConvertToWidth:La,
_fnCalculateColumnWidths:ba,_fnScrollingWidthAdjust:Na,_fnGetWidestNode:Ma,_fnGetMaxLenString:Oa,_fnStringToCss:q,_fnDetectType:z,_fnSettingsFromNode:u,_fnGetDataMaster:Y,_fnGetTrNodes:S,_fnGetTdNodes:L,_fnEscapeRegex:na,_fnDeleteIndex:fa,_fnReOrderIndex:D,_fnColumnOrdering:x,_fnLog:E,_fnClearTable:ea,_fnSaveState:qa,_fnLoadState:Ra,_fnCreateCookie:function(a,b,c,d,e){var f=new Date;f.setTime(f.getTime()+1E3*c);var c=V.location.pathname.split("/"),a=a+"_"+c.pop().replace(/[\/:]/g,"").toLowerCase(),
h;null!==e?(h="function"===typeof i.parseJSON?i.parseJSON(b):eval("("+b+")"),b=e(a,h,f.toGMTString(),c.join("/")+"/")):b=a+"="+encodeURIComponent(b)+"; expires="+f.toGMTString()+"; path="+c.join("/")+"/";e="";f=9999999999999;if(4096<(null!==Sa(a)?l.cookie.length:b.length+l.cookie.length)+10){for(var a=l.cookie.split(";"),o=0,j=a.length;o<j;o++)if(-1!=a[o].indexOf(d)){var k=a[o].split("=");try{h=eval("("+decodeURIComponent(k[1])+")")}catch(r){continue}h.iCreate&&h.iCreate<f&&(e=k[0],f=h.iCreate)}""!==
e&&(l.cookie=e+"=; expires=Thu, 01-Jan-1970 00:00:01 GMT; path="+c.join("/")+"/")}l.cookie=b},_fnReadCookie:Sa,_fnDetectHeader:T,_fnGetUniqueThs:O,_fnScrollBarWidth:Pa,_fnApplyToChildren:N,_fnMap:p,_fnGetRowData:X,_fnGetCellData:w,_fnSetCellData:I,_fnGetObjectDataFn:W,_fnSetObjectDataFn:ta,_fnApplyColumnDefs:J,_fnBindAction:Qa,_fnExtend:Ta,_fnCallbackReg:B,_fnCallbackFire:C,_fnJsonString:Va,_fnRender:R,_fnNodeToColumnIndex:da,_fnInfoMacros:ha};i.extend(j.ext.oApi,this.oApi);for(var ra in j.ext.oApi)ra&&
(this[ra]=Ua(ra));var sa=this;return this.each(function(){var a=0,b,c,d;c=this.getAttribute("id");var g=!1,f=!1;if("table"!=this.nodeName.toLowerCase())E(null,0,"Attempted to initialise DataTables on a node which is not a table: "+this.nodeName);else{a=0;for(b=j.settings.length;a<b;a++){if(j.settings[a].nTable==this){if(e===n||e.bRetrieve)return j.settings[a].oInstance;if(e.bDestroy){j.settings[a].oInstance.fnDestroy();break}else{E(j.settings[a],0,"Cannot reinitialise DataTable.\n\nTo retrieve the DataTables object for this table, pass no arguments or see the docs for bRetrieve and bDestroy");
return}}if(j.settings[a].sTableId==this.id){j.settings.splice(a,1);break}}if(null===c||""===c)this.id=c="DataTables_Table_"+j.ext._oExternConfig.iNextUnique++;var h=i.extend(!0,{},j.models.oSettings,{nTable:this,oApi:sa.oApi,oInit:e,sDestroyWidth:i(this).width(),sInstance:c,sTableId:c});j.settings.push(h);h.oInstance=1===sa.length?sa:i(this).dataTable();e||(e={});e.oLanguage&&oa(e.oLanguage);e=Ta(i.extend(!0,{},j.defaults),e);p(h.oFeatures,e,"bPaginate");p(h.oFeatures,e,"bLengthChange");p(h.oFeatures,
e,"bFilter");p(h.oFeatures,e,"bSort");p(h.oFeatures,e,"bInfo");p(h.oFeatures,e,"bProcessing");p(h.oFeatures,e,"bAutoWidth");p(h.oFeatures,e,"bSortClasses");p(h.oFeatures,e,"bServerSide");p(h.oFeatures,e,"bDeferRender");p(h.oScroll,e,"sScrollX","sX");p(h.oScroll,e,"sScrollXInner","sXInner");p(h.oScroll,e,"sScrollY","sY");p(h.oScroll,e,"bScrollCollapse","bCollapse");p(h.oScroll,e,"bScrollInfinite","bInfinite");p(h.oScroll,e,"iScrollLoadGap","iLoadGap");p(h.oScroll,e,"bScrollAutoCss","bAutoCss");p(h,
e,"asStripeClasses");p(h,e,"asStripClasses","asStripeClasses");p(h,e,"fnServerData");p(h,e,"fnFormatNumber");p(h,e,"sServerMethod");p(h,e,"aaSorting");p(h,e,"aaSortingFixed");p(h,e,"aLengthMenu");p(h,e,"sPaginationType");p(h,e,"sAjaxSource");p(h,e,"sAjaxDataProp");p(h,e,"iCookieDuration");p(h,e,"sCookiePrefix");p(h,e,"sDom");p(h,e,"bSortCellsTop");p(h,e,"iTabIndex");p(h,e,"oSearch","oPreviousSearch");p(h,e,"aoSearchCols","aoPreSearchCols");p(h,e,"iDisplayLength","_iDisplayLength");p(h,e,"bJQueryUI",
"bJUI");p(h,e,"fnCookieCallback");p(h,e,"fnStateLoad");p(h,e,"fnStateSave");p(h.oLanguage,e,"fnInfoCallback");B(h,"aoDrawCallback",e.fnDrawCallback,"user");B(h,"aoServerParams",e.fnServerParams,"user");B(h,"aoStateSaveParams",e.fnStateSaveParams,"user");B(h,"aoStateLoadParams",e.fnStateLoadParams,"user");B(h,"aoStateLoaded",e.fnStateLoaded,"user");B(h,"aoRowCallback",e.fnRowCallback,"user");B(h,"aoRowCreatedCallback",e.fnCreatedRow,"user");B(h,"aoHeaderCallback",e.fnHeaderCallback,"user");B(h,"aoFooterCallback",
e.fnFooterCallback,"user");B(h,"aoInitComplete",e.fnInitComplete,"user");B(h,"aoPreDrawCallback",e.fnPreDrawCallback,"user");h.oFeatures.bServerSide&&h.oFeatures.bSort&&h.oFeatures.bSortClasses?B(h,"aoDrawCallback",Q,"server_side_sort_classes"):h.oFeatures.bDeferRender&&B(h,"aoDrawCallback",Q,"defer_sort_classes");e.bJQueryUI?(i.extend(h.oClasses,j.ext.oJUIClasses),e.sDom===j.defaults.sDom&&"lfrtip"===j.defaults.sDom&&(h.sDom='<"H"lfr>t<"F"ip>')):i.extend(h.oClasses,j.ext.oStdClasses);i(this).addClass(h.oClasses.sTable);
if(""!==h.oScroll.sX||""!==h.oScroll.sY)h.oScroll.iBarWidth=Pa();h.iInitDisplayStart===n&&(h.iInitDisplayStart=e.iDisplayStart,h._iDisplayStart=e.iDisplayStart);e.bStateSave&&(h.oFeatures.bStateSave=!0,Ra(h,e),B(h,"aoDrawCallback",qa,"state_save"));null!==e.iDeferLoading&&(h.bDeferLoading=!0,a=i.isArray(e.iDeferLoading),h._iRecordsDisplay=a?e.iDeferLoading[0]:e.iDeferLoading,h._iRecordsTotal=a?e.iDeferLoading[1]:e.iDeferLoading);null!==e.aaData&&(f=!0);""!==e.oLanguage.sUrl?(h.oLanguage.sUrl=e.oLanguage.sUrl,
i.getJSON(h.oLanguage.sUrl,null,function(a){oa(a);i.extend(true,h.oLanguage,e.oLanguage,a);aa(h)}),g=!0):i.extend(!0,h.oLanguage,e.oLanguage);null===e.asStripeClasses&&(h.asStripeClasses=[h.oClasses.sStripeOdd,h.oClasses.sStripeEven]);c=!1;d=i(this).children("tbody").children("tr");a=0;for(b=h.asStripeClasses.length;a<b;a++)if(d.filter(":lt(2)").hasClass(h.asStripeClasses[a])){c=!0;break}c&&(h.asDestroyStripes=["",""],i(d[0]).hasClass(h.oClasses.sStripeOdd)&&(h.asDestroyStripes[0]+=h.oClasses.sStripeOdd+
" "),i(d[0]).hasClass(h.oClasses.sStripeEven)&&(h.asDestroyStripes[0]+=h.oClasses.sStripeEven),i(d[1]).hasClass(h.oClasses.sStripeOdd)&&(h.asDestroyStripes[1]+=h.oClasses.sStripeOdd+" "),i(d[1]).hasClass(h.oClasses.sStripeEven)&&(h.asDestroyStripes[1]+=h.oClasses.sStripeEven),d.removeClass(h.asStripeClasses.join(" ")));c=[];a=this.getElementsByTagName("thead");0!==a.length&&(T(h.aoHeader,a[0]),c=O(h));if(null===e.aoColumns){d=[];a=0;for(b=c.length;a<b;a++)d.push(null)}else d=e.aoColumns;a=0;for(b=
d.length;a<b;a++)e.saved_aoColumns!==n&&e.saved_aoColumns.length==b&&(null===d[a]&&(d[a]={}),d[a].bVisible=e.saved_aoColumns[a].bVisible),o(h,c?c[a]:null);J(h,e.aoColumnDefs,d,function(a,b){r(h,a,b)});a=0;for(b=h.aaSorting.length;a<b;a++){h.aaSorting[a][0]>=h.aoColumns.length&&(h.aaSorting[a][0]=0);var k=h.aoColumns[h.aaSorting[a][0]];h.aaSorting[a][2]===n&&(h.aaSorting[a][2]=0);e.aaSorting===n&&h.saved_aaSorting===n&&(h.aaSorting[a][1]=k.asSorting[0]);c=0;for(d=k.asSorting.length;c<d;c++)if(h.aaSorting[a][1]==
k.asSorting[c]){h.aaSorting[a][2]=c;break}}Q(h);a=i(this).children("caption").each(function(){this._captionSide=i(this).css("caption-side")});b=i(this).children("thead");0===b.length&&(b=[l.createElement("thead")],this.appendChild(b[0]));h.nTHead=b[0];b=i(this).children("tbody");0===b.length&&(b=[l.createElement("tbody")],this.appendChild(b[0]));h.nTBody=b[0];h.nTBody.setAttribute("role","alert");h.nTBody.setAttribute("aria-live","polite");h.nTBody.setAttribute("aria-relevant","all");b=i(this).children("tfoot");
if(0===b.length&&0<a.length&&(""!==h.oScroll.sX||""!==h.oScroll.sY))b=[l.createElement("tfoot")],this.appendChild(b[0]);0<b.length&&(h.nTFoot=b[0],T(h.aoFooter,h.nTFoot));if(f)for(a=0;a<e.aaData.length;a++)H(h,e.aaData[a]);else ua(h);h.aiDisplay=h.aiDisplayMaster.slice();h.bInitialised=!0;!1===g&&aa(h)}})};j.fnVersionCheck=function(e){for(var i=function(e,i){for(;e.length<i;)e+="0";return e},r=j.ext.sVersion.split("."),e=e.split("."),k="",n="",l=0,v=e.length;l<v;l++)k+=i(r[l],3),n+=i(e[l],3);return parseInt(k,
10)>=parseInt(n,10)};j.fnIsDataTable=function(e){for(var i=j.settings,r=0;r<i.length;r++)if(i[r].nTable===e||i[r].nScrollHead===e||i[r].nScrollFoot===e)return!0;return!1};j.fnTables=function(e){var o=[];jQuery.each(j.settings,function(j,k){(!e||!0===e&&i(k.nTable).is(":visible"))&&o.push(k.nTable)});return o};j.version="1.9.2";j.settings=[];j.models={};j.models.ext={afnFiltering:[],afnSortData:[],aoFeatures:[],aTypes:[],fnVersionCheck:j.fnVersionCheck,iApiIndex:0,ofnSearch:{},oApi:{},oStdClasses:{},
oJUIClasses:{},oPagination:{},oSort:{},sVersion:j.version,sErrMode:"alert",_oExternConfig:{iNextUnique:0}};j.models.oSearch={bCaseInsensitive:!0,sSearch:"",bRegex:!1,bSmart:!0};j.models.oRow={nTr:null,_aData:[],_aSortData:[],_anHidden:[],_sRowStripe:""};j.models.oColumn={aDataSort:null,asSorting:null,bSearchable:null,bSortable:null,bUseRendered:null,bVisible:null,_bAutoType:!0,fnCreatedCell:null,fnGetData:null,fnRender:null,fnSetData:null,mDataProp:null,nTh:null,nTf:null,sClass:null,sContentPadding:null,
sDefaultContent:null,sName:null,sSortDataType:"std",sSortingClass:null,sSortingClassJUI:null,sTitle:null,sType:null,sWidth:null,sWidthOrig:null};j.defaults={aaData:null,aaSorting:[[0,"asc"]],aaSortingFixed:null,aLengthMenu:[10,25,50,100],aoColumns:null,aoColumnDefs:null,aoSearchCols:[],asStripeClasses:null,bAutoWidth:!0,bDeferRender:!1,bDestroy:!1,bFilter:!0,bInfo:!0,bJQueryUI:!1,bLengthChange:!0,bPaginate:!0,bProcessing:!1,bRetrieve:!1,bScrollAutoCss:!0,bScrollCollapse:!1,bScrollInfinite:!1,bServerSide:!1,
bSort:!0,bSortCellsTop:!1,bSortClasses:!0,bStateSave:!1,fnCookieCallback:null,fnCreatedRow:null,fnDrawCallback:null,fnFooterCallback:null,fnFormatNumber:function(e){if(1E3>e)return e;for(var i=e+"",e=i.split(""),j="",i=i.length,k=0;k<i;k++)0===k%3&&0!==k&&(j=this.oLanguage.sInfoThousands+j),j=e[i-k-1]+j;return j},fnHeaderCallback:null,fnInfoCallback:null,fnInitComplete:null,fnPreDrawCallback:null,fnRowCallback:null,fnServerData:function(e,j,n,k){k.jqXHR=i.ajax({url:e,data:j,success:function(e){i(k.oInstance).trigger("xhr",
k);n(e)},dataType:"json",cache:!1,type:k.sServerMethod,error:function(e,i){"parsererror"==i&&k.oApi._fnLog(k,0,"DataTables warning: JSON data from server could not be parsed. This is caused by a JSON formatting error.")}})},fnServerParams:null,fnStateLoad:function(e){var e=this.oApi._fnReadCookie(e.sCookiePrefix+e.sInstance),j;try{j="function"===typeof i.parseJSON?i.parseJSON(e):eval("("+e+")")}catch(n){j=null}return j},fnStateLoadParams:null,fnStateLoaded:null,fnStateSave:function(e,i){this.oApi._fnCreateCookie(e.sCookiePrefix+
e.sInstance,this.oApi._fnJsonString(i),e.iCookieDuration,e.sCookiePrefix,e.fnCookieCallback)},fnStateSaveParams:null,iCookieDuration:7200,iDeferLoading:null,iDisplayLength:10,iDisplayStart:0,iScrollLoadGap:100,iTabIndex:0,oLanguage:{oAria:{sSortAscending:": activate to sort column ascending",sSortDescending:": activate to sort column descending"},oPaginate:{sFirst:"First",sLast:"Last",sNext:"Next",sPrevious:"Previous"},sEmptyTable:"No data available in table",sInfo:"Showing _START_ to _END_ of _TOTAL_ entries",
sInfoEmpty:"Showing 0 to 0 of 0 entries",sInfoFiltered:"(filtered from _MAX_ total entries)",sInfoPostFix:"",sInfoThousands:",",sLengthMenu:"Show _MENU_ entries",sLoadingRecords:"Loading...",sProcessing:"Processing...",sSearch:"Search:",sUrl:"",sZeroRecords:"No matching records found"},oSearch:i.extend({},j.models.oSearch),sAjaxDataProp:"aaData",sAjaxSource:null,sCookiePrefix:"SpryMedia_DataTables_",sDom:"lfrtip",sPaginationType:"two_button",sScrollX:"",sScrollXInner:"",sScrollY:"",sServerMethod:"GET"};
j.defaults.columns={aDataSort:null,asSorting:["asc","desc"],bSearchable:!0,bSortable:!0,bUseRendered:!0,bVisible:!0,fnCreatedCell:null,fnRender:null,iDataSort:-1,mDataProp:null,sCellType:"td",sClass:"",sContentPadding:"",sDefaultContent:null,sName:"",sSortDataType:"std",sTitle:null,sType:null,sWidth:null};j.models.oSettings={oFeatures:{bAutoWidth:null,bDeferRender:null,bFilter:null,bInfo:null,bLengthChange:null,bPaginate:null,bProcessing:null,bServerSide:null,bSort:null,bSortClasses:null,bStateSave:null},
oScroll:{bAutoCss:null,bCollapse:null,bInfinite:null,iBarWidth:0,iLoadGap:null,sX:null,sXInner:null,sY:null},oLanguage:{fnInfoCallback:null},aanFeatures:[],aoData:[],aiDisplay:[],aiDisplayMaster:[],aoColumns:[],aoHeader:[],aoFooter:[],asDataSearch:[],oPreviousSearch:{},aoPreSearchCols:[],aaSorting:null,aaSortingFixed:null,asStripeClasses:null,asDestroyStripes:[],sDestroyWidth:0,aoRowCallback:[],aoHeaderCallback:[],aoFooterCallback:[],aoDrawCallback:[],aoRowCreatedCallback:[],aoPreDrawCallback:[],
aoInitComplete:[],aoStateSaveParams:[],aoStateLoadParams:[],aoStateLoaded:[],sTableId:"",nTable:null,nTHead:null,nTFoot:null,nTBody:null,nTableWrapper:null,bDeferLoading:!1,bInitialised:!1,aoOpenRows:[],sDom:null,sPaginationType:"two_button",iCookieDuration:0,sCookiePrefix:"",fnCookieCallback:null,aoStateSave:[],aoStateLoad:[],oLoadedState:null,sAjaxSource:null,sAjaxDataProp:null,bAjaxDataGet:!0,jqXHR:null,fnServerData:null,aoServerParams:[],sServerMethod:null,fnFormatNumber:null,aLengthMenu:null,
iDraw:0,bDrawing:!1,iDrawError:-1,_iDisplayLength:10,_iDisplayStart:0,_iDisplayEnd:10,_iRecordsTotal:0,_iRecordsDisplay:0,bJUI:null,oClasses:{},bFiltered:!1,bSorted:!1,bSortCellsTop:null,oInit:null,aoDestroyCallback:[],fnRecordsTotal:function(){return this.oFeatures.bServerSide?parseInt(this._iRecordsTotal,10):this.aiDisplayMaster.length},fnRecordsDisplay:function(){return this.oFeatures.bServerSide?parseInt(this._iRecordsDisplay,10):this.aiDisplay.length},fnDisplayEnd:function(){return this.oFeatures.bServerSide?
!1===this.oFeatures.bPaginate||-1==this._iDisplayLength?this._iDisplayStart+this.aiDisplay.length:Math.min(this._iDisplayStart+this._iDisplayLength,this._iRecordsDisplay):this._iDisplayEnd},oInstance:null,sInstance:null,iTabIndex:0,nScrollHead:null,nScrollFoot:null};j.ext=i.extend(!0,{},j.models.ext);i.extend(j.ext.oStdClasses,{sTable:"dataTable",sPagePrevEnabled:"paginate_enabled_previous",sPagePrevDisabled:"paginate_disabled_previous",sPageNextEnabled:"paginate_enabled_next",sPageNextDisabled:"paginate_disabled_next",
sPageJUINext:"",sPageJUIPrev:"",sPageButton:"paginate_button",sPageButtonActive:"paginate_active",sPageButtonStaticDisabled:"paginate_button paginate_button_disabled",sPageFirst:"first",sPagePrevious:"previous",sPageNext:"next",sPageLast:"last",sStripeOdd:"odd",sStripeEven:"even",sRowEmpty:"dataTables_empty",sWrapper:"dataTables_wrapper",sFilter:"dataTables_filter",sInfo:"dataTables_info",sPaging:"dataTables_paginate paging_",sLength:"dataTables_length",sProcessing:"dataTables_processing",sSortAsc:"sorting_asc",
sSortDesc:"sorting_desc",sSortable:"sorting",sSortableAsc:"sorting_asc_disabled",sSortableDesc:"sorting_desc_disabled",sSortableNone:"sorting_disabled",sSortColumn:"sorting_",sSortJUIAsc:"",sSortJUIDesc:"",sSortJUI:"",sSortJUIAscAllowed:"",sSortJUIDescAllowed:"",sSortJUIWrapper:"",sSortIcon:"",sScrollWrapper:"dataTables_scroll",sScrollHead:"dataTables_scrollHead",sScrollHeadInner:"dataTables_scrollHeadInner",sScrollBody:"dataTables_scrollBody",sScrollFoot:"dataTables_scrollFoot",sScrollFootInner:"dataTables_scrollFootInner",
sFooterTH:"",sJUIHeader:"",sJUIFooter:""});i.extend(j.ext.oJUIClasses,j.ext.oStdClasses,{sPagePrevEnabled:"fg-button ui-button ui-state-default ui-corner-left",sPagePrevDisabled:"fg-button ui-button ui-state-default ui-corner-left ui-state-disabled",sPageNextEnabled:"fg-button ui-button ui-state-default ui-corner-right",sPageNextDisabled:"fg-button ui-button ui-state-default ui-corner-right ui-state-disabled",sPageJUINext:"ui-icon ui-icon-circle-arrow-e",sPageJUIPrev:"ui-icon ui-icon-circle-arrow-w",
sPageButton:"fg-button ui-button ui-state-default",sPageButtonActive:"fg-button ui-button ui-state-default ui-state-disabled",sPageButtonStaticDisabled:"fg-button ui-button ui-state-default ui-state-disabled",sPageFirst:"first ui-corner-tl ui-corner-bl",sPageLast:"last ui-corner-tr ui-corner-br",sPaging:"dataTables_paginate fg-buttonset ui-buttonset fg-buttonset-multi ui-buttonset-multi paging_",sSortAsc:"ui-state-default",sSortDesc:"ui-state-default",sSortable:"ui-state-default",sSortableAsc:"ui-state-default",
sSortableDesc:"ui-state-default",sSortableNone:"ui-state-default",sSortJUIAsc:"css_right ui-icon ui-icon-triangle-1-n",sSortJUIDesc:"css_right ui-icon ui-icon-triangle-1-s",sSortJUI:"css_right ui-icon ui-icon-carat-2-n-s",sSortJUIAscAllowed:"css_right ui-icon ui-icon-carat-1-n",sSortJUIDescAllowed:"css_right ui-icon ui-icon-carat-1-s",sSortJUIWrapper:"DataTables_sort_wrapper",sSortIcon:"DataTables_sort_icon",sScrollHead:"dataTables_scrollHead ui-state-default",sScrollFoot:"dataTables_scrollFoot ui-state-default",
sFooterTH:"ui-state-default",sJUIHeader:"fg-toolbar ui-toolbar ui-widget-header ui-corner-tl ui-corner-tr ui-helper-clearfix",sJUIFooter:"fg-toolbar ui-toolbar ui-widget-header ui-corner-bl ui-corner-br ui-helper-clearfix"});i.extend(j.ext.oPagination,{two_button:{fnInit:function(e,j,n){var k=e.oLanguage.oPaginate,l=function(i){e.oApi._fnPageChange(e,i.data.action)&&n(e)},k=!e.bJUI?'<a class="'+e.oClasses.sPagePrevDisabled+'" tabindex="'+e.iTabIndex+'" role="button">'+k.sPrevious+'</a><a class="'+
e.oClasses.sPageNextDisabled+'" tabindex="'+e.iTabIndex+'" role="button">'+k.sNext+"</a>":'<a class="'+e.oClasses.sPagePrevDisabled+'" tabindex="'+e.iTabIndex+'" role="button"><span class="'+e.oClasses.sPageJUIPrev+'"></span></a><a class="'+e.oClasses.sPageNextDisabled+'" tabindex="'+e.iTabIndex+'" role="button"><span class="'+e.oClasses.sPageJUINext+'"></span></a>';i(j).append(k);var t=i("a",j),k=t[0],t=t[1];e.oApi._fnBindAction(k,{action:"previous"},l);e.oApi._fnBindAction(t,{action:"next"},l);
e.aanFeatures.p||(j.id=e.sTableId+"_paginate",k.id=e.sTableId+"_previous",t.id=e.sTableId+"_next",k.setAttribute("aria-controls",e.sTableId),t.setAttribute("aria-controls",e.sTableId))},fnUpdate:function(e){if(e.aanFeatures.p)for(var i=e.oClasses,j=e.aanFeatures.p,k=0,n=j.length;k<n;k++)0!==j[k].childNodes.length&&(j[k].childNodes[0].className=0===e._iDisplayStart?i.sPagePrevDisabled:i.sPagePrevEnabled,j[k].childNodes[1].className=e.fnDisplayEnd()==e.fnRecordsDisplay()?i.sPageNextDisabled:i.sPageNextEnabled)}},
iFullNumbersShowPages:5,full_numbers:{fnInit:function(e,j,n){var k=e.oLanguage.oPaginate,l=e.oClasses,t=function(i){e.oApi._fnPageChange(e,i.data.action)&&n(e)};i(j).append('<a  tabindex="'+e.iTabIndex+'" class="'+l.sPageButton+" "+l.sPageFirst+'">'+k.sFirst+'</a><a  tabindex="'+e.iTabIndex+'" class="'+l.sPageButton+" "+l.sPagePrevious+'">'+k.sPrevious+'</a><span></span><a tabindex="'+e.iTabIndex+'" class="'+l.sPageButton+" "+l.sPageNext+'">'+k.sNext+'</a><a tabindex="'+e.iTabIndex+'" class="'+l.sPageButton+
" "+l.sPageLast+'">'+k.sLast+"</a>");var v=i("a",j),k=v[0],l=v[1],z=v[2],v=v[3];e.oApi._fnBindAction(k,{action:"first"},t);e.oApi._fnBindAction(l,{action:"previous"},t);e.oApi._fnBindAction(z,{action:"next"},t);e.oApi._fnBindAction(v,{action:"last"},t);e.aanFeatures.p||(j.id=e.sTableId+"_paginate",k.id=e.sTableId+"_first",l.id=e.sTableId+"_previous",z.id=e.sTableId+"_next",v.id=e.sTableId+"_last")},fnUpdate:function(e,o){if(e.aanFeatures.p){var l=j.ext.oPagination.iFullNumbersShowPages,k=Math.floor(l/
2),n=Math.ceil(e.fnRecordsDisplay()/e._iDisplayLength),t=Math.ceil(e._iDisplayStart/e._iDisplayLength)+1,v="",z,D=e.oClasses,x,J=e.aanFeatures.p,H=function(i){e.oApi._fnBindAction(this,{page:i+z-1},function(i){e.oApi._fnPageChange(e,i.data.page);o(e);i.preventDefault()})};-1===e._iDisplayLength?t=k=z=1:n<l?(z=1,k=n):t<=k?(z=1,k=l):t>=n-k?(z=n-l+1,k=n):(z=t-Math.ceil(l/2)+1,k=z+l-1);for(l=z;l<=k;l++)v+=t!==l?'<a tabindex="'+e.iTabIndex+'" class="'+D.sPageButton+'">'+e.fnFormatNumber(l)+"</a>":'<a tabindex="'+
e.iTabIndex+'" class="'+D.sPageButtonActive+'">'+e.fnFormatNumber(l)+"</a>";l=0;for(k=J.length;l<k;l++)0!==J[l].childNodes.length&&(i("span:eq(0)",J[l]).html(v).children("a").each(H),x=J[l].getElementsByTagName("a"),x=[x[0],x[1],x[x.length-2],x[x.length-1]],i(x).removeClass(D.sPageButton+" "+D.sPageButtonActive+" "+D.sPageButtonStaticDisabled),i([x[0],x[1]]).addClass(1==t?D.sPageButtonStaticDisabled:D.sPageButton),i([x[2],x[3]]).addClass(0===n||t===n||-1===e._iDisplayLength?D.sPageButtonStaticDisabled:
D.sPageButton))}}}});i.extend(j.ext.oSort,{"string-pre":function(e){"string"!=typeof e&&(e=null!==e&&e.toString?e.toString():"");return e.toLowerCase()},"string-asc":function(e,i){return e<i?-1:e>i?1:0},"string-desc":function(e,i){return e<i?1:e>i?-1:0},"html-pre":function(e){return e.replace(/<.*?>/g,"").toLowerCase()},"html-asc":function(e,i){return e<i?-1:e>i?1:0},"html-desc":function(e,i){return e<i?1:e>i?-1:0},"date-pre":function(e){e=Date.parse(e);if(isNaN(e)||""===e)e=Date.parse("01/01/1970 00:00:00");
return e},"date-asc":function(e,i){return e-i},"date-desc":function(e,i){return i-e},"numeric-pre":function(e){return"-"==e||""===e?0:1*e},"numeric-asc":function(e,i){return e-i},"numeric-desc":function(e,i){return i-e}});i.extend(j.ext.aTypes,[function(e){if("number"===typeof e)return"numeric";if("string"!==typeof e)return null;var i,j=!1;i=e.charAt(0);if(-1=="0123456789-".indexOf(i))return null;for(var k=1;k<e.length;k++){i=e.charAt(k);if(-1=="0123456789.".indexOf(i))return null;if("."==i){if(j)return null;
j=!0}}return"numeric"},function(e){var i=Date.parse(e);return null!==i&&!isNaN(i)||"string"===typeof e&&0===e.length?"date":null},function(e){return"string"===typeof e&&-1!=e.indexOf("<")&&-1!=e.indexOf(">")?"html":null}]);i.fn.DataTable=j;i.fn.dataTable=j;i.fn.dataTableSettings=j.settings;i.fn.dataTableExt=j.ext})(jQuery,window,document,void 0);

// Copyright 2006 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


// Known Issues:
//
// * Patterns only support repeat.
// * Radial gradient are not implemented. The VML version of these look very
//   different from the canvas one.
// * Clipping paths are not implemented.
// * Coordsize. The width and height attribute have higher priority than the
//   width and height style values which isn't correct.
// * Painting mode isn't implemented.
// * Canvas width/height should is using content-box by default. IE in
//   Quirks mode will draw the canvas using border-box. Either change your
//   doctype to HTML5
//   (http://www.whatwg.org/specs/web-apps/current-work/#the-doctype)
//   or use Box Sizing Behavior from WebFX
//   (http://webfx.eae.net/dhtml/boxsizing/boxsizing.html)
// * Non uniform scaling does not correctly scale strokes.
// * Filling very large shapes (above 5000 points) is buggy.
// * Optimize. There is always room for speed improvements.

// Only add this code if we do not already have a canvas implementation
if (!document.createElement('canvas').getContext) {

(function() {

  // alias some functions to make (compiled) code shorter
  var m = Math;
  var mr = m.round;
  var ms = m.sin;
  var mc = m.cos;
  var abs = m.abs;
  var sqrt = m.sqrt;

  // this is used for sub pixel precision
  var Z = 10;
  var Z2 = Z / 2;

  /**
   * This funtion is assigned to the <canvas> elements as element.getContext().
   * @this {HTMLElement}
   * @return {CanvasRenderingContext2D_}
   */
  function getContext() {
    return this.context_ ||
        (this.context_ = new CanvasRenderingContext2D_(this));
  }

  var slice = Array.prototype.slice;

  /**
   * Binds a function to an object. The returned function will always use the
   * passed in {@code obj} as {@code this}.
   *
   * Example:
   *
   *   g = bind(f, obj, a, b)
   *   g(c, d) // will do f.call(obj, a, b, c, d)
   *
   * @param {Function} f The function to bind the object to
   * @param {Object} obj The object that should act as this when the function
   *     is called
   * @param {*} var_args Rest arguments that will be used as the initial
   *     arguments when the function is called
   * @return {Function} A new function that has bound this
   */
  function bind(f, obj, var_args) {
    var a = slice.call(arguments, 2);
    return function() {
      return f.apply(obj, a.concat(slice.call(arguments)));
    };
  }

  function encodeHtmlAttribute(s) {
    return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
  }

  function addNamespacesAndStylesheet(doc) {
    // create xmlns
    if (!doc.namespaces['g_vml_']) {
      doc.namespaces.add('g_vml_', 'urn:schemas-microsoft-com:vml',
                         '#default#VML');

    }
    if (!doc.namespaces['g_o_']) {
      doc.namespaces.add('g_o_', 'urn:schemas-microsoft-com:office:office',
                         '#default#VML');
    }

    // Setup default CSS.  Only add one style sheet per document
    if (!doc.styleSheets['ex_canvas_']) {
      var ss = doc.createStyleSheet();
      ss.owningElement.id = 'ex_canvas_';
      ss.cssText = 'canvas{display:inline-block;overflow:hidden;' +
          // default size is 300x150 in Gecko and Opera
          'text-align:left;width:300px;height:150px}';
    }
  }

  // Add namespaces and stylesheet at startup.
  addNamespacesAndStylesheet(document);

  var G_vmlCanvasManager_ = {
    init: function(opt_doc) {
      if (/MSIE/.test(navigator.userAgent) && !window.opera) {
        var doc = opt_doc || document;
        // Create a dummy element so that IE will allow canvas elements to be
        // recognized.
        doc.createElement('canvas');
        doc.attachEvent('onreadystatechange', bind(this.init_, this, doc));
      }
    },

    init_: function(doc) {
      // find all canvas elements
      var els = doc.getElementsByTagName('canvas');
      for (var i = 0; i < els.length; i++) {
        this.initElement(els[i]);
      }
    },

    /**
     * Public initializes a canvas element so that it can be used as canvas
     * element from now on. This is called automatically before the page is
     * loaded but if you are creating elements using createElement you need to
     * make sure this is called on the element.
     * @param {HTMLElement} el The canvas element to initialize.
     * @return {HTMLElement} the element that was created.
     */
    initElement: function(el) {
      if (!el.getContext) {
        el.getContext = getContext;

        // Add namespaces and stylesheet to document of the element.
        addNamespacesAndStylesheet(el.ownerDocument);

        // Remove fallback content. There is no way to hide text nodes so we
        // just remove all childNodes. We could hide all elements and remove
        // text nodes but who really cares about the fallback content.
        el.innerHTML = '';

        // do not use inline function because that will leak memory
        el.attachEvent('onpropertychange', onPropertyChange);
        el.attachEvent('onresize', onResize);

        var attrs = el.attributes;
        if (attrs.width && attrs.width.specified) {
          // TODO: use runtimeStyle and coordsize
          // el.getContext().setWidth_(attrs.width.nodeValue);
          el.style.width = attrs.width.nodeValue + 'px';
        } else {
          el.width = el.clientWidth;
        }
        if (attrs.height && attrs.height.specified) {
          // TODO: use runtimeStyle and coordsize
          // el.getContext().setHeight_(attrs.height.nodeValue);
          el.style.height = attrs.height.nodeValue + 'px';
        } else {
          el.height = el.clientHeight;
        }
        //el.getContext().setCoordsize_()
      }
      return el;
    }
  };

  function onPropertyChange(e) {
    var el = e.srcElement;

    switch (e.propertyName) {
      case 'width':
        el.getContext().clearRect();
        el.style.width = el.attributes.width.nodeValue + 'px';
        // In IE8 this does not trigger onresize.
        el.firstChild.style.width =  el.clientWidth + 'px';
        break;
      case 'height':
        el.getContext().clearRect();
        el.style.height = el.attributes.height.nodeValue + 'px';
        el.firstChild.style.height = el.clientHeight + 'px';
        break;
    }
  }

  function onResize(e) {
    var el = e.srcElement;
    if (el.firstChild) {
      el.firstChild.style.width =  el.clientWidth + 'px';
      el.firstChild.style.height = el.clientHeight + 'px';
    }
  }

  G_vmlCanvasManager_.init();

  // precompute "00" to "FF"
  var decToHex = [];
  for (var i = 0; i < 16; i++) {
    for (var j = 0; j < 16; j++) {
      decToHex[i * 16 + j] = i.toString(16) + j.toString(16);
    }
  }

  function createMatrixIdentity() {
    return [
      [1, 0, 0],
      [0, 1, 0],
      [0, 0, 1]
    ];
  }

  function matrixMultiply(m1, m2) {
    var result = createMatrixIdentity();

    for (var x = 0; x < 3; x++) {
      for (var y = 0; y < 3; y++) {
        var sum = 0;

        for (var z = 0; z < 3; z++) {
          sum += m1[x][z] * m2[z][y];
        }

        result[x][y] = sum;
      }
    }
    return result;
  }

  function copyState(o1, o2) {
    o2.fillStyle     = o1.fillStyle;
    o2.lineCap       = o1.lineCap;
    o2.lineJoin      = o1.lineJoin;
    o2.lineWidth     = o1.lineWidth;
    o2.miterLimit    = o1.miterLimit;
    o2.shadowBlur    = o1.shadowBlur;
    o2.shadowColor   = o1.shadowColor;
    o2.shadowOffsetX = o1.shadowOffsetX;
    o2.shadowOffsetY = o1.shadowOffsetY;
    o2.strokeStyle   = o1.strokeStyle;
    o2.globalAlpha   = o1.globalAlpha;
    o2.font          = o1.font;
    o2.textAlign     = o1.textAlign;
    o2.textBaseline  = o1.textBaseline;
    o2.arcScaleX_    = o1.arcScaleX_;
    o2.arcScaleY_    = o1.arcScaleY_;
    o2.lineScale_    = o1.lineScale_;
  }

  var colorData = {
    aliceblue: '#F0F8FF',
    antiquewhite: '#FAEBD7',
    aquamarine: '#7FFFD4',
    azure: '#F0FFFF',
    beige: '#F5F5DC',
    bisque: '#FFE4C4',
    black: '#000000',
    blanchedalmond: '#FFEBCD',
    blueviolet: '#8A2BE2',
    brown: '#A52A2A',
    burlywood: '#DEB887',
    cadetblue: '#5F9EA0',
    chartreuse: '#7FFF00',
    chocolate: '#D2691E',
    coral: '#FF7F50',
    cornflowerblue: '#6495ED',
    cornsilk: '#FFF8DC',
    crimson: '#DC143C',
    cyan: '#00FFFF',
    darkblue: '#00008B',
    darkcyan: '#008B8B',
    darkgoldenrod: '#B8860B',
    darkgray: '#A9A9A9',
    darkgreen: '#006400',
    darkgrey: '#A9A9A9',
    darkkhaki: '#BDB76B',
    darkmagenta: '#8B008B',
    darkolivegreen: '#556B2F',
    darkorange: '#FF8C00',
    darkorchid: '#9932CC',
    darkred: '#8B0000',
    darksalmon: '#E9967A',
    darkseagreen: '#8FBC8F',
    darkslateblue: '#483D8B',
    darkslategray: '#2F4F4F',
    darkslategrey: '#2F4F4F',
    darkturquoise: '#00CED1',
    darkviolet: '#9400D3',
    deeppink: '#FF1493',
    deepskyblue: '#00BFFF',
    dimgray: '#696969',
    dimgrey: '#696969',
    dodgerblue: '#1E90FF',
    firebrick: '#B22222',
    floralwhite: '#FFFAF0',
    forestgreen: '#228B22',
    gainsboro: '#DCDCDC',
    ghostwhite: '#F8F8FF',
    gold: '#FFD700',
    goldenrod: '#DAA520',
    grey: '#808080',
    greenyellow: '#ADFF2F',
    honeydew: '#F0FFF0',
    hotpink: '#FF69B4',
    indianred: '#CD5C5C',
    indigo: '#4B0082',
    ivory: '#FFFFF0',
    khaki: '#F0E68C',
    lavender: '#E6E6FA',
    lavenderblush: '#FFF0F5',
    lawngreen: '#7CFC00',
    lemonchiffon: '#FFFACD',
    lightblue: '#ADD8E6',
    lightcoral: '#F08080',
    lightcyan: '#E0FFFF',
    lightgoldenrodyellow: '#FAFAD2',
    lightgreen: '#90EE90',
    lightgrey: '#D3D3D3',
    lightpink: '#FFB6C1',
    lightsalmon: '#FFA07A',
    lightseagreen: '#20B2AA',
    lightskyblue: '#87CEFA',
    lightslategray: '#778899',
    lightslategrey: '#778899',
    lightsteelblue: '#B0C4DE',
    lightyellow: '#FFFFE0',
    limegreen: '#32CD32',
    linen: '#FAF0E6',
    magenta: '#FF00FF',
    mediumaquamarine: '#66CDAA',
    mediumblue: '#0000CD',
    mediumorchid: '#BA55D3',
    mediumpurple: '#9370DB',
    mediumseagreen: '#3CB371',
    mediumslateblue: '#7B68EE',
    mediumspringgreen: '#00FA9A',
    mediumturquoise: '#48D1CC',
    mediumvioletred: '#C71585',
    midnightblue: '#191970',
    mintcream: '#F5FFFA',
    mistyrose: '#FFE4E1',
    moccasin: '#FFE4B5',
    navajowhite: '#FFDEAD',
    oldlace: '#FDF5E6',
    olivedrab: '#6B8E23',
    orange: '#FFA500',
    orangered: '#FF4500',
    orchid: '#DA70D6',
    palegoldenrod: '#EEE8AA',
    palegreen: '#98FB98',
    paleturquoise: '#AFEEEE',
    palevioletred: '#DB7093',
    papayawhip: '#FFEFD5',
    peachpuff: '#FFDAB9',
    peru: '#CD853F',
    pink: '#FFC0CB',
    plum: '#DDA0DD',
    powderblue: '#B0E0E6',
    rosybrown: '#BC8F8F',
    royalblue: '#4169E1',
    saddlebrown: '#8B4513',
    salmon: '#FA8072',
    sandybrown: '#F4A460',
    seagreen: '#2E8B57',
    seashell: '#FFF5EE',
    sienna: '#A0522D',
    skyblue: '#87CEEB',
    slateblue: '#6A5ACD',
    slategray: '#708090',
    slategrey: '#708090',
    snow: '#FFFAFA',
    springgreen: '#00FF7F',
    steelblue: '#4682B4',
    tan: '#D2B48C',
    thistle: '#D8BFD8',
    tomato: '#FF6347',
    turquoise: '#40E0D0',
    violet: '#EE82EE',
    wheat: '#F5DEB3',
    whitesmoke: '#F5F5F5',
    yellowgreen: '#9ACD32'
  };


  function getRgbHslContent(styleString) {
    var start = styleString.indexOf('(', 3);
    var end = styleString.indexOf(')', start + 1);
    var parts = styleString.substring(start + 1, end).split(',');
    // add alpha if needed
    if (parts.length == 4 && styleString.substr(3, 1) == 'a') {
      alpha = Number(parts[3]);
    } else {
      parts[3] = 1;
    }
    return parts;
  }

  function percent(s) {
    return parseFloat(s) / 100;
  }

  function clamp(v, min, max) {
    return Math.min(max, Math.max(min, v));
  }

  function hslToRgb(parts){
    var r, g, b;
    h = parseFloat(parts[0]) / 360 % 360;
    if (h < 0)
      h++;
    s = clamp(percent(parts[1]), 0, 1);
    l = clamp(percent(parts[2]), 0, 1);
    if (s == 0) {
      r = g = b = l; // achromatic
    } else {
      var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      var p = 2 * l - q;
      r = hueToRgb(p, q, h + 1 / 3);
      g = hueToRgb(p, q, h);
      b = hueToRgb(p, q, h - 1 / 3);
    }

    return '#' + decToHex[Math.floor(r * 255)] +
        decToHex[Math.floor(g * 255)] +
        decToHex[Math.floor(b * 255)];
  }

  function hueToRgb(m1, m2, h) {
    if (h < 0)
      h++;
    if (h > 1)
      h--;

    if (6 * h < 1)
      return m1 + (m2 - m1) * 6 * h;
    else if (2 * h < 1)
      return m2;
    else if (3 * h < 2)
      return m1 + (m2 - m1) * (2 / 3 - h) * 6;
    else
      return m1;
  }

  function processStyle(styleString) {
    var str, alpha = 1;

    styleString = String(styleString);
    if (styleString.charAt(0) == '#') {
      str = styleString;
    } else if (/^rgb/.test(styleString)) {
      var parts = getRgbHslContent(styleString);
      var str = '#', n;
      for (var i = 0; i < 3; i++) {
        if (parts[i].indexOf('%') != -1) {
          n = Math.floor(percent(parts[i]) * 255);
        } else {
          n = Number(parts[i]);
        }
        str += decToHex[clamp(n, 0, 255)];
      }
      alpha = parts[3];
    } else if (/^hsl/.test(styleString)) {
      var parts = getRgbHslContent(styleString);
      str = hslToRgb(parts);
      alpha = parts[3];
    } else {
      str = colorData[styleString] || styleString;
    }
    return {color: str, alpha: alpha};
  }

  var DEFAULT_STYLE = {
    style: 'normal',
    variant: 'normal',
    weight: 'normal',
    size: 10,
    family: 'sans-serif'
  };

  // Internal text style cache
  var fontStyleCache = {};

  function processFontStyle(styleString) {
    if (fontStyleCache[styleString]) {
      return fontStyleCache[styleString];
    }

    var el = document.createElement('div');
    var style = el.style;
    try {
      style.font = styleString;
    } catch (ex) {
      // Ignore failures to set to invalid font.
    }

    return fontStyleCache[styleString] = {
      style: style.fontStyle || DEFAULT_STYLE.style,
      variant: style.fontVariant || DEFAULT_STYLE.variant,
      weight: style.fontWeight || DEFAULT_STYLE.weight,
      size: style.fontSize || DEFAULT_STYLE.size,
      family: style.fontFamily || DEFAULT_STYLE.family
    };
  }

  function getComputedStyle(style, element) {
    var computedStyle = {};

    for (var p in style) {
      computedStyle[p] = style[p];
    }

    // Compute the size
    var canvasFontSize = parseFloat(element.currentStyle.fontSize),
        fontSize = parseFloat(style.size);

    if (typeof style.size == 'number') {
      computedStyle.size = style.size;
    } else if (style.size.indexOf('px') != -1) {
      computedStyle.size = fontSize;
    } else if (style.size.indexOf('em') != -1) {
      computedStyle.size = canvasFontSize * fontSize;
    } else if(style.size.indexOf('%') != -1) {
      computedStyle.size = (canvasFontSize / 100) * fontSize;
    } else if (style.size.indexOf('pt') != -1) {
      computedStyle.size = fontSize / .75;
    } else {
      computedStyle.size = canvasFontSize;
    }

    // Different scaling between normal text and VML text. This was found using
    // trial and error to get the same size as non VML text.
    computedStyle.size *= 0.981;

    return computedStyle;
  }

  function buildStyle(style) {
    return style.style + ' ' + style.variant + ' ' + style.weight + ' ' +
        style.size + 'px ' + style.family;
  }

  function processLineCap(lineCap) {
    switch (lineCap) {
      case 'butt':
        return 'flat';
      case 'round':
        return 'round';
      case 'square':
      default:
        return 'square';
    }
  }

  /**
   * This class implements CanvasRenderingContext2D interface as described by
   * the WHATWG.
   * @param {HTMLElement} surfaceElement The element that the 2D context should
   * be associated with
   */
  function CanvasRenderingContext2D_(surfaceElement) {
    this.m_ = createMatrixIdentity();

    this.mStack_ = [];
    this.aStack_ = [];
    this.currentPath_ = [];

    // Canvas context properties
    this.strokeStyle = '#000';
    this.fillStyle = '#000';

    this.lineWidth = 1;
    this.lineJoin = 'miter';
    this.lineCap = 'butt';
    this.miterLimit = Z * 1;
    this.globalAlpha = 1;
    this.font = '10px sans-serif';
    this.textAlign = 'left';
    this.textBaseline = 'alphabetic';
    this.canvas = surfaceElement;

    var el = surfaceElement.ownerDocument.createElement('div');
    el.style.width =  surfaceElement.clientWidth + 'px';
    el.style.height = surfaceElement.clientHeight + 'px';
    el.style.overflow = 'hidden';
    el.style.position = 'absolute';
    surfaceElement.appendChild(el);

    this.element_ = el;
    this.arcScaleX_ = 1;
    this.arcScaleY_ = 1;
    this.lineScale_ = 1;
  }

  var contextPrototype = CanvasRenderingContext2D_.prototype;
  contextPrototype.clearRect = function() {
    if (this.textMeasureEl_) {
      this.textMeasureEl_.removeNode(true);
      this.textMeasureEl_ = null;
    }
    this.element_.innerHTML = '';
  };

  contextPrototype.beginPath = function() {
    // TODO: Branch current matrix so that save/restore has no effect
    //       as per safari docs.
    this.currentPath_ = [];
  };

  contextPrototype.moveTo = function(aX, aY) {
    var p = this.getCoords_(aX, aY);
    this.currentPath_.push({type: 'moveTo', x: p.x, y: p.y});
    this.currentX_ = p.x;
    this.currentY_ = p.y;
  };

  contextPrototype.lineTo = function(aX, aY) {
    var p = this.getCoords_(aX, aY);
    this.currentPath_.push({type: 'lineTo', x: p.x, y: p.y});

    this.currentX_ = p.x;
    this.currentY_ = p.y;
  };

  contextPrototype.bezierCurveTo = function(aCP1x, aCP1y,
                                            aCP2x, aCP2y,
                                            aX, aY) {
    var p = this.getCoords_(aX, aY);
    var cp1 = this.getCoords_(aCP1x, aCP1y);
    var cp2 = this.getCoords_(aCP2x, aCP2y);
    bezierCurveTo(this, cp1, cp2, p);
  };

  // Helper function that takes the already fixed cordinates.
  function bezierCurveTo(self, cp1, cp2, p) {
    self.currentPath_.push({
      type: 'bezierCurveTo',
      cp1x: cp1.x,
      cp1y: cp1.y,
      cp2x: cp2.x,
      cp2y: cp2.y,
      x: p.x,
      y: p.y
    });
    self.currentX_ = p.x;
    self.currentY_ = p.y;
  }

  contextPrototype.quadraticCurveTo = function(aCPx, aCPy, aX, aY) {
    // the following is lifted almost directly from
    // http://developer.mozilla.org/en/docs/Canvas_tutorial:Drawing_shapes

    var cp = this.getCoords_(aCPx, aCPy);
    var p = this.getCoords_(aX, aY);

    var cp1 = {
      x: this.currentX_ + 2.0 / 3.0 * (cp.x - this.currentX_),
      y: this.currentY_ + 2.0 / 3.0 * (cp.y - this.currentY_)
    };
    var cp2 = {
      x: cp1.x + (p.x - this.currentX_) / 3.0,
      y: cp1.y + (p.y - this.currentY_) / 3.0
    };

    bezierCurveTo(this, cp1, cp2, p);
  };

  contextPrototype.arc = function(aX, aY, aRadius,
                                  aStartAngle, aEndAngle, aClockwise) {
    aRadius *= Z;
    var arcType = aClockwise ? 'at' : 'wa';

    var xStart = aX + mc(aStartAngle) * aRadius - Z2;
    var yStart = aY + ms(aStartAngle) * aRadius - Z2;

    var xEnd = aX + mc(aEndAngle) * aRadius - Z2;
    var yEnd = aY + ms(aEndAngle) * aRadius - Z2;

    // IE won't render arches drawn counter clockwise if xStart == xEnd.
    if (xStart == xEnd && !aClockwise) {
      xStart += 0.125; // Offset xStart by 1/80 of a pixel. Use something
                       // that can be represented in binary
    }

    var p = this.getCoords_(aX, aY);
    var pStart = this.getCoords_(xStart, yStart);
    var pEnd = this.getCoords_(xEnd, yEnd);

    this.currentPath_.push({type: arcType,
                           x: p.x,
                           y: p.y,
                           radius: aRadius,
                           xStart: pStart.x,
                           yStart: pStart.y,
                           xEnd: pEnd.x,
                           yEnd: pEnd.y});

  };

  contextPrototype.rect = function(aX, aY, aWidth, aHeight) {
    this.moveTo(aX, aY);
    this.lineTo(aX + aWidth, aY);
    this.lineTo(aX + aWidth, aY + aHeight);
    this.lineTo(aX, aY + aHeight);
    this.closePath();
  };

  contextPrototype.strokeRect = function(aX, aY, aWidth, aHeight) {
    var oldPath = this.currentPath_;
    this.beginPath();

    this.moveTo(aX, aY);
    this.lineTo(aX + aWidth, aY);
    this.lineTo(aX + aWidth, aY + aHeight);
    this.lineTo(aX, aY + aHeight);
    this.closePath();
    this.stroke();

    this.currentPath_ = oldPath;
  };

  contextPrototype.fillRect = function(aX, aY, aWidth, aHeight) {
    var oldPath = this.currentPath_;
    this.beginPath();

    this.moveTo(aX, aY);
    this.lineTo(aX + aWidth, aY);
    this.lineTo(aX + aWidth, aY + aHeight);
    this.lineTo(aX, aY + aHeight);
    this.closePath();
    this.fill();

    this.currentPath_ = oldPath;
  };

  contextPrototype.createLinearGradient = function(aX0, aY0, aX1, aY1) {
    var gradient = new CanvasGradient_('gradient');
    gradient.x0_ = aX0;
    gradient.y0_ = aY0;
    gradient.x1_ = aX1;
    gradient.y1_ = aY1;
    return gradient;
  };

  contextPrototype.createRadialGradient = function(aX0, aY0, aR0,
                                                   aX1, aY1, aR1) {
    var gradient = new CanvasGradient_('gradientradial');
    gradient.x0_ = aX0;
    gradient.y0_ = aY0;
    gradient.r0_ = aR0;
    gradient.x1_ = aX1;
    gradient.y1_ = aY1;
    gradient.r1_ = aR1;
    return gradient;
  };

  contextPrototype.drawImage = function(image, var_args) {
    var dx, dy, dw, dh, sx, sy, sw, sh;

    // to find the original width we overide the width and height
    var oldRuntimeWidth = image.runtimeStyle.width;
    var oldRuntimeHeight = image.runtimeStyle.height;
    image.runtimeStyle.width = 'auto';
    image.runtimeStyle.height = 'auto';

    // get the original size
    var w = image.width;
    var h = image.height;

    // and remove overides
    image.runtimeStyle.width = oldRuntimeWidth;
    image.runtimeStyle.height = oldRuntimeHeight;

    if (arguments.length == 3) {
      dx = arguments[1];
      dy = arguments[2];
      sx = sy = 0;
      sw = dw = w;
      sh = dh = h;
    } else if (arguments.length == 5) {
      dx = arguments[1];
      dy = arguments[2];
      dw = arguments[3];
      dh = arguments[4];
      sx = sy = 0;
      sw = w;
      sh = h;
    } else if (arguments.length == 9) {
      sx = arguments[1];
      sy = arguments[2];
      sw = arguments[3];
      sh = arguments[4];
      dx = arguments[5];
      dy = arguments[6];
      dw = arguments[7];
      dh = arguments[8];
    } else {
      throw Error('Invalid number of arguments');
    }

    var d = this.getCoords_(dx, dy);

    var w2 = sw / 2;
    var h2 = sh / 2;

    var vmlStr = [];

    var W = 10;
    var H = 10;

    // For some reason that I've now forgotten, using divs didn't work
    vmlStr.push(' <g_vml_:group',
                ' coordsize="', Z * W, ',', Z * H, '"',
                ' coordorigin="0,0"' ,
                ' style="width:', W, 'px;height:', H, 'px;position:absolute;');

    // If filters are necessary (rotation exists), create them
    // filters are bog-slow, so only create them if abbsolutely necessary
    // The following check doesn't account for skews (which don't exist
    // in the canvas spec (yet) anyway.

    if (this.m_[0][0] != 1 || this.m_[0][1] ||
        this.m_[1][1] != 1 || this.m_[1][0]) {
      var filter = [];

      // Note the 12/21 reversal
      filter.push('M11=', this.m_[0][0], ',',
                  'M12=', this.m_[1][0], ',',
                  'M21=', this.m_[0][1], ',',
                  'M22=', this.m_[1][1], ',',
                  'Dx=', mr(d.x / Z), ',',
                  'Dy=', mr(d.y / Z), '');

      // Bounding box calculation (need to minimize displayed area so that
      // filters don't waste time on unused pixels.
      var max = d;
      var c2 = this.getCoords_(dx + dw, dy);
      var c3 = this.getCoords_(dx, dy + dh);
      var c4 = this.getCoords_(dx + dw, dy + dh);

      max.x = m.max(max.x, c2.x, c3.x, c4.x);
      max.y = m.max(max.y, c2.y, c3.y, c4.y);

      vmlStr.push('padding:0 ', mr(max.x / Z), 'px ', mr(max.y / Z),
                  'px 0;filter:progid:DXImageTransform.Microsoft.Matrix(',
                  filter.join(''), ", sizingmethod='clip');");

    } else {
      vmlStr.push('top:', mr(d.y / Z), 'px;left:', mr(d.x / Z), 'px;');
    }

    vmlStr.push(' ">' ,
                '<g_vml_:image src="', image.src, '"',
                ' style="width:', Z * dw, 'px;',
                ' height:', Z * dh, 'px"',
                ' cropleft="', sx / w, '"',
                ' croptop="', sy / h, '"',
                ' cropright="', (w - sx - sw) / w, '"',
                ' cropbottom="', (h - sy - sh) / h, '"',
                ' />',
                '</g_vml_:group>');

    this.element_.insertAdjacentHTML('BeforeEnd', vmlStr.join(''));
  };

  contextPrototype.stroke = function(aFill) {
    var W = 10;
    var H = 10;
    // Divide the shape into chunks if it's too long because IE has a limit
    // somewhere for how long a VML shape can be. This simple division does
    // not work with fills, only strokes, unfortunately.
    var chunkSize = 5000;

    var min = {x: null, y: null};
    var max = {x: null, y: null};

    for (var j = 0; j < this.currentPath_.length; j += chunkSize) {
      var lineStr = [];
      var lineOpen = false;

      lineStr.push('<g_vml_:shape',
                   ' filled="', !!aFill, '"',
                   ' style="position:absolute;width:', W, 'px;height:', H, 'px;"',
                   ' coordorigin="0,0"',
                   ' coordsize="', Z * W, ',', Z * H, '"',
                   ' stroked="', !aFill, '"',
                   ' path="');

      var newSeq = false;

      for (var i = j; i < Math.min(j + chunkSize, this.currentPath_.length); i++) {
        if (i % chunkSize == 0 && i > 0) { // move into position for next chunk
          lineStr.push(' m ', mr(this.currentPath_[i-1].x), ',', mr(this.currentPath_[i-1].y));
        }

        var p = this.currentPath_[i];
        var c;

        switch (p.type) {
          case 'moveTo':
            c = p;
            lineStr.push(' m ', mr(p.x), ',', mr(p.y));
            break;
          case 'lineTo':
            lineStr.push(' l ', mr(p.x), ',', mr(p.y));
            break;
          case 'close':
            lineStr.push(' x ');
            p = null;
            break;
          case 'bezierCurveTo':
            lineStr.push(' c ',
                         mr(p.cp1x), ',', mr(p.cp1y), ',',
                         mr(p.cp2x), ',', mr(p.cp2y), ',',
                         mr(p.x), ',', mr(p.y));
            break;
          case 'at':
          case 'wa':
            lineStr.push(' ', p.type, ' ',
                         mr(p.x - this.arcScaleX_ * p.radius), ',',
                         mr(p.y - this.arcScaleY_ * p.radius), ' ',
                         mr(p.x + this.arcScaleX_ * p.radius), ',',
                         mr(p.y + this.arcScaleY_ * p.radius), ' ',
                         mr(p.xStart), ',', mr(p.yStart), ' ',
                         mr(p.xEnd), ',', mr(p.yEnd));
            break;
        }
  
  
        // TODO: Following is broken for curves due to
        //       move to proper paths.
  
        // Figure out dimensions so we can do gradient fills
        // properly
        if (p) {
          if (min.x == null || p.x < min.x) {
            min.x = p.x;
          }
          if (max.x == null || p.x > max.x) {
            max.x = p.x;
          }
          if (min.y == null || p.y < min.y) {
            min.y = p.y;
          }
          if (max.y == null || p.y > max.y) {
            max.y = p.y;
          }
        }
      }
      lineStr.push(' ">');
  
      if (!aFill) {
        appendStroke(this, lineStr);
      } else {
        appendFill(this, lineStr, min, max);
      }
  
      lineStr.push('</g_vml_:shape>');
  
      this.element_.insertAdjacentHTML('beforeEnd', lineStr.join(''));
    }
  };

  function appendStroke(ctx, lineStr) {
    var a = processStyle(ctx.strokeStyle);
    var color = a.color;
    var opacity = a.alpha * ctx.globalAlpha;
    var lineWidth = ctx.lineScale_ * ctx.lineWidth;

    // VML cannot correctly render a line if the width is less than 1px.
    // In that case, we dilute the color to make the line look thinner.
    if (lineWidth < 1) {
      opacity *= lineWidth;
    }

    lineStr.push(
      '<g_vml_:stroke',
      ' opacity="', opacity, '"',
      ' joinstyle="', ctx.lineJoin, '"',
      ' miterlimit="', ctx.miterLimit, '"',
      ' endcap="', processLineCap(ctx.lineCap), '"',
      ' weight="', lineWidth, 'px"',
      ' color="', color, '" />'
    );
  }

  function appendFill(ctx, lineStr, min, max) {
    var fillStyle = ctx.fillStyle;
    var arcScaleX = ctx.arcScaleX_;
    var arcScaleY = ctx.arcScaleY_;
    var width = max.x - min.x;
    var height = max.y - min.y;
    if (fillStyle instanceof CanvasGradient_) {
      // TODO: Gradients transformed with the transformation matrix.
      var angle = 0;
      var focus = {x: 0, y: 0};

      // additional offset
      var shift = 0;
      // scale factor for offset
      var expansion = 1;

      if (fillStyle.type_ == 'gradient') {
        var x0 = fillStyle.x0_ / arcScaleX;
        var y0 = fillStyle.y0_ / arcScaleY;
        var x1 = fillStyle.x1_ / arcScaleX;
        var y1 = fillStyle.y1_ / arcScaleY;
        var p0 = ctx.getCoords_(x0, y0);
        var p1 = ctx.getCoords_(x1, y1);
        var dx = p1.x - p0.x;
        var dy = p1.y - p0.y;
        angle = Math.atan2(dx, dy) * 180 / Math.PI;

        // The angle should be a non-negative number.
        if (angle < 0) {
          angle += 360;
        }

        // Very small angles produce an unexpected result because they are
        // converted to a scientific notation string.
        if (angle < 1e-6) {
          angle = 0;
        }
      } else {
        var p0 = ctx.getCoords_(fillStyle.x0_, fillStyle.y0_);
        focus = {
          x: (p0.x - min.x) / width,
          y: (p0.y - min.y) / height
        };

        width  /= arcScaleX * Z;
        height /= arcScaleY * Z;
        var dimension = m.max(width, height);
        shift = 2 * fillStyle.r0_ / dimension;
        expansion = 2 * fillStyle.r1_ / dimension - shift;
      }

      // We need to sort the color stops in ascending order by offset,
      // otherwise IE won't interpret it correctly.
      var stops = fillStyle.colors_;
      stops.sort(function(cs1, cs2) {
        return cs1.offset - cs2.offset;
      });

      var length = stops.length;
      var color1 = stops[0].color;
      var color2 = stops[length - 1].color;
      var opacity1 = stops[0].alpha * ctx.globalAlpha;
      var opacity2 = stops[length - 1].alpha * ctx.globalAlpha;

      var colors = [];
      for (var i = 0; i < length; i++) {
        var stop = stops[i];
        colors.push(stop.offset * expansion + shift + ' ' + stop.color);
      }

      // When colors attribute is used, the meanings of opacity and o:opacity2
      // are reversed.
      lineStr.push('<g_vml_:fill type="', fillStyle.type_, '"',
                   ' method="none" focus="100%"',
                   ' color="', color1, '"',
                   ' color2="', color2, '"',
                   ' colors="', colors.join(','), '"',
                   ' opacity="', opacity2, '"',
                   ' g_o_:opacity2="', opacity1, '"',
                   ' angle="', angle, '"',
                   ' focusposition="', focus.x, ',', focus.y, '" />');
    } else if (fillStyle instanceof CanvasPattern_) {
      if (width && height) {
        var deltaLeft = -min.x;
        var deltaTop = -min.y;
        lineStr.push('<g_vml_:fill',
                     ' position="',
                     deltaLeft / width * arcScaleX * arcScaleX, ',',
                     deltaTop / height * arcScaleY * arcScaleY, '"',
                     ' type="tile"',
                     // TODO: Figure out the correct size to fit the scale.
                     //' size="', w, 'px ', h, 'px"',
                     ' src="', fillStyle.src_, '" />');
       }
    } else {
      var a = processStyle(ctx.fillStyle);
      var color = a.color;
      var opacity = a.alpha * ctx.globalAlpha;
      lineStr.push('<g_vml_:fill color="', color, '" opacity="', opacity,
                   '" />');
    }
  }

  contextPrototype.fill = function() {
    this.stroke(true);
  };

  contextPrototype.closePath = function() {
    this.currentPath_.push({type: 'close'});
  };

  /**
   * @private
   */
  contextPrototype.getCoords_ = function(aX, aY) {
    var m = this.m_;
    return {
      x: Z * (aX * m[0][0] + aY * m[1][0] + m[2][0]) - Z2,
      y: Z * (aX * m[0][1] + aY * m[1][1] + m[2][1]) - Z2
    };
  };

  contextPrototype.save = function() {
    var o = {};
    copyState(this, o);
    this.aStack_.push(o);
    this.mStack_.push(this.m_);
    this.m_ = matrixMultiply(createMatrixIdentity(), this.m_);
  };

  contextPrototype.restore = function() {
    if (this.aStack_.length) {
      copyState(this.aStack_.pop(), this);
      this.m_ = this.mStack_.pop();
    }
  };

  function matrixIsFinite(m) {
    return isFinite(m[0][0]) && isFinite(m[0][1]) &&
        isFinite(m[1][0]) && isFinite(m[1][1]) &&
        isFinite(m[2][0]) && isFinite(m[2][1]);
  }

  function setM(ctx, m, updateLineScale) {
    if (!matrixIsFinite(m)) {
      return;
    }
    ctx.m_ = m;

    if (updateLineScale) {
      // Get the line scale.
      // Determinant of this.m_ means how much the area is enlarged by the
      // transformation. So its square root can be used as a scale factor
      // for width.
      var det = m[0][0] * m[1][1] - m[0][1] * m[1][0];
      ctx.lineScale_ = sqrt(abs(det));
    }
  }

  contextPrototype.translate = function(aX, aY) {
    var m1 = [
      [1,  0,  0],
      [0,  1,  0],
      [aX, aY, 1]
    ];

    setM(this, matrixMultiply(m1, this.m_), false);
  };

  contextPrototype.rotate = function(aRot) {
    var c = mc(aRot);
    var s = ms(aRot);

    var m1 = [
      [c,  s, 0],
      [-s, c, 0],
      [0,  0, 1]
    ];

    setM(this, matrixMultiply(m1, this.m_), false);
  };

  contextPrototype.scale = function(aX, aY) {
    this.arcScaleX_ *= aX;
    this.arcScaleY_ *= aY;
    var m1 = [
      [aX, 0,  0],
      [0,  aY, 0],
      [0,  0,  1]
    ];

    setM(this, matrixMultiply(m1, this.m_), true);
  };

  contextPrototype.transform = function(m11, m12, m21, m22, dx, dy) {
    var m1 = [
      [m11, m12, 0],
      [m21, m22, 0],
      [dx,  dy,  1]
    ];

    setM(this, matrixMultiply(m1, this.m_), true);
  };

  contextPrototype.setTransform = function(m11, m12, m21, m22, dx, dy) {
    var m = [
      [m11, m12, 0],
      [m21, m22, 0],
      [dx,  dy,  1]
    ];

    setM(this, m, true);
  };

  /**
   * The text drawing function.
   * The maxWidth argument isn't taken in account, since no browser supports
   * it yet.
   */
  contextPrototype.drawText_ = function(text, x, y, maxWidth, stroke) {
    var m = this.m_,
        delta = 1000,
        left = 0,
        right = delta,
        offset = {x: 0, y: 0},
        lineStr = [];

    var fontStyle = getComputedStyle(processFontStyle(this.font),
                                     this.element_);

    var fontStyleString = buildStyle(fontStyle);

    var elementStyle = this.element_.currentStyle;
    var textAlign = this.textAlign.toLowerCase();
    switch (textAlign) {
      case 'left':
      case 'center':
      case 'right':
        break;
      case 'end':
        textAlign = elementStyle.direction == 'ltr' ? 'right' : 'left';
        break;
      case 'start':
        textAlign = elementStyle.direction == 'rtl' ? 'right' : 'left';
        break;
      default:
        textAlign = 'left';
    }

    // 1.75 is an arbitrary number, as there is no info about the text baseline
    switch (this.textBaseline) {
      case 'hanging':
      case 'top':
        offset.y = fontStyle.size / 1.75;
        break;
      case 'middle':
        break;
      default:
      case null:
      case 'alphabetic':
      case 'ideographic':
      case 'bottom':
        offset.y = -fontStyle.size / 2.25;
        break;
    }

    switch(textAlign) {
      case 'right':
        left = delta;
        right = 0.05;
        break;
      case 'center':
        left = right = delta / 2;
        break;
    }

    var d = this.getCoords_(x + offset.x, y + offset.y);

    lineStr.push('<g_vml_:line from="', -left ,' 0" to="', right ,' 0.05" ',
                 ' coordsize="100 100" coordorigin="0 0"',
                 ' filled="', !stroke, '" stroked="', !!stroke,
                 '" style="position:absolute;width:1px;height:1px;">');

    if (stroke) {
      appendStroke(this, lineStr);
    } else {
      // TODO: Fix the min and max params.
      appendFill(this, lineStr, {x: -left, y: 0},
                 {x: right, y: fontStyle.size});
    }

    var skewM = m[0][0].toFixed(3) + ',' + m[1][0].toFixed(3) + ',' +
                m[0][1].toFixed(3) + ',' + m[1][1].toFixed(3) + ',0,0';

    var skewOffset = mr(d.x / Z) + ',' + mr(d.y / Z);

    lineStr.push('<g_vml_:skew on="t" matrix="', skewM ,'" ',
                 ' offset="', skewOffset, '" origin="', left ,' 0" />',
                 '<g_vml_:path textpathok="true" />',
                 '<g_vml_:textpath on="true" string="',
                 encodeHtmlAttribute(text),
                 '" style="v-text-align:', textAlign,
                 ';font:', encodeHtmlAttribute(fontStyleString),
                 '" /></g_vml_:line>');

    this.element_.insertAdjacentHTML('beforeEnd', lineStr.join(''));
  };

  contextPrototype.fillText = function(text, x, y, maxWidth) {
    this.drawText_(text, x, y, maxWidth, false);
  };

  contextPrototype.strokeText = function(text, x, y, maxWidth) {
    this.drawText_(text, x, y, maxWidth, true);
  };

  contextPrototype.measureText = function(text) {
    if (!this.textMeasureEl_) {
      var s = '<span style="position:absolute;' +
          'top:-20000px;left:0;padding:0;margin:0;border:none;' +
          'white-space:pre;"></span>';
      this.element_.insertAdjacentHTML('beforeEnd', s);
      this.textMeasureEl_ = this.element_.lastChild;
    }
    var doc = this.element_.ownerDocument;
    this.textMeasureEl_.innerHTML = '';
    this.textMeasureEl_.style.font = this.font;
    // Don't use innerHTML or innerText because they allow markup/whitespace.
    this.textMeasureEl_.appendChild(doc.createTextNode(text));
    return {width: this.textMeasureEl_.offsetWidth};
  };

  /******** STUBS ********/
  contextPrototype.clip = function() {
    // TODO: Implement
  };

  contextPrototype.arcTo = function() {
    // TODO: Implement
  };

  contextPrototype.createPattern = function(image, repetition) {
    return new CanvasPattern_(image, repetition);
  };

  // Gradient / Pattern Stubs
  function CanvasGradient_(aType) {
    this.type_ = aType;
    this.x0_ = 0;
    this.y0_ = 0;
    this.r0_ = 0;
    this.x1_ = 0;
    this.y1_ = 0;
    this.r1_ = 0;
    this.colors_ = [];
  }

  CanvasGradient_.prototype.addColorStop = function(aOffset, aColor) {
    aColor = processStyle(aColor);
    this.colors_.push({offset: aOffset,
                       color: aColor.color,
                       alpha: aColor.alpha});
  };

  function CanvasPattern_(image, repetition) {
    assertImageIsValid(image);
    switch (repetition) {
      case 'repeat':
      case null:
      case '':
        this.repetition_ = 'repeat';
        break
      case 'repeat-x':
      case 'repeat-y':
      case 'no-repeat':
        this.repetition_ = repetition;
        break;
      default:
        throwException('SYNTAX_ERR');
    }

    this.src_ = image.src;
    this.width_ = image.width;
    this.height_ = image.height;
  }

  function throwException(s) {
    throw new DOMException_(s);
  }

  function assertImageIsValid(img) {
    if (!img || img.nodeType != 1 || img.tagName != 'IMG') {
      throwException('TYPE_MISMATCH_ERR');
    }
    if (img.readyState != 'complete') {
      throwException('INVALID_STATE_ERR');
    }
  }

  function DOMException_(s) {
    this.code = this[s];
    this.message = s +': DOM Exception ' + this.code;
  }
  var p = DOMException_.prototype = new Error;
  p.INDEX_SIZE_ERR = 1;
  p.DOMSTRING_SIZE_ERR = 2;
  p.HIERARCHY_REQUEST_ERR = 3;
  p.WRONG_DOCUMENT_ERR = 4;
  p.INVALID_CHARACTER_ERR = 5;
  p.NO_DATA_ALLOWED_ERR = 6;
  p.NO_MODIFICATION_ALLOWED_ERR = 7;
  p.NOT_FOUND_ERR = 8;
  p.NOT_SUPPORTED_ERR = 9;
  p.INUSE_ATTRIBUTE_ERR = 10;
  p.INVALID_STATE_ERR = 11;
  p.SYNTAX_ERR = 12;
  p.INVALID_MODIFICATION_ERR = 13;
  p.NAMESPACE_ERR = 14;
  p.INVALID_ACCESS_ERR = 15;
  p.VALIDATION_ERR = 16;
  p.TYPE_MISMATCH_ERR = 17;

  // set up externs
  G_vmlCanvasManager = G_vmlCanvasManager_;
  CanvasRenderingContext2D = CanvasRenderingContext2D_;
  CanvasGradient = CanvasGradient_;
  CanvasPattern = CanvasPattern_;
  DOMException = DOMException_;
})();

} // if

/* Javascript plotting library for jQuery, v. 0.7.
 *
 * Released under the MIT license by IOLA, December 2007.
 *
 */
(function(b){b.color={};b.color.make=function(d,e,g,f){var c={};c.r=d||0;c.g=e||0;c.b=g||0;c.a=f!=null?f:1;c.add=function(h,j){for(var k=0;k<h.length;++k){c[h.charAt(k)]+=j}return c.normalize()};c.scale=function(h,j){for(var k=0;k<h.length;++k){c[h.charAt(k)]*=j}return c.normalize()};c.toString=function(){if(c.a>=1){return"rgb("+[c.r,c.g,c.b].join(",")+")"}else{return"rgba("+[c.r,c.g,c.b,c.a].join(",")+")"}};c.normalize=function(){function h(k,j,l){return j<k?k:(j>l?l:j)}c.r=h(0,parseInt(c.r),255);c.g=h(0,parseInt(c.g),255);c.b=h(0,parseInt(c.b),255);c.a=h(0,c.a,1);return c};c.clone=function(){return b.color.make(c.r,c.b,c.g,c.a)};return c.normalize()};b.color.extract=function(d,e){var c;do{c=d.css(e).toLowerCase();if(c!=""&&c!="transparent"){break}d=d.parent()}while(!b.nodeName(d.get(0),"body"));if(c=="rgba(0, 0, 0, 0)"){c="transparent"}return b.color.parse(c)};b.color.parse=function(c){var d,f=b.color.make;if(d=/rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(c)){return f(parseInt(d[1],10),parseInt(d[2],10),parseInt(d[3],10))}if(d=/rgba\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)/.exec(c)){return f(parseInt(d[1],10),parseInt(d[2],10),parseInt(d[3],10),parseFloat(d[4]))}if(d=/rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(c)){return f(parseFloat(d[1])*2.55,parseFloat(d[2])*2.55,parseFloat(d[3])*2.55)}if(d=/rgba\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)/.exec(c)){return f(parseFloat(d[1])*2.55,parseFloat(d[2])*2.55,parseFloat(d[3])*2.55,parseFloat(d[4]))}if(d=/#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(c)){return f(parseInt(d[1],16),parseInt(d[2],16),parseInt(d[3],16))}if(d=/#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(c)){return f(parseInt(d[1]+d[1],16),parseInt(d[2]+d[2],16),parseInt(d[3]+d[3],16))}var e=b.trim(c).toLowerCase();if(e=="transparent"){return f(255,255,255,0)}else{d=a[e]||[0,0,0];return f(d[0],d[1],d[2])}};var a={aqua:[0,255,255],azure:[240,255,255],beige:[245,245,220],black:[0,0,0],blue:[0,0,255],brown:[165,42,42],cyan:[0,255,255],darkblue:[0,0,139],darkcyan:[0,139,139],darkgrey:[169,169,169],darkgreen:[0,100,0],darkkhaki:[189,183,107],darkmagenta:[139,0,139],darkolivegreen:[85,107,47],darkorange:[255,140,0],darkorchid:[153,50,204],darkred:[139,0,0],darksalmon:[233,150,122],darkviolet:[148,0,211],fuchsia:[255,0,255],gold:[255,215,0],green:[0,128,0],indigo:[75,0,130],khaki:[240,230,140],lightblue:[173,216,230],lightcyan:[224,255,255],lightgreen:[144,238,144],lightgrey:[211,211,211],lightpink:[255,182,193],lightyellow:[255,255,224],lime:[0,255,0],magenta:[255,0,255],maroon:[128,0,0],navy:[0,0,128],olive:[128,128,0],orange:[255,165,0],pink:[255,192,203],purple:[128,0,128],violet:[128,0,128],red:[255,0,0],silver:[192,192,192],white:[255,255,255],yellow:[255,255,0]}})(jQuery);(function(c){function b(av,ai,J,af){var Q=[],O={colors:["#edc240","#afd8f8","#cb4b4b","#4da74d","#9440ed"],legend:{show:true,noColumns:1,labelFormatter:null,labelBoxBorderColor:"#ccc",container:null,position:"ne",margin:5,backgroundColor:null,backgroundOpacity:0.85},xaxis:{show:null,position:"bottom",mode:null,color:null,tickColor:null,transform:null,inverseTransform:null,min:null,max:null,autoscaleMargin:null,ticks:null,tickFormatter:null,labelWidth:null,labelHeight:null,reserveSpace:null,tickLength:null,alignTicksWithAxis:null,tickDecimals:null,tickSize:null,minTickSize:null,monthNames:null,timeformat:null,twelveHourClock:false},yaxis:{autoscaleMargin:0.02,position:"left"},xaxes:[],yaxes:[],series:{points:{show:false,radius:3,lineWidth:2,fill:true,fillColor:"#ffffff",symbol:"circle"},lines:{lineWidth:2,fill:false,fillColor:null,steps:false},bars:{show:false,lineWidth:2,barWidth:1,fill:true,fillColor:null,align:"left",horizontal:false},shadowSize:3},grid:{show:true,aboveData:false,color:"#545454",backgroundColor:null,borderColor:null,tickColor:null,labelMargin:5,axisMargin:8,borderWidth:2,minBorderMargin:null,markings:null,markingsColor:"#f4f4f4",markingsLineWidth:2,clickable:false,hoverable:false,autoHighlight:true,mouseActiveRadius:10},hooks:{}},az=null,ad=null,y=null,H=null,A=null,p=[],aw=[],q={left:0,right:0,top:0,bottom:0},G=0,I=0,h=0,w=0,ak={processOptions:[],processRawData:[],processDatapoints:[],drawSeries:[],draw:[],bindEvents:[],drawOverlay:[],shutdown:[]},aq=this;aq.setData=aj;aq.setupGrid=t;aq.draw=W;aq.getPlaceholder=function(){return av};aq.getCanvas=function(){return az};aq.getPlotOffset=function(){return q};aq.width=function(){return h};aq.height=function(){return w};aq.offset=function(){var aB=y.offset();aB.left+=q.left;aB.top+=q.top;return aB};aq.getData=function(){return Q};aq.getAxes=function(){var aC={},aB;c.each(p.concat(aw),function(aD,aE){if(aE){aC[aE.direction+(aE.n!=1?aE.n:"")+"axis"]=aE}});return aC};aq.getXAxes=function(){return p};aq.getYAxes=function(){return aw};aq.c2p=C;aq.p2c=ar;aq.getOptions=function(){return O};aq.highlight=x;aq.unhighlight=T;aq.triggerRedrawOverlay=f;aq.pointOffset=function(aB){return{left:parseInt(p[aA(aB,"x")-1].p2c(+aB.x)+q.left),top:parseInt(aw[aA(aB,"y")-1].p2c(+aB.y)+q.top)}};aq.shutdown=ag;aq.resize=function(){B();g(az);g(ad)};aq.hooks=ak;F(aq);Z(J);X();aj(ai);t();W();ah();function an(aD,aB){aB=[aq].concat(aB);for(var aC=0;aC<aD.length;++aC){aD[aC].apply(this,aB)}}function F(){for(var aB=0;aB<af.length;++aB){var aC=af[aB];aC.init(aq);if(aC.options){c.extend(true,O,aC.options)}}}function Z(aC){var aB;c.extend(true,O,aC);if(O.xaxis.color==null){O.xaxis.color=O.grid.color}if(O.yaxis.color==null){O.yaxis.color=O.grid.color}if(O.xaxis.tickColor==null){O.xaxis.tickColor=O.grid.tickColor}if(O.yaxis.tickColor==null){O.yaxis.tickColor=O.grid.tickColor}if(O.grid.borderColor==null){O.grid.borderColor=O.grid.color}if(O.grid.tickColor==null){O.grid.tickColor=c.color.parse(O.grid.color).scale("a",0.22).toString()}for(aB=0;aB<Math.max(1,O.xaxes.length);++aB){O.xaxes[aB]=c.extend(true,{},O.xaxis,O.xaxes[aB])}for(aB=0;aB<Math.max(1,O.yaxes.length);++aB){O.yaxes[aB]=c.extend(true,{},O.yaxis,O.yaxes[aB])}if(O.xaxis.noTicks&&O.xaxis.ticks==null){O.xaxis.ticks=O.xaxis.noTicks}if(O.yaxis.noTicks&&O.yaxis.ticks==null){O.yaxis.ticks=O.yaxis.noTicks}if(O.x2axis){O.xaxes[1]=c.extend(true,{},O.xaxis,O.x2axis);O.xaxes[1].position="top"}if(O.y2axis){O.yaxes[1]=c.extend(true,{},O.yaxis,O.y2axis);O.yaxes[1].position="right"}if(O.grid.coloredAreas){O.grid.markings=O.grid.coloredAreas}if(O.grid.coloredAreasColor){O.grid.markingsColor=O.grid.coloredAreasColor}if(O.lines){c.extend(true,O.series.lines,O.lines)}if(O.points){c.extend(true,O.series.points,O.points)}if(O.bars){c.extend(true,O.series.bars,O.bars)}if(O.shadowSize!=null){O.series.shadowSize=O.shadowSize}for(aB=0;aB<O.xaxes.length;++aB){V(p,aB+1).options=O.xaxes[aB]}for(aB=0;aB<O.yaxes.length;++aB){V(aw,aB+1).options=O.yaxes[aB]}for(var aD in ak){if(O.hooks[aD]&&O.hooks[aD].length){ak[aD]=ak[aD].concat(O.hooks[aD])}}an(ak.processOptions,[O])}function aj(aB){Q=Y(aB);ax();z()}function Y(aE){var aC=[];for(var aB=0;aB<aE.length;++aB){var aD=c.extend(true,{},O.series);if(aE[aB].data!=null){aD.data=aE[aB].data;delete aE[aB].data;c.extend(true,aD,aE[aB]);aE[aB].data=aD.data}else{aD.data=aE[aB]}aC.push(aD)}return aC}function aA(aC,aD){var aB=aC[aD+"axis"];if(typeof aB=="object"){aB=aB.n}if(typeof aB!="number"){aB=1}return aB}function m(){return c.grep(p.concat(aw),function(aB){return aB})}function C(aE){var aC={},aB,aD;for(aB=0;aB<p.length;++aB){aD=p[aB];if(aD&&aD.used){aC["x"+aD.n]=aD.c2p(aE.left)}}for(aB=0;aB<aw.length;++aB){aD=aw[aB];if(aD&&aD.used){aC["y"+aD.n]=aD.c2p(aE.top)}}if(aC.x1!==undefined){aC.x=aC.x1}if(aC.y1!==undefined){aC.y=aC.y1}return aC}function ar(aF){var aD={},aC,aE,aB;for(aC=0;aC<p.length;++aC){aE=p[aC];if(aE&&aE.used){aB="x"+aE.n;if(aF[aB]==null&&aE.n==1){aB="x"}if(aF[aB]!=null){aD.left=aE.p2c(aF[aB]);break}}}for(aC=0;aC<aw.length;++aC){aE=aw[aC];if(aE&&aE.used){aB="y"+aE.n;if(aF[aB]==null&&aE.n==1){aB="y"}if(aF[aB]!=null){aD.top=aE.p2c(aF[aB]);break}}}return aD}function V(aC,aB){if(!aC[aB-1]){aC[aB-1]={n:aB,direction:aC==p?"x":"y",options:c.extend(true,{},aC==p?O.xaxis:O.yaxis)}}return aC[aB-1]}function ax(){var aG;var aM=Q.length,aB=[],aE=[];for(aG=0;aG<Q.length;++aG){var aJ=Q[aG].color;if(aJ!=null){--aM;if(typeof aJ=="number"){aE.push(aJ)}else{aB.push(c.color.parse(Q[aG].color))}}}for(aG=0;aG<aE.length;++aG){aM=Math.max(aM,aE[aG]+1)}var aC=[],aF=0;aG=0;while(aC.length<aM){var aI;if(O.colors.length==aG){aI=c.color.make(100,100,100)}else{aI=c.color.parse(O.colors[aG])}var aD=aF%2==1?-1:1;aI.scale("rgb",1+aD*Math.ceil(aF/2)*0.2);aC.push(aI);++aG;if(aG>=O.colors.length){aG=0;++aF}}var aH=0,aN;for(aG=0;aG<Q.length;++aG){aN=Q[aG];if(aN.color==null){aN.color=aC[aH].toString();++aH}else{if(typeof aN.color=="number"){aN.color=aC[aN.color].toString()}}if(aN.lines.show==null){var aL,aK=true;for(aL in aN){if(aN[aL]&&aN[aL].show){aK=false;break}}if(aK){aN.lines.show=true}}aN.xaxis=V(p,aA(aN,"x"));aN.yaxis=V(aw,aA(aN,"y"))}}function z(){var aO=Number.POSITIVE_INFINITY,aI=Number.NEGATIVE_INFINITY,aB=Number.MAX_VALUE,aU,aS,aR,aN,aD,aJ,aT,aP,aH,aG,aC,a0,aX,aL;function aF(a3,a2,a1){if(a2<a3.datamin&&a2!=-aB){a3.datamin=a2}if(a1>a3.datamax&&a1!=aB){a3.datamax=a1}}c.each(m(),function(a1,a2){a2.datamin=aO;a2.datamax=aI;a2.used=false});for(aU=0;aU<Q.length;++aU){aJ=Q[aU];aJ.datapoints={points:[]};an(ak.processRawData,[aJ,aJ.data,aJ.datapoints])}for(aU=0;aU<Q.length;++aU){aJ=Q[aU];var aZ=aJ.data,aW=aJ.datapoints.format;if(!aW){aW=[];aW.push({x:true,number:true,required:true});aW.push({y:true,number:true,required:true});if(aJ.bars.show||(aJ.lines.show&&aJ.lines.fill)){aW.push({y:true,number:true,required:false,defaultValue:0});if(aJ.bars.horizontal){delete aW[aW.length-1].y;aW[aW.length-1].x=true}}aJ.datapoints.format=aW}if(aJ.datapoints.pointsize!=null){continue}aJ.datapoints.pointsize=aW.length;aP=aJ.datapoints.pointsize;aT=aJ.datapoints.points;insertSteps=aJ.lines.show&&aJ.lines.steps;aJ.xaxis.used=aJ.yaxis.used=true;for(aS=aR=0;aS<aZ.length;++aS,aR+=aP){aL=aZ[aS];var aE=aL==null;if(!aE){for(aN=0;aN<aP;++aN){a0=aL[aN];aX=aW[aN];if(aX){if(aX.number&&a0!=null){a0=+a0;if(isNaN(a0)){a0=null}else{if(a0==Infinity){a0=aB}else{if(a0==-Infinity){a0=-aB}}}}if(a0==null){if(aX.required){aE=true}if(aX.defaultValue!=null){a0=aX.defaultValue}}}aT[aR+aN]=a0}}if(aE){for(aN=0;aN<aP;++aN){a0=aT[aR+aN];if(a0!=null){aX=aW[aN];if(aX.x){aF(aJ.xaxis,a0,a0)}if(aX.y){aF(aJ.yaxis,a0,a0)}}aT[aR+aN]=null}}else{if(insertSteps&&aR>0&&aT[aR-aP]!=null&&aT[aR-aP]!=aT[aR]&&aT[aR-aP+1]!=aT[aR+1]){for(aN=0;aN<aP;++aN){aT[aR+aP+aN]=aT[aR+aN]}aT[aR+1]=aT[aR-aP+1];aR+=aP}}}}for(aU=0;aU<Q.length;++aU){aJ=Q[aU];an(ak.processDatapoints,[aJ,aJ.datapoints])}for(aU=0;aU<Q.length;++aU){aJ=Q[aU];aT=aJ.datapoints.points,aP=aJ.datapoints.pointsize;var aK=aO,aQ=aO,aM=aI,aV=aI;for(aS=0;aS<aT.length;aS+=aP){if(aT[aS]==null){continue}for(aN=0;aN<aP;++aN){a0=aT[aS+aN];aX=aW[aN];if(!aX||a0==aB||a0==-aB){continue}if(aX.x){if(a0<aK){aK=a0}if(a0>aM){aM=a0}}if(aX.y){if(a0<aQ){aQ=a0}if(a0>aV){aV=a0}}}}if(aJ.bars.show){var aY=aJ.bars.align=="left"?0:-aJ.bars.barWidth/2;if(aJ.bars.horizontal){aQ+=aY;aV+=aY+aJ.bars.barWidth}else{aK+=aY;aM+=aY+aJ.bars.barWidth}}aF(aJ.xaxis,aK,aM);aF(aJ.yaxis,aQ,aV)}c.each(m(),function(a1,a2){if(a2.datamin==aO){a2.datamin=null}if(a2.datamax==aI){a2.datamax=null}})}function j(aB,aC){var aD=document.createElement("canvas");aD.className=aC;aD.width=G;aD.height=I;if(!aB){c(aD).css({position:"absolute",left:0,top:0})}c(aD).appendTo(av);if(!aD.getContext){aD=window.G_vmlCanvasManager.initElement(aD)}aD.getContext("2d").save();return aD}function B(){G=av.width();I=av.height();if(G<=0||I<=0){throw"Invalid dimensions for plot, width = "+G+", height = "+I}}function g(aC){if(aC.width!=G){aC.width=G}if(aC.height!=I){aC.height=I}var aB=aC.getContext("2d");aB.restore();aB.save()}function X(){var aC,aB=av.children("canvas.base"),aD=av.children("canvas.overlay");if(aB.length==0||aD==0){av.html("");av.css({padding:0});if(av.css("position")=="static"){av.css("position","relative")}B();az=j(true,"base");ad=j(false,"overlay");aC=false}else{az=aB.get(0);ad=aD.get(0);aC=true}H=az.getContext("2d");A=ad.getContext("2d");y=c([ad,az]);if(aC){av.data("plot").shutdown();aq.resize();A.clearRect(0,0,G,I);y.unbind();av.children().not([az,ad]).remove()}av.data("plot",aq)}function ah(){if(O.grid.hoverable){y.mousemove(aa);y.mouseleave(l)}if(O.grid.clickable){y.click(R)}an(ak.bindEvents,[y])}function ag(){if(M){clearTimeout(M)}y.unbind("mousemove",aa);y.unbind("mouseleave",l);y.unbind("click",R);an(ak.shutdown,[y])}function r(aG){function aC(aH){return aH}var aF,aB,aD=aG.options.transform||aC,aE=aG.options.inverseTransform;if(aG.direction=="x"){aF=aG.scale=h/Math.abs(aD(aG.max)-aD(aG.min));aB=Math.min(aD(aG.max),aD(aG.min))}else{aF=aG.scale=w/Math.abs(aD(aG.max)-aD(aG.min));aF=-aF;aB=Math.max(aD(aG.max),aD(aG.min))}if(aD==aC){aG.p2c=function(aH){return(aH-aB)*aF}}else{aG.p2c=function(aH){return(aD(aH)-aB)*aF}}if(!aE){aG.c2p=function(aH){return aB+aH/aF}}else{aG.c2p=function(aH){return aE(aB+aH/aF)}}}function L(aD){var aB=aD.options,aF,aJ=aD.ticks||[],aI=[],aE,aK=aB.labelWidth,aG=aB.labelHeight,aC;function aH(aM,aL){return c('<div style="position:absolute;top:-10000px;'+aL+'font-size:smaller"><div class="'+aD.direction+"Axis "+aD.direction+aD.n+'Axis">'+aM.join("")+"</div></div>").appendTo(av)}if(aD.direction=="x"){if(aK==null){aK=Math.floor(G/(aJ.length>0?aJ.length:1))}if(aG==null){aI=[];for(aF=0;aF<aJ.length;++aF){aE=aJ[aF].label;if(aE){aI.push('<div class="tickLabel" style="float:left;width:'+aK+'px">'+aE+"</div>")}}if(aI.length>0){aI.push('<div style="clear:left"></div>');aC=aH(aI,"width:10000px;");aG=aC.height();aC.remove()}}}else{if(aK==null||aG==null){for(aF=0;aF<aJ.length;++aF){aE=aJ[aF].label;if(aE){aI.push('<div class="tickLabel">'+aE+"</div>")}}if(aI.length>0){aC=aH(aI,"");if(aK==null){aK=aC.children().width()}if(aG==null){aG=aC.find("div.tickLabel").height()}aC.remove()}}}if(aK==null){aK=0}if(aG==null){aG=0}aD.labelWidth=aK;aD.labelHeight=aG}function au(aD){var aC=aD.labelWidth,aL=aD.labelHeight,aH=aD.options.position,aF=aD.options.tickLength,aG=O.grid.axisMargin,aJ=O.grid.labelMargin,aK=aD.direction=="x"?p:aw,aE;var aB=c.grep(aK,function(aN){return aN&&aN.options.position==aH&&aN.reserveSpace});if(c.inArray(aD,aB)==aB.length-1){aG=0}if(aF==null){aF="full"}var aI=c.grep(aK,function(aN){return aN&&aN.reserveSpace});var aM=c.inArray(aD,aI)==0;if(!aM&&aF=="full"){aF=5}if(!isNaN(+aF)){aJ+=+aF}if(aD.direction=="x"){aL+=aJ;if(aH=="bottom"){q.bottom+=aL+aG;aD.box={top:I-q.bottom,height:aL}}else{aD.box={top:q.top+aG,height:aL};q.top+=aL+aG}}else{aC+=aJ;if(aH=="left"){aD.box={left:q.left+aG,width:aC};q.left+=aC+aG}else{q.right+=aC+aG;aD.box={left:G-q.right,width:aC}}}aD.position=aH;aD.tickLength=aF;aD.box.padding=aJ;aD.innermost=aM}function U(aB){if(aB.direction=="x"){aB.box.left=q.left;aB.box.width=h}else{aB.box.top=q.top;aB.box.height=w}}function t(){var aC,aE=m();c.each(aE,function(aF,aG){aG.show=aG.options.show;if(aG.show==null){aG.show=aG.used}aG.reserveSpace=aG.show||aG.options.reserveSpace;n(aG)});allocatedAxes=c.grep(aE,function(aF){return aF.reserveSpace});q.left=q.right=q.top=q.bottom=0;if(O.grid.show){c.each(allocatedAxes,function(aF,aG){S(aG);P(aG);ap(aG,aG.ticks);L(aG)});for(aC=allocatedAxes.length-1;aC>=0;--aC){au(allocatedAxes[aC])}var aD=O.grid.minBorderMargin;if(aD==null){aD=0;for(aC=0;aC<Q.length;++aC){aD=Math.max(aD,Q[aC].points.radius+Q[aC].points.lineWidth/2)}}for(var aB in q){q[aB]+=O.grid.borderWidth;q[aB]=Math.max(aD,q[aB])}}h=G-q.left-q.right;w=I-q.bottom-q.top;c.each(aE,function(aF,aG){r(aG)});if(O.grid.show){c.each(allocatedAxes,function(aF,aG){U(aG)});k()}o()}function n(aE){var aF=aE.options,aD=+(aF.min!=null?aF.min:aE.datamin),aB=+(aF.max!=null?aF.max:aE.datamax),aH=aB-aD;if(aH==0){var aC=aB==0?1:0.01;if(aF.min==null){aD-=aC}if(aF.max==null||aF.min!=null){aB+=aC}}else{var aG=aF.autoscaleMargin;if(aG!=null){if(aF.min==null){aD-=aH*aG;if(aD<0&&aE.datamin!=null&&aE.datamin>=0){aD=0}}if(aF.max==null){aB+=aH*aG;if(aB>0&&aE.datamax!=null&&aE.datamax<=0){aB=0}}}}aE.min=aD;aE.max=aB}function S(aG){var aM=aG.options;var aH;if(typeof aM.ticks=="number"&&aM.ticks>0){aH=aM.ticks}else{aH=0.3*Math.sqrt(aG.direction=="x"?G:I)}var aT=(aG.max-aG.min)/aH,aO,aB,aN,aR,aS,aQ,aI;if(aM.mode=="time"){var aJ={second:1000,minute:60*1000,hour:60*60*1000,day:24*60*60*1000,month:30*24*60*60*1000,year:365.2425*24*60*60*1000};var aK=[[1,"second"],[2,"second"],[5,"second"],[10,"second"],[30,"second"],[1,"minute"],[2,"minute"],[5,"minute"],[10,"minute"],[30,"minute"],[1,"hour"],[2,"hour"],[4,"hour"],[8,"hour"],[12,"hour"],[1,"day"],[2,"day"],[3,"day"],[0.25,"month"],[0.5,"month"],[1,"month"],[2,"month"],[3,"month"],[6,"month"],[1,"year"]];var aC=0;if(aM.minTickSize!=null){if(typeof aM.tickSize=="number"){aC=aM.tickSize}else{aC=aM.minTickSize[0]*aJ[aM.minTickSize[1]]}}for(var aS=0;aS<aK.length-1;++aS){if(aT<(aK[aS][0]*aJ[aK[aS][1]]+aK[aS+1][0]*aJ[aK[aS+1][1]])/2&&aK[aS][0]*aJ[aK[aS][1]]>=aC){break}}aO=aK[aS][0];aN=aK[aS][1];if(aN=="year"){aQ=Math.pow(10,Math.floor(Math.log(aT/aJ.year)/Math.LN10));aI=(aT/aJ.year)/aQ;if(aI<1.5){aO=1}else{if(aI<3){aO=2}else{if(aI<7.5){aO=5}else{aO=10}}}aO*=aQ}aG.tickSize=aM.tickSize||[aO,aN];aB=function(aX){var a2=[],a0=aX.tickSize[0],a3=aX.tickSize[1],a1=new Date(aX.min);var aW=a0*aJ[a3];if(a3=="second"){a1.setUTCSeconds(a(a1.getUTCSeconds(),a0))}if(a3=="minute"){a1.setUTCMinutes(a(a1.getUTCMinutes(),a0))}if(a3=="hour"){a1.setUTCHours(a(a1.getUTCHours(),a0))}if(a3=="month"){a1.setUTCMonth(a(a1.getUTCMonth(),a0))}if(a3=="year"){a1.setUTCFullYear(a(a1.getUTCFullYear(),a0))}a1.setUTCMilliseconds(0);if(aW>=aJ.minute){a1.setUTCSeconds(0)}if(aW>=aJ.hour){a1.setUTCMinutes(0)}if(aW>=aJ.day){a1.setUTCHours(0)}if(aW>=aJ.day*4){a1.setUTCDate(1)}if(aW>=aJ.year){a1.setUTCMonth(0)}var a5=0,a4=Number.NaN,aY;do{aY=a4;a4=a1.getTime();a2.push(a4);if(a3=="month"){if(a0<1){a1.setUTCDate(1);var aV=a1.getTime();a1.setUTCMonth(a1.getUTCMonth()+1);var aZ=a1.getTime();a1.setTime(a4+a5*aJ.hour+(aZ-aV)*a0);a5=a1.getUTCHours();a1.setUTCHours(0)}else{a1.setUTCMonth(a1.getUTCMonth()+a0)}}else{if(a3=="year"){a1.setUTCFullYear(a1.getUTCFullYear()+a0)}else{a1.setTime(a4+aW)}}}while(a4<aX.max&&a4!=aY);return a2};aR=function(aV,aY){var a0=new Date(aV);if(aM.timeformat!=null){return c.plot.formatDate(a0,aM.timeformat,aM.monthNames)}var aW=aY.tickSize[0]*aJ[aY.tickSize[1]];var aX=aY.max-aY.min;var aZ=(aM.twelveHourClock)?" %p":"";if(aW<aJ.minute){fmt="%h:%M:%S"+aZ}else{if(aW<aJ.day){if(aX<2*aJ.day){fmt="%h:%M"+aZ}else{fmt="%b %d %h:%M"+aZ}}else{if(aW<aJ.month){fmt="%b %d"}else{if(aW<aJ.year){if(aX<aJ.year){fmt="%b"}else{fmt="%b %y"}}else{fmt="%y"}}}}return c.plot.formatDate(a0,fmt,aM.monthNames)}}else{var aU=aM.tickDecimals;var aP=-Math.floor(Math.log(aT)/Math.LN10);if(aU!=null&&aP>aU){aP=aU}aQ=Math.pow(10,-aP);aI=aT/aQ;if(aI<1.5){aO=1}else{if(aI<3){aO=2;if(aI>2.25&&(aU==null||aP+1<=aU)){aO=2.5;++aP}}else{if(aI<7.5){aO=5}else{aO=10}}}aO*=aQ;if(aM.minTickSize!=null&&aO<aM.minTickSize){aO=aM.minTickSize}aG.tickDecimals=Math.max(0,aU!=null?aU:aP);aG.tickSize=aM.tickSize||aO;aB=function(aX){var aZ=[];var a0=a(aX.min,aX.tickSize),aW=0,aV=Number.NaN,aY;do{aY=aV;aV=a0+aW*aX.tickSize;aZ.push(aV);++aW}while(aV<aX.max&&aV!=aY);return aZ};aR=function(aV,aW){return aV.toFixed(aW.tickDecimals)}}if(aM.alignTicksWithAxis!=null){var aF=(aG.direction=="x"?p:aw)[aM.alignTicksWithAxis-1];if(aF&&aF.used&&aF!=aG){var aL=aB(aG);if(aL.length>0){if(aM.min==null){aG.min=Math.min(aG.min,aL[0])}if(aM.max==null&&aL.length>1){aG.max=Math.max(aG.max,aL[aL.length-1])}}aB=function(aX){var aY=[],aV,aW;for(aW=0;aW<aF.ticks.length;++aW){aV=(aF.ticks[aW].v-aF.min)/(aF.max-aF.min);aV=aX.min+aV*(aX.max-aX.min);aY.push(aV)}return aY};if(aG.mode!="time"&&aM.tickDecimals==null){var aE=Math.max(0,-Math.floor(Math.log(aT)/Math.LN10)+1),aD=aB(aG);if(!(aD.length>1&&/\..*0$/.test((aD[1]-aD[0]).toFixed(aE)))){aG.tickDecimals=aE}}}}aG.tickGenerator=aB;if(c.isFunction(aM.tickFormatter)){aG.tickFormatter=function(aV,aW){return""+aM.tickFormatter(aV,aW)}}else{aG.tickFormatter=aR}}function P(aF){var aH=aF.options.ticks,aG=[];if(aH==null||(typeof aH=="number"&&aH>0)){aG=aF.tickGenerator(aF)}else{if(aH){if(c.isFunction(aH)){aG=aH({min:aF.min,max:aF.max})}else{aG=aH}}}var aE,aB;aF.ticks=[];for(aE=0;aE<aG.length;++aE){var aC=null;var aD=aG[aE];if(typeof aD=="object"){aB=+aD[0];if(aD.length>1){aC=aD[1]}}else{aB=+aD}if(aC==null){aC=aF.tickFormatter(aB,aF)}if(!isNaN(aB)){aF.ticks.push({v:aB,label:aC})}}}function ap(aB,aC){if(aB.options.autoscaleMargin&&aC.length>0){if(aB.options.min==null){aB.min=Math.min(aB.min,aC[0].v)}if(aB.options.max==null&&aC.length>1){aB.max=Math.max(aB.max,aC[aC.length-1].v)}}}function W(){H.clearRect(0,0,G,I);var aC=O.grid;if(aC.show&&aC.backgroundColor){N()}if(aC.show&&!aC.aboveData){ac()}for(var aB=0;aB<Q.length;++aB){an(ak.drawSeries,[H,Q[aB]]);d(Q[aB])}an(ak.draw,[H]);if(aC.show&&aC.aboveData){ac()}}function D(aB,aI){var aE,aH,aG,aD,aF=m();for(i=0;i<aF.length;++i){aE=aF[i];if(aE.direction==aI){aD=aI+aE.n+"axis";if(!aB[aD]&&aE.n==1){aD=aI+"axis"}if(aB[aD]){aH=aB[aD].from;aG=aB[aD].to;break}}}if(!aB[aD]){aE=aI=="x"?p[0]:aw[0];aH=aB[aI+"1"];aG=aB[aI+"2"]}if(aH!=null&&aG!=null&&aH>aG){var aC=aH;aH=aG;aG=aC}return{from:aH,to:aG,axis:aE}}function N(){H.save();H.translate(q.left,q.top);H.fillStyle=am(O.grid.backgroundColor,w,0,"rgba(255, 255, 255, 0)");H.fillRect(0,0,h,w);H.restore()}function ac(){var aF;H.save();H.translate(q.left,q.top);var aH=O.grid.markings;if(aH){if(c.isFunction(aH)){var aK=aq.getAxes();aK.xmin=aK.xaxis.min;aK.xmax=aK.xaxis.max;aK.ymin=aK.yaxis.min;aK.ymax=aK.yaxis.max;aH=aH(aK)}for(aF=0;aF<aH.length;++aF){var aD=aH[aF],aC=D(aD,"x"),aI=D(aD,"y");if(aC.from==null){aC.from=aC.axis.min}if(aC.to==null){aC.to=aC.axis.max}if(aI.from==null){aI.from=aI.axis.min}if(aI.to==null){aI.to=aI.axis.max}if(aC.to<aC.axis.min||aC.from>aC.axis.max||aI.to<aI.axis.min||aI.from>aI.axis.max){continue}aC.from=Math.max(aC.from,aC.axis.min);aC.to=Math.min(aC.to,aC.axis.max);aI.from=Math.max(aI.from,aI.axis.min);aI.to=Math.min(aI.to,aI.axis.max);if(aC.from==aC.to&&aI.from==aI.to){continue}aC.from=aC.axis.p2c(aC.from);aC.to=aC.axis.p2c(aC.to);aI.from=aI.axis.p2c(aI.from);aI.to=aI.axis.p2c(aI.to);if(aC.from==aC.to||aI.from==aI.to){H.beginPath();H.strokeStyle=aD.color||O.grid.markingsColor;H.lineWidth=aD.lineWidth||O.grid.markingsLineWidth;H.moveTo(aC.from,aI.from);H.lineTo(aC.to,aI.to);H.stroke()}else{H.fillStyle=aD.color||O.grid.markingsColor;H.fillRect(aC.from,aI.to,aC.to-aC.from,aI.from-aI.to)}}}var aK=m(),aM=O.grid.borderWidth;for(var aE=0;aE<aK.length;++aE){var aB=aK[aE],aG=aB.box,aQ=aB.tickLength,aN,aL,aP,aJ;if(!aB.show||aB.ticks.length==0){continue}H.strokeStyle=aB.options.tickColor||c.color.parse(aB.options.color).scale("a",0.22).toString();H.lineWidth=1;if(aB.direction=="x"){aN=0;if(aQ=="full"){aL=(aB.position=="top"?0:w)}else{aL=aG.top-q.top+(aB.position=="top"?aG.height:0)}}else{aL=0;if(aQ=="full"){aN=(aB.position=="left"?0:h)}else{aN=aG.left-q.left+(aB.position=="left"?aG.width:0)}}if(!aB.innermost){H.beginPath();aP=aJ=0;if(aB.direction=="x"){aP=h}else{aJ=w}if(H.lineWidth==1){aN=Math.floor(aN)+0.5;aL=Math.floor(aL)+0.5}H.moveTo(aN,aL);H.lineTo(aN+aP,aL+aJ);H.stroke()}H.beginPath();for(aF=0;aF<aB.ticks.length;++aF){var aO=aB.ticks[aF].v;aP=aJ=0;if(aO<aB.min||aO>aB.max||(aQ=="full"&&aM>0&&(aO==aB.min||aO==aB.max))){continue}if(aB.direction=="x"){aN=aB.p2c(aO);aJ=aQ=="full"?-w:aQ;if(aB.position=="top"){aJ=-aJ}}else{aL=aB.p2c(aO);aP=aQ=="full"?-h:aQ;if(aB.position=="left"){aP=-aP}}if(H.lineWidth==1){if(aB.direction=="x"){aN=Math.floor(aN)+0.5}else{aL=Math.floor(aL)+0.5}}H.moveTo(aN,aL);H.lineTo(aN+aP,aL+aJ)}H.stroke()}if(aM){H.lineWidth=aM;H.strokeStyle=O.grid.borderColor;H.strokeRect(-aM/2,-aM/2,h+aM,w+aM)}H.restore()}function k(){av.find(".tickLabels").remove();var aG=['<div class="tickLabels" style="font-size:smaller">'];var aJ=m();for(var aD=0;aD<aJ.length;++aD){var aC=aJ[aD],aF=aC.box;if(!aC.show){continue}aG.push('<div class="'+aC.direction+"Axis "+aC.direction+aC.n+'Axis" style="color:'+aC.options.color+'">');for(var aE=0;aE<aC.ticks.length;++aE){var aH=aC.ticks[aE];if(!aH.label||aH.v<aC.min||aH.v>aC.max){continue}var aK={},aI;if(aC.direction=="x"){aI="center";aK.left=Math.round(q.left+aC.p2c(aH.v)-aC.labelWidth/2);if(aC.position=="bottom"){aK.top=aF.top+aF.padding}else{aK.bottom=I-(aF.top+aF.height-aF.padding)}}else{aK.top=Math.round(q.top+aC.p2c(aH.v)-aC.labelHeight/2);if(aC.position=="left"){aK.right=G-(aF.left+aF.width-aF.padding);aI="right"}else{aK.left=aF.left+aF.padding;aI="left"}}aK.width=aC.labelWidth;var aB=["position:absolute","text-align:"+aI];for(var aL in aK){aB.push(aL+":"+aK[aL]+"px")}aG.push('<div class="tickLabel" style="'+aB.join(";")+'">'+aH.label+"</div>")}aG.push("</div>")}aG.push("</div>");av.append(aG.join(""))}function d(aB){if(aB.lines.show){at(aB)}if(aB.bars.show){e(aB)}if(aB.points.show){ao(aB)}}function at(aE){function aD(aP,aQ,aI,aU,aT){var aV=aP.points,aJ=aP.pointsize,aN=null,aM=null;H.beginPath();for(var aO=aJ;aO<aV.length;aO+=aJ){var aL=aV[aO-aJ],aS=aV[aO-aJ+1],aK=aV[aO],aR=aV[aO+1];if(aL==null||aK==null){continue}if(aS<=aR&&aS<aT.min){if(aR<aT.min){continue}aL=(aT.min-aS)/(aR-aS)*(aK-aL)+aL;aS=aT.min}else{if(aR<=aS&&aR<aT.min){if(aS<aT.min){continue}aK=(aT.min-aS)/(aR-aS)*(aK-aL)+aL;aR=aT.min}}if(aS>=aR&&aS>aT.max){if(aR>aT.max){continue}aL=(aT.max-aS)/(aR-aS)*(aK-aL)+aL;aS=aT.max}else{if(aR>=aS&&aR>aT.max){if(aS>aT.max){continue}aK=(aT.max-aS)/(aR-aS)*(aK-aL)+aL;aR=aT.max}}if(aL<=aK&&aL<aU.min){if(aK<aU.min){continue}aS=(aU.min-aL)/(aK-aL)*(aR-aS)+aS;aL=aU.min}else{if(aK<=aL&&aK<aU.min){if(aL<aU.min){continue}aR=(aU.min-aL)/(aK-aL)*(aR-aS)+aS;aK=aU.min}}if(aL>=aK&&aL>aU.max){if(aK>aU.max){continue}aS=(aU.max-aL)/(aK-aL)*(aR-aS)+aS;aL=aU.max}else{if(aK>=aL&&aK>aU.max){if(aL>aU.max){continue}aR=(aU.max-aL)/(aK-aL)*(aR-aS)+aS;aK=aU.max}}if(aL!=aN||aS!=aM){H.moveTo(aU.p2c(aL)+aQ,aT.p2c(aS)+aI)}aN=aK;aM=aR;H.lineTo(aU.p2c(aK)+aQ,aT.p2c(aR)+aI)}H.stroke()}function aF(aI,aQ,aP){var aW=aI.points,aV=aI.pointsize,aN=Math.min(Math.max(0,aP.min),aP.max),aX=0,aU,aT=false,aM=1,aL=0,aR=0;while(true){if(aV>0&&aX>aW.length+aV){break}aX+=aV;var aZ=aW[aX-aV],aK=aW[aX-aV+aM],aY=aW[aX],aJ=aW[aX+aM];if(aT){if(aV>0&&aZ!=null&&aY==null){aR=aX;aV=-aV;aM=2;continue}if(aV<0&&aX==aL+aV){H.fill();aT=false;aV=-aV;aM=1;aX=aL=aR+aV;continue}}if(aZ==null||aY==null){continue}if(aZ<=aY&&aZ<aQ.min){if(aY<aQ.min){continue}aK=(aQ.min-aZ)/(aY-aZ)*(aJ-aK)+aK;aZ=aQ.min}else{if(aY<=aZ&&aY<aQ.min){if(aZ<aQ.min){continue}aJ=(aQ.min-aZ)/(aY-aZ)*(aJ-aK)+aK;aY=aQ.min}}if(aZ>=aY&&aZ>aQ.max){if(aY>aQ.max){continue}aK=(aQ.max-aZ)/(aY-aZ)*(aJ-aK)+aK;aZ=aQ.max}else{if(aY>=aZ&&aY>aQ.max){if(aZ>aQ.max){continue}aJ=(aQ.max-aZ)/(aY-aZ)*(aJ-aK)+aK;aY=aQ.max}}if(!aT){H.beginPath();H.moveTo(aQ.p2c(aZ),aP.p2c(aN));aT=true}if(aK>=aP.max&&aJ>=aP.max){H.lineTo(aQ.p2c(aZ),aP.p2c(aP.max));H.lineTo(aQ.p2c(aY),aP.p2c(aP.max));continue}else{if(aK<=aP.min&&aJ<=aP.min){H.lineTo(aQ.p2c(aZ),aP.p2c(aP.min));H.lineTo(aQ.p2c(aY),aP.p2c(aP.min));continue}}var aO=aZ,aS=aY;if(aK<=aJ&&aK<aP.min&&aJ>=aP.min){aZ=(aP.min-aK)/(aJ-aK)*(aY-aZ)+aZ;aK=aP.min}else{if(aJ<=aK&&aJ<aP.min&&aK>=aP.min){aY=(aP.min-aK)/(aJ-aK)*(aY-aZ)+aZ;aJ=aP.min}}if(aK>=aJ&&aK>aP.max&&aJ<=aP.max){aZ=(aP.max-aK)/(aJ-aK)*(aY-aZ)+aZ;aK=aP.max}else{if(aJ>=aK&&aJ>aP.max&&aK<=aP.max){aY=(aP.max-aK)/(aJ-aK)*(aY-aZ)+aZ;aJ=aP.max}}if(aZ!=aO){H.lineTo(aQ.p2c(aO),aP.p2c(aK))}H.lineTo(aQ.p2c(aZ),aP.p2c(aK));H.lineTo(aQ.p2c(aY),aP.p2c(aJ));if(aY!=aS){H.lineTo(aQ.p2c(aY),aP.p2c(aJ));H.lineTo(aQ.p2c(aS),aP.p2c(aJ))}}}H.save();H.translate(q.left,q.top);H.lineJoin="round";var aG=aE.lines.lineWidth,aB=aE.shadowSize;if(aG>0&&aB>0){H.lineWidth=aB;H.strokeStyle="rgba(0,0,0,0.1)";var aH=Math.PI/18;aD(aE.datapoints,Math.sin(aH)*(aG/2+aB/2),Math.cos(aH)*(aG/2+aB/2),aE.xaxis,aE.yaxis);H.lineWidth=aB/2;aD(aE.datapoints,Math.sin(aH)*(aG/2+aB/4),Math.cos(aH)*(aG/2+aB/4),aE.xaxis,aE.yaxis)}H.lineWidth=aG;H.strokeStyle=aE.color;var aC=ae(aE.lines,aE.color,0,w);if(aC){H.fillStyle=aC;aF(aE.datapoints,aE.xaxis,aE.yaxis)}if(aG>0){aD(aE.datapoints,0,0,aE.xaxis,aE.yaxis)}H.restore()}function ao(aE){function aH(aN,aM,aU,aK,aS,aT,aQ,aJ){var aR=aN.points,aI=aN.pointsize;for(var aL=0;aL<aR.length;aL+=aI){var aP=aR[aL],aO=aR[aL+1];if(aP==null||aP<aT.min||aP>aT.max||aO<aQ.min||aO>aQ.max){continue}H.beginPath();aP=aT.p2c(aP);aO=aQ.p2c(aO)+aK;if(aJ=="circle"){H.arc(aP,aO,aM,0,aS?Math.PI:Math.PI*2,false)}else{aJ(H,aP,aO,aM,aS)}H.closePath();if(aU){H.fillStyle=aU;H.fill()}H.stroke()}}H.save();H.translate(q.left,q.top);var aG=aE.points.lineWidth,aC=aE.shadowSize,aB=aE.points.radius,aF=aE.points.symbol;if(aG>0&&aC>0){var aD=aC/2;H.lineWidth=aD;H.strokeStyle="rgba(0,0,0,0.1)";aH(aE.datapoints,aB,null,aD+aD/2,true,aE.xaxis,aE.yaxis,aF);H.strokeStyle="rgba(0,0,0,0.2)";aH(aE.datapoints,aB,null,aD/2,true,aE.xaxis,aE.yaxis,aF)}H.lineWidth=aG;H.strokeStyle=aE.color;aH(aE.datapoints,aB,ae(aE.points,aE.color),0,false,aE.xaxis,aE.yaxis,aF);H.restore()}function E(aN,aM,aV,aI,aQ,aF,aD,aL,aK,aU,aR,aC){var aE,aT,aJ,aP,aG,aB,aO,aH,aS;if(aR){aH=aB=aO=true;aG=false;aE=aV;aT=aN;aP=aM+aI;aJ=aM+aQ;if(aT<aE){aS=aT;aT=aE;aE=aS;aG=true;aB=false}}else{aG=aB=aO=true;aH=false;aE=aN+aI;aT=aN+aQ;aJ=aV;aP=aM;if(aP<aJ){aS=aP;aP=aJ;aJ=aS;aH=true;aO=false}}if(aT<aL.min||aE>aL.max||aP<aK.min||aJ>aK.max){return}if(aE<aL.min){aE=aL.min;aG=false}if(aT>aL.max){aT=aL.max;aB=false}if(aJ<aK.min){aJ=aK.min;aH=false}if(aP>aK.max){aP=aK.max;aO=false}aE=aL.p2c(aE);aJ=aK.p2c(aJ);aT=aL.p2c(aT);aP=aK.p2c(aP);if(aD){aU.beginPath();aU.moveTo(aE,aJ);aU.lineTo(aE,aP);aU.lineTo(aT,aP);aU.lineTo(aT,aJ);aU.fillStyle=aD(aJ,aP);aU.fill()}if(aC>0&&(aG||aB||aO||aH)){aU.beginPath();aU.moveTo(aE,aJ+aF);if(aG){aU.lineTo(aE,aP+aF)}else{aU.moveTo(aE,aP+aF)}if(aO){aU.lineTo(aT,aP+aF)}else{aU.moveTo(aT,aP+aF)}if(aB){aU.lineTo(aT,aJ+aF)}else{aU.moveTo(aT,aJ+aF)}if(aH){aU.lineTo(aE,aJ+aF)}else{aU.moveTo(aE,aJ+aF)}aU.stroke()}}function e(aD){function aC(aJ,aI,aL,aG,aK,aN,aM){var aO=aJ.points,aF=aJ.pointsize;for(var aH=0;aH<aO.length;aH+=aF){if(aO[aH]==null){continue}E(aO[aH],aO[aH+1],aO[aH+2],aI,aL,aG,aK,aN,aM,H,aD.bars.horizontal,aD.bars.lineWidth)}}H.save();H.translate(q.left,q.top);H.lineWidth=aD.bars.lineWidth;H.strokeStyle=aD.color;var aB=aD.bars.align=="left"?0:-aD.bars.barWidth/2;var aE=aD.bars.fill?function(aF,aG){return ae(aD.bars,aD.color,aF,aG)}:null;aC(aD.datapoints,aB,aB+aD.bars.barWidth,0,aE,aD.xaxis,aD.yaxis);H.restore()}function ae(aD,aB,aC,aF){var aE=aD.fill;if(!aE){return null}if(aD.fillColor){return am(aD.fillColor,aC,aF,aB)}var aG=c.color.parse(aB);aG.a=typeof aE=="number"?aE:0.4;aG.normalize();return aG.toString()}function o(){av.find(".legend").remove();if(!O.legend.show){return}var aH=[],aF=false,aN=O.legend.labelFormatter,aM,aJ;for(var aE=0;aE<Q.length;++aE){aM=Q[aE];aJ=aM.label;if(!aJ){continue}if(aE%O.legend.noColumns==0){if(aF){aH.push("</tr>")}aH.push("<tr>");aF=true}if(aN){aJ=aN(aJ,aM)}aH.push('<td class="legendColorBox"><div style="border:1px solid '+O.legend.labelBoxBorderColor+';padding:1px"><div style="width:4px;height:0;border:5px solid '+aM.color+';overflow:hidden"></div></div></td><td class="legendLabel">'+aJ+"</td>")}if(aF){aH.push("</tr>")}if(aH.length==0){return}var aL='<table style="font-size:smaller;color:'+O.grid.color+'">'+aH.join("")+"</table>";if(O.legend.container!=null){c(O.legend.container).html(aL)}else{var aI="",aC=O.legend.position,aD=O.legend.margin;if(aD[0]==null){aD=[aD,aD]}if(aC.charAt(0)=="n"){aI+="top:"+(aD[1]+q.top)+"px;"}else{if(aC.charAt(0)=="s"){aI+="bottom:"+(aD[1]+q.bottom)+"px;"}}if(aC.charAt(1)=="e"){aI+="right:"+(aD[0]+q.right)+"px;"}else{if(aC.charAt(1)=="w"){aI+="left:"+(aD[0]+q.left)+"px;"}}var aK=c('<div class="legend">'+aL.replace('style="','style="position:absolute;'+aI+";")+"</div>").appendTo(av);if(O.legend.backgroundOpacity!=0){var aG=O.legend.backgroundColor;if(aG==null){aG=O.grid.backgroundColor;if(aG&&typeof aG=="string"){aG=c.color.parse(aG)}else{aG=c.color.extract(aK,"background-color")}aG.a=1;aG=aG.toString()}var aB=aK.children();c('<div style="position:absolute;width:'+aB.width()+"px;height:"+aB.height()+"px;"+aI+"background-color:"+aG+';"> </div>').prependTo(aK).css("opacity",O.legend.backgroundOpacity)}}}var ab=[],M=null;function K(aI,aG,aD){var aO=O.grid.mouseActiveRadius,a0=aO*aO+1,aY=null,aR=false,aW,aU;for(aW=Q.length-1;aW>=0;--aW){if(!aD(Q[aW])){continue}var aP=Q[aW],aH=aP.xaxis,aF=aP.yaxis,aV=aP.datapoints.points,aT=aP.datapoints.pointsize,aQ=aH.c2p(aI),aN=aF.c2p(aG),aC=aO/aH.scale,aB=aO/aF.scale;if(aH.options.inverseTransform){aC=Number.MAX_VALUE}if(aF.options.inverseTransform){aB=Number.MAX_VALUE}if(aP.lines.show||aP.points.show){for(aU=0;aU<aV.length;aU+=aT){var aK=aV[aU],aJ=aV[aU+1];if(aK==null){continue}if(aK-aQ>aC||aK-aQ<-aC||aJ-aN>aB||aJ-aN<-aB){continue}var aM=Math.abs(aH.p2c(aK)-aI),aL=Math.abs(aF.p2c(aJ)-aG),aS=aM*aM+aL*aL;if(aS<a0){a0=aS;aY=[aW,aU/aT]}}}if(aP.bars.show&&!aY){var aE=aP.bars.align=="left"?0:-aP.bars.barWidth/2,aX=aE+aP.bars.barWidth;for(aU=0;aU<aV.length;aU+=aT){var aK=aV[aU],aJ=aV[aU+1],aZ=aV[aU+2];if(aK==null){continue}if(Q[aW].bars.horizontal?(aQ<=Math.max(aZ,aK)&&aQ>=Math.min(aZ,aK)&&aN>=aJ+aE&&aN<=aJ+aX):(aQ>=aK+aE&&aQ<=aK+aX&&aN>=Math.min(aZ,aJ)&&aN<=Math.max(aZ,aJ))){aY=[aW,aU/aT]}}}}if(aY){aW=aY[0];aU=aY[1];aT=Q[aW].datapoints.pointsize;return{datapoint:Q[aW].datapoints.points.slice(aU*aT,(aU+1)*aT),dataIndex:aU,series:Q[aW],seriesIndex:aW}}return null}function aa(aB){if(O.grid.hoverable){u("plothover",aB,function(aC){return aC.hoverable!=false})}}function l(aB){if(O.grid.hoverable){u("plothover",aB,function(aC){return false})}}function R(aB){u("plotclick",aB,function(aC){return aC.clickable!=false})}function u(aC,aB,aD){var aE=y.offset(),aH=aB.pageX-aE.left-q.left,aF=aB.pageY-aE.top-q.top,aJ=C({left:aH,top:aF});aJ.pageX=aB.pageX;aJ.pageY=aB.pageY;var aK=K(aH,aF,aD);if(aK){aK.pageX=parseInt(aK.series.xaxis.p2c(aK.datapoint[0])+aE.left+q.left);aK.pageY=parseInt(aK.series.yaxis.p2c(aK.datapoint[1])+aE.top+q.top)}if(O.grid.autoHighlight){for(var aG=0;aG<ab.length;++aG){var aI=ab[aG];if(aI.auto==aC&&!(aK&&aI.series==aK.series&&aI.point[0]==aK.datapoint[0]&&aI.point[1]==aK.datapoint[1])){T(aI.series,aI.point)}}if(aK){x(aK.series,aK.datapoint,aC)}}av.trigger(aC,[aJ,aK])}function f(){if(!M){M=setTimeout(s,30)}}function s(){M=null;A.save();A.clearRect(0,0,G,I);A.translate(q.left,q.top);var aC,aB;for(aC=0;aC<ab.length;++aC){aB=ab[aC];if(aB.series.bars.show){v(aB.series,aB.point)}else{ay(aB.series,aB.point)}}A.restore();an(ak.drawOverlay,[A])}function x(aD,aB,aF){if(typeof aD=="number"){aD=Q[aD]}if(typeof aB=="number"){var aE=aD.datapoints.pointsize;aB=aD.datapoints.points.slice(aE*aB,aE*(aB+1))}var aC=al(aD,aB);if(aC==-1){ab.push({series:aD,point:aB,auto:aF});f()}else{if(!aF){ab[aC].auto=false}}}function T(aD,aB){if(aD==null&&aB==null){ab=[];f()}if(typeof aD=="number"){aD=Q[aD]}if(typeof aB=="number"){aB=aD.data[aB]}var aC=al(aD,aB);if(aC!=-1){ab.splice(aC,1);f()}}function al(aD,aE){for(var aB=0;aB<ab.length;++aB){var aC=ab[aB];if(aC.series==aD&&aC.point[0]==aE[0]&&aC.point[1]==aE[1]){return aB}}return -1}function ay(aE,aD){var aC=aD[0],aI=aD[1],aH=aE.xaxis,aG=aE.yaxis;if(aC<aH.min||aC>aH.max||aI<aG.min||aI>aG.max){return}var aF=aE.points.radius+aE.points.lineWidth/2;A.lineWidth=aF;A.strokeStyle=c.color.parse(aE.color).scale("a",0.5).toString();var aB=1.5*aF,aC=aH.p2c(aC),aI=aG.p2c(aI);A.beginPath();if(aE.points.symbol=="circle"){A.arc(aC,aI,aB,0,2*Math.PI,false)}else{aE.points.symbol(A,aC,aI,aB,false)}A.closePath();A.stroke()}function v(aE,aB){A.lineWidth=aE.bars.lineWidth;A.strokeStyle=c.color.parse(aE.color).scale("a",0.5).toString();var aD=c.color.parse(aE.color).scale("a",0.5).toString();var aC=aE.bars.align=="left"?0:-aE.bars.barWidth/2;E(aB[0],aB[1],aB[2]||0,aC,aC+aE.bars.barWidth,0,function(){return aD},aE.xaxis,aE.yaxis,A,aE.bars.horizontal,aE.bars.lineWidth)}function am(aJ,aB,aH,aC){if(typeof aJ=="string"){return aJ}else{var aI=H.createLinearGradient(0,aH,0,aB);for(var aE=0,aD=aJ.colors.length;aE<aD;++aE){var aF=aJ.colors[aE];if(typeof aF!="string"){var aG=c.color.parse(aC);if(aF.brightness!=null){aG=aG.scale("rgb",aF.brightness)}if(aF.opacity!=null){aG.a*=aF.opacity}aF=aG.toString()}aI.addColorStop(aE/(aD-1),aF)}return aI}}}c.plot=function(g,e,d){var f=new b(c(g),e,d,c.plot.plugins);return f};c.plot.version="0.7";c.plot.plugins=[];c.plot.formatDate=function(l,f,h){var o=function(d){d=""+d;return d.length==1?"0"+d:d};var e=[];var p=false,j=false;var n=l.getUTCHours();var k=n<12;if(h==null){h=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]}if(f.search(/%p|%P/)!=-1){if(n>12){n=n-12}else{if(n==0){n=12}}}for(var g=0;g<f.length;++g){var m=f.charAt(g);if(p){switch(m){case"h":m=""+n;break;case"H":m=o(n);break;case"M":m=o(l.getUTCMinutes());break;case"S":m=o(l.getUTCSeconds());break;case"d":m=""+l.getUTCDate();break;case"m":m=""+(l.getUTCMonth()+1);break;case"y":m=""+l.getUTCFullYear();break;case"b":m=""+h[l.getUTCMonth()];break;case"p":m=(k)?("am"):("pm");break;case"P":m=(k)?("AM"):("PM");break;case"0":m="";j=true;break}if(m&&j){m=o(m);j=false}e.push(m);if(!j){p=false}}else{if(m=="%"){p=true}else{e.push(m)}}}return e.join("")};function a(e,d){return d*Math.floor(e/d)}})(jQuery);
(function(b){function c(D){var h=null;var L=null;var n=null;var B=null;var p=null;var M=0;var F=true;var o=10;var w=0.95;var A=0;var d=false;var z=false;var j=[];D.hooks.processOptions.push(g);D.hooks.bindEvents.push(e);function g(O,N){if(N.series.pie.show){N.grid.show=false;if(N.series.pie.label.show=="auto"){if(N.legend.show){N.series.pie.label.show=false}else{N.series.pie.label.show=true}}if(N.series.pie.radius=="auto"){if(N.series.pie.label.show){N.series.pie.radius=3/4}else{N.series.pie.radius=1}}if(N.series.pie.tilt>1){N.series.pie.tilt=1}if(N.series.pie.tilt<0){N.series.pie.tilt=0}O.hooks.processDatapoints.push(E);O.hooks.drawOverlay.push(H);O.hooks.draw.push(r)}}function e(P,N){var O=P.getOptions();if(O.series.pie.show&&O.grid.hoverable){N.unbind("mousemove").mousemove(t)}if(O.series.pie.show&&O.grid.clickable){N.unbind("click").click(l)}}function G(O){var P="";function N(S,T){if(!T){T=0}for(var R=0;R<S.length;++R){for(var Q=0;Q<T;Q++){P+="\t"}if(typeof S[R]=="object"){P+=""+R+":\n";N(S[R],T+1)}else{P+=""+R+": "+S[R]+"\n"}}}N(O);alert(P)}function q(P){for(var N=0;N<P.length;++N){var O=parseFloat(P[N].data[0][1]);if(O){M+=O}}}function E(Q,N,O,P){if(!d){d=true;h=Q.getCanvas();L=b(h).parent();a=Q.getOptions();Q.setData(K(Q.getData()))}}function I(){A=L.children().filter(".legend").children().width();n=Math.min(h.width,(h.height/a.series.pie.tilt))/2;p=(h.height/2)+a.series.pie.offset.top;B=(h.width/2);if(a.series.pie.offset.left=="auto"){if(a.legend.position.match("w")){B+=A/2}else{B-=A/2}}else{B+=a.series.pie.offset.left}if(B<n){B=n}else{if(B>h.width-n){B=h.width-n}}}function v(O){for(var N=0;N<O.length;++N){if(typeof(O[N].data)=="number"){O[N].data=[[1,O[N].data]]}else{if(typeof(O[N].data)=="undefined"||typeof(O[N].data[0])=="undefined"){if(typeof(O[N].data)!="undefined"&&typeof(O[N].data.label)!="undefined"){O[N].label=O[N].data.label}O[N].data=[[1,0]]}}}return O}function K(Q){Q=v(Q);q(Q);var P=0;var S=0;var N=a.series.pie.combine.color;var R=[];for(var O=0;O<Q.length;++O){Q[O].data[0][1]=parseFloat(Q[O].data[0][1]);if(!Q[O].data[0][1]){Q[O].data[0][1]=0}if(Q[O].data[0][1]/M<=a.series.pie.combine.threshold){P+=Q[O].data[0][1];S++;if(!N){N=Q[O].color}}else{R.push({data:[[1,Q[O].data[0][1]]],color:Q[O].color,label:Q[O].label,angle:(Q[O].data[0][1]*(Math.PI*2))/M,percent:(Q[O].data[0][1]/M*100)})}}if(S>0){R.push({data:[[1,P]],color:N,label:a.series.pie.combine.label,angle:(P*(Math.PI*2))/M,percent:(P/M*100)})}return R}function r(S,Q){if(!L){return}ctx=Q;I();var T=S.getData();var P=0;while(F&&P<o){F=false;if(P>0){n*=w}P+=1;N();if(a.series.pie.tilt<=0.8){O()}R()}if(P>=o){N();L.prepend('<div class="error">Could not draw pie with labels contained inside canvas</div>')}if(S.setSeries&&S.insertLegend){S.setSeries(T);S.insertLegend()}function N(){ctx.clearRect(0,0,h.width,h.height);L.children().filter(".pieLabel, .pieLabelBackground").remove()}function O(){var Z=5;var Y=15;var W=10;var X=0.02;if(a.series.pie.radius>1){var U=a.series.pie.radius}else{var U=n*a.series.pie.radius}if(U>=(h.width/2)-Z||U*a.series.pie.tilt>=(h.height/2)-Y||U<=W){return}ctx.save();ctx.translate(Z,Y);ctx.globalAlpha=X;ctx.fillStyle="#000";ctx.translate(B,p);ctx.scale(1,a.series.pie.tilt);for(var V=1;V<=W;V++){ctx.beginPath();ctx.arc(0,0,U,0,Math.PI*2,false);ctx.fill();U-=V}ctx.restore()}function R(){startAngle=Math.PI*a.series.pie.startAngle;if(a.series.pie.radius>1){var U=a.series.pie.radius}else{var U=n*a.series.pie.radius}ctx.save();ctx.translate(B,p);ctx.scale(1,a.series.pie.tilt);ctx.save();var Y=startAngle;for(var W=0;W<T.length;++W){T[W].startAngle=Y;X(T[W].angle,T[W].color,true)}ctx.restore();ctx.save();ctx.lineWidth=a.series.pie.stroke.width;Y=startAngle;for(var W=0;W<T.length;++W){X(T[W].angle,a.series.pie.stroke.color,false)}ctx.restore();J(ctx);if(a.series.pie.label.show){V()}ctx.restore();function X(ab,Z,aa){if(ab<=0){return}if(aa){ctx.fillStyle=Z}else{ctx.strokeStyle=Z;ctx.lineJoin="round"}ctx.beginPath();if(Math.abs(ab-Math.PI*2)>1e-9){ctx.moveTo(0,0)}else{if(b.browser.msie){ab-=0.0001}}ctx.arc(0,0,U,Y,Y+ab,false);ctx.closePath();Y+=ab;if(aa){ctx.fill()}else{ctx.stroke()}}function V(){var ac=startAngle;if(a.series.pie.label.radius>1){var Z=a.series.pie.label.radius}else{var Z=n*a.series.pie.label.radius}for(var ab=0;ab<T.length;++ab){if(T[ab].percent>=a.series.pie.label.threshold*100){aa(T[ab],ac,ab)}ac+=T[ab].angle}function aa(ap,ai,ag){if(ap.data[0][1]==0){return}var ar=a.legend.labelFormatter,aq,ae=a.series.pie.label.formatter;if(ar){aq=ar(ap.label,ap)}else{aq=ap.label}if(ae){aq=ae(aq,ap)}var aj=((ai+ap.angle)+ai)/2;var ao=B+Math.round(Math.cos(aj)*Z);var am=p+Math.round(Math.sin(aj)*Z)*a.series.pie.tilt;var af='<span class="pieLabel" id="pieLabel'+ag+'" style="position:absolute;top:'+am+"px;left:"+ao+'px;">'+aq+"</span>";L.append(af);var an=L.children("#pieLabel"+ag);var ad=(am-an.height()/2);var ah=(ao-an.width()/2);an.css("top",ad);an.css("left",ah);if(0-ad>0||0-ah>0||h.height-(ad+an.height())<0||h.width-(ah+an.width())<0){F=true}if(a.series.pie.label.background.opacity!=0){var ak=a.series.pie.label.background.color;if(ak==null){ak=ap.color}var al="top:"+ad+"px;left:"+ah+"px;";b('<div class="pieLabelBackground" style="position:absolute;width:'+an.width()+"px;height:"+an.height()+"px;"+al+"background-color:"+ak+';"> </div>').insertBefore(an).css("opacity",a.series.pie.label.background.opacity)}}}}}function J(N){if(a.series.pie.innerRadius>0){N.save();innerRadius=a.series.pie.innerRadius>1?a.series.pie.innerRadius:n*a.series.pie.innerRadius;N.globalCompositeOperation="destination-out";N.beginPath();N.fillStyle=a.series.pie.stroke.color;N.arc(0,0,innerRadius,0,Math.PI*2,false);N.fill();N.closePath();N.restore();N.save();N.beginPath();N.strokeStyle=a.series.pie.stroke.color;N.arc(0,0,innerRadius,0,Math.PI*2,false);N.stroke();N.closePath();N.restore()}}function s(Q,R){for(var S=false,P=-1,N=Q.length,O=N-1;++P<N;O=P){((Q[P][1]<=R[1]&&R[1]<Q[O][1])||(Q[O][1]<=R[1]&&R[1]<Q[P][1]))&&(R[0]<(Q[O][0]-Q[P][0])*(R[1]-Q[P][1])/(Q[O][1]-Q[P][1])+Q[P][0])&&(S=!S)}return S}function u(R,P){var T=D.getData(),O=D.getOptions(),N=O.series.pie.radius>1?O.series.pie.radius:n*O.series.pie.radius;for(var Q=0;Q<T.length;++Q){var S=T[Q];if(S.pie.show){ctx.save();ctx.beginPath();ctx.moveTo(0,0);ctx.arc(0,0,N,S.startAngle,S.startAngle+S.angle,false);ctx.closePath();x=R-B;y=P-p;if(ctx.isPointInPath){if(ctx.isPointInPath(R-B,P-p)){ctx.restore();return{datapoint:[S.percent,S.data],dataIndex:0,series:S,seriesIndex:Q}}}else{p1X=(N*Math.cos(S.startAngle));p1Y=(N*Math.sin(S.startAngle));p2X=(N*Math.cos(S.startAngle+(S.angle/4)));p2Y=(N*Math.sin(S.startAngle+(S.angle/4)));p3X=(N*Math.cos(S.startAngle+(S.angle/2)));p3Y=(N*Math.sin(S.startAngle+(S.angle/2)));p4X=(N*Math.cos(S.startAngle+(S.angle/1.5)));p4Y=(N*Math.sin(S.startAngle+(S.angle/1.5)));p5X=(N*Math.cos(S.startAngle+S.angle));p5Y=(N*Math.sin(S.startAngle+S.angle));arrPoly=[[0,0],[p1X,p1Y],[p2X,p2Y],[p3X,p3Y],[p4X,p4Y],[p5X,p5Y]];arrPoint=[x,y];if(s(arrPoly,arrPoint)){ctx.restore();return{datapoint:[S.percent,S.data],dataIndex:0,series:S,seriesIndex:Q}}}ctx.restore()}}return null}function t(N){m("plothover",N)}function l(N){m("plotclick",N)}function m(N,T){var O=D.offset(),R=parseInt(T.pageX-O.left),P=parseInt(T.pageY-O.top),V=u(R,P);if(a.grid.autoHighlight){for(var Q=0;Q<j.length;++Q){var S=j[Q];if(S.auto==N&&!(V&&S.series==V.series)){f(S.series)}}}if(V){k(V.series,N)}var U={pageX:T.pageX,pageY:T.pageY};L.trigger(N,[U,V])}function k(O,P){if(typeof O=="number"){O=series[O]}var N=C(O);if(N==-1){j.push({series:O,auto:P});D.triggerRedrawOverlay()}else{if(!P){j[N].auto=false}}}function f(O){if(O==null){j=[];D.triggerRedrawOverlay()}if(typeof O=="number"){O=series[O]}var N=C(O);if(N!=-1){j.splice(N,1);D.triggerRedrawOverlay()}}function C(P){for(var N=0;N<j.length;++N){var O=j[N];if(O.series==P){return N}}return -1}function H(Q,R){var P=Q.getOptions();var N=P.series.pie.radius>1?P.series.pie.radius:n*P.series.pie.radius;R.save();R.translate(B,p);R.scale(1,P.series.pie.tilt);for(i=0;i<j.length;++i){O(j[i].series)}J(R);R.restore();function O(S){if(S.angle<0){return}R.fillStyle="rgba(255, 255, 255, "+P.series.pie.highlight.opacity+")";R.beginPath();if(Math.abs(S.angle-Math.PI*2)>1e-9){R.moveTo(0,0)}R.arc(0,0,N,S.startAngle,S.startAngle+S.angle,false);R.closePath();R.fill()}}}var a={series:{pie:{show:false,radius:"auto",innerRadius:0,startAngle:3/2,tilt:1,offset:{top:0,left:"auto"},stroke:{color:"#FFF",width:1},label:{show:"auto",formatter:function(d,e){return'<div style="font-size:x-small;text-align:center;padding:2px;color:'+e.color+';">'+d+"<br/>"+Math.round(e.percent)+"%</div>"},radius:1,background:{color:null,opacity:0},threshold:0},combine:{threshold:-1,color:null,label:"Other"},highlight:{opacity:0.5}}}};b.plot.plugins.push({init:c,options:a,name:"pie",version:"1.0"})})(jQuery);
/*
Flot plugin for stacking data sets, i.e. putting them on top of each
other, for accumulative graphs.

The plugin assumes the data is sorted on x (or y if stacking
horizontally). For line charts, it is assumed that if a line has an
undefined gap (from a null point), then the line above it should have
the same gap - insert zeros instead of "null" if you want another
behaviour. This also holds for the start and end of the chart. Note
that stacking a mix of positive and negative values in most instances
doesn't make sense (so it looks weird).

Two or more series are stacked when their "stack" attribute is set to
the same key (which can be any number or string or just "true"). To
specify the default stack, you can set

  series: {
    stack: null or true or key (number/string)
  }

or specify it for a specific series

  $.plot($("#placeholder"), [{ data: [ ... ], stack: true }])
  
The stacking order is determined by the order of the data series in
the array (later series end up on top of the previous).

Internally, the plugin modifies the datapoints in each series, adding
an offset to the y value. For line series, extra data points are
inserted through interpolation. If there's a second y value, it's also
adjusted (e.g for bar charts or filled areas).
*/

(function ($) {
    var options = {
        series: { stack: null } // or number/string
    };
    
    function init(plot) {
        function findMatchingSeries(s, allseries) {
            var res = null
            for (var i = 0; i < allseries.length; ++i) {
                if (s == allseries[i])
                    break;
                
                if (allseries[i].stack == s.stack)
                    res = allseries[i];
            }
            
            return res;
        }
        
        function stackData(plot, s, datapoints) {
            if (s.stack == null)
                return;

            var other = findMatchingSeries(s, plot.getData());
            if (!other)
                return;

            var ps = datapoints.pointsize,
                points = datapoints.points,
                otherps = other.datapoints.pointsize,
                otherpoints = other.datapoints.points,
                newpoints = [],
                px, py, intery, qx, qy, bottom,
                withlines = s.lines.show,
                horizontal = s.bars.horizontal,
                withbottom = ps > 2 && (horizontal ? datapoints.format[2].x : datapoints.format[2].y),
                withsteps = withlines && s.lines.steps,
                fromgap = true,
                keyOffset = horizontal ? 1 : 0,
                accumulateOffset = horizontal ? 0 : 1,
                i = 0, j = 0, l;

            while (true) {
                if (i >= points.length)
                    break;

                l = newpoints.length;

                if (points[i] == null) {
                    // copy gaps
                    for (m = 0; m < ps; ++m)
                        newpoints.push(points[i + m]);
                    i += ps;
                }
                else if (j >= otherpoints.length) {
                    // for lines, we can't use the rest of the points
                    if (!withlines) {
                        for (m = 0; m < ps; ++m)
                            newpoints.push(points[i + m]);
                    }
                    i += ps;
                }
                else if (otherpoints[j] == null) {
                    // oops, got a gap
                    for (m = 0; m < ps; ++m)
                        newpoints.push(null);
                    fromgap = true;
                    j += otherps;
                }
                else {
                    // cases where we actually got two points
                    px = points[i + keyOffset];
                    py = points[i + accumulateOffset];
                    qx = otherpoints[j + keyOffset];
                    qy = otherpoints[j + accumulateOffset];
                    bottom = 0;

                    if (px == qx) {
                        for (m = 0; m < ps; ++m)
                            newpoints.push(points[i + m]);

                        newpoints[l + accumulateOffset] += qy;
                        bottom = qy;
                        
                        i += ps;
                        j += otherps;
                    }
                    else if (px > qx) {
                        // we got past point below, might need to
                        // insert interpolated extra point
                        if (withlines && i > 0 && points[i - ps] != null) {
                            intery = py + (points[i - ps + accumulateOffset] - py) * (qx - px) / (points[i - ps + keyOffset] - px);
                            newpoints.push(qx);
                            newpoints.push(intery + qy);
                            for (m = 2; m < ps; ++m)
                                newpoints.push(points[i + m]);
                            bottom = qy; 
                        }

                        j += otherps;
                    }
                    else { // px < qx
                        if (fromgap && withlines) {
                            // if we come from a gap, we just skip this point
                            i += ps;
                            continue;
                        }
                            
                        for (m = 0; m < ps; ++m)
                            newpoints.push(points[i + m]);
                        
                        // we might be able to interpolate a point below,
                        // this can give us a better y
                        if (withlines && j > 0 && otherpoints[j - otherps] != null)
                            bottom = qy + (otherpoints[j - otherps + accumulateOffset] - qy) * (px - qx) / (otherpoints[j - otherps + keyOffset] - qx);

                        newpoints[l + accumulateOffset] += bottom;
                        
                        i += ps;
                    }

                    fromgap = false;
                    
                    if (l != newpoints.length && withbottom)
                        newpoints[l + 2] += bottom;
                }

                // maintain the line steps invariant
                if (withsteps && l != newpoints.length && l > 0
                    && newpoints[l] != null
                    && newpoints[l] != newpoints[l - ps]
                    && newpoints[l + 1] != newpoints[l - ps + 1]) {
                    for (m = 0; m < ps; ++m)
                        newpoints[l + ps + m] = newpoints[l + m];
                    newpoints[l + 1] = newpoints[l - ps + 1];
                }
            }

            datapoints.points = newpoints;
        }
        
        plot.hooks.processDatapoints.push(stackData);
    }
    
    $.plot.plugins.push({
        init: init,
        options: options,
        name: 'stack',
        version: '1.2'
    });
})(jQuery);

(function(n,p,u){var w=n([]),s=n.resize=n.extend(n.resize,{}),o,l="setTimeout",m="resize",t=m+"-special-event",v="delay",r="throttleWindow";s[v]=250;s[r]=true;n.event.special[m]={setup:function(){if(!s[r]&&this[l]){return false}var a=n(this);w=w.add(a);n.data(this,t,{w:a.width(),h:a.height()});if(w.length===1){q()}},teardown:function(){if(!s[r]&&this[l]){return false}var a=n(this);w=w.not(a);a.removeData(t);if(!w.length){clearTimeout(o)}},add:function(b){if(!s[r]&&this[l]){return false}var c;function a(d,h,g){var f=n(this),e=n.data(this,t);e.w=h!==u?h:f.width();e.h=g!==u?g:f.height();c.apply(this,arguments)}if(n.isFunction(b)){c=b;return a}else{c=b.handler;b.handler=a}}};function q(){o=p[l](function(){w.each(function(){var d=n(this),a=d.width(),b=d.height(),c=n.data(this,t);if(a!==c.w||b!==c.h){d.trigger(m,[c.w=a,c.h=b])}});q()},s[v])}})(jQuery,this);(function(b){var a={};function c(f){function e(){var h=f.getPlaceholder();if(h.width()==0||h.height()==0){return}f.resize();f.setupGrid();f.draw()}function g(i,h){i.getPlaceholder().resize(e)}function d(i,h){i.getPlaceholder().unbind("resize",e)}f.hooks.bindEvents.push(g);f.hooks.shutdown.push(d)}b.plot.plugins.push({init:c,options:a,name:"resize",version:"1.0"})})(jQuery);
// Chosen, a Select Box Enhancer for jQuery and Protoype
// by Patrick Filler for Harvest, http://getharvest.com
// 
// Version 0.9.8
// Full source at https://github.com/harvesthq/chosen
// Copyright (c) 2011 Harvest http://getharvest.com

// MIT License, https://github.com/harvesthq/chosen/blob/master/LICENSE.md
// This file is generated by `cake build`, do not edit it by hand.
((function(){var a;a=function(){function a(){this.options_index=0,this.parsed=[]}return a.prototype.add_node=function(a){return a.nodeName==="OPTGROUP"?this.add_group(a):this.add_option(a)},a.prototype.add_group=function(a){var b,c,d,e,f,g;b=this.parsed.length,this.parsed.push({array_index:b,group:!0,label:a.label,children:0,disabled:a.disabled}),f=a.childNodes,g=[];for(d=0,e=f.length;d<e;d++)c=f[d],g.push(this.add_option(c,b,a.disabled));return g},a.prototype.add_option=function(a,b,c){if(a.nodeName==="OPTION")return a.text!==""?(b!=null&&(this.parsed[b].children+=1),this.parsed.push({array_index:this.parsed.length,options_index:this.options_index,value:a.value,text:a.text,html:a.innerHTML,selected:a.selected,disabled:c===!0?c:a.disabled,group_array_index:b,classes:a.className,style:a.style.cssText})):this.parsed.push({array_index:this.parsed.length,options_index:this.options_index,empty:!0}),this.options_index+=1},a}(),a.select_to_array=function(b){var c,d,e,f,g;d=new a,g=b.childNodes;for(e=0,f=g.length;e<f;e++)c=g[e],d.add_node(c);return d.parsed},this.SelectParser=a})).call(this),function(){var a,b;b=this,a=function(){function a(a,b){this.form_field=a,this.options=b!=null?b:{},this.set_default_values(),this.is_multiple=this.form_field.multiple,this.set_default_text(),this.setup(),this.set_up_html(),this.register_observers(),this.finish_setup()}return a.prototype.set_default_values=function(){var a=this;return this.click_test_action=function(b){return a.test_active_click(b)},this.activate_action=function(b){return a.activate_field(b)},this.active_field=!1,this.mouse_on_container=!1,this.results_showing=!1,this.result_highlighted=null,this.result_single_selected=null,this.allow_single_deselect=this.options.allow_single_deselect!=null&&this.form_field.options[0]!=null&&this.form_field.options[0].text===""?this.options.allow_single_deselect:!1,this.disable_search_threshold=this.options.disable_search_threshold||0,this.search_contains=this.options.search_contains||!1,this.choices=0,this.single_backstroke_delete=this.options.single_backstroke_delete||!1,this.max_selected_options=this.options.max_selected_options||Infinity},a.prototype.set_default_text=function(){return this.form_field.getAttribute("data-placeholder")?this.default_text=this.form_field.getAttribute("data-placeholder"):this.is_multiple?this.default_text=this.options.placeholder_text_multiple||this.options.placeholder_text||"Select Some Options":this.default_text=this.options.placeholder_text_single||this.options.placeholder_text||"Select an Option",this.results_none_found=this.form_field.getAttribute("data-no_results_text")||this.options.no_results_text||"No results match"},a.prototype.mouse_enter=function(){return this.mouse_on_container=!0},a.prototype.mouse_leave=function(){return this.mouse_on_container=!1},a.prototype.input_focus=function(a){var b=this;if(!this.active_field)return setTimeout(function(){return b.container_mousedown()},50)},a.prototype.input_blur=function(a){var b=this;if(!this.mouse_on_container)return this.active_field=!1,setTimeout(function(){return b.blur_test()},100)},a.prototype.result_add_option=function(a){var b,c;return a.disabled?"":(a.dom_id=this.container_id+"_o_"+a.array_index,b=a.selected&&this.is_multiple?[]:["active-result"],a.selected&&b.push("result-selected"),a.group_array_index!=null&&b.push("group-option"),a.classes!==""&&b.push(a.classes),c=a.style.cssText!==""?' style="'+a.style+'"':"",'<li id="'+a.dom_id+'" class="'+b.join(" ")+'"'+c+">"+a.html+"</li>")},a.prototype.results_update_field=function(){return this.is_multiple||this.results_reset_cleanup(),this.result_clear_highlight(),this.result_single_selected=null,this.results_build()},a.prototype.results_toggle=function(){return this.results_showing?this.results_hide():this.results_show()},a.prototype.results_search=function(a){return this.results_showing?this.winnow_results():this.results_show()},a.prototype.keyup_checker=function(a){var b,c;b=(c=a.which)!=null?c:a.keyCode,this.search_field_scale();switch(b){case 8:if(this.is_multiple&&this.backstroke_length<1&&this.choices>0)return this.keydown_backstroke();if(!this.pending_backstroke)return this.result_clear_highlight(),this.results_search();break;case 13:a.preventDefault();if(this.results_showing)return this.result_select(a);break;case 27:return this.results_showing&&this.results_hide(),!0;case 9:case 38:case 40:case 16:case 91:case 17:break;default:return this.results_search()}},a.prototype.generate_field_id=function(){var a;return a=this.generate_random_id(),this.form_field.id=a,a},a.prototype.generate_random_char=function(){var a,b,c;return a="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",c=Math.floor(Math.random()*a.length),b=a.substring(c,c+1)},a}(),b.AbstractChosen=a}.call(this),function(){var a,b,c,d,e=Object.prototype.hasOwnProperty,f=function(a,b){function d(){this.constructor=a}for(var c in b)e.call(b,c)&&(a[c]=b[c]);return d.prototype=b.prototype,a.prototype=new d,a.__super__=b.prototype,a};d=this,a=jQuery,a.fn.extend({chosen:function(c){return!a.browser.msie||a.browser.version!=="6.0"&&a.browser.version!=="7.0"?this.each(function(d){var e;e=a(this);if(!e.hasClass("chzn-done"))return e.data("chosen",new b(this,c))}):this}}),b=function(b){function e(){e.__super__.constructor.apply(this,arguments)}return f(e,b),e.prototype.setup=function(){return this.form_field_jq=a(this.form_field),this.current_value=this.form_field_jq.val(),this.is_rtl=this.form_field_jq.hasClass("chzn-rtl")},e.prototype.finish_setup=function(){return this.form_field_jq.addClass("chzn-done")},e.prototype.set_up_html=function(){var b,d,e,f;return this.container_id=this.form_field.id.length?this.form_field.id.replace(/[^\w]/g,"_"):this.generate_field_id(),this.container_id+="_chzn",this.f_width=this.form_field_jq.outerWidth(),b=a("<div />",{id:this.container_id,"class":"chzn-container"+(this.is_rtl?" chzn-rtl":""),style:"width: "+this.f_width+"px;"}),this.is_multiple?b.html('<ul class="chzn-choices"><li class="search-field"><input type="text" value="'+this.default_text+'" class="default" autocomplete="off" style="width:25px;" /></li></ul><div class="chzn-drop" style="left:-9000px;"><ul class="chzn-results"></ul></div>'):b.html('<a href="javascript:void(0)" class="chzn-single chzn-default"><span>'+this.default_text+'</span><div><b></b></div></a><div class="chzn-drop" style="left:-9000px;"><div class="chzn-search"><input type="text" autocomplete="off" /></div><ul class="chzn-results"></ul></div>'),this.form_field_jq.hide().after(b),this.container=a("#"+this.container_id),this.container.addClass("chzn-container-"+(this.is_multiple?"multi":"single")),this.dropdown=this.container.find("div.chzn-drop").first(),d=this.container.height(),e=this.f_width-c(this.dropdown),this.dropdown.css({width:e+"px",top:d+"px"}),this.search_field=this.container.find("input").first(),this.search_results=this.container.find("ul.chzn-results").first(),this.search_field_scale(),this.search_no_results=this.container.find("li.no-results").first(),this.is_multiple?(this.search_choices=this.container.find("ul.chzn-choices").first(),this.search_container=this.container.find("li.search-field").first()):(this.search_container=this.container.find("div.chzn-search").first(),this.selected_item=this.container.find(".chzn-single").first(),f=e-c(this.search_container)-c(this.search_field),this.search_field.css({width:f+"px"})),this.results_build(),this.set_tab_index(),this.form_field_jq.trigger("liszt:ready",{chosen:this})},e.prototype.register_observers=function(){var a=this;return this.container.mousedown(function(b){return a.container_mousedown(b)}),this.container.mouseup(function(b){return a.container_mouseup(b)}),this.container.mouseenter(function(b){return a.mouse_enter(b)}),this.container.mouseleave(function(b){return a.mouse_leave(b)}),this.search_results.mouseup(function(b){return a.search_results_mouseup(b)}),this.search_results.mouseover(function(b){return a.search_results_mouseover(b)}),this.search_results.mouseout(function(b){return a.search_results_mouseout(b)}),this.form_field_jq.bind("liszt:updated",function(b){return a.results_update_field(b)}),this.search_field.blur(function(b){return a.input_blur(b)}),this.search_field.keyup(function(b){return a.keyup_checker(b)}),this.search_field.keydown(function(b){return a.keydown_checker(b)}),this.is_multiple?(this.search_choices.click(function(b){return a.choices_click(b)}),this.search_field.focus(function(b){return a.input_focus(b)})):this.container.click(function(a){return a.preventDefault()})},e.prototype.search_field_disabled=function(){this.is_disabled=this.form_field_jq[0].disabled;if(this.is_disabled)return this.container.addClass("chzn-disabled"),this.search_field[0].disabled=!0,this.is_multiple||this.selected_item.unbind("focus",this.activate_action),this.close_field();this.container.removeClass("chzn-disabled"),this.search_field[0].disabled=!1;if(!this.is_multiple)return this.selected_item.bind("focus",this.activate_action)},e.prototype.container_mousedown=function(b){var c;if(!this.is_disabled)return c=b!=null?a(b.target).hasClass("search-choice-close"):!1,b&&b.type==="mousedown"&&!this.results_showing&&b.stopPropagation(),!this.pending_destroy_click&&!c?(this.active_field?!this.is_multiple&&b&&(a(b.target)[0]===this.selected_item[0]||a(b.target).parents("a.chzn-single").length)&&(b.preventDefault(),this.results_toggle()):(this.is_multiple&&this.search_field.val(""),a(document).click(this.click_test_action),this.results_show()),this.activate_field()):this.pending_destroy_click=!1},e.prototype.container_mouseup=function(a){if(a.target.nodeName==="ABBR"&&!this.is_disabled)return this.results_reset(a)},e.prototype.blur_test=function(a){if(!this.active_field&&this.container.hasClass("chzn-container-active"))return this.close_field()},e.prototype.close_field=function(){return a(document).unbind("click",this.click_test_action),this.is_multiple||(this.selected_item.attr("tabindex",this.search_field.attr("tabindex")),this.search_field.attr("tabindex",-1)),this.active_field=!1,this.results_hide(),this.container.removeClass("chzn-container-active"),this.winnow_results_clear(),this.clear_backstroke(),this.show_search_field_default(),this.search_field_scale()},e.prototype.activate_field=function(){return!this.is_multiple&&!this.active_field&&(this.search_field.attr("tabindex",this.selected_item.attr("tabindex")),this.selected_item.attr("tabindex",-1)),this.container.addClass("chzn-container-active"),this.active_field=!0,this.search_field.val(this.search_field.val()),this.search_field.focus()},e.prototype.test_active_click=function(b){return a(b.target).parents("#"+this.container_id).length?this.active_field=!0:this.close_field()},e.prototype.results_build=function(){var a,b,c,e,f;this.parsing=!0,this.results_data=d.SelectParser.select_to_array(this.form_field),this.is_multiple&&this.choices>0?(this.search_choices.find("li.search-choice").remove(),this.choices=0):this.is_multiple||(this.selected_item.addClass("chzn-default").find("span").text(this.default_text),this.form_field.options.length<=this.disable_search_threshold?this.container.addClass("chzn-container-single-nosearch"):this.container.removeClass("chzn-container-single-nosearch")),a="",f=this.results_data;for(c=0,e=f.length;c<e;c++)b=f[c],b.group?a+=this.result_add_group(b):b.empty||(a+=this.result_add_option(b),b.selected&&this.is_multiple?this.choice_build(b):b.selected&&!this.is_multiple&&(this.selected_item.removeClass("chzn-default").find("span").text(b.text),this.allow_single_deselect&&this.single_deselect_control_build()));return this.search_field_disabled(),this.show_search_field_default(),this.search_field_scale(),this.search_results.html(a),this.parsing=!1},e.prototype.result_add_group=function(b){return b.disabled?"":(b.dom_id=this.container_id+"_g_"+b.array_index,'<li id="'+b.dom_id+'" class="group-result">'+a("<div />").text(b.label).html()+"</li>")},e.prototype.result_do_highlight=function(a){var b,c,d,e,f;if(a.length){this.result_clear_highlight(),this.result_highlight=a,this.result_highlight.addClass("highlighted"),d=parseInt(this.search_results.css("maxHeight"),10),f=this.search_results.scrollTop(),e=d+f,c=this.result_highlight.position().top+this.search_results.scrollTop(),b=c+this.result_highlight.outerHeight();if(b>=e)return this.search_results.scrollTop(b-d>0?b-d:0);if(c<f)return this.search_results.scrollTop(c)}},e.prototype.result_clear_highlight=function(){return this.result_highlight&&this.result_highlight.removeClass("highlighted"),this.result_highlight=null},e.prototype.results_show=function(){var a;if(!this.is_multiple)this.selected_item.addClass("chzn-single-with-drop"),this.result_single_selected&&this.result_do_highlight(this.result_single_selected);else if(this.max_selected_options<=this.choices)return this.form_field_jq.trigger("liszt:maxselected",{chosen:this}),!1;return a=this.is_multiple?this.container.height():this.container.height()-1,this.form_field_jq.trigger("liszt:showing_dropdown",{chosen:this}),this.dropdown.css({top:a+"px",left:0}),this.results_showing=!0,this.search_field.focus(),this.search_field.val(this.search_field.val()),this.winnow_results()},e.prototype.results_hide=function(){return this.is_multiple||this.selected_item.removeClass("chzn-single-with-drop"),this.result_clear_highlight(),this.form_field_jq.trigger("liszt:hiding_dropdown",{chosen:this}),this.dropdown.css({left:"-9000px"}),this.results_showing=!1},e.prototype.set_tab_index=function(a){var b;if(this.form_field_jq.attr("tabindex"))return b=this.form_field_jq.attr("tabindex"),this.form_field_jq.attr("tabindex",-1),this.is_multiple?this.search_field.attr("tabindex",b):(this.selected_item.attr("tabindex",b),this.search_field.attr("tabindex",-1))},e.prototype.show_search_field_default=function(){return this.is_multiple&&this.choices<1&&!this.active_field?(this.search_field.val(this.default_text),this.search_field.addClass("default")):(this.search_field.val(""),this.search_field.removeClass("default"))},e.prototype.search_results_mouseup=function(b){var c;c=a(b.target).hasClass("active-result")?a(b.target):a(b.target).parents(".active-result").first();if(c.length)return this.result_highlight=c,this.result_select(b)},e.prototype.search_results_mouseover=function(b){var c;c=a(b.target).hasClass("active-result")?a(b.target):a(b.target).parents(".active-result").first();if(c)return this.result_do_highlight(c)},e.prototype.search_results_mouseout=function(b){if(a(b.target).hasClass("active-result"))return this.result_clear_highlight()},e.prototype.choices_click=function(b){b.preventDefault();if(this.active_field&&!a(b.target).hasClass("search-choice")&&!this.results_showing)return this.results_show()},e.prototype.choice_build=function(b){var c,d,e=this;return this.is_multiple&&this.max_selected_options<=this.choices?(this.form_field_jq.trigger("liszt:maxselected",{chosen:this}),!1):(c=this.container_id+"_c_"+b.array_index,this.choices+=1,this.search_container.before('<li class="search-choice" id="'+c+'"><span>'+b.html+'</span><a href="javascript:void(0)" class="search-choice-close" rel="'+b.array_index+'"></a></li>'),d=a("#"+c).find("a").first(),d.click(function(a){return e.choice_destroy_link_click(a)}))},e.prototype.choice_destroy_link_click=function(b){return b.preventDefault(),this.is_disabled?b.stopPropagation:(this.pending_destroy_click=!0,this.choice_destroy(a(b.target)))},e.prototype.choice_destroy=function(a){return this.choices-=1,this.show_search_field_default(),this.is_multiple&&this.choices>0&&this.search_field.val().length<1&&this.results_hide(),this.result_deselect(a.attr("rel")),a.parents("li").first().remove()},e.prototype.results_reset=function(){this.form_field.options[0].selected=!0,this.selected_item.find("span").text(this.default_text),this.is_multiple||this.selected_item.addClass("chzn-default"),this.show_search_field_default(),this.results_reset_cleanup(),this.form_field_jq.trigger("change");if(this.active_field)return this.results_hide()},e.prototype.results_reset_cleanup=function(){return this.selected_item.find("abbr").remove()},e.prototype.result_select=function(a){var b,c,d,e;if(this.result_highlight)return b=this.result_highlight,c=b.attr("id"),this.result_clear_highlight(),this.is_multiple?this.result_deactivate(b):(this.search_results.find(".result-selected").removeClass("result-selected"),this.result_single_selected=b,this.selected_item.removeClass("chzn-default")),b.addClass("result-selected"),e=c.substr(c.lastIndexOf("_")+1),d=this.results_data[e],d.selected=!0,this.form_field.options[d.options_index].selected=!0,this.is_multiple?this.choice_build(d):(this.selected_item.find("span").first().text(d.text),this.allow_single_deselect&&this.single_deselect_control_build()),(!a.metaKey||!this.is_multiple)&&this.results_hide(),this.search_field.val(""),(this.is_multiple||this.form_field_jq.val()!==this.current_value)&&this.form_field_jq.trigger("change",{selected:this.form_field.options[d.options_index].value}),this.current_value=this.form_field_jq.val(),this.search_field_scale()},e.prototype.result_activate=function(a){return a.addClass("active-result")},e.prototype.result_deactivate=function(a){return a.removeClass("active-result")},e.prototype.result_deselect=function(b){var c,d;return d=this.results_data[b],d.selected=!1,this.form_field.options[d.options_index].selected=!1,c=a("#"+this.container_id+"_o_"+b),c.removeClass("result-selected").addClass("active-result").show(),this.result_clear_highlight(),this.winnow_results(),this.form_field_jq.trigger("change",{deselected:this.form_field.options[d.options_index].value}),this.search_field_scale()},e.prototype.single_deselect_control_build=function(){if(this.allow_single_deselect&&this.selected_item.find("abbr").length<1)return this.selected_item.find("span").first().after('<abbr class="search-choice-close"></abbr>')},e.prototype.winnow_results=function(){var b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s;this.no_results_clear(),j=0,k=this.search_field.val()===this.default_text?"":a("<div/>").text(a.trim(this.search_field.val())).html(),g=this.search_contains?"":"^",f=new RegExp(g+k.replace(/[-[\]{}()*+?.,\\^$|#\s]/g,"\\$&"),"i"),n=new RegExp(k.replace(/[-[\]{}()*+?.,\\^$|#\s]/g,"\\$&"),"i"),s=this.results_data;for(o=0,q=s.length;o<q;o++){c=s[o];if(!c.disabled&&!c.empty)if(c.group)a("#"+c.dom_id).css("display","none");else if(!this.is_multiple||!c.selected){b=!1,i=c.dom_id,h=a("#"+i);if(f.test(c.html))b=!0,j+=1;else if(c.html.indexOf(" ")>=0||c.html.indexOf("[")===0){e=c.html.replace(/\[|\]/g,"").split(" ");if(e.length)for(p=0,r=e.length;p<r;p++)d=e[p],f.test(d)&&(b=!0,j+=1)}b?(k.length?(l=c.html.search(n),m=c.html.substr(0,l+k.length)+"</em>"+c.html.substr(l+k.length),m=m.substr(0,l)+"<em>"+m.substr(l)):m=c.html,h.html(m),this.result_activate(h),c.group_array_index!=null&&a("#"+this.results_data[c.group_array_index].dom_id).css("display","list-item")):(this.result_highlight&&i===this.result_highlight.attr("id")&&this.result_clear_highlight(),this.result_deactivate(h))}}return j<1&&k.length?this.no_results(k):this.winnow_results_set_highlight()},e.prototype.winnow_results_clear=function(){var b,c,d,e,f;this.search_field.val(""),c=this.search_results.find("li"),f=[];for(d=0,e=c.length;d<e;d++)b=c[d],b=a(b),b.hasClass("group-result")?f.push(b.css("display","auto")):!this.is_multiple||!b.hasClass("result-selected")?f.push(this.result_activate(b)):f.push(void 0);return f},e.prototype.winnow_results_set_highlight=function(){var a,b;if(!this.result_highlight){b=this.is_multiple?[]:this.search_results.find(".result-selected.active-result"),a=b.length?b.first():this.search_results.find(".active-result").first();if(a!=null)return this.result_do_highlight(a)}},e.prototype.no_results=function(b){var c;return c=a('<li class="no-results">'+this.results_none_found+' "<span></span>"</li>'),c.find("span").first().html(b),this.search_results.append(c)},e.prototype.no_results_clear=function(){return this.search_results.find(".no-results").remove()},e.prototype.keydown_arrow=function(){var b,c;this.result_highlight?this.results_showing&&(c=this.result_highlight.nextAll("li.active-result").first(),c&&this.result_do_highlight(c)):(b=this.search_results.find("li.active-result").first(),b&&this.result_do_highlight(a(b)));if(!this.results_showing)return this.results_show()},e.prototype.keyup_arrow=function(){var a;if(!this.results_showing&&!this.is_multiple)return this.results_show();if(this.result_highlight)return a=this.result_highlight.prevAll("li.active-result"),a.length?this.result_do_highlight(a.first()):(this.choices>0&&this.results_hide(),this.result_clear_highlight())},e.prototype.keydown_backstroke=function(){return this.pending_backstroke?(this.choice_destroy(this.pending_backstroke.find("a").first()),this.clear_backstroke()):(this.pending_backstroke=this.search_container.siblings("li.search-choice").last(),this.single_backstroke_delete?this.keydown_backstroke():this.pending_backstroke.addClass("search-choice-focus"))},e.prototype.clear_backstroke=function(){return this.pending_backstroke&&this.pending_backstroke.removeClass("search-choice-focus"),this.pending_backstroke=null},e.prototype.keydown_checker=function(a){var b,c;b=(c=a.which)!=null?c:a.keyCode,this.search_field_scale(),b!==8&&this.pending_backstroke&&this.clear_backstroke();switch(b){case 8:this.backstroke_length=this.search_field.val().length;break;case 9:this.results_showing&&!this.is_multiple&&this.result_select(a),this.mouse_on_container=!1;break;case 13:a.preventDefault();break;case 38:a.preventDefault(),this.keyup_arrow();break;case 40:this.keydown_arrow()}},e.prototype.search_field_scale=function(){var b,c,d,e,f,g,h,i,j;if(this.is_multiple){d=0,h=0,f="position:absolute; left: -1000px; top: -1000px; display:none;",g=["font-size","font-style","font-weight","font-family","line-height","text-transform","letter-spacing"];for(i=0,j=g.length;i<j;i++)e=g[i],f+=e+":"+this.search_field.css(e)+";";return c=a("<div />",{style:f}),c.text(this.search_field.val()),a("body").append(c),h=c.width()+25,c.remove(),h>this.f_width-10&&(h=this.f_width-10),this.search_field.css({width:h+"px"}),b=this.container.height(),this.dropdown.css({top:b+"px"})}},e.prototype.generate_random_id=function(){var b;b="sel"+this.generate_random_char()+this.generate_random_char()+this.generate_random_char();while(a("#"+b).length>0)b+=this.generate_random_char();return b},e}(AbstractChosen),c=function(a){var b;return b=a.outerWidth()-a.width()},d.get_side_border_padding=c}.call(this);
(function(a){a.uniform={options:{selectClass:"selector",radioClass:"radio",checkboxClass:"checker",fileClass:"uploader",filenameClass:"filename",fileBtnClass:"action",fileDefaultText:"No file selected",fileBtnText:"Choose File",checkedClass:"checked",focusClass:"focus",disabledClass:"disabled",buttonClass:"button",activeClass:"active",hoverClass:"hover",useID:true,idPrefix:"uniform",resetSelector:false,autoHide:true},elements:[]};if(a.browser.msie&&a.browser.version<7){a.support.selectOpacity=false}else{a.support.selectOpacity=true}a.fn.uniform=function(k){k=a.extend(a.uniform.options,k);var d=this;if(k.resetSelector!=false){a(k.resetSelector).mouseup(function(){function l(){a.uniform.update(d)}setTimeout(l,10)})}function j(l){$el=a(l);$el.addClass($el.attr("type"));b(l)}function g(l){a(l).addClass("uniform");b(l)}function i(o){var m=a(o);var p=a("<div>"),l=a("<span>");p.addClass(k.buttonClass);if(k.useID&&m.attr("id")!=""){p.attr("id",k.idPrefix+"-"+m.attr("id"))}var n;if(m.is("a")||m.is("button")){n=m.text()}else{if(m.is(":submit")||m.is(":reset")||m.is("input[type=button]")){n=m.attr("value")}}n=n==""?m.is(":reset")?"Reset":"Submit":n;l.html(n);m.css("opacity",0);m.wrap(p);m.wrap(l);p=m.closest("div");l=m.closest("span");if(m.is(":disabled")){p.addClass(k.disabledClass)}p.bind({"mouseenter.uniform":function(){p.addClass(k.hoverClass)},"mouseleave.uniform":function(){p.removeClass(k.hoverClass);p.removeClass(k.activeClass)},"mousedown.uniform touchbegin.uniform":function(){p.addClass(k.activeClass)},"mouseup.uniform touchend.uniform":function(){p.removeClass(k.activeClass)},"click.uniform touchend.uniform":function(r){if(a(r.target).is("span")||a(r.target).is("div")){if(o[0].dispatchEvent){var q=document.createEvent("MouseEvents");q.initEvent("click",true,true);o[0].dispatchEvent(q)}else{o[0].click()}}}});o.bind({"focus.uniform":function(){p.addClass(k.focusClass)},"blur.uniform":function(){p.removeClass(k.focusClass)}});a.uniform.noSelect(p);b(o)}function e(o){var m=a(o);var p=a("<div />"),l=a("<span />");if(!m.css("display")=="none"&&k.autoHide){p.hide()}p.addClass(k.selectClass);if(k.useID&&o.attr("id")!=""){p.attr("id",k.idPrefix+"-"+o.attr("id"))}var n=o.find(":selected:first");if(n.length==0){n=o.find("option:first")}l.html(n.html());o.css("opacity",0);o.wrap(p);o.before(l);p=o.parent("div");l=o.siblings("span");o.bind({"change.uniform":function(){l.text(o.find(":selected").html());p.removeClass(k.activeClass)},"focus.uniform":function(){p.addClass(k.focusClass)},"blur.uniform":function(){p.removeClass(k.focusClass);p.removeClass(k.activeClass)},"mousedown.uniform touchbegin.uniform":function(){p.addClass(k.activeClass)},"mouseup.uniform touchend.uniform":function(){p.removeClass(k.activeClass)},"click.uniform touchend.uniform":function(){p.removeClass(k.activeClass)},"mouseenter.uniform":function(){p.addClass(k.hoverClass)},"mouseleave.uniform":function(){p.removeClass(k.hoverClass);p.removeClass(k.activeClass)},"keyup.uniform":function(){l.text(o.find(":selected").html())}});if(a(o).attr("disabled")){p.addClass(k.disabledClass)}a.uniform.noSelect(l);b(o)}function f(n){var m=a(n);var o=a("<div />"),l=a("<span />");if(!m.css("display")=="none"&&k.autoHide){o.hide()}o.addClass(k.checkboxClass);if(k.useID&&n.attr("id")!=""){o.attr("id",k.idPrefix+"-"+n.attr("id"))}a(n).wrap(o);a(n).wrap(l);l=n.parent();o=l.parent();a(n).css("opacity",0).bind({"focus.uniform":function(){o.addClass(k.focusClass)},"blur.uniform":function(){o.removeClass(k.focusClass)},"click.uniform touchend.uniform":function(){if(!a(n).attr("checked")){l.removeClass(k.checkedClass)}else{l.addClass(k.checkedClass)}},"mousedown.uniform touchbegin.uniform":function(){o.addClass(k.activeClass)},"mouseup.uniform touchend.uniform":function(){o.removeClass(k.activeClass)},"mouseenter.uniform":function(){o.addClass(k.hoverClass)},"mouseleave.uniform":function(){o.removeClass(k.hoverClass);o.removeClass(k.activeClass)}});if(a(n).attr("checked")){l.addClass(k.checkedClass)}if(a(n).attr("disabled")){o.addClass(k.disabledClass)}b(n)}function c(n){var m=a(n);var o=a("<div />"),l=a("<span />");if(!m.css("display")=="none"&&k.autoHide){o.hide()}o.addClass(k.radioClass);if(k.useID&&n.attr("id")!=""){o.attr("id",k.idPrefix+"-"+n.attr("id"))}a(n).wrap(o);a(n).wrap(l);l=n.parent();o=l.parent();a(n).css("opacity",0).bind({"focus.uniform":function(){o.addClass(k.focusClass)},"blur.uniform":function(){o.removeClass(k.focusClass)},"click.uniform touchend.uniform":function(){if(!a(n).attr("checked")){l.removeClass(k.checkedClass)}else{var p=k.radioClass.split(" ")[0];a("."+p+" span."+k.checkedClass+":has([name='"+a(n).attr("name")+"'])").removeClass(k.checkedClass);l.addClass(k.checkedClass)}},"mousedown.uniform touchend.uniform":function(){if(!a(n).is(":disabled")){o.addClass(k.activeClass)}},"mouseup.uniform touchbegin.uniform":function(){o.removeClass(k.activeClass)},"mouseenter.uniform touchend.uniform":function(){o.addClass(k.hoverClass)},"mouseleave.uniform":function(){o.removeClass(k.hoverClass);o.removeClass(k.activeClass)}});if(a(n).attr("checked")){l.addClass(k.checkedClass)}if(a(n).attr("disabled")){o.addClass(k.disabledClass)}b(n)}function h(q){var o=a(q);var r=a("<div />"),p=a("<span>"+k.fileDefaultText+"</span>"),m=a("<span>"+k.fileBtnText+"</span>");if(!o.css("display")=="none"&&k.autoHide){r.hide()}r.addClass(k.fileClass);p.addClass(k.filenameClass);m.addClass(k.fileBtnClass);if(k.useID&&o.attr("id")!=""){r.attr("id",k.idPrefix+"-"+o.attr("id"))}o.wrap(r);o.after(m);o.after(p);r=o.closest("div");p=o.siblings("."+k.filenameClass);m=o.siblings("."+k.fileBtnClass);if(!o.attr("size")){var l=r.width();o.attr("size",l/10)}var n=function(){var s=o.val();if(s===""){s=k.fileDefaultText}else{s=s.split(/[\/\\]+/);s=s[(s.length-1)]}p.text(s)};n();o.css("opacity",0).bind({"focus.uniform":function(){r.addClass(k.focusClass)},"blur.uniform":function(){r.removeClass(k.focusClass)},"mousedown.uniform":function(){if(!a(q).is(":disabled")){r.addClass(k.activeClass)}},"mouseup.uniform":function(){r.removeClass(k.activeClass)},"mouseenter.uniform":function(){r.addClass(k.hoverClass)},"mouseleave.uniform":function(){r.removeClass(k.hoverClass);r.removeClass(k.activeClass)}});if(a.browser.msie){o.bind("click.uniform.ie7",function(){setTimeout(n,0)})}else{o.bind("change.uniform",n)}if(o.attr("disabled")){r.addClass(k.disabledClass)}a.uniform.noSelect(p);a.uniform.noSelect(m);b(q)}a.uniform.restore=function(l){if(l==undefined){l=a(a.uniform.elements)}a(l).each(function(){if(a(this).is(":checkbox")){a(this).unwrap().unwrap()}else{if(a(this).is("select")){a(this).siblings("span").remove();a(this).unwrap()}else{if(a(this).is(":radio")){a(this).unwrap().unwrap()}else{if(a(this).is(":file")){a(this).siblings("span").remove();a(this).unwrap()}else{if(a(this).is("button, :submit, :reset, a, input[type='button']")){a(this).unwrap().unwrap()}}}}}a(this).unbind(".uniform");a(this).css("opacity","1");var m=a.inArray(a(l),a.uniform.elements);a.uniform.elements.splice(m,1)})};function b(l){l=a(l).get();if(l.length>1){a.each(l,function(m,n){a.uniform.elements.push(n)})}else{a.uniform.elements.push(l)}}a.uniform.noSelect=function(l){function m(){return false}a(l).each(function(){this.onselectstart=this.ondragstart=m;a(this).mousedown(m).css({MozUserSelect:"none"})})};a.uniform.update=function(l){if(l==undefined){l=a(a.uniform.elements)}l=a(l);l.each(function(){var n=a(this);if(n.is("select")){var m=n.siblings("span");var p=n.parent("div");p.removeClass(k.hoverClass+" "+k.focusClass+" "+k.activeClass);m.html(n.find(":selected").html());if(n.is(":disabled")){p.addClass(k.disabledClass)}else{p.removeClass(k.disabledClass)}}else{if(n.is(":checkbox")){var m=n.closest("span");var p=n.closest("div");p.removeClass(k.hoverClass+" "+k.focusClass+" "+k.activeClass);m.removeClass(k.checkedClass);if(n.is(":checked")){m.addClass(k.checkedClass)}if(n.is(":disabled")){p.addClass(k.disabledClass)}else{p.removeClass(k.disabledClass)}}else{if(n.is(":radio")){var m=n.closest("span");var p=n.closest("div");p.removeClass(k.hoverClass+" "+k.focusClass+" "+k.activeClass);m.removeClass(k.checkedClass);if(n.is(":checked")){m.addClass(k.checkedClass)}if(n.is(":disabled")){p.addClass(k.disabledClass)}else{p.removeClass(k.disabledClass)}}else{if(n.is(":file")){var p=n.parent("div");var o=n.siblings(k.filenameClass);btnTag=n.siblings(k.fileBtnClass);p.removeClass(k.hoverClass+" "+k.focusClass+" "+k.activeClass);o.text(n.val());if(n.is(":disabled")){p.addClass(k.disabledClass)}else{p.removeClass(k.disabledClass)}}else{if(n.is(":submit")||n.is(":reset")||n.is("button")||n.is("a")||l.is("input[type=button]")){var p=n.closest("div");p.removeClass(k.hoverClass+" "+k.focusClass+" "+k.activeClass);if(n.is(":disabled")){p.addClass(k.disabledClass)}else{p.removeClass(k.disabledClass)}}}}}}})};return this.each(function(){if(a.support.selectOpacity){var l=a(this);if(l.is("select")){if(l.attr("multiple")!=true){if(l.attr("size")==undefined||l.attr("size")<=1){e(l)}}}else{if(l.is(":checkbox")){f(l)}else{if(l.is(":radio")){c(l)}else{if(l.is(":file")){h(l)}else{if(l.is(":text, :password, input[type='email']")){j(l)}else{if(l.is("textarea")){g(l)}else{if(l.is("a")||l.is(":submit")||l.is(":reset")||l.is("button")||l.is("input[type=button]")){i(l)}}}}}}}}})}})(jQuery);
// ColorBox v1.3.19.3 - jQuery lightbox plugin
// (c) 2011 Jack Moore - jacklmoore.com
// License: http://www.opensource.org/licenses/mit-license.php
(function(a,b,c){function Z(c,d,e){var g=b.createElement(c);return d&&(g.id=f+d),e&&(g.style.cssText=e),a(g)}function $(a){var b=y.length,c=(Q+a)%b;return c<0?b+c:c}function _(a,b){return Math.round((/%/.test(a)?(b==="x"?z.width():z.height())/100:1)*parseInt(a,10))}function ab(a){return K.photo||/\.(gif|png|jpe?g|bmp|ico)((#|\?).*)?$/i.test(a)}function bb(){var b,c=a.data(P,e);c==null?(K=a.extend({},d),console&&console.log&&console.log("Error: cboxElement missing settings object")):K=a.extend({},c);for(b in K)a.isFunction(K[b])&&b.slice(0,2)!=="on"&&(K[b]=K[b].call(P));K.rel=K.rel||P.rel||"nofollow",K.href=K.href||a(P).attr("href"),K.title=K.title||P.title,typeof K.href=="string"&&(K.href=a.trim(K.href))}function cb(b,c){a.event.trigger(b),c&&c.call(P)}function db(){var a,b=f+"Slideshow_",c="click."+f,d,e,g;K.slideshow&&y[1]?(d=function(){F.text(K.slideshowStop).unbind(c).bind(j,function(){if(K.loop||y[Q+1])a=setTimeout(W.next,K.slideshowSpeed)}).bind(i,function(){clearTimeout(a)}).one(c+" "+k,e),r.removeClass(b+"off").addClass(b+"on"),a=setTimeout(W.next,K.slideshowSpeed)},e=function(){clearTimeout(a),F.text(K.slideshowStart).unbind([j,i,k,c].join(" ")).one(c,function(){W.next(),d()}),r.removeClass(b+"on").addClass(b+"off")},K.slideshowAuto?d():e()):r.removeClass(b+"off "+b+"on")}function eb(b){U||(P=b,bb(),y=a(P),Q=0,K.rel!=="nofollow"&&(y=a("."+g).filter(function(){var b=a.data(this,e),c;return b&&(c=b.rel||this.rel),c===K.rel}),Q=y.index(P),Q===-1&&(y=y.add(P),Q=y.length-1)),S||(S=T=!0,r.show(),K.returnFocus&&a(P).blur().one(l,function(){a(this).focus()}),q.css({opacity:+K.opacity,cursor:K.overlayClose?"pointer":"auto"}).show(),K.w=_(K.initialWidth,"x"),K.h=_(K.initialHeight,"y"),W.position(),o&&z.bind("resize."+p+" scroll."+p,function(){q.css({width:z.width(),height:z.height(),top:z.scrollTop(),left:z.scrollLeft()})}).trigger("resize."+p),cb(h,K.onOpen),J.add(D).hide(),I.html(K.close).show()),W.load(!0))}function fb(){!r&&b.body&&(Y=!1,z=a(c),r=Z(X).attr({id:e,"class":n?f+(o?"IE6":"IE"):""}).hide(),q=Z(X,"Overlay",o?"position:absolute":"").hide(),s=Z(X,"Wrapper"),t=Z(X,"Content").append(A=Z(X,"LoadedContent","width:0; height:0; overflow:hidden"),C=Z(X,"LoadingOverlay").add(Z(X,"LoadingGraphic")),D=Z(X,"Title"),E=Z(X,"Current"),G=Z(X,"Next"),H=Z(X,"Previous"),F=Z(X,"Slideshow").bind(h,db),I=Z(X,"Close")),s.append(Z(X).append(Z(X,"TopLeft"),u=Z(X,"TopCenter"),Z(X,"TopRight")),Z(X,!1,"clear:left").append(v=Z(X,"MiddleLeft"),t,w=Z(X,"MiddleRight")),Z(X,!1,"clear:left").append(Z(X,"BottomLeft"),x=Z(X,"BottomCenter"),Z(X,"BottomRight"))).find("div div").css({"float":"left"}),B=Z(X,!1,"position:absolute; width:9999px; visibility:hidden; display:none"),J=G.add(H).add(E).add(F),a(b.body).append(q,r.append(s,B)))}function gb(){return r?(Y||(Y=!0,L=u.height()+x.height()+t.outerHeight(!0)-t.height(),M=v.width()+w.width()+t.outerWidth(!0)-t.width(),N=A.outerHeight(!0),O=A.outerWidth(!0),r.css({"padding-bottom":L,"padding-right":M}),G.click(function(){W.next()}),H.click(function(){W.prev()}),I.click(function(){W.close()}),q.click(function(){K.overlayClose&&W.close()}),a(b).bind("keydown."+f,function(a){var b=a.keyCode;S&&K.escKey&&b===27&&(a.preventDefault(),W.close()),S&&K.arrowKey&&y[1]&&(b===37?(a.preventDefault(),H.click()):b===39&&(a.preventDefault(),G.click()))}),a("."+g,b).live("click",function(a){a.which>1||a.shiftKey||a.altKey||a.metaKey||(a.preventDefault(),eb(this))})),!0):!1}var d={transition:"elastic",speed:300,width:!1,initialWidth:"600",innerWidth:!1,maxWidth:!1,height:!1,initialHeight:"450",innerHeight:!1,maxHeight:!1,scalePhotos:!0,scrolling:!0,inline:!1,html:!1,iframe:!1,fastIframe:!0,photo:!1,href:!1,title:!1,rel:!1,opacity:.9,preloading:!0,current:"image {current} of {total}",previous:"previous",next:"next",close:"close",xhrError:"This content failed to load.",imgError:"This image failed to load.",open:!1,returnFocus:!0,reposition:!0,loop:!0,slideshow:!1,slideshowAuto:!0,slideshowSpeed:2500,slideshowStart:"start slideshow",slideshowStop:"stop slideshow",onOpen:!1,onLoad:!1,onComplete:!1,onCleanup:!1,onClosed:!1,overlayClose:!0,escKey:!0,arrowKey:!0,top:!1,bottom:!1,left:!1,right:!1,fixed:!1,data:undefined},e="colorbox",f="cbox",g=f+"Element",h=f+"_open",i=f+"_load",j=f+"_complete",k=f+"_cleanup",l=f+"_closed",m=f+"_purge",n=!a.support.opacity&&!a.support.style,o=n&&!c.XMLHttpRequest,p=f+"_IE6",q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X="div",Y;if(a.colorbox)return;a(fb),W=a.fn[e]=a[e]=function(b,c){var f=this;b=b||{},fb();if(gb()){if(!f[0]){if(f.selector)return f;f=a("<a/>"),b.open=!0}c&&(b.onComplete=c),f.each(function(){a.data(this,e,a.extend({},a.data(this,e)||d,b))}).addClass(g),(a.isFunction(b.open)&&b.open.call(f)||b.open)&&eb(f[0])}return f},W.position=function(a,b){function i(a){u[0].style.width=x[0].style.width=t[0].style.width=a.style.width,t[0].style.height=v[0].style.height=w[0].style.height=a.style.height}var c=0,d=0,e=r.offset(),g,h;z.unbind("resize."+f),r.css({top:-9e4,left:-9e4}),g=z.scrollTop(),h=z.scrollLeft(),K.fixed&&!o?(e.top-=g,e.left-=h,r.css({position:"fixed"})):(c=g,d=h,r.css({position:"absolute"})),K.right!==!1?d+=Math.max(z.width()-K.w-O-M-_(K.right,"x"),0):K.left!==!1?d+=_(K.left,"x"):d+=Math.round(Math.max(z.width()-K.w-O-M,0)/2),K.bottom!==!1?c+=Math.max(z.height()-K.h-N-L-_(K.bottom,"y"),0):K.top!==!1?c+=_(K.top,"y"):c+=Math.round(Math.max(z.height()-K.h-N-L,0)/2),r.css({top:e.top,left:e.left}),a=r.width()===K.w+O&&r.height()===K.h+N?0:a||0,s[0].style.width=s[0].style.height="9999px",r.dequeue().animate({width:K.w+O,height:K.h+N,top:c,left:d},{duration:a,complete:function(){i(this),T=!1,s[0].style.width=K.w+O+M+"px",s[0].style.height=K.h+N+L+"px",K.reposition&&setTimeout(function(){z.bind("resize."+f,W.position)},1),b&&b()},step:function(){i(this)}})},W.resize=function(a){S&&(a=a||{},a.width&&(K.w=_(a.width,"x")-O-M),a.innerWidth&&(K.w=_(a.innerWidth,"x")),A.css({width:K.w}),a.height&&(K.h=_(a.height,"y")-N-L),a.innerHeight&&(K.h=_(a.innerHeight,"y")),!a.innerHeight&&!a.height&&(A.css({height:"auto"}),K.h=A.height()),A.css({height:K.h}),W.position(K.transition==="none"?0:K.speed))},W.prep=function(b){function g(){return K.w=K.w||A.width(),K.w=K.mw&&K.mw<K.w?K.mw:K.w,K.w}function h(){return K.h=K.h||A.height(),K.h=K.mh&&K.mh<K.h?K.mh:K.h,K.h}if(!S)return;var c,d=K.transition==="none"?0:K.speed;A.remove(),A=Z(X,"LoadedContent").append(b),A.hide().appendTo(B.show()).css({width:g(),overflow:K.scrolling?"auto":"hidden"}).css({height:h()}).prependTo(t),B.hide(),a(R).css({"float":"none"}),o&&a("select").not(r.find("select")).filter(function(){return this.style.visibility!=="hidden"}).css({visibility:"hidden"}).one(k,function(){this.style.visibility="inherit"}),c=function(){function s(){n&&r[0].style.removeAttribute("filter")}var b,c,g=y.length,h,i="frameBorder",k="allowTransparency",l,o,p,q;if(!S)return;l=function(){clearTimeout(V),C.hide(),cb(j,K.onComplete)},n&&R&&A.fadeIn(100),D.html(K.title).add(A).show();if(g>1){typeof K.current=="string"&&E.html(K.current.replace("{current}",Q+1).replace("{total}",g)).show(),G[K.loop||Q<g-1?"show":"hide"]().html(K.next),H[K.loop||Q?"show":"hide"]().html(K.previous),K.slideshow&&F.show();if(K.preloading){b=[$(-1),$(1)];while(c=y[b.pop()])q=a.data(c,e),q&&q.href?(o=q.href,a.isFunction(o)&&(o=o.call(c))):o=c.href,ab(o)&&(p=new Image,p.src=o)}}else J.hide();K.iframe?(h=Z("iframe")[0],i in h&&(h[i]=0),k in h&&(h[k]="true"),h.name=f+ +(new Date),K.fastIframe?l():a(h).one("load",l),h.src=K.href,K.scrolling||(h.scrolling="no"),a(h).addClass(f+"Iframe").appendTo(A).one(m,function(){h.src="//about:blank"})):l(),K.transition==="fade"?r.fadeTo(d,1,s):s()},K.transition==="fade"?r.fadeTo(d,0,function(){W.position(0,c)}):W.position(d,c)},W.load=function(b){var c,d,e=W.prep;T=!0,R=!1,P=y[Q],b||bb(),cb(m),cb(i,K.onLoad),K.h=K.height?_(K.height,"y")-N-L:K.innerHeight&&_(K.innerHeight,"y"),K.w=K.width?_(K.width,"x")-O-M:K.innerWidth&&_(K.innerWidth,"x"),K.mw=K.w,K.mh=K.h,K.maxWidth&&(K.mw=_(K.maxWidth,"x")-O-M,K.mw=K.w&&K.w<K.mw?K.w:K.mw),K.maxHeight&&(K.mh=_(K.maxHeight,"y")-N-L,K.mh=K.h&&K.h<K.mh?K.h:K.mh),c=K.href,V=setTimeout(function(){C.show()},100),K.inline?(Z(X).hide().insertBefore(a(c)[0]).one(m,function(){a(this).replaceWith(A.children())}),e(a(c))):K.iframe?e(" "):K.html?e(K.html):ab(c)?(a(R=new Image).addClass(f+"Photo").error(function(){K.title=!1,e(Z(X,"Error").html(K.imgError))}).load(function(){var a;R.onload=null,K.scalePhotos&&(d=function(){R.height-=R.height*a,R.width-=R.width*a},K.mw&&R.width>K.mw&&(a=(R.width-K.mw)/R.width,d()),K.mh&&R.height>K.mh&&(a=(R.height-K.mh)/R.height,d())),K.h&&(R.style.marginTop=Math.max(K.h-R.height,0)/2+"px"),y[1]&&(K.loop||y[Q+1])&&(R.style.cursor="pointer",R.onclick=function(){W.next()}),n&&(R.style.msInterpolationMode="bicubic"),setTimeout(function(){e(R)},1)}),setTimeout(function(){R.src=c},1)):c&&B.load(c,K.data,function(b,c,d){e(c==="error"?Z(X,"Error").html(K.xhrError):a(this).contents())})},W.next=function(){!T&&y[1]&&(K.loop||y[Q+1])&&(Q=$(1),W.load())},W.prev=function(){!T&&y[1]&&(K.loop||Q)&&(Q=$(-1),W.load())},W.close=function(){S&&!U&&(U=!0,S=!1,cb(k,K.onCleanup),z.unbind("."+f+" ."+p),q.fadeTo(200,0),r.stop().fadeTo(300,0,function(){r.add(q).css({opacity:1,cursor:"auto"}).hide(),cb(m),A.remove(),setTimeout(function(){U=!1,cb(l,K.onClosed)},1)}))},W.remove=function(){a([]).add(r).add(q).remove(),r=null,a("."+g).removeData(e).removeClass(g).die()},W.element=function(){return a(P)},W.settings=d})(jQuery,document,this);
/*
 CLEditor WYSIWYG HTML Editor v1.3.0
 http://premiumsoftware.net/cleditor
 requires jQuery v1.4.2 or later

 Copyright 2010, Chris Landowski, Premium Software, LLC
 Dual licensed under the MIT or GPL Version 2 licenses.
*/
(function(e){function aa(a){var b=this,c=a.target,d=e.data(c,x),h=s[d],f=h.popupName,i=p[f];if(!(b.disabled||e(c).attr(n)==n)){var g={editor:b,button:c,buttonName:d,popup:i,popupName:f,command:h.command,useCSS:b.options.useCSS};if(h.buttonClick&&h.buttonClick(a,g)===false)return false;if(d=="source"){if(t(b)){delete b.range;b.$area.hide();b.$frame.show();c.title=h.title}else{b.$frame.hide();b.$area.show();c.title="Show Rich Text"}setTimeout(function(){u(b)},100)}else if(!t(b))if(f){var j=e(i);if(f==
"url"){if(d=="link"&&M(b)===""){z(b,"A selection is required when inserting a link.",c);return false}j.children(":button").unbind(q).bind(q,function(){var k=j.find(":text"),o=e.trim(k.val());o!==""&&v(b,g.command,o,null,g.button);k.val("http://");r();w(b)})}else f=="pastetext"&&j.children(":button").unbind(q).bind(q,function(){var k=j.find("textarea"),o=k.val().replace(/\n/g,"<br />");o!==""&&v(b,g.command,o,null,g.button);k.val("");r();w(b)});if(c!==e.data(i,A)){N(b,i,c);return false}return}else if(d==
"print")b.$frame[0].contentWindow.print();else if(!v(b,g.command,g.value,g.useCSS,c))return false;w(b)}}function O(a){a=e(a.target).closest("div");a.css(H,a.data(x)?"#FFF":"#FFC")}function P(a){e(a.target).closest("div").css(H,"transparent")}function ba(a){var b=a.data.popup,c=a.target;if(!(b===p.msg||e(b).hasClass(B))){var d=e.data(b,A),h=e.data(d,x),f=s[h],i=f.command,g,j=this.options.useCSS;if(h=="font")g=c.style.fontFamily.replace(/"/g,"");else if(h=="size"){if(c.tagName=="DIV")c=c.children[0];
g=c.innerHTML}else if(h=="style")g="<"+c.tagName+">";else if(h=="color")g=Q(c.style.backgroundColor);else if(h=="highlight"){g=Q(c.style.backgroundColor);if(l)i="backcolor";else j=true}b={editor:this,button:d,buttonName:h,popup:b,popupName:f.popupName,command:i,value:g,useCSS:j};if(!(f.popupClick&&f.popupClick(a,b)===false)){if(b.command&&!v(this,b.command,b.value,b.useCSS,d))return false;r();w(this)}}}function C(a){for(var b=1,c=0,d=0;d<a.length;++d){b=(b+a.charCodeAt(d))%65521;c=(c+b)%65521}return c<<
16|b}function R(a,b,c,d,h){if(p[a])return p[a];var f=e(m).hide().addClass(ca).appendTo("body");if(d)f.html(d);else if(a=="color"){b=b.colors.split(" ");b.length<10&&f.width("auto");e.each(b,function(i,g){e(m).appendTo(f).css(H,"#"+g)});c=da}else if(a=="font")e.each(b.fonts.split(","),function(i,g){e(m).appendTo(f).css("fontFamily",g).html(g)});else if(a=="size")e.each(b.sizes.split(","),function(i,g){e(m).appendTo(f).html("<font size="+g+">"+g+"</font>")});else if(a=="style")e.each(b.styles,function(i,
g){e(m).appendTo(f).html(g[1]+g[0]+g[1].replace("<","</"))});else if(a=="url"){f.html('Enter URL:<br><input type=text value="http://" size=35><br><input type=button value="Submit">');c=B}else if(a=="pastetext"){f.html("Paste your content here and click submit.<br /><textarea cols=40 rows=3></textarea><br /><input type=button value=Submit>");c=B}if(!c&&!d)c=S;f.addClass(c);l&&f.attr(I,"on").find("div,font,p,h1,h2,h3,h4,h5,h6").attr(I,"on");if(f.hasClass(S)||h===true)f.children().hover(O,P);p[a]=f[0];
return f[0]}function T(a,b){if(b){a.$area.attr(n,n);a.disabled=true}else{a.$area.removeAttr(n);delete a.disabled}try{if(l)a.doc.body.contentEditable=!b;else a.doc.designMode=!b?"on":"off"}catch(c){}u(a)}function v(a,b,c,d,h){D(a);if(!l){if(d===undefined||d===null)d=a.options.useCSS;a.doc.execCommand("styleWithCSS",0,d.toString())}d=true;var f;if(l&&b.toLowerCase()=="inserthtml")y(a).pasteHTML(c);else{try{d=a.doc.execCommand(b,0,c||null)}catch(i){f=i.description;d=false}d||("cutcopypaste".indexOf(b)>
-1?z(a,"For security reasons, your browser does not support the "+b+" command. Try using the keyboard shortcut or context menu instead.",h):z(a,f?f:"Error executing the "+b+" command.",h))}u(a);return d}function w(a){setTimeout(function(){t(a)?a.$area.focus():a.$frame[0].contentWindow.focus();u(a)},0)}function y(a){if(l)return J(a).createRange();return J(a).getRangeAt(0)}function J(a){if(l)return a.doc.selection;return a.$frame[0].contentWindow.getSelection()}function Q(a){var b=/rgba?\((\d+), (\d+), (\d+)/.exec(a),
c=a.split("");if(b)for(a=(b[1]<<16|b[2]<<8|b[3]).toString(16);a.length<6;)a="0"+a;return"#"+(a.length==6?a:c[1]+c[1]+c[2]+c[2]+c[3]+c[3])}function r(){e.each(p,function(a,b){e(b).hide().unbind(q).removeData(A)})}function U(){var a=e("link[href$='jquery.cleditor.css']").attr("href");return a.substr(0,a.length-19)+"images/"}function K(a){var b=a.$main,c=a.options;a.$frame&&a.$frame.remove();var d=a.$frame=e('<iframe frameborder="0" src="javascript:true;">').hide().appendTo(b),h=d[0].contentWindow,f=
a.doc=h.document,i=e(f);f.open();f.write(c.docType+"<html>"+(c.docCSSFile===""?"":'<head><link rel="stylesheet" type="text/css" href="'+c.docCSSFile+'" /></head>')+'<body style="'+c.bodyStyle+'"></body></html>');f.close();l&&i.click(function(){w(a)});E(a);if(l){i.bind("beforedeactivate beforeactivate selectionchange keypress",function(g){if(g.type=="beforedeactivate")a.inactive=true;else if(g.type=="beforeactivate"){!a.inactive&&a.range&&a.range.length>1&&a.range.shift();delete a.inactive}else if(!a.inactive){if(!a.range)a.range=
[];for(a.range.unshift(y(a));a.range.length>2;)a.range.pop()}});d.focus(function(){D(a)})}(e.browser.mozilla?i:e(h)).blur(function(){V(a,true)});i.click(r).bind("keyup mouseup",function(){u(a)});L?a.$area.show():d.show();e(function(){var g=a.$toolbar,j=g.children("div:last"),k=b.width();j=j.offset().top+j.outerHeight()-g.offset().top+1;g.height(j);j=(/%/.test(""+c.height)?b.height():parseInt(c.height))-j;d.width(k).height(j);a.$area.width(k).height(ea?j-2:j);T(a,a.disabled);u(a)})}function u(a){if(!L&&
e.browser.webkit&&!a.focused){a.$frame[0].contentWindow.focus();window.focus();a.focused=true}var b=a.doc;if(l)b=y(a);var c=t(a);e.each(a.$toolbar.find("."+W),function(d,h){var f=e(h),i=e.cleditor.buttons[e.data(h,x)],g=i.command,j=true;if(a.disabled)j=false;else if(i.getEnabled){j=i.getEnabled({editor:a,button:h,buttonName:i.name,popup:p[i.popupName],popupName:i.popupName,command:i.command,useCSS:a.options.useCSS});if(j===undefined)j=true}else if((c||L)&&i.name!="source"||l&&(g=="undo"||g=="redo"))j=
false;else if(g&&g!="print"){if(l&&g=="hilitecolor")g="backcolor";if(!l||g!="inserthtml")try{j=b.queryCommandEnabled(g)}catch(k){j=false}}if(j){f.removeClass(X);f.removeAttr(n)}else{f.addClass(X);f.attr(n,n)}})}function D(a){l&&a.range&&a.range[0].select()}function M(a){D(a);if(l)return y(a).text;return J(a).toString()}function z(a,b,c){var d=R("msg",a.options,fa);d.innerHTML=b;N(a,d,c)}function N(a,b,c){var d,h,f=e(b);if(c){var i=e(c);d=i.offset();h=--d.left;d=d.top+i.height()}else{i=a.$toolbar;
d=i.offset();h=Math.floor((i.width()-f.width())/2)+d.left;d=d.top+i.height()-2}r();f.css({left:h,top:d}).show();if(c){e.data(b,A,c);f.bind(q,{popup:b},e.proxy(ba,a))}setTimeout(function(){f.find(":text,textarea").eq(0).focus().select()},100)}function t(a){return a.$area.is(":visible")}function E(a,b){var c=a.$area.val(),d=a.options,h=d.updateFrame,f=e(a.doc.body);if(h){var i=C(c);if(b&&a.areaChecksum==i)return;a.areaChecksum=i}c=h?h(c):c;c=c.replace(/<(?=\/?script)/ig,"&lt;");if(d.updateTextArea)a.frameChecksum=
C(c);if(c!=f.html()){f.html(c);e(a).triggerHandler(F)}}function V(a,b){var c=e(a.doc.body).html(),d=a.options,h=d.updateTextArea,f=a.$area;if(h){var i=C(c);if(b&&a.frameChecksum==i)return;a.frameChecksum=i}c=h?h(c):c;if(d.updateFrame)a.areaChecksum=C(c);if(c!=f.val()){f.val(c);e(a).triggerHandler(F)}}e.cleditor={defaultOptions:{width:500,height:250,controls:"bold italic underline strikethrough subscript superscript | font size style | color highlight removeformat | bullets numbering | outdent indent | alignleft center alignright justify | undo redo | rule image link unlink | cut copy paste pastetext | print source",
colors:"FFF FCC FC9 FF9 FFC 9F9 9FF CFF CCF FCF CCC F66 F96 FF6 FF3 6F9 3FF 6FF 99F F9F BBB F00 F90 FC6 FF0 3F3 6CC 3CF 66C C6C 999 C00 F60 FC3 FC0 3C0 0CC 36F 63F C3C 666 900 C60 C93 990 090 399 33F 60C 939 333 600 930 963 660 060 366 009 339 636 000 300 630 633 330 030 033 006 309 303",fonts:"Arial,Arial Black,Comic Sans MS,Courier New,Narrow,Garamond,Georgia,Impact,Sans Serif,Serif,Tahoma,Trebuchet MS,Verdana",sizes:"1,2,3,4,5,6,7",styles:[["Paragraph","<p>"],["Header 1","<h1>"],["Header 2","<h2>"],
["Header 3","<h3>"],["Header 4","<h4>"],["Header 5","<h5>"],["Header 6","<h6>"]],useCSS:false,docType:'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',docCSSFile:"",bodyStyle:"margin:4px; font:10pt Arial,Verdana; cursor:text"},buttons:{init:"bold,,|italic,,|underline,,|strikethrough,,|subscript,,|superscript,,|font,,fontname,|size,Font Size,fontsize,|style,,formatblock,|color,Font Color,forecolor,|highlight,Text Highlight Color,hilitecolor,color|removeformat,Remove Formatting,|bullets,,insertunorderedlist|numbering,,insertorderedlist|outdent,,|indent,,|alignleft,Align Text Left,justifyleft|center,,justifycenter|alignright,Align Text Right,justifyright|justify,,justifyfull|undo,,|redo,,|rule,Insert Horizontal Rule,inserthorizontalrule|image,Insert Image,insertimage,url|link,Insert Hyperlink,createlink,url|unlink,Remove Hyperlink,|cut,,|copy,,|paste,,|pastetext,Paste as Text,inserthtml,|print,,|source,Show Source"},
imagesPath:function(){return U()}};e.fn.cleditor=function(a){var b=e([]);this.each(function(c,d){if(d.tagName=="TEXTAREA"){var h=e.data(d,Y);h||(h=new cleditor(d,a));b=b.add(h)}});return b};var H="backgroundColor",A="button",x="buttonName",F="change",Y="cleditor",q="click",n="disabled",m="<div>",I="unselectable",W="cleditorButton",X="cleditorDisabled",ca="cleditorPopup",S="cleditorList",da="cleditorColor",B="cleditorPrompt",fa="cleditorMsg",l=e.browser.msie,ea=/msie\s6/i.test(navigator.userAgent),
L=/iphone|ipad|ipod/i.test(navigator.userAgent),p={},Z,s=e.cleditor.buttons;e.each(s.init.split("|"),function(a,b){var c=b.split(","),d=c[0];s[d]={stripIndex:a,name:d,title:c[1]===""?d.charAt(0).toUpperCase()+d.substr(1):c[1],command:c[2]===""?d:c[2],popupName:c[3]===""?d:c[3]}});delete s.init;cleditor=function(a,b){var c=this;c.options=b=e.extend({},e.cleditor.defaultOptions,b);var d=c.$area=e(a).hide().data(Y,c).blur(function(){E(c,true)}),h=c.$main=e(m).addClass("cleditorMain").width(b.width).height(b.height),
f=c.$toolbar=e(m).addClass("cleditorToolbar").appendTo(h),i=e(m).addClass("cleditorGroup").appendTo(f);e.each(b.controls.split(" "),function(g,j){if(j==="")return true;if(j=="|"){e(m).addClass("cleditorDivider").appendTo(i);i=e(m).addClass("cleditorGroup").appendTo(f)}else{var k=s[j],o=e(m).data(x,k.name).addClass(W).attr("title",k.title).bind(q,e.proxy(aa,c)).appendTo(i).hover(O,P),G={};if(k.css)G=k.css;else if(k.image)G.backgroundImage="url("+U()+k.image+")";if(k.stripIndex)G.backgroundPosition=
k.stripIndex*-24;o.css(G);l&&o.attr(I,"on");k.popupName&&R(k.popupName,b,k.popupClass,k.popupContent,k.popupHover)}});h.insertBefore(d).append(d);if(!Z){e(document).click(function(g){g=e(g.target);g.add(g.parents()).is("."+B)||r()});Z=true}/auto|%/.test(""+b.width+b.height)&&e(window).resize(function(){K(c)});K(c)};var $=cleditor.prototype;e.each([["clear",function(a){a.$area.val("");E(a)}],["disable",T],["execCommand",v],["focus",w],["hidePopups",r],["sourceMode",t,true],["refresh",K],["select",
function(a){setTimeout(function(){t(a)?a.$area.select():v(a,"selectall")},0)}],["selectedHTML",function(a){D(a);a=y(a);if(l)return a.htmlText;var b=e("<layer>")[0];b.appendChild(a.cloneContents());return b.innerHTML},true],["selectedText",M,true],["showMessage",z],["updateFrame",E],["updateTextArea",V]],function(a,b){$[b[0]]=function(){for(var c=[this],d=0;d<arguments.length;d++)c.push(arguments[d]);c=b[1].apply(this,c);if(b[2])return c;return this}});$.change=function(a){var b=e(this);return a?b.bind(F,
a):b.trigger(F)}})(jQuery);
/**
* noty - jQuery Notification Plugin v1.2.1
* Contributors: https://github.com/needim/noty/graphs/contributors
*
* Examples and Documentation - http://needim.github.com/noty/
*
* Licensed under the MIT licenses:
* http://www.opensource.org/licenses/mit-license.php
*
**/
(function($) {
	$.noty = function(options, customContainer) {

		var base = {};
		var $noty = null;
		var isCustom = false;

		base.init = function(options) {
			base.options = $.extend({}, $.noty.defaultOptions, options);
			base.options.type = base.options.cssPrefix+base.options.type;
			base.options.id = base.options.type+'_'+new Date().getTime();
			base.options.layout = base.options.cssPrefix+'layout_'+base.options.layout;

			if (base.options.custom.container) customContainer = base.options.custom.container;
			isCustom = ($.type(customContainer) === 'object') ? true : false;

			return base.addQueue();
		};

		// Push notification to queue
		base.addQueue = function() {
			var isGrowl = ($.inArray(base.options.layout, $.noty.growls) == -1) ? false : true;
	  	if (!isGrowl) (base.options.force) ? $.noty.queue.unshift({options: base.options}) : $.noty.queue.push({options: base.options});
	  	return base.render(isGrowl);
		};

		// Render the noty
		base.render = function(isGrowl) {

			// Layout spesific container settings
			var container = (isCustom) ? customContainer.addClass(base.options.theme+' '+base.options.layout+' noty_custom_container') : $('body');
	  	if (isGrowl) {
	  		if ($('ul.noty_cont.' + base.options.layout).length == 0)
	  			container.prepend($('<ul/>').addClass('noty_cont ' + base.options.layout));
	  		container = $('ul.noty_cont.' + base.options.layout);
	  	} else {
	  		if ($.noty.available) {
					var fromQueue = $.noty.queue.shift(); // Get noty from queue
					if ($.type(fromQueue) === 'object') {
						$.noty.available = false;
						base.options = fromQueue.options;
					} else {
						$.noty.available = true; // Queue is over
						return base.options.id;
					}
	  		} else {
	  			return base.options.id;
	  		}
	  	}
	  	base.container = container;

	  	// Generating noty bar
	  	base.bar = $('<div class="noty_bar"/>').attr('id', base.options.id).addClass(base.options.theme+' '+base.options.layout+' '+base.options.type);
	  	$noty = base.bar;
	  	$noty.append(base.options.template).find('.noty_text').html(base.options.text);
	  	$noty.data('noty_options', base.options);

	  	// Close button display
	  	(base.options.closeButton) ? $noty.addClass('noty_closable').find('.noty_close').show() : $noty.find('.noty_close').remove();

	  	// Bind close event to button
	  	$noty.find('.noty_close').bind('click', function() { $noty.trigger('noty.close'); });

	  	// If we have a button we must disable closeOnSelfClick and closeOnSelfOver option
	  	if (base.options.buttons) base.options.closeOnSelfClick = base.options.closeOnSelfOver = false;
	  	// Close on self click
	  	if (base.options.closeOnSelfClick) $noty.bind('click', function() { $noty.trigger('noty.close'); }).css('cursor', 'pointer');
	  	// Close on self mouseover
	  	if (base.options.closeOnSelfOver) $noty.bind('mouseover', function() { $noty.trigger('noty.close'); }).css('cursor', 'pointer');

	  	// Set buttons if available
	  	if (base.options.buttons) {
				$buttons = $('<div/>').addClass('noty_buttons');
				$noty.find('.noty_message').append($buttons);
				$.each(base.options.buttons, function(i, button) {
					bclass = (button.type) ? button.type : 'gray';
					$button = $('<button/>').addClass(bclass).html(button.text).appendTo($noty.find('.noty_buttons'))
					.bind('click', function() {
						if ($.isFunction(button.click)) {
							button.click.call($button, $noty);
						}
					});
				});
			}

	  	return base.show(isGrowl);
		};

		base.show = function(isGrowl) {

			// is Modal?
			if (base.options.modal) $('<div/>').addClass('noty_modal').addClass(base.options.theme).prependTo($('body')).fadeIn('fast');

			$noty.close = function() { return this.trigger('noty.close'); };

			// Prepend noty to container
			(isGrowl) ? base.container.prepend($('<li/>').append($noty)) : base.container.prepend($noty);

	  	// topCenter and center specific options
	  	if (base.options.layout == 'noty_layout_topCenter' || base.options.layout == 'noty_layout_center') {
				$.noty.reCenter($noty);
			}

	  	$noty.bind('noty.setText', function(event, text) {
	  		$noty.find('.noty_text').html(text); 
	  		
	  		if (base.options.layout == 'noty_layout_topCenter' || base.options.layout == 'noty_layout_center') {
	  			$.noty.reCenter($noty);
	  		}
	  	});

	  	$noty.bind('noty.setType', function(event, type) {
	  		$noty.removeClass($noty.data('noty_options').type); 

			type = $noty.data('noty_options').cssPrefix+type;

			$noty.data('noty_options').type = type;

			$noty.addClass(type);
	  		
	  		if (base.options.layout == 'noty_layout_topCenter' || base.options.layout == 'noty_layout_center') {
	  			$.noty.reCenter($noty);
	  		}
	  	});

	  	$noty.bind('noty.getId', function(event) {
	  		return $noty.data('noty_options').id;
	  	});

	  	// Bind close event
	  	$noty.one('noty.close', function(event) {
				var options = $noty.data('noty_options');
        if(options.onClose){options.onClose();}

				// Modal Cleaning
				if (options.modal) $('.noty_modal').fadeOut('fast', function() { $(this).remove(); });

				$noty.clearQueue().stop().animate(
						$noty.data('noty_options').animateClose,
						$noty.data('noty_options').speed,
						$noty.data('noty_options').easing,
						$noty.data('noty_options').onClosed)
				.promise().done(function() {

					// Layout spesific cleaning
					if ($.inArray($noty.data('noty_options').layout, $.noty.growls) > -1) {
						$noty.parent().remove();
					} else {
						$noty.remove();

						// queue render
						$.noty.available = true;
						base.render(false);
					}

				});
			});

	  	// Start the show
      if(base.options.onShow){base.options.onShow();}
	  	$noty.animate(base.options.animateOpen, base.options.speed, base.options.easing, base.options.onShown);

	  	// If noty is have a timeout option
	  	if (base.options.timeout) $noty.delay(base.options.timeout).promise().done(function() { $noty.trigger('noty.close'); });
			return base.options.id;
		};

		// Run initializer
		return base.init(options);
	};

	// API
	$.noty.get = function(id) { return $('#'+id); };
	$.noty.close = function(id) {
		//remove from queue if not already visible
		for(var i=0;i<$.noty.queue.length;) {
			if($.noty.queue[i].options.id==id)
				$.noty.queue.splice(id,1);
			else
				i++;
		}
		//close if already visible
		$.noty.get(id).trigger('noty.close');
	};
	$.noty.setText = function(id, text) {
		$.noty.get(id).trigger('noty.setText', text);
	};
	$.noty.setType = function(id, type) {
		$.noty.get(id).trigger('noty.setType', type);
	};
	$.noty.closeAll = function() {
		$.noty.clearQueue();
		$('.noty_bar').trigger('noty.close');
	};
	$.noty.reCenter = function(noty) {
		noty.css({'left': ($(window).width() - noty.outerWidth()) / 2 + 'px'});
	};
	$.noty.clearQueue = function() {
		$.noty.queue = [];
	};
  
  var windowAlert = window.alert;
  $.noty.consumeAlert = function(options){
    window.alert = function(text){
      if(options){options.text = text;}
      else{options = {text:text};}
      $.noty(options);
    };
  }
  $.noty.stopConsumeAlert = function(){
    window.alert = windowAlert;
  }

	$.noty.queue = [];
	$.noty.growls = ['noty_layout_topLeft', 'noty_layout_topRight', 'noty_layout_bottomLeft', 'noty_layout_bottomRight'];
	$.noty.available = true;
	$.noty.defaultOptions = {
		layout: 'top',
		theme: 'noty_theme_default',
		animateOpen: {height: 'toggle'},
		animateClose: {height: 'toggle'},
		easing: 'swing',
		text: '',
		type: 'alert',
		speed: 500,
		timeout: 5000,
		closeButton: false,
		closeOnSelfClick: true,
		closeOnSelfOver: false,
		force: false,
		onShow: false,
		onShown: false,
		onClose: false,
		onClosed: false,
		buttons: false,
		modal: false,
		template: '<div class="noty_message"><span class="noty_text"></span><div class="noty_close"></div></div>',
		cssPrefix: 'noty_',
		custom: {
			container: null
		}
	};

	$.fn.noty = function(options) {
		return this.each(function() {
			 (new $.noty(options, $(this)));
		});
	};

})(jQuery);

//Helper
function noty(options) {
	return jQuery.noty(options); // returns an id
}

/*!
 * elFinder - file manager for web
 * Version 2.0 rc1 (2012-04-10)
 * http://elfinder.org
 * 
 * Copyright 2009-2012, Studio 42
 * Licensed under a 3 clauses BSD license
 */
(function(a){window.elFinder=function(b,c){this.time("load");var d=this,b=a(b),e=a("<div/>").append(b.contents()),f=b.attr("style"),g=b.attr("id")||"",h="elfinder-"+(g||Math.random().toString().substr(2,7)),i="mousedown."+h,j="keydown."+h,k="keypress."+h,l=!0,m=!0,n=["enable","disable","load","open","reload","select","add","remove","change","dblclick","getfile","lockfiles","unlockfiles","dragstart","dragstop"],o={},p="",q={path:"",url:"",tmbUrl:"",disabled:[],separator:"/",archives:[],extract:[],copyOverwrite:!0,tmb:!1},r={},s=[],t={},u={},v=[],w=[],x=[],y=new d.command(d),z="auto",A=400,B=a(document.createElement("audio")).hide().appendTo("body")[0],C,D=function(b){if(b.init)r={};else for(var c in r)r.hasOwnProperty(c)&&r[c].mime!="directory"&&r[c].phash==p&&a.inArray(c,w)===-1&&delete r[c];p=b.cwd.hash,E(b.files),r[p]||E([b.cwd]),d.lastDir(p)},E=function(a){var b=a.length,c;while(b--)c=a[b],c.name&&c.hash&&c.mime&&(r[c.hash]=c)},F=function(b){var c=b.keyCode,e=!!b.ctrlKey||!!b.metaKey;l&&(a.each(u,function(a,f){f.type==b.type&&f.keyCode==c&&f.shiftKey==b.shiftKey&&f.ctrlKey==e&&f.altKey==b.altKey&&(b.preventDefault(),b.stopPropagation(),f.callback(b,d),d.debug("shortcut-exec",a+" : "+f.description))}),c==9&&b.preventDefault())},G=new Date,H,I;this.api=null,this.newAPI=!1,this.oldAPI=!1,this.OS=navigator.userAgent.indexOf("Mac")!==-1?"mac":navigator.userAgent.indexOf("Win")!==-1?"win":"other",this.options=a.extend(!0,{},this._options,c||{}),c.ui&&(this.options.ui=c.ui),c.commands&&(this.options.commands=c.commands),c.uiOptions&&c.uiOptions.toolbar&&(this.options.uiOptions.toolbar=c.uiOptions.toolbar),a.extend(this.options.contextmenu,c.contextmenu),this.requestType=/^(get|post)$/i.test(this.options.requestType)?this.options.requestType.toLowerCase():"get",this.customData=a.isPlainObject(this.options.customData)?this.options.customData:{},this.id=g,this.uploadURL=c.urlUpload||c.url,this.namespace=h,this.lang=this.i18[this.options.lang]&&this.i18[this.options.lang].messages?this.options.lang:"en",I=this.lang=="en"?this.i18.en:a.extend(!0,{},this.i18.en,this.i18[this.lang]),this.direction=I.direction,this.messages=I.messages,this.dateFormat=this.options.dateFormat||I.dateFormat,this.fancyFormat=this.options.fancyDateFormat||I.fancyDateFormat,this.today=(new Date(G.getFullYear(),G.getMonth(),G.getDate())).getTime()/1e3,this.yesterday=this.today-86400,H=this.options.UTCDate?"UTC":"",this.getHours="get"+H+"Hours",this.getMinutes="get"+H+"Minutes",this.getSeconds="get"+H+"Seconds",this.getDate="get"+H+"Date",this.getDay="get"+H+"Day",this.getMonth="get"+H+"Month",this.getFullYear="get"+H+"FullYear",this.cssClass="ui-helper-reset ui-helper-clearfix ui-widget ui-widget-content ui-corner-all elfinder elfinder-"+(this.direction=="rtl"?"rtl":"ltr")+" "+this.options.cssClass,this.storage=function(){try{return"localStorage"in window&&window.localStorage!==null?d.localStorage:d.cookie}catch(a){return d.cookie}}(),this.notifyDelay=this.options.notifyDelay>0?parseInt(this.options.notifyDelay):500,this.draggable={appendTo:"body",addClasses:!0,delay:30,revert:!0,refreshPositions:!0,cursor:"move",cursorAt:{left:50,top:47},drag:function(a,b){b.helper.toggleClass("elfinder-drag-helper-plus",a.shiftKey||a.ctrlKey||a.metaKey)},stop:function(){d.trigger("focus").trigger("dragstop")},helper:function(b,c){var e=this.id?a(this):a(this).parents("[id]:first"),f=a('<div class="elfinder-drag-helper"><span class="elfinder-drag-helper-icon-plus"/></div>'),g=function(a){return'<div class="elfinder-cwd-icon '+d.mime2class(a)+' ui-corner-all"/>'},h,i;return d.trigger("dragstart",{target:e[0],originalEvent:b}),h=e.is("."+d.res("class","cwdfile"))?d.selected():[d.navId2Hash(e.attr("id"))],f.append(g(r[h[0]].mime)).data("files",h),(i=h.length)>1&&f.append(g(r[h[i-1]].mime)+'<span class="elfinder-drag-num">'+i+"</span>"),f}},this.droppable={tolerance:"pointer",accept:".elfinder-cwd-file-wrapper,.elfinder-navbar-dir,.elfinder-cwd-file",hoverClass:this.res("class","adroppable"),drop:function(b,c){var e=a(this),f=a.map(c.helper.data("files")||[],function(a){return a||null}),g=[],h="class",i,j,k,l;e.is("."+d.res(h,"cwd"))?j=p:e.is("."+d.res(h,"cwdfile"))?j=e.attr("id"):e.is("."+d.res(h,"navdir"))&&(j=d.navId2Hash(e.attr("id"))),i=f.length;while(i--)l=f[i],l!=j&&r[l].phash!=j&&g.push(l);g.length&&(c.helper.hide(),d.clipboard(g,!(b.ctrlKey||b.shiftKey||b.metaKey)),d.exec("paste",j).always(function(){d.clipboard([])}),d.trigger("drop",{files:f}))}},this.enabled=function(){return b.is(":visible")&&l},this.visible=function(){return b.is(":visible")},this.root=function(a){var b=r[a||p],c;while(b&&b.phash)b=r[b.phash];if(b)return b.hash;while(c in r&&r.hasOwnProperty(c)){b=r[c];if(!b.phash&&!b.mime=="directory"&&b.read)return b.hash}return""},this.cwd=function(){return r[p]||{}},this.option=function(a){return q[a]||""},this.file=function(a){return r[a]},this.files=function(){return a.extend(!0,{},r)},this.parents=function(a){var b=[],c;while(c=this.file(a))b.unshift(c.hash),a=c.phash;return b},this.path2array=function(a){var b,c=[];while(a&&(b=r[a])&&b.hash)c.unshift(b.name),a=b.phash;return c},this.path=function(a){return r[a]&&r[a].path?r[a].path:this.path2array(a).join(q.separator)},this.url=function(b){var c=r[b];if(!c||!c.read)return"";if(c.url)return c.url;if(q.url)return q.url+a.map(this.path2array(b),function(a){return encodeURIComponent(a)}).slice(1).join("/");var d=a.extend({},this.customData,{cmd:"file",target:c.hash});return this.oldAPI&&(d.cmd="open",d.current=c.phash),this.options.url+(this.options.url.indexOf("?")===-1?"?":"&")+a.param(d,!0)},this.tmb=function(b){var c=r[b],d=c&&c.tmb&&c.tmb!=1?q.tmbUrl+c.tmb:"";return d&&(a.browser.opera||a.browser.msie)&&(d+="?_="+(new Date).getTime()),d},this.selected=function(){return s.slice(0)},this.selectedFiles=function(){return a.map(s,function(a){return r[a]||null})},this.fileByName=function(a,b){var c;for(c in r)if(r.hasOwnProperty(c)&&r[c].phash==b&&r[c].name==a)return r[c]},this.validResponse=function(a,b){return b.error||this.rules[this.rules[a]?a:"defaults"](b)},this.request=function(b){var c=this,d=this.options,e=a.Deferred(),f=a.extend({},d.customData,{mimes:d.onlyMimes},b.data||b),g=f.cmd,h=!b.preventDefault&&!b.preventFail,i=!b.preventDefault&&!b.preventDone,j=a.extend({},b.notify),k=!!b.raw,l=b.syncOnFail,m,b=a.extend({url:d.url,async:!0,type:this.requestType,dataType:"json",cache:!1,data:f},b.options||{}),n=function(b){b.warning&&c.error(b.warning),g=="open"&&D(a.extend(!0,{},b)),b.removed&&b.removed.length&&c.remove(b),b.added&&b.added.length&&c.add(b),b.changed&&b.changed.length&&c.change(b),c.trigger(g,b),b.sync&&c.sync()},o=function(a,b){var c;switch(b){case"abort":c=a.quiet?"":["errConnect","errAbort"];break;case"timeout":c=["errConnect","errTimeout"];break;case"parsererror":c=["errResponse","errDataNotJSON"];break;default:a.status==403?c=["errConnect","errAccess"]:a.status==404?c=["errConnect","errNotFound"]:c="errConnect"}e.reject(c,a,b)},p=function(b){if(k)return e.resolve(b);if(!b)return e.reject(["errResponse","errDataEmpty"],r);if(!a.isPlainObject(b))return e.reject(["errResponse","errDataNotJSON"],r);if(b.error)return e.reject(b.error,r);if(!c.validResponse(g,b))return e.reject("errResponse",r);b=c.normalize(b),c.api||(c.api=b.api||1,c.newAPI=c.api>=2,c.oldAPI=!c.newAPI),b.options&&(q=a.extend({},q,b.options)),e.resolve(b),b.debug&&c.debug("backend-debug",b.debug)},r,s;i&&e.done(n),e.fail(function(a){a&&(h?c.error(a):c.debug("error",c.i18n(a)))});if(!g)return e.reject("errCmdReq");l&&e.fail(function(a){a&&c.sync()}),j.type&&j.cnt&&(m=setTimeout(function(){c.notify(j),e.always(function(){j.cnt=-(parseInt(j.cnt)||0),c.notify(j)})},c.notifyDelay),e.always(function(){clearTimeout(m)}));if(g=="open")while(s=x.pop())!s.isRejected()&&!s.isResolved()&&(s.quiet=!0,s.abort());return delete b.preventFail,r=this.transport.send(b).fail(o).done(p),g=="open"&&(x.unshift(r),e.always(function(){var b=a.inArray(r,x);b!==-1&&x.splice(b,1)})),e},this.diff=function(b){var c={},d=[],e=[],f=[],g=function(a){var b=f.length;while(b--)if(f[b].hash==a)return!0};return a.each(b,function(a,b){c[b.hash]=b}),a.each(r,function(a,b){!c[a]&&
e.push(a)}),a.each(c,function(b,c){var e=r[b];e?a.each(c,function(a){if(c[a]!=e[a])return f.push(c),!1}):d.push(c)}),a.each(e,function(b,d){var h=r[d],i=h.phash;i&&h.mime=="directory"&&a.inArray(i,e)===-1&&c[i]&&!g(i)&&f.push(c[i])}),{added:d,removed:e,changed:f}},this.sync=function(){var b=this,c=a.Deferred().done(function(){b.trigger("sync")}),d={data:{cmd:"open",init:1,target:p,tree:this.ui.tree?1:0},preventDefault:!0},e={data:{cmd:"parents",target:p},preventDefault:!0};return a.when(this.request(d),this.request(e)).fail(function(a){c.reject(a),a&&b.request({data:{cmd:"open",target:b.lastDir(""),tree:1,init:1},notify:{type:"open",cnt:1,hideCnt:!0}})}).done(function(a,d){var e=b.diff(a.files.concat(d&&d.tree?d.tree:[]));return e.removed.length&&b.remove(e),e.added.length&&b.add(e),e.changed.length&&b.change(e),c.resolve(e)}),c},this.upload=function(a){return this.transport.upload(a,this)},this.bind=function(a,b){var c;if(typeof b=="function"){a=(""+a).toLowerCase().split(/\s+/);for(c=0;c<a.length;c++)t[a[c]]===void 0&&(t[a[c]]=[]),t[a[c]].push(b)}return this},this.unbind=function(a,b){var c=t[(""+a).toLowerCase()]||[],d=c.indexOf(b);return d>-1&&c.splice(d,1),b=null,this},this.trigger=function(b,c){var b=b.toLowerCase(),d=t[b]||[],e,f;this.debug("event-"+b,c);if(d.length){b=a.Event(b);for(e=0;e<d.length;e++){b.data=a.extend(!0,{},c);try{if(d[e](b,this)===!1||b.isDefaultPrevented()){this.debug("event-stoped",b.type);break}}catch(g){window.console&&window.console.log&&window.console.log(g)}}}return this},this.shortcut=function(b){var c,d,e,f,g;if(this.options.allowShortcuts&&b.pattern&&a.isFunction(b.callback)){c=b.pattern.toUpperCase().split(/\s+/);for(f=0;f<c.length;f++)d=c[f],g=d.split("+"),e=(e=g.pop()).length==1?e>0?e:e.charCodeAt(0):a.ui.keyCode[e],e&&!u[d]&&(u[d]={keyCode:e,altKey:a.inArray("ALT",g)!=-1,ctrlKey:a.inArray("CTRL",g)!=-1,shiftKey:a.inArray("SHIFT",g)!=-1,type:b.type||"keydown",callback:b.callback,description:b.description,pattern:d})}return this},this.shortcuts=function(){var b=[];return a.each(u,function(a,c){b.push([c.pattern,d.i18n(c.description)])}),b},this.clipboard=function(b,c){var d=function(){return a.map(v,function(a){return a.hash})};return b!==void 0&&(v.length&&this.trigger("unlockfiles",{files:d()}),w=[],v=a.map(b||[],function(a){var b=r[a];return b?(w.push(a),{hash:a,phash:b.phash,name:b.name,mime:b.mime,read:b.read,locked:b.locked,cut:!!c}):null}),this.trigger("changeclipboard",{clipboard:v.slice(0,v.length)}),c&&this.trigger("lockfiles",{files:d()})),v.slice(0,v.length)},this.isCommandEnabled=function(b){return this._commands[b]?a.inArray(b,q.disabled)===-1:!1},this.exec=function(b,c,d){return this._commands[b]&&this.isCommandEnabled(b)?this._commands[b].exec(c,d):a.Deferred().reject("No such command")},this.dialog=function(c,d){return a("<div/>").append(c).appendTo(b).elfinderdialog(d)},this.getUI=function(a){return this.ui[a]||b},this.command=function(a){return a===void 0?this._commands:this._commands[a]},this.resize=function(a,c){b.css("width",a).height(c).trigger("resize"),this.trigger("resize",{width:b.width(),height:b.height()})},this.restoreSize=function(){this.resize(z,A)},this.show=function(){b.show(),this.enable().trigger("show")},this.hide=function(){this.disable().trigger("hide"),b.hide()},this.destroy=function(){b&&b[0].elfinder&&(this.trigger("destroy").disable(),t={},u={},a(document).add(b).unbind("."+this.namespace),d.trigger=function(){},b.children().remove(),b.append(e.contents()).removeClass(this.cssClass).attr("style",f),b[0].elfinder=null,C&&clearInterval(C))},this.setSort(this.options.sort,this.options.sortDirect);if(!(a.fn.selectable&&a.fn.draggable&&a.fn.droppable))return alert(this.i18n("errJqui"));if(!b.length)return alert(this.i18n("errNode"));if(!this.options.url)return alert(this.i18n("errURL"));a.extend(a.ui.keyCode,{F1:112,F2:113,F3:114,F4:115,F5:116,F6:117,F7:118,F8:119,F9:120}),this.dragUpload=!1,this.xhrUpload=typeof XMLHttpRequestUpload!="undefined"&&typeof File!="undefined"&&typeof FormData!="undefined",this.transport={},typeof this.options.transport=="object"&&(this.transport=this.options.transport,typeof this.transport.init=="function"&&this.transport.init(this)),typeof this.transport.send!="function"&&(this.transport.send=function(b){return a.ajax(b)}),this.transport.upload=="iframe"?this.transport.upload=a.proxy(this.uploads.iframe,this):typeof this.transport.upload=="function"?this.dragUpload=!!this.options.dragUploadAllow:this.xhrUpload?(this.transport.upload=a.proxy(this.uploads.xhr,this),this.dragUpload=!0):this.transport.upload=a.proxy(this.uploads.iframe,this),this.error=function(){var a=arguments[0];return arguments.length==1&&typeof a=="function"?d.bind("error",a):d.trigger("error",{error:a})},a.each(["enable","disable","load","open","reload","select","add","remove","change","dblclick","getfile","lockfiles","unlockfiles","dragstart","dragstop","search","searchend","viewchange"],function(b,c){d[c]=function(){var b=arguments[0];return arguments.length==1&&typeof b=="function"?d.bind(c,b):d.trigger(c,a.isPlainObject(b)?b:{})}}),this.enable(function(){!l&&d.visible()&&d.ui.overlay.is(":hidden")&&(l=!0,a("texarea:focus,input:focus,button").blur(),b.removeClass("elfinder-disabled"))}).disable(function(){m=l,l=!1,b.addClass("elfinder-disabled")}).open(function(){s=[]}).select(function(b){s=a.map(b.data.selected||b.data.value||[],function(a){return r[a]?a:null})}).error(function(b){var c={cssClass:"elfinder-dialog-error",title:d.i18n(d.i18n("error")),resizable:!1,destroyOnClose:!0,buttons:{}};c.buttons[d.i18n(d.i18n("btnClose"))]=function(){a(this).elfinderdialog("close")},d.dialog('<span class="elfinder-dialog-icon elfinder-dialog-icon-error"/>'+d.i18n(b.data.error),c)}).bind("tree parents",function(a){E(a.data.tree||[])}).bind("tmb",function(b){a.each(b.data.images||[],function(a,b){r[a]&&(r[a].tmb=b)})}).add(function(a){E(a.data.added||[])}).change(function(b){a.each(b.data.changed||[],function(b,c){var d=c.hash;r[d]=r[d]?a.extend(r[d],c):c})}).remove(function(b){var c=b.data.removed||[],d=c.length,e=function(b){var c=r[b];c&&(c.mime=="directory"&&c.dirs&&a.each(r,function(a,c){c.phash==b&&e(a)}),delete r[b])};while(d--)e(c[d])}).bind("search",function(a){E(a.data.files)}).bind("rm",function(b){var c=B.canPlayType&&B.canPlayType('audio/wav; codecs="1"');c&&c!=""&&c!="no"&&a(B).html('<source src="./sounds/rm.wav" type="audio/wav">')[0].play()}),a.each(this.options.handlers,function(a,b){d.bind(a,b)}),this.history=new this.history(this),typeof this.options.getFileCallback=="function"&&this.commands.getfile&&(this.bind("dblclick",function(a){a.preventDefault(),d.exec("getfile").fail(function(){d.exec("open")})}),this.shortcut({pattern:"enter",description:this.i18n("cmdgetfile"),callback:function(){d.exec("getfile").fail(function(){d.exec(d.OS=="mac"?"rename":"open")})}}).shortcut({pattern:"ctrl+enter",description:this.i18n(this.OS=="mac"?"cmdrename":"cmdopen"),callback:function(){d.exec(d.OS=="mac"?"rename":"open")}})),this._commands={},a.isArray(this.options.commands)||(this.options.commands=[]),a.each(["open","reload","back","forward","up","home","info","quicklook","getfile","help"],function(b,c){a.inArray(c,d.options.commands)===-1&&d.options.commands.push(c)}),a.each(this.options.commands,function(b,c){var e=d.commands[c];a.isFunction(e)&&!d._commands[c]&&(e.prototype=y,d._commands[c]=new e,d._commands[c].setup(c,d.options.commandsOptions[c]||{}))}),b.addClass(this.cssClass).bind(i,function(){!l&&d.enable()}),this.ui={workzone:a("<div/>").appendTo(b).elfinderworkzone(this),navbar:a("<div/>").appendTo(b).elfindernavbar(this,this.options.uiOptions.navbar||{}),contextmenu:a("<div/>").appendTo(b).elfindercontextmenu(this),overlay:a("<div/>").appendTo(b).elfinderoverlay({show:function(){d.disable()},hide:function(){m&&d.enable()}}),cwd:a("<div/>").appendTo(b).elfindercwd(this),notify:this.dialog("",{cssClass:"elfinder-dialog-notify",position:{top:"12px",right:"12px"},resizable:!1,autoOpen:!1,title:"&nbsp;",width:280}),statusbar:a('<div class="ui-widget-header ui-helper-clearfix ui-corner-bottom elfinder-statusbar"/>').hide().appendTo(b)},a.each(this.options.ui||
[],function(c,e){var f="elfinder"+e,g=d.options.uiOptions[e]||{};!d.ui[e]&&a.fn[f]&&(d.ui[e]=a("<"+(g.tag||"div")+"/>").appendTo(b)[f](d,g))}),b[0].elfinder=this,this.options.resizable&&a.fn.resizable&&b.resizable({handles:"se",minWidth:300,minHeight:200}),this.options.width&&(z=this.options.width),this.options.height&&(A=parseInt(this.options.height)),d.resize(z,A),a(document).bind("click."+this.namespace,function(c){l&&!a(c.target).closest(b).length&&d.disable()}).bind(j+" "+k,F),this.trigger("init").request({data:{cmd:"open",target:d.lastDir(),init:1,tree:this.ui.tree?1:0},preventDone:!0,notify:{type:"open",cnt:1,hideCnt:!0},freeze:!0}).fail(function(){d.trigger("fail").disable().lastDir(""),t={},u={},a(document).add(b).unbind("."+this.namespace),d.trigger=function(){}}).done(function(b){d.load().debug("api",d.api),b=a.extend(!0,{},b),D(b),d.trigger("open",b)}),this.one("load",function(){b.trigger("resize"),d.options.sync>1e3&&(C=setInterval(function(){d.sync()},d.options.sync))})},elFinder.prototype={res:function(a,b){return this.resources[a]&&this.resources[a][b]},i18:{en:{translator:"",language:"English",direction:"ltr",dateFormat:"d.m.Y H:i",fancyDateFormat:"$1 H:i",messages:{}},months:["January","February","March","April","May","June","July","August","September","October","November","December"],monthsShort:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],days:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],daysShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]},kinds:{unknown:"Unknown",directory:"Folder",symlink:"Alias","symlink-broken":"AliasBroken","application/x-empty":"TextPlain","application/postscript":"Postscript","application/vnd.ms-office":"MsOffice","application/vnd.ms-word":"MsWord","application/vnd.ms-excel":"MsExcel","application/vnd.ms-powerpoint":"MsPP","application/pdf":"PDF","application/xml":"XML","application/vnd.oasis.opendocument.text":"OO","application/x-shockwave-flash":"AppFlash","application/flash-video":"Flash video","application/x-bittorrent":"Torrent","application/javascript":"JS","application/rtf":"RTF","application/rtfd":"RTF","application/x-font-ttf":"TTF","application/x-font-otf":"OTF","application/x-rpm":"RPM","application/x-web-config":"TextPlain","application/xhtml+xml":"HTML","application/docbook+xml":"DOCBOOK","application/x-awk":"AWK","application/x-gzip":"GZIP","application/x-bzip2":"BZIP","application/zip":"ZIP","application/x-zip":"ZIP","application/x-rar":"RAR","application/x-tar":"TAR","application/x-7z-compressed":"7z","application/x-jar":"JAR","text/plain":"TextPlain","text/x-php":"PHP","text/html":"HTML","text/javascript":"JS","text/css":"CSS","text/rtf":"RTF","text/rtfd":"RTF","text/x-c":"C","text/x-csrc":"C","text/x-chdr":"CHeader","text/x-c++":"CPP","text/x-c++src":"CPP","text/x-c++hdr":"CPPHeader","text/x-shellscript":"Shell","application/x-csh":"Shell","text/x-python":"Python","text/x-java":"Java","text/x-java-source":"Java","text/x-ruby":"Ruby","text/x-perl":"Perl","text/x-sql":"SQL","text/xml":"XML","text/x-comma-separated-values":"CSV","image/x-ms-bmp":"BMP","image/jpeg":"JPEG","image/gif":"GIF","image/png":"PNG","image/tiff":"TIFF","image/x-targa":"TGA","image/vnd.adobe.photoshop":"PSD","image/xbm":"XBITMAP","image/pxm":"PXM","audio/mpeg":"AudioMPEG","audio/midi":"AudioMIDI","audio/ogg":"AudioOGG","audio/mp4":"AudioMPEG4","audio/x-m4a":"AudioMPEG4","audio/wav":"AudioWAV","audio/x-mp3-playlist":"AudioPlaylist","video/x-dv":"VideoDV","video/mp4":"VideoMPEG4","video/mpeg":"VideoMPEG","video/x-msvideo":"VideoAVI","video/quicktime":"VideoMOV","video/x-ms-wmv":"VideoWM","video/x-flv":"VideoFlash","video/x-matroska":"VideoMKV","video/ogg":"VideoOGG"},rules:{defaults:function(b){return!b||b.added&&!a.isArray(b.added)||b.removed&&!a.isArray(b.removed)||b.changed&&!a.isArray(b.changed)?!1:!0},open:function(b){return b&&b.cwd&&b.files&&a.isPlainObject(b.cwd)&&a.isArray(b.files)},tree:function(b){return b&&b.tree&&a.isArray(b.tree)},parents:function(b){return b&&b.tree&&a.isArray(b.tree)},tmb:function(b){return b&&b.images&&(a.isPlainObject(b.images)||a.isArray(b.images))},upload:function(b){return b&&(a.isPlainObject(b.added)||a.isArray(b.added))},search:function(b){return b&&b.files&&a.isArray(b.files)}},sorts:{nameDirsFirst:1,kindDirsFirst:2,sizeDirsFirst:3,dateDirsFirst:4,name:5,kind:6,size:7,date:8},setSort:function(a,b){this.sort=this.sorts[a]||1,this.sortDirect=b=="asc"||b=="desc"?b:"asc",this.trigger("sortchange")},commands:{},parseUploadData:function(b){var c;if(!a.trim(b))return{error:["errResponse","errDataEmpty"]};try{c=a.parseJSON(b)}catch(d){return{error:["errResponse","errDataNotJSON"]}}return this.validResponse("upload",c)?(c=this.normalize(c),c.removed=a.map(c.added||[],function(a){return a.hash}),c):{error:["errResponse"]}},iframeCnt:0,uploads:{iframe:function(b,c){var d=c?c:this,e=b.input,f=a.Deferred().fail(function(a){a&&d.error(a)}).done(function(a){a.warning&&d.error(a.warning),a.removed&&d.remove(a),a.added&&d.add(a),a.changed&&d.change(a),d.trigger("upload",a),a.sync&&d.sync()}),g="iframe-"+d.namespace+ ++d.iframeCnt,h=a('<form action="'+d.uploadURL+'" method="post" enctype="multipart/form-data" encoding="multipart/form-data" target="'+g+'" style="display:none"><input type="hidden" name="cmd" value="upload" /></form>'),i=a.browser.msie,j=function(){o&&clearTimeout(o),n&&clearTimeout(n),m&&d.notify({type:"upload",cnt:-l}),setTimeout(function(){i&&a('<iframe src="javascript:false;"/>').appendTo(h),h.remove(),k.remove()},100)},k=a('<iframe src="'+(i?"javascript:false;":"about:blank")+'" name="'+g+'" style="position:absolute;left:-1000px;top:-1000px" />').bind("load",function(){k.unbind("load").bind("load",function(){var a=d.parseUploadData(k.contents().text());j(),a.error?f.reject(a.error):f.resolve(a)}),n=setTimeout(function(){m=!0,d.notify({type:"upload",cnt:l})},d.options.notifyDelay),d.options.iframeTimeout>0&&(o=setTimeout(function(){j(),f.reject([errors.connect,errors.timeout])},d.options.iframeTimeout)),h.submit()}),l,m,n,o;return e&&a(e).is(":file")&&a(e).val()?(h.append(e),l=e.files?e.files.length:1,h.append('<input type="hidden" name="'+(d.newAPI?"target":"current")+'" value="'+d.cwd().hash+'"/>').append('<input type="hidden" name="html" value="1"/>').append(a(e).attr("name","upload[]")),a.each(d.options.onlyMimes||[],function(a,b){h.append('<input type="hidden" name="mimes[]" value="'+b+'"/>')}),a.each(d.options.customData,function(a,b){h.append('<input type="hidden" name="'+a+'" value="'+b+'"/>')}),h.appendTo("body"),k.appendTo("body"),f):f.reject()},xhr:function(b,c){var d=c?c:this,e=a.Deferred().fail(function(a){a&&d.error(a)}).done(function(a){a.warning&&d.error(a.warning),a.removed&&d.remove(a),a.added&&d.add(a),a.changed&&d.change(a),d.trigger("upload",a),a.sync&&d.sync()}).always(function(){m&&clearTimeout(m),k&&d.notify({type:"upload",cnt:-i,progress:100*i})}),f=new XMLHttpRequest,g=new FormData,h=b.input?b.input.files:b.files,i=h.length,j=5,k=!1,l=function(){return setTimeout(function(){k=!0,d.notify({type:"upload",cnt:i,progress:j*i})},d.options.notifyDelay)},m;if(!i)return e.reject();f.addEventListener("error",function(){e.reject("errConnect")},!1),f.addEventListener("abort",function(){e.reject(["errConnect","errAbort"])},!1),f.addEventListener("load",function(){var a=f.status,b;if(a>500)return e.reject("errResponse");if(a!=200)return e.reject("errConnect");if(f.readyState!=4)return e.reject(["errConnect","errTimeout"]);if(!f.responseText)return e.reject(["errResponse","errDataEmpty"]);b=d.parseUploadData(f.responseText),b.error?e.reject(b.error):e.resolve(b)},!1),f.upload.addEventListener("progress",function(a){var b=j,c;a.lengthComputable&&(c=parseInt(a.loaded*100/a.total),c>0&&!m&&(m=l()),c-b>4&&(j=c,k&&d.notify({type:"upload",cnt:0,progress:(j-b)*i})))},!1),f.open("POST",d.uploadURL,!0),g.append("cmd","upload"),g.append(d.newAPI?"target":"current",d.cwd().hash),a.each(d.options.customData,function(a,b){g.append(a,b)}),a.each(d.options.onlyMimes,function(a,b){g.append("mimes["+a+"]",b)}),a.each(h,function(a,b){g.append("upload[]",b)}),f.onreadystatechange=function(){f.readyState==4&&f.status==0&&
e.reject(["errConnect","errAbort"])},f.send(g);if(!a.browser.safari||!b.files)m=l();return e}},one:function(b,c){var d=this,e=a.proxy(c,function(a){return setTimeout(function(){d.unbind(a.type,e)},3),c.apply(this,arguments)});return this.bind(b,e)},localStorage:function(a,b){var c=window.localStorage;return a="elfinder-"+a+this.id,b!==void 0&&c.setItem(a,b),c.getItem(a)||""},cookie:function(b,c){var d,e,f,g;b="elfinder-"+b+this.id;if(c===void 0){if(document.cookie&&document.cookie!=""){f=document.cookie.split(";"),b+="=";for(g=0;g<f.length;g++){f[g]=a.trim(f[g]);if(f[g].substring(0,b.length)==b)return decodeURIComponent(f[g].substring(b.length))}}return""}return e=a.extend({},this.options.cookie),c===null&&(c="",e.expires=-1),typeof e.expires=="number"&&(d=new Date,d.setTime(d.getTime()+e.expires*864e5),e.expires=d),document.cookie=b+"="+encodeURIComponent(c)+"; expires="+e.expires.toUTCString()+(e.path?"; path="+e.path:"")+(e.domain?"; domain="+e.domain:"")+(e.secure?"; secure":""),c},lastDir:function(a){return this.options.rememberLastDir?this.storage("lastdir",a):""},_node:a("<span/>"),escape:function(a){return this._node.text(a).html()},normalize:function(b){var c=function(a){return a&&a.hash&&a.name&&a.mime?(a.mime=="application/x-empty"&&(a.mime="text/plain"),a):null};return b.files&&(b.files=a.map(b.files,c)),b.tree&&(b.tree=a.map(b.tree,c)),b.added&&(b.added=a.map(b.added,c)),b.changed&&(b.changed=a.map(b.changed,c)),b.api&&(b.init=!0),b},compare:function(a,b){var c=this.sort,d=this.sortDirect=="asc",e=d?a:b,f=d?b:a,g=this.mime2kind(e.mime).toLowerCase(),h=this.mime2kind(f.mime).toLowerCase(),i=a.mime=="directory",j=b.mime=="directory",k=e.name.toLowerCase(),l=f.name.toLowerCase(),m=i?0:parseInt(e.size)||0,n=j?0:parseInt(f.size)||0,o=e.ts||e.date||"",p=f.ts||f.date||"";if(c<=4){if(i&&!j)return-1;if(!i&&j)return 1}return c!=2&&c!=6||g==h?c!=3&&c!=7||m==n?c!=4&&c!=8||o==p?e.name.localeCompare(f.name):o>p?1:-1:m>n?1:-1:g.localeCompare(h)},sortFiles:function(b){return b.sort(a.proxy(this.compare,this))},notify:function(b){var c=b.type,d=this.messages["ntf"+c]?this.i18n("ntf"+c):this.i18n("ntfsmth"),e=this.ui.notify,f=e.children(".elfinder-notify-"+c),g='<div class="elfinder-notify elfinder-notify-{type}"><span class="elfinder-dialog-icon elfinder-dialog-icon-{type}"/><span class="elfinder-notify-msg">{msg}</span> <span class="elfinder-notify-cnt"/><div class="elfinder-notify-progressbar"><div class="elfinder-notify-progress"/></div></div>',h=b.cnt,i=b.progress>=0&&b.progress<=100?b.progress:0,j,k,l;return c?(f.length||(f=a(g.replace(/\{type\}/g,c).replace(/\{msg\}/g,d)).appendTo(e).data("cnt",0),i&&f.data({progress:0,total:0})),j=h+parseInt(f.data("cnt")),j>0?(!b.hideCnt&&f.children(".elfinder-notify-cnt").text("("+j+")"),e.is(":hidden")&&e.elfinderdialog("open"),f.data("cnt",j),i<100&&(k=f.data("total"))>=0&&(l=f.data("progress"))>=0&&(k=h+parseInt(f.data("total")),l=i+l,i=parseInt(l/k),f.data({progress:l,total:k}),e.find(".elfinder-notify-progress").animate({width:(i<100?i:100)+"%"},20))):(f.remove(),!e.children().length&&e.elfinderdialog("close")),this):this},confirm:function(b){var c=!1,d={cssClass:"elfinder-dialog-confirm",modal:!0,resizable:!1,title:this.i18n(b.title||"confirmReq"),buttons:{},close:function(){!c&&b.cancel.callback(),a(this).elfinderdialog("destroy")}},e=this.i18n("apllyAll"),f,g;return b.reject&&(d.buttons[this.i18n(b.reject.label)]=function(){b.reject.callback(!!g&&!!g.prop("checked")),c=!0,a(this).elfinderdialog("close")}),d.buttons[this.i18n(b.accept.label)]=function(){b.accept.callback(!!g&&!!g.prop("checked")),c=!0,a(this).elfinderdialog("close")},d.buttons[this.i18n(b.cancel.label)]=function(){a(this).elfinderdialog("close")},b.all&&(b.reject&&(d.width=370),d.create=function(){g=a('<input type="checkbox" />'),a(this).next().children().before(a("<label>"+e+"</label>").prepend(g))},d.open=function(){var b=a(this).next(),c=parseInt(b.children(":first").outerWidth()+b.children(":last").outerWidth());c>parseInt(b.width())&&a(this).closest(".elfinder-dialog").width(c+30)}),this.dialog('<span class="elfinder-dialog-icon elfinder-dialog-icon-confirm"/>'+this.i18n(b.text),d)},uniqueName:function(a,b){var c=0,d="",e,f;a=this.i18n(a),b=b||this.cwd().hash,(e=a.indexOf(".txt"))!=-1&&(d=".txt",a=a.substr(0,e)),f=a+d;if(!this.fileByName(f,b))return f;while(c<1e4){f=a+" "+ ++c+d;if(!this.fileByName(f,b))return f}return a+Math.random()+d},i18n:function(){var b=this,c=this.messages,d=[],e=[],f=function(a){var c;if(a.indexOf("#")===0)if(c=b.file(a.substr(1)))return c.name;return a},g,h,i;for(g=0;g<arguments.length;g++){i=arguments[g];if(typeof i=="string")d.push(f(i));else if(a.isArray(i))for(h=0;h<i.length;h++)typeof i[h]=="string"&&d.push(f(i[h]))}for(g=0;g<d.length;g++){if(a.inArray(g,e)!==-1)continue;i=d[g],i=c[i]||i,i=i.replace(/\$(\d+)/g,function(a,b){return b=g+parseInt(b),b>0&&d[b]&&e.push(b),d[b]||""}),d[g]=i}return a.map(d,function(b,c){return a.inArray(c,e)===-1?b:null}).join("<br>")},mime2class:function(a){var b="elfinder-cwd-icon-";return a=a.split("/"),b+a[0]+(a[0]!="image"&&a[1]?" "+b+a[1].replace(/(\.|\+)/g,"-"):"")},mime2kind:function(a){var b=typeof a=="object"?a.mime:a,c;a.alias?c="Alias":this.kinds[b]?c=this.kinds[b]:b.indexOf("text")===0?c="Text":b.indexOf("image")===0?c="Image":b.indexOf("audio")===0?c="Audio":b.indexOf("video")===0?c="Video":b.indexOf("application")===0?c="App":c=b;return this.messages["kind"+c]?this.i18n("kind"+c):b;var b,c},formatDate:function(a,b){var c=this,b=b||a.ts,d=c.i18,e,f,g,h,i,j,k,l,m,n,o;return c.options.clientFormatDate&&b>0?(e=new Date(b*1e3),l=e[c.getHours](),m=l>12?l-12:l,n=e[c.getMinutes](),o=e[c.getSeconds](),h=e[c.getDate](),i=e[c.getDay](),j=e[c.getMonth]()+1,k=e[c.getFullYear](),f=b>=this.yesterday?this.fancyFormat:this.dateFormat,g=f.replace(/[a-z]/gi,function(a){switch(a){case"d":return h>9?h:"0"+h;case"j":return h;case"D":return c.i18n(d.daysShort[i]);case"l":return c.i18n(d.days[i]);case"m":return j>9?j:"0"+j;case"n":return j;case"M":return c.i18n(d.monthsShort[j-1]);case"F":return c.i18n(d.months[j-1]);case"Y":return k;case"y":return(""+k).substr(2);case"H":return l>9?l:"0"+l;case"G":return l;case"g":return m;case"h":return m>9?m:"0"+m;case"a":return l>12?"pm":"am";case"A":return l>12?"PM":"AM";case"i":return n>9?n:"0"+n;case"s":return o>9?o:"0"+o}return a}),b>=this.yesterday?g.replace("$1",this.i18n(b>=this.today?"Today":"Yesterday")):g):a.date?a.date.replace(/([a-z]+)\s/i,function(a,b){return c.i18n(b)+" "}):c.i18n("dateUnknown")},perms2class:function(a){var b="";return!a.read&&!a.write?b="elfinder-na":a.read?a.write||(b="elfinder-ro"):b="elfinder-wo",b},formatPermissions:function(a){var b=[];return a.read&&b.push(this.i18n("read")),a.write&&b.push(this.i18n("write")),b.length?b.join(" "+this.i18n("and")+" "):this.i18n("noaccess")},formatSize:function(a){var b=1,c="b";return a=="unknown"?this.i18n("unknown"):(a>1073741824?(b=1073741824,c="GB"):a>1048576?(b=1048576,c="MB"):a>1024&&(b=1024,c="KB"),(a>0?Math.round(a/b):0)+" "+c)},navHash2Id:function(a){return"nav-"+a},navId2Hash:function(a){return typeof a=="string"?a.substr(4):!1},log:function(a){return window.console&&window.console.log&&window.console.log(a),this},debug:function(b,c){var d=this.options.debug;return(d=="all"||d===!0||a.isArray(d)&&a.inArray(b,d)!=-1)&&window.console&&window.console.log&&window.console.log("elfinder debug: ["+b+"] ["+this.id+"]",c),this},time:function(a){window.console&&window.console.time&&window.console.time(a)},timeEnd:function(a){window.console&&window.console.timeEnd&&window.console.timeEnd(a)}},elFinder.prototype.version="2.0 rc1",a.fn.elfinder=function(a){return a=="instance"?this.getElFinder():this.each(function(){var b=typeof a=="string"?a:"";this.elfinder||new elFinder(this,typeof a=="object"?a:{});switch(b){case"close":case"hide":this.elfinder.hide();break;case"open":case"show":this.elfinder.show();break;case"destroy":this.elfinder.destroy()}})},a.fn.getElFinder=function(){var a;return this.each(function(){if(this.elfinder)return a=this.elfinder,!1}),a},elFinder.prototype._options={url:"",requestType:"get",transport:{},urlUpload:"",dragUploadAllow:"auto",iframeTimeout
:0,customData:{},handlers:{},lang:"en",cssClass:"",commands:["open","reload","home","up","back","forward","getfile","quicklook","download","rm","duplicate","rename","mkdir","mkfile","upload","copy","cut","paste","edit","extract","archive","search","info","view","help","resize","sort"],commandsOptions:{getfile:{onlyURL:!0,multiple:!1,folders:!1,oncomplete:""},upload:{ui:"uploadbutton"},quicklook:{autoplay:!0,jplayer:"extensions/jplayer"},edit:{mimes:[],editors:[]},help:{view:["about","shortcuts","help"]}},getFileCallback:null,ui:["toolbar","tree","path","stat"],uiOptions:{toolbar:[["back","forward"],["mkdir","mkfile","upload"],["open","download","getfile"],["info"],["quicklook"],["copy","cut","paste"],["rm"],["duplicate","rename","edit","resize"],["extract","archive"],["search"],["view","sort"],["help"]],tree:{openRootOnLoad:!0,syncTree:!0},navbar:{minWidth:150,maxWidth:500}},onlyMimes:[],sort:"nameDirsFirst",sortDirect:"asc",clientFormatDate:!0,UTCDate:!1,dateFormat:"",fancyDateFormat:"",width:"auto",height:400,resizable:!0,notifyDelay:500,allowShortcuts:!0,rememberLastDir:!0,showFiles:30,showThreshold:50,validName:!1,sync:0,loadTmbs:5,cookie:{expires:30,domain:"",path:"/",secure:!1},contextmenu:{navbar:["open","|","copy","cut","paste","duplicate","|","rm","|","info"],cwd:["reload","back","|","upload","mkdir","mkfile","paste","|","sort","|","info"],files:["getfile","|","open","quicklook","|","download","|","copy","cut","paste","duplicate","|","rm","|","edit","rename","resize","|","archive","extract","|","info"]},debug:["error","warning","event-destroy"]},elFinder.prototype.history=function(b){var c=this,d=!0,e=[],f,g=function(){e=[b.cwd().hash],f=0,d=!0},h=function(h){return h&&c.canForward()||!h&&c.canBack()?(d=!1,b.exec("open",e[h?++f:--f]).fail(g)):a.Deferred().reject()};this.canBack=function(){return f>0},this.canForward=function(){return f<e.length-1},this.back=h,this.forward=function(){return h(!0)},b.open(function(a){var c=e.length,g=b.cwd().hash;d&&(f>=0&&c>f+1&&e.splice(f+1),e[e.length-1]!=g&&e.push(g),f=e.length-1),d=!0}).reload(g)},elFinder.prototype.command=function(b){this.fm=b,this.name="",this.title="",this.state=-1,this.alwaysEnabled=!1,this._disabled=!1,this.disableOnSearch=!1,this.updateOnSelect=!0,this._handlers={enable:function(){this.update(void 0,this.value)},disable:function(){this.update(-1,this.value)},"open reload load":function(a){this._disabled=!this.alwaysEnabled&&!this.fm.isCommandEnabled(this.name),this.update(void 0,this.value),this.change()}},this.handlers={},this.shortcuts=[],this.options={ui:"button"},this.setup=function(b,c){var d=this,e=this.fm,f,g;this.name=b,this.title=e.messages["cmd"+b]?e.i18n("cmd"+b):b,this.options=a.extend({},this.options,c),this.listeners=[],this.updateOnSelect&&(this._handlers.select=function(){this.update(void 0,this.value)}),a.each(a.extend({},d._handlers,d.handlers),function(b,c){e.bind(b,a.proxy(c,d))});for(f=0;f<this.shortcuts.length;f++)g=this.shortcuts[f],g.callback=a.proxy(g.callback||function(){this.exec()},this),!g.description&&(g.description=this.title),e.shortcut(g);this.disableOnSearch&&e.bind("search searchend",function(a){d._disabled=a.type=="search",d.update(void 0,d.value)}),this.init()},this.init=function(){},this.exec=function(b,c){return a.Deferred().reject()},this.disabled=function(){return this.state<0},this.enabled=function(){return this.state>-1},this.active=function(){return this.state>0},this.getstate=function(){return-1},this.update=function(a,b){var c=this.state,d=this.value;this._disabled?this.state=-1:this.state=a!==void 0?a:this.getstate(),this.value=b,(c!=this.state||d!=this.value)&&this.change()},this.change=function(a){var b,c;if(typeof a=="function")this.listeners.push(a);else for(c=0;c<this.listeners.length;c++){b=this.listeners[c];try{b(this.state,this.value)}catch(d){this.fm.debug("error",d)}}return this},this.hashes=function(c){return c?a.map(a.isArray(c)?c:[c],function(a){return b.file(a)?a:null}):b.selected()},this.files=function(b){var c=this.fm;return b?a.map(a.isArray(b)?b:[b],function(a){return c.file(a)||null}):c.selectedFiles()}},elFinder.prototype.resources={"class":{hover:"ui-state-hover",active:"ui-state-active",disabled:"ui-state-disabled",draggable:"ui-draggable",droppable:"ui-droppable",adroppable:"elfinder-droppable-active",cwdfile:"elfinder-cwd-file",cwd:"elfinder-cwd",tree:"elfinder-tree",treeroot:"elfinder-navbar-root",navdir:"elfinder-navbar-dir",navdirwrap:"elfinder-navbar-dir-wrapper",navarrow:"elfinder-navbar-arrow",navsubtree:"elfinder-navbar-subtree",navcollapse:"elfinder-navbar-collapsed",navexpand:"elfinder-navbar-expanded",treedir:"elfinder-tree-dir",placedir:"elfinder-place-dir",searchbtn:"elfinder-button-search"},tpl:{perms:'<span class="elfinder-perms"/>',symlink:'<span class="elfinder-symlink"/>',navicon:'<span class="elfinder-nav-icon"/>',navspinner:'<span class="elfinder-navbar-spinner"/>',navdir:'<div class="elfinder-navbar-wrapper"><span id="{id}" class="ui-corner-all elfinder-navbar-dir {cssclass}"><span class="elfinder-navbar-arrow"/><span class="elfinder-navbar-icon"/>{symlink}{permissions}{name}</span><div class="elfinder-navbar-subtree"/></div>'},mimes:{text:["application/x-empty","application/javascript","application/xhtml+xml","audio/x-mp3-playlist","application/x-web-config","application/docbook+xml","application/x-php","application/x-perl","application/x-awk","application/x-config","application/x-csh","application/xml"]},mixin:{make:function(){var b=this.fm,c=this.name,d=b.getUI("cwd"),e=a.Deferred().fail(function(a){a&&b.error(a)}).always(function(){k.remove(),j.remove(),b.enable()}),f="tmp_"+parseInt(Math.random()*1e5),g=b.cwd().hash,h=new Date,i={hash:f,name:b.uniqueName(this.prefix),mime:this.mime,read:!0,write:!0,date:"Today "+h.getHours()+":"+h.getMinutes()},j=d.trigger("create."+b.namespace,i).find("#"+f),k=a('<input type="text"/>').keydown(function(b){b.stopImmediatePropagation(),b.keyCode==a.ui.keyCode.ESCAPE?e.reject():b.keyCode==a.ui.keyCode.ENTER&&k.blur()}).mousedown(function(a){a.stopPropagation()}).blur(function(){var d=a.trim(k.val()),h=k.parent();if(h.length){if(!d)return e.reject("errInvName");if(b.fileByName(d,g))return e.reject(["errExists",d]);h.html(b.escape(d)),b.lockfiles({files:[f]}),b.request({data:{cmd:c,name:d,target:g},notify:{type:c,cnt:1},preventFail:!0,syncOnFail:!0}).fail(function(a){e.reject(a)}).done(function(a){e.resolve(a)})}});return this.disabled()||!j.length?e.reject():(b.disable(),j.find(".elfinder-cwd-filename").empty("").append(k.val(i.name)),k.select().focus(),e)}}},a.fn.dialogelfinder=function(b){var c="elfinderPosition",d="elfinderDestroyOnClose";this.not(".elfinder").each(function(){var e=a(document),f=a('<div class="ui-widget-header dialogelfinder-drag ui-corner-top">'+(b.title||"Files")+"</div>"),g=a('<a href="#" class="dialogelfinder-drag-close ui-corner-all"><span class="ui-icon ui-icon-closethick"/></a>').appendTo(f).click(function(a){a.preventDefault(),h.dialogelfinder("close")}),h=a(this).addClass("dialogelfinder").css("position","absolute").hide().appendTo("body").draggable({handle:".dialogelfinder-drag",containment:"parent"}).elfinder(b).prepend(f),i=h.elfinder("instance");h.width(parseInt(h.width())||840).data(d,!!b.destroyOnClose).find(".elfinder-toolbar").removeClass("ui-corner-top"),b.position&&h.data(c,b.position),b.autoOpen!==!1&&a(this).dialogelfinder("open")});if(b=="open"){var e=a(this),f=e.data(c)||{top:parseInt(a(document).scrollTop()+(a(window).height()<e.height()?2:(a(window).height()-e.height())/2)),left:parseInt(a(document).scrollLeft()+(a(window).width()<e.width()?2:(a(window).width()-e.width())/2))},g=100;e.is(":hidden")&&(a("body").find(":visible").each(function(){var b=a(this),c;this!==e[0]&&b.css("position")=="absolute"&&(c=parseInt(b.zIndex()))>g&&(g=c+1)}),e.zIndex(g).css(f).show().trigger("resize"),setTimeout(function(){e.trigger("resize").mousedown()},200))}else if(b=="close"){var e=a(this);e.is(":visible")&&(e.data(d)?e.elfinder("destroy").remove():e.elfinder("close"))}else if(b=="instance")return a(this).getElFinder();return this},elFinder&&elFinder.prototype&&typeof elFinder.prototype.i18=="object"&&(elFinder.prototype
.i18.en={translator:"Troex Nevelin &lt;troex@fury.scancode.ru&gt;",language:"English",direction:"ltr",dateFormat:"M d, Y h:i A",fancyDateFormat:"$1 h:i A",messages:{error:"Error",errUnknown:"Unknown error.",errUnknownCmd:"Unknown command.",errJqui:"Invalid jQuery UI configuration. Selectable, draggable and droppable components must be included.",errNode:"elFinder requires DOM Element to be created.",errURL:"Invalid elFinder configuration! URL option is not set.",errAccess:"Access denied.",errConnect:"Unable to connect to backend.",errAbort:"Connection aborted.",errTimeout:"Connection timeout.",errNotFound:"Backend not found.",errResponse:"Invalid backend response.",errConf:"Invalid backend configuration.",errJSON:"PHP JSON module not installed.",errNoVolumes:"Readable volumes not available.",errCmdParams:'Invalid parameters for command "$1".',errDataNotJSON:"Data is not JSON.",errDataEmpty:"Data is empty.",errCmdReq:"Backend request requires command name.",errOpen:'Unable to open "$1".',errNotFolder:"Object is not a folder.",errNotFile:"Object is not a file.",errRead:'Unable to read "$1".',errWrite:'Unable to write into "$1".',errPerm:"Permission denied.",errLocked:'"$1" is locked and can not be renamed, moved or removed.',errExists:'File named "$1" already exists.',errInvName:"Invalid file name.",errFolderNotFound:"Folder not found.",errFileNotFound:"File not found.",errTrgFolderNotFound:'Target folder "$1" not found.',errPopup:"Browser prevented opening popup window. To open file enable it in browser options.",errMkdir:'Unable to create folder "$1".',errMkfile:'Unable to create file "$1".',errRename:'Unable to rename "$1".',errCopyFrom:'Copying files from volume "$1" not allowed.',errCopyTo:'Copying files to volume "$1" not allowed.',errUpload:"Upload error.",errUploadFile:'Unable to upload "$1".',errUploadNoFiles:"No files found for upload.",errUploadTotalSize:"Data exceeds the maximum allowed size.",errUploadFileSize:"File exceeds maximum allowed size.",errUploadMime:"File type not allowed.",errUploadTransfer:'"$1" transfer error.',errNotReplace:'Object "$1" already exists at this location and can not be replaced by object with another type.',errReplace:'Unable to replace "$1".',errSave:'Unable to save "$1".',errCopy:'Unable to copy "$1".',errMove:'Unable to move "$1".',errCopyInItself:'Unable to copy "$1" into itself.',errRm:'Unable to remove "$1".',errRmSrc:"Unable remove source file(s).",errExtract:'Unable to extract files from "$1".',errArchive:"Unable to create archive.",errArcType:"Unsupported archive type.",errNoArchive:"File is not archive or has unsupported archive type.",errCmdNoSupport:"Backend does not support this command.",errReplByChild:"The folder “$1” can’t be replaced by an item it contains.",errArcSymlinks:"For security reason denied to unpack archives contains symlinks.",errArcMaxSize:"Archive files exceeds maximum allowed size.",errResize:'Unable to resize "$1".',errUsupportType:"Unsupported file type.",errNotUTF8Content:'File "$1" is not in UTF-8 and cannot be edited.',cmdarchive:"Create archive",cmdback:"Back",cmdcopy:"Copy",cmdcut:"Cut",cmddownload:"Download",cmdduplicate:"Duplicate",cmdedit:"Edit file",cmdextract:"Extract files from archive",cmdforward:"Forward",cmdgetfile:"Select files",cmdhelp:"About this software",cmdhome:"Home",cmdinfo:"Get info",cmdmkdir:"New folder",cmdmkfile:"New text file",cmdopen:"Open",cmdpaste:"Paste",cmdquicklook:"Preview",cmdreload:"Reload",cmdrename:"Rename",cmdrm:"Delete",cmdsearch:"Find files",cmdup:"Go to parent directory",cmdupload:"Upload files",cmdview:"View",cmdresize:"Resize & Rotate",cmdsort:"Sort",btnClose:"Close",btnSave:"Save",btnRm:"Remove",btnApply:"Apply",btnCancel:"Cancel",btnNo:"No",btnYes:"Yes",ntfopen:"Open folder",ntffile:"Open file",ntfreload:"Reload folder content",ntfmkdir:"Creating directory",ntfmkfile:"Creating files",ntfrm:"Delete files",ntfcopy:"Copy files",ntfmove:"Move files",ntfprepare:"Prepare to copy files",ntfrename:"Rename files",ntfupload:"Uploading files",ntfdownload:"Downloading files",ntfsave:"Save files",ntfarchive:"Creating archive",ntfextract:"Extracting files from archive",ntfsearch:"Searching files",ntfresize:"Resizing images",ntfsmth:"Doing something >_<",ntfloadimg:"Loading image",dateUnknown:"unknown",Today:"Today",Yesterday:"Yesterday",Jan:"Jan",Feb:"Feb",Mar:"Mar",Apr:"Apr",May:"May",Jun:"Jun",Jul:"Jul",Aug:"Aug",Sep:"Sep",Oct:"Oct",Nov:"Nov",Dec:"Dec",sortnameDirsFirst:"by name (folders first)",sortkindDirsFirst:"by kind (folders first)",sortsizeDirsFirst:"by size (folders first)",sortdateDirsFirst:"by date (folders first)",sortname:"by name",sortkind:"by kind",sortsize:"by size",sortdate:"by date",confirmReq:"Confirmation required",confirmRm:"Are you sure you want to remove files?<br/>This cannot be undone!",confirmRepl:"Replace old file with new one?",apllyAll:"Apply to all",name:"Name",size:"Size",perms:"Permissions",modify:"Modified",kind:"Kind",read:"read",write:"write",noaccess:"no access",and:"and",unknown:"unknown",selectall:"Select all files",selectfiles:"Select file(s)",selectffile:"Select first file",selectlfile:"Select last file",viewlist:"List view",viewicons:"Icons view",places:"Places",calc:"Calculate",path:"Path",aliasfor:"Alias for",locked:"Locked",dim:"Dimensions",files:"Files",folders:"Folders",items:"Items",yes:"yes",no:"no",link:"Link",searcresult:"Search results",selected:"selected items",about:"About",shortcuts:"Shortcuts",help:"Help",webfm:"Web file manager",ver:"Version",protocol:"protocol version",homepage:"Project home",docs:"Documentation",github:"Fork us on Github",twitter:"Follow us on twitter",facebook:"Join us on facebook",team:"Team",chiefdev:"chief developer",developer:"developer",contributor:"contributor",maintainer:"maintainer",translator:"translator",icons:"Icons",dontforget:"and don't forget to take your towel",shortcutsof:"Shortcuts disabled",dropFiles:"Drop files here",or:"or",selectForUpload:"Select files to upload",moveFiles:"Move files",copyFiles:"Copy files",rmFromPlaces:"Remove from places",aspectRatio:"Aspect ratio",scale:"Scale",width:"Width",height:"Height",resize:"Resize",crop:"Crop",rotate:"Rotate","rotate-cw":"Rotate 90 degrees CW","rotate-ccw":"Rotate 90 degrees CCW",degree:"°",kindUnknown:"Unknown",kindFolder:"Folder",kindAlias:"Alias",kindAliasBroken:"Broken alias",kindApp:"Application",kindPostscript:"Postscript document",kindMsOffice:"Microsoft Office document",kindMsWord:"Microsoft Word document",kindMsExcel:"Microsoft Excel document",kindMsPP:"Microsoft Powerpoint presentation",kindOO:"Open Office document",kindAppFlash:"Flash application",kindPDF:"Portable Document Format (PDF)",kindTorrent:"Bittorrent file",kind7z:"7z archive",kindTAR:"TAR archive",kindGZIP:"GZIP archive",kindBZIP:"BZIP archive",kindZIP:"ZIP archive",kindRAR:"RAR archive",kindJAR:"Java JAR file",kindTTF:"True Type font",kindOTF:"Open Type font",kindRPM:"RPM package",kindText:"Text document",kindTextPlain:"Plain text",kindPHP:"PHP source",kindCSS:"Cascading style sheet",kindHTML:"HTML document",kindJS:"Javascript source",kindRTF:"Rich Text Format",kindC:"C source",kindCHeader:"C header source",kindCPP:"C++ source",kindCPPHeader:"C++ header source",kindShell:"Unix shell script",kindPython:"Python source",kindJava:"Java source",kindRuby:"Ruby source",kindPerl:"Perl script",kindSQL:"SQL source",kindXML:"XML document",kindAWK:"AWK source",kindCSV:"Comma separated values",kindDOCBOOK:"Docbook XML document",kindImage:"Image",kindBMP:"BMP image",kindJPEG:"JPEG image",kindGIF:"GIF Image",kindPNG:"PNG Image",kindTIFF:"TIFF image",kindTGA:"TGA image",kindPSD:"Adobe Photoshop image",kindXBITMAP:"X bitmap image",kindPXM:"Pixelmator image",kindAudio:"Audio media",kindAudioMPEG:"MPEG audio",kindAudioMPEG4:"MPEG-4 audio",kindAudioMIDI:"MIDI audio",kindAudioOGG:"Ogg Vorbis audio",kindAudioWAV:"WAV audio",AudioPlaylist:"MP3 playlist",kindVideo:"Video media",kindVideoDV:"DV movie",kindVideoMPEG:"MPEG movie",kindVideoMPEG4:"MPEG-4 movie",kindVideoAVI:"AVI movie",kindVideoMOV:"Quick Time movie",kindVideoWM:"Windows Media movie",kindVideoFlash:"Flash movie",kindVideoMKV:"Matroska movie",kindVideoOGG:"Ogg movie"}}),a.fn.elfinderbutton=
function(b){return this.each(function(){var c="class",d=b.fm,e=d.res(c,"disabled"),f=d.res(c,"active"),g=d.res(c,"hover"),h="elfinder-button-menu-item",i="elfinder-button-menu-item-selected",j,k=a(this).addClass("ui-state-default elfinder-button").attr("title",b.title).append('<span class="elfinder-button-icon elfinder-button-icon-'+b.name+'"/>').hover(function(a){!k.is("."+e)&&k[a.type=="mouseleave"?"removeClass":"addClass"](g)}).click(function(a){k.is("."+e)||(j&&b.variants.length>1?(j.is(":hidden")&&b.fm.getUI().click(),a.stopPropagation(),j.slideToggle(100)):b.exec())}),l=function(){j.hide()};a.isArray(b.variants)&&(k.addClass("elfinder-menubutton"),j=a('<div class="ui-widget ui-widget-content elfinder-button-menu ui-corner-all"/>').hide().appendTo(k).zIndex(10+k.zIndex()).delegate("."+h,"hover",function(){a(this).toggleClass(g)}).delegate("."+h,"click",function(c){c.preventDefault(),c.stopPropagation(),k.removeClass(g),b.exec(b.fm.selected(),a(this).data("value"))}),b.fm.bind("disable select",l).getUI().click(l),b.change(function(){j.html(""),a.each(b.variants,function(c,d){j.append(a('<div class="'+h+'">'+d[1]+"</div>").data("value",d[0]).addClass(d[0]==b.value?i:""))})})),b.change(function(){b.disabled()?k.removeClass(f+" "+g).addClass(e):(k.removeClass(e),k[b.active()?"addClass":"removeClass"](f))}).change()})},a.fn.elfindercontextmenu=function(b){return this.each(function(){var c=a(this).addClass("ui-helper-reset ui-widget ui-state-default ui-corner-all elfinder-contextmenu elfinder-contextmenu-"+b.direction).hide().appendTo("body").delegate(".elfinder-contextmenu-item","hover",function(){a(this).toggleClass("ui-state-hover")}),d=b.direction=="ltr"?"left":"right",e=a.extend({},b.options.contextmenu),f='<div class="elfinder-contextmenu-item"><span class="elfinder-button-icon {icon} elfinder-contextmenu-icon"/><span>{label}</span></div>',g=function(b,c,d){return a(f.replace("{icon}",c?"elfinder-button-icon-"+c:"").replace("{label}",b)).click(function(a){a.stopPropagation(),a.stopPropagation(),d()})},h=function(e,f){var g=a(window),h=c.outerWidth(),i=c.outerHeight(),j=g.width(),k=g.height(),l=g.scrollTop(),m=g.scrollLeft(),n={top:(f+i<k?f:f-i>0?f-i:f)+l,left:(e+h<j?e:e-h)+m,"z-index":100+b.getUI("workzone").zIndex()};c.css(n).show(),n={"z-index":n["z-index"]+10},n[d]=parseInt(c.width()),c.find(".elfinder-contextmenu-sub").css(n)},i=function(){c.hide().empty()},j=function(d,f){var h=!1;a.each(e[d]||[],function(d,e){var j,k,l;if(e=="|"&&h){c.append('<div class="elfinder-contextmenu-separator"/>'),h=!1;return}j=b.command(e);if(j&&j.getstate(f)!=-1){if(j.variants){if(!j.variants.length)return;k=g(j.title,j.name,function(){}),l=a('<div class="ui-corner-all elfinder-contextmenu-sub"/>').appendTo(k.append('<span class="elfinder-contextmenu-arrow"/>')),k.addClass("elfinder-contextmenu-group").hover(function(){l.toggle()}),a.each(j.variants,function(b,c){l.append(a('<div class="elfinder-contextmenu-item"><span>'+c[1]+"</span></div>").click(function(a){a.stopPropagation(),i(),j.exec(f,c[0])}))})}else k=g(j.title,j.name,function(){i(),j.exec(f)});c.append(k),h=!0}})},k=function(b){a.each(b,function(a,b){var d;b.label&&typeof b.callback=="function"&&(d=g(b.label,b.icon,function(){i(),b.callback()}),c.append(d))})};b.one("load",function(){b.bind("contextmenu",function(a){var b=a.data;i(),b.type&&b.targets?j(b.type,b.targets):b.raw&&k(b.raw),c.children().length&&h(b.x,b.y)}).one("destroy",function(){c.remove()}).bind("disable select",i).getUI().click(i)})})},a.fn.elfindercwd=function(b){return this.not(".elfinder-cwd").each(function(){var c=b.storage("view")=="list",d="undefined",e="select."+b.namespace,f="unselect."+b.namespace,g="disable."+b.namespace,h="enable."+b.namespace,i="class",j=b.res(i,"cwdfile"),k="."+j,l="ui-selected",m=b.res(i,"disabled"),n=b.res(i,"draggable"),o=b.res(i,"droppable"),p=b.res(i,"hover"),q=b.res(i,"adroppable"),r=j+"-tmp",s=b.options.loadTmbs>0?b.options.loadTmbs:5,t="",u={icon:'<div id="{hash}" class="'+j+' {permsclass} {dirclass} ui-corner-all"><div class="elfinder-cwd-file-wrapper ui-corner-all"><div class="elfinder-cwd-icon {mime} ui-corner-all" unselectable="on" {style}/>{marker}</div><div class="elfinder-cwd-filename" title="{name}">{name}</div></div>',row:'<tr id="{hash}" class="'+j+' {permsclass} {dirclass}"><td><div class="elfinder-cwd-file-wrapper"><span class="elfinder-cwd-icon {mime}"/>{marker}<span class="elfinder-cwd-filename">{name}</span></div></td><td>{perms}</td><td>{date}</td><td>{size}</td><td>{kind}</td></tr>'},v=b.res("tpl","perms"),w=b.res("tpl","symlink"),x={permsclass:function(a){return b.perms2class(a)},perms:function(a){return b.formatPermissions(a)},dirclass:function(a){return a.mime=="directory"?"directory":""},mime:function(a){return b.mime2class(a.mime)},size:function(a){return b.formatSize(a.size)},date:function(a){return b.formatDate(a)},kind:function(a){return b.mime2kind(a)},marker:function(a){return(a.alias||a.mime=="symlink-broken"?w:"")+(!a.read||!a.write?v:"")}},y=function(a){return a.name=b.escape(a.name),u[c?"row":"icon"].replace(/\{([a-z]+)\}/g,function(b,c){return x[c]?x[c](a):a[c]?a[c]:""})},z=!1,A=function(b,d){function r(a,b){return a[b+"All"]("[id]:not(."+m+"):first")}var g=a.ui.keyCode,h=b==g.LEFT||b==g.UP,i=S.find("[id]."+l),j=h?"first":"last",k,n,o,p,q;if(i.length){k=i.filter(h?":first":":last"),o=r(k,h?"prev":"next");if(!o.length)n=k;else if(c||b==g.LEFT||b==g.RIGHT)n=o;else{p=k.position().top,q=k.position().left,n=k;if(h){do n=n.prev("[id]");while(n.length&&!(n.position().top<p&&n.position().left<=q));n.is("."+m)&&(n=r(n,"next"))}else{do n=n.next("[id]");while(n.length&&!(n.position().top>p&&n.position().left>=q));n.is("."+m)&&(n=r(n,"prev")),n.length||(o=S.find("[id]:not(."+m+"):last"),o.position().top>p&&(n=o))}}}else n=S.find("[id]:not(."+m+"):"+(h?"last":"first"));n&&n.length&&(d?n=k.add(k[h?"prevUntil":"nextUntil"]("#"+n.attr("id"))).add(n):i.trigger(f),n.trigger(e),F(n.filter(h?":first":":last")),E())},B=function(a){S.find("#"+a).trigger(e)},C=function(){S.find("[id]."+l).trigger(f)},D=function(){return a.map(S.find("[id]."+l),function(b){return b=a(b),b.is("."+m)?null:a(b).attr("id")})},E=function(){b.trigger("select",{selected:D()})},F=function(a){var b=a.position().top,c=a.outerHeight(!0),d=T.scrollTop(),e=T.innerHeight();b+c>d+e?T.scrollTop(parseInt(b+c-e)):b<d&&T.scrollTop(b)},G=[],H=function(a){var b=G.length;while(b--)if(G[b].hash==a)return b;return-1},I="scroll."+b.namespace,J=function(){var d=[],e=!1,f=[],g={},h=S.find("[id]:last"),i=!h.length,j=c?S.children("table").children("tbody"):S,k;if(!G.length)return T.unbind(I);while((!h.length||h.position().top<=T.height()+T.scrollTop()+b.options.showThreshold)&&(k=G.splice(0,b.options.showFiles)).length)d=a.map(k,function(a){return a.hash&&a.name?(a.mime=="directory"&&(e=!0),a.tmb&&(a.tmb===1?f.push(a.hash):g[a.hash]=a.tmb),y(a)):null}),j.append(d.join("")),h=S.find("[id]:last"),i&&S.scrollTop(0);M(g),f.length&&N(f),e&&L()},K=a.extend({},b.droppable,{over:function(c,d){var e=b.cwd().hash;a.each(d.helper.data("files"),function(a,c){if(b.file(c).phash==e)return S.removeClass(q),!1})}}),L=function(){setTimeout(function(){S.find(".directory:not(."+o+",.elfinder-na,.elfinder-ro)").droppable(b.droppable)},20)},M=function(c){var d=b.option("tmbUrl"),e=!0,f;return a.each(c,function(b,c){var g=S.find("#"+b);g.length?function(b,c){a("<img/>").load(function(){b.find(".elfinder-cwd-icon").css("background","url('"+c+"') center center no-repeat")}).attr("src",c)}(g,d+c):(e=!1,(f=H(b))!=-1&&(G[f].tmb=c))}),e},N=function(a){var c=[];if(b.oldAPI){b.request({data:{cmd:"tmb",current:b.cwd().hash},preventFail:!0}).done(function(a){M(a.images||[])&&a.tmb&&N()});return}c=c=a.splice(0,s),c.length&&b.request({data:{cmd:"tmb",targets:c},preventFail:!0}).done(function(b){M(b.images||[])&&N(a)})},O=function(a){var d=c?S.find("tbody"):S,e=a.length,f=[],g={},h=!1,i=function(a){var c=S.find("[id]:first"),d;while(c.length){d=b.file(c.attr("id"));if(d&&b.compare(a,d)<0)return c;c=c.next("[id]")}},j=function(a){var c=G.length,d;for(d=0;d<c;d++)if(b.compare(a,G[d])<0)return d;return c||-1},k,l,m,n;while(e--){k=a[e],l=k.hash;if(S.find("#"+l)
.length)continue;(m=i(k))&&m.length?m.before(y(k)):(n=j(k))>=0?G.splice(n,0,k):d.append(y(k)),S.find("#"+l).length&&(k.mime=="directory"?h=!0:k.tmb&&(k.tmb===1?f.push(l):g[l]=k.tmb))}M(g),f.length&&N(f),h&&L()},P=function(a){var c=a.length,d,e,f;while(c--){d=a[c];if((e=S.find("#"+d)).length)try{e.detach()}catch(g){b.debug("error",g)}else(f=H(d))!=-1&&G.splice(f,1)}},Q={name:b.i18n("name"),perm:b.i18n("perms"),mod:b.i18n("modify"),size:b.i18n("size"),kind:b.i18n("kind")},R=function(d,e){var f=b.cwd().hash;try{S.children("table,"+k).remove().end()}catch(g){S.html("")}S.removeClass("elfinder-cwd-view-icons elfinder-cwd-view-list").addClass("elfinder-cwd-view-"+(c?"list":"icons")),T[c?"addClass":"removeClass"]("elfinder-cwd-wrapper-list"),c&&S.html('<table><thead><tr class="ui-state-default"><td >'+Q.name+"</td><td>"+Q.perm+"</td><td>"+Q.mod+"</td><td>"+Q.size+"</td><td>"+Q.kind+"</td></tr></thead><tbody/></table>"),G=a.map(d,function(a){return e||a.phash==f?a:null}),G=b.sortFiles(G),T.bind(I,J).trigger(I),E()},S=a(this).addClass("ui-helper-clearfix elfinder-cwd").attr("unselectable","on").delegate(k,"click."+b.namespace,function(b){var c=this.id?a(this):a(this).parents("[id]:first"),d=c.prevAll("."+l+":first"),g=c.nextAll("."+l+":first"),h=d.length,i=g.length,j;b.stopImmediatePropagation(),b.shiftKey&&(h||i)?(j=h?c.prevUntil("#"+d.attr("id")):c.nextUntil("#"+g.attr("id")),j.add(c).trigger(e)):b.ctrlKey||b.metaKey?c.trigger(c.is("."+l)?f:e):(S.find("[id]."+l).trigger(f),c.trigger(e)),E()}).delegate(k,"dblclick."+b.namespace,function(a){b.dblclick({file:this.id})}).delegate(k,"mouseenter."+b.namespace,function(d){var e=a(this),f=c?e:e.children();!e.is("."+r)&&!f.is("."+n+",."+m)&&f.draggable(b.draggable)}).delegate(k,e,function(b){var c=a(this);!z&&!c.is("."+m)&&c.addClass(l).children().addClass(p)}).delegate(k,f,function(b){!z&&a(this).removeClass(l).children().removeClass(p)}).delegate(k,g,function(){var b=a(this).removeClass(l).addClass(m),d=(c?b:b.children()).removeClass(p);b.is("."+o)&&b.droppable("disable"),d.is("."+n)&&d.draggable("disable"),!c&&d.removeClass(m)}).delegate(k,h,function(){var b=a(this).removeClass(m),d=c?b:b.children();b.is("."+o)&&b.droppable("enable"),d.is("."+n)&&d.draggable("enable")}).delegate(k,"scrolltoview",function(){F(a(this))}).delegate(k,"hover",function(c){b.trigger("hover",{hash:a(this).attr("id"),type:c.type})}).bind("contextmenu."+b.namespace,function(c){var d=a(c.target).closest("."+j);d.length&&(c.stopPropagation(),c.preventDefault(),d.is("."+m)||(d.is("."+l)||(S.trigger("unselectall"),d.trigger(e),E()),b.trigger("contextmenu",{type:"files",targets:b.selected(),x:c.clientX,y:c.clientY})))}).selectable({filter:k,stop:E,selected:function(b,c){a(c.selected).trigger(e)},unselected:function(b,c){a(c.unselected).trigger(f)}}).droppable(K).bind("create."+b.namespace,function(b,d){var e=c?S.find("tbody"):S;S.trigger("unselectall"),e.prepend(a(y(d)).addClass(r)),S.scrollTop(0)}).bind("unselectall",function(){S.find("[id]."+l+"").trigger(f),E()}).bind("selectfile",function(a,b){S.find("#"+b).trigger(e),E()}),T=a('<div class="elfinder-cwd-wrapper"/>').bind("contextmenu",function(a){a.preventDefault(),b.trigger("contextmenu",{type:"cwd",targets:[b.cwd().hash],x:a.clientX,y:a.clientY})}),U=function(){var b=0;T.siblings(".elfinder-panel:visible").each(function(){b+=a(this).outerHeight(!0)}),T.height(W.height()-b)},V=a(this).parent().resize(U),W=V.children(".elfinder-workzone").append(T.append(this));b.dragUpload&&(T[0].addEventListener("dragenter",function(a){a.preventDefault(),a.stopPropagation(),T.addClass(q)},!1),T[0].addEventListener("dragleave",function(a){a.preventDefault(),a.stopPropagation(),a.target==S[0]&&T.removeClass(q)},!1),T[0].addEventListener("dragover",function(a){a.preventDefault(),a.stopPropagation()},!1),T[0].addEventListener("drop",function(a){a.preventDefault(),T.removeClass(q),a.dataTransfer&&a.dataTransfer.files&&a.dataTransfer.files.length&&b.exec("upload",{files:a.dataTransfer.files})},!1)),b.bind("open search",function(a){R(a.data.files,a.type=="search")}).bind("searchend sortchange",function(){t&&R(b.files())}).bind("searchstart",function(a){t=a.data.query}).bind("searchend",function(){t=""}).bind("viewchange",function(){var d=b.selected(),e=b.storage("view")=="list";e!=c&&(c=e,R(b.files()),a.each(d,function(a,b){B(b)}),E()),U()}).add(function(c){var d=b.cwd().hash,e=t?a.map(c.data.added||[],function(a){return a.name.indexOf(t)===-1?null:a}):a.map(c.data.added||[],function(a){return a.phash==d?a:null});O(e)}).change(function(c){var d=b.cwd().hash,e=b.selected(),f;t?a.each(c.data.changed||[],function(b,c){P([c.hash]),c.name.indexOf(t)!==-1&&(O([c]),a.inArray(c.hash,e)!==-1&&B(c.hash))}):a.each(a.map(c.data.changed||[],function(a){return a.phash==d?a:null}),function(b,c){P([c.hash]),O([c]),a.inArray(c.hash,e)!==-1&&B(c.hash)}),E()}).remove(function(a){P(a.data.removed||[]),E()}).bind("open add search searchend",function(){S.css("height","auto"),S.outerHeight(!0)<T.height()&&S.height(T.height()-(S.outerHeight(!0)-S.height())-2)}).dragstart(function(b){var c=a(b.data.target),d=b.data.originalEvent;c.is(k)&&(c.is("."+l)||(!(d.ctrlKey||d.metaKey||d.shiftKey)&&C(),c.trigger(e),E()),S.droppable("disable")),S.selectable("disable").removeClass(m),z=!0}).dragstop(function(){S.selectable("enable"),z=!1}).bind("lockfiles unlockfiles",function(a){var b=a.type=="lockfiles"?g:h,c=a.data.files||[],d=c.length;while(d--)S.find("#"+c[d]).trigger(b);E()}).bind("mkdir mkfile duplicate upload rename archive extract",function(c){var d=b.cwd().hash,e;S.trigger("unselectall"),a.each(c.data.added||[],function(a,b){b&&b.phash==d&&B(b.hash)}),E()}).shortcut({pattern:"ctrl+a",description:"selectall",callback:function(){var c=[],d;S.find("[id]:not(."+l+")").trigger(e),G.length?(d=b.cwd().hash,b.select({selected:a.map(b.files(),function(a){return a.phash==d?a.hash:null})})):E()}}).shortcut({pattern:"left right up down shift+left shift+right shift+up shift+down",description:"selectfiles",type:"keydown",callback:function(a){A(a.keyCode,a.shiftKey)}}).shortcut({pattern:"home",description:"selectffile",callback:function(a){C(),F(S.find("[id]:first").trigger(e)),E()}}).shortcut({pattern:"end",description:"selectlfile",callback:function(a){C(),F(S.find("[id]:last").trigger(e)),E()}})}),this},a.fn.elfinderdialog=function(b){var c;return typeof b=="string"&&(c=this.closest(".ui-dialog")).length&&(b=="open"&&c.is(":hidden")?c.fadeIn(120,function(){c.trigger("open")}):b=="close"&&c.is(":visible")?c.hide().trigger("close"):b=="destroy"?c.hide().remove():b=="toTop"&&c.trigger("totop")),b=a.extend({},a.fn.elfinderdialog.defaults,b),this.filter(":not(.ui-dialog-content)").each(function(){var c=a(this).addClass("ui-dialog-content ui-widget-content"),d=c.parent(),e="elfinder-dialog-active",f="elfinder-dialog",g="elfinder-dialog-notify",h="ui-state-hover",i=parseInt(Math.random()*1e6),j=d.children(".elfinder-overlay"),k=a('<div class="ui-dialog-buttonset"/>'),l=a('<div class=" ui-helper-clearfix ui-dialog-buttonpane ui-widget-content"/>').append(k),m=a('<div class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-draggable std42-dialog  '+f+" "+b.cssClass+'"/>').hide().append(c).appendTo(d).draggable({handle:".ui-dialog-titlebar",containment:a("body")}).css({width:b.width,height:b.height}).mousedown(function(b){b.stopPropagation(),a(document).mousedown(),m.is("."+e)||(d.find("."+f+":visible").removeClass(e),m.addClass(e).zIndex(n()+1))}).bind("open",function(){b.modal&&j.elfinderoverlay("show"),m.trigger("totop"),typeof b.open=="function"&&a.proxy(b.open,c[0])(),m.is("."+g)||d.find("."+f+":visible").not("."+g).each(function(){var b=a(this),c=parseInt(b.css("top")),d=parseInt(b.css("left")),e=parseInt(m.css("top")),f=parseInt(m.css("left"));b[0]!=m[0]&&(c==e||d==f)&&m.css({top:c+10+"px",left:d+10+"px"})})}).bind("close",function(){var e=d.find(".elfinder-dialog:visible"),f=n();b.modal&&j.elfinderoverlay("hide"),e.length?e.each(function(){var b=a(this);if(b.zIndex()>=f)return b.trigger("totop"),!1}):setTimeout(function(){d.mousedown().click()},10),typeof b.close=="function"?a.proxy(b.close,c[0])():b.destroyOnClose&&m.hide().remove()
}).bind("totop",function(){a(this).mousedown().find(".ui-button:first").focus().end().find(":text:first").focus()}),n=function(){var b=d.zIndex()+10;return d.find("."+f+":visible").each(function(){var c;this!=m[0]&&(c=a(this).zIndex(),c>b&&(b=c))}),b},o;b.position||(o=parseInt((d.height()-m.outerHeight())/2-42),b.position={top:(o>0?o:0)+"px",left:parseInt((d.width()-m.outerWidth())/2)+"px"}),m.css(b.position),b.closeOnEscape&&a(document).bind("keyup."+i,function(b){b.keyCode==a.ui.keyCode.ESCAPE&&m.is("."+e)&&(c.elfinderdialog("close"),a(document).unbind("keyup."+i))}),m.prepend(a('<div class="ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix">'+b.title+"</div>").prepend(a('<a href="#" class="ui-dialog-titlebar-close ui-corner-all"><span class="ui-icon ui-icon-closethick"/></a>').mousedown(function(a){a.preventDefault(),c.elfinderdialog("close")}))),a.each(b.buttons,function(b,d){var e=a('<button type="button" class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only"><span class="ui-button-text">'+b+"</span></button>").click(a.proxy(d,c[0])).hover(function(b){a(this)[b.type=="mouseenter"?"focus":"blur"]()}).focus(function(){a(this).addClass(h)}).blur(function(){a(this).removeClass(h)}).keydown(function(b){var c;b.keyCode==a.ui.keyCode.ENTER?a(this).click():b.keyCode==a.ui.keyCode.TAB&&(c=a(this).next(".ui-button"),c.length?c.focus():a(this).parent().children(".ui-button:first").focus())});k.append(e)}),k.children().length&&m.append(l),b.resizable&&a.fn.resizable&&m.resizable({minWidth:b.minWidth,minHeight:b.minHeight,alsoResize:this}),typeof b.create=="function"&&a.proxy(b.create,this)(),b.autoOpen&&c.elfinderdialog("open")}),this},a.fn.elfinderdialog.defaults={cssClass:"",title:"",modal:!1,resizable:!0,autoOpen:!0,closeOnEscape:!0,destroyOnClose:!1,buttons:{},position:null,width:320,height:"auto",minWidth:200,minHeight:110},a.fn.elfindernavbar=function(b,c){return this.not(".elfinder-navbar").each(function(){var d=a(this).addClass("ui-state-default elfinder-navbar"),e=d.parent().resize(function(){d.height(f.height()-g)}),f=e.children(".elfinder-workzone").append(d),g=d.outerHeight()-d.height(),h=b.direction=="ltr",i;a.fn.resizable&&(i=d.resizable({handles:h?"e":"w",minWidth:c.minWidth||150,maxWidth:c.maxWidth||500}).bind("resize scroll",function(){i.css({top:parseInt(d.scrollTop())+"px",left:parseInt(h?d.width()+d.scrollLeft()-i.width()-2:d.scrollLeft()+2)})}).find(".ui-resizable-handle").zIndex(d.zIndex()+10),h||d.resize(function(){d.css("left",null).css("right",0)}),b.one("open",function(){setTimeout(function(){d.trigger("resize")},150)}))}),this},a.fn.elfinderoverlay=function(b){this.filter(":not(.elfinder-overlay)").each(function(){b=a.extend({},b),a(this).addClass("ui-widget-overlay elfinder-overlay").hide().mousedown(function(a){a.preventDefault(),a.stopPropagation()}).data({cnt:0,show:typeof b.show=="function"?b.show:function(){},hide:typeof b.hide=="function"?b.hide:function(){}})});if(b=="show"){var c=this.eq(0),d=c.data("cnt")+1,e=c.data("show");c.data("cnt",d),c.is(":hidden")&&(c.zIndex(c.parent().zIndex()+1),c.show(),e())}if(b=="hide"){var c=this.eq(0),d=c.data("cnt")-1,f=c.data("hide");c.data("cnt",d),d==0&&c.is(":visible")&&(c.hide(),f())}return this},a.fn.elfinderpanel=function(b){return this.each(function(){var c=a(this).addClass("elfinder-panel ui-state-default ui-corner-all"),d="margin-"+(b.direction=="ltr"?"left":"right");b.one("load",function(a){var e=b.getUI("navbar");c.css(d,parseInt(e.outerWidth(!0))),e.bind("resize",function(){c.is(":visible")&&c.css(d,parseInt(e.outerWidth(!0)))})})})},a.fn.elfinderpath=function(b){return this.each(function(){var c=a(this).addClass("elfinder-path").html("&nbsp;").delegate("a","click",function(c){var d=a(this).attr("href").substr(1);c.preventDefault(),d!=b.cwd().hash&&b.exec("open",d)}).prependTo(b.getUI("statusbar").show());b.bind("open searchend",function(){var d=[];a.each(b.parents(b.cwd().hash),function(a,c){d.push('<a href="#'+c+'">'+b.escape(b.file(c).name)+"</a>")}),c.html(d.join(b.option("separator")))}).bind("search",function(){c.html(b.i18n("searcresult"))})})},a.fn.elfinderplaces=function(b,c){return this.each(function(){var d=[],e="class",f=b.res(e,"navdir"),g=b.res(e,"navcollapse"),h=b.res(e,"navexpand"),i=b.res(e,"hover"),j=b.res(e,"treeroot"),k=b.res("tpl","navdir"),l=b.res("tpl","perms"),m=a(b.res("tpl","navspinner")),n=function(a){return a.substr(6)},o=function(a){return"place-"+a},p=function(){b.storage("places",d.join(","))},q=function(c){return a(k.replace(/\{id\}/,o(c.hash)).replace(/\{name\}/,b.escape(c.name)).replace(/\{cssclass\}/,b.perms2class(c)).replace(/\{permissions\}/,!c.read||!c.write?l:"").replace(/\{symlink\}/,""))},r=function(c){var e=q(c);w.children().length&&a.each(w.children(),function(){var b=a(this);if(c.name.localeCompare(b.children("."+f).text())<0)return!e.insertBefore(b)}),d.push(c.hash),!e.parent().length&&w.append(e),v.addClass(g),e.draggable({appendTo:"body",revert:!1,helper:function(){var c=a(this);return c.children().removeClass("ui-state-hover"),a('<div class="elfinder-place-drag elfinder-'+b.direction+'"/>').append(c.clone()).data("hash",n(c.children(":first").attr("id")))},start:function(){a(this).hide()},stop:function(b,c){var d=x.offset().top,e=x.offset().left,f=x.width(),g=x.height(),h=b.clientX,i=b.clientY;h>e&&h<e+f&&i>d&&i<i+g?a(this).show():(s(c.helper.data("hash")),p())}})},s=function(b){var c=a.inArray(b,d);c!==-1&&(d.splice(c,1),w.find("#"+o(b)).parent().remove(),!w.children().length&&v.removeClass(g+" "+h))},t=function(){w.empty(),v.removeClass(g+" "+h)},u=q({hash:"root-"+b.namespace,name:b.i18n(c.name,"places"),read:!0,write:!0}),v=u.children("."+f).addClass(j).click(function(){v.is("."+g)&&(x.toggleClass(h),w.slideToggle(),b.storage("placesState",x.is("."+h)?1:0))}),w=u.children("."+b.res(e,"navsubtree")),x=a(this).addClass(b.res(e,"tree")+" elfinder-places ui-corner-all").hide().append(u).appendTo(b.getUI("navbar")).delegate("."+f,"hover",function(){a(this).toggleClass("ui-state-hover")}).delegate("."+f,"click",function(c){b.exec("open",a(this).attr("id").substr(6))}).delegate("."+f+":not(."+j+")","contextmenu",function(c){var d=a(this).attr("id").substr(6);c.preventDefault(),b.trigger("contextmenu",{raw:[{label:b.i18n("rmFromPlaces"),icon:"rm",callback:function(){s(d),p()}}],x:c.clientX,y:c.clientY})}).droppable({tolerance:"pointer",accept:".elfinder-cwd-file-wrapper,.elfinder-tree-dir,.elfinder-cwd-file",hoverClass:b.res("class","adroppable"),drop:function(c,e){var f=!0;a.each(e.helper.data("files"),function(c,e){var g=b.file(e);g&&g.mime=="directory"&&a.inArray(g.hash,d)===-1?r(g):f=!1}),p(),f&&e.helper.hide()}});b.one("load",function(){if(b.oldAPI)return;x.show().parent().show(),d=a.map(b.storage("places").split(","),function(a){return a||null}),d.length&&(v.prepend(m),b.request({data:{cmd:"info",targets:d},preventDefault:!0}).done(function(c){d=[],a.each(c.files,function(a,b){b.mime=="directory"&&r(b)}),p(),b.storage("placesState")>0&&v.click()}).always(function(){m.remove()})),b.remove(function(b){a.each(b.data.removed,function(a,b){s(b)}),p()}).change(function(b){a.each(b.data.changed,function(b,c){a.inArray(c.hash,d)!==-1&&(s(c.hash),c.mime=="directory"&&r(c))}),p()}).bind("sync",function(){d.length&&(v.prepend(m),b.request({data:{cmd:"info",targets:d},preventDefault:!0}).done(function(b){a.each(b.files||[],function(b,c){a.inArray(c.hash,d)===-1&&s(c.hash)}),p()}).always(function(){m.remove()}))})})})},a.fn.elfindersearchbutton=function(b){return this.each(function(){var c=!1,d=a(this).hide().addClass("ui-widget-content elfinder-button "+b.fm.res("class","searchbtn")+""),e=function(){b.exec(a.trim(g.val())).done(function(){c=!0,g.focus()})},f=function(){g.val(""),c&&(c=!1,b.fm.trigger("searchend"))},g=a('<input type="text" size="42"/>').appendTo(d).keypress(function(a){a.stopPropagation()}).keydown(function(a){a.stopPropagation(),a.keyCode==13&&e(),a.keyCode==27&&(a.preventDefault(),f())});a('<span class="ui-icon ui-icon-search" title="'+b.title+'"/>').appendTo(d).click(e),a('<span class="ui-icon ui-icon-close"/>').appendTo(d).click(f),setTimeout(function(){d.parent().
detach(),b.fm.getUI("toolbar").prepend(d.show());if(a.browser.msie){var c=d.children(b.fm.direction=="ltr"?".ui-icon-close":".ui-icon-search");c.css({right:"",left:parseInt(d.width())-c.outerWidth(!0)})}},200),b.fm.error(function(){g.unbind("keydown")}).select(function(){g.blur()}).bind("searchend",function(){g.val("")}).viewchange(f).shortcut({pattern:"ctrl+f f3",description:b.title,callback:function(){g.select().focus()}})})},a.fn.elfindersortbutton=function(b){return this.each(function(){var c="class",d=b.fm,e=d.res(c,"disabled"),f=d.res(c,"active"),g=d.res(c,"hover"),h="elfinder-button-menu-item",i="elfinder-button-menu-item-selected",j,k=a(this).addClass("ui-state-default elfinder-button elfiner-button-"+b.name).attr("title",b.title).append('<span class="elfinder-button-icon elfinder-button-icon-'+b.name+'"/>').hover(function(a){!k.is("."+e)&&k.toggleClass(g)}).click(function(a){k.is("."+e)||(j&&b.variants.length>1?(j.is(":hidden")&&b.fm.getUI().click(),a.stopPropagation(),j.slideToggle(100)):b.exec())}),l=function(){j.hide()};a.isArray(b.variants)&&(k.addClass("elfinder-menubutton"),j=a('<div class="ui-widget ui-widget-content elfinder-button-menu ui-corner-all"/>').hide().appendTo(k).zIndex(10+k.zIndex()).delegate("."+h,"hover",function(){a(this).toggleClass(g)}).delegate("."+h,"click",function(c){c.preventDefault(),c.stopPropagation(),k.removeClass(g),b.exec(b.fm.selected(),a(this).data("value"))}),b.fm.bind("disable select",l).getUI().click(l),b.change(function(){j.html(""),a.each(b.variants,function(c,d){j.append(a('<div class="'+h+" "+(d[0]==b.value?i:"")+" elfinder-menu-item-sort-"+b.fm.sortDirect+'"><span class="elfinder-menu-item-sort-dir"/>'+d[1]+"</div>").data("value",d[0]))})})),b.change(function(){b.disabled()?k.removeClass(f+" "+g).addClass(e):(k.removeClass(e),k[b.active()?"addClass":"removeClass"](f))}).change()})},a.fn.elfinderstat=function(b){return this.each(function(){var c=a(this).addClass("elfinder-stat-size"),d=a('<div class="elfinder-stat-selected"/>'),e=b.i18n("size").toLowerCase(),f=b.i18n("items").toLowerCase(),g=b.i18n("selected"),h=function(d,g){var h=0,i=0;a.each(d,function(a,b){if(!g||b.phash==g)h++,i+=parseInt(b.size)||0}),c.html(f+": "+h+", "+e+": "+b.formatSize(i))};b.getUI("statusbar").prepend(c).append(d).show(),b.bind("open reload add remove change searchend",function(){h(b.files(),b.cwd().hash)}).search(function(a){h(a.data.files)}).select(function(){var c=0,f=0,h=b.selectedFiles();if(h.length==1){c=h[0].size,d.html(b.escape(h[0].name)+(c>0?", "+b.formatSize(c):""));return}a.each(h,function(a,b){f++,c+=parseInt(b.size)||0}),d.html(f?g+": "+f+", "+e+": "+b.formatSize(c):"&nbsp;")})})},a.fn.elfindertoolbar=function(b,c){return this.not(".elfinder-toolbar").each(function(){var d=b._commands,e=a(this).addClass("ui-helper-clearfix ui-widget-header ui-corner-top elfinder-toolbar"),f=c||[],g=f.length,h,i,j,k;e.prev().length&&e.parent().prepend(this);while(g--)if(f[g]){j=a('<div class="ui-widget-content ui-corner-all elfinder-buttonset"/>'),h=f[g].length;while(h--)if(i=d[f[g][h]])k="elfinder"+i.options.ui,a.fn[k]&&j.prepend(a("<div/>")[k](i));j.children().length&&e.prepend(j),j.children(":not(:last),:not(:first):not(:last)").after('<span class="ui-widget-content elfinder-toolbar-button-separator"/>')}e.children().length&&e.show()}),this},a.fn.elfindertree=function(b,c){var d=b.res("class","tree");return this.not("."+d).each(function(){var e="class",f=b.res(e,"treeroot"),g=c.openRootOnLoad,h=b.res(e,"navsubtree"),i=b.res(e,"treedir"),j=b.res(e,"navcollapse"),k=b.res(e,"navexpand"),l="elfinder-subtree-loaded",m=b.res(e,"navarrow"),n=b.res(e,"active"),o=b.res(e,"adroppable"),p=b.res(e,"hover"),q=b.res(e,"disabled"),r=b.res(e,"draggable"),s=b.res(e,"droppable"),t=a.extend({},b.droppable,{hoverClass:p+" "+o,over:function(){var b=a(this);b.is("."+j+":not(."+k+")")&&setTimeout(function(){b.is("."+o)&&b.children("."+m).click()},500)}}),u=a(b.res("tpl","navspinner")),v=b.res("tpl","navdir"),w=b.res("tpl","perms"),x=b.res("tpl","symlink"),y={id:function(a){return b.navHash2Id(a.hash)},cssclass:function(a){return(a.phash?"":f)+" "+i+" "+b.perms2class(a)+" "+(a.dirs&&!a.link?j:"")},permissions:function(a){return!a.read||!a.write?w:""},symlink:function(a){return a.alias?x:""}},z=function(a){return a.name=b.escape(a.name),v.replace(/(?:\{([a-z]+)\})/ig,function(b,c){return a[c]||(y[c]?y[c](a):"")})},A=function(b){return a.map(b||[],function(a){return a.mime=="directory"?a:null})},B=function(a){return a?H.find("#"+b.navHash2Id(a)).next("."+h):H},C=function(c,d){var e=c.children(":first"),f;while(e.length){if((f=b.file(b.navId2Hash(e.children("[id]").attr("id"))))&&d.name.localeCompare(f.name)<0)return e;e=e.next()}return a("")},D=function(a){var c=a.length,d=[],e,f,g,h,i;for(e=0;e<c;e++){f=a[e];if(H.find("#"+b.navHash2Id(f.hash)).length)continue;(h=B(f.phash)).length?(g=z(f),f.phash&&(i=C(h,f)).length?i.before(g):h.append(g)):d.push(f)}if(d.length&&d.length<c)return D(d);F()},E=function(){var a=b.cwd().hash,d=H.find("#"+b.navHash2Id(a)),e;g&&(e=H.find("#"+b.navHash2Id(b.root())),e.is("."+l)&&e.addClass(k).next("."+h).show(),g=!1),d.is("."+n)||(H.find("."+i+"."+n).removeClass(n),d.addClass(n)),c.syncTree&&(d.length?d.parentsUntil("."+f).filter("."+h).show().prev("."+i).addClass(k):b.newAPI&&b.request({data:{cmd:"parents",target:a},preventFail:!0}).done(function(c){var d=A(c.tree);D(d),G(d,l),a==b.cwd().hash&&E()}))},F=function(){H.find("."+i+":not(."+s+",.elfinder-ro,.elfinder-na)").droppable(t)},G=function(c,d){var e=d==l?"."+j+":not(."+l+")":":not(."+j+")";a.each(c,function(c,f){H.find("#"+b.navHash2Id(f.phash)+e).filter(function(){return a(this).next("."+h).children().length>0}).addClass(d)})},H=a(this).addClass(d).delegate("."+i,"hover",function(c){var d=a(this),e=c.type=="mouseenter";d.is("."+o+" ,."+q)||(e&&!d.is("."+f+",."+r+",.elfinder-na,.elfinder-wo")&&d.draggable(b.draggable),d.toggleClass(p,e))}).delegate("."+i,"dropover dropout drop",function(b){a(this)[b.type=="dropover"?"addClass":"removeClass"](o+" "+p)}).delegate("."+i,"click",function(c){var d=a(this),e=b.navId2Hash(d.attr("id")),f=b.file(e);b.trigger("searchend"),e!=b.cwd().hash&&!d.is("."+q)?b.exec("open",f.thash||e):d.is("."+j)&&d.children("."+m).click()}).delegate("."+i+"."+j+" ."+m,"click",function(c){var d=a(this),e=d.parent("."+i),f=e.next("."+h);c.stopPropagation(),e.is("."+l)?(e.toggleClass(k),f.slideToggle()):(u.insertBefore(d),e.removeClass(j),b.request({cmd:"tree",target:b.navId2Hash(e.attr("id"))}).done(function(a){D(A(a.tree)),f.children().length&&(e.addClass(j+" "+k),f.slideDown()),E()}).always(function(a){u.remove(),e.addClass(l)}))}).delegate("."+i,"contextmenu",function(c){c.preventDefault(),b.trigger("contextmenu",{type:"navbar",targets:[b.navId2Hash(a(this).attr("id"))],x:c.clientX,y:c.clientY})});H.parent().find(".elfinder-navbar").append(H).show(),b.open(function(a){var b=a.data,c=A(b.files);b.init&&H.empty(),c.length&&(D(c),G(c,l)),E()}).add(function(a){var b=A(a.data.added);b.length&&(D(b),G(b,j))}).change(function(c){var d=A(c.data.changed),e=d.length,f,g,j,m,n,o,p,q,r;while(e--){f=d[e];if((g=H.find("#"+b.navHash2Id(f.hash))).length){if(f.phash){m=g.closest("."+h),n=B(f.phash),o=g.parent().next(),p=C(n,f);if(!n.length)continue;if(n[0]!==m[0]||o.get(0)!==p.get(0))p.length?p.before(g):n.append(g)}q=g.is("."+k),r=g.is("."+l),j=a(z(f)),g.replaceWith(j.children("."+i)),f.dirs&&(q||r)&&(g=H.find("#"+b.navHash2Id(f.hash)))&&g.next("."+h).children().length&&(q&&g.addClass(k),r&&g.addClass(l))}}E(),F()}).remove(function(a){var c=a.data.removed,d=c.length,e,f;while(d--)(e=H.find("#"+b.navHash2Id(c[d]))).length&&(f=e.closest("."+h),e.parent().detach(),f.children().length||f.hide().prev("."+i).removeClass(j+" "+k+" "+l))}).bind("search searchend",function(a){H.find("#"+b.navHash2Id(b.cwd().hash))[a.type=="search"?"removeClass":"addClass"](n)}).bind("lockfiles unlockfiles",function(c){var d=c.type=="lockfiles",e=d?"disable":"enable",f=a.map(c.data.files||[],function(a){var c=b.file(a);return c&&c.mime=="directory"?a:null});a.each(f,function(a,c){var f=H.find("#"+b.navHash2Id(c));f.length&&(f.is("."+r)&&f.draggable(e),f.is("."+s)&&f.droppable
(n),f[d?"addClass":"removeClass"](q))})})}),this},a.fn.elfinderuploadbutton=function(b){return this.each(function(){var c=a(this).elfinderbutton(b).unbind("click"),d=a("<form/>").appendTo(c),e=a('<input type="file" multiple="true"/>').change(function(){var c=a(this);c.val()&&(b.exec({input:c.remove()[0]}),e.clone(!0).appendTo(d))});d.append(e.clone(!0)),b.change(function(){d[b.disabled()?"hide":"show"]()}).change()})},a.fn.elfinderviewbutton=function(b){return this.each(function(){var c=a(this).elfinderbutton(b),d=c.children(".elfinder-button-icon");b.change(function(){var a=b.value=="icons";d.toggleClass("elfinder-button-icon-view-list",a),c.attr("title",b.fm.i18n(a?"viewlist":"viewicons"))})})},a.fn.elfinderworkzone=function(b){var c="elfinder-workzone";return this.not("."+c).each(function(){var b=a(this).addClass(c),d=b.outerHeight(!0)-b.height(),e=b.parent();e.add(window).bind("resize",function(){var f=e.height();e.children(":visible:not(."+c+")").each(function(){var b=a(this);b.css("position")!="absolute"&&(f-=b.outerHeight(!0))}),b.height(f-d)})}),this},elFinder.prototype.commands.archive=function(){var b=this,c=b.fm,d=[];this.variants=[],this.disableOnSearch=!0,c.bind("open reload",function(){b.variants=[],a.each(d=c.option("archivers").create||[],function(a,d){b.variants.push([d,c.mime2kind(d)])}),b.change()}),this.getstate=function(){return!this._disabled&&d.length&&c.selected().length&&c.cwd().write?0:-1},this.exec=function(b,e){var f=this.files(b),g=f.length,h=e||d[0],i=c.cwd(),j=["errArchive","errPerm"],k=a.Deferred().fail(function(a){a&&c.error(a)}),l;if(!(this.enabled()&&g&&d.length&&a.inArray(h,d)!==-1))return k.reject();if(!i.write)return k.reject(j);for(l=0;l<g;l++)if(!f[l].read)return k.reject(j);return c.request({data:{cmd:"archive",targets:this.hashes(b),type:h},notify:{type:"archive",cnt:1},syncOnFail:!0})}},elFinder.prototype.commands.back=function(){this.alwaysEnabled=!0,this.updateOnSelect=!1,this.shortcuts=[{pattern:"ctrl+left backspace"}],this.getstate=function(){return this.fm.history.canBack()?0:-1},this.exec=function(){return this.fm.history.back()}},elFinder.prototype.commands.copy=function(){this.shortcuts=[{pattern:"ctrl+c ctrl+insert"}],this.getstate=function(b){var b=this.files(b),c=b.length;return c&&a.map(b,function(a){return a.phash&&a.read?a:null}).length==c?0:-1},this.exec=function(b){var c=this.fm,d=a.Deferred().fail(function(a){c.error(a)});return a.each(this.files(b),function(a,b){if(!b.read||!b.phash)return!d.reject(["errCopy",b.name,"errPerm"])}),d.isRejected()?d:d.resolve(c.clipboard(this.hashes(b)))}},elFinder.prototype.commands.cut=function(){this.shortcuts=[{pattern:"ctrl+x shift+insert"}],this.getstate=function(b){var b=this.files(b),c=b.length;return c&&a.map(b,function(a){return a.phash&&a.read&&!a.locked?a:null}).length==c?0:-1},this.exec=function(b){var c=this.fm,d=a.Deferred().fail(function(a){c.error(a)});return a.each(this.files(b),function(a,b){if(!b.read||!b.phash)return!d.reject(["errCopy",b.name,"errPerm"]);if(b.locked)return!d.reject(["errLocked",b.name])}),d.isRejected()?d:d.resolve(c.clipboard(this.hashes(b),!0))}},elFinder.prototype.commands.download=function(){var b=this,c=this.fm,d=function(c){return a.map(b.files(c),function(a){return a.mime=="directory"?null:a})};this.shortcuts=[{pattern:"shift+enter"}],this.getstate=function(){var b=this.fm.selected(),c=b.length;return!this._disabled&&c&&(!a.browser.msie||c==1)&&c==d(b).length?0:-1},this.exec=function(b){var c=this.fm,e=c.options.url,f=d(b),g=a.Deferred(),h="",i="",j,k;if(this.disabled())return g.reject();if(c.oldAPI)return c.error("errCmdNoSupport"),g.reject();a.each(c.options.customData||{},function(a,b){i+="&"+a+"="+b}),e+=e.indexOf("?")===-1?"?":"&";for(j=0;j<f.length;j++)h+='<iframe class="downloader" id="downloader-'+f[j].hash+'" style="display:none" src="'+e+"cmd=file&target="+f[j].hash+"&download=1"+i+'"/>';return a(h).appendTo("body").ready(function(){setTimeout(function(){a(h).each(function(){a("#"+a(this).attr("id")).remove()})},a.browser.mozilla?2e4+1e4*j:1e3)}),c.trigger("download",{files:f}),g.resolve(b)}},elFinder.prototype.commands.duplicate=function(){var b=this.fm;this.getstate=function(c){var c=this.files(c),d=c.length;return!this._disabled&&d&&b.cwd().write&&a.map(c,function(a){return a.phash&&a.read?a:null}).length==d?0:-1},this.exec=function(b){var c=this.fm,d=this.files(b),e=d.length,f=a.Deferred().fail(function(a){a&&c.error(a)}),g=[];return!e||this._disabled?f.reject():(a.each(d,function(a,b){if(!b.read||!c.file(b.phash).write)return!f.reject(["errCopy",b.name,"errPerm"])}),f.isRejected()?f:c.request({data:{cmd:"duplicate",targets:this.hashes(b)},notify:{type:"copy",cnt:e}}))}},elFinder.prototype.commands.edit=function(){var b=this,c=this.fm,d=c.res("mimes","text")||[],e=function(c){return a.map(c,function(c){return(c.mime.indexOf("text/")===0||a.inArray(c.mime,d)!==-1)&&c.mime.indexOf("text/rtf")&&(!b.onlyMimes.length||a.inArray(c.mime,b.onlyMimes)!==-1)&&c.read&&c.write?c:null})},f=function(d,e,f){var g=a.Deferred(),h=a('<textarea class="elfinder-file-edit" rows="20" id="'+d+'-ta">'+c.escape(f)+"</textarea>"),i=function(){h.editor&&h.editor.save(h[0],h.editor.instance),g.resolve(h.getContent()),h.elfinderdialog("close")},j=function(){g.reject(),h.elfinderdialog("close")},k={title:e.name,width:b.options.dialogWidth||450,buttons:{},close:function(){h.editor&&h.editor.close(h[0],h.editor.instance),a(this).elfinderdialog("destroy")},open:function(){c.disable(),h.focus(),h[0].setSelectionRange&&h[0].setSelectionRange(0,0),h.editor&&h.editor.load(h[0])}};return h.getContent=function(){return h.val()},a.each(b.options.editors||[],function(b,c){if(a.inArray(e.mime,c.mimes||[])!==-1&&typeof c.load=="function"&&typeof c.save=="function")return h.editor={load:c.load,save:c.save,close:typeof c.close=="function"?c.close:function(){},instance:null},!1}),h.editor||h.keydown(function(a){var b=a.keyCode,c,d;a.stopPropagation(),b==9&&(a.preventDefault(),this.setSelectionRange&&(c=this.value,d=this.selectionStart,this.value=c.substr(0,d)+"	"+c.substr(this.selectionEnd),d+=1,this.setSelectionRange(d,d)));if(a.ctrlKey||a.metaKey){if(b==81||b==87)a.preventDefault(),j();b==83&&(a.preventDefault(),i())}}),k.buttons[c.i18n("Save")]=i,k.buttons[c.i18n("Cancel")]=j,c.dialog(h,k).attr("id",d),g.promise()},g=function(b){var d=b.hash,e=c.options,g=a.Deferred(),h={cmd:"file",target:d},i=c.url(d)||c.options.url,j="edit-"+c.namespace+"-"+b.hash,k=c.getUI().find("#"+j),l;return k.length?(k.elfinderdialog("toTop"),g.resolve()):!b.read||!b.write?(l=["errOpen",b.name,"errPerm"],c.error(l),g.reject(l)):(c.request({data:{cmd:"get",target:d},notify:{type:"openfile",cnt:1},syncOnFail:!0}).done(function(a){f(j,b,a.content).done(function(a){c.request({options:{type:"post"},data:{cmd:"put",target:d,content:a},notify:{type:"save",cnt:1},syncOnFail:!0}).fail(function(a){g.reject(a)}).done(function(a){a.changed&&a.changed.length&&c.change(a),g.resolve(a)})})}).fail(function(a){g.reject(a)}),g.promise())};this.shortcuts=[{pattern:"ctrl+e"}],this.init=function(){this.onlyMimes=this.options.mimes||[]},this.getstate=function(a){var a=this.files(a),b=a.length;return!this._disabled&&b&&e(a).length==b?0:-1},this.exec=function(b){var c=e(this.files(b)),d=[],f;if(this.disabled())return a.Deferred().reject();while(f=c.shift())d.push(g(f));return d.length?a.when.apply(null,d):a.Deferred().reject()}},elFinder.prototype.commands.extract=function(){var b=this,c=b.fm,d=[],e=function(b){return a.map(b,function(b){return b.read&&a.inArray(b.mime,d)!==-1?b:null})};this.disableOnSearch=!0,c.bind("open reload",function(){d=c.option("archivers").extract||[],b.change()}),this.getstate=function(a){var a=this.files(a),b=a.length;return!this._disabled&&b&&e(a).length==b?0:-1},this.exec=function(b){var e=this.files(b),f=a.Deferred(),g=e.length,h=g,i,j,k;if(!(this.enabled()&&g&&d.length))return f.reject();for(i=0;i<g;i++){j=e[i];if(!j.read||!c.file(j.phash).write)return k=["errExtract",j.name,"errPerm"],c.error(k),f.reject(k);if(a.inArray(j.mime,d)===-1)return k=["errExtract",j.name,"errNoArchive"],c.error(k),f.reject(k);c.request({data:{cmd:"extract",target:j.hash}
,notify:{type:"extract",cnt:1},syncOnFail:!0}).fail(function(a){f.isRejected()||f.reject(a)}).done(function(){h--,h==0&&f.resolve()})}return f}},elFinder.prototype.commands.forward=function(){this.alwaysEnabled=!0,this.updateOnSelect=!0,this.shortcuts=[{pattern:"ctrl+right"}],this.getstate=function(){return this.fm.history.canForward()?0:-1},this.exec=function(){return this.fm.history.forward()}},elFinder.prototype.commands.getfile=function(){var b=this,c=this.fm,d=function(c){var d=b.options;return c=a.map(c,function(a){return a.mime!="directory"||d.folders?a:null}),d.multiple||c.length==1?c:[]};this.alwaysEnabled=!0,this.callback=c.options.getFileCallback,this._disabled=typeof this.callback=="function",this.getstate=function(a){var a=this.files(a),b=a.length;return this.callback&&b&&d(a).length==b?0:-1},this.exec=function(c){var d=this.fm,e=this.options,f=this.files(c),g=f.length,h=d.option("url"),i=d.option("tmbUrl"),j=a.Deferred().done(function(a){d.trigger("getfile",{files:a}),b.callback(a,d),e.oncomplete=="close"?d.hide():e.oncomplete=="destroy"&&d.destroy()}),k=function(b){return e.onlyURL?e.multiple?a.map(f,function(a){return a.url}):f[0].url:e.multiple?f:f[0]},l=[],m,n,o;if(this.getstate()==-1)return j.reject();for(m=0;m<g;m++){n=f[m];if(n.mime=="directory"&&!e.folders)return j.reject();n.baseUrl=h,n.url=d.url(n.hash),n.path=d.path(n.hash),n.tmb&&n.tmb!=1&&(n.tmb=i+n.tmb),!n.width&&!n.height&&(n.dim?(o=n.dim.split("x"),n.width=o[0],n.height=o[1]):n.mime.indexOf("image")!==-1&&l.push(d.request({data:{cmd:"dim",target:n.hash},preventDefault:!0}).done(a.proxy(function(a){a.dim&&(o=a.dim.split("x"),this.width=o[0],this.height=o[1]),this.dim=a.dim},f[m]))))}return l.length?(a.when.apply(null,l).always(function(){j.resolve(k(f))}),j):j.resolve(k(f))}},elFinder.prototype.commands.help=function(){var b=this.fm,c=this,d='<div class="elfinder-help-link"> <a href="{url}">{link}</a></div>',e='<div class="elfinder-help-team"><div>{author}</div>{work}</div>',f=/\{url\}/,g=/\{link\}/,h=/\{author\}/,i=/\{work\}/,j="replace",k="ui-priority-primary",l="ui-priority-secondary",m="elfinder-help-license",n='<li class="ui-state-default ui-corner-top"><a href="#{id}">{title}</a></li>',o=['<div class="ui-tabs ui-widget ui-widget-content ui-corner-all elfinder-help">','<ul class="ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all">'],p='<div class="elfinder-help-shortcut"><div class="elfinder-help-shortcut-pattern">{pattern}</div> {descrip}</div>',q='<div class="elfinder-help-separator"/>',r=function(){o.push('<div id="about" class="ui-tabs-panel ui-widget-content ui-corner-bottom"><div class="elfinder-help-logo"/>'),o.push("<h3>elFinder</h3>"),o.push('<div class="'+k+'">'+b.i18n("webfm")+"</div>"),o.push('<div class="'+l+'">'+b.i18n("ver")+": "+b.version+", "+b.i18n("protocol")+": "+b.api+"</div>"),o.push('<div class="'+l+'">jQuery/jQuery UI: '+a().jquery+"/"+a.ui.version+"</div>"),o.push(q),o.push(d[j](f,"http://elfinder.org/")[j](g,b.i18n("homepage"))),o.push(d[j](f,"https://github.com/Studio-42/elFinder/wiki")[j](g,b.i18n("docs"))),o.push(d[j](f,"https://github.com/Studio-42/elFinder")[j](g,b.i18n("github"))),o.push(d[j](f,"http://twitter.com/elrte_elfinder")[j](g,b.i18n("twitter"))),o.push(q),o.push('<div class="'+k+'">'+b.i18n("team")+"</div>"),o.push(e[j](h,'Dmitry "dio" Levashov &lt;dio@std42.ru&gt;')[j](i,b.i18n("chiefdev"))),o.push(e[j](h,"Troex Nevelin &lt;troex@fury.scancode.ru&gt;")[j](i,b.i18n("maintainer"))),o.push(e[j](h,"Alexey Sukhotin &lt;strogg@yandex.ru&gt;")[j](i,b.i18n("contributor"))),o.push(e[j](h,"Naoki Sawada &lt;hypweb@gmail.com&gt;")[j](i,b.i18n("contributor"))),b.i18[b.lang].translator&&o.push(e[j](h,b.i18[b.lang].translator)[j](i,b.i18n("translator")+" ("+b.i18[b.lang].language+")")),o.push(q),o.push('<div class="'+m+'">'+b.i18n("icons")+': <a href="http://pixelmixer.ru/" target="_blank">Pixelmixer</a>, <a href="http://p.yusukekamiyamane.com" target="_blank">Fugue</a></div>'),o.push(q),o.push('<div class="'+m+'">Licence: BSD Licence</div>'),o.push('<div class="'+m+'">Copyright © 2009-2011, Studio 42</div>'),o.push('<div class="'+m+'">„ …'+b.i18n("dontforget")+" ”</div>"),o.push("</div>")},s=function(){var c=b.shortcuts();o.push('<div id="shortcuts" class="ui-tabs-panel ui-widget-content ui-corner-bottom">'),c.length?(o.push('<div class="ui-widget-content elfinder-help-shortcuts">'),a.each(c,function(a,b){o.push(p.replace(/\{pattern\}/,b[0]).replace(/\{descrip\}/,b[1]))}),o.push("</div>")):o.push('<div class="elfinder-help-disabled">'+b.i18n("shortcutsof")+"</div>"),o.push("</div>")},t=function(){o.push('<div id="help" class="ui-tabs-panel ui-widget-content ui-corner-bottom">'),o.push('<a href="http://elfinder.org/forum/" target="_blank" class="elfinder-dont-panic"><span>DON\'T PANIC</span></a>'),o.push("</div>")},u;this.alwaysEnabled=!0,this.updateOnSelect=!1,this.state=0,this.shortcuts=[{pattern:"f1",description:this.title}],setTimeout(function(){var d=c.options.view||["about","shortcuts","help"];a.each(d,function(a,c){o.push(n[j](/\{id\}/,c)[j](/\{title\}/,b.i18n(c)))}),o.push("</ul>"),a.inArray("about",d)!==-1&&r(),a.inArray("shortcuts",d)!==-1&&s(),a.inArray("help",d)!==-1&&t(),o.push("</div>"),u=a(o.join("")),u.find(".ui-tabs-nav li").hover(function(){a(this).toggleClass("ui-state-hover")}).children().click(function(b){var c=a(this);b.preventDefault(),b.stopPropagation(),c.is(".ui-tabs-selected")||(c.parent().addClass("ui-tabs-selected ui-state-active").siblings().removeClass("ui-tabs-selected").removeClass("ui-state-active"),u.find(".ui-tabs-panel").hide().filter(c.attr("href")).show())}).filter(":first").click()},200),this.getstate=function(){return 0},this.exec=function(){this.dialog||(this.dialog=this.fm.dialog(u,{title:this.title,width:530,autoOpen:!1,destroyOnClose:!1})),this.dialog.elfinderdialog("open").find(".ui-tabs-nav li a:first").click()}},elFinder.prototype.commands.home=function(){this.title="Home",this.alwaysEnabled=!0,this.updateOnSelect=!1,this.shortcuts=[{pattern:"ctrl+home ctrl+shift+up",description:"Home"}],this.getstate=function(){var a=this.fm.root(),b=this.fm.cwd().hash;return a&&b&&a!=b?0:-1},this.exec=function(){return this.fm.exec("open",this.fm.root())}},elFinder.prototype.commands.info=function(){var b="msg",c=this.fm,d="elfinder-info-spinner",e={calc:c.i18n("calc"),size:c.i18n("size"),unknown:c.i18n("unknown"),path:c.i18n("path"),aliasfor:c.i18n("aliasfor"),modify:c.i18n("modify"),perms:c.i18n("perms"),locked:c.i18n("locked"),dim:c.i18n("dim"),kind:c.i18n("kind"),files:c.i18n("files"),folders:c.i18n("folders"),items:c.i18n("items"),yes:c.i18n("yes"),no:c.i18n("no"),link:c.i18n("link")};this.tpl={main:'<div class="ui-helper-clearfix elfinder-info-title"><span class="elfinder-cwd-icon {class} ui-corner-all"/>{title}</div><table class="elfinder-info-tb">{content}</table>',itemTitle:'<strong>{name}</strong><span class="elfinder-info-kind">{kind}</span>',groupTitle:"<strong>{items}: {num}</strong>",row:"<tr><td>{label} : </td><td>{value}</td></tr>",spinner:'<span>{text}</span> <span class="'+d+'"/>'},this.alwaysEnabled=!0,this.updateOnSelect=!1,this.shortcuts=[{pattern:"ctrl+i"}],this.init=function(){a.each(e,function(a,b){e[a]=c.i18n(b)})},this.getstate=function(){return 0},this.exec=function(b){var c=this,f=this.fm,g=this.tpl,h=g.row,i=this.files(b),j=i.length,k=[],l=g.main,m="{label}",n="{value}",o={title:this.title,width:"auto",close:function(){a(this).elfinderdialog("destroy")}},p=[],q=function(a){s.find("."+d).parent().text(a)},r=f.namespace+"-info-"+a.map(i,function(a){return a.hash}).join("-"),s=f.getUI().find("#"+r),t,u,v,w,x;if(!j)return a.Deferred().reject();if(s.length)return s.elfinderdialog("toTop"),a.Deferred().resolve();j==1?(v=i[0],l=l.replace("{class}",f.mime2class(v.mime)),w=g.itemTitle.replace("{name}",v.name).replace("{kind}",f.mime2kind(v)),v.tmb&&(u=f.option("tmbUrl")+v.tmb),v.read?v.mime!="directory"||v.alias?t=f.formatSize(v.size):(t=g.spinner.replace("{text}",e.calc),p.push(v.hash)):t=e.unknown,k.push(h.replace(m,e.size).replace(n,t)),v.alias&&k.push(h.replace(m,e.aliasfor).replace(n,v.alias)),k.push(h.replace(m,e.path).replace(n,f.escape(f.path
(v.hash)))),v.read&&k.push(h.replace(m,e.link).replace(n,'<a href="'+f.url(v.hash)+'" target="_blank">'+v.name+"</a>")),v.dim?k.push(h.replace(m,e.dim).replace(n,v.dim)):v.mime.indexOf("image")!==-1&&(v.width&&v.height?k.push(h.replace(m,e.dim).replace(n,v.width+"x"+v.height)):(k.push(h.replace(m,e.dim).replace(n,g.spinner.replace("{text}",e.calc))),f.request({data:{cmd:"dim",target:v.hash},preventDefault:!0}).fail(function(){q(e.unknown)}).done(function(a){q(a.dim||e.unknown)}))),k.push(h.replace(m,e.modify).replace(n,f.formatDate(v))),k.push(h.replace(m,e.perms).replace(n,f.formatPermissions(v))),k.push(h.replace(m,e.locked).replace(n,v.locked?e.yes:e.no))):(l=l.replace("{class}","elfinder-cwd-icon-group"),w=g.groupTitle.replace("{items}",e.items).replace("{num}",j),x=a.map(i,function(a){return a.mime=="directory"?1:null}).length,x?(k.push(h.replace(m,e.kind).replace(n,x==j?e.folders:e.folders+" "+x+", "+e.files+" "+(j-x))),k.push(h.replace(m,e.size).replace(n,g.spinner.replace("{text}",e.calc))),p=a.map(i,function(a){return a.hash})):(t=0,a.each(i,function(a,b){var c=parseInt(b.size);c>=0&&t>=0?t+=c:t="unknown"}),k.push(h.replace(m,e.kind).replace(n,e.files)),k.push(h.replace(m,e.size).replace(n,f.formatSize(t))))),l=l.replace("{title}",w).replace("{content}",k.join("")),s=f.dialog(l,o),s.attr("id",r),u&&a("<img/>").load(function(){s.find(".elfinder-cwd-icon").css("background",'url("'+u+'") center center no-repeat')}).attr("src",u),p.length&&f.request({data:{cmd:"size",targets:p},preventDefault:!0}).fail(function(){q(e.unknown)}).done(function(a){var b=parseInt(a.size);f.log(a.size),q(b>=0?f.formatSize(b):e.unknown)})}},elFinder.prototype.commands.mkdir=function(){this.disableOnSearch=!0,this.updateOnSelect=!1,this.mime="directory",this.prefix="untitled folder",this.exec=a.proxy(this.fm.res("mixin","make"),this),this.shortcuts=[{pattern:"ctrl+shift+n"}],this.getstate=function(){return!this._disabled&&this.fm.cwd().write?0:-1}},elFinder.prototype.commands.mkfile=function(){this.disableOnSearch=!0,this.updateOnSelect=!1,this.mime="text/plain",this.prefix="untitled file.txt",this.exec=a.proxy(this.fm.res("mixin","make"),this),this.getstate=function(){return!this._disabled&&this.fm.cwd().write?0:-1}},elFinder.prototype.commands.open=function(){this.alwaysEnabled=!0,this._handlers={dblclick:function(a){a.preventDefault(),this.exec()},"select enable disable reload":function(a){this.update(a.type=="disable"?-1:void 0)}},this.shortcuts=[{pattern:"ctrl+down numpad_enter"+(this.fm.OS!="mac"&&" enter")}],this.getstate=function(b){var b=this.files(b),c=b.length;return c==1?0:c?a.map(b,function(a){return a.mime=="directory"?null:a}).length==c?0:-1:-1},this.exec=function(b){var c=this.fm,d=a.Deferred().fail(function(a){a&&c.error(a)}),e=this.files(b),f=e.length,g,h,i,j;if(!f)return d.reject();if(f==1&&(g=e[0])&&g.mime=="directory")return g&&!g.read?d.reject(["errOpen",g.name,"errPerm"]):c.request({data:{cmd:"open",target:g.thash||g.hash},notify:{type:"open",cnt:1,hideCnt:!0},syncOnFail:!0});e=a.map(e,function(a){return a.mime!="directory"?a:null});if(f!=e.length)return d.reject();f=e.length;while(f--){g=e[f];if(!g.read)return d.reject(["errOpen",g.name,"errPerm"]);(h=c.url(g.hash))||(h=c.options.url,h=h+(h.indexOf("?")===-1?"?":"&")+(c.oldAPI?"cmd=open&current="+g.phash:"cmd=file")+"&target="+g.hash),j="",g.dim&&(i=g.dim.split("x"),j="width="+(parseInt(i[0])+20)+",height="+(parseInt(i[1])+20));if(!window.open(h,"_blank",j+",top=50,left=50,scrollbars=yes,resizable=yes"))return d.reject("errPopup")}return d.resolve(b)}},elFinder.prototype.commands.paste=function(){this.disableOnSearch=!0,this.updateOnSelect=!1,this.handlers={changeclipboard:function(){this.update()}},this.shortcuts=[{pattern:"ctrl+v shift+insert"}],this.getstate=function(b){if(this._disabled)return-1;if(b){if(a.isArray(b)){if(b.length!=1)return-1;b=this.fm.file(b[0])}}else b=this.fm.cwd();return this.fm.clipboard().length&&b.mime=="directory"&&b.write?0:-1},this.exec=function(b){var c=this,d=c.fm,b=b?this.files(b)[0]:d.cwd(),e=d.clipboard(),f=e.length,g=f?e[0].cut:!1,h=g?"errMove":"errCopy",i=[],j=[],k=a.Deferred().fail(function(a){a&&d.error(a)}),l=function(b){return b.length&&d._commands.duplicate?d.exec("duplicate",b):a.Deferred().resolve()},m=function(e){var f=a.Deferred(),h=[],i=function(b,c){var d=[],e=b.length;while(e--)a.inArray(b[e].name,c)!==-1&&d.unshift(e);return d},j=function(a){var b=h[a],c=e[b],i=a==h.length-1;if(!c)return;d.confirm({title:d.i18n(g?"moveFiles":"copyFiles"),text:d.i18n(["errExists",c.name,"confirmRepl"]),all:!i,accept:{label:"btnYes",callback:function(b){!i&&!b?j(++a):l(e)}},reject:{label:"btnNo",callback:function(b){var c;if(b){c=h.length;while(a<c--)e[h[c]].remove=!0}else e[h[a]].remove=!0;!i&&!b?j(++a):l(e)}},cancel:{label:"btnCancel",callback:function(){f.resolve()}}})},k=function(a){h=i(e,a),h.length?j(0):l(e)},l=function(c){var c=a.map(c,function(a){return a.remove?null:a}),e=c.length,h={},i=[],j;if(!e)return f.resolve();j=c[0].phash,c=a.map(c,function(a){return a.hash}),d.request({data:{cmd:"paste",dst:b.hash,targets:c,cut:g?1:0,src:j},notify:{type:g?"move":"copy",cnt:e}}).always(function(){d.unlockfiles({files:c})})};return c._disabled||!e.length?f.resolve():(d.oldAPI?l(e):d.option("copyOverwrite")?b.hash==d.cwd().hash?k(a.map(d.files(),function(a){return a.phash==b.hash?a.name:null})):d.request({data:{cmd:"ls",target:b.hash},notify:{type:"prepare",cnt:1,hideCnt:!0},preventFail:!0}).always(function(a){k(a.list||[])}):l(e),f)},n,o;return!f||!b||b.mime!="directory"?k.reject():b.write?(n=d.parents(b.hash),a.each(e,function(c,f){if(!f.read)return!k.reject([h,e[0].name,"errPerm"]);if(g&&f.locked)return!k.reject(["errLocked",f.name]);if(a.inArray(f.hash,n)!==-1)return!k.reject(["errCopyInItself",f.name]);o=d.parents(f.hash);if(a.inArray(b.hash,o)!==-1&&a.map(o,function(a){var c=d.file(a);return c.phash==b.hash&&c.name==f.name?c:null}).length)return!k.reject(["errReplByChild",f.name]);f.phash==b.hash?j.push(f.hash):i.push({hash:f.hash,phash:f.phash,name:f.name})}),k.isRejected()?k:a.when(l(j),m(i)).always(function(){g&&d.clipboard([])})):k.reject([h,e[0].name,"errPerm"])}},elFinder.prototype.commands.quicklook=function(){var b=this,c=b.fm,d=0,e=1,f=2,g=d,h="elfinder-quicklook-navbar-icon",i="elfinder-quicklook-fullscreen",j=function(b){a(document).trigger(a.Event("keydown",{keyCode:b,ctrlKey:!1,shiftKey:!1,altKey:!1,metaKey:!1}))},k=function(a){return{opacity:0,width:20,height:c.view=="list"?1:20,top:a.offset().top+"px",left:a.offset().left+"px"}},l=function(){var b=a(window);return{opacity:1,width:n,height:o,top:parseInt((b.height()-o)/2+b.scrollTop()),left:parseInt((b.width()-n)/2+b.scrollLeft())}},m=function(a){var b=document.createElement(a.substr(0,a.indexOf("/"))),c=b.canPlayType&&b.canPlayType(a);return c&&c!==""&&c!="no"},n,o,p,q,r=a('<div class="elfinder-quicklook-title"/>'),s=a("<div/>"),t=a('<div class="elfinder-quicklook-info"/>'),u=a('<div class="'+h+" "+h+'-fullscreen"/>').mousedown(function(d){var e=b.window,f=e.is("."+i),g="scroll."+c.namespace,j=a(window);d.stopPropagation(),f?(e.css(e.data("position")).unbind("mousemove"),j.unbind(g).trigger(b.resize).unbind(b.resize),v.unbind("mouseenter").unbind("mousemove")):(e.data("position",{left:e.css("left"),top:e.css("top"),width:e.width(),height:e.height()}).css({width:"100%",height:"100%"}),a(window).bind(g,function(){e.css({left:parseInt(a(window).scrollLeft())+"px",top:parseInt(a(window).scrollTop())+"px"})}).bind(b.resize,function(a){b.preview.trigger("changesize")}).trigger(g).trigger(b.resize),e.bind("mousemove",function(a){v.stop(!0,!0).show().delay(3e3).fadeOut("slow")}).mousemove(),v.mouseenter(function(){v.stop(!0,!0).show()}).mousemove(function(a){a.stopPropagation()})),v.attr("style","").draggable(f?"destroy":{}),e.toggleClass(i),a(this).toggleClass(h+"-fullscreen-off"),a.fn.resizable&&p.add(e).resizable(f?"enable":"disable").removeClass("ui-state-disabled")}),v=a('<div class="elfinder-quicklook-navbar"/>').append(a('<div class="'+h+" "+h+'-prev"/>').mousedown(function(){j(37)})).append(u).append(a('<div class="'+h+" "+h+'-next"/>').mousedown(function(){j(39)})).append('<div class="elfinder-quicklook-navbar-separator"/>'
).append(a('<div class="'+h+" "+h+'-close"/>').mousedown(function(){b.window.trigger("close")}));this.resize="resize."+c.namespace,this.info=a('<div class="elfinder-quicklook-info-wrapper"/>').append(s).append(t),this.preview=a('<div class="elfinder-quicklook-preview ui-helper-clearfix"/>').bind("change",function(a){b.info.attr("style","").hide(),s.removeAttr("class").attr("style",""),t.html("")}).bind("update",function(c){var d=b.fm,e=b.preview,f=c.file,g='<div class="elfinder-quicklook-info-data">{value}</div>',h;f?(!f.read&&c.stopImmediatePropagation(),b.window.data("hash",f.hash),b.preview.unbind("changesize").trigger("change").children().remove(),r.html(d.escape(f.name)),t.html(g.replace(/\{value\}/,f.name)+g.replace(/\{value\}/,d.mime2kind(f))+(f.mime=="directory"?"":g.replace(/\{value\}/,d.formatSize(f.size)))+g.replace(/\{value\}/,d.i18n("modify")+": "+d.formatDate(f.date))),s.addClass("elfinder-cwd-icon ui-corner-all "+d.mime2class(f.mime)),f.tmb&&a("<img/>").hide().appendTo(b.preview).load(function(){s.css("background",'url("'+h+'") center center no-repeat'),a(this).remove()}).attr("src",h=d.tmb(f.hash)),b.info.delay(100).fadeIn(10)):c.stopImmediatePropagation()}),this.window=a('<div class="ui-helper-reset ui-widget elfinder-quicklook" style="position:absolute"/>').click(function(a){a.stopPropagation()}).append(a('<div class="elfinder-quicklook-titlebar"/>').append(r).append(a('<span class="ui-icon ui-icon-circle-close"/>').mousedown(function(a){a.stopPropagation(),b.window.trigger("close")}))).append(this.preview.add(v)).append(b.info.hide()).draggable({handle:"div.elfinder-quicklook-titlebar"}).bind("open",function(a){var c=b.window,d=b.value,h;b.closed()&&d&&(h=q.find("#"+d.hash)).length&&(g=e,h.trigger("scrolltoview"),c.css(k(h)).show().animate(l(),550,function(){g=f,b.update(1,b.value)}))}).bind("close",function(a){var c=b.window,f=b.preview.trigger("change"),h=b.value,j=q.find("#"+c.data("hash")),l=function(){g=d,c.hide(),f.children().remove(),b.update(0,b.value)};b.opened()&&(g=e,c.is("."+i)&&u.mousedown(),j.length?c.animate(k(j),500,l):l())}),this.alwaysEnabled=!0,this.value=null,this.handlers={select:function(){this.update(void 0,this.fm.selectedFiles()[0])},error:function(){b.window.is(":visible")&&b.window.data("hash","").trigger("close")},"searchshow searchhide":function(){this.opened()&&this.window.trigger("close")}},this.shortcuts=[{pattern:"space"}],this.support={audio:{ogg:m('audio/ogg; codecs="vorbis"'),mp3:m("audio/mpeg;"),wav:m('audio/wav; codecs="1"'),m4a:m("audio/x-m4a;")||m("audio/aac;")},video:{ogg:m('video/ogg; codecs="theora"'),webm:m('video/webm; codecs="vp8, vorbis"'),mp4:m('video/mp4; codecs="avc1.42E01E"')||m('video/mp4; codecs="avc1.42E01E, mp4a.40.2"')}},this.closed=function(){return g==d},this.opened=function(){return g==f},this.init=function(){var d=this.options,e=this.window,f=this.preview,g,h;n=d.width>0?parseInt(d.width):450,o=d.height>0?parseInt(d.height):300,c.one("load",function(){p=c.getUI(),q=c.getUI("cwd"),e.appendTo("body").zIndex(100+p.zIndex()),a(document).keydown(function(a){a.keyCode==27&&b.opened()&&e.trigger("close")}),a.fn.resizable&&e.resizable({handles:"se",minWidth:350,minHeight:120,resize:function(){f.trigger("changesize")}}),b.change(function(){b.opened()&&(b.value?f.trigger(a.Event("update",{file:b.value})):e.trigger("close"))}),a.each(c.commands.quicklook.plugins||[],function(a,c){typeof c=="function"&&new c(b)}),f.bind("update",function(){b.info.show()})})},this.getstate=function(){return this.fm.selected().length==1?g==f?1:0:-1},this.exec=function(){this.enabled()&&this.window.trigger(this.opened()?"close":"open")},this.hideinfo=function(){this.info.stop(!0).hide()}},elFinder.prototype.commands.quicklook.plugins=[function(b){var c=["image/jpeg","image/png","image/gif"],d=b.preview;a.each(navigator.mimeTypes,function(b,d){var e=d.type;e.indexOf("image/")===0&&a.inArray(e,c)&&c.push(e)}),d.bind("update",function(e){var f=e.file,g;a.inArray(f.mime,c)!==-1&&(e.stopImmediatePropagation(),g=a("<img/>").hide().appendTo(d).load(function(){setTimeout(function(){var a=(g.width()/g.height()).toFixed(2);d.bind("changesize",function(){var b=parseInt(d.width()),c=parseInt(d.height()),e,f;a<(b/c).toFixed(2)?(f=c,e=Math.floor(f*a)):(e=b,f=Math.floor(e/a)),g.width(e).height(f).css("margin-top",f<c?Math.floor((c-f)/2):0)}).trigger("changesize"),b.hideinfo(),g.fadeIn(100)},1)}).attr("src",b.fm.url(f.hash)))})},function(b){var c=["text/html","application/xhtml+xml"],d=b.preview,e=b.fm;d.bind("update",function(f){var g=f.file,h;a.inArray(g.mime,c)!==-1&&(f.stopImmediatePropagation(),d.one("change",function(){!h.isResolved()&&!h.isRejected()&&h.reject()}),h=e.request({data:{cmd:"get",target:g.hash,current:g.phash},preventDefault:!0}).done(function(c){b.hideinfo(),doc=a('<iframe class="elfinder-quicklook-preview-html"/>').appendTo(d)[0].contentWindow.document,doc.open(),doc.write(c.content),doc.close()}))})},function(b){var c=b.fm,d=c.res("mimes","text"),e=b.preview;e.bind("update",function(f){var g=f.file,h=g.mime,i;if(h.indexOf("text/")===0||a.inArray(h,d)!==-1)f.stopImmediatePropagation(),e.one("change",function(){!i.isResolved()&&!i.isRejected()&&i.reject()}),i=c.request({data:{cmd:"get",target:g.hash},preventDefault:!0}).done(function(d){b.hideinfo(),a('<div class="elfinder-quicklook-preview-text-wrapper"><pre class="elfinder-quicklook-preview-text">'+c.escape(d.content)+"</pre></div>").appendTo(e)})})},function(b){var c=b.fm,d="application/pdf",e=b.preview,f=!1;a.browser.safari&&navigator.platform.indexOf("Mac")!=-1||a.browser.msie?f=!0:a.each(navigator.plugins,function(b,c){a.each(c,function(a,b){if(b.type==d)return!(f=!0)})}),f&&e.bind("update",function(f){var g=f.file,h;g.mime==d&&(f.stopImmediatePropagation(),e.one("change",function(){h.unbind("load").remove()}),h=a('<iframe class="elfinder-quicklook-preview-pdf"/>').hide().appendTo(e).load(function(){b.hideinfo(),h.show()}).attr("src",c.url(g.hash)))})},function(b){var c=b.fm,d="application/x-shockwave-flash",e=b.preview,f=!1;a.each(navigator.plugins,function(b,c){a.each(c,function(a,b){if(b.type==d)return!(f=!0)})}),f&&e.bind("update",function(f){var g=f.file,h;g.mime==d&&(f.stopImmediatePropagation(),b.hideinfo(),e.append(h=a('<embed class="elfinder-quicklook-preview-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" src="'+c.url(g.hash)+'" quality="high" type="application/x-shockwave-flash" />')))})},function(b){var c=b.preview,d=!!b.options.autoplay,e={"audio/mpeg":"mp3","audio/mpeg3":"mp3","audio/mp3":"mp3","audio/x-mpeg3":"mp3","audio/x-mp3":"mp3","audio/x-wav":"wav","audio/wav":"wav","audio/x-m4a":"m4a","audio/aac":"m4a","audio/mp4":"m4a","audio/x-mp4":"m4a","audio/ogg":"ogg"},f;c.bind("update",function(g){var h=g.file,i=e[h.mime];b.support.audio[i]&&(g.stopImmediatePropagation(),f=a('<audio class="elfinder-quicklook-preview-audio" controls preload="auto" autobuffer><source src="'+b.fm.url(h.hash)+'" /></audio>').appendTo(c),d&&f[0].play())}).bind("change",function(){f&&f.parent().length&&(f[0].pause(),f.remove(),f=null)})},function(b){var c=b.preview,d=!!b.options.autoplay,e={"video/mp4":"mp4","video/x-m4v":"mp4","video/ogg":"ogg","application/ogg":"ogg","video/webm":"webm"},f;c.bind("update",function(g){var h=g.file,i=e[h.mime];b.support.video[i]&&(g.stopImmediatePropagation(),b.hideinfo(),f=a('<video class="elfinder-quicklook-preview-video" controls preload="auto" autobuffer><source src="'+b.fm.url(h.hash)+'" /></video>').appendTo(c),d&&f[0].play())}).bind("change",function(){f&&f.parent().length&&(f[0].pause(),f.remove(),f=null)})},function(b){var c=b.preview,d=[],e;a.each(navigator.plugins,function(b,c){a.each(c,function(a,b){(b.type.indexOf("audio/")===0||b.type.indexOf("video/")===0)&&d.push(b.type)})}),c.bind("update",function(f){var g=f.file,h=g.mime,i;a.inArray(g.mime,d)!==-1&&(f.stopImmediatePropagation(),(i=h.indexOf("video/")===0)&&b.hideinfo(),e=a('<embed src="'+b.fm.url(g.hash)+'" type="'+h+'" class="elfinder-quicklook-preview-'+(i?"video":"audio")+'"/>').appendTo(c))}).bind("change",function(){e&&e.parent().length&&(e.remove(),e=null)})}],elFinder.prototype.commands.reload=function(){this.alwaysEnabled=!0
,this.updateOnSelect=!0,this.shortcuts=[{pattern:"ctrl+shift+r f5"}],this.getstate=function(){return 0},this.exec=function(){var a=this.fm,b=a.sync(),c=setTimeout(function(){a.notify({type:"reload",cnt:1,hideCnt:!0}),b.always(function(){a.notify({type:"reload",cnt:-1})})},a.notifyDelay);return b.always(function(){clearTimeout(c),a.trigger("reload")})}},elFinder.prototype.commands.rename=function(){this.shortcuts=[{pattern:"f2"+(this.fm.OS=="mac"?" enter":"")}],this.getstate=function(){var a=this.fm.selectedFiles();return!this._disabled&&a.length==1&&a[0].phash&&!a[0].locked?0:-1},this.exec=function(){var b=this.fm,c=b.getUI("cwd"),d=b.selected(),e=d.length,f=b.file(d.shift()),g=".elfinder-cwd-filename",h=a.Deferred().fail(function(a){var d=i.parent(),e=b.escape(f.name);d.length?(i.remove(),d.html(e)):(c.find("#"+f.hash).find(g).html(e),setTimeout(function(){c.find("#"+f.hash).click()},50)),a&&b.error(a)}).always(function(){b.enable()}),i=a('<input type="text"/>').keydown(function(b){b.stopPropagation(),b.stopImmediatePropagation(),b.keyCode==a.ui.keyCode.ESCAPE?h.reject():b.keyCode==a.ui.keyCode.ENTER&&i.blur()}).mousedown(function(a){a.stopPropagation()}).dblclick(function(a){a.stopPropagation(),a.preventDefault()}).blur(function(){var c=a.trim(i.val()),d=i.parent();if(d.length){i[0].setSelectionRange&&i[0].setSelectionRange(0,0);if(c==f.name)return h.reject();if(!c)return h.reject("errInvName");if(b.fileByName(c,f.phash))return h.reject(["errExists",c]);d.html(b.escape(c)),b.lockfiles({files:[f.hash]}),b.request({data:{cmd:"rename",target:f.hash,name:c},notify:{type:"rename",cnt:1}}).fail(function(a){h.reject(),b.sync()}).done(function(a){h.resolve(a)}).always(function(){b.unlockfiles({files:[f.hash]})})}}),j=c.find("#"+f.hash).find(g).empty().append(i.val(f.name)),k=i.val().replace(/\.((tar\.(gz|bz|bz2|z|lzo))|cpio\.gz|ps\.gz|xcf\.(gz|bz2)|[a-z0-9]{1,4})$/ig,"");return this.disabled()?h.reject():!f||e>1||!j.length?h.reject("errCmdParams",this.title):f.locked?h.reject(["errLocked",f.name]):(b.one("select",function(){i.parent().length&&f&&a.inArray(f.hash,b.selected())===-1&&i.blur()}),i.select().focus(),i[0].setSelectionRange&&i[0].setSelectionRange(0,k.length),h)}},elFinder.prototype.commands.resize=function(){this.updateOnSelect=!1,this.getstate=function(){var a=this.fm.selectedFiles();return!this._disabled&&a.length==1&&a[0].read&&a[0].write&&a[0].mime.indexOf("image/")!==-1?0:-1},this.exec=function(b){var c=this.fm,d=this.files(b),e=a.Deferred(),f=function(b,d){var f=a('<div class="elfinder-dialog-resize"/>'),g='<input type="text" size="5"/>',h='<div class="elfinder-resize-row"/>',i='<div class="elfinder-resize-label"/>',j=a('<div class="elfinder-resize-control"/>'),k=a('<div class="elfinder-resize-preview"/>'),l=a('<div class="elfinder-resize-spinner">'+c.i18n("ntfloadimg")+"</div>"),m=a('<div class="elfinder-resize-handle"/>'),n=a('<div class="elfinder-resize-handle"/>'),o=a('<div class="elfinder-resize-uiresize"/>'),p=a('<div class="elfinder-resize-uicrop"/>'),q='<div class="ui-widget-content ui-corner-all elfinder-buttonset"/>',r='<div class="ui-state-default elfinder-button"/>',s='<span class="ui-widget-content elfinder-toolbar-button-separator"/>',t=a('<div class="elfinder-resize-rotate"/>'),u=a(r).attr("title",c.i18n("rotate-cw")).append(a('<span class="elfinder-button-icon elfinder-button-icon-rotate-l"/>').click(function(){S-=90,ab.update(S)})),v=a(r).attr("title",c.i18n("rotate-ccw")).append(a('<span class="elfinder-button-icon elfinder-button-icon-rotate-r"/>').click(function(){S+=90,ab.update(S)})),w=a("<span />"),x=a('<div class="ui-state-default ui-corner-all elfinder-resize-reset"><span class="ui-icon ui-icon-arrowreturnthick-1-w"/></div>'),y=a('<div class="elfinder-resize-type"/>').append('<input type="radio" name="type" id="type-resize" value="resize" checked="checked" /><label for="type-resize">'+c.i18n("resize")+"</label>").append('<input type="radio" name="type" id="type-crop"   value="crop"/><label for="type-crop">'+c.i18n("crop")+"</label>").append('<input type="radio" name="type" id="type-rotate" value="rotate"/><label for="type-rotate">'+c.i18n("rotate")+"</label>"),z=a("input",y).change(function(){var b=a("input:checked",y).val();Y(),bb(!0),cb(!0),db(!0),b=="resize"?(o.show(),t.hide(),p.hide(),bb()):b=="crop"?(t.hide(),o.hide(),p.show(),cb()):b=="rotate"&&(o.hide(),p.hide(),t.show(),db())}),A=a('<input type="checkbox" checked="checked"/>').change(function(){N=!!A.prop("checked"),Z.fixHeight(),bb(!0),bb()}),B=a(g).change(function(){var a=parseInt(B.val()),b=parseInt(N?a/J:C.val());a>0&&b>0&&(Z.updateView(a,b),C.val(b))}),C=a(g).change(function(){var a=parseInt(C.val()),b=parseInt(N?a*J:B.val());b>0&&a>0&&(Z.updateView(b,a),B.val(b))}),D=a(g),E=a(g),F=a(g),G=a(g),H=a('<input type="text" size="3" maxlength="3" value="0" />').change(function(){ab.update()}),I=a('<div class="elfinder-resize-rotate-slider"/>').slider({min:0,max:359,value:H.val(),animate:!0,change:function(a,b){b.value!=I.slider("value")&&ab.update(b.value)},slide:function(a,b){ab.update(b.value,!1)}}),J=1,K=1,L=0,M=0,N=!0,O=0,P=0,Q=0,R=0,S=0,T=a("<img/>").load(function(){l.remove(),L=T.width(),M=T.height(),J=L/M,Z.updateView(L,M),m.append(T.show()).show(),B.val(L),C.val(M);var b=Math.min(O,P)/Math.sqrt(Math.pow(L,2)+Math.pow(M,2));Q=L*b,R=M*b,j.find("input,select").removeAttr("disabled").filter(":text").keydown(function(b){var c=b.keyCode,d;b.stopPropagation();if(c>=37&&c<=40||c==a.ui.keyCode.BACKSPACE||c==a.ui.keyCode.DELETE||c==65&&(b.ctrlKey||b.metaKey)||c==27)return;c==9&&(d=a(this).parent()[b.shiftKey?"prev":"next"](".elfinder-resize-row").children(":text"),d.length&&d.focus());if(c==13){eb();return}(c<48||c>57)&&b.preventDefault()}).filter(":first").focus(),bb(),x.hover(function(){x.toggleClass("ui-state-hover")}).click(Y)}).error(function(){l.text("Unable to load image").css("background","transparent")}),U=a("<div/>"),V=a("<img/>"),W=a("<div/>"),X=a("<img/>"),Y=function(){B.val(L),C.val(M),Z.updateView(L,M)},Z={update:function(){B.val(parseInt(T.width()/K)),C.val(parseInt(T.height()/K))},updateView:function(a,b){a>O||b>P?a/O>b/P?T.width(O).height(Math.ceil(T.width()/J)):T.height(P).width(Math.ceil(T.height()*J)):T.width(a).height(b),K=T.width()/a,w.text("1 : "+(1/K).toFixed(2)),Z.updateHandle()},updateHandle:function(){m.width(T.width()).height(T.height())},fixWidth:function(){var a,b;N&&(b=C.val(),b=parseInt(b*J),Z.updateView(a,b),B.val(a))},fixHeight:function(){var a,b;N&&(a=B.val(),b=parseInt(a/J),Z.updateView(a,b),C.val(b))}},_={update:function(){F.val(parseInt(n.width()/K)),G.val(parseInt(n.height()/K)),D.val(parseInt((n.offset().left-V.offset().left)/K)),E.val(parseInt((n.offset().top-V.offset().top)/K))},resize_update:function(){_.update(),W.width(n.width()),W.height(n.height())}},ab={mouseStartAngle:0,imageStartAngle:0,imageBeingRotated:!1,update:function(b,c){typeof b=="undefined"&&(S=b=parseInt(H.val())),typeof c=="undefined"&&(c=!0),!c||a.browser.opera||a.browser.msie&&parseInt(a.browser.version)<9?X.rotate(b):X.animate({rotate:b+"deg"}),b%=360,b<0&&(b+=360),H.val(parseInt(b)),I.slider("value",H.val())},execute:function(a){if(!ab.imageBeingRotated)return;var b=ab.getCenter(X),c=a.pageX-b[0],d=a.pageY-b[1],e=Math.atan2(d,c),f=e-ab.mouseStartAngle+ab.imageStartAngle;return f=Math.round(parseFloat(f)*180/Math.PI),a.shiftKey&&(f=Math.round((f+6)/15)*15),X.rotate(f),f%=360,f<0&&(f+=360),H.val(f),I.slider("value",H.val()),!1},start:function(b){ab.imageBeingRotated=!0;var c=ab.getCenter(X),d=b.pageX-c[0],e=b.pageY-c[1];return ab.mouseStartAngle=Math.atan2(e,d),ab.imageStartAngle=parseFloat(X.rotate())*Math.PI/180,a(document).mousemove(ab.execute),!1},stop:function(b){if(!ab.imageBeingRotated)return;return a(document).unbind("mousemove",ab.execute),setTimeout(function(){ab.imageBeingRotated=!1},10),!1},getCenter:function(a){var b=X.rotate();X.rotate(0);var c=X.offset(),d=c.left+X.width()/2,e=c.top+X.height()/2;return X.rotate(b),Array(d,e)}},bb=function(b){a.fn.resizable&&(b?(m.resizable("destroy"),m.hide()):(m.show(),m.resizable({alsoResize:T,aspectRatio:N,resize:Z.update,stop:Z.fixHeight})))},cb=function(b){a.fn.draggable&&a.fn.resizable&&
(b?(n.resizable("destroy"),n.draggable("destroy"),U.hide()):(V.width(T.width()).height(T.height()),W.width(T.width()).height(T.height()),n.width(V.width()).height(V.height()).offset(V.offset()).resizable({containment:U,resize:_.resize_update,handles:"all"}).draggable({handle:n,containment:V,drag:_.update}),U.show().width(T.width()).height(T.height()),_.update()))},db=function(b){a.fn.draggable&&a.fn.resizable&&(b?X.hide():X.show().width(Q).height(R).css("margin-top",(P-R)/2+"px").css("margin-left",(O-Q)/2+"px"))},eb=function(){var d,g,h,i,j,k=a("input:checked",y).val();B.add(C).change();if(k=="resize")d=parseInt(B.val())||0,g=parseInt(C.val())||0;else if(k=="crop")d=parseInt(F.val())||0,g=parseInt(G.val())||0,h=parseInt(D.val())||0,i=parseInt(E.val())||0;else if(k="rotate"){d=L,g=M,j=parseInt(H.val())||0;if(j<0||j>360)return c.error("Invalid rotate degree");if(j==0||j==360)return c.error("Image dose not rotated")}if(k!="rotate"){if(d<=0||g<=0)return c.error("Invalid image size");if(d==L&&g==M)return c.error("Image size not changed")}f.elfinderdialog("close"),c.request({data:{cmd:"resize",target:b.hash,width:d,height:g,x:h,y:i,degree:j,mode:k},notify:{type:"resize",cnt:1}}).fail(function(a){e.reject(a)}).done(function(){e.resolve()})},fb={},gb="elfinder-resize-handle-hline",hb="elfinder-resize-handle-vline",ib="elfinder-resize-handle-point",jb=c.url(b.hash);X.mousedown(ab.start),a(document).mouseup(ab.stop),o.append(a(h).append(a(i).text(c.i18n("width"))).append(B).append(x)).append(a(h).append(a(i).text(c.i18n("height"))).append(C)).append(a(h).append(a("<label/>").text(c.i18n("aspectRatio")).prepend(A))).append(a(h).append(c.i18n("scale")+" ").append(w)),p.append(a(h).append(a(i).text("X")).append(D)).append(a(h).append(a(i).text("Y")).append(E)).append(a(h).append(a(i).text(c.i18n("width"))).append(F)).append(a(h).append(a(i).text(c.i18n("height"))).append(G)),t.append(a(h).append(a(i).text(c.i18n("rotate"))).append(a('<div style="float:left; width: 130px;">').append(a('<div style="float:left;">').append(H).append(a("<span/>").text(c.i18n("degree")))).append(a(q).append(u).append(a(s)).append(v))).append(I)),f.append(y),j.append(a(h)).append(o).append(p.hide()).append(t.hide()).find("input,select").attr("disabled","disabled"),m.append('<div class="'+gb+" "+gb+'-top"/>').append('<div class="'+gb+" "+gb+'-bottom"/>').append('<div class="'+hb+" "+hb+'-left"/>').append('<div class="'+hb+" "+hb+'-right"/>').append('<div class="'+ib+" "+ib+'-e"/>').append('<div class="'+ib+" "+ib+'-se"/>').append('<div class="'+ib+" "+ib+'-s"/>'),k.append(l).append(m.hide()).append(T.hide()),n.css("position","absolute").append('<div class="'+gb+" "+gb+'-top"/>').append('<div class="'+gb+" "+gb+'-bottom"/>').append('<div class="'+hb+" "+hb+'-left"/>').append('<div class="'+hb+" "+hb+'-right"/>').append('<div class="'+ib+" "+ib+'-n"/>').append('<div class="'+ib+" "+ib+'-e"/>').append('<div class="'+ib+" "+ib+'-s"/>').append('<div class="'+ib+" "+ib+'-w"/>').append('<div class="'+ib+" "+ib+'-ne"/>').append('<div class="'+ib+" "+ib+'-se"/>').append('<div class="'+ib+" "+ib+'-sw"/>').append('<div class="'+ib+" "+ib+'-nw"/>'),k.append(U.css("position","absolute").hide().append(V).append(n.append(W))),k.append(X.hide()),k.css("overflow","hidden"),f.append(k).append(j),fb[c.i18n("btnCancel")]=function(){f.elfinderdialog("close")},fb[c.i18n("btnApply")]=eb,c.dialog(f,{title:b.name,width:650,resizable:!1,destroyOnClose:!0,buttons:fb,open:function(){k.zIndex(1+a(this).parent().zIndex())}}).attr("id",d),a.browser.msie&&parseInt(a.browser.version)<9&&a(".elfinder-dialog").css("filter",""),x.css("left",B.position().left+B.width()+12),W.css({opacity:.2,"background-color":"#fff",position:"absolute"}),n.css("cursor","move"),n.find(".elfinder-resize-handle-point").css({"background-color":"#fff",opacity:.5,"border-color":"#000"}),X.css("cursor","pointer"),y.buttonset(),O=k.width()-(m.outerWidth()-m.width()),P=k.height()-(m.outerHeight()-m.height()),T.attr("src",jb+(jb.indexOf("?")===-1?"?":"&")+"_="+Math.random()),V.attr("src",T.attr("src")),X.attr("src",T.attr("src"))},g,h;return!d.length||d[0].mime.indexOf("image/")===-1?e.reject():(g="resize-"+c.namespace+"-"+d[0].hash,h=c.getUI().find("#"+g),h.length?(h.elfinderdialog("toTop"),e.resolve()):(f(d[0],g),e))}},function(a){var b=function(a,b){var c=0;for(c in b)if(typeof a[b[c]]!="undefined")return b[c];return a[b[c]]="",b[c]};a.cssHooks.rotate={get:function(b,c,d){return a(b).rotate()},set:function(b,c){return a(b).rotate(c),c}},a.cssHooks.transform={get:function(a,c,d){var e=b(a.style,["WebkitTransform","MozTransform","OTransform","msTransform","transform"]);return a.style[e]},set:function(a,c){var d=b(a.style,["WebkitTransform","MozTransform","OTransform","msTransform","transform"]);return a.style[d]=c,c}},a.fn.rotate=function(b){if(typeof b=="undefined"){if(a.browser.opera){var c=this.css("transform").match(/rotate\((.*?)\)/);return c&&c[1]?Math.round(parseFloat(c[1])*180/Math.PI):0}var c=this.css("transform").match(/rotate\((.*?)\)/);return c&&c[1]?parseInt(c[1]):0}return this.css("transform",this.css("transform").replace(/none|rotate\(.*?\)/,"")+"rotate("+parseInt(b)+"deg)"),this},a.fx.step.rotate=function(b){b.state==0&&(b.start=a(b.elem).rotate(),b.now=b.start),a(b.elem).rotate(b.now)};if(a.browser.msie&&parseInt(a.browser.version)<9){var c=function(a){var b=a,c=b.offsetLeft,d=b.offsetTop;while(b.offsetParent){b=b.offsetParent;if(b!=document.body&&b.currentStyle["position"]!="static")break;b!=document.body&&b!=document.documentElement&&(c-=b.scrollLeft,d-=b.scrollTop),c+=b.offsetLeft,d+=b.offsetTop}return{x:c,y:d}},d=function(a){if(a.currentStyle["position"]!="static")return;var b=c(a);a.style.position="absolute",a.style.left=b.x+"px",a.style.top=b.y+"px"},e=function(a,b){var c,e=1,f=1,g=1,h=1;if(typeof a.style["msTransform"]!="undefined")return!0;d(a),c=b.match(/rotate\((.*?)\)/);var i=c&&c[1]?parseInt(c[1]):0;i%=360,i<0&&(i=360+i);var j=i*Math.PI/180,k=Math.cos(j),l=Math.sin(j);e*=k,f*=-l,g*=l,h*=k,a.style.filter=(a.style.filter||"").replace(/progid:DXImageTransform\.Microsoft\.Matrix\([^)]*\)/,"")+("progid:DXImageTransform.Microsoft.Matrix(M11="+e+",M12="+f+",M21="+g+",M22="+h+",FilterType='bilinear',sizingMethod='auto expand')");var m=parseInt(a.style.width||a.width||0),n=parseInt(a.style.height||a.height||0),j=i*Math.PI/180,o=Math.abs(Math.cos(j)),p=Math.abs(Math.sin(j)),q=(m-(m*o+n*p))/2,r=(n-(m*p+n*o))/2;return a.style.marginLeft=Math.floor(q)+"px",a.style.marginTop=Math.floor(r)+"px",!0},f=a.cssHooks.transform.set;a.cssHooks.transform.set=function(a,b){return f.apply(this,[a,b]),e(a,b),b}}}(jQuery),elFinder.prototype.commands.rm=function(){this.shortcuts=[{pattern:"delete ctrl+backspace"}],this.getstate=function(b){var c=this.fm;return b=b||c.selected(),!this._disabled&&b.length&&a.map(b,function(a){var b=c.file(a);return b&&b.phash&&!b.locked?a:null}).length==b.length?0:-1},this.exec=function(b){var c=this,d=this.fm,e=a.Deferred().fail(function(a){a&&d.error(a)}),f=this.files(b),g=f.length,h=d.cwd().hash,i=!1;return!g||this._disabled?e.reject():(a.each(f,function(a,b){if(!b.phash)return!e.reject(["errRm",b.name,"errPerm"]);if(b.locked)return!e.reject(["errLocked",b.name]);b.hash==h&&(i=d.root(b.hash))}),e.isRejected()||(f=this.hashes(b),d.confirm({title:c.title,text:"confirmRm",accept:{label:"btnRm",callback:function(){d.lockfiles({files:f}),d.request({data:{cmd:"rm",targets:f},notify:{type:"rm",cnt:g},preventFail:!0}).fail(function(a){e.reject(a)}).done(function(a){e.done(a),i&&d.exec("open",i)}).always(function(){d.unlockfiles({files:f})})}},cancel:{label:"btnCancel",callback:function(){e.reject()}}})),e)}},elFinder.prototype.commands.search=function(){this.title="Find files",this.options={ui:"searchbutton"},this.alwaysEnabled=!0,this.updateOnSelect=!1,this.getstate=function(){return 0},this.exec=function(b){var c=this.fm;return typeof b=="string"&&b?(c.trigger("searchstart",{query:b}),c.request({data:{cmd:"search",q:b},notify:{type:"search",cnt:1,hideCnt:!0}})):(c.getUI("toolbar").find("."+c.res("class","searchbtn")+" :text").focus(),a.Deferred().reject())}},elFinder.prototype.commands.sort=function(){var b=
this,c=["nameDirsFirst","kindDirsFirst","sizeDirsFirst","dateDirsFirst","name","kind","size","date"],d;this.options={ui:"sortbutton"},this.value=1,this.variants=[];for(d=0;d<c.length;d++)this.variants.push([c[d],this.fm.i18n("sort"+c[d])]);this.disableOnSearch=!0,this.fm.bind("load sortchange",function(){b.value=c[b.fm.sort-1],b.change()}),this.getstate=function(){return 0},this.exec=function(b,d){var e=a.inArray(d,c)+1==this.fm.sort?this.fm.sortDirect=="asc"?"desc":"asc":this.fm.sortDirect;this.fm.setSort(d,e)}},elFinder.prototype.commands.up=function(){this.alwaysEnabled=!0,this.updateOnSelect=!1,this.shortcuts=[{pattern:"ctrl+up"}],this.getstate=function(){return this.fm.cwd().phash?0:-1},this.exec=function(){return this.fm.cwd().phash?this.fm.exec("open",this.fm.cwd().phash):a.Deferred().reject()}},elFinder.prototype.commands.upload=function(){var b=this.fm.res("class","hover");this.disableOnSearch=!0,this.updateOnSelect=!1,this.shortcuts=[{pattern:"ctrl+u"}],this.getstate=function(){return!this._disabled&&this.fm.cwd().write?0:-1},this.exec=function(c){var d=this.fm,e=function(a){g.elfinderdialog("close"),d.upload(a).fail(function(a){f.reject(a)}).done(function(a){f.resolve(a)})},f,g,h,i,j;return this.disabled()?a.Deferred().reject():c&&(c.input||c.files)?d.upload(c):(f=a.Deferred(),h=a('<input type="file" multiple="true"/>').change(function(){e({input:h[0]})}),i=a('<div class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only"><span class="ui-button-text">'+d.i18n("selectForUpload")+"</span></div>").append(a("<form/>").append(h)).hover(function(){i.toggleClass(b)}),g=a('<div class="elfinder-upload-dialog-wrapper"/>').append(i),d.dragUpload&&(j=a('<div class="ui-corner-all elfinder-upload-dropbox">'+d.i18n("dropFiles")+"</div>").prependTo(g).after('<div class="elfinder-upload-dialog-or">'+d.i18n("or")+"</div>")[0],j.addEventListener("dragenter",function(c){c.stopPropagation(),c.preventDefault(),a(j).addClass(b)},!1),j.addEventListener("dragleave",function(c){c.stopPropagation(),c.preventDefault(),a(j).removeClass(b)},!1),j.addEventListener("dragover",function(a){a.stopPropagation(),a.preventDefault()},!1),j.addEventListener("drop",function(a){a.stopPropagation(),a.preventDefault(),e({files:a.dataTransfer.files})},!1)),d.dialog(g,{title:this.title,modal:!0,resizable:!1,destroyOnClose:!0}),f)}},elFinder.prototype.commands.view=function(){this.value=this.fm.storage("view"),this.alwaysEnabled=!0,this.updateOnSelect=!1,this.options={ui:"viewbutton"},this.getstate=function(){return 0},this.exec=function(){var a=this.fm.storage("view",this.value=="list"?"icons":"list");this.fm.viewchange(),this.update(void 0,a)}}})(jQuery)
/*!
 * jQuery Raty - A Star Rating Plugin
 *
 * Licensed under The MIT License
 *
 * @version        2.4.5
 * @author         Washington Botelho
 * @documentation  wbotelhos.com/raty
 * 
 */

;(function(b){var a={init:function(c){return this.each(function(){var d=this,h=b(d).empty();d.opt=b.extend(true,{},b.fn.raty.defaults,c);h.data("settings",d.opt);d.opt.number=a.between(d.opt.number,0,20);if(d.opt.path.substring(d.opt.path.length-1,d.opt.path.length)!="/"){d.opt.path+="/";}if(typeof d.opt.score=="function"){d.opt.score=d.opt.score.call(d);}if(d.opt.score){d.opt.score=a.between(d.opt.score,0,d.opt.number);}for(var e=1;e<=d.opt.number;e++){b("<img />",{src:d.opt.path+((!d.opt.score||d.opt.score<e)?d.opt.starOff:d.opt.starOn),alt:e,title:(e<=d.opt.hints.length&&d.opt.hints[e-1]!==null)?d.opt.hints[e-1]:e}).appendTo(d);if(d.opt.space){h.append((e<d.opt.number)?"&#160;":"");}}d.stars=h.children('img:not(".raty-cancel")');d.score=b("<input />",{type:"hidden",name:d.opt.scoreName}).appendTo(d);if(d.opt.score&&d.opt.score>0){d.score.val(d.opt.score);a.roundStar.call(d,d.opt.score);}if(d.opt.iconRange){a.fill.call(d,d.opt.score);}a.setTarget.call(d,d.opt.score,d.opt.targetKeep);var g=d.opt.space?4:0,f=d.opt.width||(d.opt.number*d.opt.size+d.opt.number*g);if(d.opt.cancel){d.cancel=b("<img />",{src:d.opt.path+d.opt.cancelOff,alt:"x",title:d.opt.cancelHint,"class":"raty-cancel"});if(d.opt.cancelPlace=="left"){h.prepend("&#160;").prepend(d.cancel);}else{h.append("&#160;").append(d.cancel);}f+=(d.opt.size+g);}if(d.opt.readOnly){a.fixHint.call(d);if(d.cancel){d.cancel.hide();}}else{h.css("cursor","pointer");a.bindAction.call(d);}h.css("width",f);});},between:function(e,d,c){return Math.min(Math.max(parseFloat(e),d),c);},bindAction:function(){var c=this,e=b(c);e.mouseleave(function(){var f=c.score.val()||undefined;a.initialize.call(c,f);a.setTarget.call(c,f,c.opt.targetKeep);if(c.opt.mouseover){c.opt.mouseover.call(c,f);}});var d=c.opt.half?"mousemove":"mouseover";if(c.opt.cancel){c.cancel.mouseenter(function(){b(this).attr("src",c.opt.path+c.opt.cancelOn);c.stars.attr("src",c.opt.path+c.opt.starOff);a.setTarget.call(c,null,true);if(c.opt.mouseover){c.opt.mouseover.call(c,null);}}).mouseleave(function(){b(this).attr("src",c.opt.path+c.opt.cancelOff);if(c.opt.mouseover){c.opt.mouseover.call(c,c.score.val()||null);}}).click(function(f){c.score.removeAttr("value");if(c.opt.click){c.opt.click.call(c,null,f);}});}c.stars.bind(d,function(g){var h=parseInt(this.alt,10);if(c.opt.half){var f=parseFloat((g.pageX-b(this).offset().left)/c.opt.size),i=(f>0.5)?1:0.5;h=parseFloat(this.alt)-1+i;a.fill.call(c,h);if(c.opt.precision){h=h-i+f;}a.showHalf.call(c,h);}else{a.fill.call(c,h);}e.data("score",h);a.setTarget.call(c,h,true);if(c.opt.mouseover){c.opt.mouseover.call(c,h,g);}}).click(function(f){c.score.val((c.opt.half||c.opt.precision)?e.data("score"):this.alt);if(c.opt.click){c.opt.click.call(c,c.score.val(),f);}});},cancel:function(c){return b(this).each(function(){var d=this,e=b(d);if(e.data("readonly")===true){return this;}if(c){a.click.call(d,null);}else{a.score.call(d,null);}d.score.removeAttr("value");});},click:function(c){return b(this).each(function(){if(b(this).data("readonly")===true){return this;}a.initialize.call(this,c);if(this.opt.click){this.opt.click.call(this,c);}else{a.error.call(this,'you must add the "click: function(score, evt) { }" callback.');}a.setTarget.call(this,c,true);});},error:function(c){b(this).html(c);b.error(c);},fill:function(k){var c=this,h=c.stars.length,g=0,d,j,f;for(var e=1;e<=h;e++){d=c.stars.eq(e-1);if(c.opt.iconRange&&c.opt.iconRange.length>g){j=c.opt.iconRange[g];if(c.opt.single){f=(e==k)?(j.on||c.opt.starOn):(j.off||c.opt.starOff);}else{f=(e<=k)?(j.on||c.opt.starOn):(j.off||c.opt.starOff);}if(e<=j.range){d.attr("src",c.opt.path+f);}if(e==j.range){g++;}}else{if(c.opt.single){f=(e==k)?c.opt.starOn:c.opt.starOff;}else{f=(e<=k)?c.opt.starOn:c.opt.starOff;}d.attr("src",c.opt.path+f);}}},fixHint:function(){var c=b(this),e=parseInt(this.score.val(),10),d=this.opt.noRatedMsg;if(!isNaN(e)&&e>0){d=(e<=this.opt.hints.length&&this.opt.hints[e-1]!==null)?this.opt.hints[e-1]:e;}c.data("readonly",true).css("cursor","default").attr("title",d);this.score.attr("readonly","readonly");this.stars.attr("title",d);},getScore:function(){var d=[],c;b(this).each(function(){c=this.score.val();d.push(c?parseFloat(c):undefined);});return(d.length>1)?d:d[0];},readOnly:function(c){return this.each(function(){var d=b(this);if(d.data("readonly")===c){return this;}if(this.cancel){if(c){this.cancel.hide();}else{this.cancel.show();}}if(c){d.unbind();d.children("img").unbind();a.fixHint.call(this);}else{a.bindAction.call(this);a.unfixHint.call(this);}d.data("readonly",c);});},reload:function(){return a.set.call(this,{});},roundStar:function(e){var d=(e-Math.floor(e)).toFixed(2);if(d>this.opt.round.down){var c=this.opt.starOn;if(d<this.opt.round.up&&this.opt.halfShow){c=this.opt.starHalf;}else{if(d<this.opt.round.full){c=this.opt.starOff;}}this.stars.eq(Math.ceil(e)-1).attr("src",this.opt.path+c);}},score:function(){return arguments.length?a.setScore.apply(this,arguments):a.getScore.call(this);},set:function(c){this.each(function(){var d=b(this),f=d.data("settings"),e=d.clone().removeAttr("style").insertBefore(d);d.remove();e.raty(b.extend(f,c));});return b(this.selector);},setScore:function(c){return b(this).each(function(){if(b(this).data("readonly")===true){return this;}a.initialize.call(this,c);a.setTarget.call(this,c,true);});},setTarget:function(e,d){if(this.opt.target){var c=b(this.opt.target);if(c.length==0){a.error.call(this,"target selector invalid or missing!");}var f=e;if(!d||f===undefined){f=this.opt.targetText;}else{if(this.opt.targetType=="hint"){f=(f===null&&this.opt.cancel)?this.opt.cancelHint:this.opt.hints[Math.ceil(f-1)];}else{f=this.opt.precision?parseFloat(f).toFixed(1):parseInt(f,10);}}if(this.opt.targetFormat.indexOf("{score}")<0){a.error.call(this,'template "{score}" missing!');}if(e!==null){f=this.opt.targetFormat.toString().replace("{score}",f);}if(c.is(":input")){c.val(f);}else{c.html(f);}}},showHalf:function(d){var c=(d-Math.floor(d)).toFixed(1);if(c>0&&c<0.6){this.stars.eq(Math.ceil(d)-1).attr("src",this.opt.path+this.opt.starHalf);}},initialize:function(c){c=!c?0:a.between(c,0,this.opt.number);a.fill.call(this,c);if(c>0){if(this.opt.halfShow){a.roundStar.call(this,c);}this.score.val(c);}},unfixHint:function(){for(var c=0;c<this.opt.number;c++){this.stars.eq(c).attr("title",(c<this.opt.hints.length&&this.opt.hints[c]!==null)?this.opt.hints[c]:c);}b(this).data("readonly",false).css("cursor","pointer").removeAttr("title");this.score.attr("readonly","readonly");}};b.fn.raty=function(c){if(a[c]){return a[c].apply(this,Array.prototype.slice.call(arguments,1));}else{if(typeof c==="object"||!c){return a.init.apply(this,arguments);}else{b.error("Method "+c+" does not exist!");}}};b.fn.raty.defaults={cancel:false,cancelHint:"cancel this rating!",cancelOff:"cancel-off.png",cancelOn:"cancel-on.png",cancelPlace:"left",click:undefined,half:false,halfShow:true,hints:["bad","poor","regular","good","gorgeous"],iconRange:undefined,mouseover:undefined,noRatedMsg:"not rated yet",number:5,path:"/assets/img/",precision:false,round:{down:0.25,full:0.6,up:0.76},readOnly:false,score:undefined,scoreName:"score",single:false,size:16,space:true,starHalf:"star-half.png",starOff:"star-off.png",starOn:"star-on.png",target:undefined,targetFormat:"{score}",targetKeep:false,targetText:"",targetType:"hint",width:undefined};})(jQuery);

(function() {
  var iOSCheckbox;
  var __slice = Array.prototype.slice;
  iOSCheckbox = (function() {
    function iOSCheckbox(elem, options) {
      var key, opts, value;
      this.elem = $(elem);
      opts = $.extend({}, iOSCheckbox.defaults, options);
      for (key in opts) {
        value = opts[key];
        this[key] = value;
      }
      this.elem.data(this.dataName, this);
      this.wrapCheckboxWithDivs();
      this.attachEvents();
      this.disableTextSelection();
      if (this.resizeHandle) {
        this.optionallyResize('handle');
      }
      if (this.resizeContainer) {
        this.optionallyResize('container');
      }
      this.initialPosition();
    }
    iOSCheckbox.prototype.isDisabled = function() {
      return this.elem.is(':disabled');
    };
    iOSCheckbox.prototype.wrapCheckboxWithDivs = function() {
      this.elem.wrap("<div class='" + this.containerClass + "' />");
      this.container = this.elem.parent();
      this.offLabel = $("<label class='" + this.labelOffClass + "'>\n  <span>" + this.uncheckedLabel + "</span>\n</label>").appendTo(this.container);
      this.offSpan = this.offLabel.children('span');
      this.onLabel = $("<label class='" + this.labelOnClass + "'>\n  <span>" + this.checkedLabel + "</span>\n</label>").appendTo(this.container);
      this.onSpan = this.onLabel.children('span');
      return this.handle = $("<div class='" + this.handleClass + "'>\n  <div class='" + this.handleRightClass + "'>\n    <div class='" + this.handleCenterClass + "' />\n  </div>\n</div>").appendTo(this.container);
    };
    iOSCheckbox.prototype.disableTextSelection = function() {
      if ($.browser.msie) {
        return $([this.handle, this.offLabel, this.onLabel, this.container]).attr("unselectable", "on");
      }
    };
    iOSCheckbox.prototype._getDimension = function(elem, dimension) {
      if ($.fn.actual != null) {
        return elem.actual(dimension);
      } else {
        return elem[dimension]();
      }
    };
    iOSCheckbox.prototype.optionallyResize = function(mode) {
      var newWidth, offLabelWidth, onLabelWidth;
      onLabelWidth = this._getDimension(this.onLabel, "width");
      offLabelWidth = this._getDimension(this.offLabel, "width");
      if (mode === "container") {
        newWidth = onLabelWidth > offLabelWidth ? onLabelWidth : offLabelWidth;
        newWidth += this._getDimension(this.handle, "width") + this.handleMargin;
        return this.container.css({
          width: newWidth
        });
      } else {
        newWidth = onLabelWidth > offLabelWidth ? onLabelWidth : offLabelWidth;
        return this.handle.css({
          width: newWidth
        });
      }
    };
    iOSCheckbox.prototype.onMouseDown = function(event) {
      var x;
      event.preventDefault();
      if (this.isDisabled()) {
        return;
      }
      x = event.pageX || event.originalEvent.changedTouches[0].pageX;
      iOSCheckbox.currentlyClicking = this.handle;
      iOSCheckbox.dragStartPosition = x;
      return iOSCheckbox.handleLeftOffset = parseInt(this.handle.css('left'), 10) || 0;
    };
    iOSCheckbox.prototype.onDragMove = function(event, x) {
      var newWidth, p;
      if (iOSCheckbox.currentlyClicking !== this.handle) {
        return;
      }
      p = (x + iOSCheckbox.handleLeftOffset - iOSCheckbox.dragStartPosition) / this.rightSide;
      if (p < 0) {
        p = 0;
      }
      if (p > 1) {
        p = 1;
      }
      newWidth = p * this.rightSide;
      this.handle.css({
        left: newWidth
      });
      this.onLabel.css({
        width: newWidth + this.handleRadius
      });
      this.offSpan.css({
        marginRight: -newWidth
      });
      return this.onSpan.css({
        marginLeft: -(1 - p) * this.rightSide
      });
    };
    iOSCheckbox.prototype.onDragEnd = function(event, x) {
      var p;
      if (iOSCheckbox.currentlyClicking !== this.handle) {
        return;
      }
      if (this.isDisabled()) {
        return;
      }
      if (iOSCheckbox.dragging) {
        p = (x - iOSCheckbox.dragStartPosition) / this.rightSide;
        this.elem.prop('checked', p >= 0.5);
      } else {
        this.elem.prop('checked', !this.elem.prop('checked'));
      }
      iOSCheckbox.currentlyClicking = null;
      iOSCheckbox.dragging = null;
      return this.didChange();
    };
    iOSCheckbox.prototype.refresh = function() {
      return this.didChange();
    };
    iOSCheckbox.prototype.didChange = function() {
      var new_left;
      if (typeof this.onChange === "function") {
        this.onChange(this.elem, this.elem.prop('checked'));
      }
      if (this.isDisabled()) {
        this.container.addClass(this.disabledClass);
        return false;
      } else {
        this.container.removeClass(this.disabledClass);
      }
      new_left = this.elem.prop('checked') ? this.rightSide : 0;
      this.handle.animate({
        left: new_left
      }, this.duration);
      this.onLabel.animate({
        width: new_left + this.handleRadius
      }, this.duration);
      this.offSpan.animate({
        marginRight: -new_left
      }, this.duration);
      return this.onSpan.animate({
        marginLeft: new_left - this.rightSide
      }, this.duration);
    };
    iOSCheckbox.prototype.attachEvents = function() {
      var localMouseMove, localMouseUp, self;
      self = this;
      localMouseMove = function(event) {
        return self.onGlobalMove.apply(self, arguments);
      };
      localMouseUp = function(event) {
        self.onGlobalUp.apply(self, arguments);
        $(document).unbind('mousemove touchmove', localMouseMove);
        return $(document).unbind('mouseup touchend', localMouseUp);
      };
      this.elem.change(function() {
        return self.refresh();
      });
      return this.container.bind('mousedown touchstart', function(event) {
        self.onMouseDown.apply(self, arguments);
        $(document).bind('mousemove touchmove', localMouseMove);
        return $(document).bind('mouseup touchend', localMouseUp);
      });
    };
    iOSCheckbox.prototype.initialPosition = function() {
      var containerWidth, offset;
      containerWidth = this._getDimension(this.container, "width");
      this.offLabel.css({
        width: containerWidth - this.containerRadius
      });
      offset = this.containerRadius + 1;
      if ($.browser.msie && $.browser.version < 7) {
        offset -= 3;
      }
      this.rightSide = containerWidth - this._getDimension(this.handle, "width") - offset;
      if (this.elem.is(':checked')) {
        this.handle.css({
          left: this.rightSide
        });
        this.onLabel.css({
          width: this.rightSide + this.handleRadius
        });
        this.offSpan.css({
          marginRight: -this.rightSide
        });
      } else {
        this.onLabel.css({
          width: 0
        });
        this.onSpan.css({
          marginLeft: -this.rightSide
        });
      }
      if (this.isDisabled()) {
        return this.container.addClass(this.disabledClass);
      }
    };
    iOSCheckbox.prototype.onGlobalMove = function(event) {
      var x;
      if (!(!this.isDisabled() && iOSCheckbox.currentlyClicking)) {
        return;
      }
      event.preventDefault();
      x = event.pageX || event.originalEvent.changedTouches[0].pageX;
      if (!iOSCheckbox.dragging && (Math.abs(iOSCheckbox.dragStartPosition - x) > this.dragThreshold)) {
        iOSCheckbox.dragging = true;
      }
      return this.onDragMove(event, x);
    };
    iOSCheckbox.prototype.onGlobalUp = function(event) {
      var x;
      if (!iOSCheckbox.currentlyClicking) {
        return;
      }
      event.preventDefault();
      x = event.pageX || event.originalEvent.changedTouches[0].pageX;
      this.onDragEnd(event, x);
      return false;
    };
    iOSCheckbox.defaults = {
      duration: 200,
      checkedLabel: 'ON',
      uncheckedLabel: 'OFF',
      resizeHandle: true,
      resizeContainer: true,
      disabledClass: 'iPhoneCheckDisabled',
      containerClass: 'iPhoneCheckContainer',
      labelOnClass: 'iPhoneCheckLabelOn',
      labelOffClass: 'iPhoneCheckLabelOff',
      handleClass: 'iPhoneCheckHandle',
      handleCenterClass: 'iPhoneCheckHandleCenter',
      handleRightClass: 'iPhoneCheckHandleRight',
      dragThreshold: 5,
      handleMargin: 15,
      handleRadius: 4,
      containerRadius: 5,
      dataName: "iphoneStyle",
      onChange: function() {}
    };
    return iOSCheckbox;
  })();
  $.iphoneStyle = this.iOSCheckbox = iOSCheckbox;
  $.fn.iphoneStyle = function() {
    var args, checkbox, dataName, existingControl, method, params, _i, _len, _ref, _ref2, _ref3, _ref4;
    args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    dataName = (_ref = (_ref2 = args[0]) != null ? _ref2.dataName : void 0) != null ? _ref : iOSCheckbox.defaults.dataName;
    _ref3 = this.filter(':checkbox');
    for (_i = 0, _len = _ref3.length; _i < _len; _i++) {
      checkbox = _ref3[_i];
      existingControl = $(checkbox).data(dataName);
      if (existingControl != null) {
        method = args[0], params = 2 <= args.length ? __slice.call(args, 1) : [];
        if ((_ref4 = existingControl[method]) != null) {
          _ref4.apply(existingControl, params);
        }
      } else {
        new iOSCheckbox(checkbox, args[0]);
      }
    }
    return this;
  };
  $.fn.iOSCheckbox = function(options) {
    var opts;
    if (options == null) {
      options = {};
    }
    opts = $.extend({}, options, {
      resizeHandle: false,
      disabledClass: 'iOSCheckDisabled',
      containerClass: 'iOSCheckContainer',
      labelOnClass: 'iOSCheckLabelOn',
      labelOffClass: 'iOSCheckLabelOff',
      handleClass: 'iOSCheckHandle',
      handleCenterClass: 'iOSCheckHandleCenter',
      handleRightClass: 'iOSCheckHandleRight',
      dataName: 'iOSCheckbox'
    });
    return this.iphoneStyle(opts);
  };
}).call(this);

(function($)
{
    /**
     * Auto-growing textareas; technique ripped from Facebook
     *
     * http://github.com/jaz303/jquery-grab-bag/tree/master/javascripts/jquery.autogrow-textarea.js
     */
    $.fn.autogrow = function(options)
    {
        return this.filter('textarea').each(function()
        {
            var self                                = this;
            var $self                               = $(self);
            var minHeight                           = $self.height();
            var noFlickerPad                        = $self.hasClass('autogrow-short') ? 0 : parseInt($self.css('lineHeight'));

            var shadow = $('<div></div>').css({
                position:   'absolute',
                top:        -10000,
                left:       -10000,
                width:      $self.width(),
                fontSize:   $self.css('fontSize'),
                fontFamily: $self.css('fontFamily'),
                fontWeight: $self.css('fontWeight'),
                lineHeight: $self.css('lineHeight'),
                resize:     'none'
            }).appendTo(document.body);

            var update = function()
            {
                var times = function(string, number)
                {
                    for (var i=0, r=''; i<number; i++) r += string;
                    return r;
                };

                var val = self.value.replace(/</g, '&lt;')
                                    .replace(/>/g, '&gt;')
                                    .replace(/&/g, '&amp;')
                                    .replace(/\n$/, '<br/>&nbsp;')
                                    .replace(/\n/g, '<br/>')
                                    .replace(/ {2,}/g, function(space){ return times('&nbsp;', space.length - 1) + ' ' });

                shadow.css('width', $self.width());
                shadow.html(val);
                $self.css('height', Math.max(shadow.height() + noFlickerPad, minHeight));
            }

            $self.change(update).keyup(update).keydown(update);
            $(window).resize(update);

            update();
        });
    };
})(jQuery);

/*
Uploadify v3.1.1
Copyright (c) 2012 Reactive Apps, Ronnie Garcia
Released under the MIT License <http://www.opensource.org/licenses/mit-license.php>

SWFUpload: http://www.swfupload.org, http://swfupload.googlecode.com
mmSWFUpload 1.0: Flash upload dialog - http://profandesign.se/swfupload/,  http://www.vinterwebb.se/
SWFUpload is (c) 2006-2007 Lars Huring, Olov Nilzén and Mammon Media and is released under the MIT License:
http://www.opensource.org/licenses/mit-license.php
SWFUpload 2 is (c) 2007-2008 Jake Roberts and is released under the MIT License:
http://www.opensource.org/licenses/mit-license.php

SWFObject v2.2 <http://code.google.com/p/swfobject/> 
is released under the MIT License <http://www.opensource.org/licenses/mit-license.php>
*/
;var swfobject=function(){var aq="undefined",aD="object",ab="Shockwave Flash",X="ShockwaveFlash.ShockwaveFlash",aE="application/x-shockwave-flash",ac="SWFObjectExprInst",ax="onreadystatechange",af=window,aL=document,aB=navigator,aa=false,Z=[aN],aG=[],ag=[],al=[],aJ,ad,ap,at,ak=false,aU=false,aH,an,aI=true,ah=function(){var a=typeof aL.getElementById!=aq&&typeof aL.getElementsByTagName!=aq&&typeof aL.createElement!=aq,e=aB.userAgent.toLowerCase(),c=aB.platform.toLowerCase(),h=c?/win/.test(c):/win/.test(e),j=c?/mac/.test(c):/mac/.test(e),g=/webkit/.test(e)?parseFloat(e.replace(/^.*webkit\/(\d+(\.\d+)?).*$/,"$1")):false,d=!+"\v1",f=[0,0,0],k=null;if(typeof aB.plugins!=aq&&typeof aB.plugins[ab]==aD){k=aB.plugins[ab].description;if(k&&!(typeof aB.mimeTypes!=aq&&aB.mimeTypes[aE]&&!aB.mimeTypes[aE].enabledPlugin)){aa=true;d=false;k=k.replace(/^.*\s+(\S+\s+\S+$)/,"$1");f[0]=parseInt(k.replace(/^(.*)\..*$/,"$1"),10);f[1]=parseInt(k.replace(/^.*\.(.*)\s.*$/,"$1"),10);f[2]=/[a-zA-Z]/.test(k)?parseInt(k.replace(/^.*[a-zA-Z]+(.*)$/,"$1"),10):0;}}else{if(typeof af.ActiveXObject!=aq){try{var i=new ActiveXObject(X);if(i){k=i.GetVariable("$version");if(k){d=true;k=k.split(" ")[1].split(",");f=[parseInt(k[0],10),parseInt(k[1],10),parseInt(k[2],10)];}}}catch(b){}}}return{w3:a,pv:f,wk:g,ie:d,win:h,mac:j};}(),aK=function(){if(!ah.w3){return;}if((typeof aL.readyState!=aq&&aL.readyState=="complete")||(typeof aL.readyState==aq&&(aL.getElementsByTagName("body")[0]||aL.body))){aP();}if(!ak){if(typeof aL.addEventListener!=aq){aL.addEventListener("DOMContentLoaded",aP,false);}if(ah.ie&&ah.win){aL.attachEvent(ax,function(){if(aL.readyState=="complete"){aL.detachEvent(ax,arguments.callee);aP();}});if(af==top){(function(){if(ak){return;}try{aL.documentElement.doScroll("left");}catch(a){setTimeout(arguments.callee,0);return;}aP();})();}}if(ah.wk){(function(){if(ak){return;}if(!/loaded|complete/.test(aL.readyState)){setTimeout(arguments.callee,0);return;}aP();})();}aC(aP);}}();function aP(){if(ak){return;}try{var b=aL.getElementsByTagName("body")[0].appendChild(ar("span"));b.parentNode.removeChild(b);}catch(a){return;}ak=true;var d=Z.length;for(var c=0;c<d;c++){Z[c]();}}function aj(a){if(ak){a();}else{Z[Z.length]=a;}}function aC(a){if(typeof af.addEventListener!=aq){af.addEventListener("load",a,false);}else{if(typeof aL.addEventListener!=aq){aL.addEventListener("load",a,false);}else{if(typeof af.attachEvent!=aq){aM(af,"onload",a);}else{if(typeof af.onload=="function"){var b=af.onload;af.onload=function(){b();a();};}else{af.onload=a;}}}}}function aN(){if(aa){Y();}else{am();}}function Y(){var d=aL.getElementsByTagName("body")[0];var b=ar(aD);b.setAttribute("type",aE);var a=d.appendChild(b);if(a){var c=0;(function(){if(typeof a.GetVariable!=aq){var e=a.GetVariable("$version");if(e){e=e.split(" ")[1].split(",");ah.pv=[parseInt(e[0],10),parseInt(e[1],10),parseInt(e[2],10)];}}else{if(c<10){c++;setTimeout(arguments.callee,10);return;}}d.removeChild(b);a=null;am();})();}else{am();}}function am(){var g=aG.length;if(g>0){for(var h=0;h<g;h++){var c=aG[h].id;var l=aG[h].callbackFn;var a={success:false,id:c};if(ah.pv[0]>0){var i=aS(c);if(i){if(ao(aG[h].swfVersion)&&!(ah.wk&&ah.wk<312)){ay(c,true);if(l){a.success=true;a.ref=av(c);l(a);}}else{if(aG[h].expressInstall&&au()){var e={};e.data=aG[h].expressInstall;e.width=i.getAttribute("width")||"0";e.height=i.getAttribute("height")||"0";if(i.getAttribute("class")){e.styleclass=i.getAttribute("class");}if(i.getAttribute("align")){e.align=i.getAttribute("align");}var f={};var d=i.getElementsByTagName("param");var k=d.length;for(var j=0;j<k;j++){if(d[j].getAttribute("name").toLowerCase()!="movie"){f[d[j].getAttribute("name")]=d[j].getAttribute("value");}}ae(e,f,c,l);}else{aF(i);if(l){l(a);}}}}}else{ay(c,true);if(l){var b=av(c);if(b&&typeof b.SetVariable!=aq){a.success=true;a.ref=b;}l(a);}}}}}function av(b){var d=null;var c=aS(b);if(c&&c.nodeName=="OBJECT"){if(typeof c.SetVariable!=aq){d=c;}else{var a=c.getElementsByTagName(aD)[0];if(a){d=a;}}}return d;}function au(){return !aU&&ao("6.0.65")&&(ah.win||ah.mac)&&!(ah.wk&&ah.wk<312);}function ae(f,d,h,e){aU=true;ap=e||null;at={success:false,id:h};var a=aS(h);if(a){if(a.nodeName=="OBJECT"){aJ=aO(a);ad=null;}else{aJ=a;ad=h;}f.id=ac;if(typeof f.width==aq||(!/%$/.test(f.width)&&parseInt(f.width,10)<310)){f.width="310";}if(typeof f.height==aq||(!/%$/.test(f.height)&&parseInt(f.height,10)<137)){f.height="137";}aL.title=aL.title.slice(0,47)+" - Flash Player Installation";var b=ah.ie&&ah.win?"ActiveX":"PlugIn",c="MMredirectURL="+af.location.toString().replace(/&/g,"%26")+"&MMplayerType="+b+"&MMdoctitle="+aL.title;if(typeof d.flashvars!=aq){d.flashvars+="&"+c;}else{d.flashvars=c;}if(ah.ie&&ah.win&&a.readyState!=4){var g=ar("div");h+="SWFObjectNew";g.setAttribute("id",h);a.parentNode.insertBefore(g,a);a.style.display="none";(function(){if(a.readyState==4){a.parentNode.removeChild(a);}else{setTimeout(arguments.callee,10);}})();}aA(f,d,h);}}function aF(a){if(ah.ie&&ah.win&&a.readyState!=4){var b=ar("div");a.parentNode.insertBefore(b,a);b.parentNode.replaceChild(aO(a),b);a.style.display="none";(function(){if(a.readyState==4){a.parentNode.removeChild(a);}else{setTimeout(arguments.callee,10);}})();}else{a.parentNode.replaceChild(aO(a),a);}}function aO(b){var d=ar("div");if(ah.win&&ah.ie){d.innerHTML=b.innerHTML;}else{var e=b.getElementsByTagName(aD)[0];if(e){var a=e.childNodes;if(a){var f=a.length;for(var c=0;c<f;c++){if(!(a[c].nodeType==1&&a[c].nodeName=="PARAM")&&!(a[c].nodeType==8)){d.appendChild(a[c].cloneNode(true));}}}}}return d;}function aA(e,g,c){var d,a=aS(c);if(ah.wk&&ah.wk<312){return d;}if(a){if(typeof e.id==aq){e.id=c;}if(ah.ie&&ah.win){var f="";for(var i in e){if(e[i]!=Object.prototype[i]){if(i.toLowerCase()=="data"){g.movie=e[i];}else{if(i.toLowerCase()=="styleclass"){f+=' class="'+e[i]+'"';}else{if(i.toLowerCase()!="classid"){f+=" "+i+'="'+e[i]+'"';}}}}}var h="";for(var j in g){if(g[j]!=Object.prototype[j]){h+='<param name="'+j+'" value="'+g[j]+'" />';}}a.outerHTML='<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"'+f+">"+h+"</object>";ag[ag.length]=e.id;d=aS(e.id);}else{var b=ar(aD);b.setAttribute("type",aE);for(var k in e){if(e[k]!=Object.prototype[k]){if(k.toLowerCase()=="styleclass"){b.setAttribute("class",e[k]);}else{if(k.toLowerCase()!="classid"){b.setAttribute(k,e[k]);}}}}for(var l in g){if(g[l]!=Object.prototype[l]&&l.toLowerCase()!="movie"){aQ(b,l,g[l]);}}a.parentNode.replaceChild(b,a);d=b;}}return d;}function aQ(b,d,c){var a=ar("param");a.setAttribute("name",d);a.setAttribute("value",c);b.appendChild(a);}function aw(a){var b=aS(a);if(b&&b.nodeName=="OBJECT"){if(ah.ie&&ah.win){b.style.display="none";(function(){if(b.readyState==4){aT(a);}else{setTimeout(arguments.callee,10);}})();}else{b.parentNode.removeChild(b);}}}function aT(a){var b=aS(a);if(b){for(var c in b){if(typeof b[c]=="function"){b[c]=null;}}b.parentNode.removeChild(b);}}function aS(a){var c=null;try{c=aL.getElementById(a);}catch(b){}return c;}function ar(a){return aL.createElement(a);}function aM(a,c,b){a.attachEvent(c,b);al[al.length]=[a,c,b];}function ao(a){var b=ah.pv,c=a.split(".");c[0]=parseInt(c[0],10);c[1]=parseInt(c[1],10)||0;c[2]=parseInt(c[2],10)||0;return(b[0]>c[0]||(b[0]==c[0]&&b[1]>c[1])||(b[0]==c[0]&&b[1]==c[1]&&b[2]>=c[2]))?true:false;}function az(b,f,a,c){if(ah.ie&&ah.mac){return;}var e=aL.getElementsByTagName("head")[0];if(!e){return;}var g=(a&&typeof a=="string")?a:"screen";if(c){aH=null;an=null;}if(!aH||an!=g){var d=ar("style");d.setAttribute("type","text/css");d.setAttribute("media",g);aH=e.appendChild(d);if(ah.ie&&ah.win&&typeof aL.styleSheets!=aq&&aL.styleSheets.length>0){aH=aL.styleSheets[aL.styleSheets.length-1];}an=g;}if(ah.ie&&ah.win){if(aH&&typeof aH.addRule==aD){aH.addRule(b,f);}}else{if(aH&&typeof aL.createTextNode!=aq){aH.appendChild(aL.createTextNode(b+" {"+f+"}"));}}}function ay(a,c){if(!aI){return;}var b=c?"visible":"hidden";if(ak&&aS(a)){aS(a).style.visibility=b;}else{az("#"+a,"visibility:"+b);}}function ai(b){var a=/[\\\"<>\.;]/;var c=a.exec(b)!=null;return c&&typeof encodeURIComponent!=aq?encodeURIComponent(b):b;}var aR=function(){if(ah.ie&&ah.win){window.attachEvent("onunload",function(){var a=al.length;for(var b=0;b<a;b++){al[b][0].detachEvent(al[b][1],al[b][2]);}var d=ag.length;for(var c=0;c<d;c++){aw(ag[c]);}for(var e in ah){ah[e]=null;}ah=null;for(var f in swfobject){swfobject[f]=null;}swfobject=null;});}}();return{registerObject:function(a,e,c,b){if(ah.w3&&a&&e){var d={};d.id=a;d.swfVersion=e;d.expressInstall=c;d.callbackFn=b;aG[aG.length]=d;ay(a,false);}else{if(b){b({success:false,id:a});}}},getObjectById:function(a){if(ah.w3){return av(a);}},embedSWF:function(k,e,h,f,c,a,b,i,g,j){var d={success:false,id:e};if(ah.w3&&!(ah.wk&&ah.wk<312)&&k&&e&&h&&f&&c){ay(e,false);aj(function(){h+="";f+="";var q={};if(g&&typeof g===aD){for(var o in g){q[o]=g[o];}}q.data=k;q.width=h;q.height=f;var n={};if(i&&typeof i===aD){for(var p in i){n[p]=i[p];}}if(b&&typeof b===aD){for(var l in b){if(typeof n.flashvars!=aq){n.flashvars+="&"+l+"="+b[l];}else{n.flashvars=l+"="+b[l];}}}if(ao(c)){var m=aA(q,n,e);if(q.id==e){ay(e,true);}d.success=true;d.ref=m;}else{if(a&&au()){q.data=a;ae(q,n,e,j);return;}else{ay(e,true);}}if(j){j(d);}});}else{if(j){j(d);}}},switchOffAutoHideShow:function(){aI=false;},ua:ah,getFlashPlayerVersion:function(){return{major:ah.pv[0],minor:ah.pv[1],release:ah.pv[2]};},hasFlashPlayerVersion:ao,createSWF:function(a,b,c){if(ah.w3){return aA(a,b,c);}else{return undefined;}},showExpressInstall:function(b,a,d,c){if(ah.w3&&au()){ae(b,a,d,c);}},removeSWF:function(a){if(ah.w3){aw(a);}},createCSS:function(b,a,c,d){if(ah.w3){az(b,a,c,d);}},addDomLoadEvent:aj,addLoadEvent:aC,getQueryParamValue:function(b){var a=aL.location.search||aL.location.hash;if(a){if(/\?/.test(a)){a=a.split("?")[1];}if(b==null){return ai(a);}var c=a.split("&");for(var d=0;d<c.length;d++){if(c[d].substring(0,c[d].indexOf("="))==b){return ai(c[d].substring((c[d].indexOf("=")+1)));}}}return"";},expressInstallCallback:function(){if(aU){var a=aS(ac);if(a&&aJ){a.parentNode.replaceChild(aJ,a);if(ad){ay(ad,true);if(ah.ie&&ah.win){aJ.style.display="block";}}if(ap){ap(at);}}aU=false;}}};}();var SWFUpload;if(SWFUpload==undefined){SWFUpload=function(b){this.initSWFUpload(b);};}SWFUpload.prototype.initSWFUpload=function(c){try{this.customSettings={};this.settings=c;this.eventQueue=[];this.movieName="SWFUpload_"+SWFUpload.movieCount++;this.movieElement=null;SWFUpload.instances[this.movieName]=this;this.initSettings();this.loadFlash();this.displayDebugInfo();}catch(d){delete SWFUpload.instances[this.movieName];throw d;}};SWFUpload.instances={};SWFUpload.movieCount=0;SWFUpload.version="2.2.0 2009-03-25";SWFUpload.QUEUE_ERROR={QUEUE_LIMIT_EXCEEDED:-100,FILE_EXCEEDS_SIZE_LIMIT:-110,ZERO_BYTE_FILE:-120,INVALID_FILETYPE:-130};SWFUpload.UPLOAD_ERROR={HTTP_ERROR:-200,MISSING_UPLOAD_URL:-210,IO_ERROR:-220,SECURITY_ERROR:-230,UPLOAD_LIMIT_EXCEEDED:-240,UPLOAD_FAILED:-250,SPECIFIED_FILE_ID_NOT_FOUND:-260,FILE_VALIDATION_FAILED:-270,FILE_CANCELLED:-280,UPLOAD_STOPPED:-290};SWFUpload.FILE_STATUS={QUEUED:-1,IN_PROGRESS:-2,ERROR:-3,COMPLETE:-4,CANCELLED:-5};SWFUpload.BUTTON_ACTION={SELECT_FILE:-100,SELECT_FILES:-110,START_UPLOAD:-120};SWFUpload.CURSOR={ARROW:-1,HAND:-2};SWFUpload.WINDOW_MODE={WINDOW:"window",TRANSPARENT:"transparent",OPAQUE:"opaque"};SWFUpload.completeURL=function(e){if(typeof(e)!=="string"||e.match(/^https?:\/\//i)||e.match(/^\//)){return e;}var f=window.location.protocol+"//"+window.location.hostname+(window.location.port?":"+window.location.port:"");var d=window.location.pathname.lastIndexOf("/");if(d<=0){path="/";}else{path=window.location.pathname.substr(0,d)+"/";}return path+e;};SWFUpload.prototype.initSettings=function(){this.ensureDefault=function(c,d){this.settings[c]=(this.settings[c]==undefined)?d:this.settings[c];};this.ensureDefault("upload_url","");this.ensureDefault("preserve_relative_urls",false);this.ensureDefault("file_post_name","Filedata");this.ensureDefault("post_params",{});this.ensureDefault("use_query_string",false);this.ensureDefault("requeue_on_error",false);this.ensureDefault("http_success",[]);this.ensureDefault("assume_success_timeout",0);this.ensureDefault("file_types","*.*");this.ensureDefault("file_types_description","All Files");this.ensureDefault("file_size_limit",0);this.ensureDefault("file_upload_limit",0);this.ensureDefault("file_queue_limit",0);this.ensureDefault("flash_url","swfupload.swf");this.ensureDefault("prevent_swf_caching",true);this.ensureDefault("button_image_url","");this.ensureDefault("button_width",1);this.ensureDefault("button_height",1);this.ensureDefault("button_text","");this.ensureDefault("button_text_style","color: #000000; font-size: 16pt;");this.ensureDefault("button_text_top_padding",0);this.ensureDefault("button_text_left_padding",0);this.ensureDefault("button_action",SWFUpload.BUTTON_ACTION.SELECT_FILES);this.ensureDefault("button_disabled",false);this.ensureDefault("button_placeholder_id","");this.ensureDefault("button_placeholder",null);this.ensureDefault("button_cursor",SWFUpload.CURSOR.ARROW);this.ensureDefault("button_window_mode",SWFUpload.WINDOW_MODE.WINDOW);this.ensureDefault("debug",false);this.settings.debug_enabled=this.settings.debug;this.settings.return_upload_start_handler=this.returnUploadStart;this.ensureDefault("swfupload_loaded_handler",null);this.ensureDefault("file_dialog_start_handler",null);this.ensureDefault("file_queued_handler",null);this.ensureDefault("file_queue_error_handler",null);this.ensureDefault("file_dialog_complete_handler",null);this.ensureDefault("upload_start_handler",null);this.ensureDefault("upload_progress_handler",null);this.ensureDefault("upload_error_handler",null);this.ensureDefault("upload_success_handler",null);this.ensureDefault("upload_complete_handler",null);this.ensureDefault("debug_handler",this.debugMessage);this.ensureDefault("custom_settings",{});this.customSettings=this.settings.custom_settings;if(!!this.settings.prevent_swf_caching){this.settings.flash_url=this.settings.flash_url+(this.settings.flash_url.indexOf("?")<0?"?":"&")+"preventswfcaching="+new Date().getTime();}if(!this.settings.preserve_relative_urls){this.settings.upload_url=SWFUpload.completeURL(this.settings.upload_url);this.settings.button_image_url=SWFUpload.completeURL(this.settings.button_image_url);}delete this.ensureDefault;};SWFUpload.prototype.loadFlash=function(){var d,c;if(document.getElementById(this.movieName)!==null){throw"ID "+this.movieName+" is already in use. The Flash Object could not be added";}d=document.getElementById(this.settings.button_placeholder_id)||this.settings.button_placeholder;if(d==undefined){throw"Could not find the placeholder element: "+this.settings.button_placeholder_id;}c=document.createElement("div");c.innerHTML=this.getFlashHTML();d.parentNode.replaceChild(c.firstChild,d);if(window[this.movieName]==undefined){window[this.movieName]=this.getMovieElement();}};SWFUpload.prototype.getFlashHTML=function(){return['<object id="',this.movieName,'" type="application/x-shockwave-flash" data="',this.settings.flash_url,'" width="',this.settings.button_width,'" height="',this.settings.button_height,'" class="swfupload">','<param name="wmode" value="',this.settings.button_window_mode,'" />','<param name="movie" value="',this.settings.flash_url,'" />','<param name="quality" value="high" />','<param name="menu" value="false" />','<param name="allowScriptAccess" value="always" />','<param name="flashvars" value="'+this.getFlashVars()+'" />',"</object>"].join("");};SWFUpload.prototype.getFlashVars=function(){var c=this.buildParamString();var d=this.settings.http_success.join(",");return["movieName=",encodeURIComponent(this.movieName),"&amp;uploadURL=",encodeURIComponent(this.settings.upload_url),"&amp;useQueryString=",encodeURIComponent(this.settings.use_query_string),"&amp;requeueOnError=",encodeURIComponent(this.settings.requeue_on_error),"&amp;httpSuccess=",encodeURIComponent(d),"&amp;assumeSuccessTimeout=",encodeURIComponent(this.settings.assume_success_timeout),"&amp;params=",encodeURIComponent(c),"&amp;filePostName=",encodeURIComponent(this.settings.file_post_name),"&amp;fileTypes=",encodeURIComponent(this.settings.file_types),"&amp;fileTypesDescription=",encodeURIComponent(this.settings.file_types_description),"&amp;fileSizeLimit=",encodeURIComponent(this.settings.file_size_limit),"&amp;fileUploadLimit=",encodeURIComponent(this.settings.file_upload_limit),"&amp;fileQueueLimit=",encodeURIComponent(this.settings.file_queue_limit),"&amp;debugEnabled=",encodeURIComponent(this.settings.debug_enabled),"&amp;buttonImageURL=",encodeURIComponent(this.settings.button_image_url),"&amp;buttonWidth=",encodeURIComponent(this.settings.button_width),"&amp;buttonHeight=",encodeURIComponent(this.settings.button_height),"&amp;buttonText=",encodeURIComponent(this.settings.button_text),"&amp;buttonTextTopPadding=",encodeURIComponent(this.settings.button_text_top_padding),"&amp;buttonTextLeftPadding=",encodeURIComponent(this.settings.button_text_left_padding),"&amp;buttonTextStyle=",encodeURIComponent(this.settings.button_text_style),"&amp;buttonAction=",encodeURIComponent(this.settings.button_action),"&amp;buttonDisabled=",encodeURIComponent(this.settings.button_disabled),"&amp;buttonCursor=",encodeURIComponent(this.settings.button_cursor)].join("");};SWFUpload.prototype.getMovieElement=function(){if(this.movieElement==undefined){this.movieElement=document.getElementById(this.movieName);}if(this.movieElement===null){throw"Could not find Flash element";}return this.movieElement;};SWFUpload.prototype.buildParamString=function(){var f=this.settings.post_params;var d=[];if(typeof(f)==="object"){for(var e in f){if(f.hasOwnProperty(e)){d.push(encodeURIComponent(e.toString())+"="+encodeURIComponent(f[e].toString()));}}}return d.join("&amp;");};SWFUpload.prototype.destroy=function(){try{this.cancelUpload(null,false);var g=null;g=this.getMovieElement();if(g&&typeof(g.CallFunction)==="unknown"){for(var j in g){try{if(typeof(g[j])==="function"){g[j]=null;}}catch(h){}}try{g.parentNode.removeChild(g);}catch(f){}}window[this.movieName]=null;SWFUpload.instances[this.movieName]=null;delete SWFUpload.instances[this.movieName];this.movieElement=null;this.settings=null;this.customSettings=null;this.eventQueue=null;this.movieName=null;return true;}catch(i){return false;}};SWFUpload.prototype.displayDebugInfo=function(){this.debug(["---SWFUpload Instance Info---\n","Version: ",SWFUpload.version,"\n","Movie Name: ",this.movieName,"\n","Settings:\n","\t","upload_url:               ",this.settings.upload_url,"\n","\t","flash_url:                ",this.settings.flash_url,"\n","\t","use_query_string:         ",this.settings.use_query_string.toString(),"\n","\t","requeue_on_error:         ",this.settings.requeue_on_error.toString(),"\n","\t","http_success:             ",this.settings.http_success.join(", "),"\n","\t","assume_success_timeout:   ",this.settings.assume_success_timeout,"\n","\t","file_post_name:           ",this.settings.file_post_name,"\n","\t","post_params:              ",this.settings.post_params.toString(),"\n","\t","file_types:               ",this.settings.file_types,"\n","\t","file_types_description:   ",this.settings.file_types_description,"\n","\t","file_size_limit:          ",this.settings.file_size_limit,"\n","\t","file_upload_limit:        ",this.settings.file_upload_limit,"\n","\t","file_queue_limit:         ",this.settings.file_queue_limit,"\n","\t","debug:                    ",this.settings.debug.toString(),"\n","\t","prevent_swf_caching:      ",this.settings.prevent_swf_caching.toString(),"\n","\t","button_placeholder_id:    ",this.settings.button_placeholder_id.toString(),"\n","\t","button_placeholder:       ",(this.settings.button_placeholder?"Set":"Not Set"),"\n","\t","button_image_url:         ",this.settings.button_image_url.toString(),"\n","\t","button_width:             ",this.settings.button_width.toString(),"\n","\t","button_height:            ",this.settings.button_height.toString(),"\n","\t","button_text:              ",this.settings.button_text.toString(),"\n","\t","button_text_style:        ",this.settings.button_text_style.toString(),"\n","\t","button_text_top_padding:  ",this.settings.button_text_top_padding.toString(),"\n","\t","button_text_left_padding: ",this.settings.button_text_left_padding.toString(),"\n","\t","button_action:            ",this.settings.button_action.toString(),"\n","\t","button_disabled:          ",this.settings.button_disabled.toString(),"\n","\t","custom_settings:          ",this.settings.custom_settings.toString(),"\n","Event Handlers:\n","\t","swfupload_loaded_handler assigned:  ",(typeof this.settings.swfupload_loaded_handler==="function").toString(),"\n","\t","file_dialog_start_handler assigned: ",(typeof this.settings.file_dialog_start_handler==="function").toString(),"\n","\t","file_queued_handler assigned:       ",(typeof this.settings.file_queued_handler==="function").toString(),"\n","\t","file_queue_error_handler assigned:  ",(typeof this.settings.file_queue_error_handler==="function").toString(),"\n","\t","upload_start_handler assigned:      ",(typeof this.settings.upload_start_handler==="function").toString(),"\n","\t","upload_progress_handler assigned:   ",(typeof this.settings.upload_progress_handler==="function").toString(),"\n","\t","upload_error_handler assigned:      ",(typeof this.settings.upload_error_handler==="function").toString(),"\n","\t","upload_success_handler assigned:    ",(typeof this.settings.upload_success_handler==="function").toString(),"\n","\t","upload_complete_handler assigned:   ",(typeof this.settings.upload_complete_handler==="function").toString(),"\n","\t","debug_handler assigned:             ",(typeof this.settings.debug_handler==="function").toString(),"\n"].join(""));};SWFUpload.prototype.addSetting=function(d,f,e){if(f==undefined){return(this.settings[d]=e);}else{return(this.settings[d]=f);}};SWFUpload.prototype.getSetting=function(b){if(this.settings[b]!=undefined){return this.settings[b];}return"";};SWFUpload.prototype.callFlash=function(functionName,argumentArray){argumentArray=argumentArray||[];var movieElement=this.getMovieElement();var returnValue,returnString;try{returnString=movieElement.CallFunction('<invoke name="'+functionName+'" returntype="javascript">'+__flash__argumentsToXML(argumentArray,0)+"</invoke>");returnValue=eval(returnString);}catch(ex){throw"Call to "+functionName+" failed";}if(returnValue!=undefined&&typeof returnValue.post==="object"){returnValue=this.unescapeFilePostParams(returnValue);}return returnValue;};SWFUpload.prototype.selectFile=function(){this.callFlash("SelectFile");};SWFUpload.prototype.selectFiles=function(){this.callFlash("SelectFiles");};SWFUpload.prototype.startUpload=function(b){this.callFlash("StartUpload",[b]);};SWFUpload.prototype.cancelUpload=function(d,c){if(c!==false){c=true;}this.callFlash("CancelUpload",[d,c]);};SWFUpload.prototype.stopUpload=function(){this.callFlash("StopUpload");};SWFUpload.prototype.getStats=function(){return this.callFlash("GetStats");};SWFUpload.prototype.setStats=function(b){this.callFlash("SetStats",[b]);};SWFUpload.prototype.getFile=function(b){if(typeof(b)==="number"){return this.callFlash("GetFileByIndex",[b]);}else{return this.callFlash("GetFile",[b]);}};SWFUpload.prototype.addFileParam=function(e,d,f){return this.callFlash("AddFileParam",[e,d,f]);};SWFUpload.prototype.removeFileParam=function(d,c){this.callFlash("RemoveFileParam",[d,c]);};SWFUpload.prototype.setUploadURL=function(b){this.settings.upload_url=b.toString();this.callFlash("SetUploadURL",[b]);};SWFUpload.prototype.setPostParams=function(b){this.settings.post_params=b;this.callFlash("SetPostParams",[b]);};SWFUpload.prototype.addPostParam=function(d,c){this.settings.post_params[d]=c;this.callFlash("SetPostParams",[this.settings.post_params]);};SWFUpload.prototype.removePostParam=function(b){delete this.settings.post_params[b];this.callFlash("SetPostParams",[this.settings.post_params]);};SWFUpload.prototype.setFileTypes=function(d,c){this.settings.file_types=d;this.settings.file_types_description=c;this.callFlash("SetFileTypes",[d,c]);};SWFUpload.prototype.setFileSizeLimit=function(b){this.settings.file_size_limit=b;this.callFlash("SetFileSizeLimit",[b]);};SWFUpload.prototype.setFileUploadLimit=function(b){this.settings.file_upload_limit=b;this.callFlash("SetFileUploadLimit",[b]);};SWFUpload.prototype.setFileQueueLimit=function(b){this.settings.file_queue_limit=b;this.callFlash("SetFileQueueLimit",[b]);};SWFUpload.prototype.setFilePostName=function(b){this.settings.file_post_name=b;this.callFlash("SetFilePostName",[b]);};SWFUpload.prototype.setUseQueryString=function(b){this.settings.use_query_string=b;this.callFlash("SetUseQueryString",[b]);};SWFUpload.prototype.setRequeueOnError=function(b){this.settings.requeue_on_error=b;this.callFlash("SetRequeueOnError",[b]);};SWFUpload.prototype.setHTTPSuccess=function(b){if(typeof b==="string"){b=b.replace(" ","").split(",");}this.settings.http_success=b;this.callFlash("SetHTTPSuccess",[b]);};SWFUpload.prototype.setAssumeSuccessTimeout=function(b){this.settings.assume_success_timeout=b;this.callFlash("SetAssumeSuccessTimeout",[b]);};SWFUpload.prototype.setDebugEnabled=function(b){this.settings.debug_enabled=b;this.callFlash("SetDebugEnabled",[b]);};SWFUpload.prototype.setButtonImageURL=function(b){if(b==undefined){b="";}this.settings.button_image_url=b;this.callFlash("SetButtonImageURL",[b]);};SWFUpload.prototype.setButtonDimensions=function(f,e){this.settings.button_width=f;this.settings.button_height=e;var d=this.getMovieElement();if(d!=undefined){d.style.width=f+"px";d.style.height=e+"px";}this.callFlash("SetButtonDimensions",[f,e]);};SWFUpload.prototype.setButtonText=function(b){this.settings.button_text=b;this.callFlash("SetButtonText",[b]);};SWFUpload.prototype.setButtonTextPadding=function(c,d){this.settings.button_text_top_padding=d;this.settings.button_text_left_padding=c;this.callFlash("SetButtonTextPadding",[c,d]);};SWFUpload.prototype.setButtonTextStyle=function(b){this.settings.button_text_style=b;this.callFlash("SetButtonTextStyle",[b]);};SWFUpload.prototype.setButtonDisabled=function(b){this.settings.button_disabled=b;this.callFlash("SetButtonDisabled",[b]);};SWFUpload.prototype.setButtonAction=function(b){this.settings.button_action=b;this.callFlash("SetButtonAction",[b]);};SWFUpload.prototype.setButtonCursor=function(b){this.settings.button_cursor=b;this.callFlash("SetButtonCursor",[b]);};SWFUpload.prototype.queueEvent=function(d,f){if(f==undefined){f=[];}else{if(!(f instanceof Array)){f=[f];}}var e=this;if(typeof this.settings[d]==="function"){this.eventQueue.push(function(){this.settings[d].apply(this,f);});setTimeout(function(){e.executeNextEvent();},0);}else{if(this.settings[d]!==null){throw"Event handler "+d+" is unknown or is not a function";}}};SWFUpload.prototype.executeNextEvent=function(){var b=this.eventQueue?this.eventQueue.shift():null;if(typeof(b)==="function"){b.apply(this);}};SWFUpload.prototype.unescapeFilePostParams=function(l){var j=/[$]([0-9a-f]{4})/i;var i={};var k;if(l!=undefined){for(var h in l.post){if(l.post.hasOwnProperty(h)){k=h;var g;while((g=j.exec(k))!==null){k=k.replace(g[0],String.fromCharCode(parseInt("0x"+g[1],16)));}i[k]=l.post[h];}}l.post=i;}return l;};SWFUpload.prototype.testExternalInterface=function(){try{return this.callFlash("TestExternalInterface");}catch(b){return false;}};SWFUpload.prototype.flashReady=function(){var b=this.getMovieElement();if(!b){this.debug("Flash called back ready but the flash movie can't be found.");return;}this.cleanUp(b);this.queueEvent("swfupload_loaded_handler");};SWFUpload.prototype.cleanUp=function(f){try{if(this.movieElement&&typeof(f.CallFunction)==="unknown"){this.debug("Removing Flash functions hooks (this should only run in IE and should prevent memory leaks)");for(var h in f){try{if(typeof(f[h])==="function"){f[h]=null;}}catch(e){}}}}catch(g){}window.__flash__removeCallback=function(c,b){try{if(c){c[b]=null;}}catch(a){}};};SWFUpload.prototype.fileDialogStart=function(){this.queueEvent("file_dialog_start_handler");};SWFUpload.prototype.fileQueued=function(b){b=this.unescapeFilePostParams(b);this.queueEvent("file_queued_handler",b);};SWFUpload.prototype.fileQueueError=function(e,f,d){e=this.unescapeFilePostParams(e);this.queueEvent("file_queue_error_handler",[e,f,d]);};SWFUpload.prototype.fileDialogComplete=function(d,f,e){this.queueEvent("file_dialog_complete_handler",[d,f,e]);};SWFUpload.prototype.uploadStart=function(b){b=this.unescapeFilePostParams(b);this.queueEvent("return_upload_start_handler",b);};SWFUpload.prototype.returnUploadStart=function(d){var c;if(typeof this.settings.upload_start_handler==="function"){d=this.unescapeFilePostParams(d);c=this.settings.upload_start_handler.call(this,d);}else{if(this.settings.upload_start_handler!=undefined){throw"upload_start_handler must be a function";}}if(c===undefined){c=true;}c=!!c;this.callFlash("ReturnUploadStart",[c]);};SWFUpload.prototype.uploadProgress=function(e,f,d){e=this.unescapeFilePostParams(e);this.queueEvent("upload_progress_handler",[e,f,d]);};SWFUpload.prototype.uploadError=function(e,f,d){e=this.unescapeFilePostParams(e);this.queueEvent("upload_error_handler",[e,f,d]);};SWFUpload.prototype.uploadSuccess=function(d,e,f){d=this.unescapeFilePostParams(d);this.queueEvent("upload_success_handler",[d,e,f]);};SWFUpload.prototype.uploadComplete=function(b){b=this.unescapeFilePostParams(b);this.queueEvent("upload_complete_handler",b);};SWFUpload.prototype.debug=function(b){this.queueEvent("debug_handler",b);};SWFUpload.prototype.debugMessage=function(h){if(this.settings.debug){var f,g=[];if(typeof h==="object"&&typeof h.name==="string"&&typeof h.message==="string"){for(var e in h){if(h.hasOwnProperty(e)){g.push(e+": "+h[e]);}}f=g.join("\n")||"";g=f.split("\n");f="EXCEPTION: "+g.join("\nEXCEPTION: ");SWFUpload.Console.writeLine(f);}else{SWFUpload.Console.writeLine(h);}}};SWFUpload.Console={};SWFUpload.Console.writeLine=function(g){var e,f;try{e=document.getElementById("SWFUpload_Console");if(!e){f=document.createElement("form");document.getElementsByTagName("body")[0].appendChild(f);e=document.createElement("textarea");e.id="SWFUpload_Console";e.style.fontFamily="monospace";e.setAttribute("wrap","off");e.wrap="off";e.style.overflow="auto";e.style.width="700px";e.style.height="350px";e.style.margin="5px";f.appendChild(e);}e.value+=g+"\n";e.scrollTop=e.scrollHeight-e.clientHeight;}catch(h){alert("Exception: "+h.name+" Message: "+h.message);}};(function(c){var b={init:function(d,e){return this.each(function(){var n=c(this);var m=n.clone();var j=c.extend({id:n.attr("id"),swf:"uploadify.swf",uploader:"uploadify.php",auto:true,buttonClass:"",buttonCursor:"hand",buttonImage:null,buttonText:"SELECT FILES",checkExisting:false,debug:false,fileObjName:"Filedata",fileSizeLimit:0,fileTypeDesc:"All Files",fileTypeExts:"*.*",height:30,method:"post",multi:true,formData:{},preventCaching:true,progressData:"percentage",queueID:false,queueSizeLimit:999,removeCompleted:true,removeTimeout:3,requeueErrors:false,successTimeout:30,uploadLimit:0,width:120,overrideEvents:[]},d);var g={assume_success_timeout:j.successTimeout,button_placeholder_id:j.id,button_width:j.width,button_height:j.height,button_text:null,button_text_style:null,button_text_top_padding:0,button_text_left_padding:0,button_action:(j.multi?SWFUpload.BUTTON_ACTION.SELECT_FILES:SWFUpload.BUTTON_ACTION.SELECT_FILE),button_disabled:false,button_cursor:(j.buttonCursor=="arrow"?SWFUpload.CURSOR.ARROW:SWFUpload.CURSOR.HAND),button_window_mode:SWFUpload.WINDOW_MODE.TRANSPARENT,debug:j.debug,requeue_on_error:j.requeueErrors,file_post_name:j.fileObjName,file_size_limit:j.fileSizeLimit,file_types:j.fileTypeExts,file_types_description:j.fileTypeDesc,file_queue_limit:j.queueSizeLimit,file_upload_limit:j.uploadLimit,flash_url:j.swf,prevent_swf_caching:j.preventCaching,post_params:j.formData,upload_url:j.uploader,use_query_string:(j.method=="get"),file_dialog_complete_handler:a.onDialogClose,file_dialog_start_handler:a.onDialogOpen,file_queued_handler:a.onSelect,file_queue_error_handler:a.onSelectError,swfupload_loaded_handler:j.onSWFReady,upload_complete_handler:a.onUploadComplete,upload_error_handler:a.onUploadError,upload_progress_handler:a.onUploadProgress,upload_start_handler:a.onUploadStart,upload_success_handler:a.onUploadSuccess};if(e){g=c.extend(g,e);}g=c.extend(g,j);var o=swfobject.getFlashPlayerVersion();var h=(o.major>=9);if(h){window["uploadify_"+j.id]=new SWFUpload(g);var i=window["uploadify_"+j.id];n.data("uploadify",i);var l=c("<div />",{id:j.id,"class":"uploadify",css:{height:j.height+"px",width:j.width+"px"}});c("#"+i.movieName).wrap(l);l=c("#"+j.id);l.data("uploadify",i);var f=c("<div />",{id:j.id+"-button","class":"uploadify-button "+j.buttonClass});if(j.buttonImage){f.css({"background-image":"url('"+j.buttonImage+"')","text-indent":"-9999px"});}f.html('<span class="uploadify-button-text">'+j.buttonText+"</span>").css({height:j.height+"px","line-height":j.height+"px",width:j.width+"px"});l.append(f);c("#"+i.movieName).css({position:"absolute","z-index":1});if(!j.queueID){var k=c("<div />",{id:j.id+"-queue","class":"uploadify-queue"});l.after(k);i.settings.queueID=j.id+"-queue";i.settings.defaultQueue=true;}i.queueData={files:{},filesSelected:0,filesQueued:0,filesReplaced:0,filesCancelled:0,filesErrored:0,uploadsSuccessful:0,uploadsErrored:0,averageSpeed:0,queueLength:0,queueSize:0,uploadSize:0,queueBytesUploaded:0,uploadQueue:[],errorMsg:"Some files were not added to the queue:"};i.original=m;i.wrapper=l;i.button=f;i.queue=k;if(j.onInit){j.onInit.call(n,i);}}else{if(j.onFallback){j.onFallback.call(n);}}});},cancel:function(d,f){var e=arguments;this.each(function(){var l=c(this),i=l.data("uploadify"),j=i.settings,h=-1;if(e[0]){if(e[0]=="*"){var g=i.queueData.queueLength;c("#"+j.queueID).find(".uploadify-queue-item").each(function(){h++;if(e[1]===true){i.cancelUpload(c(this).attr("id"),false);}else{i.cancelUpload(c(this).attr("id"));}c(this).find(".data").removeClass("data").html(" - Cancelled");c(this).find(".uploadify-progress-bar").remove();c(this).delay(1000+100*h).fadeOut(500,function(){c(this).remove();});});i.queueData.queueSize=0;i.queueData.queueLength=0;if(j.onClearQueue){j.onClearQueue.call(l,g);}}else{for(var m=0;m<e.length;m++){i.cancelUpload(e[m]);c("#"+e[m]).find(".data").removeClass("data").html(" - Cancelled");c("#"+e[m]).find(".uploadify-progress-bar").remove();c("#"+e[m]).delay(1000+100*m).fadeOut(500,function(){c(this).remove();});}}}else{var k=c("#"+j.queueID).find(".uploadify-queue-item").get(0);$item=c(k);i.cancelUpload($item.attr("id"));$item.find(".data").removeClass("data").html(" - Cancelled");$item.find(".uploadify-progress-bar").remove();$item.delay(1000).fadeOut(500,function(){c(this).remove();});}});},destroy:function(){this.each(function(){var f=c(this),d=f.data("uploadify"),e=d.settings;d.destroy();if(e.defaultQueue){c("#"+e.queueID).remove();}c("#"+e.id).replaceWith(d.original);if(e.onDestroy){e.onDestroy.call(this);}delete d;});},disable:function(d){this.each(function(){var g=c(this),e=g.data("uploadify"),f=e.settings;if(d){e.button.addClass("disabled");if(f.onDisable){f.onDisable.call(this);}}else{e.button.removeClass("disabled");if(f.onEnable){f.onEnable.call(this);}}e.setButtonDisabled(d);});},settings:function(e,g,h){var d=arguments;var f=g;this.each(function(){var k=c(this),i=k.data("uploadify"),j=i.settings;if(typeof(d[0])=="object"){for(var l in g){setData(l,g[l]);}}if(d.length===1){f=j[e];}else{switch(e){case"uploader":i.setUploadURL(g);break;case"formData":if(!h){g=c.extend(j.formData,g);}i.setPostParams(j.formData);break;case"method":if(g=="get"){i.setUseQueryString(true);}else{i.setUseQueryString(false);}break;case"fileObjName":i.setFilePostName(g);break;case"fileTypeExts":i.setFileTypes(g,j.fileTypeDesc);break;case"fileTypeDesc":i.setFileTypes(j.fileTypeExts,g);break;case"fileSizeLimit":i.setFileSizeLimit(g);break;case"uploadLimit":i.setFileUploadLimit(g);break;case"queueSizeLimit":i.setFileQueueLimit(g);break;case"buttonImage":i.button.css("background-image",settingValue);break;case"buttonCursor":if(g=="arrow"){i.setButtonCursor(SWFUpload.CURSOR.ARROW);}else{i.setButtonCursor(SWFUpload.CURSOR.HAND);}break;case"buttonText":c("#"+j.id+"-button").find(".uploadify-button-text").html(g);break;case"width":i.setButtonDimensions(g,j.height);break;case"height":i.setButtonDimensions(j.width,g);break;case"multi":if(g){i.setButtonAction(SWFUpload.BUTTON_ACTION.SELECT_FILES);}else{i.setButtonAction(SWFUpload.BUTTON_ACTION.SELECT_FILE);}break;}j[e]=g;}});if(d.length===1){return f;}},stop:function(){this.each(function(){var e=c(this),d=e.data("uploadify");d.queueData.averageSpeed=0;d.queueData.uploadSize=0;d.queueData.bytesUploaded=0;d.queueData.uploadQueue=[];d.stopUpload();});},upload:function(){var d=arguments;this.each(function(){var f=c(this),e=f.data("uploadify");e.queueData.averageSpeed=0;e.queueData.uploadSize=0;e.queueData.bytesUploaded=0;e.queueData.uploadQueue=[];if(d[0]){if(d[0]=="*"){e.queueData.uploadSize=e.queueData.queueSize;e.queueData.uploadQueue.push("*");e.startUpload();}else{for(var g=0;g<d.length;g++){e.queueData.uploadSize+=e.queueData.files[d[g]].size;e.queueData.uploadQueue.push(d[g]);}e.startUpload(e.queueData.uploadQueue.shift());}}else{e.startUpload();}});}};var a={onDialogOpen:function(){var d=this.settings;this.queueData.errorMsg="Some files were not added to the queue:";this.queueData.filesReplaced=0;this.queueData.filesCancelled=0;if(d.onDialogOpen){d.onDialogOpen.call(this);}},onDialogClose:function(d,f,g){var e=this.settings;this.queueData.filesErrored=d-f;this.queueData.filesSelected=d;this.queueData.filesQueued=f-this.queueData.filesCancelled;this.queueData.queueLength=g;if(c.inArray("onDialogClose",e.overrideEvents)<0){if(this.queueData.filesErrored>0){alert(this.queueData.errorMsg);}}if(e.onDialogClose){e.onDialogClose.call(this,this.queueData);}if(e.auto){c("#"+e.id).uploadify("upload","*");}},onSelect:function(g){var h=this.settings;var e={};for(var f in this.queueData.files){e=this.queueData.files[f];if(e.uploaded!=true&&e.name==g.name){var d=confirm('The file named "'+g.name+'" is already in the queue.\nDo you want to replace the existing item in the queue?');if(!d){this.cancelUpload(g.id);this.queueData.filesCancelled++;return false;}else{c("#"+e.id).remove();this.cancelUpload(e.id);this.queueData.filesReplaced++;}}}var i=Math.round(g.size/1024);var l="KB";if(i>1000){i=Math.round(i/1000);l="MB";}var k=i.toString().split(".");i=k[0];if(k.length>1){i+="."+k[1].substr(0,2);}i+=l;var j=g.name;if(j.length>25){j=j.substr(0,25)+"...";}if(c.inArray("onSelect",h.overrideEvents)<0){c("#"+h.queueID).append('<div id="'+g.id+'" class="uploadify-queue-item">					<div class="cancel">						<a href="javascript:$(\'#'+h.id+"').uploadify('cancel', '"+g.id+'\')">X</a>					</div>					<span class="fileName">'+j+" ("+i+')</span><span class="data"></span>					<div class="uploadify-progress">						<div class="uploadify-progress-bar"><!--Progress Bar--></div>					</div>				</div>');}this.queueData.queueSize+=g.size;this.queueData.files[g.id]=g;if(h.onSelect){h.onSelect.apply(this,arguments);}},onSelectError:function(d,g,f){var e=this.settings;if(c.inArray("onSelectError",e.overrideEvents)<0){switch(g){case SWFUpload.QUEUE_ERROR.QUEUE_LIMIT_EXCEEDED:if(e.queueSizeLimit>f){this.queueData.errorMsg+="\nThe number of files selected exceeds the remaining upload limit ("+f+").";}else{this.queueData.errorMsg+="\nThe number of files selected exceeds the queue size limit ("+e.queueSizeLimit+").";}break;case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:this.queueData.errorMsg+='\nThe file "'+d.name+'" exceeds the size limit ('+e.fileSizeLimit+").";break;case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:this.queueData.errorMsg+='\nThe file "'+d.name+'" is empty.';break;case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:this.queueData.errorMsg+='\nThe file "'+d.name+'" is not an accepted file type ('+e.fileTypeDesc+").";break;}}if(g!=SWFUpload.QUEUE_ERROR.QUEUE_LIMIT_EXCEEDED){delete this.queueData.files[d.id];}if(e.onSelectError){e.onSelectError.apply(this,arguments);}},onQueueComplete:function(){if(this.settings.onQueueComplete){this.settings.onQueueComplete.call(this,this.settings.queueData);}},onUploadComplete:function(f){var g=this.settings,d=this;var e=this.getStats();this.queueData.queueLength=e.files_queued;if(this.queueData.uploadQueue[0]=="*"){if(this.queueData.queueLength>0){this.startUpload();}else{this.queueData.uploadQueue=[];if(g.onQueueComplete){g.onQueueComplete.call(this,this.queueData);}}}else{if(this.queueData.uploadQueue.length>0){this.startUpload(this.queueData.uploadQueue.shift());}else{this.queueData.uploadQueue=[];if(g.onQueueComplete){g.onQueueComplete.call(this,this.queueData);}}}if(c.inArray("onUploadComplete",g.overrideEvents)<0){if(g.removeCompleted){switch(f.filestatus){case SWFUpload.FILE_STATUS.COMPLETE:setTimeout(function(){if(c("#"+f.id)){d.queueData.queueSize-=f.size;d.queueData.queueLength-=1;delete d.queueData.files[f.id];c("#"+f.id).fadeOut(500,function(){c(this).remove();});}},g.removeTimeout*1000);break;case SWFUpload.FILE_STATUS.ERROR:if(!g.requeueErrors){setTimeout(function(){if(c("#"+f.id)){d.queueData.queueSize-=f.size;d.queueData.queueLength-=1;delete d.queueData.files[f.id];c("#"+f.id).fadeOut(500,function(){c(this).remove();});}},g.removeTimeout*1000);}break;}}else{f.uploaded=true;}}if(g.onUploadComplete){g.onUploadComplete.call(this,f);}},onUploadError:function(e,i,h){var f=this.settings;var g="Error";switch(i){case SWFUpload.UPLOAD_ERROR.HTTP_ERROR:g="HTTP Error ("+h+")";break;case SWFUpload.UPLOAD_ERROR.MISSING_UPLOAD_URL:g="Missing Upload URL";break;case SWFUpload.UPLOAD_ERROR.IO_ERROR:g="IO Error";break;case SWFUpload.UPLOAD_ERROR.SECURITY_ERROR:g="Security Error";break;case SWFUpload.UPLOAD_ERROR.UPLOAD_LIMIT_EXCEEDED:alert("The upload limit has been reached ("+h+").");g="Exceeds Upload Limit";break;case SWFUpload.UPLOAD_ERROR.UPLOAD_FAILED:g="Failed";break;case SWFUpload.UPLOAD_ERROR.SPECIFIED_FILE_ID_NOT_FOUND:break;case SWFUpload.UPLOAD_ERROR.FILE_VALIDATION_FAILED:g="Validation Error";break;case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:g="Cancelled";this.queueData.queueSize-=e.size;this.queueData.queueLength-=1;if(e.status==SWFUpload.FILE_STATUS.IN_PROGRESS||c.inArray(e.id,this.queueData.uploadQueue)>=0){this.queueData.uploadSize-=e.size;}if(f.onCancel){f.onCancel.call(this,e);}delete this.queueData.files[e.id];break;case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:g="Stopped";break;}if(c.inArray("onUploadError",f.overrideEvents)<0){if(i!=SWFUpload.UPLOAD_ERROR.FILE_CANCELLED&&i!=SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED){c("#"+e.id).addClass("uploadify-error");}c("#"+e.id).find(".uploadify-progress-bar").css("width","1px");if(i!=SWFUpload.UPLOAD_ERROR.SPECIFIED_FILE_ID_NOT_FOUND&&e.status!=SWFUpload.FILE_STATUS.COMPLETE){c("#"+e.id).find(".data").html(" - "+g);}}var d=this.getStats();this.queueData.uploadsErrored=d.upload_errors;if(f.onUploadError){f.onUploadError.call(this,e,i,h,g);}},onUploadProgress:function(g,m,j){var h=this.settings;var e=new Date();var n=e.getTime();var k=n-this.timer;if(k>500){this.timer=n;}var i=m-this.bytesLoaded;this.bytesLoaded=m;var d=this.queueData.queueBytesUploaded+m;var p=Math.round(m/j*100);var o="KB/s";var l=0;var f=(i/1024)/(k/1000);f=Math.floor(f*10)/10;if(this.queueData.averageSpeed>0){this.queueData.averageSpeed=Math.floor((this.queueData.averageSpeed+f)/2);}else{this.queueData.averageSpeed=Math.floor(f);}if(f>1000){l=(f*0.001);this.queueData.averageSpeed=Math.floor(l);o="MB/s";}if(c.inArray("onUploadProgress",h.overrideEvents)<0){if(h.progressData=="percentage"){c("#"+g.id).find(".data").html(" - "+p+"%");}else{if(h.progressData=="speed"&&k>500){c("#"+g.id).find(".data").html(" - "+this.queueData.averageSpeed+o);}}c("#"+g.id).find(".uploadify-progress-bar").css("width",p+"%");}if(h.onUploadProgress){h.onUploadProgress.call(this,g,m,j,d,this.queueData.uploadSize);}},onUploadStart:function(d){var e=this.settings;var f=new Date();this.timer=f.getTime();this.bytesLoaded=0;if(this.queueData.uploadQueue.length==0){this.queueData.uploadSize=d.size;}if(e.checkExisting){c.ajax({type:"POST",async:false,url:e.checkExisting,data:{filename:d.name},success:function(h){if(h==1){var g=confirm('A file with the name "'+d.name+'" already exists on the server.\nWould you like to replace the existing file?');if(!g){this.cancelUpload(d.id);c("#"+d.id).remove();if(this.queueData.uploadQueue.length>0&&this.queueData.queueLength>0){if(this.queueData.uploadQueue[0]=="*"){this.startUpload();}else{this.startUpload(this.queueData.uploadQueue.shift());}}}}}});}if(e.onUploadStart){e.onUploadStart.call(this,d);}},onUploadSuccess:function(f,h,d){var g=this.settings;var e=this.getStats();this.queueData.uploadsSuccessful=e.successful_uploads;this.queueData.queueBytesUploaded+=f.size;if(c.inArray("onUploadSuccess",g.overrideEvents)<0){c("#"+f.id).find(".data").html(" - Complete");}if(g.onUploadSuccess){g.onUploadSuccess.call(this,f,h,d);}}};c.fn.uploadify=function(d){if(b[d]){return b[d].apply(this,Array.prototype.slice.call(arguments,1));}else{if(typeof d==="object"||!d){return b.init.apply(this,arguments);}else{c.error("The method "+d+" does not exist in $.uploadify");}}};})($);
window.JSON||(window.JSON={}),function(){function f(a){return a<10?"0"+a:a}function quote(a){return escapable.lastIndex=0,escapable.test(a)?'"'+a.replace(escapable,function(a){var b=meta[a];return typeof b=="string"?b:"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)})+'"':'"'+a+'"'}function str(a,b){var c,d,e,f,g=gap,h,i=b[a];i&&typeof i=="object"&&typeof i.toJSON=="function"&&(i=i.toJSON(a)),typeof rep=="function"&&(i=rep.call(b,a,i));switch(typeof i){case"string":return quote(i);case"number":return isFinite(i)?String(i):"null";case"boolean":case"null":return String(i);case"object":if(!i)return"null";gap+=indent,h=[];if(Object.prototype.toString.apply(i)==="[object Array]"){f=i.length;for(c=0;c<f;c+=1)h[c]=str(c,i)||"null";return e=h.length===0?"[]":gap?"[\n"+gap+h.join(",\n"+gap)+"\n"+g+"]":"["+h.join(",")+"]",gap=g,e}if(rep&&typeof rep=="object"){f=rep.length;for(c=0;c<f;c+=1)d=rep[c],typeof d=="string"&&(e=str(d,i),e&&h.push(quote(d)+(gap?": ":":")+e))}else for(d in i)Object.hasOwnProperty.call(i,d)&&(e=str(d,i),e&&h.push(quote(d)+(gap?": ":":")+e));return e=h.length===0?"{}":gap?"{\n"+gap+h.join(",\n"+gap)+"\n"+g+"}":"{"+h.join(",")+"}",gap=g,e}}"use strict",typeof Date.prototype.toJSON!="function"&&(Date.prototype.toJSON=function(a){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+f(this.getUTCMonth()+1)+"-"+f(this.getUTCDate())+"T"+f(this.getUTCHours())+":"+f(this.getUTCMinutes())+":"+f(this.getUTCSeconds())+"Z":null},String.prototype.toJSON=Number.prototype.toJSON=Boolean.prototype.toJSON=function(a){return this.valueOf()});var JSON=window.JSON,cx=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,escapable=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,gap,indent,meta={"\b":"\\b","\t":"\\t","\n":"\\n","\f":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"},rep;typeof JSON.stringify!="function"&&(JSON.stringify=function(a,b,c){var d;gap="",indent="";if(typeof c=="number")for(d=0;d<c;d+=1)indent+=" ";else typeof c=="string"&&(indent=c);rep=b;if(!b||typeof b=="function"||typeof b=="object"&&typeof b.length=="number")return str("",{"":a});throw new Error("JSON.stringify")}),typeof JSON.parse!="function"&&(JSON.parse=function(text,reviver){function walk(a,b){var c,d,e=a[b];if(e&&typeof e=="object")for(c in e)Object.hasOwnProperty.call(e,c)&&(d=walk(e,c),d!==undefined?e[c]=d:delete e[c]);return reviver.call(a,b,e)}var j;text=String(text),cx.lastIndex=0,cx.test(text)&&(text=text.replace(cx,function(a){return"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)}));if(/^[\],:{}\s]*$/.test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:\s*\[)+/g,"")))return j=eval("("+text+")"),typeof reviver=="function"?walk({"":j},""):j;throw new SyntaxError("JSON.parse")})}(),function(a,b){"use strict";var c=a.History=a.History||{},d=a.jQuery;if(typeof c.Adapter!="undefined")throw new Error("History.js Adapter has already been loaded...");c.Adapter={bind:function(a,b,c){d(a).bind(b,c)},trigger:function(a,b,c){d(a).trigger(b,c)},extractEventData:function(a,c,d){var e=c&&c.originalEvent&&c.originalEvent[a]||d&&d[a]||b;return e},onDomLoad:function(a){d(a)}},typeof c.init!="undefined"&&c.init()}(window),function(a,b){"use strict";var c=a.document,d=a.setTimeout||d,e=a.clearTimeout||e,f=a.setInterval||f,g=a.History=a.History||{};if(typeof g.initHtml4!="undefined")throw new Error("History.js HTML4 Support has already been loaded...");g.initHtml4=function(){if(typeof g.initHtml4.initialized!="undefined")return!1;g.initHtml4.initialized=!0,g.enabled=!0,g.savedHashes=[],g.isLastHash=function(a){var b=g.getHashByIndex(),c;return c=a===b,c},g.saveHash=function(a){return g.isLastHash(a)?!1:(g.savedHashes.push(a),!0)},g.getHashByIndex=function(a){var b=null;return typeof a=="undefined"?b=g.savedHashes[g.savedHashes.length-1]:a<0?b=g.savedHashes[g.savedHashes.length+a]:b=g.savedHashes[a],b},g.discardedHashes={},g.discardedStates={},g.discardState=function(a,b,c){var d=g.getHashByState(a),e;return e={discardedState:a,backState:c,forwardState:b},g.discardedStates[d]=e,!0},g.discardHash=function(a,b,c){var d={discardedHash:a,backState:c,forwardState:b};return g.discardedHashes[a]=d,!0},g.discardedState=function(a){var b=g.getHashByState(a),c;return c=g.discardedStates[b]||!1,c},g.discardedHash=function(a){var b=g.discardedHashes[a]||!1;return b},g.recycleState=function(a){var b=g.getHashByState(a);return g.discardedState(a)&&delete g.discardedStates[b],!0},g.emulated.hashChange&&(g.hashChangeInit=function(){g.checkerFunction=null;var b="",d,e,h,i;return g.isInternetExplorer()?(d="historyjs-iframe",e=c.createElement("iframe"),e.setAttribute("id",d),e.style.display="none",c.body.appendChild(e),e.contentWindow.document.open(),e.contentWindow.document.close(),h="",i=!1,g.checkerFunction=function(){if(i)return!1;i=!0;var c=g.getHash()||"",d=g.unescapeHash(e.contentWindow.document.location.hash)||"";return c!==b?(b=c,d!==c&&(h=d=c,e.contentWindow.document.open(),e.contentWindow.document.close(),e.contentWindow.document.location.hash=g.escapeHash(c)),g.Adapter.trigger(a,"hashchange")):d!==h&&(h=d,g.setHash(d,!1)),i=!1,!0}):g.checkerFunction=function(){var c=g.getHash();return c!==b&&(b=c,g.Adapter.trigger(a,"hashchange")),!0},g.intervalList.push(f(g.checkerFunction,g.options.hashChangeInterval)),!0},g.Adapter.onDomLoad(g.hashChangeInit)),g.emulated.pushState&&(g.onHashChange=function(b){var d=b&&b.newURL||c.location.href,e=g.getHashByUrl(d),f=null,h=null,i=null,j;return g.isLastHash(e)?(g.busy(!1),!1):(g.doubleCheckComplete(),g.saveHash(e),e&&g.isTraditionalAnchor(e)?(g.Adapter.trigger(a,"anchorchange"),g.busy(!1),!1):(f=g.extractState(g.getFullUrl(e||c.location.href,!1),!0),g.isLastSavedState(f)?(g.busy(!1),!1):(h=g.getHashByState(f),j=g.discardedState(f),j?(g.getHashByIndex(-2)===g.getHashByState(j.forwardState)?g.back(!1):g.forward(!1),!1):(g.pushState(f.data,f.title,f.url,!1),!0))))},g.Adapter.bind(a,"hashchange",g.onHashChange),g.pushState=function(b,d,e,f){if(g.getHashByUrl(e))throw new Error("History.js does not support states with fragement-identifiers (hashes/anchors).");if(f!==!1&&g.busy())return g.pushQueue({scope:g,callback:g.pushState,args:arguments,queue:f}),!1;g.busy(!0);var h=g.createStateObject(b,d,e),i=g.getHashByState(h),j=g.getState(!1),k=g.getHashByState(j),l=g.getHash();return g.storeState(h),g.expectedStateId=h.id,g.recycleState(h),g.setTitle(h),i===k?(g.busy(!1),!1):i!==l&&i!==g.getShortUrl(c.location.href)?(g.setHash(i,!1),!1):(g.saveState(h),g.Adapter.trigger(a,"statechange"),g.busy(!1),!0)},g.replaceState=function(a,b,c,d){if(g.getHashByUrl(c))throw new Error("History.js does not support states with fragement-identifiers (hashes/anchors).");if(d!==!1&&g.busy())return g.pushQueue({scope:g,callback:g.replaceState,args:arguments,queue:d}),!1;g.busy(!0);var e=g.createStateObject(a,b,c),f=g.getState(!1),h=g.getStateByIndex(-2);return g.discardState(f,e,h),g.pushState(e.data,e.title,e.url,!1),!0}),g.emulated.pushState&&g.getHash()&&!g.emulated.hashChange&&g.Adapter.onDomLoad(function(){g.Adapter.trigger(a,"hashchange")})},typeof g.init!="undefined"&&g.init()}(window),function(a,b){"use strict";var c=a.console||b,d=a.document,e=a.navigator,f=a.sessionStorage||!1,g=a.setTimeout,h=a.clearTimeout,i=a.setInterval,j=a.clearInterval,k=a.JSON,l=a.alert,m=a.History=a.History||{},n=a.history;k.stringify=k.stringify||k.encode,k.parse=k.parse||k.decode;if(typeof m.init!="undefined")throw new Error("History.js Core has already been loaded...");m.init=function(){return typeof m.Adapter=="undefined"?!1:(typeof m.initCore!="undefined"&&m.initCore(),typeof m.initHtml4!="undefined"&&m.initHtml4(),!0)},m.initCore=function(){if(typeof m.initCore.initialized!="undefined")return!1;m.initCore.initialized=!0,m.options=m.options||{},m.options.hashChangeInterval=m.options.hashChangeInterval||100,m.options.safariPollInterval=m.options.safariPollInterval||500,m.options.doubleCheckInterval=m.options.doubleCheckInterval||500,m.options.storeInterval=m.options.storeInterval||1e3,m.options.busyDelay=m.options.busyDelay||250,m.options.debug=m.options.debug||!1,m.options.initialTitle=m.options.initialTitle||d.title,m.intervalList=[],m.clearAllIntervals=function(){var a,b=m.intervalList;if(typeof b!="undefined"&&b!==null){for(a=0;a<b.length;a++)j(b[a]);m.intervalList=null}},m.debug=function(){(m.options.debug||!1)&&m.log.apply(m,arguments)},m.log=function(){var a=typeof c!="undefined"&&typeof c.log!="undefined"&&typeof c.log.apply!="undefined",b=d.getElementById("log"),e,f,g,h,i;a?(h=Array.prototype.slice.call(arguments),e=h.shift(),typeof c.debug!="undefined"?c.debug.apply(c,[e,h]):c.log.apply(c,[e,h])):e="\n"+arguments[0]+"\n";for(f=1,g=arguments.length;f<g;++f){i=arguments[f];if(typeof i=="object"&&typeof k!="undefined")try{i=k.stringify(i)}catch(j){}e+="\n"+i+"\n"}return b?(b.value+=e+"\n-----\n",b.scrollTop=b.scrollHeight-b.clientHeight):a||l(e),!0},m.getInternetExplorerMajorVersion=function(){var a=m.getInternetExplorerMajorVersion.cached=typeof m.getInternetExplorerMajorVersion.cached!="undefined"?m.getInternetExplorerMajorVersion.cached:function(){var a=3,b=d.createElement("div"),c=b.getElementsByTagName("i");while((b.innerHTML="<!--[if gt IE "+ ++a+"]><i></i><![endif]-->")&&c[0]);return a>4?a:!1}();return a},m.isInternetExplorer=function(){var a=m.isInternetExplorer.cached=typeof m.isInternetExplorer.cached!="undefined"?m.isInternetExplorer.cached:Boolean(m.getInternetExplorerMajorVersion());return a},m.emulated={pushState:!Boolean(a.history&&a.history.pushState&&a.history.replaceState&&!/ Mobile\/([1-7][a-z]|(8([abcde]|f(1[0-8]))))/i.test(e.userAgent)&&!/AppleWebKit\/5([0-2]|3[0-2])/i.test(e.userAgent)),hashChange:Boolean(!("onhashchange"in a||"onhashchange"in d)||m.isInternetExplorer()&&m.getInternetExplorerMajorVersion()<8)},m.enabled=!m.emulated.pushState,m.bugs={setHash:Boolean(!m.emulated.pushState&&e.vendor==="Apple Computer, Inc."&&/AppleWebKit\/5([0-2]|3[0-3])/.test(e.userAgent)),safariPoll:Boolean(!m.emulated.pushState&&e.vendor==="Apple Computer, Inc."&&/AppleWebKit\/5([0-2]|3[0-3])/.test(e.userAgent)),ieDoubleCheck:Boolean(m.isInternetExplorer()&&m.getInternetExplorerMajorVersion()<8),hashEscape:Boolean(m.isInternetExplorer()&&m.getInternetExplorerMajorVersion()<7)},m.isEmptyObject=function(a){for(var b in a)return!1;return!0},m.cloneObject=function(a){var b,c;return a?(b=k.stringify(a),c=k.parse(b)):c={},c},m.getRootUrl=function(){var a=d.location.protocol+"//"+(d.location.hostname||d.location.host);if(d.location.port||!1)a+=":"+d.location.port;return a+="/",a},m.getBaseHref=function(){var a=d.getElementsByTagName("base"),b=null,c="";return a.length===1&&(b=a[0],c=b.href.replace(/[^\/]+$/,"")),c=c.replace(/\/+$/,""),c&&(c+="/"),c},m.getBaseUrl=function(){var a=m.getBaseHref()||m.getBasePageUrl()||m.getRootUrl();return a},m.getPageUrl=function(){var a=m.getState(!1,!1),b=(a||{}).url||d.location.href,c;return c=b.replace(/\/+$/,"").replace(/[^\/]+$/,function(a,b,c){return/\./.test(a)?a:a+"/"}),c},m.getBasePageUrl=function(){var a=d.location.href.replace(/[#\?].*/,"").replace(/[^\/]+$/,function(a,b,c){return/[^\/]$/.test(a)?"":a}).replace(/\/+$/,"")+"/";return a},m.getFullUrl=function(a,b){var c=a,d=a.substring(0,1);return b=typeof b=="undefined"?!0:b,/[a-z]+\:\/\//.test(a)||(d==="/"?c=m.getRootUrl()+a.replace(/^\/+/,""):d==="#"?c=m.getPageUrl().replace(/#.*/,"")+a:d==="?"?c=m.getPageUrl().replace(/[\?#].*/,"")+a:b?c=m.getBaseUrl()+a.replace(/^(\.\/)+/,""):c=m.getBasePageUrl()+a.replace(/^(\.\/)+/,"")),c.replace(/\#$/,"")},m.getShortUrl=function(a){var b=a,c=m.getBaseUrl(),d=m.getRootUrl();return m.emulated.pushState&&(b=b.replace(c,"")),b=b.replace(d,"/"),m.isTraditionalAnchor(b)&&(b="./"+b),b=b.replace(/^(\.\/)+/g,"./").replace(/\#$/,""),b},m.store={},m.idToState=m.idToState||{},m.stateToId=m.stateToId||{},m.urlToId=m.urlToId||{},m.storedStates=m.storedStates||[],m.savedStates=m.savedStates||[],m.normalizeStore=function(){m.store.idToState=m.store.idToState||{},m.store.urlToId=m.store.urlToId||{},m.store.stateToId=m.store.stateToId||{}},m.getState=function(a,b){typeof a=="undefined"&&(a=!0),typeof b=="undefined"&&(b=!0);var c=m.getLastSavedState();return!c&&b&&(c=m.createStateObject()),a&&(c=m.cloneObject(c),c.url=c.cleanUrl||c.url),c},m.getIdByState=function(a){var b=m.extractId(a.url),c;if(!b){c=m.getStateString(a);if(typeof m.stateToId[c]!="undefined")b=m.stateToId[c];else if(typeof m.store.stateToId[c]!="undefined")b=m.store.stateToId[c];else{for(;;){b=(new Date).getTime()+String(Math.random()).replace(/\D/g,"");if(typeof m.idToState[b]=="undefined"&&typeof m.store.idToState[b]=="undefined")break}m.stateToId[c]=b,m.idToState[b]=a}}return b},m.normalizeState=function(a){var b,c;if(!a||typeof a!="object")a={};if(typeof a.normalized!="undefined")return a;if(!a.data||typeof a.data!="object")a.data={};b={},b.normalized=!0,b.title=a.title||"",b.url=m.getFullUrl(m.unescapeString(a.url||d.location.href)),b.hash=m.getShortUrl(b.url),b.data=m.cloneObject(a.data),b.id=m.getIdByState(b),b.cleanUrl=b.url.replace(/\??\&_suid.*/,""),b.url=b.cleanUrl,c=!m.isEmptyObject(b.data);if(b.title||c)b.hash=m.getShortUrl(b.url).replace(/\??\&_suid.*/,""),/\?/.test(b.hash)||(b.hash+="?"),b.hash+="&_suid="+b.id;return b.hashedUrl=m.getFullUrl(b.hash),(m.emulated.pushState||m.bugs.safariPoll)&&m.hasUrlDuplicate(b)&&(b.url=b.hashedUrl),b},m.createStateObject=function(a,b,c){var d={data:a,title:b,url:c};return d=m.normalizeState(d),d},m.getStateById=function(a){a=String(a);var c=m.idToState[a]||m.store.idToState[a]||b;return c},m.getStateString=function(a){var b,c,d;return b=m.normalizeState(a),c={data:b.data,title:a.title,url:a.url},d=k.stringify(c),d},m.getStateId=function(a){var b,c;return b=m.normalizeState(a),c=b.id,c},m.getHashByState=function(a){var b,c;return b=m.normalizeState(a),c=b.hash,c},m.extractId=function(a){var b,c,d;return c=/(.*)\&_suid=([0-9]+)$/.exec(a),d=c?c[1]||a:a,b=c?String(c[2]||""):"",b||!1},m.isTraditionalAnchor=function(a){var b=!/[\/\?\.]/.test(a);return b},m.extractState=function(a,b){var c=null,d,e;return b=b||!1,d=m.extractId(a),d&&(c=m.getStateById(d)),c||(e=m.getFullUrl(a),d=m.getIdByUrl(e)||!1,d&&(c=m.getStateById(d)),!c&&b&&!m.isTraditionalAnchor(a)&&(c=m.createStateObject(null,null,e))),c},m.getIdByUrl=function(a){var c=m.urlToId[a]||m.store.urlToId[a]||b;return c},m.getLastSavedState=function(){return m.savedStates[m.savedStates.length-1]||b},m.getLastStoredState=function(){return m.storedStates[m.storedStates.length-1]||b},m.hasUrlDuplicate=function(a){var b=!1,c;return c=m.extractState(a.url),b=c&&c.id!==a.id,b},m.storeState=function(a){return m.urlToId[a.url]=a.id,m.storedStates.push(m.cloneObject(a)),a},m.isLastSavedState=function(a){var b=!1,c,d,e;return m.savedStates.length&&(c=a.id,d=m.getLastSavedState(),e=d.id,b=c===e),b},m.saveState=function(a){return m.isLastSavedState(a)?!1:(m.savedStates.push(m.cloneObject(a)),!0)},m.getStateByIndex=function(a){var b=null;return typeof a=="undefined"?b=m.savedStates[m.savedStates.length-1]:a<0?b=m.savedStates[m.savedStates.length+a]:b=m.savedStates[a],b},m.getHash=function(){var a=m.unescapeHash(d.location.hash);return a},m.unescapeString=function(b){var c=b,d;for(;;){d=a.unescape(c);if(d===c)break;c=d}return c},m.unescapeHash=function(a){var b=m.normalizeHash(a);return b=m.unescapeString(b),b},m.normalizeHash=function(a){var b=a.replace(/[^#]*#/,"").replace(/#.*/,"");return b},m.setHash=function(a,b){var c,e,f;return b!==!1&&m.busy()?(m.pushQueue({scope:m,callback:m.setHash,args:arguments,queue:b}),!1):(c=m.escapeHash(a),m.busy(!0),e=m.extractState(a,!0),e&&!m.emulated.pushState?m.pushState(e.data,e.title,e.url,!1):d.location.hash!==c&&(m.bugs.setHash?(f=m.getPageUrl(),m.pushState(null,null,f+"#"+c,!1)):d.location.hash=c),m)},m.escapeHash=function(b){var c=m.normalizeHash(b);return c=a.escape(c),m.bugs.hashEscape||(c=c.replace(/\%21/g,"!").replace(/\%26/g,"&").replace(/\%3D/g,"=").replace(/\%3F/g,"?")),c},m.getHashByUrl=function(a){var b=String(a).replace(/([^#]*)#?([^#]*)#?(.*)/,"$2");return b=m.unescapeHash(b),b},m.setTitle=function(a){var b=a.title,c;b||(c=m.getStateByIndex(0),c&&c.url===a.url&&(b=c.title||m.options.initialTitle));try{d.getElementsByTagName("title")[0].innerHTML=b.replace("<","&lt;").replace(">","&gt;").replace(" & "," &amp; ")}catch(e){}return d.title=b,m},m.queues=[],m.busy=function(a){typeof a!="undefined"?m.busy.flag=a:typeof m.busy.flag=="undefined"&&(m.busy.flag=!1);if(!m.busy.flag){h(m.busy.timeout);var b=function(){var a,c,d;if(m.busy.flag)return;for(a=m.queues.length-1;a>=0;--a){c=m.queues[a];if(c.length===0)continue;d=c.shift(),m.fireQueueItem(d),m.busy.timeout=g(b,m.options.busyDelay)}};m.busy.timeout=g(b,m.options.busyDelay)}return m.busy.flag},m.busy.flag=!1,m.fireQueueItem=function(a){return a.callback.apply(a.scope||m,a.args||[])},m.pushQueue=function(a){return m.queues[a.queue||0]=m.queues[a.queue||0]||[],m.queues[a.queue||0].push(a),m},m.queue=function(a,b){return typeof a=="function"&&(a={callback:a}),typeof b!="undefined"&&(a.queue=b),m.busy()?m.pushQueue(a):m.fireQueueItem(a),m},m.clearQueue=function(){return m.busy.flag=!1,m.queues=[],m},m.stateChanged=!1,m.doubleChecker=!1,m.doubleCheckComplete=function(){return m.stateChanged=!0,m.doubleCheckClear(),m},m.doubleCheckClear=function(){return m.doubleChecker&&(h(m.doubleChecker),m.doubleChecker=!1),m},m.doubleCheck=function(a){return m.stateChanged=!1,m.doubleCheckClear(),m.bugs.ieDoubleCheck&&(m.doubleChecker=g(function(){return m.doubleCheckClear(),m.stateChanged||a(),!0},m.options.doubleCheckInterval)),m},m.safariStatePoll=function(){var b=m.extractState(d.location.href),c;if(!m.isLastSavedState(b))c=b;else return;return c||(c=m.createStateObject()),m.Adapter.trigger(a,"popstate"),m},m.back=function(a){return a!==!1&&m.busy()?(m.pushQueue({scope:m,callback:m.back,args:arguments,queue:a}),!1):(m.busy(!0),m.doubleCheck(function(){m.back(!1)}),n.go(-1),!0)},m.forward=function(a){return a!==!1&&m.busy()?(m.pushQueue({scope:m,callback:m.forward,args:arguments,queue:a}),!1):(m.busy(!0),m.doubleCheck(function(){m.forward(!1)}),n.go(1),!0)},m.go=function(a,b){var c;if(a>0)for(c=1;c<=a;++c)m.forward(b);else{if(!(a<0))throw new Error("History.go: History.go requires a positive or negative integer passed.");for(c=-1;c>=a;--c)m.back(b)}return m};if(m.emulated.pushState){var o=function(){};m.pushState=m.pushState||o,m.replaceState=m.replaceState||o}else m.onPopState=function(b,c){var e=!1,f=!1,g,h;return m.doubleCheckComplete(),g=m.getHash(),g?(h=m.extractState(g||d.location.href,!0),h?m.replaceState(h.data,h.title,h.url,!1):(m.Adapter.trigger(a,"anchorchange"),m.busy(!1)),m.expectedStateId=!1,!1):(e=m.Adapter.extractEventData("state",b,c)||!1,e?f=m.getStateById(e):m.expectedStateId?f=m.getStateById(m.expectedStateId):f=m.extractState(d.location.href),f||(f=m.createStateObject(null,null,d.location.href)),m.expectedStateId=!1,m.isLastSavedState(f)?(m.busy(!1),!1):(m.storeState(f),m.saveState(f),m.setTitle(f),m.Adapter.trigger(a,"statechange"),m.busy(!1),!0))},m.Adapter.bind(a,"popstate",m.onPopState),m.pushState=function(b,c,d,e){if(m.getHashByUrl(d)&&m.emulated.pushState)throw new Error("History.js does not support states with fragement-identifiers (hashes/anchors).");if(e!==!1&&m.busy())return m.pushQueue({scope:m,callback:m.pushState,args:arguments,queue:e}),!1;m.busy(!0);var f=m.createStateObject(b,c,d);return m.isLastSavedState(f)?m.busy(!1):(m.storeState(f),m.expectedStateId=f.id,n.pushState(f.id,f.title,f.url),m.Adapter.trigger(a,"popstate")),!0},m.replaceState=function(b,c,d,e){if(m.getHashByUrl(d)&&m.emulated.pushState)throw new Error("History.js does not support states with fragement-identifiers (hashes/anchors).");if(e!==!1&&m.busy())return m.pushQueue({scope:m,callback:m.replaceState,args:arguments,queue:e}),!1;m.busy(!0);var f=m.createStateObject(b,c,d);return m.isLastSavedState(f)?m.busy(!1):(m.storeState(f),m.expectedStateId=f.id,n.replaceState(f.id,f.title,f.url),m.Adapter.trigger(a,"popstate")),!0};if(f){try{m.store=k.parse(f.getItem("History.store"))||{}}catch(p){m.store={}}m.normalizeStore()}else m.store={},m.normalizeStore();m.Adapter.bind(a,"beforeunload",m.clearAllIntervals),m.Adapter.bind(a,"unload",m.clearAllIntervals),m.saveState(m.storeState(m.extractState(d.location.href,!0))),f&&(m.onUnload=function(){var a,b;try{a=k.parse(f.getItem("History.store"))||{}}catch(c){a={}}a.idToState=a.idToState||{},a.urlToId=a.urlToId||{},a.stateToId=a.stateToId||{};for(b in m.idToState){if(!m.idToState.hasOwnProperty(b))continue;a.idToState[b]=m.idToState[b]}for(b in m.urlToId){if(!m.urlToId.hasOwnProperty(b))continue;a.urlToId[b]=m.urlToId[b]}for(b in m.stateToId){if(!m.stateToId.hasOwnProperty(b))continue;a.stateToId[b]=m.stateToId[b]}m.store=a,m.normalizeStore(),f.setItem("History.store",k.stringify(a))},m.intervalList.push(i(m.onUnload,m.options.storeInterval)),m.Adapter.bind(a,"beforeunload",m.onUnload),m.Adapter.bind(a,"unload",m.onUnload));if(!m.emulated.pushState){m.bugs.safariPoll&&m.intervalList.push(i(m.safariStatePoll,m.options.safariPollInterval));if(e.vendor==="Apple Computer, Inc."||(e.appCodeName||"")==="Mozilla")m.Adapter.bind(a,"hashchange",function(){m.Adapter.trigger(a,"popstate")}),m.getHash()&&m.Adapter.onDomLoad(function(){m.Adapter.trigger(a,"hashchange")})}},m.init()}(window)
$(document).ready(function(){
	//themes, change CSS with JS
	//default theme(CSS) is cerulean, change it if needed
	var current_theme = $.cookie('current_theme')==null ? 'cerulean' :$.cookie('current_theme');
	switch_theme(current_theme);
	
	$('#themes a[data-value="'+current_theme+'"]').find('i').addClass('icon-ok');
				 
	$('#themes a').click(function(e){
		e.preventDefault();
		current_theme=$(this).attr('data-value');
		$.cookie('current_theme',current_theme,{expires:365});
		switch_theme(current_theme);
		$('#themes i').removeClass('icon-ok');
		$(this).find('i').addClass('icon-ok');
	});
	
	
	function switch_theme(theme_name)
	{
		$('#bs-css').attr('href','/assets/css/bootstrap-'+theme_name+'.css');
	}
	
	//ajax menu checkbox
	$('#is-ajax').click(function(e){
		$.cookie('is-ajax',$(this).prop('checked'),{expires:365});
	});
	$('#is-ajax').prop('checked',$.cookie('is-ajax')==='true' ? true : false);
	
	//disbaling some functions for Internet Explorer
	if($.browser.msie)
	{
		$('#is-ajax').prop('checked',false);
		$('#for-is-ajax').hide();
		$('#toggle-fullscreen').hide();
		$('.login-box').find('.input-large').removeClass('span10');
		
	}
	
	
	//highlight current / active link
	$('ul.main-menu li a').each(function(){
		if($($(this))[0].href==String(window.location))
			$(this).parent().addClass('active');
	});
	
	//establish history variables
	var
		History = window.History, // Note: We are using a capital H instead of a lower h
		State = History.getState(),
		$log = $('#log');

	//bind to State Change
	History.Adapter.bind(window,'statechange',function(){ // Note: We are using statechange instead of popstate
		var State = History.getState(); // Note: We are using History.getState() instead of event.state
		$.ajax({
			url:State.url,
			success:function(msg){
				$('#content').html($(msg).find('#content').html());
				$('#loading').remove();
				$('#content').fadeIn();
				docReady();
			}
		});
	});
	
	//ajaxify menus
	$('a.ajax-link').click(function(e){
		if($.browser.msie) e.which=1;
		if(e.which!=1 || !$('#is-ajax').prop('checked') || $(this).parent().hasClass('active')) return;
		e.preventDefault();
		if($('.btn-navbar').is(':visible'))
		{
			$('.btn-navbar').click();
		}
		$('#loading').remove();
		$('#content').fadeOut().parent().append('<div id="loading" class="center">Loading...<div class="center"></div></div>');
		var $clink=$(this);
		History.pushState(null, null, $clink.attr('href'));
		$('ul.main-menu li.active').removeClass('active');
		$clink.parent('li').addClass('active');	
	});
	
	//animating menus on hover
	$('ul.main-menu li:not(.nav-header)').hover(function(){
		$(this).animate({'margin-left':'+=5'},300);
	},
	function(){
		$(this).animate({'margin-left':'-=5'},300);
	});
	
	//other things to do on document ready, seperated for ajax calls
	docReady();
});
		
		
function docReady(){
	//prevent # links from moving to top
	$('a[href="#"][data-top!=true]').click(function(e){
		e.preventDefault();
	});
	
	//rich text editor
	$('.cleditor').cleditor();
	
	//datepicker
	$('.datepicker').datepicker();
	
	//notifications
	$('.noty').click(function(e){
		e.preventDefault();
		var options = $.parseJSON($(this).attr('data-noty-options'));
		noty(options);
	});


	//uniform - styler for checkbox, radio and file input
	$("input:checkbox, input:radio, input:file").not('[data-no-uniform="true"],#uniform-is-ajax').uniform();

	//chosen - improves select
	$('[data-rel="chosen"],[rel="chosen"]').chosen();

	//tabs
	$('#myTab a:first').tab('show');
	$('#myTab a').click(function (e) {
	  e.preventDefault();
	  $(this).tab('show');
	});

	//makes elements soratble, elements that sort need to have id attribute to save the result
	$('.sortable').sortable({
		revert:true,
		cancel:'.btn,.box-content,.nav-header',
		update:function(event,ui){
			//line below gives the ids of elements, you can make ajax call here to save it to the database
			//console.log($(this).sortable('toArray'));
		}
	});

	//slider
	$('.slider').slider({range:true,values:[10,65]});

	//tooltip
	$('[rel="tooltip"],[data-rel="tooltip"]').tooltip({"placement":"bottom",delay: { show: 400, hide: 200 }});

	//auto grow textarea
	$('textarea.autogrow').autogrow();

	//popover
	$('[rel="popover"],[data-rel="popover"]').popover();

	//file manager
	var elf = $('.file-manager').elfinder({
		url : '/assets/misc/elfinder-connector/connector.php'  // connector URL (REQUIRED)
	}).elfinder('instance');

	//iOS / iPhone style toggle switch
	$('.iphone-toggle').iphoneStyle();

	//star rating
	$('.raty').raty({
		score : 4 //default stars
	});

	//uploadify - multiple uploads
	$('#file_upload').uploadify({
		'swf'      : '/assets/misc/uploadify.swf',
		'uploader' : '/assets/misc/uploadify.php'
		// Put your options here
	});

	//gallery controlls container animation
	$('ul.gallery li').hover(function(){
		$('img',this).fadeToggle(1000);
		$(this).find('.gallery-controls').remove();
		$(this).append('<div class="well gallery-controls">'+
							'<p><a href="#" class="gallery-edit btn"><i class="icon-edit"></i></a> <a href="#" class="gallery-delete btn"><i class="icon-remove"></i></a></p>'+
						'</div>');
		$(this).find('.gallery-controls').stop().animate({'margin-top':'-1'},400,'easeInQuint');
	},function(){
		$('img',this).fadeToggle(1000);
		$(this).find('.gallery-controls').stop().animate({'margin-top':'-30'},200,'easeInQuint',function(){
				$(this).remove();
		});
	});


	//gallery image controls example
	//gallery delete
	$('.thumbnails').on('click','.gallery-delete',function(e){
		e.preventDefault();
		//get image id
		//alert($(this).parents('.thumbnail').attr('id'));
		$(this).parents('.thumbnail').fadeOut();
	});
	//gallery edit
	$('.thumbnails').on('click','.gallery-edit',function(e){
		e.preventDefault();
		//get image id
		//alert($(this).parents('.thumbnail').attr('id'));
	});

	//gallery colorbox
	$('.thumbnail a').colorbox({rel:'thumbnail a', transition:"elastic", maxWidth:"95%", maxHeight:"95%"});

	//gallery fullscreen
	$('#toggle-fullscreen').button().click(function () {
		var button = $(this), root = document.documentElement;
		if (!button.hasClass('active')) {
			$('#thumbnails').addClass('modal-fullscreen');
			if (root.webkitRequestFullScreen) {
				root.webkitRequestFullScreen(
					window.Element.ALLOW_KEYBOARD_INPUT
				);
			} else if (root.mozRequestFullScreen) {
				root.mozRequestFullScreen();
			}
		} else {
			$('#thumbnails').removeClass('modal-fullscreen');
			(document.webkitCancelFullScreen ||
				document.mozCancelFullScreen ||
				$.noop).apply(document);
		}
	});

	//tour
	if($('.tour').length && typeof(tour)=='undefined')
	{
		var tour = new Tour();
		tour.addStep({
			element: ".span10:first", /* html element next to which the step popover should be shown */
			placement: "top",
			title: "Custom Tour", /* title of the popover */
			content: "You can create tour like this. Click Next." /* content of the popover */
		});
		tour.addStep({
			element: ".theme-container",
			placement: "left",
			title: "Themes",
			content: "You change your theme from here."
		});
		tour.addStep({
			element: "ul.main-menu a:first",
			title: "Dashboard",
			content: "This is your dashboard from here you will find highlights."
		});
		tour.addStep({
			element: "#for-is-ajax",
			title: "Ajax",
			content: "You can change if pages load with Ajax or not."
		});
		tour.addStep({
			element: ".top-nav a:first",
			placement: "bottom",
			title: "Visit Site",
			content: "Visit your front end from here."
		});
		
		tour.restart();
	}

	//datatable
	$('.datatable').dataTable({
			"sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span12'i><'span12 center'p>>",
			"sPaginationType": "bootstrap",
			"oLanguage": {
			"sLengthMenu": "_MENU_ records per page"
			}
		} );
	$('.btn-close').click(function(e){
		e.preventDefault();
		$(this).parent().parent().parent().fadeOut();
	});
	$('.btn-minimize').click(function(e){
		e.preventDefault();
		var $target = $(this).parent().parent().next('.box-content');
		if($target.is(':visible')) $('i',$(this)).removeClass('icon-chevron-up').addClass('icon-chevron-down');
		else 					   $('i',$(this)).removeClass('icon-chevron-down').addClass('icon-chevron-up');
		$target.slideToggle();
	});
	$('.btn-setting').click(function(e){
		e.preventDefault();
		$('#myModal').modal('show');
	});



		
	//initialize the external events for calender

	$('#external-events div.external-event').each(function() {

		// it doesn't need to have a start or end
		var eventObject = {
			title: $.trim($(this).text()) // use the element's text as the event title
		};
		
		// store the Event Object in the DOM element so we can get to it later
		$(this).data('eventObject', eventObject);
		
		// make the event draggable using jQuery UI
		$(this).draggable({
			zIndex: 999,
			revert: true,      // will cause the event to go back to its
			revertDuration: 0  //  original position after the drag
		});
		
	});


	//initialize the calendar
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		editable: true,
		droppable: true, // this allows things to be dropped onto the calendar !!!
		drop: function(date, allDay) { // this function is called when something is dropped
		
			// retrieve the dropped element's stored Event Object
			var originalEventObject = $(this).data('eventObject');
			
			// we need to copy it, so that multiple events don't have a reference to the same object
			var copiedEventObject = $.extend({}, originalEventObject);
			
			// assign it the date that was reported
			copiedEventObject.start = date;
			copiedEventObject.allDay = allDay;
			
			// render the event on the calendar
			// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
			$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
			
			// is the "remove after drop" checkbox checked?
			if ($('#drop-remove').is(':checked')) {
				// if so, remove the element from the "Draggable Events" list
				$(this).remove();
			}
			
		}
	});
	
	
	//chart with points
	if($("#sincos").length)
	{
		var sin = [], cos = [];

		for (var i = 0; i < 14; i += 0.5) {
			sin.push([i, Math.sin(i)/i]);
			cos.push([i, Math.cos(i)]);
		}

		var plot = $.plot($("#sincos"),
			   [ { data: sin, label: "sin(x)/x"}, { data: cos, label: "cos(x)" } ], {
				   series: {
					   lines: { show: true  },
					   points: { show: true }
				   },
				   grid: { hoverable: true, clickable: true, backgroundColor: { colors: ["#fff", "#eee"] } },
				   yaxis: { min: -1.2, max: 1.2 },
				   colors: ["#539F2E", "#3C67A5"]
				 });

		function showTooltip(x, y, contents) {
			$('<div id="tooltip">' + contents + '</div>').css( {
				position: 'absolute',
				display: 'none',
				top: y + 5,
				left: x + 5,
				border: '1px solid #fdd',
				padding: '2px',
				'background-color': '#dfeffc',
				opacity: 0.80
			}).appendTo("body").fadeIn(200);
		}

		var previousPoint = null;
		$("#sincos").bind("plothover", function (event, pos, item) {
			$("#x").text(pos.x.toFixed(2));
			$("#y").text(pos.y.toFixed(2));

				if (item) {
					if (previousPoint != item.dataIndex) {
						previousPoint = item.dataIndex;

						$("#tooltip").remove();
						var x = item.datapoint[0].toFixed(2),
							y = item.datapoint[1].toFixed(2);

						showTooltip(item.pageX, item.pageY,
									item.series.label + " of " + x + " = " + y);
					}
				}
				else {
					$("#tooltip").remove();
					previousPoint = null;
				}
		});
		


		$("#sincos").bind("plotclick", function (event, pos, item) {
			if (item) {
				$("#clickdata").text("You clicked point " + item.dataIndex + " in " + item.series.label + ".");
				plot.highlight(item.series, item.datapoint);
			}
		});
	}
	
	//flot chart
	if($("#flotchart").length)
	{
		var d1 = [];
		for (var i = 0; i < Math.PI * 2; i += 0.25)
			d1.push([i, Math.sin(i)]);
		
		var d2 = [];
		for (var i = 0; i < Math.PI * 2; i += 0.25)
			d2.push([i, Math.cos(i)]);

		var d3 = [];
		for (var i = 0; i < Math.PI * 2; i += 0.1)
			d3.push([i, Math.tan(i)]);
		
		$.plot($("#flotchart"), [
			{ label: "sin(x)",  data: d1},
			{ label: "cos(x)",  data: d2},
			{ label: "tan(x)",  data: d3}
		], {
			series: {
				lines: { show: true },
				points: { show: true }
			},
			xaxis: {
				ticks: [0, [Math.PI/2, "\u03c0/2"], [Math.PI, "\u03c0"], [Math.PI * 3/2, "3\u03c0/2"], [Math.PI * 2, "2\u03c0"]]
			},
			yaxis: {
				ticks: 10,
				min: -2,
				max: 2
			},
			grid: {
				backgroundColor: { colors: ["#fff", "#eee"] }
			}
		});
	}
	
	//stack chart
	if($("#stackchart").length)
	{
		var d1 = [];
		for (var i = 0; i <= 10; i += 1)
		d1.push([i, parseInt(Math.random() * 30)]);

		var d2 = [];
		for (var i = 0; i <= 10; i += 1)
			d2.push([i, parseInt(Math.random() * 30)]);

		var d3 = [];
		for (var i = 0; i <= 10; i += 1)
			d3.push([i, parseInt(Math.random() * 30)]);

		var stack = 0, bars = true, lines = false, steps = false;

		function plotWithOptions() {
			$.plot($("#stackchart"), [ d1, d2, d3 ], {
				series: {
					stack: stack,
					lines: { show: lines, fill: true, steps: steps },
					bars: { show: bars, barWidth: 0.6 }
				}
			});
		}

		plotWithOptions();

		$(".stackControls input").click(function (e) {
			e.preventDefault();
			stack = $(this).val() == "With stacking" ? true : null;
			plotWithOptions();
		});
		$(".graphControls input").click(function (e) {
			e.preventDefault();
			bars = $(this).val().indexOf("Bars") != -1;
			lines = $(this).val().indexOf("Lines") != -1;
			steps = $(this).val().indexOf("steps") != -1;
			plotWithOptions();
		});
	}

	//pie chart
	var data = [
	{ label: "Internet Explorer",  data: 12},
	{ label: "Mobile",  data: 27},
	{ label: "Safari",  data: 85},
	{ label: "Opera",  data: 64},
	{ label: "Firefox",  data: 90},
	{ label: "Chrome",  data: 112}
	];
	
	if($("#piechart").length)
	{
		$.plot($("#piechart"), data,
		{
			series: {
					pie: {
							show: true
					}
			},
			grid: {
					hoverable: true,
					clickable: true
			},
			legend: {
				show: false
			}
		});
		
		function pieHover(event, pos, obj)
		{
			if (!obj)
					return;
			percent = parseFloat(obj.series.percent).toFixed(2);
			$("#hover").html('<span style="font-weight: bold; color: '+obj.series.color+'">'+obj.series.label+' ('+percent+'%)</span>');
		}
		$("#piechart").bind("plothover", pieHover);
	}
	
	//donut chart
	if($("#donutchart").length)
	{
		$.plot($("#donutchart"), data,
		{
				series: {
						pie: {
								innerRadius: 0.5,
								show: true
						}
				},
				legend: {
					show: false
				}
		});
	}




	 // we use an inline data source in the example, usually data would
	// be fetched from a server
	var data = [], totalPoints = 300;
	function getRandomData() {
		if (data.length > 0)
			data = data.slice(1);

		// do a random walk
		while (data.length < totalPoints) {
			var prev = data.length > 0 ? data[data.length - 1] : 50;
			var y = prev + Math.random() * 10 - 5;
			if (y < 0)
				y = 0;
			if (y > 100)
				y = 100;
			data.push(y);
		}

		// zip the generated y values with the x values
		var res = [];
		for (var i = 0; i < data.length; ++i)
			res.push([i, data[i]])
		return res;
	}

	// setup control widget
	var updateInterval = 30;
	$("#updateInterval").val(updateInterval).change(function () {
		var v = $(this).val();
		if (v && !isNaN(+v)) {
			updateInterval = +v;
			if (updateInterval < 1)
				updateInterval = 1;
			if (updateInterval > 2000)
				updateInterval = 2000;
			$(this).val("" + updateInterval);
		}
	});

	//realtime chart
	if($("#realtimechart").length)
	{
		var options = {
			series: { shadowSize: 1 }, // drawing is faster without shadows
			yaxis: { min: 0, max: 100 },
			xaxis: { show: false }
		};
		var plot = $.plot($("#realtimechart"), [ getRandomData() ], options);
		function update() {
			plot.setData([ getRandomData() ]);
			// since the axes don't change, we don't need to call plot.setupGrid()
			plot.draw();
			
			setTimeout(update, updateInterval);
		}

		update();
	}
}


//additional functions for data table
$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
	return {
		"iStart":         oSettings._iDisplayStart,
		"iEnd":           oSettings.fnDisplayEnd(),
		"iLength":        oSettings._iDisplayLength,
		"iTotal":         oSettings.fnRecordsTotal(),
		"iFilteredTotal": oSettings.fnRecordsDisplay(),
		"iPage":          Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
		"iTotalPages":    Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
	};
}
$.extend( $.fn.dataTableExt.oPagination, {
	"bootstrap": {
		"fnInit": function( oSettings, nPaging, fnDraw ) {
			var oLang = oSettings.oLanguage.oPaginate;
			var fnClickHandler = function ( e ) {
				e.preventDefault();
				if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
					fnDraw( oSettings );
				}
			};

			$(nPaging).addClass('pagination').append(
				'<ul>'+
					'<li class="prev disabled"><a href="#">&larr; '+oLang.sPrevious+'</a></li>'+
					'<li class="next disabled"><a href="#">'+oLang.sNext+' &rarr; </a></li>'+
				'</ul>'
			);
			var els = $('a', nPaging);
			$(els[0]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
			$(els[1]).bind( 'click.DT', { action: "next" }, fnClickHandler );
		},

		"fnUpdate": function ( oSettings, fnDraw ) {
			var iListLength = 5;
			var oPaging = oSettings.oInstance.fnPagingInfo();
			var an = oSettings.aanFeatures.p;
			var i, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);

			if ( oPaging.iTotalPages < iListLength) {
				iStart = 1;
				iEnd = oPaging.iTotalPages;
			}
			else if ( oPaging.iPage <= iHalf ) {
				iStart = 1;
				iEnd = iListLength;
			} else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
				iStart = oPaging.iTotalPages - iListLength + 1;
				iEnd = oPaging.iTotalPages;
			} else {
				iStart = oPaging.iPage - iHalf + 1;
				iEnd = iStart + iListLength - 1;
			}

			for ( i=0, iLen=an.length ; i<iLen ; i++ ) {
				// remove the middle elements
				$('li:gt(0)', an[i]).filter(':not(:last)').remove();

				// add the new list items and their event handlers
				for ( j=iStart ; j<=iEnd ; j++ ) {
					sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
					$('<li '+sClass+'><a href="#">'+j+'</a></li>')
						.insertBefore( $('li:last', an[i])[0] )
						.bind('click', function (e) {
							e.preventDefault();
							oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
							fnDraw( oSettings );
						} );
				}

				// add / remove disabled classes from the static elements
				if ( oPaging.iPage === 0 ) {
					$('li:first', an[i]).addClass('disabled');
				} else {
					$('li:first', an[i]).removeClass('disabled');
				}

				if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
					$('li:last', an[i]).addClass('disabled');
				} else {
					$('li:last', an[i]).removeClass('disabled');
				}
			}
		}
	}
});
