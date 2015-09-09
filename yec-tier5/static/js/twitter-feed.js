! function () {
	var t;
	Function && Function.prototype && Function.prototype.bind && (/MSIE [678]/.test(navigator.userAgent) || ! function e(t, i, n) {
			function r(s, a) {
				if (!i[s]) {
					if (!t[s]) {
						var l = "function" == typeof require && require;
						if (!a && l) return l(s, !0);
						if (o) return o(s, !0);
						var u = new Error("Cannot find module '" + s + "'");
						throw u.code = "MODULE_NOT_FOUND", u
					}
					var c = i[s] = {
						exports: {}
					};
					t[s][0].call(c.exports, function (e) {
						var i = t[s][1][e];
						return r(i ? i : e)
					}, c, c.exports, e, t, i, n)
				}
				return i[s].exports
			}
			for (var o = "function" == typeof require && require, s = 0; s < n.length; s++) r(n[s]);
			return r
		}({
				1: [function (e, i) {
					(function () {
						"use strict";

						function e(t) {
							return "function" == typeof t || "object" == typeof t && null !== t
						}

						function n(t) {
							return "function" == typeof t
						}

						function r(t) {
							return "object" == typeof t && null !== t
						}

						function o() {}

						function s() {
							return function () {
								process.nextTick(c)
							}
						}

						function a() {
							var t = 0,
								e = new H(c),
								i = document.createTextNode("");
							return e.observe(i, {
									characterData: !0
								}),
								function () {
									i.data = t = ++t % 2
								}
						}

						function l() {
							var t = new MessageChannel;
							return t.port1.onmessage = c,
								function () {
									t.port2.postMessage(0)
								}
						}

						function u() {
							return function () {
								setTimeout(c, 1)
							}
						}

						function c() {
							for (var t = 0; O > t; t += 2) {
								var e = U[t],
									i = U[t + 1];
								e(i), U[t] = void 0, U[t + 1] = void 0
							}
							O = 0
						}

						function d() {}

						function h() {
							return new TypeError("You cannot resolve a promise with itself")
						}

						function f() {
							return new TypeError("A promises callback cannot return that same promise.")
						}

						function m(t) {
							try {
								return t.then
							} catch (e) {
								return B.error = e, B
							}
						}

						function p(t, e, i, n) {
							try {
								t.call(e, i, n)
							} catch (r) {
								return r
							}
						}

						function g(t, e, i) {
							F(function (t) {
								var n = !1,
									r = p(i, e, function (i) {
										n || (n = !0, e !== i ? b(t, i) : _(t, i))
									}, function (e) {
										n || (n = !0, T(t, e))
									}, "Settle: " + (t._label || " unknown promise"));
								!n && r && (n = !0, T(t, r))
							}, t)
						}

						function w(t, e) {
							e._state === z ? _(t, e._result) : t._state === K ? T(t, e._result) : x(e, void 0, function (e) {
								b(t, e)
							}, function (e) {
								T(t, e)
							})
						}

						function v(t, e) {
							if (e.constructor === t.constructor) w(t, e);
							else {
								var i = m(e);
								i === B ? T(t, B.error) : void 0 === i ? _(t, e) : n(i) ? g(t, e, i) : _(t, e)
							}
						}

						function b(t, i) {
							t === i ? T(t, h()) : e(i) ? v(t, i) : _(t, i)
						}

						function y(t) {
							t._onerror && t._onerror(t._result), A(t)
						}

						function _(t, e) {
							t._state === q && (t._result = e, t._state = z, 0 === t._subscribers.length || F(A, t))
						}

						function T(t, e) {
							t._state === q && (t._state = K, t._result = e, F(y, t))
						}

						function x(t, e, i, n) {
							var r = t._subscribers,
								o = r.length;
							t._onerror = null, r[o] = e, r[o + z] = i, r[o + K] = n, 0 === o && t._state && F(A, t)
						}

						function A(t) {
							var e = t._subscribers,
								i = t._state;
							if (0 !== e.length) {
								for (var n, r, o = t._result, s = 0; s < e.length; s += 3) n = e[s], r = e[s + i], n ? S(i, n, r, o) : r(o);
								t._subscribers.length = 0
							}
						}

						function E() {
							this.error = null
						}

						function I(t, e) {
							try {
								return t(e)
							} catch (i) {
								return V.error = i, V
							}
						}

						function S(t, e, i, r) {
							var o, s, a, l, u = n(i);
							if (u) {
								if (o = I(i, r), o === V ? (l = !0, s = o.error, o = null) : a = !0, e === o) return void T(e, f())
							} else o = r, a = !0;
							e._state !== q || (u && a ? b(e, o) : l ? T(e, s) : t === z ? _(e, o) : t === K && T(e, o))
						}

						function N(t, e) {
							try {
								e(function (e) {
									b(t, e)
								}, function (e) {
									T(t, e)
								})
							} catch (i) {
								T(t, i)
							}
						}

						function D(t, e, i, n) {
							this._instanceConstructor = t, this.promise = new t(d, n), this._abortOnReject = i, this._validateInput(e) ? (this._input = e, this.length = e.length, this._remaining = e.length, this._init(), 0 === this.length ? _(this.promise, this._result) : (this.length = this.length || 0, this._enumerate(), 0 === this._remaining && _(this.promise, this._result))) : T(this.promise, this._validationError())
						}

						function R() {
							throw new TypeError("You must pass a resolver function as the first argument to the promise constructor")
						}

						function k() {
							throw new TypeError("Failed to construct 'Promise': Please use the 'new' operator, this object constructor cannot be called as a function.")
						}

						function P(t) {
							this._id = X++, this._state = void 0, this._result = void 0, this._subscribers = [], d !== t && (n(t) || R(), this instanceof P || k(), N(this, t))
						}
						var L;
						L = Array.isArray ? Array.isArray : function (t) {
							return "[object Array]" === Object.prototype.toString.call(t)
						};
						var C, M = L,
							O = (Date.now || function () {
								return (new Date).getTime()
							}, Object.create || function (t) {
								if (arguments.length > 1) throw new Error("Second argument not supported");
								if ("object" != typeof t) throw new TypeError("Argument must be an object");
								return o.prototype = t, new o
							}, 0),
							F = function (t, e) {
								U[O] = t, U[O + 1] = e, O += 2, 2 === O && C()
							},
							j = "undefined" != typeof window ? window : {},
							H = j.MutationObserver || j.WebKitMutationObserver,
							W = "undefined" != typeof Uint8ClampedArray && "undefined" != typeof importScripts && "undefined" != typeof MessageChannel,
							U = new Array(1e3);
						C = "undefined" != typeof process && "[object process]" === {}.toString.call(process) ? s() : H ? a() : W ? l() : u();
						var q = void 0,
							z = 1,
							K = 2,
							B = new E,
							V = new E;
						D.prototype._validateInput = function (t) {
							return M(t)
						}, D.prototype._validationError = function () {
							return new Error("Array Methods must be provided an Array")
						}, D.prototype._init = function () {
							this._result = new Array(this.length)
						};
						var G = D;
						D.prototype._enumerate = function () {
							for (var t = this.length, e = this.promise, i = this._input, n = 0; e._state === q && t > n; n++) this._eachEntry(i[n], n)
						}, D.prototype._eachEntry = function (t, e) {
							var i = this._instanceConstructor;
							r(t) ? t.constructor === i && t._state !== q ? (t._onerror = null, this._settledAt(t._state, e, t._result)) : this._willSettleAt(i.resolve(t), e) : (this._remaining--, this._result[e] = this._makeResult(z, e, t))
						}, D.prototype._settledAt = function (t, e, i) {
							var n = this.promise;
							n._state === q && (this._remaining--, this._abortOnReject && t === K ? T(n, i) : this._result[e] = this._makeResult(t, e, i)), 0 === this._remaining && _(n, this._result)
						}, D.prototype._makeResult = function (t, e, i) {
							return i
						}, D.prototype._willSettleAt = function (t, e) {
							var i = this;
							x(t, void 0, function (t) {
								i._settledAt(z, e, t)
							}, function (t) {
								i._settledAt(K, e, t)
							})
						};
						var $ = function (t, e) {
								return new G(this, t, !0, e).promise
							},
							J = function (t, e) {
								function i(t) {
									b(o, t)
								}

								function n(t) {
									T(o, t)
								}
								var r = this,
									o = new r(d, e);
								if (!M(t)) return T(o, new TypeError("You must pass an array to race.")), o;
								for (var s = t.length, a = 0; o._state === q && s > a; a++) x(r.resolve(t[a]), void 0, i, n);
								return o
							},
							Y = function (t, e) {
								var i = this;
								if (t && "object" == typeof t && t.constructor === i) return t;
								var n = new i(d, e);
								return b(n, t), n
							},
							Q = function (t, e) {
								var i = this,
									n = new i(d, e);
								return T(n, t), n
							},
							X = 0,
							Z = P;
						P.all = $, P.race = J, P.resolve = Y, P.reject = Q, P.prototype = {
							constructor: P,
							then: function (t, e) {
								var i = this,
									n = i._state;
								if (n === z && !t || n === K && !e) return this;
								var r = new this.constructor(d),
									o = i._result;
								if (n) {
									var s = arguments[n - 1];
									F(function () {
										S(n, r, s, o)
									})
								} else x(i, r, t, e);
								return r
							},
							"catch": function (t) {
								return this.then(null, t)
							}
						};
						var tt = function () {
								var t;
								t = "undefined" != typeof global ? global : "undefined" != typeof window && window.document ? window : self;
								var e = "Promise" in t && "resolve" in t.Promise && "reject" in t.Promise && "all" in t.Promise && "race" in t.Promise && function () {
									var e;
									return new t.Promise(function (t) {
										e = t
									}), n(e)
								}();
								e || (t.Promise = Z)
							},
							et = {
								Promise: Z,
								polyfill: tt
							};
						"function" == typeof t && t.amd ? t(function () {
							return et
						}) : "undefined" != typeof i && i.exports ? i.exports = et : "undefined" != typeof this && (this.ES6Promise = et)
					}).call(this)
		}, {}],
				2: [function (t, e) {
					function i(t, e) {
						var i;
						return e = e || o, (i = e.requestAnimationFrame || e.webkitRequestAnimationFrame || e.mozRequestAnimationFrame || e.msRequestAnimationFrame || e.oRequestAnimationFrame || function () {
							e.setTimeout(function () {
								t(+new Date)
							}, 1e3 / 60)
						})(t)
					}

					function n(t, e) {
						return Math.sin(Math.PI / 2 * e) * t
					}

					function r(t, e, n, r, o) {
						function s() {
							var l = +new Date,
								u = l - a,
								c = Math.min(u / n, 1),
								d = r ? r(e, c) : e * c,
								h = 1 == c;
							t(d, h), h || i(s, o)
						}
						var a = +new Date;
						i(s)
					}
					var o = t("env/window");
					e.exports = {
						animate: r,
						requestAnimationFrame: i,
						easeOut: n
					}
		}, {
					"env/window": 14
		}],
				3: [function (t, e) {
					function i() {
						return l.builtUrl(c)
					}

					function n(t) {
						return "dark" === t ? "dark" : "light"
					}

					function r(t, e, i) {
						var r, o;
						return i = n(i), r = a.isRtlLang(e) ? "rtl" : "ltr", o = [t, u.css, i, r, "css"].join("."), l.base() + "/css/" + o
					}

					function o(t) {
						return function () {
							return s.isEnabled() ? t.apply(null, arguments) : i()
						}
					}
					var s = t("assets/refresh"),
						a = t("i18n/util"),
						l = t("tfw/util/assets"),
						u = t("var/thumbprints"),
						c = "embed/timeline.css";
					e.exports = {
						tweet: o(r.bind(null, "tweet")),
						timeline: i,
						video: o(r.bind(null, "video")),
						tweetRefresh: r.bind(null, "tweet")
					}
		}, {
					"assets/refresh": 4,
					"i18n/util": 20,
					"tfw/util/assets": 37,
					"var/thumbprints": 72
		}],
				4: [function (t, e) {
					function i() {
						return a.contains(r.location.hash, l)
					}

					function n() {
						return i() || s.asBoolean(o.val("widgets:new-embed-design"))
					}
					var r = t("env/window"),
						o = t("globals/pagemetadata"),
						s = t("util/typevalidator"),
						a = t("util/util"),
						l = "__twREFRESH__";
					e.exports = {
						isEnabled: n
					}
		}, {
					"env/window": 14,
					"globals/pagemetadata": 17,
					"util/typevalidator": 66,
					"util/util": 69
		}],
				5: [function (t, e) {
					function i(t) {
						return new RegExp("\\b" + t + "\\b", "g")
					}

					function n(t, e) {
						return t.classList ? void t.classList.add(e) : void(i(e).test(t.className) || (t.className += " " + e))
					}

					function r(t, e) {
						return t.classList ? void t.classList.remove(e) : void(t.className = t.className.replace(i(e), " "))
					}

					function o(t, e, i) {
						return void 0 === i && t.classList && t.classList.toggle ? t.classList.toggle(e, i) : (i ? n(t, e) : r(t, e), i)
					}

					function s(t, e, o) {
						return t.classList && a(t, e) ? (r(t, e), void n(t, o)) : void(t.className = t.className.replace(i(e), o))
					}

					function a(t, e) {
						return t.classList ? t.classList.contains(e) : i(e).test(t.className)
					}
					e.exports = {
						add: n,
						remove: r,
						replace: s,
						toggle: o,
						present: a
					}
		}, {}],
				6: [function (t, e) {
					function i(t) {
						var e = t.getAttribute("data-twitter-event-id");
						return e ? e : (t.setAttribute("data-twitter-event-id", ++m), m)
					}

					function n(t, e, i) {
						var n = 0,
							r = t && t.length || 0;
						for (n = 0; r > n; n++) t[n].call(e, i)
					}

					function r(t, e, i) {
						for (var o = i || t.target || t.srcElement, s = o.className.split(" "), a = 0, l = s.length; l > a; a++) n(e["." + s[a]], o, t);
						n(e[o.tagName], o, t), t.cease || o !== this && r.call(this, t, e, o.parentElement || o.parentNode)
					}

					function o(t, e, i, n) {
						function o(n) {
							r.call(t, n, i[e])
						}
						s(t, o, e, n), t.addEventListener(e, o, !1)
					}

					function s(t, e, i, n) {
						t.id && (p[t.id] = p[t.id] || [], p[t.id].push({
							el: t,
							listener: e,
							type: i,
							rootId: n
						}))
					}

					function a(t) {
						var e = p[t];
						e && (e.forEach(function (t) {
							t.el.removeEventListener(t.type, t.listener, !1), delete f[t.rootId]
						}), delete p[t])
					}

					function l(t, e, n, r) {
						var s = i(t);
						f[s] = f[s] || {}, f[s][e] || (f[s][e] = {}, o(t, e, f[s], s)), f[s][e][n] = f[s][e][n] || [], f[s][e][n].push(r)
					}

					function u(t, e, n) {
						var o = i(e),
							s = f[o] && f[o];
						r.call(e, {
							target: n
						}, s[t])
					}

					function c(t) {
						return h(t), d(t), !1
					}

					function d(t) {
						t && t.preventDefault ? t.preventDefault() : t.returnValue = !1
					}

					function h(t) {
						t && (t.cease = !0) && t.stopPropagation ? t.stopPropagation() : t.cancelBubble = !0
					}
					var f = {},
						m = -1,
						p = {};
					e.exports = {
						stop: c,
						stopPropagation: h,
						preventDefault: d,
						delegate: l,
						simulate: u,
						removeDelegatesForWidget: a
					}
		}, {}],
				7: [function (t, e) {
					function i(t) {
						var e = t.charAt(0);
						return "." === e ? function (e) {
							var i = e.className ? e.className.split(/\s+/) : [];
							return r.contains(i, t.slice(1))
						} : "#" === e ? function (e) {
							return e.id === t.slice(1)
						} : function (e) {
							return e.tagName === t.toUpperCase()
						}
					}

					function n(t, e, o) {
						var s;
						if (e) return o = o || e && e.ownerDocument, s = r.isType("function", t) ? t : i(t), e === o ? s(e) ? e : void 0 : s(e) ? e : n(s, e.parentNode, o)
					}
					var r = t("util/util");
					e.exports = {
						closest: n
					}
		}, {
					"util/util": 69
		}],
				8: [function (t, e) {
					function i(t) {
						return t = t || n, t.getSelection && t.getSelection().toString()
					}
					var n = t("env/window");
					e.exports = {
						getSelection: i
					}
		}, {
					"env/window": 14
		}],
				9: [function (t, e) {
					function i(t) {
						return t && 1 === t.nodeType ? t.offsetWidth || i(t.parentNode) : 0
					}
					e.exports = {
						effectiveWidth: i
					}
		}, {}],
				10: [function (t, e) {
					function i(t, e, i) {
						for (var n, r = [], o = 0; n = i[o]; o++) r.push(n[0]), r.push(n[1]);
						return t + e + r.join(":")
					}

					function n(t) {
						var e = t || "";
						return e.replace(/([A-Z])/g, function (t) {
							return "-" + t.toLowerCase()
						})
					}
					var r = t("env/document"),
						o = {};
					e.exports = function (t, e, s) {
						var a, l = r.createElement("span"),
							u = {},
							c = "",
							d = 0,
							h = 0,
							f = [];
						if (s = s || [], e = e || "", c = i(t, e, s), o[c]) return o[c];
						l.className = e + " twitter-measurement";
						try {
							for (; a = s[d]; d++) l.style[a[0]] = a[1]
						} catch (m) {
							for (; a = s[h]; h++) f.push(n(a[0]) + ":" + a[1]);
							l.setAttribute("style", f.join(";") + ";")
						}
						return l.innerHTML = t, r.body.appendChild(l), u.width = l.clientWidth || l.offsetWidth, u.height = l.clientHeight || l.offsetHeight, r.body.removeChild(l), l = null, o[c] = u
					}
		}, {
					"env/document": 11
		}],
				11: [function (t, e) {
					e.exports = document
		}, {}],
				12: [function (t, e) {
					e.exports = location
		}, {}],
				13: [function (t, e) {
					e.exports = navigator
		}, {}],
				14: [function (t, e) {
					e.exports = window
		}, {}],
				15: [function (t, e) {
					function i(t, e, i) {
						e.ready = t.then.bind(t), i && Array.isArray(e[i]) && (e[i].forEach(t.then.bind(t)), delete e[i])
					}
					e.exports = {
						exposeReadyPromise: i
					}
		}, {}],
				16: [function (t, e) {
					function i(t) {
						return s.isType("string", t) ? t.split(".") : s.isType("array", t) ? t : []
					}

					function n(t, e) {
						var n = i(e),
							r = n.slice(0, -1);
						return r.reduce(function (t, e, i) {
							if (t[e] = t[e] || {}, !s.isObject(t[e])) throw new Error(r.slice(0, i + 1).join(".") + " is already defined with a value.");
							return t[e]
						}, t)
					}

					function r(t, e) {
						e = e || o, e[t] = e[t] || {}, Object.defineProperty(this, "base", {
							value: e[t]
						}), Object.defineProperty(this, "name", {
							value: t
						})
					}
					var o = t("env/window"),
						s = t("util/util");
					s.aug(r.prototype, {
						get: function (t) {
							var e = i(t);
							return e.reduce(function (t, e) {
								return s.isObject(t) ? t[e] : void 0
							}, this.base)
						},
						set: function (t, e, r) {
							var o = i(t),
								s = n(this.base, t),
								a = o.slice(-1);
							return r && a in s ? s[a] : s[a] = e
						},
						init: function (t, e) {
							return this.set(t, e, !0)
						},
						unset: function (t) {
							var e = i(t),
								n = this.get(e.slice(0, -1));
							n && delete n[e.slice(-1)]
						},
						aug: function (t) {
							var e = this.get(t),
								i = s.toRealArray(arguments).slice(1);
							if (e = "undefined" != typeof e ? e : {}, i.unshift(e), !i.every(s.isObject)) throw new Error("Cannot augment non-object.");
							return this.set(t, s.aug.apply(null, i))
						},
						call: function (t) {
							var e = this.get(t),
								i = s.toRealArray(arguments).slice(1);
							if (!s.isType("function", e)) throw new Error("Function " + t + "does not exist.");
							return e.apply(null, i)
						},
						fullPath: function (t) {
							var e = i(t);
							return e.unshift(this.name), e.join(".")
						}
					}), e.exports = r
		}, {
					"env/window": 14,
					"util/util": 69
		}],
				17: [function (t, e) {
					function i(t) {
						var e, i, n, s = 0;
						for (r = {}, t = t || o, e = t.getElementsByTagName("meta"); i = e[s]; s++) / ^ twitter: /.test(i.name)&&(n=i.name.replace(/ ^ twitter: /,""),r[n]=i.content)}function n(t){return r[t]}var r,o=t("env/document
						");i(),e.exports={init:i,val:n}},{"
						env / document ":11}],18:[function(t,e){var i=t("
						globals / object ");e.exports=new i("
						__twttr ")},{"
						globals / object ":16}],19:[function(t,e){var i=t("
						globals / object ");e.exports=new i("
						twttr ")},{"
						globals / object ":16}],20:[function(t,e){function i(t){return t=String(t).toLowerCase(),n.contains(r,t)}var n=t("
						util / util "),r=["
						ar ","
						fa ","
						he ","
						ur "];e.exports={isRtlLang:i}},{"
						util / util ":69}],21:[function(t,e){function i(t){var e=~o.host.indexOf("
						poptip.com ")?"
						https: //poptip.com":o.href,i="original_referer="+e;return[t,i].join(-1==t.indexOf("?")?"?":"&")}function n(t){var e,n;t.altKey||t.metaKey||t.shiftKey||(e=a.closest(function(t){return"A"===t.tagName||"AREA"===t.tagName},t.target),e&&u.isIntentURL(e.href)&&(n=i(e.href),n=n.replace(/ ^ http[: ] / , "https:"), n = n.replace(/^\/\//, "https://"), l.open(n, e), s.preventDefault(t)))
			}

			function r(t) {
				t.addEventListener("click", n, !1)
			}
			var o = t("env/location"), s = t("dom/delegate"), a = t("dom/get"), l = t("tfw/widget/intent"), u = t("util/twitter"); e.exports = {
				attachTo: r
			}
		}, {
			"dom/delegate": 6,
			"dom/get": 7,
			"env/location": 12,
			"tfw/widget/intent": 45,
			"util/twitter": 65
		}], 22: [function (t, e) {
			function i(t) {
				var e = [];
				return d.forIn(t, function (t, i) {
					e.push(t + "=" + i)
				}), e.join(",")
			}

			function n() {
				return h + c.generate()
			}

			function r(t, e) {
				function i(t) {
					return Math.round(t / 2)
				}
				return t > e ? {
					coordinate: 0,
					size: e
				} : {
					coordinate: i(e) - i(t),
					size: t
				}
			}

			function o(t, e, n) {
				var o, a;
				e = s.parse(e), n = n || {}, o = r(e.width, n.width || f), e.left = o.coordinate, e.width = o.size, a = r(e.height, n.height || m), e.top = a.coordinate, e.height = a.size, this.win = t, this.features = i(e)
			}
			var s, a = t("env/window"),
				l = t("util/options_parser"),
				u = t("util/twitter"),
				c = t("util/uid"),
				d = t("util/util"),
				h = "intent_",
				f = a.screen.width,
				m = a.screen.height;
			s = (new l).defaults({
				width: 550,
				height: 520,
				personalbar: "0",
				toolbar: "0",
				location: "1",
				scrollbars: "1",
				resizable: "1"
			}), o.prototype.open = function (t) {
				return u.isTwitterURL(t) ? (this.name = n(), this.popup = this.win.open(t, this.name, this.features), this) : void 0
			}, o.open = function (t, e) {
				var i = new o(a, e);
				return i.open(t)
			}, e.exports = o
		}, {
			"env/window": 14,
			"util/options_parser": 60,
			"util/twitter": 65,
			"util/uid": 67,
			"util/util": 69
		}], 23: [function (t, e) {
			function i(t) {
				l[t] = +new Date
			}

			function n(t) {
				return l[t] ? +new Date - l[t] : null
			}

			function r(t, e, i, r, s) {
				var a = n(e);
				a && o(t, i, r, a, s)
			}

			function o(t, e, i, n, r) {
				var o, l = void 0 === r ? u : r;
				100 * Math.random() > l || (i = a.aug(i || {}, {
					duration_ms: n
				}), o = {
					page: e,
					component: "performance",
					action: t
				}, s.clientEvent(o, i, !0))
			}
			var s = t("scribe/pixel"),
				a = t("util/util"),
				l = {},
				u = 1;
			e.exports = {
				start: i,
				end: n,
				track: o,
				endAndTrack: r
			}
		}, {
			"scribe/pixel": 32,
			"util/util": 69
		}], 24: [function (t, e) {
			e.exports = {
				PARSE_ERROR: {
					code: -32700,
					message: "Parse error"
				},
				INVALID_REQUEST: {
					code: -32600,
					message: "Invalid Request"
				},
				INVALID_PARAMS: {
					code: -32602,
					message: "Invalid params"
				},
				METHOD_NOT_FOUND: {
					code: -32601,
					message: "Method not found"
				},
				INTERNAL_ERROR: {
					code: -32603,
					message: "Internal error"
				}
			}
		}, {}], 25: [function (t, e) {
			function i(t) {
				this.registry = t || {}
			}

			function n(t) {
				return d.isType("string", t) ? JSON.parse(t) : t
			}

			function r(t) {
				var e, i, n;
				return d.isObject(t) ? (e = t.jsonrpc === f, i = d.isType("string", t.method), n = !("id" in t) || o(t.id), e && i && n) : !1
			}

			function o(t) {
				var e, i, n;
				return e = d.isType("string", t), i = d.isType("number", t), n = null === t, e || i || n
			}

			function s(t) {
				return d.isObject(t) && !d.isType("function", t)
			}

			function a(t, e) {
				return {
					jsonrpc: f,
					id: t,
					result: e
				}
			}

			function l(t, e) {
				return {
					jsonrpc: f,
					id: o(t) ? t : null,
					error: e
				}
			}

			function u(t) {
				return h.every.apply(h, t).then(function (t) {
					return t = t.filter(function (t) {
						return void 0 !== t
					}), t.length ? t : void 0
				})
			}
			var c = t("rpc/jsonrpc/errors"),
				d = t("util/util"),
				h = t("util/promise"),
				f = "2.0";
			i.prototype._invoke = function (t, e) {
				var i, n, r;
				i = this.registry[t.method], n = t.params || [], n = d.isType("array", n) ? n : [n];
				try {
					r = i.apply(e.source || null, n)
				} catch (o) {
					r = h.reject(o.message)
				}
				return h.isThenable(r) ? r : h.fulfill(r)
			}, i.prototype._processRequest = function (t, e) {
				function i(e) {
					return a(t.id, e)
				}

				function n() {
					return l(t.id, c.INTERNAL_ERROR)
				}
				var o;
				return r(t) ? (o = "params" in t && !s(t.params) ? h.fulfill(l(t.id, c.INVALID_PARAMS)) : this.registry[t.method] ? this._invoke(t, {
					source: e
				}).then(i, n) : h.fulfill(l(t.id, c.METHOD_NOT_FOUND)), null != t.id ? o : h.fulfill()) : h.fulfill(l(t.id, c.INVALID_REQUEST))
			}, i.prototype.attachReceiver = function (t) {
				return t.attachTo(this), this
			}, i.prototype.bind = function (t, e) {
				return this.registry[t] = e, this
			}, i.prototype.receive = function (t, e) {
				var i, r, o, s = this;
				try {
					t = n(t)
				} catch (a) {
					return h.fulfill(l(null, c.PARSE_ERROR))
				}
				return e = e || null, i = d.isType("array", t), r = i ? t : [t], o = r.map(function (t) {
					return s._processRequest(t, e)
				}), i ? u(o) : o[0]
			}, e.exports = i
		}, {
			"rpc/jsonrpc/errors": 24,
			"util/promise": 62,
			"util/util": 69
		}], 26: [function (t, e) {
			function i(t, e) {
				t && t.postMessage && (e = h ? JSON.stringify(e) : e, t.postMessage(e, "*"))
			}

			function n(t) {
				var e = t.document;
				this.server = null, this.isTwitterFrame = d.isTwitterURL(e.location.href), t.addEventListener("message", this._onMessage.bind(this), !1)
			}

			function r(t) {
				this.pending = {}, this.target = t, this.isTwitterHost = d.isTwitterURL(s.href), a.addEventListener("message", this._onMessage.bind(this), !1)
			}

			function o(t) {
				return arguments.length > 0 && (h = !!t), h
			}
			var s = t("env/location"),
				a = t("env/window"),
				l = t("util/env"),
				u = t("util/util"),
				c = t("util/promise"),
				d = t("util/twitter"),
				h = l.ie9();
			u.aug(n.prototype, {
				_onMessage: function (t) {
					this.server && (!this.isTwitterFrame || d.isTwitterURL(t.origin)) && this.server.receive(t.data, t.source).then(function (e) {
						e && i(t.source, e)
					})
				},
				attachTo: function (t) {
					this.server = t
				},
				detach: function () {
					this.server = null
				}
			}), u.aug(r.prototype, {
				_processResponse: function (t) {
					var e = this.pending[t.id];
					e && (e.fulfill(t), delete this.pending[t.id])
				},
				_onMessage: function (t) {
					var e = t.data;
					if (!this.isTwitterHost || d.isTwitterURL(t.origin)) {
						if (u.isType("string", e)) try {
							e = JSON.parse(e)
						} catch (i) {
							return
						}
						e = u.isType("array", e) ? e : [e], e.forEach(this._processResponse.bind(this))
					}
				},
				send: function (t) {
					var e, n = this.pending;
					return e = t.id ? new c(function (e) {
						n[t.id] = e
					}) : c.fulfill(), i(this.target, t), e
				}
			}), e.exports = {
				Receiver: n,
				Dispatcher: r,
				_stringifyPayload: o
			}
		}, {
			"env/location": 12,
			"env/window": 14,
			"util/env": 55,
			"util/promise": 62,
			"util/twitter": 65,
			"util/util": 69
		}], 27: [function (t, e) {
			function i(t, e, i, r) {
				var a, l = this;
				this.readyPromise = new s(function (t) {
					l.resolver = t
				}), this.attrs = t || {}, this.styles = e || {}, this.appender = i || function (t) {
					n.body.appendChild(t)
				}, this.layout = r || function (t) {
					return new s(function (e) {
						return e.fulfill(t())
					})
				}, this.frame = a = o(this.attrs, this.styles), a.onreadystatechange = a.onload = this.getCallback(this.onLoad), this.layout(function () {
					l.appender(a)
				})
			}
			var n = t("env/document"),
				r = t("util/env"),
				o = t("util/iframe"),
				s = t("util/promise"),
				a = t("globals/private"),
				l = 0;
			i.prototype.getCallback = function (t) {
				var e = this,
					i = !1;
				return function () {
					i || (i = !0, t.call(e))
				}
			}, i.prototype.registerCallback = function (t) {
				var e = "cb" + l++;
				return a.set(["sandbox", e], t), e
			}, i.prototype.onLoad = function () {
				try {
					this.document = this.frame.contentWindow.document
				} catch (t) {
					return void this.setDocDomain()
				}
				this.writeStandardsDoc(), this.resolver.fulfill(this)
			}, i.prototype.ready = function () {
				return this.readyPromise
			}, i.prototype.setDocDomain = function () {
				var t = this,
					e = o(this.attrs, this.styles),
					i = this.registerCallback(this.getCallback(this.onLoad));
				e.src = ["javascript:", 'document.write("");', "try { window.parent.document; }", "catch (e) {", 'document.domain="' + n.domain + '";', "}", "window.parent." + a.fullPath(["sandbox", i]) + "();"].join(""), this.layout(function () {
					t.frame.parentNode.removeChild(t.frame), t.frame = null, t.appender ? t.appender(e) : n.body.appendChild(e), t.frame = e
				})
			}, i.prototype.writeStandardsDoc = function () {
				if (r.anyIE() && !r.cspEnabled()) {
					var t = ["<!DOCTYPE html>", "<html>", "<head>", "<scr", "ipt>", "try { window.parent.document; }", 'catch (e) {document.domain="' + n.domain + '";}', "</scr", "ipt>", "</head>", "<body></body>", "</html>"].join("");
					this.document.write(t), this.document.close()
				}
			}, e.exports = i
		}, {
			"env/document": 11,
			"globals/private": 18,
			"util/env": 55,
			"util/iframe": 57,
			"util/promise": 62
		}], 28: [function (t, e) {
			function i() {
				var t, e;
				w = {}, o || (t = s.body.offsetHeight, e = s.body.offsetWidth, (t != b || e != v) && (g.forEach(function (t) {
					t.dispatchFrameResize(v, b)
				}), b = t, v = e))
			}

			function n(t) {
				var e;
				return t.id ? t.id : (e = t.getAttribute("data-twttr-id")) ? e : (e = "twttr-sandbox-" + p++, t.setAttribute("data-twttr-id", e), e)
			}

			function r(t, e) {
				var i = this;
				u.apply(this, [t, e]), this._resizeHandlers = [], g = g.filter(function (t) {
					var e = t._frame.parentElement;
					return e || h.async(function () {
						f.removeDelegatesForWidget(t._frame.id)
					}), e
				}), g.push(this), this._win.addEventListener("resize", function () {
					i.dispatchFrameResize()
				}, !1)
			}
			var o, s = t("env/document"),
				a = t("env/window"),
				l = t("sandbox/baseframe"),
				u = t("sandbox/minimal"),
				c = t("util/env"),
				d = t("util/promise"),
				h = t("util/util"),
				f = t("dom/delegate"),
				m = t("dom/classname"),
				p = 0,
				g = [],
				w = {},
				v = 0,
				b = 0;
			a.addEventListener("resize", i, !1), r.prototype = new u, h.aug(r.prototype, {
				dispatchFrameResize: function () {
					var t = this._frame.parentNode,
						e = n(t),
						i = w[e];
					o = !0, this._resizeHandlers.length && (i || (i = w[e] = {
						w: this._frame.offsetWidth,
						h: this._frame.offsetHeight
					}), (this._frameWidth != i.w || this._frameHeight != i.h) && (this._frameWidth = i.w, this._frameHeight = i.h, this._resizeHandlers.forEach(function (t) {
						t(i.w, i.h)
					}), a.setTimeout(function () {
						w = {}
					}, 50)))
				},
				addClass: function (t) {
					var e = this._doc.documentElement;
					return this.layout(function () {
						m.add(e, t)
					})
				},
				appendStyleSheet: function (t) {
					var e = this,
						i = this._doc.createElement("link");
					return i.type = "text/css", i.rel = "stylesheet", i.href = t, this.layout(function () {
						return e._head.appendChild(i)
					})
				},
				removeStyleSheet: function (t) {
					var e, i = this;
					return e = 'link[rel="stylesheet"][href="' + t + '"]', this.layout(function () {
						var t = i._doc.querySelector(e);
						return t && i._head.removeChild(t)
					})
				},
				appendCss: function (t) {
					var e, i = this;
					return c.cspEnabled() ? d.reject("CSP enabled; cannot embed inline styles.") : (e = this._doc.createElement("style"), e.type = "text/css", e.styleSheet ? e.styleSheet.cssText = t : e.appendChild(this._doc.createTextNode(t)), this.layout(function () {
						return i._head.appendChild(e)
					}))
				},
				style: function (t, e) {
					var i = this;
					return this.layout(function () {
						e && (i._frame.style.cssText = ""), h.forIn(t, function (t, e) {
							i._frame.style[t] = e
						})
					})
				},
				onresize: function (t) {
					this._resizeHandlers.push(t)
				},
				width: function (t) {
					return void 0 !== t && (this._frame.style.width = t + "px"), c.ios() ? Math.min(this._frame.parentNode.offsetWidth, this._frame.offsetWidth) : this._frame.offsetWidth
				},
				height: function (t) {
					return void 0 !== t && (this._frame.height = t), this._frame.offsetHeight
				},
				contentHeight: function () {
					return this._doc.body.firstChild.offsetHeight
				},
				resizeToContent: function () {
					var t = this;
					return this.layout(function () {
						return t.height(t.contentHeight())
					})
				}
			}), r.createSandbox = function (t, e, i, n) {
				var o = new l(t, e, i, n);
				return o.ready().then(function (t) {
					return new r(t.frame, t.layout)
				})
			}, e.exports = r
		}, {
			"dom/classname": 5,
			"dom/delegate": 6,
			"env/document": 11,
			"env/window": 14,
			"sandbox/baseframe": 27,
			"sandbox/minimal": 29,
			"util/env": 55,
			"util/promise": 62,
			"util/util": 69
		}], 29: [function (t, e) {
			function i(t, e) {
				t && (this._frame = t, this._win = t.contentWindow, this._doc = this._win.document, this._body = this._doc.body, this._head = this._body.parentNode.children[0], this.layout = e, this._doc.documentElement.className = "SandboxRoot")
			}
			var n = t("sandbox/baseframe"),
				r = t("util/util");
			r.aug(i.prototype, {
				createElement: function (t) {
					return this._doc.createElement(t)
				},
				createDocumentFragment: function () {
					return this._doc.createDocumentFragment()
				},
				appendChild: function (t) {
					var e = this;
					return this.layout(function () {
						return e._body.appendChild(t)
					})
				},
				setBaseTarget: function (t) {
					var e = this,
						i = this._doc.createElement("base");
					return i.target = t, this.layout(function () {
						return e._head.appendChild(i)
					})
				},
				setTitle: function (t) {
					t && (this._frame.title = t)
				},
				element: function () {
					return this._frame
				},
				document: function () {
					return this._doc
				}
			}), i.createSandbox = function (t, e, r, o) {
				var s = new n(t, e, r, o);
				return s.ready().then(function (t) {
					return new i(t.frame, t.layout)
				})
			}, e.exports = i
		}, {
			"sandbox/baseframe": 27,
			"util/util": 69
		}], 30: [function (t, e) {
			function i() {
				return u.formatGenericEventData("syndicated_impression", {})
			}

			function n() {
				a("tweet")
			}

			function r() {
				a("timeline")
			}

			function o() {
				a("video")
			}

			function s() {
				a("partnertweet")
			}

			function a(t) {
				c.isHostPageSensitive() || d[t] || (d[t] = !0, l.scribe(u.formatClientEventNamespace({
					page: t,
					action: "impression"
				}), i(), u.AUDIENCE_ENDPOINT))
			}
			var l = t("scribe/pixel"),
				u = t("scribe/util"),
				c = t("util/tld"),
				d = {};
			e.exports = {
				scribePartnerTweetAudienceImpression: s,
				scribeTweetAudienceImpression: n,
				scribeTimelineAudienceImpression: r,
				scribeVideoAudienceImpression: o,
				resetTracking: function () {
					d = {}
				}
			}
		}, {
			"scribe/pixel": 32,
			"scribe/util": 33,
			"util/tld": 64
		}], 31: [function (t, e) {
			function i() {
				return A ? E : (p.createSandbox({
					id: "rufous-sandbox"
				}, {
					display: "none"
				}).then(function (t) {
					d = t, u = a(), c = l(), h.fulfill([u, c])
				}), A = !0, E)
			}

			function n(t, e) {
				var i, n, r;
				v.isObject(t) && v.isObject(e) && (r = w.flattenClientEventPayload(t, e), i = u.firstChild, i.value = +(+i.value || r.dnt || 0), n = d.createElement("input"), n.type = "hidden", n.name = "l", n.value = w.stringify(r), u.appendChild(n))
			}

			function r(t, e, i) {
				var r = !v.isObject(t),
					o = e ? !v.isObject(e) : !1;
				r || o || E.then(function () {
					n(w.formatClientEventNamespace(t), w.formatClientEventData(e, i))
				})
			}

			function o() {
				return E.then(function () {
					if (u.children.length <= 2) return g.reject();
					var t = g.every(d.appendChild(u), d.appendChild(c)).then(function (t) {
						var e = t[0],
							i = t[1];
						return i.addEventListener("load", function () {
							s(e, i)(), b.get("events").trigger("logFlushed")
						}), e.submit(), t
					});
					return u = a(), c = l(), t
				})
			}

			function s(t, e) {
				return function () {
					var i = t.parentNode;
					i && (i.removeChild(t), i.removeChild(e))
				}
			}

			function a() {
				var t = d.createElement("form"),
					e = d.createElement("input"),
					i = d.createElement("input");
				return x++, t.action = w.CLIENT_EVENT_ENDPOINT, t.method = "POST", t.target = _ + x, t.id = T + x, e.type = "hidden", e.name = "dnt", e.value = m.enabled(), i.type = "hidden", i.name = "tfw_redirect", i.value = w.RUFOUS_REDIRECT, t.appendChild(e), t.appendChild(i), t
			}

			function l() {
				var t = _ + x;
				return f({
					id: t,
					name: t,
					width: 0,
					height: 0,
					border: 0
				}, {
					display: "none"
				}, d.document())
			}
			var u, c, d, h, f = t("util/iframe"),
				m = t("util/donottrack"),
				p = t("sandbox/minimal"),
				g = t("util/promise"),
				w = t("scribe/util"),
				v = t("util/util"),
				b = t("globals/twttr"),
				y = Math.floor(1e3 * Math.random()) + "_",
				_ = "rufous-frame-" + y + "-",
				T = "rufous-form-" + y + "-",
				x = 0,
				A = !1,
				E = new g(function (t) {
					h = t
				});
			e.exports = {
				clientEvent: r,
				flush: o,
				init: i
			}
		}, {
			"globals/twttr": 19,
			"sandbox/minimal": 29,
			"scribe/util": 33,
			"util/donottrack": 54,
			"util/iframe": 57,
			"util/promise": 62,
			"util/util": 69
		}], 32: [function (t, e) {
			function i(t, e, i) {
				return n(t, e, i, 2)
			}

			function n(t, e, i, n) {
				var r = !f.isObject(t),
					s = e ? !f.isObject(e) : !1;
				r || s || o(h.formatClientEventNamespace(t), h.formatClientEventData(e, i, n), h.CLIENT_EVENT_ENDPOINT)
			}

			function r(t, e, i, r) {
				var o = h.extractTermsFromDOM(t.target || t.srcElement);
				o.action = r || "click", n(o, e, i)
			}

			function o(t, e, i) {
				var n, r;
				i && f.isObject(t) && f.isObject(e) && (n = h.flattenClientEventPayload(t, e), r = {
					l: h.stringify(n)
				}, n.dnt && (r.dnt = 1), u(d.url(i, r)))
			}

			function s(t, e, i, n) {
				var r, o = !f.isObject(t),
					s = e ? !f.isObject(e) : !1;
				if (!o && !s) return r = h.flattenClientEventPayload(h.formatClientEventNamespace(t), h.formatClientEventData(e, i, n)), a(r)
			}

			function a(t) {
				return p.push(t), p
			}

			function l() {
				var t, e, i = d.url(h.CLIENT_EVENT_ENDPOINT, {
						dnt: 0,
						l: ""
					}),
					n = encodeURIComponent(i).length;
				return p.length > 1 && s({
					page: "widgets_js",
					component: "scribe_pixel",
					action: "batch_log"
				}, {}), t = p, p = [], e = t.reduce(function (e, i, r) {
					var o, s, a = e.length,
						l = a && e[a - 1],
						u = r + 1 == t.length;
					return u && i.event_namespace && "batch_log" == i.event_namespace.action && (i.message = ["entries:" + r, "requests:" + a].join("/")), o = h.stringify(i), s = encodeURIComponent(o).length + 3, n + s > m ? e : ((!l || l.urlLength + s > m) && (l = {
						urlLength: n,
						items: []
					}, e.push(l)), l.urlLength += s, l.items.push(o), e)
				}, []), e.map(function (t) {
					var e = {
						l: t.items
					};
					return c.enabled() && (e.dnt = 1), u(d.url(h.CLIENT_EVENT_ENDPOINT, e))
				})
			}

			function u(t) {
				var e = new Image;
				return e.src = t
			}
			var c = t("util/donottrack"),
				d = t("util/querystring"),
				h = t("scribe/util"),
				f = t("util/util"),
				m = 2083,
				p = [];
			e.exports = {
				_enqueueRawObject: a,
				scribe: o,
				clientEvent: n,
				clientEvent2: i,
				enqueueClientEvent: s,
				flushClientEvents: l,
				interaction: r
			}
		}, {
			"scribe/util": 33,
			"util/donottrack": 54,
			"util/querystring": 63,
			"util/util": 69
		}], 33: [function (t, e) {
			function i(t, e) {
				var n;
				return e = e || {}, t && t.nodeType === Node.ELEMENT_NODE ? ((n = t.getAttribute("data-scribe")) && n.split(" ").forEach(function (t) {
					var i = t.trim().split(":"),
						n = i[0],
						r = i[1];
					n && r && !e[n] && (e[n] = r)
				}), i(t.parentNode, e)) : e
			}

			function n(t) {
				return c.aug({
					client: "tfw"
				}, t || {})
			}

			function r(t, e, i) {
				var n = t && t.widget_origin || l.referrer;
				return t = o("tfw_client_event", t, n), t.client_version = f, t.format_version = void 0 !== i ? i : 1, e || (t.widget_origin = n), t
			}

			function o(t, e, i) {
				return e = e || {}, c.aug(e, {
					_category_: t,
					triggered_on: e.triggered_on || +new Date,
					dnt: u.enabled(i)
				})
			}

			function s(t, e) {
				return c.aug({}, e, {
					event_namespace: t
				})
			}

			function a(t) {
				var e, i = Array.prototype.toJSON;
				return delete Array.prototype.toJSON, e = JSON.stringify(t), i && (Array.prototype.toJSON = i), e
			}
			var l = t("env/document"),
				u = t("util/donottrack"),
				c = t("util/util"),
				d = t("var/build"),
				h = t("globals/private"),
				f = d.version,
				m = h.get("endpoints.rufous") || "https://syndication.twitter.com/i/jot",
				p = h.get("endpoints.rufousAudience") || "https://syndication.twitter.com/i/jot/syndication",
				g = h.get("endpoints.rufousRedirect") || "https://platform.twitter.com/jot.html";
			e.exports = {
				extractTermsFromDOM: i,
				flattenClientEventPayload: s,
				formatGenericEventData: o,
				formatClientEventData: r,
				formatClientEventNamespace: n,
				stringify: a,
				AUDIENCE_ENDPOINT: p,
				CLIENT_EVENT_ENDPOINT: m,
				RUFOUS_REDIRECT: g
			}
		}, {
			"env/document": 11,
			"globals/private": 18,
			"util/donottrack": 54,
			"util/util": 69,
			"var/build": 71
		}], 34: [function (t, e) {
			function i(t, e, i, n) {
				return t = t || [], i = i || {},
					function () {
						var r, a, u, c, d = Array.prototype.slice.apply(arguments, [0, t.length]),
							h = Array.prototype.slice.apply(arguments, [t.length]);
						return h.forEach(function (t) {
							return t ? 1 === t.nodeType ? void(u = t) : o.isType("function", t) ? void(r = t) : void(o.isType("object", t) && (a = t)) : void 0
						}), d.length != t.length || 0 === h.length ? (r && o.async(function () {
							r(!1)
						}), s.reject("Not enough parameters")) : u ? (a = o.aug(a || {}, i), a.targetEl = u, t.forEach(function (t) {
							a[t] = d.shift()
						}), c = new e(a), l.doLayout(), c.render(), n && n(), r && c.completed().then(r, function () {
							r(!1)
						}), c.completed()) : (r && o.async(function () {
							r(!1)
						}), s.reject("No target specified"))
					}
			}

			function n(t) {
				var e;
				t.linkColor = t.linkColor || t.previewParams.link_color, t.theme = t.theme || t.previewParams.theme, t.height = t.height || t.previewParams.height, e = new f(t), this.render = e.render.bind(e), this.completed = e.completed.bind(e)
			}
			var r = t("env/window"),
				o = t("util/util"),
				s = t("util/promise"),
				a = t("util/twitter"),
				l = t("tfw/widget/base"),
				u = t("tfw/widget/tweetbutton"),
				c = t("tfw/widget/follow"),
				d = t("tfw/widget/embed"),
				h = t("tfw/widget/video"),
				f = t("tfw/widget/timeline"),
				m = i(["url"], u, {
					type: "share"
				}),
				p = i(["hashtag"], u, {
					type: "hashtag"
				}),
				g = i(["screenName"], u, {
					type: "mention"
				}),
				w = i(["screenName"], c),
				v = i(["tweetId"], d, {}, d.fetchAndRender),
				b = i(["tweetId"], h, {}, h.fetchAndRender),
				y = i(["widgetId"], f),
				_ = i(["previewParams"], n),
				T = {
					createShareButton: m,
					createMentionButton: g,
					createHashtagButton: p,
					createFollowButton: w,
					createTweet: v,
					createVideo: b,
					createTweetEmbed: v,
					createTimeline: y
				};
			a.isTwitterURL(r.location.href) && (T.createTimelinePreview = _), e.exports = T
		}, {
			"env/window": 14,
			"tfw/widget/base": 42,
			"tfw/widget/embed": 43,
			"tfw/widget/follow": 44,
			"tfw/widget/timeline": 47,
			"tfw/widget/tweetbutton": 48,
			"tfw/widget/video": 49,
			"util/promise": 62,
			"util/twitter": 65,
			"util/util": 69
		}],
		35: [function (t, e) {
			function i(t, e) {
				var i = l.connect({
					src: t,
					iframe: {
						name: e,
						style: "position:absolute;top:-9999em;width:10px;height:10px"
					}
				});
				return u(i).expose({
					trigger: function (t, e, i) {
						e = e || {};
						var n = e.region;
						delete e.region, h.get("events").trigger(t, {
							target: c.find(i),
							data: e,
							region: n,
							type: t
						})
					},
					initXPHub: function () {
						r(!0)
					}
				}), i
			}

			function n(t) {
				return t ? d.secureHubId : d.contextualHubId
			}

			function r(t) {
				var e = a.base(t) + "/widgets/hub.fc14798fe2fa0e727916eda9fa1be224.html",
					r = n(t);
				if (!s.getElementById(r)) return i(e, r)
			}

			function o(t, e) {
				var i = l.connect({
					window: {
						width: 550,
						height: 450
					},
					src: t
				});
				u(i).expose({
					trigger: function (t, i) {
						h.get("events").trigger(t, {
							target: e,
							region: "intent",
							type: t,
							data: i
						})
					}
				})
			}
			var s = t("env/document"),
				a = t("tfw/util/assets"),
				l = t("xd/parent"),
				u = t("xd/jsonrpc"),
				c = t("tfw/widget/base"),
				d = t("util/widgetrpc"),
				h = t("globals/twttr");
			e.exports = {
				init: r,
				openIntent: o
			}
		}, {
			"env/document": 11,
			"globals/twttr": 19,
			"tfw/util/assets": 37,
			"tfw/widget/base": 42,
			"util/widgetrpc": 70,
			"xd/jsonrpc": 77,
			"xd/parent": 78
		}],
		36: [function (t, e) {
			function i(t) {
				return t = t || n, t.top.postMessage ? t === t.top ? void t.addEventListener("message", function (t) {
					var e;
					if (!t.data || "{" == t.data[0]) {
						try {
							e = JSON.parse(t.data)
						} catch (i) {}
						e && "twttr:private:requestArticleUrl" == e.name && t.source.postMessage(JSON.stringify({
							name: "twttr:private:provideArticleUrl",
							data: {
								url: r.rootDocumentLocation(),
								dnt: o.enabled()
							}
						}), "*")
					}
				}, !1) : (t.addEventListener("message", function (t) {
					var e;
					if (!t.data || "{" == t.data[0]) {
						try {
							e = JSON.parse(t.data)
						} catch (i) {}
						if (e && "twttr:private:provideArticleUrl" == e.name) {
							if (!e.data) return;
							r.rootDocumentLocation(e.data.url), e.data.dnt && o.setOn()
						}
					}
				}, !1), void t.top.postMessage(JSON.stringify({
					name: "twttr:private:requestArticleUrl"
				}), "*")) : void 0
			}
			var n = t("env/window"),
				r = t("util/document"),
				o = t("util/donottrack");
			e.exports = {
				requestArticleUrl: i
			}
		}, {
			"env/window": 14,
			"util/document": 52,
			"util/donottrack": 54
		}],
		37: [function (t, e) {
			function i(t, e) {
				var i, o = l[t];
				return "embed/timeline.css" === t && a.contains(r.href, "localhost.twitter.com") ? "/node_modules/syndication-templates/lib/css/index.css" : (i = s.retina() ? "2x" : "default", e && (i += ".rtl"), n() + "/" + o[i])
			}

			function n(t) {
				var e = o.get("host");
				return u(t) + "://" + e
			}
			var r = t("env/location"),
				o = t("globals/private"),
				s = t("util/env"),
				a = t("util/util"),
				l = {
					"embed/timeline.css": {
						"default": "embed/timeline.e29dd159fa96a0aa7d51146cd88dc050.default.css",
						"2x": "embed/timeline.e29dd159fa96a0aa7d51146cd88dc050.2x.css",
						gif: "embed/timeline.e29dd159fa96a0aa7d51146cd88dc050.gif.css",
						"default.rtl": "embed/timeline.e29dd159fa96a0aa7d51146cd88dc050.default.rtl.css",
						"2x.rtl": "embed/timeline.e29dd159fa96a0aa7d51146cd88dc050.2x.rtl.css",
						"gif.rtl": "embed/timeline.e29dd159fa96a0aa7d51146cd88dc050.gif.rtl.css"
					}
				},
				u = function () {
					return /^http\:$/.test(r.protocol) ? function (t) {
						return t ? "https" : "http"
					} : function () {
						return "https"
					}
				}();
			e.exports = {
				builtUrl: i,
				base: n
			}
		}, {
			"env/location": 12,
			"globals/private": 18,
			"util/env": 55,
			"util/util": 69
		}],
		38: [function (t, e) {
			function i(t) {
				return function (e) {
					e.error ? t.error && t.error(e) : e.headers && 200 != e.headers.status ? (t.error && t.error(e), u.warn(e.headers.message)) : t.success && t.success(e), t.complete && t.complete(e), n(t)
				}
			}

			function n(t) {
				var e = t.script;
				e && (e.onload = e.onreadystatechange = null, e.parentNode && e.parentNode.removeChild(e), t.script = void 0, e = void 0), t.callbackName && l.unset(["callbacks", t.callbackName])
			}

			function r(t) {
				var e = {};
				return t.success && c.isType("function", t.success) && (e.success = t.success), t.error && c.isType("function", t.error) && (e.error = t.error), t.complete && c.isType("function", t.complete) && (e.complete = t.complete), e
			}
			var o = t("env/document"),
				s = t("env/location"),
				a = t("assets/refresh"),
				l = t("globals/private"),
				u = t("util/logger"),
				c = t("util/util"),
				d = t("util/querystring"),
				h = "cb",
				f = 0,
				m = !1,
				p = {},
				g = c.aug({
					tweets: "https://syndication.twitter.com/tweets.json",
					timeline: "https://cdn.syndication.twimg.com/widgets/timelines/",
					timelinePoll: "https://syndication.twitter.com/widgets/timelines/paged/",
					timelinePreview: "https://syndication.twitter.com/widgets/timelines/preview/",
					videos: "https://syndication.twitter.com/widgets/video/"
				}, l.get("endpoints") || {});
			p.jsonp = function (t, e, n) {
				var r = n || h + f,
					a = l.fullPath(["callbacks", r]),
					u = o.createElement("script"),
					c = {
						callback: a,
						suppress_response_codes: !0
					};
				l.set(["callbacks", r], i(e)), (m || !/^https?\:$/.test(s.protocol)) && (t = t.replace(/^\/\//, "https://")), u.src = d.url(t, c), u.async = "async", o.body.appendChild(u), e.script = u, e.callbackName = r, n || f++
			}, p.config = function (t) {
				(t.forceSSL === !0 || t.forceSSL === !1) && (m = t.forceSSL)
			}, p.tweets = function (t) {
				var e, i = r(t),
					n = {
						ids: t.ids.join(","),
						lang: t.lang
					};
				a.isEnabled() && (n.new_html = !0), e = d.url(g.tweets, n), this.jsonp(e, i)
			}, p.videos = function (t) {
				var e = r(t),
					i = {
						ids: t.ids.join(","),
						lang: t.lang
					},
					n = d.url(g.videos, i);
				this.jsonp(n, e)
			}, p.timeline = function (t) {
				var e, i = r(t),
					n = 9e5,
					o = Math.floor(+new Date / n),
					a = {
						lang: t.lang,
						t: o,
						domain: s.host,
						dnt: t.dnt,
						override_type: t.overrideType,
						override_id: t.overrideId,
						override_name: t.overrideName,
						override_owner_id: t.overrideOwnerId,
						override_owner_name: t.overrideOwnerName,
						with_replies: t.withReplies
					};
				c.compact(a), e = d.url(g.timeline + t.id, a), this.jsonp(e, i, "tl_" + t.id + "_" + t.instanceId)
			}, p.timelinePoll = function (t) {
				var e, i = r(t),
					n = {
						lang: t.lang,
						since_id: t.sinceId,
						max_id: t.maxId,
						min_position: t.minPosition,
						max_position: t.maxPosition,
						domain: s.host,
						dnt: t.dnt,
						override_type: t.overrideType,
						override_id: t.overrideId,
						override_name: t.overrideName,
						override_owner_id: t.overrideOwnerId,
						override_owner_name: t.overrideOwnerName,
						with_replies: t.withReplies
					};
				c.compact(n), e = d.url(g.timelinePoll + t.id, n), this.jsonp(e, i, "tlPoll_" + t.id + "_" + t.instanceId + "_" + (t.sinceId || t.maxId || t.maxPosition || t.minPosition))
			}, p.timelinePreview = function (t) {
				var e = r(t),
					i = t.params,
					n = d.url(g.timelinePreview, i);
				this.jsonp(n, e)
			}, e.exports = p
		}, {
			"assets/refresh": 4,
			"env/document": 11,
			"env/location": 12,
			"globals/private": 18,
			"util/logger": 59,
			"util/querystring": 63,
			"util/util": 69
		}],
		39: [function (t, e) {
			function i() {
				var t = 36e5,
					e = o.combined(r)._;
				return void 0 !== n ? n : (n = !1, e && /^\d+$/.test(e) && (n = +new Date - parseInt(e) < t), n)
			}
			var n, r = t("env/location"),
				o = t("util/params");
			e.exports = {
				isDynamicWidget: i
			}
		}, {
			"env/location": 12,
			"util/params": 61
		}],
		40: [function (t, e) {
			function i(t, e) {
				return 2 == t || 3 == t && 0 === +e
			}

			function n(t) {
				var e = t.split(" ");
				this.url = decodeURIComponent(e[0].trim()), this.width = +e[1].replace(/w$/, "").trim()
			}

			function r(t, e, i) {
				var r, o, s, a;
				if (t = c.devicePixelRatio ? t * c.devicePixelRatio : t, o = e.split(",").map(function (t) {
						return new n(t.trim())
					}), i)
					for (a = 0; a < o.length; a++) o[a].url === i && (r = o[a]);
				return s = o.reduce(function (e, i) {
					return i.width < e.width && i.width >= t ? i : e
				}, o[0]), r && r.width > s.width ? r : s
			}

			function o(t, e) {
				var i, n = t.getAttribute("data-srcset"),
					o = t.src;
				n && (i = r(e, n, o), t.src = i.url)
			}

			function s(t, e) {
				e = void 0 !== e ? !!e : h.retina(), d.toRealArray(t.getElementsByTagName("IMG")).forEach(function (t) {
					var i = t.getAttribute("data-src-1x") || t.getAttribute("src"),
						n = t.getAttribute("data-src-2x");
					e && n ? t.src = n : i && (t.src = i)
				})
			}

			function a(t, e, n, r) {
				var s = 0,
					a = t.querySelector(".multi-photo"),
					c = a && +a.getAttribute("data-photo-count");
				if (t) return d.toRealArray(t.querySelectorAll(".NaturalImage-image")).forEach(function (t) {
					r(function () {
						o(t, e)
					})
				}), d.toRealArray(t.querySelectorAll(".CroppedImage-image")).forEach(function (t) {
					r(function () {
						o(t, e / 2)
					})
				}), (h.ios() || h.android()) && d.toRealArray(t.querySelectorAll(".FilledIframe")).forEach(function (t) {
					r(function () {
						u(t, {
							width: t.offsetWidth,
							height: t.offsetHeight
						})
					})
				}), d.toRealArray(t.querySelectorAll(".autosized-media")).forEach(function (t) {
					var i = l(t.getAttribute("data-width"), t.getAttribute("data-height"), e, n);
					r(function () {
						o(t, e), t.width = i.width, t.height = i.height, u(t, i)
					}), s = i.height > s ? i.height : s
				}), d.toRealArray(t.querySelectorAll("img.cropped-media")).forEach(function (t) {
					var a, u, d, h = e - 12,
						f = t.parentNode,
						w = t.getAttribute("data-crop-x") || 0,
						v = t.getAttribute("data-crop-y") || 0,
						b = i(c, t.getAttribute("data-image-index")),
						y = Math.floor(h / 2 - m),
						_ = Math.floor(y / (b ? p : g));
					b || (_ -= m / 2), d = l(t.getAttribute("data-width"), t.getAttribute("data-height"), y, n, y, _), a = d.width - y - w, u = d.height - _ - v, 0 > a && Math.max(0, w += a), 0 > u && Math.max(0, v += u), r(function () {
						o(t, y), t.width = d.width, t.height = d.height, f.style.width = y - 1 + "px", f.style.height = _ + "px", w && (t.style.marginLeft = "-" + Math.floor(d.width * w / 100) + "px"), v && (t.style.marginTop = "-" + Math.floor(d.height * v / 100) + "px")
					}), s = d.height * (b ? 2 : 1) > s ? d.height : s
				}), s
			}

			function l(t, e, i, n, r, o) {
				return i = i || t, n = n || e, r = r || 0, o = o || 0, t > i && (e *= i / t, t = i), e > n && (t *= n / e, e = n), r > t && (e *= r / t, t = r), o > e && (t *= o / e, e = o), {
					width: Math.floor(t),
					height: Math.floor(e)
				}
			}

			function u(t, e) {
				function i() {
					var t = {
						name: "tfw:resize",
						dimensions: e
					};
					r.postMessage(t, "*")
				}
				var n, r, o, s, a;
				t && (r = t.contentWindow, n = t.ownerDocument && t.ownerDocument.defaultView, o = h.ios() || h.android(), s = f.isTwitterURL(t.src), a = r && h.canPostMessage(r), o && s && a && (i(), n && n.addEventListener("message", function (t) {
					"tfw:requestsize" === t.data && i()
				}, !1)))
			}
			var c = t("env/window"),
				d = t("util/util"),
				h = t("util/env"),
				f = t("util/twitter"),
				m = 6,
				p = 8 / 9,
				g = 16 / 9;
			e.exports = {
				scaleDimensions: l,
				retinize: s,
				constrainMedia: a,
				__setSrcFromSet: o
			}
		}, {
			"env/window": 14,
			"util/env": 55,
			"util/twitter": 65,
			"util/util": 69
		}],
		41: [function (t, e) {
			var i = t("util/querystring"),
				n = t("util/twitter");
			e.exports = function (t, e) {
				return function (r) {
					var o, s, a = "data-tw-params";
					if (r && n.isTwitterURL(r.href) && !r.getAttribute(a)) {
						if (r.setAttribute(a, !0), "function" == typeof e) {
							o = e.call(this, r);
							for (s in o) o.hasOwnProperty(s) && (t[s] = o[s])
						}
						r.href = i.url(r.href, t)
					}
				}
			}
		}, {
			"util/querystring": 63,
			"util/twitter": 65
		}],
		42: [function (t, e) {
			function i(t) {
				var e, i = this;
				t && (t.ownerDocument ? (this.srcEl = t, this.classAttr = t.className.split(" ")) : (this.srcOb = t, this.classAttr = []), e = this.params(), this.id = this.generateId(), this.setLanguage(), this.related = e.related || this.dataAttr("related"), this.partner = e.partner || this.dataAttr("partner") || g.val("partner"), this.styleAttr = [], this.targetEl = t.targetEl, m.asBoolean(e.dnt || this.dataAttr("dnt")) && w.setOn(), T[this.id] = this, this.completePromise = new h(function (t) {
					i.completeResolver = t
				}), this.completed().then(function (t) {
					t && t != s.body && y.get("events").trigger("rendered", {
						target: t
					})
				}))
			}

			function n() {
				x.forEach(function (t) {
					t()
				}), i.doLayout()
			}

			function r(t) {
				return t ? t.lang ? t.lang : r(t.parentNode) : void 0
			}
			var o, s = t("env/document"),
				a = t("env/window"),
				l = t("tfw/util/assets"),
				u = t("performance/perf-timers"),
				c = t("util/iframe"),
				d = t("util/layout"),
				h = t("util/promise"),
				f = t("util/querystring"),
				m = t("util/typevalidator"),
				p = t("util/util"),
				g = t("globals/pagemetadata"),
				w = t("util/donottrack"),
				v = t("util/logger"),
				b = t("util/document"),
				y = t("globals/twttr"),
				_ = 0,
				T = {},
				x = [],
				A = new d,
				E = "data-twttr-rendered",
				I = {
					ar: {
						"%{followers_count} followers": "عدد المتابعين %{followers_count}",
						"100K+": "+100 ألف",
						"10k unit": "10 آلاف وحدة",
						Follow: "تابِع",
						"Follow %{screen_name}": "تابِع %{screen_name}",
						K: "ألف",
						M: "م",
						Tweet: "غرِّد",
						"Tweet %{hashtag}": "غرِّد %{hashtag}",
						"Tweet to %{name}": "غرِّد لـ %{name}"
					},
					bn: {
						"Follow %{screen_name}": "%{screen_name}-কে অনুসরণ করুন"
					},
					cs: {
						"Follow %{screen_name}": "Sledovat uživatele %{screen_name}"
					},
					da: {
						"%{followers_count} followers": "%{followers_count} følgere",
						"10k unit": "10k enhed",
						Follow: "Følg",
						"Follow %{screen_name}": "Følg %{screen_name}",
						"Tweet to %{name}": "Tweet til %{name}"
					},
					de: {
						"%{followers_count} followers": "%{followers_count} Follower",
						"100K+": "100Tsd+",
						"10k unit": "10tsd-Einheit",
						Follow: "Folgen",
						"Follow %{screen_name}": "%{screen_name} folgen",
						K: "Tsd",
						Tweet: "Twittern",
						"Tweet to %{name}": "Tweet an %{name}"
					},
					es: {
						"%{followers_count} followers": "%{followers_count} seguidores",
						"10k unit": "unidad de 10 mil",
						Follow: "Seguir",
						"Follow %{screen_name}": "Seguir a %{screen_name}",
						Tweet: "Twittear",
						"Tweet %{hashtag}": "Twittear %{hashtag}",
						"Tweet to %{name}": "Twittear a %{name}"
					},
					fa: {
						"%{followers_count} followers": "%{followers_count} دنبال‌کننده",
						"100K+": ">۱۰۰هزار",
						"10k unit": "۱۰هزار واحد",
						Follow: "دنبال کردن",
						"Follow %{screen_name}": "دنبال کردن %{screen_name}",
						K: "هزار",
						M: "میلیون",
						Tweet: "توییت",
						"Tweet %{hashtag}": "توییت کردن %{hashtag}",
						"Tweet to %{name}": "به %{name} توییت کنید"
					},
					fi: {
						"%{followers_count} followers": "%{followers_count} seuraajaa",
						"100K+": "100 000+",
						"10k unit": "10 000 yksikköä",
						Follow: "Seuraa",
						"Follow %{screen_name}": "Seuraa käyttäjää %{screen_name}",
						K: "tuhatta",
						M: "milj.",
						Tweet: "Twiittaa",
						"Tweet %{hashtag}": "Twiittaa %{hashtag}",
						"Tweet to %{name}": "Twiittaa käyttäjälle %{name}"
					},
					fil: {
						"%{followers_count} followers": "%{followers_count} mga tagasunod",
						"10k unit": "10k yunit",
						Follow: "Sundan",
						"Follow %{screen_name}": "Sundan si %{screen_name}",
						Tweet: "I-tweet",
						"Tweet %{hashtag}": "I-tweet ang %{hashtag}",
						"Tweet to %{name}": "Mag-Tweet kay %{name}"
					},
					fr: {
						"%{followers_count} followers": "%{followers_count} abonnés",
						"10k unit": "unité de 10k",
						Follow: "Suivre",
						"Follow %{screen_name}": "Suivre %{screen_name}",
						Tweet: "Tweeter",
						"Tweet %{hashtag}": "Tweeter %{hashtag}",
						"Tweet to %{name}": "Tweeter à %{name}"
					},
					he: {
						"%{followers_count} followers": "%{followers_count} עוקבים",
						"100K+": "מאות אלפים",
						"10k unit": "עשרות אלפים",
						Follow: "מעקב",
						"Follow %{screen_name}": "לעקוב אחר %{screen_name}",
						K: "אלף",
						M: "מיליון",
						Tweet: "ציוץ",
						"Tweet %{hashtag}": "צייצו %{hashtag}",
						"Tweet to %{name}": "ציוץ אל %{name}"
					},
					hi: {
						"%{followers_count} followers": "%{followers_count} फ़ॉलोअर्स",
						"100K+": "1 लाख से अधिक",
						"10k unit": "10 हजार इकाईयां",
						Follow: "फ़ॉलो",
						"Follow %{screen_name}": "%{screen_name} को फ़ॉलो करें",
						K: "हजार",
						M: "मिलियन",
						Tweet: "ट्वीट",
						"Tweet %{hashtag}": "ट्वीट %{hashtag}",
						"Tweet to %{name}": "%{name} के प्रति ट्वीट करें"
					},
					hu: {
						"%{followers_count} followers": "%{followers_count} követő",
						"100K+": "100E+",
						"10k unit": "10E+",
						Follow: "Követés",
						"Follow %{screen_name}": "%{screen_name} követése",
						K: "E",
						"Tweet %{hashtag}": "%{hashtag} tweetelése",
						"Tweet to %{name}": "Tweet küldése neki: %{name}"
					},
					id: {
						"%{followers_count} followers": "%{followers_count} pengikut",
						"100K+": "100 ribu+",
						"10k unit": "10 ribu unit",
						Follow: "Ikuti",
						"Follow %{screen_name}": "Ikuti %{screen_name}",
						K: "&nbsp;ribu",
						M: "&nbsp;juta",
						"Tweet to %{name}": "Tweet ke %{name}"
					},
					it: {
						"%{followers_count} followers": "%{followers_count} follower",
						"10k unit": "10k unità",
						Follow: "Segui",
						"Follow %{screen_name}": "Segui %{screen_name}",
						"Tweet %{hashtag}": "Twitta %{hashtag}",
						"Tweet to %{name}": "Twitta a %{name}"
					},
					ja: {
						"%{followers_count} followers": "%{followers_count}人のフォロワー",
						"100K+": "100K以上",
						"10k unit": "万",
						Follow: "フォローする",
						"Follow %{screen_name}": "%{screen_name}さんをフォロー",
						Tweet: "ツイート",
						"Tweet %{hashtag}": "%{hashtag} をツイートする",
						"Tweet to %{name}": "%{name}さんへツイートする"
					},
					ko: {
						"%{followers_count} followers": "%{followers_count}명의 팔로워",
						"100K+": "100만 이상",
						"10k unit": "만 단위",
						Follow: "팔로우",
						"Follow %{screen_name}": "%{screen_name} 님 팔로우하기",
						K: "천",
						M: "백만",
						Tweet: "트윗",
						"Tweet %{hashtag}": "%{hashtag} 관련 트윗하기",
						"Tweet to %{name}": "%{name} 님에게 트윗하기"
					},
					msa: {
						"%{followers_count} followers": "%{followers_count} pengikut",
						"100K+": "100 ribu+",
						"10k unit": "10 ribu unit",
						Follow: "Ikut",
						"Follow %{screen_name}": "Ikut %{screen_name}",
						K: "ribu",
						M: "juta",
						"Tweet to %{name}": "Tweet kepada %{name}"
					},
					nl: {
						"%{followers_count} followers": "%{followers_count} volgers",
						"100K+": "100k+",
						"10k unit": "10k-eenheid",
						Follow: "Volgen",
						"Follow %{screen_name}": "%{screen_name} volgen",
						K: "k",
						M: " mln.",
						Tweet: "Tweeten",
						"Tweet %{hashtag}": "%{hashtag} tweeten",
						"Tweet to %{name}": "Tweeten naar %{name}"
					},
					no: {
						"%{followers_count} followers": "%{followers_count} følgere",
						"100K+": "100 K+",
						"10k unit": "10-K-enhet",
						Follow: "Følg",
						"Follow %{screen_name}": "Følg %{screen_name}",
						"Tweet to %{name}": "Send en tweet til %{name}"
					},
					pl: {
						"%{followers_count} followers": "%{followers_count} obserwujących",
						"100K+": "100 tys.+",
						"10k unit": "10 tys.",
						Follow: "Obserwuj",
						"Follow %{screen_name}": "Obserwuj %{screen_name}",
						K: "tys.",
						M: "mln",
						Tweet: "Tweetnij",
						"Tweet %{hashtag}": "Tweetnij %{hashtag}",
						"Tweet to %{name}": "Tweetnij do %{name}"
					},
					pt: {
						"%{followers_count} followers": "%{followers_count} seguidores",
						"100K+": "+100 mil",
						"10k unit": "10 mil unidades",
						Follow: "Seguir",
						"Follow %{screen_name}": "Seguir %{screen_name}",
						K: "Mil",
						Tweet: "Tweetar",
						"Tweet %{hashtag}": "Tweetar %{hashtag}",
						"Tweet to %{name}": "Tweetar para %{name}"
					},
					ro: {
						"Follow %{screen_name}": "Urmăreşte pe %{screen_name}"
					},
					ru: {
						"%{followers_count} followers": "Читатели: %{followers_count} ",
						"100K+": "100 тыс.+",
						"10k unit": "блок 10k",
						Follow: "Читать",
						"Follow %{screen_name}": "Читать %{screen_name}",
						K: "тыс.",
						M: "млн.",
						Tweet: "Твитнуть",
						"Tweet %{hashtag}": "Твитнуть %{hashtag}",
						"Tweet to %{name}": "Твитнуть %{name}"
					},
					sv: {
						"%{followers_count} followers": "%{followers_count} följare",
						"10k unit": "10k",
						Follow: "Följ",
						"Follow %{screen_name}": "Följ %{screen_name}",
						Tweet: "Tweeta",
						"Tweet %{hashtag}": "Tweeta %{hashtag}",
						"Tweet to %{name}": "Tweeta till %{name}"
					},
					th: {
						"%{followers_count} followers": "%{followers_count} ผู้ติดตาม",
						"100K+": "100พัน+",
						"10k unit": "หน่วย 10พัน",
						Follow: "ติดตาม",
						"Follow %{screen_name}": "ติดตาม %{screen_name}",
						M: "ล้าน",
						Tweet: "ทวีต",
						"Tweet %{hashtag}": "ทวีต %{hashtag}",
						"Tweet to %{name}": "ทวีตถึง %{name}"
					},
					tr: {
						"%{followers_count} followers": "%{followers_count} takipçi",
						"100K+": "+100 bin",
						"10k unit": "10 bin birim",
						Follow: "Takip et",
						"Follow %{screen_name}": "Takip et: %{screen_name}",
						K: "bin",
						M: "milyon",
						Tweet: "Tweetle",
						"Tweet %{hashtag}": "Tweetle: %{hashtag}",
						"Tweet to %{name}": "Tweetle: %{name}"
					},
					uk: {
						"Follow %{screen_name}": "Читати %{screen_name}"
					},
					ur: {
						"%{followers_count} followers": "%{followers_count} فالورز",
						"100K+": "ایک لاکھ سے زیادہ",
						"10k unit": "دس ہزار یونٹ",
						Follow: "فالو کریں",
						"Follow %{screen_name}": "%{screen_name} کو فالو کریں",
						K: "ہزار",
						M: "ملین",
						Tweet: "ٹویٹ کریں",
						"Tweet %{hashtag}": "%{hashtag} ٹویٹ کریں",
						"Tweet to %{name}": "%{name} کو ٹویٹ کریں"
					},
					vi: {
						"Follow %{screen_name}": "Theo dõi %{screen_name}"
					},
					"zh-cn": {
						"%{followers_count} followers": "%{followers_count} 关注者",
						"100K+": "10万+",
						"10k unit": "1万单元",
						Follow: "关注",
						"Follow %{screen_name}": "关注 %{screen_name}",
						K: "千",
						M: "百万",
						Tweet: "发推",
						"Tweet %{hashtag}": "以 %{hashtag} 发推",
						"Tweet to %{name}": "发推给 %{name}"
					},
					"zh-tw": {
						"%{followers_count} followers": "%{followers_count} 位跟隨者",
						"100K+": "超過十萬",
						"10k unit": "1萬 單位",
						Follow: "跟隨",
						"Follow %{screen_name}": "跟隨 %{screen_name}",
						K: "千",
						M: "百萬",
						Tweet: "推文",
						"Tweet %{hashtag}": "推文%{hashtag}",
						"Tweet to %{name}": "推文給%{name}"
					}
				};
			p.aug(i.prototype, {
				setLanguage: function (t) {
					var e;
					return t || (t = this.params().lang || this.dataAttr("lang") || r(this.srcEl)), (t = t && t.toLowerCase()) ? I[t] ? this.lang = t : (e = t.replace(/[\-_].*/, ""), I[e] ? this.lang = e : void(this.lang = "en")) : this.lang = "en"
				},
				_: function (t, e) {
					var i = this.lang;
					return e = e || {}, i && I.hasOwnProperty(i) || (i = this.lang = "en"), t = I[i] && I[i][t] || t, this.ringo(t, e, /%\{([\w_]+)\}/g)
				},
				ringo: function (t, e, i) {
					return i = i || /\{\{([\w_]+)\}\}/g, t.replace(i, function (t, i) {
						return void 0 !== e[i] ? e[i] : t
					})
				},
				makeIframeSource: function () {
					if (this.iframeSource) {
						var t = f.encode(this.widgetUrlParams());
						return [l.base(), "/", this.ringo(this.iframeSource, {
							lang: this.lang
						}), "#", t].join("")
					}
				},
				add: function (t) {
					T[this.id] = t
				},
				create: function (t, e, i) {
					var n, r = this;
					return i[E] = !0, n = c(p.aug({
						id: this.id,
						src: t,
						"class": this.classAttr.join(" ")
					}, i), e, this.targetEl && this.targetEl.ownerDocument), this.srcEl ? this.layout(function () {
						return r.srcEl.parentNode.replaceChild(n, r.srcEl), r.completeResolver.fulfill(n), n
					}) : this.targetEl ? this.layout(function () {
						return r.targetEl.appendChild(n), r.completeResolver.fulfill(n), n
					}) : h.reject("Did not append widget")
				},
				params: function () {
					var t, e;
					return this.srcOb ? e = this.srcOb : (t = this.srcEl && this.srcEl.href && this.srcEl.href.split("?")[1], e = t ? f.decode(t) : {}), this.params = function () {
						return e
					}, e
				},
				widgetUrlParams: function () {
					return {}
				},
				dataAttr: function (t) {
					return this.srcEl && this.srcEl.getAttribute("data-" + t)
				},
				attr: function (t) {
					return this.srcEl && this.srcEl.getAttribute(t)
				},
				layout: function (t) {
					return A.enqueue(t)
				},
				styles: {
					base: [["font", "normal normal normal 11px/18px 'Helvetica Neue', Arial, sans-serif"], ["margin", "0"], ["padding", "0"], ["whiteSpace", "nowrap"]],
					button: [["fontWeight", "bold"], ["textShadow", "0 1px 0 rgba(255,255,255,.5)"]],
					large: [["fontSize", "13px"], ["lineHeight", "26px"]],
					vbubble: [["fontSize", "16px"]]
				},
				width: function () {
					throw new Error("not implemented")
				},
				height: function () {
					return "m" == this.size ? 20 : 28
				},
				minWidth: function () {},
				maxWidth: function () {},
				minHeight: function () {},
				maxHeight: function () {},
				dimensions: function () {
					function t(t) {
						switch (typeof t) {
						case "string":
							return t;
						case "undefined":
							return;
						default:
							return t + "px"
						}
					}
					var e = {
						width: this.width(),
						height: this.height()
					};
					return this.minWidth() && (e["min-width"] = this.minWidth()), this.maxWidth() && (e["max-width"] = this.maxWidth()), this.minHeight() && (e["min-height"] = this.minHeight()), this.maxHeight() && (e["max-height"] = this.maxHeight()), p.forIn(e, function (i, n) {
						e[i] = t(n)
					}), e
				},
				generateId: function () {
					return this.srcEl && this.srcEl.id || "twitter-widget-" + _++
				},
				completed: function () {
					return this.completePromise
				}
			}), i.afterLoad = function (t) {
				x.push(t)
			}, i.doLayout = function () {
				A.exec()
			}, i.doLayoutAsync = function () {
				A.delayedExec()
			}, i.init = function (t) {
				o = t
			}, i.reset = function () {
				T = {}
			}, i.find = function (t) {
				return t && T[t] ? T[t].element : null
			}, i.embed = function (t) {
				var e = [],
					r = [],
					a = [];
				m.isArray(t) || (t = [t || s]), v.time("sandboxes"), t.forEach(function (t) {
					p.forIn(o, function (i, n) {
						var r = t.querySelectorAll(i);
						p.toRealArray(r).forEach(function (t) {
							var i;
							t.getAttribute(E) || (t.setAttribute(E, "true"), i = new n(t), e.push(i), a.push(i.sandboxCreated))
						})
					})
				}), h.every.apply(null, a).then(function () {
					v.timeEnd("sandboxes")
				}), i.doLayout(), e.forEach(function (t) {
					r.push(t.completed()), t.render()
				}), h.every.apply(null, r).then(function (t) {
					t = t.filter(function (t) {
						return t
					}), t.length && (y.get("events").trigger("loaded", {
						widgets: t
					}), v.timeEnd("load"))
				}).then(i.trackRender), i.doLayoutAsync(), n()
			}, i.trackRender = function () {
				u.endAndTrack("render", "widgets-js-load", "page", {
					widget_origin: b.rootDocumentLocation(),
					widget_frame: b.isFramed() && b.currentDocumentLocation()
				})
			}, a.setInterval(function () {
				i.doLayout()
			}, 500), e.exports = i
		}, {
			"env/document": 11,
			"env/window": 14,
			"globals/pagemetadata": 17,
			"globals/twttr": 19,
			"performance/perf-timers": 23,
			"tfw/util/assets": 37,
			"util/document": 52,
			"util/donottrack": 54,
			"util/iframe": 57,
			"util/layout": 58,
			"util/logger": 59,
			"util/promise": 62,
			"util/querystring": 63,
			"util/typevalidator": 66,
			"util/util": 69
		}],
		43: [function (t, e) {
			function i(t, e) {
				var i = t.querySelector("blockquote.subject"),
					n = t.querySelector("blockquote.reply"),
					r = i && i.getAttribute("data-tweet-id"),
					o = n && n.getAttribute("data-tweet-id"),
					s = {},
					a = {};
				r && (s[r] = {
					item_type: 0
				}, T.clientEvent({
					page: "tweet",
					section: "subject",
					component: "tweet",
					action: "results"
				}, v.aug({}, e, {
					item_ids: [r],
					item_details: s
				}), !0), _.scribeTweetAudienceImpression(), o && (a[o] = {
					item_type: 0
				}, T.clientEvent({
					page: "tweet",
					section: "conversation",
					component: "tweet",
					action: "results"
				}, v.aug({}, e, {
					item_ids: [o],
					item_details: a,
					associations: {
						4: {
							association_id: r,
							association_type: 4
						}
					}
				}), !0)))
			}

			function n(t, e) {
				var i = {};
				t && (i[t] = {
					item_type: 0
				}, T.clientEvent({
					page: "tweet",
					section: "subject",
					component: "rawembedcode",
					action: "no_results"
				}, {
					widget_origin: A.rootDocumentLocation(),
					widget_frame: A.isFramed() && A.currentDocumentLocation(),
					message: e,
					item_ids: [t],
					item_details: i
				}, !0), _.scribeTweetAudienceImpression())
			}

			function r(t, e, i, n) {
				D[t] = D[t] || [], D[t].push({
					s: i,
					f: n,
					lang: e
				})
			}

			function o(t) {
				if (t) {
					var e, i, n;
					d.apply(this, [t]), e = this.params(), i = this.srcEl && this.srcEl.getElementsByTagName("A"), n = i && i[i.length - 1], this.hideThread = "none" == (e.conversation || this.dataAttr("conversation")) || v.contains(this.classAttr, "tw-hide-thread"), this.hideCard = "hidden" == (e.cards || this.dataAttr("cards")) || v.contains(this.classAttr, "tw-hide-media"), "left" == (e.align || this.attr("align")) || v.contains(this.classAttr, "tw-align-left") ? this.align = "left" : "right" == (e.align || this.attr("align")) || v.contains(this.classAttr, "tw-align-right") ? this.align = "right" : ("center" == (e.align || this.attr("align")) || v.contains(this.classAttr, "tw-align-center")) && (this.align = "center", this.containerWidth > this.dimensions.MIN_WIDTH * (1 / .7) && this.width > .7 * this.containerWidth && (this.width = .7 * this.containerWidth)), this.narrow = e.narrow || this.width <= this.dimensions.NARROW_WIDTH, this.narrow && this.classAttr.push("var-narrow"), this.tweetId = e.tweetId || n && b.status(n.href)
				}
			}
			var s = t("assets/css"),
				a = t("assets/refresh"),
				l = t("env/window"),
				u = t("dom/selection"),
				c = t("tfw/widget/base"),
				d = t("tfw/widget/syndicatedbase"),
				h = t("util/datetime"),
				f = t("tfw/util/params"),
				m = t("dom/classname"),
				p = t("dom/get"),
				g = t("performance/perf-timers"),
				w = t("util/promise"),
				v = t("util/util"),
				b = t("util/twitter"),
				y = t("tfw/util/data"),
				_ = t("scribe/audience"),
				T = t("scribe/frame"),
				x = t("tfw/util/media"),
				A = t("util/document"),
				E = t("globals/twttr"),
				I = t("dom/delegate"),
				S = t("scribe/pixel"),
				N = "tweetembed",
				D = {},
				R = [];
			o.prototype = new d, v.aug(o.prototype, {
				renderedClassNames: "twitter-tweet twitter-tweet-rendered",
				dimensions: {
					DEFAULT_HEIGHT: "0",
					DEFAULT_WIDTH: "500",
					NARROW_WIDTH: "350",
					maxHeight: "375",
					FULL_BLEED_PHOTO_MAX_HEIGHT: "600",
					MIN_WIDTH: "220",
					MIN_HEIGHT: "0",
					MARGIN: "10px 0",
					WIDE_MEDIA_PADDING: 32,
					NARROW_MEDIA_PADDING: 32,
					BORDERS: 0
				},
				styleSheetUrl: s.tweet,
				ensureStyleSheetConsistency: function (t) {
					var e, i;
					return m.present(t, "EmbeddedTweet") && !a.isEnabled() ? (e = this.styleSheetUrl(), i = s.tweetRefresh(this.lang), w.every(this.sandbox.removeStyleSheet(e), this.sandbox.appendStyleSheet(i))) : w.fulfill()
				},
				create: function (t) {
					var e, n, r, o = this,
						s = this.sandbox.createElement("div");
					return s.innerHTML = t, (e = s.children[0] || !1) ? ("dark" == this.theme && this.classAttr.push("thm-dark"), this.linkColor && this.addSiteStyles(), m.present(e, "media-forward") && (this.fullBleedPhoto = !0, this.dimensions.maxHeight = this.dimensions.FULL_BLEED_PHOTO_MAX_HEIGHT), m.present(e, "with-border") || m.present(e, "EmbeddedTweet") || this.sandbox.style({
						border: "#ddd 1px solid",
						borderTopColor: "#eee",
						borderBottomColor: "#bbb",
						borderRadius: "5px",
						boxShadow: "0 1px 3px rgba(0,0,0,0.15)",
						maxWidth: "99%"
					}), m.present(e, "with-border") ? (s.style.padding = "2px 3px 3px 2px", r = s) : r = e, x.retinize(e), e.id = this.id, e.className += " " + this.classAttr.join(" "), e.lang = this.lang, this.sandbox.setTitle(e.getAttribute("data-iframe-title") || "Tweet"), w.every(this.ensureStyleSheetConsistency(e), this.sandbox.appendChild(r)).then(function () {
						o.renderResolver.fulfill(o.sandbox)
					}), n = this.layout(function () {
						o.predefinedWidth = o.width, o.width = o.sandbox.width(o.width), o.collapseRegions()
					}), n.then(function () {
						o.constrainMedia(e, o.contentWidth(o.width)), o.setNarrow().then(function () {
							o.layout(function () {
								o.completeResolver.fulfill(o.sandbox.element())
							})
						})
					}), i(e, this.baseScribeData(), this.partner), e) : void 0
				},
				render: function () {
					var t = this,
						e = "",
						i = this.tweetId;
					return i ? (this.hideCard && (e += "c"), this.hideThread && (e += "t"), e && (i += "-" + e), this.rendered().then(function (e) {
						var i = t.srcEl;
						i && i.parentNode && t.layout(function () {
							i && i.parentNode && i.parentNode.removeChild(i)
						}), "center" == t.align ? e.style({
							margin: "7px auto",
							cssFloat: "none"
						}) : t.align && (t.width == t.dimensions.DEFAULT_WIDTH && (t.predefinedWidth = t.width = t.dimensions.NARROW_WIDTH), e.style({
							cssFloat: t.align
						})), t.sandbox.resizeToContent().then(function (e) {
							return t.height = e, c.doLayoutAsync(), t.sandbox.resizeToContent().then(function (e) {
								t.height = e
							})
						}).then(function () {
							e.onresize(t.handleResize.bind(t))
						}), e.style({
							position: "static",
							visibility: "visible"
						}), c.doLayoutAsync()
					}), r(i, this.lang, function (e) {
						t.ready().then(function () {
							t.element = t.create(e), t.readTimestampTranslations(), t.updateTimeStamps(), t.bindIntentHandlers(), t.bindUIHandlers(), t.bindPermalinkHandler(), c.doLayoutAsync()
						})
					}, function () {
						n(t.tweetId, t.partner), t.completeResolver.fulfill(t.srcEl)
					}), R.push(this.completed()), this.completed().then(this.scribePerformance.bind(this)), this.completed()) : (this.completeResolver.fulfill(this.srcEl), this.completed())
				},
				bindPermalinkHandler: function () {
					var t = this;
					m.present(this.element, "decider-tapOpensPermalink") && (I.delegate(this.element, "click", "A", function (t) {
						I.stopPropagation(t)
					}), I.delegate(this.element, "click", ".twitter-tweet", function (e) {
						var i, n;
						u.getSelection(t.sandbox._win) || (i = t.element.querySelectorAll("blockquote.tweet"), n = i[i.length - 1], t.openPermalink(n), t.scribePermalinkClick(n, e), I.stopPropagation(e))
					}))
				},
				scribePermalinkClick: function (t, e) {
					var i = this.createScribeData(t);
					S.interaction(e, i, !1)
				},
				openPermalink: function (t) {
					var e = t.cite;
					b.isStatus(e) && l.open(e)
				},
				scribePerformance: function () {
					g.endAndTrack("render", "widgets-js-load", "tweet", this.baseScribeData())
				},
				addUrlParams: function (t) {
					var e = this,
						i = {
							related: this.related,
							partner: this.partner,
							original_referer: A.rootDocumentLocation(),
							tw_p: N
						};
					return this.addUrlParams = f(i, function (t) {
						var i = p.closest(".tweet", t, e.element);
						return {
							tw_i: i.getAttribute("data-tweet-id")
						}
					}), this.addUrlParams(t)
				},
				baseScribeData: function () {
					return {
						widget_origin: A.rootDocumentLocation(),
						widget_frame: A.isFramed() && A.currentDocumentLocation(),
						message: this.partner
					}
				},
				handleResize: function (t) {
					var e = this;
					t != this.width && (this.width = t, this.setNarrow(), this.constrainMedia(this.element, this.contentWidth(t)), this.collapseRegions(), this.sandbox.resizeToContent().then(function (t) {
						e.height = t, E.get("events").trigger("resize", {
							target: e.sandbox.element()
						})
					}), c.doLayoutAsync())
				},
				readTimestampTranslations: function () {
					var t = this.element,
						e = "data-dt-",
						i = t.getAttribute(e + "months") || "";
					this.datetime = new h(v.compact({
						phrases: {
							AM: t.getAttribute(e + "am"),
							PM: t.getAttribute(e + "pm")
						},
						months: i.split("|"),
						formats: {
							full: t.getAttribute(e + "full")
						}
					}))
				},
				updateTimeStamps: function () {
					var t = this.element.querySelector(".long-permalink"),
						e = t.getAttribute("data-datetime"),
						i = e && this.datetime.localTimeStamp(e),
						n = t.getElementsByTagName("TIME")[0];
					i && (this.layout(function () {
						return n && n.innerHTML ? void(n.innerHTML = i) : void(t.innerHTML = i)
					}, "Update Timestamp"), c.doLayoutAsync())
				}
			}), o.fetchAndRender = function () {
				var t, e, i = D,
					n = [];
				if (D = {}, i.keys) n = i.keys();
				else
					for (t in i) i.hasOwnProperty(t) && n.push(t);
				n.length && (T.init(), e = i[n[0]][0].lang, y.tweets({
					ids: n.sort(),
					lang: e,
					complete: function (t) {
						v.forIn(t, function (t, e) {
							var n = i[t];
							n.forEach(function (t) {
								t.s && t.s.call(this, e)
							}), delete i[t]
						}), c.doLayout(), v.forIn(i, function (t, e) {
							e.forEach(function (e) {
								e.f && e.f.call(this, t)
							})
						}), c.doLayout()
					}
				}), w.every.apply(null, R).then(function () {
					T.flush()
				}), R = [])
			}, c.afterLoad(o.fetchAndRender), e.exports = o
		}, {
			"assets/css": 3,
			"assets/refresh": 4,
			"dom/classname": 5,
			"dom/delegate": 6,
			"dom/get": 7,
			"dom/selection": 8,
			"env/window": 14,
			"globals/twttr": 19,
			"performance/perf-timers": 23,
			"scribe/audience": 30,
			"scribe/frame": 31,
			"scribe/pixel": 32,
			"tfw/util/data": 38,
			"tfw/util/media": 40,
			"tfw/util/params": 41,
			"tfw/widget/base": 42,
			"tfw/widget/syndicatedbase": 46,
			"util/datetime": 51,
			"util/document": 52,
			"util/promise": 62,
			"util/twitter": 65,
			"util/util": 69
		}],
		44: [function (t, e) {
			function i(t) {
				if (t) {
					var e, i, n, r;
					o.apply(this, [t]), e = this.params(), i = e.size || this.dataAttr("size"), n = e.showScreenName || this.dataAttr("show-screen-name"), r = e.count || this.dataAttr("count"), this.classAttr.push("twitter-follow-button"), this.showScreenName = "false" != n, this.showCount = !(e.showCount === !1 || "false" == this.dataAttr("show-count")), "none" == r && (this.showCount = !1), this.explicitWidth = e.width || this.dataAttr("width") || "", this.screenName = e.screen_name || e.screenName || s.screenName(this.attr("href")), this.preview = e.preview || this.dataAttr("preview") || "", this.align = e.align || this.dataAttr("align") || "", this.size = "large" == i ? "l" : "m"
				}
			}
			var n = t("util/donottrack"),
				r = t("util/util"),
				o = t("tfw/widget/base"),
				s = t("util/twitter"),
				a = t("util/promise"),
				l = t("dom/textsize");
			i.prototype = new o, r.aug(i.prototype, {
				iframeSource: "widgets/follow_button.3afdf1fe9dd484034da3e37c7d9e99ed.{{lang}}.html",
				widgetUrlParams: function () {
					return r.compact({
						screen_name: this.screenName,
						lang: this.lang,
						show_count: this.showCount,
						show_screen_name: this.showScreenName,
						align: this.align,
						id: this.id,
						preview: this.preview,
						size: this.size,
						partner: this.partner,
						dnt: n.enabled(),
						_: +new Date
					})
				},
				width: function () {
					if (this.calculatedWidth) return this.calculatedWidth;
					if (this.explicitWidth) return this.explicitWidth;
					var t, e, i = {
							cnt: 13,
							btn: 24,
							xlcnt: 22,
							xlbtn: 38
						},
						n = this.showScreenName ? "Follow %{screen_name}" : "Follow",
						o = this._(n, {
							screen_name: "@" + this.screenName
						}),
						s = this._(r.contains(["ja", "ko"], this.lang) ? "10k unit" : "M"),
						a = this._("%{followers_count} followers", {
							followers_count: "88888" + s
						}),
						u = 0,
						c = 0,
						d = this.styles.base;
					return "l" == this.size ? (d = d.concat(this.styles.large), t = i.xlbtn, e = i.xlcnt) : (t = i.btn, e = i.cnt), this.showCount && (c = l(a, "", d).width + e), u = l(o, "", d.concat(this.styles.button)).width + t,
						this.calculatedWidth = u + c
				},
				render: function () {
					if (!this.screenName) return a.reject("Missing Screen Name");
					var t = this,
						e = this.makeIframeSource(),
						i = this.create(e, this.dimensions(), {
							title: this._("Twitter Follow Button")
						}).then(function (e) {
							return t.element = e
						});
					return i
				}
			}), e.exports = i
		}, {
			"dom/textsize": 10,
			"tfw/widget/base": 42,
			"util/donottrack": 54,
			"util/promise": 62,
			"util/twitter": 65,
			"util/util": 69
		}],
		45: [function (t, e) {
			function i(t) {
				f.open(t)
			}

			function n(e, i) {
				var n = t("tfw/hub/client");
				n.openIntent(e, i)
			}

			function r(t, e) {
				if (h.isTwitterURL(t))
					if (p.get("eventsHub") && e) {
						var r = new o(a.generateId(), e);
						a.add(r), n(t, e), m.get("events").trigger("click", {
							target: e,
							region: "intent",
							type: "click",
							data: {}
						})
					} else i(t)
			}

			function o(t, e) {
				this.id = t, this.element = this.srcEl = e
			}

			function s(t) {
				this.srcEl = [], this.element = t
			}
			var a, l = t("env/document"),
				u = t("tfw/widget/base"),
				c = t("util/util"),
				d = t("util/promise"),
				h = t("util/twitter"),
				f = t("intents/intent"),
				m = t("globals/twttr"),
				p = t("globals/private");
			s.prototype = new u, c.aug(s.prototype, {
				render: function () {
					return a = this, d.fulfill(l.body)
				}
			}), s.open = r, e.exports = s
		}, {
			"env/document": 11,
			"globals/private": 18,
			"globals/twttr": 19,
			"intents/intent": 22,
			"tfw/hub/client": 35,
			"tfw/widget/base": 42,
			"util/promise": 62,
			"util/twitter": 65,
			"util/util": 69
		}],
		46: [function (t, e) {
			function i() {
				o = n.VALID_COLOR.test(d.val("widgets:link-color")) && RegExp.$1, a = n.VALID_COLOR.test(d.val("widgets:border-color")) && RegExp.$1, s = d.val("widgets:theme")
			}

			function n(t) {
				if (t) {
					var e, i = this;
					this.readyPromise = new _(function (t) {
						i.readyResolver = t
					}), this.renderedPromise = new _(function (t) {
						i.renderResolver = t
					}), u.apply(this, [t]), e = this.params(), this.targetEl = this.srcEl && this.srcEl.parentNode || e.targetEl || l.body, this.predefinedWidth = n.VALID_UNIT.test(e.width || this.attr("width")) && RegExp.$1, this.layout(function () {
						return i.containerWidth = v.effectiveWidth(i.targetEl)
					}).then(function (t) {
						var r = i.predefinedWidth || t || i.dimensions.DEFAULT_WIDTH;
						i.height = n.VALID_UNIT.test(e.height || i.attr("height")) && RegExp.$1, i.width = Math.max(i.dimensions.MIN_WIDTH, Math.min(r, i.dimensions.DEFAULT_WIDTH))
					}), this.linkColor = n.VALID_COLOR.test(e.linkColor || this.dataAttr("link-color")) ? RegExp.$1 : o, this.borderColor = n.VALID_COLOR.test(e.borderColor || this.dataAttr("border-color")) ? RegExp.$1 : a, this.theme = e.theme || this.attr("data-theme") || s, this.theme = /(dark|light)/.test(this.theme) ? this.theme : "", this.classAttr.push(y.touch() ? "is-touch" : "not-touch"), y.ie9() && this.classAttr.push("ie9"), this.sandboxCreated = b.createSandbox({
						"class": this.renderedClassNames,
						id: this.id,
						allowfullscreen: ""
					}, {
						position: "absolute",
						visibility: "hidden"
					}, function (t) {
						i.srcEl ? i.targetEl.insertBefore(t, i.srcEl) : i.targetEl.appendChild(t)
					}, this.layout).then(function (t) {
						i.setupSandbox(t), new m(t.element().contentWindow)
					}), this.rendered().then(function (t) {
						i.applyVisibleSandboxStyles(t)
					})
				}
			}

			function r(t, e) {
				return t + e
			}
			var o, s, a, l = t("env/document"),
				u = t("tfw/widget/base"),
				c = t("tfw/widget/intent"),
				d = t("globals/pagemetadata"),
				h = t("tfw/util/media"),
				f = t("scribe/pixel"),
				m = t("video/video_post_message_interface"),
				p = t("dom/classname"),
				g = t("dom/get"),
				w = t("dom/delegate"),
				v = t("dom/size"),
				b = t("sandbox/frame"),
				y = t("util/env"),
				_ = t("util/promise"),
				T = t("util/twitter"),
				x = t("util/typevalidator"),
				A = t("util/util"),
				E = [".customisable", ".customisable:link", ".customisable:visited", ".customisable:hover", ".customisable:focus", ".customisable:active", ".customisable-highlight:hover", ".customisable-highlight:focus", "a:hover .customisable-highlight", "a:focus .customisable-highlight"],
				I = ["a:hover .ic-mask", "a:focus .ic-mask"],
				S = [".customisable-border"],
				N = [".timeline-header h1.summary", ".timeline-header h1.summary a:link", ".timeline-header h1.summary a:visited"],
				D = {
					TWEET: 0,
					RETWEET: 10
				};
			n.prototype = new u, A.aug(n.prototype, {
				styleSheetUrl: function () {
					throw new Error("must set styleSheetUrl")
				},
				setupSandbox: function (t) {
					var e = this;
					this.sandbox = t, _.some(e.applyInitialSandboxStyles(t), t.appendCss(".SandboxRoot { display:none }"), t.setBaseTarget("_blank"), t.appendStyleSheet(this.styleSheetUrl(this.lang, this.theme))).then(function () {
						e.readyResolver.fulfill(t)
					})
				},
				ready: function () {
					return this.readyPromise
				},
				rendered: function () {
					return this.renderedPromise
				},
				contentWidth: function (t) {
					var e = this.dimensions,
						i = this.borderless ? 0 : e.BORDERS,
						n = this.fullBleedPhoto ? 0 : this.chromeless && this.narrow ? e.NARROW_MEDIA_PADDING_CL : this.chromeless ? e.WIDE_MEDIA_PADDING_CL : this.narrow ? e.NARROW_MEDIA_PADDING : e.WIDE_MEDIA_PADDING;
					return (t || this.width) - (n + i)
				},
				applyInitialSandboxStyles: function (t) {
					var e = this;
					return t.style({
						border: "none",
						maxWidth: "100%",
						minWidth: e.dimensions.MIN_WIDTH + "px",
						margin: e.dimensions.MARGIN,
						padding: "0",
						display: "block",
						position: "absolute",
						visibility: "hidden"
					}, !0)
				},
				applyVisibleSandboxStyles: function (t) {
					return t.style({
						position: "static",
						visibility: "visible"
					})
				},
				addSiteStyles: function () {
					function t(t) {
						return ("dark" == e.theme ? ".thm-dark " : "") + t
					}
					var e = this,
						i = [];
					return this.headingStyle && i.push(N.map(t).join(",") + "{" + this.headingStyle + "}"), this.linkColor && (i.push(E.map(t).join(",") + "{color:" + this.linkColor + "}"), i.push(I.map(t).join(",") + "{background-color:" + this.linkColor + "}")), this.borderColor && i.push(S.map(t).concat("dark" == this.theme ? [".thm-dark.customisable-border"] : []).join(",") + "{border-color:" + this.borderColor + "}"), i.length ? this.sandbox.appendCss(i.join("")) : void 0
				},
				setNarrow: function () {
					var t = this,
						e = this.narrow;
					return this.narrow = this.width < this.dimensions.NARROW_WIDTH, e != this.narrow ? this.layout(function () {
						return p.toggle(t.element, "var-narrow", t.narrow)
					}) : _.fulfill(this.narrow)
				},
				createScribeData: function (t) {
					var e = A.aug({}, this.baseScribeData(), {
						item_ids: [],
						item_details: this.extractTweetScribeDetails(t)
					});
					return A.forIn(e.item_details, function (t) {
						e.item_ids.push(t)
					}), e
				},
				bindUIHandlers: function () {
					var t = this.element;
					w.delegate(t, "click", ".MediaCard-dismissNsfw", function () {
						var e = g.closest(".MediaCard", this, t);
						p.remove(e, "MediaCard--nsfw")
					})
				},
				bindIntentHandlers: function () {
					function t(t) {
						var n = g.closest(".tweet", this, i),
							r = e.createScribeData(n);
						f.interaction(t, r, !0)
					}
					var e = this,
						i = this.element;
					w.delegate(i, "click", "A", t), w.delegate(i, "click", "BUTTON", t), w.delegate(i, "click", ".profile", function () {
						e.addUrlParams(this)
					}), w.delegate(i, "click", ".follow-button", function (t) {
						var i;
						t.altKey || t.metaKey || t.shiftKey || y.ios() || y.android() || x.asBoolean(this.getAttribute("data-age-gate")) || (i = T.intentForFollowURL(this.href, !0), i && (c.open(i, e.sandbox.element()), w.preventDefault(t)))
					}), w.delegate(i, "click", ".web-intent", function (t) {
						e.addUrlParams(this), t.altKey || t.metaKey || t.shiftKey || (c.open(this.href, e.sandbox.element()), w.preventDefault(t))
					})
				},
				baseScribeData: function () {
					return {}
				},
				extractTweetScribeDetails: function (t) {
					var e, i, n = {};
					return t ? (e = t.getAttribute("data-tweet-id"), i = t.getAttribute("data-rendered-tweet-id") || e, i == e ? n[i] = {
						item_type: D.TWEET
					} : e && (n[i] = {
						item_type: D.RETWEET,
						target_type: D.TWEET,
						target_id: e
					}), n) : n
				},
				constrainMedia: function (t, e) {
					return h.constrainMedia(t || this.element, e || this.contentWidth(), this.dimensions.maxHeight, this.layout)
				},
				collapseRegions: function () {
					var t = this;
					A.toRealArray(this.element.querySelectorAll(".collapsible-container")).forEach(function (e) {
						var i, n, o = A.toRealArray(e.children),
							s = o.length && e.offsetWidth,
							a = o.length && o.map(function (t) {
								return t.offsetWidth
							}),
							l = o.length;
						if (o.length)
							for (; l > 0;) {
								if (l--, i = a.reduce(r, 0), !s || !i) return;
								if (s > i) return;
								n = o[l].getAttribute("data-collapsed-class"), n && (p.add(t.element, n), a[l] = o[l].offsetWidth)
							}
					})
				}
			}), n.VALID_UNIT = /^([0-9]+)( ?px)?$/, n.VALID_COLOR = /^(#(?:[0-9a-f]{3}|[0-9a-f]{6}))$/i, i(), e.exports = n
		}, {
			"dom/classname": 5,
			"dom/delegate": 6,
			"dom/get": 7,
			"dom/size": 9,
			"env/document": 11,
			"globals/pagemetadata": 17,
			"sandbox/frame": 28,
			"scribe/pixel": 32,
			"tfw/util/media": 40,
			"tfw/widget/base": 42,
			"tfw/widget/intent": 45,
			"util/env": 55,
			"util/promise": 62,
			"util/twitter": 65,
			"util/typevalidator": 66,
			"util/util": 69,
			"video/video_post_message_interface": 73
		}],
		47: [function (t, e) {
			function i(t) {
				if (t) {
					var e, i, n, r, o, a, l, u;
					s.apply(this, [t]), e = this.params(), i = (e.chrome || this.dataAttr("chrome") || "").split(" "), this.preview = e.previewParams, this.widgetId = e.widgetId || this.dataAttr("widget-id"), this.instanceId = ++q, this.cursors = {
						maxPosition: 0,
						minPosition: 0
					}, this.override = (r = e.screenName || this.dataAttr("screen-name")) || (o = e.userId || this.dataAttr("user-id")) ? {
						overrideType: "user",
						overrideId: o,
						overrideName: r,
						withReplies: w.asBoolean(e.showReplies || this.dataAttr("show-replies")) ? "true" : "false"
					} : (r = e.favoritesScreenName || this.dataAttr("favorites-screen-name")) || (o = e.favoritesUserId || this.dataAttr("favorites-user-id")) ? {
						overrideType: "favorites",
						overrideId: o,
						overrideName: r
					} : ((r = e.listOwnerScreenName || this.dataAttr("list-owner-screen-name")) || (o = e.listOwnerId || this.dataAttr("list-owner-id"))) && ((a = e.listId || this.dataAttr("list-id")) || (l = e.listSlug || this.dataAttr("list-slug"))) ? {
						overrideType: "list",
						overrideOwnerId: o,
						overrideOwnerName: r,
						overrideId: a,
						overrideName: l
					} : (u = e.customTimelineId || this.dataAttr("custom-timeline-id")) ? {
						overrideType: "custom",
						overrideId: u
					} : {}, this.tweetLimit = w.asInt(e.tweetLimit || this.dataAttr("tweet-limit")), this.staticTimeline = this.tweetLimit > 0, i.length && (n = v.contains(i, "none"), this.chromeless = n || v.contains(i, "transparent"), this.headerless = n || v.contains(i, "noheader"), this.footerless = n || v.contains(i, "nofooter"), this.borderless = n || v.contains(i, "noborders"), this.noscrollbar = v.contains(i, "noscrollbar")), this.headingStyle = p.sanitize(e.headingStyle || this.dataAttr("heading-style"), void 0, !0), this.classAttr.push("twitter-timeline-rendered"), this.ariaPolite = e.ariaPolite || this.dataAttr("aria-polite")
				}
			}
			var n = t("env/window"),
				r = t("assets/css"),
				o = t("tfw/widget/base"),
				s = t("tfw/widget/syndicatedbase"),
				a = t("util/datetime"),
				l = t("anim/transition"),
				u = t("performance/perf-timers"),
				c = t("tfw/util/data"),
				d = t("tfw/util/media"),
				h = t("scribe/audience"),
				f = t("scribe/frame"),
				m = t("tfw/util/params"),
				p = t("util/css"),
				g = t("util/env"),
				w = t("util/typevalidator"),
				v = t("util/util"),
				b = t("dom/delegate"),
				y = t("dom/classname"),
				_ = t("dom/get"),
				T = t("util/donottrack"),
				x = t("util/document"),
				A = t("globals/twttr"),
				E = t("globals/private"),
				I = {
					CLIENT_SIDE_USER: 0,
					CLIENT_SIDE_APP: 2
				},
				S = ".timeline",
				N = ".new-tweets-bar",
				D = ".timeline-header",
				R = ".timeline-footer",
				k = ".stream",
				P = ".h-feed",
				L = ".tweet",
				C = ".detail-expander",
				M = ".expand",
				O = ".permalink",
				F = ".no-more-pane",
				j = "expanded",
				H = "pending-scroll-in",
				W = "pending-new-tweet-display",
				U = "pending-new-tweet",
				q = 0;
			i.prototype = new s, v.aug(i.prototype, {
				renderedClassNames: "twitter-timeline twitter-timeline-rendered",
				dimensions: {
					DEFAULT_HEIGHT: "600",
					DEFAULT_WIDTH: "520",
					NARROW_WIDTH: "320",
					maxHeight: "375",
					MIN_WIDTH: "180",
					MIN_HEIGHT: "200",
					MARGIN: "0",
					WIDE_MEDIA_PADDING: 81,
					NARROW_MEDIA_PADDING: 16,
					WIDE_MEDIA_PADDING_CL: 60,
					NARROW_MEDIA_PADDING_CL: 12,
					BORDERS: 2
				},
				styleSheetUrl: r.timeline,
				create: function (t) {
					var e, i, n, r, o = this,
						s = this.sandbox.createElement("div"),
						a = [];
					return s.innerHTML = t.body, (e = s.children[0] || !1) ? (this.reconfigure(t.config), this.discardStaticOverflow(e), this.sandbox.setTitle(e.getAttribute("data-iframe-title") || "Timeline"), d.retinize(e), this.constrainMedia(e), this.searchQuery = e.getAttribute("data-search-query"), this.profileId = e.getAttribute("data-profile-id"), this.timelineType = e.getAttribute("data-timeline-type"), r = this.getTweetDetails(s.querySelector(P)), v.forIn(r, function (t) {
						a.push(t)
					}), n = this.baseScribeData(), n.item_ids = a, n.item_details = r, this.timelineType && f.clientEvent({
						page: this.timelineType + "_timeline",
						component: "timeline",
						element: "initial",
						action: a.length ? "results" : "no_results"
					}, n, !0), f.clientEvent({
						page: "timeline",
						component: "timeline",
						element: "initial",
						action: a.length ? "results" : "no_results"
					}, n, !0), h.scribeTimelineAudienceImpression(), f.flush(), "assertive" == this.ariaPolite && (i = e.querySelector(N), i.setAttribute("aria-polite", "assertive")), e.id = this.id, e.className += " " + this.classAttr.join(" "), e.lang = this.lang, this.ready().then(function (t) {
						t.appendChild(e).then(function () {
							o.renderResolver.fulfill(o.sandbox)
						}), t.style({
							display: "inline-block"
						}), o.layout(function () {
							o.srcEl && o.srcEl.parentNode && o.srcEl.parentNode.removeChild(o.srcEl), o.predefinedWidth = o.width, o.predefinedHeight = o.height, o.width = t.width(o.width), o.height = t.height(o.height)
						}).then(function () {
							o.setNarrow(), o.sandbox.onresize(o.handleResize.bind(o)), o.completeResolver.fulfill(o.sandbox.element())
						})
					}), e) : void 0
				},
				render: function () {
					var t = this;
					return this.preview || this.widgetId ? (this.rendered().then(this.staticTimeline ? function (t) {
						t.resizeToContent(), o.doLayoutAsync()
					} : function () {
						t.recalculateStreamHeight(), o.doLayoutAsync()
					}), this.preview ? this.getPreviewTimeline() : this.getTimeline(), this.completed().then(this.scribePerformance.bind(this)), this.completed()) : (this.completeResolver.reject(400), this.completed())
				},
				scribePerformance: function () {
					u.endAndTrack("render", "widgets-js-load", "timeline", this.baseScribeData())
				},
				getPreviewTimeline: function () {
					var t = this;
					c.timelinePreview({
						success: function (e) {
							t.ready().then(function () {
								t.element = t.create(e), t.readTranslations(), t.bindInteractions(), t.updateCursors(e.headers, {
									initial: !0
								}), o.doLayoutAsync()
							})
						},
						error: function (e) {
							return e && e.headers ? void t.completeResolver.reject(e.headers.status) : void t.completeResolver.fulfill(t.srcEl)
						},
						params: this.preview
					})
				},
				getTimeline: function () {
					var t = this;
					f.init(), c.timeline(v.aug({
						id: this.widgetId,
						instanceId: this.instanceId,
						dnt: T.enabled(),
						lang: this.lang,
						success: function (e) {
							t.ready().then(function () {
								t.element = t.create(e), t.readTranslations(), t.bindInteractions(), t.updateTimeStamps(), t.updateCursors(e.headers, {
									initial: !0
								}), e.headers.xPolling && /\d/.test(e.headers.xPolling) && (t.pollInterval = 1e3 * e.headers.xPolling), t.staticTimeline || t.schedulePolling(), o.doLayoutAsync()
							})
						},
						error: function (e) {
							return e && e.headers ? void t.completeResolver.reject(e.headers.status) : void t.completeResolver.fulfill(t.srcEl)
						}
					}, this.override))
				},
				reconfigure: function (t) {
					this.lang = t.lang, this.theme || (this.theme = t.theme), "dark" == this.theme && this.classAttr.push("thm-dark"), this.chromeless && this.classAttr.push("var-chromeless"), this.borderless && this.classAttr.push("var-borderless"), this.headerless && this.classAttr.push("var-headerless"), this.footerless && this.classAttr.push("var-footerless"), this.staticTimeline && this.classAttr.push("var-static"), !this.linkColor && t.linkColor && s.VALID_COLOR.test(t.linkColor) && (this.linkColor = RegExp.$1), !this.height && s.VALID_UNIT.test(t.height) && (this.height = RegExp.$1), this.height = Math.max(this.dimensions.MIN_HEIGHT, this.height ? this.height : this.dimensions.DEFAULT_HEIGHT), this.preview && this.classAttr.push("var-preview"), this.narrow = this.width <= this.dimensions.NARROW_WIDTH, this.narrow && this.classAttr.push("var-narrow"), this.addSiteStyles()
				},
				getTweetDetails: function (t) {
					var e, i = this,
						n = {};
					return e = t && t.children || [], v.toRealArray(e).forEach(function (t) {
						v.aug(n, i.extractTweetScribeDetails(t))
					}), n
				},
				baseScribeData: function () {
					return {
						widget_id: this.widgetId,
						widget_origin: x.rootDocumentLocation(),
						widget_frame: x.isFramed() && x.currentDocumentLocation(),
						message: this.partner,
						query: this.searchQuery,
						profile_id: this.profileId
					}
				},
				bindInteractions: function () {
					var t = this,
						e = this.element,
						i = !0;
					this.bindIntentHandlers(), this.bindUIHandlers(), b.delegate(e, "click", ".load-tweets", function (e) {
						i && (i = !1, t.forceLoad(), b.stop(e))
					}), b.delegate(e, "click", ".display-sensitive-image", function (i) {
						t.showNSFW(_.closest(L, this, e)), b.stop(i)
					}), b.delegate(e, "mouseover", S, function () {
						t.mouseOver = !0
					}), b.delegate(e, "mouseout", S, function () {
						t.mouseOver = !1
					}), b.delegate(e, "mouseover", N, function () {
						t.mouseOverNotifier = !0
					}), b.delegate(e, "mouseout", N, function () {
						t.mouseOverNotifier = !1, n.setTimeout(function () {
							t.hideNewTweetNotifier()
						}, 3e3)
					}), this.staticTimeline || (b.delegate(e, "click", M, function (i) {
						i.altKey || i.metaKey || i.shiftKey || (t.toggleExpando(_.closest(L, this, e)), b.stop(i))
					}), b.delegate(e, "click", "A", function (t) {
						b.stopPropagation(t)
					}), b.delegate(e, "click", ".with-expansion", function (e) {
						t.toggleExpando(this), b.stop(e)
					}), b.delegate(e, "click", ".load-more", function () {
						t.loadMore()
					}), b.delegate(e, "click", N, function () {
						t.scrollToTop(), t.hideNewTweetNotifier(!0)
					}))
				},
				scrollToTop: function () {
					var t = this.element.querySelector(k);
					t.scrollTop = 0, t.focus()
				},
				update: function () {
					var t = this,
						e = this.element.querySelector(P),
						i = e && e.children[0],
						n = i && i.getAttribute("data-tweet-id");
					this.updateTimeStamps(), this.requestTweets(n, !0, function (e) {
						e.childNodes.length > 0 && t.insertNewTweets(e)
					})
				},
				loadMore: function () {
					var t = this,
						e = v.toRealArray(this.element.querySelectorAll(L)).pop(),
						i = e && e.getAttribute("data-tweet-id");
					this.requestTweets(i, !1, function (e) {
						var n = t.element.querySelector(F),
							r = e.childNodes[0];
						return n.style.cssText = "", r && r.getAttribute("data-tweet-id") == i && e.removeChild(r), e.childNodes.length > 0 ? void t.appendTweets(e) : (y.add(t.element, "no-more"), void n.focus())
					})
				},
				forceLoad: function () {
					var t = this,
						e = !!this.element.querySelectorAll(P).length;
					this.requestTweets(1, !0, function (i) {
						i.childNodes.length && (t[e ? "insertNewTweets" : "appendTweets"](i), y.add(t.element, "has-tweets"))
					})
				},
				schedulePolling: function (t) {
					var e = this;
					null !== this.pollInterval && (t = E.get("timeline.pollInterval") || t || this.pollInterval || 1e4, t > -1 && n.setTimeout(function () {
						e.isUpdating || e.update(), e.schedulePolling()
					}, t))
				},
				updateCursors: function (t, e) {
					(e || {}).initial ? (this.cursors.maxPosition = t.maxPosition, this.cursors.minPosition = t.minPosition) : (e || {}).newer ? this.cursors.maxPosition = t.maxPosition || this.cursors.maxPosition : this.cursors.minPosition = t.minPosition || this.cursors.minPosition
				},
				requestTweets: function (t, e, i) {
					var n = this,
						r = {
							id: this.widgetId,
							instanceId: this.instanceId,
							screenName: this.widgetScreenName,
							userId: this.widgetUserId,
							withReplies: this.widgetShowReplies,
							dnt: T.enabled(),
							lang: this.lang
						};
					e && this.cursors.maxPosition ? r.minPosition = this.cursors.maxPosition : !e && this.cursors.minPosition ? r.maxPosition = this.cursors.minPosition : e ? r.sinceId = t : r.maxId = t, r.complete = function () {
						n.isUpdating = !1
					}, r.error = function (t) {
						if (t && t.headers) {
							if ("404" == t.headers.status) return void(n.pollInterval = null);
							if ("503" == t.headers.status) return void(n.pollInterval *= 1.5)
						}
					}, r.success = function (t) {
						var r, o, s = n.sandbox.createDocumentFragment(),
							a = n.sandbox.createElement("ol"),
							l = [];
						if (n.updateCursors(t.headers, {
								newer: e
							}), t && t.headers && t.headers.xPolling && /\d+/.test(t.headers.xPolling) && (n.pollInterval = 1e3 * t.headers.xPolling), t && void 0 !== t.body) {
							if (a.innerHTML = t.body, a.children[0] && "LI" != a.children[0].tagName) return;
							for (o = n.getTweetDetails(a), v.forIn(o, function (t) {
									l.push(t)
								}), l.length && (r = n.baseScribeData(), r.item_ids = l, r.item_details = o, r.event_initiator = e ? I.CLIENT_SIDE_APP : I.CLIENT_SIDE_USER, n.timelineType && f.clientEvent({
									page: n.timelineType + "_timeline",
									component: "timeline",
									element: "initial",
									action: l.length ? "results" : "no_results"
								}, r, !0), f.clientEvent({
									page: "timeline",
									component: "timeline",
									element: e ? "newer" : "older",
									action: "results"
								}, r, !0), f.flush()), d.retinize(a), n.constrainMedia(a); a.children[0];) s.appendChild(a.children[0]);
							i(s)
						}
					}, c.timelinePoll(v.aug(r, this.override))
				},
				insertNewTweets: function (t) {
					var e, i = this,
						r = this.element.querySelector(k),
						o = r.querySelector(P),
						s = o.offsetHeight;
					return o.insertBefore(t, o.firstChild), e = o.offsetHeight - s, A.get("events").trigger("timelineUpdated", {
						target: this.sandbox.element(),
						region: "newer"
					}), r.scrollTop > 40 || this.mouseIsOver() ? (r.scrollTop = r.scrollTop + e, this.updateTimeStamps(), void this.showNewTweetNotifier()) : (y.remove(this.element, H), o.style.cssText = "margin-top: -" + e + "px", n.setTimeout(function () {
						r.scrollTop = 0, y.add(i.element, H), g.cssTransitions() ? o.style.cssText = "" : l.animate(function (t) {
							o.style.cssText = e > t ? "margin-top: -" + (e - t) + "px" : ""
						}, e, 500, l.easeOut)
					}, 500), this.updateTimeStamps(), void("custom" != this.timelineType && this.gcTweets(50)))
				},
				appendTweets: function (t) {
					var e = this.element.querySelector(P);
					e.appendChild(t), this.updateTimeStamps(), A.get("events").trigger("timelineUpdated", {
						target: this.sandbox.element(),
						region: "older"
					})
				},
				gcTweets: function (t) {
					var e, i = this.element.querySelector(P),
						n = i.children.length;
					for (t = t || 50; n > t && (e = i.children[n - 1]); n--) i.removeChild(e)
				},
				showNewTweetNotifier: function () {
					var t = this,
						e = this.element.querySelector(N),
						i = e.children[0];
					e.style.cssText = "", e.removeChild(i), e.appendChild(i), y.add(this.element, W), n.setTimeout(function () {
						y.add(t.element, U)
					}, 10), this.newNoticeDisplayTime = +new Date, n.setTimeout(function () {
						t.hideNewTweetNotifier()
					}, 5e3)
				},
				hideNewTweetNotifier: function (t) {
					var e = this;
					(t || !this.mouseOverNotifier) && (y.remove(this.element, U), n.setTimeout(function () {
						y.remove(e.element, W)
					}, 500))
				},
				discardStaticOverflow: function (t) {
					var e, i = t.querySelector(P);
					if (this.staticTimeline)
						for (this.height = 0; e = i.children[this.tweetLimit];) i.removeChild(e)
				},
				hideStreamScrollBar: function () {
					var t, e = this.element.querySelector(k),
						i = this.element.querySelector(P);
					e.style.width = "", t = this.element.offsetWidth - i.offsetWidth, t > 0 && (e.style.width = this.element.offsetWidth + t + "px")
				},
				readTranslations: function () {
					var t = this.element,
						e = "data-dt-";
					this.datetime = new a(v.compact({
						phrases: {
							now: t.getAttribute(e + "now"),
							s: t.getAttribute(e + "s"),
							m: t.getAttribute(e + "m"),
							h: t.getAttribute(e + "h"),
							second: t.getAttribute(e + "second"),
							seconds: t.getAttribute(e + "seconds"),
							minute: t.getAttribute(e + "minute"),
							minutes: t.getAttribute(e + "minutes"),
							hour: t.getAttribute(e + "hour"),
							hours: t.getAttribute(e + "hours")
						},
						months: t.getAttribute(e + "months").split("|"),
						formats: {
							abbr: t.getAttribute(e + "abbr"),
							shortdate: t.getAttribute(e + "short"),
							longdate: t.getAttribute(e + "long")
						}
					}))
				},
				updateTimeStamps: function () {
					for (var t, e, i, n, r = this.element.querySelectorAll(O), o = 0; t = r[o]; o++) i = t.getAttribute("data-datetime"), n = i && this.datetime.timeAgo(i, this.i18n), e = t.getElementsByTagName("TIME")[0], n && (e && e.innerHTML ? e.innerHTML = n : t.innerHTML = n)
				},
				mouseIsOver: function () {
					return this.mouseOver
				},
				addUrlParams: function (t) {
					var e = this,
						i = {
							tw_w: this.widgetId,
							related: this.related,
							partner: this.partner,
							query: this.searchQuery,
							profile_id: this.profileId,
							original_referer: x.rootDocumentLocation(),
							tw_p: "embeddedtimeline"
						};
					return this.addUrlParams = m(i, function (t) {
						var i = _.closest(L, t, e.element);
						return i && {
							tw_i: i.getAttribute("data-tweet-id")
						}
					}), this.addUrlParams(t)
				},
				showNSFW: function (t) {
					var e, i, n, r, o, s, a = t.querySelector(".nsfw"),
						l = 0;
					a && (i = d.scaleDimensions(a.getAttribute("data-width"), a.getAttribute("data-height"), this.contentWidth(), a.getAttribute("data-height")), e = !!(r = a.getAttribute("data-player")), e ? o = this.sandbox.createElement("iframe") : (o = this.sandbox.createElement("img"), r = a.getAttribute(g.retina() ? "data-image-2x" : "data-image"), o.alt = a.getAttribute("data-alt"), s = this.sandbox.createElement("a"), s.href = a.getAttribute("data-href"), s.appendChild(o)), o.title = a.getAttribute("data-title"), o.src = r, o.width = i.width, o.height = i.height, n = _.closest(C, a, t), l = i.height - a.offsetHeight, a.parentNode.replaceChild(e ? o : s, a), n.style.cssText = "height:" + (n.offsetHeight + l) + "px")
				},
				toggleExpando: function (t) {
					var e, i, n = t.querySelector(C),
						r = n && n.children[0],
						s = r && r.getAttribute("data-expanded-media"),
						a = 0,
						l = t.querySelector(M),
						u = l && l.getElementsByTagName("B")[0],
						c = u && (u.innerText || u.textContent);
					if (u) {
						if (this.layout(function () {
								u.innerHTML = l.getAttribute("data-toggled-text"), l.setAttribute("data-toggled-text", c)
							}), y.present(t, j)) return this.layout(function () {
							y.remove(t, j)
						}), n ? (this.layout(function () {
							n.style.cssText = "", r.innerHTML = ""
						}), void o.doLayout()) : void o.doLayout();
						s && (e = this.sandbox.createElement("DIV"), e.innerHTML = s, d.retinize(e), a = this.constrainMedia(e), this.layout(function () {
							r.appendChild(e)
						})), n && this.layout(function () {
							i = Math.max(r.offsetHeight, a), n.style.cssText = "height:" + i + "px"
						}), this.layout(function () {
							y.add(t, j)
						}), o.doLayout()
					}
				},
				recalculateStreamHeight: function (t) {
					var e = this,
						i = this.element.querySelector(D),
						n = this.element.querySelector(R),
						r = this.element.querySelector(k);
					this.layout(function () {
						var o = i.offsetHeight + (n ? n.offsetHeight : 0),
							s = t || e.sandbox.height();
						r.style.cssText = "height:" + (s - o - 2) + "px", e.noscrollbar && e.hideStreamScrollBar()
					})
				},
				handleResize: function (t, e) {
					var i = this,
						n = Math.min(this.dimensions.DEFAULT_WIDTH, Math.max(this.dimensions.MIN_WIDTH, Math.min(this.predefinedWidth || this.dimensions.DEFAULT_WIDTH, t)));
					(n != this.width || e != this.height) && (this.width = n, this.height = e, this.setNarrow(), this.constrainMedia(this.element, this.contentWidth(n)), this.staticTimeline ? this.layout(function () {
						i.height = i.element.offsetHeight, i.sandbox.height(i.height), A.get("events").trigger("resize", {
							target: i.sandbox.element()
						})
					}) : (this.recalculateStreamHeight(e), A.get("events").trigger("resize", {
						target: this.sandbox.element()
					})), o.doLayoutAsync())
				}
			}), e.exports = i
		}, {
			"anim/transition": 2,
			"assets/css": 3,
			"dom/classname": 5,
			"dom/delegate": 6,
			"dom/get": 7,
			"env/window": 14,
			"globals/private": 18,
			"globals/twttr": 19,
			"performance/perf-timers": 23,
			"scribe/audience": 30,
			"scribe/frame": 31,
			"tfw/util/data": 38,
			"tfw/util/media": 40,
			"tfw/util/params": 41,
			"tfw/widget/base": 42,
			"tfw/widget/syndicatedbase": 46,
			"util/css": 50,
			"util/datetime": 51,
			"util/document": 52,
			"util/donottrack": 54,
			"util/env": 55,
			"util/typevalidator": 66,
			"util/util": 69
		}],
		48: [function (t, e) {
			function i(t) {
				o.apply(this, [t]);
				var e = this.params(),
					i = e.count || this.dataAttr("count"),
					n = e.size || this.dataAttr("size"),
					r = l.getScreenNameFromPage(),
					c = "" + (e.shareWithRetweet || this.dataAttr("share-with-retweet") || s.val("share-with-retweet"));
				this.classAttr.push("twitter-tweet-button"), "hashtag" == e.type || a.contains(this.classAttr, "twitter-hashtag-button") ? (this.type = "hashtag", this.classAttr.push("twitter-hashtag-button")) : "mention" == e.type || a.contains(this.classAttr, "twitter-mention-button") ? (this.type = "mention", this.classAttr.push("twitter-mention-button")) : this.classAttr.push("twitter-share-button"), this.text = e.text || this.dataAttr("text"), this.text && /\+/.test(this.text) && !/ /.test(this.text) && (this.text = this.text.replace(/\+/g, " ")), this.counturl = e.counturl || this.dataAttr("counturl"), this.searchlink = e.searchlink || this.dataAttr("searchlink"), this.button_hashtag = u.hashTag(e.button_hashtag || e.hashtag || this.dataAttr("button-hashtag"), !1), this.size = "large" == n ? "l" : "m", this.align = e.align || this.dataAttr("align") || "", this.via = e.via || this.dataAttr("via"), this.hashtags = e.hashtags || this.dataAttr("hashtags"), this.screen_name = u.screenName(e.screen_name || e.screenName || this.dataAttr("button-screen-name")), this.url = e.url || this.dataAttr("url"), this.type ? (this.count = "none", this.shareWithRetweet = "never", r && (this.related = this.related ? r + "," + this.related : r)) : (this.text = this.text || h, this.url = this.url || l.getCanonicalURL() || f, this.count = a.contains(m, i) ? i : "horizontal", this.count = "vertical" == this.count && "l" == this.size ? "none" : this.count, this.via = this.via || r, c && a.contains(p, c) && (this.shareWithRetweet = c.replace("-", "_")))
			}
			var n = t("env/document"),
				r = t("env/location"),
				o = t("tfw/widget/base"),
				s = t("globals/pagemetadata"),
				a = t("util/util"),
				l = t("util/uri"),
				u = t("util/twitter"),
				c = t("dom/textsize"),
				d = t("util/donottrack"),
				h = n.title,
				f = r.href,
				m = ["vertical", "horizontal", "none"],
				p = ["never", "publisher-first", "publisher-only", "author-first", "author-only"];
			i.prototype = new o, a.aug(i.prototype, {
				iframeSource: "widgets/tweet_button.969b16495674bbe6e2f655caeedb071c.{{lang}}.html",
				widgetUrlParams: function () {
					return a.compact({
						text: this.text,
						url: this.url,
						via: this.via,
						related: this.related,
						count: this.count,
						lang: this.lang,
						counturl: this.counturl,
						searchlink: this.searchlink,
						placeid: this.placeid,
						original_referer: r.href,
						id: this.id,
						size: this.size,
						type: this.type,
						screen_name: this.screen_name,
						share_with_retweet: this.shareWithRetweet,
						button_hashtag: this.button_hashtag,
						hashtags: this.hashtags,
						align: this.align,
						partner: this.partner,
						dnt: d.enabled(),
						_: +new Date
					})
				},
				height: function () {
					return "vertical" == this.count ? 62 : "m" == this.size ? 20 : 28
				},
				width: function () {
					var t = {
							ver: 8,
							cnt: 14,
							btn: 24,
							xlcnt: 18,
							xlbtn: 38
						},
						e = "vertical" == this.count,
						i = "hashtag" == this.type && this.button_hashtag ? "Tweet %{hashtag}" : "mention" == this.type && this.screen_name ? "Tweet to %{name}" : "Tweet",
						n = this._(i, {
							name: "@" + this.screen_name,
							hashtag: "#" + this.button_hashtag
						}),
						r = this._("K"),
						o = this._("100K+"),
						s = (e ? "8888" : "88888") + r,
						l = 0,
						u = 0,
						d = 0,
						h = 0,
						f = this.styles.base,
						m = f;
					return a.contains(["ja", "ko"], this.lang) ? s += this._("10k unit") : s = s.length > o.length ? s : o, e ? (m = f.concat(this.styles.vbubble), h = t.ver, d = t.btn) : "l" == this.size ? (f = m = f.concat(this.styles.large), d = t.xlbtn, h = t.xlcnt) : (d = t.btn, h = t.cnt), "none" != this.count && (u = c(s, "", m).width + h), l = c(n, "", f.concat(this.styles.button)).width + d, e ? l > u ? l : u : this.calculatedWidth = l + u
				},
				render: function () {
					var t, e = this,
						i = this.makeIframeSource();
					return this.count && this.classAttr.push("twitter-count-" + this.count), t = this.create(i, this.dimensions(), {
						title: this._("Twitter Tweet Button")
					}).then(function (t) {
						return e.element = t
					})
				}
			}), e.exports = i
		}, {
			"dom/textsize": 10,
			"env/document": 11,
			"env/location": 12,
			"globals/pagemetadata": 17,
			"tfw/widget/base": 42,
			"util/donottrack": 54,
			"util/twitter": 65,
			"util/uri": 68,
			"util/util": 69
		}],
		49: [function (t, e) {
			function i(t, e, i, n) {
				v[t] = v[t] || [], v[t].push({
					s: i,
					f: n,
					lang: e
				})
			}

			function n(t, e) {
				var i = {};
				i[t] = {
					item_type: 0
				}, p.clientEvent({
					page: "video",
					component: "tweet",
					action: "results"
				}, d.aug({}, e, {
					item_ids: [t],
					item_details: i
				}), !0), m.scribeVideoAudienceImpression()
			}

			function r(t, e) {
				var i = {};
				i[t] = {
					item_type: 0
				}, p.clientEvent({
					page: "video",
					component: "rawembedcode",
					action: "no_results"
				}, {
					widget_origin: h.rootDocumentLocation(),
					widget_frame: h.isFramed() && h.currentDocumentLocation(),
					message: e,
					item_ids: [t],
					item_details: i
				}, !0), m.scribeVideoAudienceImpression()
			}

			function o(t) {
				if (t) {
					l.apply(this, [t]);
					var e = this.srcEl && this.srcEl.getElementsByTagName("A"),
						i = e && e[e.length - 1],
						n = this.params();
					this.hideStatus = "hidden" === (n.status || this.dataAttr("status")), this.tweetId = n.tweetId || i && w.status(i.href)
				}
			}
			var s = t("assets/css"),
				a = t("tfw/widget/base"),
				l = t("tfw/widget/syndicatedbase"),
				u = t("util/datetime"),
				c = t("util/promise"),
				d = t("util/util"),
				h = t("util/document"),
				f = t("tfw/util/data"),
				m = t("scribe/audience"),
				p = t("scribe/frame"),
				g = t("globals/twttr"),
				w = t("util/twitter"),
				v = {},
				b = [];
			o.prototype = new l, d.aug(o.prototype, {
				renderedClassNames: "twitter-video twitter-video-rendered",
				videoPlayer: !0,
				dimensions: {
					DEFAULT_HEIGHT: "360",
					DEFAULT_WIDTH: "640",
					maxHeight: "500",
					MIN_WIDTH: "320",
					MIN_HEIGHT: "180",
					MARGIN: "10px 0",
					WIDE_MEDIA_PADDING: 0,
					NARROW_MEDIA_PADDING: 0,
					BORDERS: 0
				},
				styleSheetUrl: s.video,
				create: function (t) {
					var e, i = this,
						r = this.sandbox.createElement("div");
					return r.innerHTML = t, (e = r.children[0]) ? (this.playerConfig = JSON.parse(e.getAttribute("data-player-config")), this.sandbox.setTitle(e.getAttribute("data-iframe-title") || "Video"), this.sandbox.appendChild(e).then(function () {
						i.renderResolver.fulfill(i.sandbox)
					}), this.layout(function () {
						i.predefinedWidth = i.width, i.width = i.sandbox.width(i.width), i.constrainMedia(e, i.contentWidth(i.width)), i.completeResolver.fulfill(i.sandbox.element())
					}), n(this.tweetId, this.baseScribeData()), e) : void 0
				},
				render: function () {
					var t = this;
					return this.tweetId ? (this.rendered().then(function (e) {
						var i = t.srcEl;
						i && i.parentNode && t.layout(function () {
							i && i.parentNode && i.parentNode.removeChild(i)
						}), t.layout(function () {
							t.height = t.sandbox.height(t.element.offsetHeight)
						}).then(function () {
							e.onresize(t.handleResize.bind(t))
						}), a.doLayoutAsync()
					}), i(this.tweetId, this.lang, function (e) {
						t.ready().then(function () {
							t.element = t.create(e), t.readTimestampTranslations(), t.writePlayerConfig(), a.doLayoutAsync()
						})
					}, function () {
						r(t.tweetId, t.partner), t.completeResolver.fulfill(t.srcEl)
					}), b.push(this.completed()), this.completed()) : (this.completeResolver.fulfill(this.srcEl), this.completed())
				},
				handleResize: function (t) {
					var e = this;
					t != this.width && (this.width = t, this.constrainMedia(this.element, this.contentWidth(this.width)), this.layout(function () {
						e.height = e.sandbox.height(e.element.offsetHeight), g.get("events").trigger("resize", {
							target: e.sandbox.element()
						})
					}), a.doLayoutAsync())
				},
				baseScribeData: function () {
					return {
						widget_origin: h.rootDocumentLocation(),
						widget_frame: h.isFramed() && h.currentDocumentLocation(),
						message: this.partner
					}
				},
				readTimestampTranslations: function () {
					var t = this.element,
						e = "data-dt-",
						i = t.getAttribute(e + "months") || "";
					this.datetime = new u(d.compact({
						phrases: {
							AM: t.getAttribute(e + "am"),
							PM: t.getAttribute(e + "pm")
						},
						months: i.split("|"),
						formats: {
							full: t.getAttribute(e + "full")
						}
					}))
				},
				getTimestamp: function () {
					var t = this.element.getAttribute("data-datetime"),
						e = t && this.datetime.localTimeStamp(t);
					return {
						local: e
					}
				},
				writePlayerConfig: function () {
					this.playerConfig.statusTimestamp = this.getTimestamp(), this.playerConfig.hideStatus = this.hideStatus, this.element.setAttribute("data-player-config", JSON.stringify(this.playerConfig));

				}
			}), o.fetchAndRender = function () {
				var t = v,
					e = [];
				v = {};
				for (var i in t) t.hasOwnProperty(i) && e.push(i);
				e.length && (f.videos({
					ids: e.sort(),
					lang: t[e[0]][0].lang,
					complete: function (e) {
						d.forIn(e, function (e, i) {
							var n = t[e];
							n.forEach(function (t) {
								t.s && t.s.call(this, i)
							}), delete t[e]
						}), a.doLayout(), d.forIn(t, function (t, e) {
							e.forEach(function (e) {
								e.f && e.f.call(this, t)
							})
						}), a.doLayout()
					}
				}), c.every.apply(null, b), b = [])
			}, a.afterLoad(o.fetchAndRender), e.exports = o
		}, {
			"assets/css": 3,
			"globals/twttr": 19,
			"scribe/audience": 30,
			"scribe/frame": 31,
			"tfw/util/data": 38,
			"tfw/widget/base": 42,
			"tfw/widget/syndicatedbase": 46,
			"util/datetime": 51,
			"util/document": 52,
			"util/promise": 62,
			"util/twitter": 65,
			"util/util": 69
		}],
		50: [function (t, e) {
			e.exports = {
				sanitize: function (t, e, i) {
					var n, r = /^[\w ,%\/"'\-_#]+$/,
						o = t && t.split(";").map(function (t) {
							return t.split(":").slice(0, 2).map(function (t) {
								return t.trim()
							})
						}),
						s = 0,
						a = [],
						l = i ? "!important" : "";
					for (e = e || /^(font|text\-|letter\-|color|line\-)[\w\-]*$/; o && (n = o[s]); s++) n[0].match(e) && n[1].match(r) && a.push(n.join(":") + l);
					return a.join(";")
				}
			}
		}, {}],
		51: [function (t, e) {
			function i(t) {
				return 10 > t ? "0" + t : t
			}

			function n(t) {
				function e(t, e) {
					return r && r[t] && (t = r[t]), t.replace(/%\{([\w_]+)\}/g, function (t, i) {
						return void 0 !== e[i] ? e[i] : t
					})
				}
				var r = t && t.phrases,
					o = t && t.months || a,
					s = t && t.formats || l;
				this.timeAgo = function (t) {
					var i, r = n.parseDate(t),
						a = +new Date,
						l = a - r;
					return r ? isNaN(l) || 2 * u > l ? e("now") : c > l ? (i = Math.floor(l / u), e(s.abbr, {
						number: i,
						symbol: e(f, {
							abbr: e("s"),
							expanded: e(i > 1 ? "seconds" : "second")
						})
					})) : d > l ? (i = Math.floor(l / c), e(s.abbr, {
						number: i,
						symbol: e(f, {
							abbr: e("m"),
							expanded: e(i > 1 ? "minutes" : "minute")
						})
					})) : h > l ? (i = Math.floor(l / d), e(s.abbr, {
						number: i,
						symbol: e(f, {
							abbr: e("h"),
							expanded: e(i > 1 ? "hours" : "hour")
						})
					})) : 365 * h > l ? e(s.shortdate, {
						day: r.getDate(),
						month: e(o[r.getMonth()])
					}) : e(s.longdate, {
						day: r.getDate(),
						month: e(o[r.getMonth()]),
						year: r.getFullYear().toString().slice(2)
					}) : ""
				}, this.localTimeStamp = function (t) {
					var r = n.parseDate(t),
						a = r && r.getHours();
					return r ? e(s.full, {
						day: r.getDate(),
						month: e(o[r.getMonth()]),
						year: r.getFullYear(),
						hours24: i(a),
						hours12: 13 > a ? a ? a : "12" : a - 12,
						minutes: i(r.getMinutes()),
						seconds: i(r.getSeconds()),
						amPm: e(12 > a ? "AM" : "PM")
					}) : ""
				}
			}
			var r = /(\d{4})-?(\d{2})-?(\d{2})T(\d{2}):?(\d{2}):?(\d{2})(Z|[\+\-]\d{2}:?\d{2})/,
				o = /[a-z]{3,4} ([a-z]{3}) (\d{1,2}) (\d{1,2}):(\d{2}):(\d{2}) ([\+\-]\d{2}:?\d{2}) (\d{4})/i,
				s = /^\d+$/,
				a = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
				l = {
					abbr: "%{number}%{symbol}",
					shortdate: "%{day} %{month}",
					longdate: "%{day} %{month} %{year}",
					full: "%{hours12}:%{minutes} %{amPm} - %{day} %{month} %{year}"
				},
				u = 1e3,
				c = 60 * u,
				d = 60 * c,
				h = 24 * d,
				f = '<abbr title="%{expanded}">%{abbr}</abbr>';
			n.parseDate = function (t) {
				var e, i, n = t || "",
					l = n.toString();
				return (e = function () {
					var t;
					return s.test(l) ? parseInt(l, 10) : (t = l.match(o)) ? Date.UTC(t[7], a.indexOf(t[1]), t[2], t[3], t[4], t[5]) : (t = l.match(r)) ? Date.UTC(t[1], t[2] - 1, t[3], t[4], t[5], t[6]) : void 0
				}()) ? (i = new Date(e), !isNaN(i.getTime()) && i) : !1
			}, e.exports = n
		}, {}],
		52: [function (t, e) {
			function i(t) {
				return t && a.isType("string", t) && (l = t), l
			}

			function n() {
				return u
			}

			function r() {
				return l !== u
			}
			var o = t("env/location"),
				s = t("util/uri"),
				a = t("util/util"),
				l = s.getCanonicalURL() || o.href,
				u = l;
			e.exports = {
				isFramed: r,
				rootDocumentLocation: i,
				currentDocumentLocation: n
			}
		}, {
			"env/location": 12,
			"util/uri": 68,
			"util/util": 69
		}],
		53: [function (t, e) {
			function i() {
				l = 1;
				for (var t = 0, e = u.length; e > t; t++) u[t]()
			}
			var n, r, o, s = t("env/document"),
				a = t("env/window"),
				l = 0,
				u = [],
				c = !1,
				d = s.createElement("a");
			/^loade|c/.test(s.readyState) && (l = 1), s.addEventListener && s.addEventListener("DOMContentLoaded", r = function () {
				s.removeEventListener("DOMContentLoaded", r, c), i()
			}, c), d.doScroll && s.attachEvent("onreadystatechange", n = function () {
				/^c/.test(s.readyState) && (s.detachEvent("onreadystatechange", n), i())
			}), o = d.doScroll ? function (t) {
				a.self != a.top ? l ? t() : u.push(t) : ! function () {
					try {
						d.doScroll("left")
					} catch (e) {
						return setTimeout(function () {
							o(t)
						}, 50)
					}
					t()
				}()
			} : function (t) {
				l ? t() : u.push(t)
			}, e.exports = o
		}, {
			"env/document": 11,
			"env/window": 14
		}],
		54: [function (t, e) {
			function i() {
				d = !0
			}

			function n(t, e) {
				return d ? !0 : u.asBoolean(c.val("dnt")) ? !0 : !s || 1 != s.doNotTrack && 1 != s.msDoNotTrack ? l.isUrlSensitive(e || o.host) ? !0 : a.isFramed() && l.isUrlSensitive(a.rootDocumentLocation()) ? !0 : (t = h.test(t || r.referrer) && RegExp.$1, t && l.isUrlSensitive(t) ? !0 : !1) : !0
			}
			var r = t("env/document"),
				o = t("env/location"),
				s = t("env/navigator"),
				a = t("util/document"),
				l = t("util/tld"),
				u = t("util/typevalidator"),
				c = t("globals/pagemetadata"),
				d = !1,
				h = /https?:\/\/([^\/]+).*/i;
			e.exports = {
				setOn: i,
				enabled: n
			}
		}, {
			"env/document": 11,
			"env/location": 12,
			"env/navigator": 13,
			"globals/pagemetadata": 17,
			"util/document": 52,
			"util/tld": 64,
			"util/typevalidator": 66
		}],
		55: [function (t, e) {
			function i(t) {
				return t = t || p, t.devicePixelRatio ? t.devicePixelRatio >= 1.5 : t.matchMedia ? t.matchMedia("only screen and (min-resolution: 144dpi)").matches : !1
			}

			function n(t) {
				return t = t || T, /(Trident|MSIE \d)/.test(t)
			}

			function r(t) {
				return t = t || T, /MSIE 9/.test(t)
			}

			function o(t) {
				return t = t || T, /(iPad|iPhone|iPod)/.test(t)
			}

			function s(t) {
				return t = t || T, /^Mozilla\/5\.0 \(Linux; (U; )?Android/.test(t)
			}

			function a() {
				return x
			}

			function l(t, e) {
				return t = t || p, e = e || T, t.postMessage && !(n(e) && t.opener)
			}

			function u(t) {
				t = t || m;
				try {
					return !!t.plugins["Shockwave Flash"] || !!new ActiveXObject("ShockwaveFlash.ShockwaveFlash")
				} catch (e) {
					return !1
				}
			}

			function c(t, e, i) {
				return t = t || p, e = e || m, i = i || T, "ontouchstart" in t || /Opera Mini/.test(i) || e.msMaxTouchPoints > 0
			}

			function d() {
				var t = f.body.style;
				return void 0 !== t.transition || void 0 !== t.webkitTransition || void 0 !== t.mozTransition || void 0 !== t.oTransition || void 0 !== t.msTransition
			}

			function h() {
				return !!(p.Promise && p.Promise.resolve && p.Promise.reject && p.Promise.all && p.Promise.race && function () {
					var t;
					return new p.Promise(function (e) {
						t = e
					}), b.isType("function", t)
				}())
			}
			var f = t("env/document"),
				m = t("env/navigator"),
				p = t("env/window"),
				g = t("util/domready"),
				w = t("util/logger"),
				v = t("util/typevalidator"),
				b = t("util/util"),
				y = t("globals/pagemetadata"),
				_ = t("globals/private"),
				T = m.userAgent,
				x = !1,
				A = !1,
				E = "twitter-csp-test";
			_.set("verifyCSP", function (t) {
				var e = f.getElementById(E);
				A = !0, x = !!t, e && e.parentNode.removeChild(e)
			}), g(function () {
				var t;
				return v.asBoolean(y.val("widgets:csp")) ? x = !0 : (t = f.createElement("script"), t.id = E, t.text = _.fullPath("verifyCSP") + "(false);", f.body.appendChild(t), void p.setTimeout(function () {
					A || (w.warn('TWITTER: Content Security Policy restrictions may be applied to your site. Add <meta name="twitter:widgets:csp" content="on"> to supress this warning.'), w.warn("TWITTER: Please note: Not all embedded timeline and embedded Tweet functionality is supported when CSP is applied."))
				}, 5e3))
			}), e.exports = {
				retina: i,
				anyIE: n,
				ie9: r,
				ios: o,
				android: s,
				cspEnabled: a,
				flashEnabled: u,
				canPostMessage: l,
				touch: c,
				cssTransitions: d,
				hasPromiseSupport: h
			}
		}, {
			"env/document": 11,
			"env/navigator": 13,
			"env/window": 14,
			"globals/pagemetadata": 17,
			"globals/private": 18,
			"util/domready": 53,
			"util/logger": 59,
			"util/typevalidator": 66,
			"util/util": 69
		}],
		56: [function (t, e) {
			var i = t("util/util"),
				n = {
					bind: function (t, e) {
						return this._handlers = this._handlers || {}, this._handlers[t] = this._handlers[t] || [], this._handlers[t].push(e)
					},
					unbind: function (t, e) {
						if (this._handlers[t])
							if (e) {
								var i = this._handlers[t].indexOf(e);
								i >= 0 && this._handlers[t].splice(i, 1)
							} else this._handlers[t] = []
					},
					trigger: function (t, e) {
						var n = this._handlers && this._handlers[t];
						e = e || {}, e.type = t, n && n.forEach(function (t) {
							i.async(t.bind(this, e))
						})
					}
				};
			e.exports = {
				Emitter: n
			}
		}, {
			"util/util": 69
		}],
		57: [function (t, e) {
			var i = t("env/document"),
				n = t("util/util");
			e.exports = function (t, e, r) {
				var o;
				if (r = r || i, t = t || {}, e = e || {}, t.name) {
					try {
						o = r.createElement('<iframe name="' + t.name + '"></iframe>')
					} catch (s) {
						o = r.createElement("iframe"), o.name = t.name
					}
					delete t.name
				} else o = r.createElement("iframe");
				return t.id && (o.id = t.id, delete t.id), o.allowtransparency = "true", o.scrolling = "no", o.setAttribute("frameBorder", 0), o.setAttribute("allowTransparency", !0), n.forIn(t, function (t, e) {
					o.setAttribute(t, e)
				}), n.forIn(e, function (t, e) {
					o.style[t] = e
				}), o
			}
		}, {
			"env/document": 11,
			"util/util": 69
		}],
		58: [function (t, e) {
			function i() {}
			var n, r = t("env/window"),
				o = t("util/promise"),
				s = [];
			i.prototype.enqueue = function (t, e) {
				return new o(function (i) {
					s.push({
						action: t,
						resolver: i,
						note: e
					})
				})
			}, i.prototype.exec = function () {
				var t, e = s;
				if (e.length)
					for (s = []; e.length;) t = e.shift(), t && t.action ? t.resolver.fulfill(t.action()) : t.resolver.reject()
			}, i.prototype.delayedExec = function () {
				n && r.clearTimeout(n), n = r.setTimeout(this.exec, 100)
			}, e.exports = i
		}, {
			"env/window": 14,
			"util/promise": 62
		}],
		59: [function (t, e) {
			function i() {
				l("info", d.toRealArray(arguments))
			}

			function n() {
				l("warn", d.toRealArray(arguments))
			}

			function r() {
				l("error", d.toRealArray(arguments))
			}

			function o(t) {
				m && (f[t] = a())
			}

			function s(t) {
				var e;
				m && (f[t] ? (e = a(), i("_twitter", t, e - f[t])) : r("timeEnd() called before time() for id: ", t))
			}

			function a() {
				return c.performance && +c.performance.now() || +new Date
			}

			function l(t, e) {
				if (c[h] && c[h][t]) switch (e.length) {
				case 1:
					c[h][t](e[0]);
					break;
				case 2:
					c[h][t](e[0], e[1]);
					break;
				case 3:
					c[h][t](e[0], e[1], e[2]);
					break;
				case 4:
					c[h][t](e[0], e[1], e[2], e[3]);
					break;
				case 5:
					c[h][t](e[0], e[1], e[2], e[3], e[4]);
					break;
				default:
					0 !== e.length && c[h].warn && c[h].warn("too many params passed to logger." + t)
				}
			}
			var u = t("env/location"),
				c = t("env/window"),
				d = t("util/util"),
				h = ["con", "sole"].join(""),
				f = {},
				m = d.contains(u.href, "tw_debug=true");
			e.exports = {
				info: i,
				warn: n,
				error: r,
				time: o,
				timeEnd: s
			}
		}, {
			"env/location": 12,
			"env/window": 14,
			"util/util": 69
		}],
		60: [function (t, e) {
			function i(t) {
				return function (e) {
					return r.hasValue(e[t])
				}
			}

			function n() {
				this.assertions = [], this._defaults = {}
			}
			var r = t("util/typevalidator"),
				o = t("util/util");
			n.prototype.assert = function (t, e) {
				return this.assertions.push({
					fn: t,
					msg: e || "assertion failed"
				}), this
			}, n.prototype.defaults = function (t) {
				return this._defaults = t || this._defaults, this
			}, n.prototype.require = function (t) {
				var e = this;
				return t = Array.isArray(t) ? t : o.toRealArray(arguments), t.forEach(function (t) {
					e.assert(i(t), "required: " + t)
				}), this
			}, n.prototype.parse = function (t) {
				var e, i;
				if (e = o.aug({}, this._defaults, t || {}), i = this.assertions.reduce(function (t, i) {
						return i.fn(e) || t.push(i.msg), t
					}, []), i.length > 0) throw new Error(i.join("\n"));
				return e
			}, e.exports = n
		}, {
			"util/typevalidator": 66,
			"util/util": 69
		}],
		61: [function (t, e) {
			var i, n, r, o = t("util/querystring");
			i = function (t) {
				var e = t.search.substr(1);
				return o.decode(e)
			}, n = function (t) {
				var e = t.href,
					i = e.indexOf("#"),
					n = 0 > i ? "" : e.substring(i + 1);
				return o.decode(n)
			}, r = function (t) {
				var e, r = {},
					o = i(t),
					s = n(t);
				for (e in o) o.hasOwnProperty(e) && (r[e] = o[e]);
				for (e in s) s.hasOwnProperty(e) && (r[e] = s[e]);
				return r
			}, e.exports = {
				combined: r,
				fromQuery: i,
				fromFragment: n
			}
		}, {
			"util/querystring": 63
		}],
		62: [function (t, e) {
			function i(t) {
				var e, i, n;
				return e = new a(function (t, e) {
					i = t, n = e
				}), t && t({
					fulfill: i,
					reject: n
				}), e
			}
			var n = t("es6-promise").Promise,
				r = t("env/window"),
				o = t("util/env"),
				s = t("util/util"),
				a = o.hasPromiseSupport() ? r.Promise : n;
			i.fulfill = function (t) {
				return a.resolve(t)
			}, i.reject = function (t) {
				return a.reject(t)
			}, i.every = function () {
				var t = s.toRealArray(arguments);
				return a.all(t)
			}, i.some = function () {
				var t = s.toRealArray(arguments),
					e = 0;
				return t.length ? new a(function (i, n) {
					function r() {
						e += 1, e === t.length && n()
					}
					t.forEach(function (t) {
						t.then(i, r)
					})
				}) : a.reject("no promises passed to .some")
			}, i.isThenable = function (t) {
				try {
					var e = t.then;
					if ("function" == typeof e) return !0
				} catch (i) {}
				return !1
			}, e.exports = i
		}, {
			"env/window": 14,
			"es6-promise": 1,
			"util/env": 55,
			"util/util": 69
		}],
		63: [function (t, e) {
			function i(t) {
				return encodeURIComponent(t).replace(/\+/g, "%2B").replace(/'/g, "%27")
			}

			function n(t) {
				return decodeURIComponent(t)
			}

			function r(t) {
				var e = [];
				return u.forIn(t, function (t, n) {
					var r = i(t);
					u.isType("array", n) || (n = [n]), n.forEach(function (t) {
						l.hasValue(t) && e.push(r + "=" + i(t))
					})
				}), e.sort().join("&")
			}

			function o(t) {
				var e, i = {};
				return t ? (e = t.split("&"), e.forEach(function (t) {
					var e = t.split("="),
						r = n(e[0]),
						o = n(e[1]);
					return 2 == e.length ? u.isType("array", i[r]) ? void i[r].push(o) : r in i ? (i[r] = [i[r]], void i[r].push(o)) : void(i[r] = o) : void 0
				}), i) : {}
			}

			function s(t, e) {
				var i = r(e);
				return i.length > 0 ? u.contains(t, "?") ? t + "&" + r(e) : t + "?" + r(e) : t
			}

			function a(t) {
				var e = t && t.split("?");
				return 2 == e.length ? o(e[1]) : {}
			}
			var l = t("util/typevalidator"),
				u = t("util/util");
			e.exports = {
				url: s,
				decodeURL: a,
				decode: o,
				encode: r,
				encodePart: i,
				decodePart: n
			}
		}, {
			"util/typevalidator": 66,
			"util/util": 69
		}],
		64: [function (t, e) {
			function i(t) {
				return t in s ? s[t] : s[t] = o.test(t)
			}

			function n() {
				return i(r.host)
			}
			var r = t("env/location"),
				o = /^[^#?]*\.(gov|mil)(:\d+)?([#?].*)?$/i,
				s = {};
			e.exports = {
				isUrlSensitive: i,
				isHostPageSensitive: n
			}
		}, {
			"env/location": 12
		}],
		65: [function (t, e) {
			function i(t) {
				return "string" == typeof t && m.test(t) && RegExp.$1.length <= 20
			}

			function n(t) {
				return i(t) ? RegExp.$1 : void 0
			}

			function r(t, e) {
				var i = f.decodeURL(t);
				return e = e || !1, i.screen_name = n(t), i.screen_name ? f.url("https://twitter.com/intent/" + (e ? "follow" : "user"), i) : void 0
			}

			function o(t) {
				return r(t, !0)
			}

			function s(t) {
				return "string" == typeof t && v.test(t)
			}

			function a(t, e) {
				return e = void 0 === e ? !0 : e, s(t) ? (e ? "#" : "") + RegExp.$1 : void 0
			}

			function l(t) {
				return "string" == typeof t && p.test(t)
			}

			function u(t) {
				return l(t) && RegExp.$1
			}

			function c(t) {
				return g.test(t)
			}

			function d(t) {
				return w.test(t)
			}

			function h(t) {
				return b.test(t)
			}
			var f = t("util/querystring"),
				m = /(?:^|(?:https?\:)?\/\/(?:www\.)?twitter\.com(?:\:\d+)?(?:\/intent\/(?:follow|user)\/?\?screen_name=|(?:\/#!)?\/))@?([\w]+)(?:\?|&|$)/i,
				p = /(?:^|(?:https?\:)?\/\/(?:www\.)?twitter\.com(?:\:\d+)?\/(?:#!\/)?[\w_]+\/status(?:es)?\/)(\d+)/i,
				g = /^http(s?):\/\/(\w+\.)*twitter\.com([\:\/]|$)/i,
				w = /^http(s?):\/\/pbs\.twimg\.com\//,
				v = /^#?([^.,<>!\s\/#\-\(\)\'\"]+)$/,
				b = /twitter\.com(\:\d{2,4})?\/intent\/(\w+)/;
			e.exports = {
				isHashTag: s,
				hashTag: a,
				isScreenName: i,
				screenName: n,
				isStatus: l,
				status: u,
				intentForProfileURL: r,
				intentForFollowURL: o,
				isTwitterURL: c,
				isTwimgURL: d,
				isIntentURL: h,
				regexen: {
					profile: m
				}
			}
		}, {
			"util/querystring": 63
		}],
		66: [function (t, e) {
			function i(t) {
				return void 0 !== t && null !== t && "" !== t
			}

			function n(t) {
				return o(t) && t % 1 === 0
			}

			function r(t) {
				return o(t) && !n(t)
			}

			function o(t) {
				return i(t) && !isNaN(t)
			}

			function s(t) {
				return i(t) && "array" == d.toType(t)
			}

			function a(t) {
				if (!i(t)) return !1;
				switch (t) {
				case "1":
				case "on":
				case "ON":
				case "true":
				case "TRUE":
				case "yes":
				case "YES":
					return !0;
				case "0":
				case "off":
				case "OFF":
				case "false":
				case "FALSE":
				case "no":
				case "NO":
					return !1;
				default:
					return !!t
				}
			}

			function l(t) {
				return o(t) ? t : void 0
			}

			function u(t) {
				return r(t) ? t : void 0
			}

			function c(t) {
				return n(t) ? t : void 0
			}
			var d = t("util/util");
			e.exports = {
				hasValue: i,
				isInt: n,
				isFloat: r,
				isNumber: o,
				isArray: s,
				asInt: c,
				asFloat: u,
				asNumber: l,
				asBoolean: a
			}
		}, {
			"util/util": 69
		}],
		67: [function (t, e) {
			function i() {
				return String(+new Date) + Math.floor(1e5 * Math.random()) + n++
			}
			var n = 0;
			e.exports = {
				generate: i
			}
		}, {}],
		68: [function (t, e) {
			function i(t, e) {
				var i, n;
				return e = e || s, /^https?:\/\//.test(t) ? t : /^\/\//.test(t) ? e.protocol + t : (i = e.host + (e.port.length ? ":" + e.port : ""), 0 !== t.indexOf("/") && (n = e.pathname.split("/"), n.pop(), n.push(t), t = "/" + n.join("/")), [e.protocol, "//", i, t].join(""))
			}

			function n() {
				for (var t, e = o.getElementsByTagName("link"), n = 0; t = e[n]; n++)
					if ("canonical" == t.rel) return i(t.href)
			}

			function r() {
				for (var t, e, i, n = o.getElementsByTagName("a"), r = o.getElementsByTagName("link"), s = [n, r], l = 0, u = 0, c = /\bme\b/; t = s[l]; l++)
					for (u = 0; e = t[u]; u++)
						if (c.test(e.rel) && (i = a.screenName(e.href))) return i
			}
			var o = t("env/document"),
				s = t("env/location"),
				a = t("util/twitter");
			e.exports = {
				absolutize: i,
				getCanonicalURL: n,
				getScreenNameFromPage: r
			}
		}, {
			"env/document": 11,
			"env/location": 12,
			"util/twitter": 65
		}],
		69: [function (t, e) {
			function i(t) {
				return c(arguments).slice(1).forEach(function (e) {
					r(e, function (e, i) {
						t[e] = i
					})
				}), t
			}

			function n(t) {
				return r(t, function (e, i) {
					a(i) && (n(i), l(i) && delete t[e]), (void 0 === i || null === i || "" === i) && delete t[e]
				}), t
			}

			function r(t, e) {
				for (var i in t)(!t.hasOwnProperty || t.hasOwnProperty(i)) && e(i, t[i]);
				return t
			}

			function o(t) {
				return {}.toString.call(t).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
			}

			function s(t, e) {
				return t == o(e)
			}

			function a(t) {
				return t === Object(t)
			}

			function l(t) {
				if (!a(t)) return !1;
				if (Object.keys) return !Object.keys(t).length;
				for (var e in t)
					if (t.hasOwnProperty(e)) return !1;
				return !0
			}

			function u(t, e) {
				h.setTimeout(function () {
					t.call(e || null)
				}, 0)
			}

			function c(t) {
				return Array.prototype.slice.call(t)
			}

			function d(t, e) {
				return t && t.indexOf ? t.indexOf(e) > -1 : !1
			}
			var h = t("env/window");
			e.exports = {
				aug: i,
				async: u,
				compact: n,
				contains: d,
				forIn: r,
				isObject: a,
				isEmptyObject: l,
				toType: o,
				isType: s,
				toRealArray: c
			}
		}, {
			"env/window": 14
		}],
		70: [function (t, e) {
			function i() {
				if (r) return r;
				if (l.isDynamicWidget()) {
					var t, e = 0,
						i = a.parent.frames.length;
					try {
						if (r = a.parent.frames[d]) return r
					} catch (n) {}
					if (u.anyIE())
						for (; i > e; e++) try {
							if (t = a.parent.frames[e], t && "function" == typeof t.openIntent) return r = t
						} catch (n) {}
				}
			}

			function n() {
				var t, e, r, s, u, c, d = {};
				if ("function" === (typeof arguments[0]).toLowerCase() ? d.success = arguments[0] : d = arguments[0], t = d.success || function () {}, e = d.timeout || function () {}, r = d.nohub || function () {}, s = d.complete || function () {}, u = void 0 !== d.attempt ? d.attempt : m, !l.isDynamicWidget() || o) return r(), s(), !1;
				c = i(), u--;
				try {
					if (c && c.trigger) return t(c), void s()
				} catch (p) {}
				return 0 >= u ? (o = !0, e(), void s()) : +new Date - h > f * m ? (o = !0, void r()) : void a.setTimeout(function () {
					n({
						success: t,
						timeout: e,
						nohub: r,
						attempt: u,
						complete: s
					})
				}, f)
			}
			var r, o, s = t("env/location"),
				a = t("env/window"),
				l = t("tfw/util/env"),
				u = t("util/env"),
				c = "twttrHubFrameSecure",
				d = "http:" == s.protocol ? "twttrHubFrame" : c,
				h = +new Date,
				f = 100,
				m = 20;
			e.exports = {
				withHub: n,
				contextualHubId: d,
				secureHubId: c
			}
		}, {
			"env/location": 12,
			"env/window": 14,
			"tfw/util/env": 39,
			"util/env": 55
		}],
		71: [function (t, e) {
			e.exports = {
				version: "2771f31464043db8d0ab30d0f06978b2c2df253d:1427140465012"
			}
		}, {}],
		72: [function (t, e) {
			e.exports = {
				css: "72799cf560bf8e00476b51e7ca075646"
			}
		}, {}],
		73: [function (t, e) {
			function i(t, e) {
				return t && t.getAttribute ? t.getAttribute("data-" + e) : void 0
			}

			function n(t, e) {
				return {
					element: t.element || p,
					action: t.action || g,
					page: r(e) ? "video" : void 0
				}
			}

			function r(t) {
				return u.closest(".embedded-video", t)
			}

			function o(t) {
				return JSON.parse(i(r(t), "player-config"))
			}

			function s(t, e) {
				var n, o, s, a = r(e);
				return a ? n = l.aug({
					item_type: f,
					card_type: m,
					id: i(a, "tweet-id"),
					card_name: i(a, "card-name"),
					publisher_id: i(a, "publisher-id"),
					content_id: i(a, "content-id")
				}, t.itemData || {}) : (o = u.closest(".cards-multimedia", e), s = u.closest(".tweet", e), n = l.aug({
					item_type: f,
					card_type: m,
					id: i(s, "tweet-id"),
					card_name: i(o, "card-name"),
					publisher_id: i(o, "publisher-id"),
					content_id: i(o, "video-content-id")
				}, t.itemData || {})), {
					items: [n]
				}
			}

			function a(t) {
				var e = this;
				this.global = t, this.server = (new c).attachReceiver(new h.Receiver(t)).bind("scribe", function (t) {
					e.scribe(t, this)
				}).bind("requestPlayerConfig", function () {
					return e.requestPlayerConfig(this)
				})
			}
			var l = t("util/util"),
				u = t("dom/get"),
				c = t("rpc/jsonrpc/server"),
				d = t("scribe/pixel"),
				h = t("rpc/postmessage"),
				f = 0,
				m = 6,
				p = "amplify_player",
				g = "undefined";
			a.prototype.findIframeByWindow = function (t) {
				for (var e = this.global.document.getElementsByTagName("iframe"), i = e.length, n = 0; i > n; n++)
					if (e[n].contentWindow == t) return e[n]
			}, a.prototype.requestPlayerConfig = function (t) {
				var e = this.findIframeByWindow(t);
				if (e) return o(e)
			}, a.prototype.scribe = function (t, e) {
				var i, r, o, a;
				i = t && t.customScribe, r = this.findIframeByWindow(e), i && r && (o = n(i, r), a = s(i, r), d.clientEvent2(o, a, !0))
			}, e.exports = a
		}, {
			"dom/get": 7,
			"rpc/jsonrpc/server": 25,
			"rpc/postmessage": 26,
			"scribe/pixel": 32,
			"util/util": 69
		}],
		74: [function (t) {
			! function () {
				var e = t("env/document"),
					i = t("tfw/util/article"),
					n = t("util/domready"),
					r = t("util/logger"),
					o = t("performance/perf-timers"),
					s = t("tfw/widget/base"),
					a = t("tfw/widget/follow"),
					l = t("tfw/widget/tweetbutton"),
					u = t("tfw/widget/embed"),
					c = t("tfw/widget/timeline"),
					d = t("tfw/widget/video"),
					h = t("tfw/widget/intent"),
					f = t("tfw/factories"),
					m = t("util/events"),
					p = t("tfw/hub/client"),
					g = t("intents/delegate"),
					w = t("globals/twttr"),
					v = t("globals/private"),
					b = t("events/ready"),
					y = t("util/promise");
				if (v.init("host", "platform.twitter.com"), o.start("widgets-js-load"), i.requestArticleUrl(), v.get("widgets.loaded")) return w.call("widgets.load"), !1;
				if (v.get("widgets.init")) return !1;
				v.set("widgets.init", !0), w.set("init", !0);
				var _, T = new y(function (t) {
					_ = t.fulfill.bind(t)
				});
				b.exposeReadyPromise(T, w.base, "_e"), w.set("events", {
					bind: function (t, e) {
						T.then(function (i) {
							i.events.bind(t, e)
						})
					}
				}), n(function () {
					function t() {
						v.set("eventsHub", p.init()), p.init(!0)
					}
					var i, n = {
							"a.twitter-share-button": l,
							"a.twitter-mention-button": l,
							"a.twitter-hashtag-button": l,
							"a.twitter-follow-button": a,
							"blockquote.twitter-tweet": u,
							"a.twitter-timeline": c,
							"div.twitter-timeline": c,
							"blockquote.twitter-video": d,
							body: h
						},
						o = v.get("eventsHub") ? w.get("events") : {};
					w.aug("widgets", f, {
						load: function (t) {
							r.time("load"), s.init(n), s.embed(t), v.set("widgets.loaded", !0)
						}
					}), w.aug("events", o, m.Emitter), i = w.get("events.bind"), w.set("events.bind", function (e, n) {
						t(), this.bind = i, this.bind(e, n)
					}), _(w.base), g.attachTo(e), w.call("widgets.load")
				})
			}()
		}, {
			"env/document": 11,
			"events/ready": 15,
			"globals/private": 18,
			"globals/twttr": 19,
			"intents/delegate": 21,
			"performance/perf-timers": 23,
			"tfw/factories": 34,
			"tfw/hub/client": 35,
			"tfw/util/article": 36,
			"tfw/widget/base": 42,
			"tfw/widget/embed": 43,
			"tfw/widget/follow": 44,
			"tfw/widget/intent": 45,
			"tfw/widget/timeline": 47,
			"tfw/widget/tweetbutton": 48,
			"tfw/widget/video": 49,
			"util/domready": 53,
			"util/events": 56,
			"util/logger": 59,
			"util/promise": 62
		}],
		75: [function (t, e) {
			function i() {}
			var n = t("util/util"),
				r = t("util/events");
			n.aug(i.prototype, r.Emitter, {
				transportMethod: "",
				init: function () {},
				send: function (t) {
					var e;
					this._ready ? this._performSend(t) : e = this.bind("ready", function () {
						this.unbind("ready", e), this._performSend(t)
					})
				},
				ready: function () {
					this.trigger("ready", this), this._ready = !0
				},
				isReady: function () {
					return !!this._ready
				},
				receive: function (t) {
					this.trigger("message", t)
				}
			}), e.exports = {
				Connection: i
			}
		}, {
			"util/events": 56,
			"util/util": 69
		}],
		76: [function (t, e) {
			function i(t, e) {
				var i = e || Math.floor(100 * Math.random()),
					r = ['<object id="xdflashshim' + i + '" name="xdflashshim' + i + '"', 'type="application/x-shockwave-flash" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"', 'width="1" height="1" style="position:absolute;left:-9999px;top:-9999px;">', '<param name="movie" value="' + t + "&debug=" + n.__XDDEBUG__ + '">', '<param name="wmode" value="window">', '<param name="allowscriptaccess" value="always">', "</object>"].join(" ");
				return r
			}
			var n = t("env/window");
			e.exports = {
				object: i
			}
		}, {
			"env/window": 14
		}],
		77: [function (t, e) {
			function i(t) {
				return (JSON.parse || JSON.decode)(t)
			}

			function n(t) {
				this.con = t
			}

			function r() {
				this.id = r.id++
			}
			var o = t("util/util"),
				s = t("util/events");
			o.aug(n.prototype, {
				expose: function (t) {
					this.con.bind("message", this._handleRequest(t))
				},
				call: function (t) {
					var e, n = this;
					return this._requests || (this._requests = {}, this.con.bind("message", function (t) {
						var e;
						try {
							t = i(t)
						} catch (r) {
							return
						}
						t.callback && "number" == typeof t.id && (e = n._requests[t.id]) && (t.error ? e.trigger("error", t) : e.trigger("success", t), delete n._requests[t.id])
					})), e = new r, this._requests[e.id] = e, e.send(this.con, t, Array.prototype.slice.call(arguments, 1))
				},
				_handleRequest: function (t) {
					var e = this;
					return function (n) {
						var r, o;
						try {
							n = i(n)
						} catch (s) {
							return
						}
						n.callback || "number" == typeof n.id && "function" == typeof t[n.method] && (o = e._responseCallbacks(n.id), r = t[n.method].apply(t, n.params.concat(o)), "undefined" != typeof r && o[0](r))
					}
				},
				_responseCallbacks: function (t) {
					var e = this.con;
					return [function (i) {
						e.send(JSON.stringify({
							id: t,
							result: i,
							callback: !0
						}))
					}, function i(n) {
						e.send(JSON.stringify({
							id: t,
							error: i,
							callback: n
						}))
					}]
				}
			}), r.id = 0, o.aug(r.prototype, s.Emitter, {
				send: function (t, e, i) {
					return t.send(JSON.stringify({
						id: this.id,
						method: e,
						params: i
					})), this
				},
				success: function (t) {
					return this.bind("success", t), this
				},
				error: function (t) {
					return this.bind("error", t), this
				}
			}), e.exports = function (t) {
				return new n(t)
			}
		}, {
			"util/events": 56,
			"util/util": 69
		}],
		78: [function (t, e) {
			function i() {}

			function n(t) {
				this.transportMethod = "PostMessage", this.options = t, this._createChild()
			}

			function r(t) {
				this.transportMethod = "Flash", this.options = t, this.token = Math.random().toString(16).substring(2), this._setup()
			}

			function o(t) {
				this.transportMethod = "Fallback", this.options = t, this._createChild()
			}
			var s, a = t("env/document"),
				l = t("env/window"),
				u = t("xd/base"),
				c = t("util/util"),
				d = t("util/env"),
				h = t("intents/intent"),
				f = "__ready__",
				m = 0;
			i.prototype = new u.Connection, c.aug(i.prototype, {
				_createChild: function () {
					this.options.window ? this._createWindow() : this._createIframe()
				},
				_createIframe: function () {
					function t() {
						o.child = e.contentWindow, o._ready || o.init()
					}
					var e, i, n, r, o = this,
						u = {
							allowTransparency: !0,
							frameBorder: "0",
							scrolling: "no",
							tabIndex: "0",
							name: this._name()
						},
						d = c.aug(c.aug({}, u), this.options.iframe);
					l.postMessage ? (s || (s = a.createElement("iframe")), e = s.cloneNode(!1)) : e = a.createElement('<iframe name="' + d.name + '">'), e.id = d.name, c.forIn(d, function (t, i) {
						"style" != t && e.setAttribute(t, i)
					}), r = e.getAttribute("style"), r && "undefined" != typeof r.cssText ? r.cssText = d.style : e.style.cssText = d.style, e.addEventListener("load", t, !1), e.src = this._source(), (i = this.options.appendTo) ? i.appendChild(e) : (n = this.options.replace) ? (i = n.parentNode, i && i.replaceChild(e, n)) : a.body.insertBefore(e, a.body.firstChild)
				},
				_createWindow: function () {
					var t = h.open(this._source()).popup;
					t && t.focus(), this.child = t, this.init()
				},
				_source: function () {
					return this.options.src
				},
				_name: function () {
					var t = "_xd_" + m++;
					return l.parent && l.parent != l && l.name && (t = l.name + t), t
				}
			}), n.prototype = new i, c.aug(n.prototype, {
				init: function () {
					function t(t) {
						t.source === e.child && (e._ready || t.data !== f ? e.receive(t.data) : e.ready())
					}
					var e = this;
					l.addEventListener("message", t, !1)
				},
				_performSend: function (t) {
					this.child.postMessage(t, this.options.src)
				}
			}), r.prototype = new i, c.aug(r.prototype, {
				_setup: function () {
					var e = this,
						i = t("xd/flash");
					l["__xdcb" + e.token] = {
						receive: function (t) {
							e._ready || t !== f ? e.receive(t) : e.ready()
						},
						loaded: function () {}
					};
					var n = a.createElement("div");
					n.innerHTML = i.object("https://platform.twitter.com/xd/ft.swf?&token=" + e.token + "&parent=true&callback=__xdcb" + e.token + "&xdomain=" + e._host(), e.token), a.body.insertBefore(n, a.body.firstChild), e.proxy = n.firstChild, e._createChild()
				},
				init: function () {},
				_performSend: function (t) {
					this.proxy.send(t)
				},
				_host: function () {
					return this.options.src.replace(/https?:\/\//, "").split(/(:|\/)/)[0]
				},
				_source: function () {
					return this.options.src + (this.options.src.match(/\?/) ? "&" : "?") + "xd_token=" + l.escape(this.token)
				}
			}), o.prototype = new i, c.aug(o.prototype, {
				init: function () {},
				_performSend: function () {}
			}), e.exports = {
				connect: function (t) {
					return !d.canPostMessage() || d.anyIE() && t.window ? d.anyIE() && d.flashEnabled() ? new r(t) : new o(t) : new n(t)
				}
			}
		}, {
			"env/document": 11,
			"env/window": 14,
			"intents/intent": 22,
			"util/env": 55,
			"util/util": 69,
			"xd/base": 75,
			"xd/flash": 76
		}]
}, {}, [74]))
}();