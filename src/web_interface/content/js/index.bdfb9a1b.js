(function(t){function e(e){for(var n,i,c=e[0],l=e[1],o=e[2],f=0,m=[];f<c.length;f++)i=c[f],Object.prototype.hasOwnProperty.call(r,i)&&r[i]&&m.push(r[i][0]),r[i]=0;for(n in l)Object.prototype.hasOwnProperty.call(l,n)&&(t[n]=l[n]);u&&u(e);while(m.length)m.shift()();return s.push.apply(s,o||[]),a()}function a(){for(var t,e=0;e<s.length;e++){for(var a=s[e],n=!0,c=1;c<a.length;c++){var l=a[c];0!==r[l]&&(n=!1)}n&&(s.splice(e--,1),t=i(i.s=a[0]))}return t}var n={},r={index:0},s=[];function i(e){if(n[e])return n[e].exports;var a=n[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,i),a.l=!0,a.exports}i.m=t,i.c=n,i.d=function(t,e,a){i.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},i.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},i.t=function(t,e){if(1&e&&(t=i(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(i.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)i.d(a,n,function(e){return t[e]}.bind(null,n));return a},i.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return i.d(e,"a",e),e},i.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},i.p="/";var c=window["webpackJsonp"]=window["webpackJsonp"]||[],l=c.push.bind(c);c.push=e,c=c.slice();for(var o=0;o<c.length;o++)e(c[o]);var u=l;s.push([0,"chunk-vendors"]),a()})({0:function(t,e,a){t.exports=a("56d7")},"56d7":function(t,e,a){"use strict";a.r(e);a("e260"),a("e6cf"),a("cca6"),a("a79d");var n=a("2b0e"),r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"container-fluid"},[a("div",{staticClass:"row"},[a("div",{staticClass:"container-fluid"},[a("h1",{staticClass:"text-center h1"},[t._v(t._s(t.title))]),a("h2",{staticClass:"text-center h4"},[t._v(t._s(t.subtitle))]),a("NavigationBar")],1)]),a("div",{staticClass:"row"},[a("div",{staticClass:"container-fluid"},[a("TeamOnlineDisplay")],1)]),t._m(0)])},s=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"row"},[a("span",{staticClass:"text-primary text-center"},[t._v("*A Discord version of this bot is available on "),a("a",{attrs:{href:"https://discord.gg/6bGNeRYUsc"}},[t._v("LJLOfficiallyUnofficial")])])])}],i=(a("d3b7"),function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"container-fluid d-flex justify-content-center"},[a("ul",{staticClass:"nav navigation-bar"},t._l(t.teams,(function(e){return a("li",{key:e,staticClass:"nav-item"},[a("a",{staticClass:"nav-link",attrs:{href:"#"},on:{click:t.setActiveTeam}},[t._v(t._s(e))])])})),0)])}),c=[],l={methods:{setActiveTeam:function(t){var e=this;t.preventDefault(),this.$store.commit("setActiveTeam",t.target.text),fetch("api/team/"+this.$store.getters.getActiveTeam).then((function(t){return t.json()})).then((function(t){e.$store.commit("setActiveTeamPlayers",t.players)}))}},created:function(){var t=this;fetch("api/teams").then((function(t){return t.json()})).then((function(e){t.$store.commit("setTeams",e.teams),t.$store.commit("setActiveTeam",e.teams[0]),fetch("api/team/"+t.$store.getters.getActiveTeam).then((function(t){return t.json()})).then((function(e){t.$store.commit("setActiveTeamPlayers",e.players)}))}))},computed:{teams:function(){return this.$store.getters.getTeams}}},o=l,u=a("2877"),f=Object(u["a"])(o,i,c,!1,null,null,null),m=f.exports,v=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"container-fluid"},["All"!=t.activeTeamName?a("h3",{staticClass:"text-left"},[a("a",{attrs:{href:"https://lol.fandom.com/wiki/"+t.activeTeamName}},[t._v(t._s(t.activeTeamName))])]):a("h3",{staticClass:"text-left"},[t._v("All Teams")]),a("table",{staticClass:"table table-striped table-bordered table-hover"},[t._m(0),a("tbody",t._l(t.players,(function(e){return a("tr",{key:e.Pos},[a("td",[t._v(t._s(e.Name))]),a("td",[a("a",{attrs:{href:"https://twitter.com/"+e.Twitter}},[t._v(t._s(e.Twitter))])]),"Twitch"==e.Platform?a("td",[a("a",{attrs:{href:"https://twitch.tv/"+e.StreamName}},[t._v(t._s(e.StreamName))])]):"OPENREC.tv"==e.Platform?a("td",[a("a",{attrs:{href:"https://openrec.tv/user/"+e.StreamName}},[t._v(t._s(e.StreamName))])]):a("td",[t._v(t._s(e.StreamName))]),a("td",[t._v(t._s(e.Platform))]),1==e.Status?a("td",[a("b-icon-check-circle-fill"),a("b",{staticClass:"text-success",staticStyle:{"padding-left":"10px"}},[t._v(" Online ")])],1):0==e.Status?a("td",[a("b-icon-x-circle-fill"),a("b",{staticClass:"text-danger",staticStyle:{"padding-left":"10px"}},[t._v(" Offline ")])],1):a("td",[a("b-icon-question-circle-fill"),a("b",{staticClass:"text-warning",staticStyle:{"padding-left":"10px"}},[t._v(" UNKNOWN :( ")])],1)])})),0)])])},d=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("thead",[a("tr",[a("th",[t._v("Player")]),a("th",[t._v("Twitter")]),a("th",[t._v("Stream")]),a("th",[t._v("Platform")]),a("th",[t._v("Status")])])])}],p={computed:{activeTeamName:function(){return this.$store.getters.getActiveTeam},players:function(){return this.$store.getters.getActiveTeamPlayers}}},h=p,_=Object(u["a"])(h,v,d,!1,null,null,null),b=_.exports,y={name:"App",data:function(){return{title:"LJL Stream Tracker",subtitle:"Updated every 5 minutes (or so)",footer:"I am the bottom (text)"}},components:{NavigationBar:m,TeamOnlineDisplay:b},created:function(){var t=this;fetch("/api/last_update").then((function(t){return t.json()})).then((function(e){t.subtitle="Updated every 5 minutes (or so). Last updated: "+e.time}))}},T=y,g=Object(u["a"])(T,r,s,!1,null,null,null),x=g.exports,w=a("5f5b"),P=a("b1e0"),C=(a("50c9"),a("2dd8"),a("2f62"));n["default"].use(w["a"]),n["default"].use(P["a"]),n["default"].use(C["a"]),n["default"].config.productionTip=!1;var O=new C["a"].Store({state:{teams:[],activeTeam:null,activeTeamPlayers:[]},mutations:{setActiveTeam:function(t,e){t.activeTeam=e},setTeams:function(t,e){t.teams=e},setActiveTeamPlayers:function(t,e){t.activeTeamPlayers=e}},getters:{getActiveTeam:function(t){return t.activeTeam},getTeams:function(t){return t.teams},getActiveTeamPlayers:function(t){return t.activeTeamPlayers}}});new n["default"]({render:function(t){return t(x)},store:O}).$mount("#app")}});
//# sourceMappingURL=index.bdfb9a1b.js.map