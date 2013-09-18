(function(W){
	if (!(W.Y && typeof W.Y === 'object'))
	{
		W.Y = {};
	}
	var Y = W.Y;
	Y.VERSION = 1.1;
	//Y.loginarray = {};
	//Y.loginarray.current = {"domain":"http://192.168.0.83:85","path":"/systemdata","hdir":"/2011/01/28/7c127e0c66f06e58c7c7310a7c6fa488","udir":"/users/blackhole","hostname":"zhanguo","member":"10032","number":"10172","username":"blackhole","hosts":"10036","degree":"administrators","locks":"f","systemuser":"t","activation":"t","usersystemdir":"http://192.168.0.83:85/systemdata/2011/01/28/7c127e0c66f06e58c7c7310a7c6fa488/users/blackhole"};
	//Y.loginarray.member = {"id":"33","number":"10032","email":"zhanguoxingzhe@gmail.com","password":"71cd8f985ebc954d4c9f4701c2d110ac","ip":"192.168.0.83","locks":"f","addtime":"2011-01-28 22:27:45.625+08","name":"%u6218%u56FD%u884C%u8005","nickname":"媛石神话","sex":"f","headimg":"http://app.qlogo.cn/mbloghead/28578724a0852b39f890/120","hostname":"zhanguo"};
	//搜寻类 逐级上搜 pa=true 获得父级
	var getobj = Y.getobj = function(object,pa)
	{
		if(!object)return false;
		var objects = object.split(".");
		var parents = "",i=0,Parent = "";
		var O,X,EVAL;
		while(i<4)
		{
			i++;
			O = "";
			if(parents) 
			{
				Parent += parents;
				if(Parent) Parent += "&&";
				parents += ".";
			}
			EVAL = "";
			for(var j=0; j<objects.length; j++)
			{
				if(O) O += ".";
				O += objects[j];
				if(EVAL) EVAL += "&&";
				EVAL += 'typeof(' + parents + O + ')!="undefined"';
			}
			try
			{
				if(eval(Parent + EVAL))
				{
					if(pa)
					{
						var Pa = parents + O;
						return  eval(Pa.slice(0,Pa.lastIndexOf(".")));
					}
					else
					{
						return  eval(parents + O);
					}
				}
			}
			catch(e){}
			parents += "parent";
		}
		try
		{
			if(opener&&typeof(opener.Y)!="undefined"&&typeof(opener.Y.getobj)!="undefined") 
			{
				return opener.Y.getobj(object);
			}
			else
			{
				return false;
			}
		}
		catch(e){
			return false;
		}
	};
	
	Y.storage = {
		set : function(name,value)
		{
			var current = Y.getobj("Y.loginarray.current");
			var names = current["dname"] + "_" + current["hname"] + "_" + name;
			//var hasSessionStorage = window.sessionStorage;
			var LocalStorage = window.localStorage;
			if(!LocalStorage)return false;
			if(typeof(value)=="object")
			{
				var json = Y.JSON.encode(value);
			}
			else
			{
				var json = value;
			}
			LocalStorage.setItem(names,json);
			return json;
		},
		get : function(name)
		{
			var current = Y.getobj("Y.loginarray.current");
			var names = current["dname"] + "_" + current["hname"] + "_" + name;
			//var hasSessionStorage = window.sessionStorage;
			var LocalStorage = window.localStorage;
			if(!LocalStorage)return false;
			var value = LocalStorage.getItem(names);
			return value;
		},
		getjson : function(name,json)
		{
			var current = Y.getobj("Y.loginarray.current");
			var names = current["dname"] + "_" + current["hname"] + "_" + name;
			//var hasSessionStorage = window.sessionStorage;
			var LocalStorage = window.localStorage;
			if(!LocalStorage)return false;
			var value = LocalStorage.getItem(names);
			try
			{
				var jsons = eval("(" + value + ")");
				if(typeof(json)=="object")
				{
					jsons = $.extend(json, jsons);
					return jsons;
				}
				else
				{
					return jsons;
				}
			}
			catch(e){
				if(typeof(json)=="object")
				{
					return json;
				}
				else
				{
					return value;
				}
			}
		},
		del : function(name)
		{
			var current = Y.getobj("Y.loginarray.current");
			var names = current["dname"] + "_" + current["hname"] + "_" + name;
			localStorage.removeItem(names);
		},
		remove : function(name)
		{
			var current = Y.getobj("Y.loginarray.current");
			var names = current["dname"] + "_" + current["hname"] + "_" + name;
			localStorage.removeItem(names);
		}
	};

	function extendFunction(callbackFunction,extend)
	{
		var extendStr = "this is extend string!";
		var args = [];
		if(typeof(extend) == "object")
		{
			for (var property in extend)
			{
				callbackFunction[property] = extend[property];
				args.push(extend[property]);
			}
		}
		callbackFunction["extendStr"] = extendStr;
		args.push(extendStr);   
		return callbackFunction.apply(this,args);
	};

	var getfun = Y.getfun = function(fun,pa,boo)
	{
		if(!fun)return false;
		var funs = fun.split(".");
		var parents = "",i=0,Parent = "";
		var O,X,EVAL;
		while(i<4)
		{
			i++;
			O = "";
			if(parents) 
			{
				Parent += parents;
				if(Parent) Parent += "&&";
				parents += ".";
			}
			EVAL = "";
			for(var j=0; j<funs.length; j++)
			{
				if(O) O += ".";
				O += funs[j];
				if(EVAL) EVAL += "&&";
				EVAL += 'typeof(' + parents + O + ')!="undefined"';
			}
			try
			{
				if(eval(Parent + EVAL))
				{
					var Fun = eval(parents + O);
					if(typeof(Fun)=="function")
					{
						if(boo)
						{
							var returns = extendFunction(Fun,pa);
							if(returns!=null&&returns!=undefined)
							{
								return returns;
							}
						}
						else
						{
							return extendFunction(Fun,pa);
						}
					}
				}
			}
			catch(e){}
			parents += "parent";
		}
		if(opener&&typeof(opener.Y.getfun)!="undefined") 
		{
			return opener.Y.getfun(fun,pa,boo);
		}
		else
		{
			return false;
		}
	};
	
	var PoMe = Y.PoMe = {
		pool : {},
		passw : "FDA$#@$#@FDA321764",
		commamd : {
			open : function(json){
				if(json["data"])
				{
					Y.openapp.bu_onclick_idcode(json["data"],{pmid:json["id"],pas:["domin"]});
				}
			},
			send : function(json){
				if(json["pmid"])
				{
					if(Y.PoMe.pool[json["pmid"]])
					{
						var pools = Y.PoMe.pool[json["pmid"]];
						var data = {"command":"return","data":json["data"]};
						var datas = Y.PoMe.encode(Y.JSON.encode(data));
						pools["source"] && pools["source"].postMessage(
							datas,
							pools["origin"]
						);
					}
				}
			},
			"return" : function(json){}
		},
		send : function(data,domin,win)
		{
			switch(win)
			{
				case "parent":
					var win = window.parent;
					win.postMessage(
						data,
						(domin.slice(0,7)=="http://")?domin:"http://" + domin
					);
					break;
				case "top":
					var win = window.top;
					win.postMessage(
						data,
						(domin.slice(0,7)=="http://")?domin:"http://" + domin
					);
					break;
			}
		},
		decode : function(data)
		{
			return Y.Code.decode(Y.PoMe.passw,data) || data;
		},
		encode : function(data)
		{
			return Y.Code.encode(Y.PoMe.passw,data);
		}
	};
	$(function(){
		window.onmessage = function(e){
			try
			{
				var data = Y.Code.decode(Y.PoMe.passw,e.data) || e.data;
				var array = eval("(" + data + ")");
				if(array)
				{
					if(array["pmid"])
					{
						Y.PoMe.commamd[array["command"]] && Y.PoMe.commamd[array["command"]](array);
					}
					else
					{
						var id = "pm" + Y.GetTimeName("ms");
						Y.PoMe.pool[id] = {};
						Y.PoMe.pool[id]["id"] = id;
						Y.PoMe.pool[id]["source"] = e.source;
						Y.PoMe.pool[id]["origin"] = e.origin;
						Y.PoMe.pool[id]["data"] = array["data"] || "";
						Y.PoMe.pool[id]["command"] = array["command"] || "";
						Y.PoMe.commamd[Y.PoMe.pool[id]["command"]] && Y.PoMe.commamd[Y.PoMe.pool[id]["command"]](Y.PoMe.pool[id]);
					}
				}
				else
				{
					var id = "pm" + Y.GetTimeName("ms");
					Y.PoMe.pool[id] = {};
					Y.PoMe.pool[id]["id"] = id;
					Y.PoMe.pool[id]["source"] = e.source;
					Y.PoMe.pool[id]["origin"] = e.origin;
					Y.PoMe.pool[id]["data"] = data || "";
					Y.PoMe.pool[id]["command"] = data || "";
					Y.PoMe.commamd[Y.PoMe.pool[id]["command"]] && Y.PoMe.commamd[Y.PoMe.pool[id]["command"]](Y.PoMe.pool[id]);
				}
			}
			catch(e){
				var id = "pm" + Y.GetTimeName("ms");
				Y.PoMe.pool[id] = {};
				Y.PoMe.pool[id]["id"] = id;
				Y.PoMe.pool[id]["source"] = e.source;
				Y.PoMe.pool[id]["origin"] = e.origin;
				Y.PoMe.pool[id]["data"] = data || "";
				Y.PoMe.pool[id]["command"] = data || "";
				Y.PoMe.commamd[Y.PoMe.pool[id]["command"]] && Y.PoMe.commamd[Y.PoMe.pool[id]["command"]](Y.PoMe.pool[id]);
			}
		};
	});
	
	var Getapi = Y.Getapi = function()
	{
		return "/YuanClass/yuanio.php";
	};
	
	var RunUI = Y.RunUI = function(name,fun)
	{
		switch (name){
			case 'YuanButton':
				if($.YuanButton)
				{
					if(typeof(fun) == "function")
					{
						fun();
					}
				}
				else
				{
					Y.IncCssFiles('/css/yuanui.css');
					Y.IncJsFiles("/Library_js_2010/ui/yuan.button.js",[fun]);
				}
			break;
			case 'YuanRadio':
				if($.YuanRadio)
				{
					if(typeof(fun) == "function")
					{
						fun();
					}
				}
				else
				{
					Y.IncJsFiles("/Library_js_2010/ui/yuan.radios.js",[fun]);
				}
			break;
			case 'YuanCheckbox':
				if($.YuanCheckbox)
				{
					if(typeof(fun) == "function")
					{
						fun();
					}
				}
				else
				{
					Y.IncJsFiles("/Library_js_2010/ui/yuan.checkbox.js",[fun]);
				}
			break;
			case 'Sliders':
				if($.Sliders)
				{
					if(typeof(fun) == "function")
					{
						fun();
					}
				}
				else
				{
					Y.IncJsFiles("/Library_js_2010/ui/yuan.sliders.js",[fun]);
				}
			break;
		}
		
	};

	var RunUIs = Y.RunUIs = function(name,fun)
	{
		switch (name){
			case 'YuanButton':
				if($.YuanButton)
				{
					if(typeof(fun) == "function")
					{
						fun();
					}
				}
				else
				{
					Y.IncCssFiles('/css/yuanui.css');
					Y.IncJsFiles("/Library_js_2010/ui/yuan.button.js",[fun]);
				}
			break;
			case 'YuanRadio':
				if($.YuanRadio)
				{
					if(typeof(fun) == "function")
					{
						fun();
					}
				}
				else
				{
					Y.IncJsFiles("/Library_js_2010/ui/yuan.radios.js",[fun]);
				}
			break;
			case 'YuanCheckbox':
				if($.YuanCheckbox)
				{
					if(typeof(fun) == "function")
					{
						fun();
					}
				}
				else
				{
					Y.IncJsFiles("/Library_js_2010/ui/yuan.checkboxs.js",[fun]);
				}
			break;
			case 'Sliders':
				if($.Sliders)
				{
					if(typeof(fun) == "function")
					{
						fun();
					}
				}
				else
				{
					Y.IncJsFiles("/Library_js_2010/ui/yuan.sliders.js",[fun]);
				}
			break;
		}
		
	};

	/**************************
	**********打开应用*********
	**************************/
	Y.zIndex = 500;
	
	var openapp = Y.openapp = {
		zIndex : 100,
		button_activity : [],
		openclock : {},
		openfile : function(array,boo)
		{
			if(!array) return false;
			var type1 = array["type"];
			var type2 = array["name"].split(".");
			var type3 = "";
			

			if(type2.length>2) type3 = type2[type2.length - 2];
			if(type1=="link")
			{
				var API = Getapi();
				var url = array["path"] + "/" + array["name"];
				var code = '{"url":"' + url + '","readfile":true,"class":"Blackhole","fun":"get_json"}';
				$.post(API,{code:base6.encode(code)},function(data){
							try
							{
								var array = eval("(" + data + ")");
								if(array["url"]&&array["type"])
								{
									var program = Y.openapp.program_files(array["type"],"");
									
									if(program)
									{
										if(program=="mp3play"||program[0]=="mp3play")
										{
											if(typeof(Mp3play.mp3play)!="undefined")
											{
												Mp3play.mp3play(array["url"]);
											}
											else
											{
												if(!boo)
												{
													Y.UI.alert("不能播放音乐！");
													return false;
												}
												else
												{
													return false;
												}
											}
										}
										else if(program=="img"||program[0]=="img")
										{
											var parameter = {img:array["url"],url:array["url"]};
											Y.openapp.bu_onclick_idcode(program[0],parameter);
											return true;
										}
										else
										{
											Y.openapp.bu_onclick_idcode(program[0],array);
											return true;
										}
									}
									else
									{
										if(!boo)
										{
											Y.UI.alert("无法打开的文件,请指定应用程序！");
											return false;
										}
										else
										{
											return false;
										}
									}
								}
							}
							catch(e){
								if(!boo)
								{
									Y.UI.alert("无法打开的文件,请指定应用程序！");
									return false;
								}
								else
								{
									return false;
								}
							}
						});
			}
			else
			{
				var program = Y.openapp.program_files(type1,type3);
				if(program)
				{
					if(program=="mp3play")
					{
						if(typeof(Mp3play)!="undefined"&&typeof(Mp3play.mp3play)!="undefined")
						{
							Mp3play.mp3play(array["path"] + "/" + array["name"]);
							return true;
						}
						else
						{
							if(!boo)
							{
								Y.UI.alert("不能播放音乐！");
								return false;
							}
							else
							{
								return false;
							}
						}
					}
					else
					{
						var parameter = {};
						for(var i=0; i<program[1].length; i++)
						{
							switch(program[1][i].toLowerCase())
							{
								case "url":
									if(program[0]=="img")
									{
										parameter["img"] = array["path"] + "/" + array["name"];
									}
									else
									{
										parameter["url"] = array["path"] + "/" + array["name"];
									}
									break;
								case "popedom":
									parameter["popedom"] = array["popedom"];
									break;
							}
						}
						if(program[2])
						{
							Y.openapp.bu_onclick_idcode(program[0],parameter,program[2]);
							return true;
						}
						else
						{
							Y.openapp.bu_onclick_idcode(program[0],parameter);
							return true;
						}
					}
				}
				else
				{
					if(!boo)
					{
						Y.UI.alert("无法打开的文件,请指定应用程序！");
						return false;
					}
					else
					{
						return false;
					}
				}
			}
		},

		change_size : function (id,W,H)
		{
			if(!id||!W||!H) return false;
			if(W<200) W = 200;
			if(H<200) H = 200;
			var course = $("#" + id);
			if(!course) return false;
			var ID = id.replace(/window/gi,"").split("_");
			
			var L = Math.ceil((Y.openapp.button_activity[ID[0]][ID[1]]['width'] - W)/2);
			//var T = Math.ceil((os_object.button_activity[ID[0]][ID[1]]['height'] - H)/2);
			var T = ((document.body.clientHeight - H - Y.foot_height)/4);
			//alert(T);
			T = Math.ceil(T);
			//alert(W + " " + H + " " + L + " " + T);
			Y.openapp.button_activity[ID[0]][ID[1]]['width'] = W;
			Y.openapp.button_activity[ID[0]][ID[1]]['height'] = H;

			course.css({
				width : W + "px",
				height : H + "px",
				top : (T) + "px",
				left : (L + course.css("left").delpx()*1) + "px"
			});
			course.find(".iframes").css({
				width : W + "px",
				height : (H - 30) + "px"
			});
		},

		program_files : function(type1,type2)
		{
				switch(type2.toLowerCase())
				{
					case "video":
						return ["webvideo",["url"]];
					case "xiami":
						return ["xiami",["url"]];
						break;
					case "url":
						return ["openurl",["url"]];
						break;
					case "rss":
						return ["openrss",["url"]];
						break;
					case "design":
						return ["design",["url"]];
						break;
					case "designs":
						return ["design",["url"]];
						break;
					case "pdf":
						return ["kankan",["url"]];
						break;
				}
				
				switch(type1.toLowerCase())
				{
					case "jpg":
					case "jpeg":
					case "gif":
					case "png":
					case "bmp":
						return ["img",["url"]];
						break;
					case "doc":
					case "docx":
					case "sxw":
					case "odt":
					case "rtf":
						return ["xiexie",["url","number"]];
						break;
					case "ppt":
					case "pptx":
					case "pps":
						return ["xiuxiu",["url","number"]];
						break;
					case "csv":
					case "sxc":
					case "xls":
					case "xlsx":
						return ["gege",["url","number"]];
						break;
					case "pdf":
						return ["kankan",["url"]];
						break;
					case "html":
					case "htm":
					case "asp":
					case "php":
					case "txt":
					case "js":
					case "css":
					case "asa":
						return ["editarea",["url","popedom"]];
					case "swf":
						return ["flashplay",["url"],["id"]];
						break;
					case "mp3":
						return "mp3play";
						break;
				}
		},
		
		default : {
			editarea:{number:"editarea",icon:"",title:"editarea",url:"/applications/editarea/exemples/index.html",width:1100,height:600,top:0,left:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:true,task:"much"},
			xiami:{number:"xiami",icon:"/BlackHole/icon/apple/admin.png",title:"虾米音乐",url:"/applications/xiami/yuanos.html",width:257,height:63,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:true,task:"much"},
			openurl:{number:"openurl",icon:"",title:"简易浏览器",url:"/applications/urlfile/yuanos.html",width:1100,height:600,top:0,left:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:false,task:"much"},
			openrss:{number:"openrss",icon:"",title:"rss阅读器",url:"/applications/rssfile/yuanos.html",width:1100,height:600,top:0,left:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:false,task:"much"},
			design:{number:"design","icon":"","title":"画册在线定制软件","iframes":true,"url":"/applications/diy/diys.html","width":1200,"height":700,"top":0,"left":0,"right":0,"max":false,"tension":true,"movlock":false,"autosize":true,"movdisplay":false,"task":"much"},
			share:{number:"share",icon:"",privacy:false,iframes:true,title:"分享",url:"/applications/design/share.html",width:600,height:560,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:true,movdisplay:1,task:"much"},
			sandtimg:{number:"sandtimg",icon:"",privacy:false,iframes:true,title:"发送新浪微博",url:"/applications/design/sandtimg.html",width:600,height:700,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:true,movdisplay:1,task:"much",mask:2},
			sandtq:{number:"sandtq",icon:"",privacy:false,iframes:true,title:"发送腾讯微博",url:"/applications/design/sandtq.html",width:600,height:700,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:true,movdisplay:1,task:"much"},
			sandt:{number:"sandt",icon:"",privacy:false,iframes:true,title:"发送新浪微博",url:"/applications/design/sandt.html",width:600,height:700,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:true,movdisplay:1,task:"much"},
			tsinarepost:{number:"tsinarepost",icon:"",privacy:false,iframes:true,title:"微博转发",url:"/applications/design/tsinarepost.html",width:600,height:700,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:true,movdisplay:1,task:"much"},
			tsinacomments:{number:"tsinacomments",icon:"",privacy:false,iframes:true,title:"微博评论",url:"/applications/design/tsinacomments.html",width:600,height:700,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:true,movdisplay:1,task:"much"},
			browser:{number:"browser",icon:"/BlackHole/images/foot/browser.png",privacy:false,iframes:true,title:"web浏览器",url:"/applications/browser/yuanos.html",width:1100,height:600,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			xiexie:{number:"xiexie",icon:"/icon/64/605.png",privacy:false,iframes:true,title:"百会写写",url:"/applications/zoho/writer.html",width:1100,height:600,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			kankan:{number:"kankan",icon:"/icon/64/3155.png",privacy:false,iframes:true,title:"百会看看",url:"/applications/zoho/kankan.html",width:1100,height:600,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			xiuxiu:{number:"xiuxiu",icon:"/icon/64/3155.png",privacy:false,iframes:true,title:"百会秀秀",url:"/applications/zoho/xiuxiu.html",width:1100,height:600,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			gege:{number:"browser",icon:"/icon/64/2277.png",privacy:false,iframes:true,title:"百会格格",url:"/applications/zoho/gege.html",width:1100,height:600,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			kamera:{number:"kamera",icon:"/BlackHole/images/foot/kamera.png",privacy:false,iframes:true,title:"照相机",url:"/applications/cameras/yuanos.html",width:370,height:368,top:0,left:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			email:{number:"email",icon:"/BlackHole/images/foot/smail.png",privacy:false,iframes:true,title:"给我发送邮件",url:"/applications/sendmail/yuanos.html",width:570,height:430,top:0,left:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			tsina:{number:"tsina",icon:"/BlackHole/icon/apple/news.png",privacy:false,iframes:true,title:"新浪微博",url:"/applications/design/tsina.html",width:494,height:0,top:0,left:20,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"much"},
			tqq:{number:"tqq",icon:"/BlackHole/icon/apple/music.png",privacy:false,iframes:true,title:"腾讯微博",url:"/applications/design/tqq.html",width:494,height:0,top:0,left:20,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"much"},
			t163:{number:"t163",icon:"/BlackHole/icon/apple/t163.png",privacy:false,iframes:true,title:"网易微博",url:"/applications/design/t163.html",width:570,height:660,top:0,left:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"much"},
			bookmark:{number:"bookmark",icon:"/BlackHole/images/foot/bookmark.png",privacy:false,iframes:true,title:"我的书签",url:"/bookmark/yuanos.html",width:400,height:0,top:0,left:20,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"single"},
			rssnews:{number:"rssnews",icon:"/BlackHole/icon/apple/news.png",privacy:false,iframes:true,title:"新闻中心",url:"/applications/news/rssnews.html",width:1100,height:600,top:0,left:0,right:0,max:true,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			//rss:{number:"design",icon:"/BlackHole/icon/apple/rss.png",privacy:false,iframes:true,title:"rss订阅中心",url:"/applications/news/rssnews.html",width:1100,height:600,top:0,left:0,right:0,max:true,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			webvideo:{number:"webvideo",icon:"/BlackHole/icon/apple/music.png",privacy:false,iframes:true,title:"视频播放器",url:"/applications/video/yuanos.html",width:700,height:500,top:0,left:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:0,task:"much"},
			os:{number:"os",icon:"/BlackHole/images/foot/os.png",iframes:true,title:"YuanOS",url:"http://os.yuan.io/",width:0,height:0,top:-1,left:-1,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"single"},
			//os:{number:"design",icon:"/BlackHole/icon/apple/os.png",privacy:false,iframes:true,title:"YuanOS",url:"http://192.168.0.83:81/" + hostname,width:0,height:0,top:-1,left:-1,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			tudou:{number:"tudou",icon:"/BlackHole/images/foot/tudou.png",privacy:false,iframes:true,title:"土豆",url:"/applications/design/tudou.html",width:700,height:720,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			douban:{number:"douban",icon:"/BlackHole/icon/apple/music.png",privacy:false,iframes:true,title:"豆瓣",url:"/applications/design/douban.html",width:680,height:680,top:0,left:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			social:{number:"social",icon:"/BlackHole/images/foot/social.png",privacy:false,iframes:true,title:"足迹",url:"/applications/design/social.html",width:660,height:720,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			help:{number:"help",icon:"/BlackHole/images/foot/help.png",privacy:false,iframes:true,title:"设置向导",url:"/applications/design/help.html",width:700,height:600,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single",mask:true},
			bingdesktop:{number:"bingdesktop",icon:"/BlackHole/images/foot/bings.png",privacy:true,iframes:true,title:"bing壁纸",url:"/applications/design/bingdesktop.html",width:806,height:450,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"single"},
			explor:{number:"explor",icon:"/icon/explor.png",privacy:true,title:"资源管理器",iframes:true,url:"/explor/explorer.os.html",width:1100,height:600,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			diydesign:{number:"diydesign",icon:"/icon/explor.png",privacy:true,title:"个性卡片定制",iframes:true,url:"/applications/diy/diys.html",width:1200,height:700,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"much"},
			album:{number:"album",icon:"/icon/explor.png",privacy:true,title:"照片墙",iframes:true,url:"/applications/album/indexs.html",width:0,height:0,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"single"},
			config:{number:"config",icon:"/icon/config.png",privacy:true,title:"系统设置",iframes:true,url:"/commander-in-chief/config/index.html",width:1100,height:600,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"single"},
			social:{number:"explor",icon:"/icon/social.png",privacy:true,title:"关系中心",iframes:true,url:"/social/index.html",width:1100,height:600,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"single"},
			appstore:{number:"appstore",icon:"/icon/appstore.png",privacy:true,title:"应用商店",iframes:true,url:"/appstore/index.html",width:1200,height:700,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:1,task:"single"},
			message:{number:"message",icon:"/BlackHole/images/foot/message.png",privacy:true,iframes:true,title:"私信中心",url:"/applications/design/message.html",width:600,height:700,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			//tools:{number:"design",icon:"/BlackHole/icon/apple/tools.png",privacy:true,iframes:true,title:"设计中心",url:"/applications/blackholeadmin/yuanos.html",width:700,height:500,top:0,left:0,right:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:0,task:"single"},
			backgrounds:{number:"backgrounds",icon:"/BlackHole/images/foot/admin.png",privacy:true,iframes:true,title:"设置背景",url:"/applications/design/backgrounds.html",width:700,height:500,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			appadd:{number:"appadd",icon:"/BlackHole/images/foot/admin.png",privacy:true,iframes:true,title:"添加新的应用程序",url:"/appstore/add.html",width:700,height:500,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:0,task:"single"},
			xiami:{number:"xiami",icon:"/BlackHole/icon/apple/admin.png",privacy:false,iframes:true,title:"虾米音乐",url:"/applications/xiami/yuanos.html",width:257,height:63,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:0,task:"much"},
			//icon:{number:"icon",icon:"/BlackHole/images/foot/os.png",iframes:true,title:"图标选择器",url:"/icon/index.html",width:1020,height:600,top:0,left:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			calculator : {"number":"calculator","types":3,"category":8,"stretch":0,"movdisplay":1,"autosize":0,"width":540,"height":630,"top":0,"left":0,"right":0,"bottom":0,"scrolling":0,"task":0,"icon":"/icon/64/849.png","name":"科学计算器","url":"http://app.baidu.com/116526?canvas_pos=platform"},
			icon:{number:"icon",icon:"/BlackHole/images/foot/os.png",iframes:true,title:"图标选择器",url:"/icon/index.html",width:1020,height:600,top:0,left:0,max:false,tension:false,movlock:false,autosize:false,movdisplay:1,task:"single"},
			flashplay:{number:"flashplay",icon:"",title:"flash播放器",iframes:true,url:"/program_files/plashplay/flashplay.html",width:400,height:250,top:0,left:0,max:false,tension:true,movlock:false,autosize:false,movdisplay:true,task:"much"}
		},
		
		bu_onclick_idcode : function(app,pa,pas,url)
		{
			if(typeof(app) == 'string')
			{
				var number = app;
				if(number!="img")
				{
					app = Y.openapp.default[number];
					if(!app)
					{
						if(Y.Getapp)
						{
							app = Y.Getapp(number);
							if(!app)
							{
								Y.UI.alert("应用程序不存在！");
								return false;
							}
						}
						else
						{
							Y.UI.alert("应用程序不存在！");
							return false;
						}
					}
				}
			}
			else if(typeof(app) == 'object')
			{
				var number = app["number"];
			}

			if(Y.openapp.openclock[number]) return false;
			Y.openapp.openclock[number] = true;
			if(number=="img")
			{
				var tips = $.tips("正在载入图片...",{auto:false,location:["center","center"],load:true});
				ImgLoads({
					img:unescape(pa["img"]),
					onload:function(img){
						var title = pa["img"].split("/");
						title = title[title.length-1];
						Y.openapp.default["img"]={number:"img",icon:"",privacy:false,iframes:true,title:title,url:"/applications/design/img.html",width:img.width,height:img.height + 30,top:0,left:0,right:0,max:false,tension:false,movlock:false,autosize:true,movdisplay:1,task:"much"};
						if(!url)
						{
							Y.openapp.default["img"]["scrolling"] = "no";
						}
						Y.openapp.bu_onclick(Y.openapp.default["img"],null,pa,["id"]);
						Y.openapp.openclock[number] = false;
						tips&&tips.close();
					},
					onerror : function()
					{
						tips&&tips.close();
						Y.openapp.openclock[number] = false;
					}
				});
			}
			else
			{
				Y.openapp.bu_onclick(app,null,pa,pas,url);
			}
		},
		
		bu_onclick : function(app,y,pa,pas,url,title)//pa:参数
		{
			Y.History = Y.getobj("Y.History");
			if(Y.History)
			{
				Y.History["openapp"].splice(0,0,{
					"number" : app["number"],
					"pa" : pa,
					"pas" : pas,
					"title" : app["title"] || app["name"]
				});
				if(Y.History["openapp"].length>10)
				{
					Y.History["openapp"].length = 10;
				}
				Y.saveHistory&&Y.saveHistory();
			}
			if(!y&&y!=0)//打开新窗口
			{
				if(!app)
				{
					Y.UI.alert("应用程序不存在！");
				}
				if(!app["task"])app["task"] = "single";
				if(app["task"]=="single")//单任务程序
				{
					y = 0;
					if(!Y.openapp.button_activity[app["number"]]) Y.openapp.button_activity[app["number"]] = new Array();//新建活动程序池
					if(!Y.openapp.button_activity[app["number"]][y]) 
					{
						Y.openapp.button_activity[app["number"]][y] = Y.openapp.clone_button(app);
					}
					if(!Y.openapp.button_activity[app["number"]][y]["url"]&&pa)
					{
						Y.openapp.button_activity[app["number"]][y]["url"] = pa;
						Y.openapp.button_activity[app["number"]][y]["title"] = pa;
						Y.openapp.button_activity[app["number"]][y]["scrolling"] = "auto";
					}
					else
					{
						if(pa) Y.openapp.button_activity[app["number"]][y]["pa"] = pa;
						if(pas) Y.openapp.button_activity[app["number"]][y]["pas"] = pas;//传递特殊参数 例如窗口id等等
					}
					if(title) Y.openapp.button_activity[app["number"]][y]["title"] = title;
					Y.openapp.active_number = [app["number"],y,app["number"] + "_" + y];//活跃的窗口编号
					if (!($("#window" + app["number"] + "_" + y).length))//如果窗口不存在则打开新窗口
					{
						Y.openapp.open_window(app["number"],y);//打开窗口
						Y.openapp.openclock[app["number"]] = false;
					}
					else
					{
						if ($("#window" + app["number"] + "_" + y).css("display") == 'none')//如果窗口隐藏则显示窗口
						{
							Y.openapp.open_window(app["number"],y);//打开窗口
							Y.openapp.openclock[app["number"]] = false;
						}
						else
						{
							$("#window" + app["number"] + "_" + y).css({display:""});
							$("#window" + app["number"] + "_" + y).css({"z-index":Y.zIndex++});
							if(Y.openapp.button_activity[app["number"]][y]["number"]=="bookmark")
							{
								Y.close_window(app["number"],y);
								Y.openapp.openclock[app["number"]] = false;
							}
							else
							{
								Y.openapp.redwindow();//红色闪动
								Y.openapp.openclock[app["number"]] = false;
							}
						}
					}
				}
				else if(app["task"]=="much")//多任务程序
				{
					if(!Y.openapp.button_activity[app["number"]]) Y.openapp.button_activity[app["number"]] = new Array();//新建活动程序池
					y = Y.openapp.button_activity[app["number"]].length;
					if(!Y.openapp.button_activity[app["number"]][y])
					{
						Y.openapp.button_activity[app["number"]][y] = Y.openapp.clone_button(app);
					}
					if(url)Y.openapp.button_activity[app["number"]][y]["url"] = url;
					if(!Y.openapp.button_activity[app["number"]][y]["url"]&&pa)
					{
						Y.openapp.button_activity[app["number"]][y]["url"] = pa;
						Y.openapp.button_activity[app["number"]][y]["title"] = pa;
						Y.openapp.button_activity[app["number"]][y]["scrolling"] = "auto";
					}
					else
					{
						if(pa) Y.openapp.button_activity[app["number"]][y]["pa"] = pa;
						if(pas) Y.openapp.button_activity[app["number"]][y]["pas"] = pas;
					}
					if(title) Y.openapp.button_activity[app["number"]][y]["title"] = title;
					Y.openapp.active_number = [app["number"],y,app["number"] + "_" + y];//活跃的窗口编号
				
					if (!($("#window" + app["number"] + "_" + y).length))//如果窗口不存在则打开新窗口
					{
						Y.openapp.open_window(app["number"],y);//打开窗口
					}
					else
					{
						if ($("#window" + app["number"] + "_" + y).css("display") == 'none')//如果窗口隐藏则显示窗口
						{
							Y.openapp.open_window(app["number"],y);//打开窗口
						}
						else
						{
							$("#window" + app["number"] + "_" + y).css({display:""});
							$("#window" + app["number"] + "_" + y).css({"z-index":Y.zIndex++});
							Y.openapp.redwindow();//红色闪动
						}
					}
				}
				//任务管理
			}
			else//显示已有窗口
			{
				if(!app["task"])app["task"] = "single";
				if(app["task"]=="single")//单任务程序
				{
					y = 0;
					if(!Y.openapp.button_activity[app["number"]]) Y.openapp.button_activity[app["number"]] = new Array();//新建活动程序池
					if(!Y.openapp.button_activity[app["number"]][y]) 
					{
						Y.openapp.button_activity[app["number"]][y] = Y.openapp.clone_button(app);
					}
					if(pa) Y.openapp.button_activity[app["number"]][y]["pa"] = pa;
					if(pa) Y.openapp.button_activity[app["number"]][y]["pas"] = pas;
					
					Y.openapp.active_number = [app["number"],y,app["number"] + "_" + y];//活跃的窗口编号
				
					if (!($("#window" + app["number"] + "_" + y).length))//如果窗口不存在则打开新窗口
					{
						Y.openapp.open_window(app["number"],y);//打开窗口
					}
					else
					{
						if ($("#window" + app["number"] + "_" + y).css("display") == 'none')//如果窗口隐藏则显示窗口
						{
							Y.openapp.open_window(app["number"],y);//打开窗口
						}
						else
						{
							$("#window" + app["number"] + "_" + y).css({display:""});
							$("#window" + app["number"] + "_" + y).css({"z-index":Y.zIndex++});
							if(Y.openapp.button_activity[app["number"]][y]["number"]=="bookmark")
							{
								Y.close_window(app["number"],y);
							}
							else
							{
								Y.openapp.redwindow();//红色闪动
							}
						}
					}
				}
				else if(app["task"]=="much")//多任务程序
				{
					if(!Y.openapp.button_activity[app["number"]]) Y.openapp.button_activity[app["number"]] = new Array();//新建活动程序池
					if(!Y.openapp.button_activity[app["number"]][y]) 
					{
						Y.openapp.button_activity[app["number"]][y] = Y.openapp.clone_button(app);
					}
					if(pa) Y.openapp.button_activity[app["number"]][y]["pa"] = pa;
					if(pa) Y.openapp.button_activity[app["number"]][y]["pas"] = pas;
					
					Y.openapp.active_number = [app["number"],y,app["number"] + "_" + y];//活跃的窗口编号
					if (!($("#window" + app["number"] + "_" + y).length))//如果窗口不存在则打开新窗口
					{
						Y.openapp.open_window(app["number"],y);//打开窗口
					}
					else
					{
						if ($("#window" + app["number"] + "_" + y).css("display") == 'none')//如果窗口隐藏则显示窗口
						{
							Y.openapp.open_window(app["number"],y);//打开窗口
						}
						else
						{
							$("#window" + app["number"] + "_" + y).css({display:""});
							$("#window" + app["number"] + "_" + y).css({"z-index":Y.zIndex++});
							if(Y.openapp.button_activity[app["number"]][y]["number"]=="bookmark")
							{
								Y.close_window(app["number"],y);
							}
							else
							{
								Y.openapp.redwindow();//红色闪动
							}
						}
					}
				}
			}
		},

		clone_button : function(json)
		{
			if(!json) return false;
			var newjson = new Object;
			for(i in json)
			{
				newjson[i] = json[i];
			}
			return newjson;
		},
		//*************************点击鼠标响应函数***********************

		//****************************************************************
		//***************************打开窗口函数*************************
		//****************************************************************
		//窗口红色闪动
		redwindow : function()
		{
			var dom = $("#window_red" + Y.openapp.active_number[2]);
			if(!dom.length) return false;
			if (((Y.red++ % 2)==0))
			{
				dom.attr({"class" : "window_red"});
			}
			else
			{
				dom.attr({"class" : "ui-window"});
			}
			if (Y.red > Y.redx)
			{
				Y.red = 0;
				dom.attr({"class" : "ui-window"});
				//置顶默认窗口
				if ($("#window" + Y.ding).length)
				$("#window" + Y.ding).css({"z-index":Y.zIndex++});
			}
			else
			{
				setTimeout("Y.openapp.redwindow()",Y.redt);
			}
		},

		//打开窗口
		open_window : function(number,y)
		{
			//curriculum_object.ClientY = e.clientY;
			Y.clientHeight = $(document.body).height();
			Y.clientWidth = $(document.body).width();
			Y.HH = Y.getobj('Y.HH');
			Y.foot_height = Y.getobj('Y.foot_height');
			//获得窗口信息
			if(!Y.openapp.button_activity[number][y]) return false;
			
			if($("#window" + number + "_" + y).length)
			{
				var domt = $("#window" + number + "_" + y);
				var offset = domt.offset();
				Y.openapp.button_activity[number][y]['top'] = offset.top;
				Y.openapp.button_activity[number][y]['left'] = offset.left;
				Y.openapp.button_activity[number][y]['width'] = domt.width();
				Y.openapp.button_activity[number][y]['height'] = domt.height();
			}
			else
			{
				//----自动改变窗口大小---------------------------------------
				if(Y.openapp.button_activity[number][y]['width']>0&&(Y.openapp.button_activity[number][y]['autosize']||1))
				{
					if(Y.openapp.button_activity[number][y]['width']>(Y.clientWidth - 20))
					{
						Y.openapp.button_activity[number][y]['width'] = Y.clientWidth - 20;
					}
				}
				var HH = (Y.HH||0) + 40;
				if(Y.openapp.button_activity[number][y]['height']>0&&(Y.openapp.button_activity[number][y]['autosize']||1))
				{
					if(Y.openapp.button_activity[number][y]['height']>(Y.clientHeight - HH - Y.foot_height))
					{
						Y.openapp.button_activity[number][y]['height'] = Y.clientHeight - HH - Y.foot_height;
						Y.openapp.button_activity[number][y]['top'] = HH - 20;
					}
				}
				//----自动改变窗口大小---------------------------------------
				
				if (!(Y.openapp.button_activity[number][y]['top']))
				{
					//app['top'] = Y.top;
					var T =((Y.clientHeight - Y.openapp.button_activity[number][y]['height'] - Y.foot_height + 43)/2);
					//if (T<20) T = 20;
					T = Math.ceil(T);
					Y.openapp.button_activity[number][y]['top'] = T;
				}
				
				if (!(Y.openapp.button_activity[number][y]['left'])&&!(Y.openapp.button_activity[number][y]['right']))
				{
					Y.openapp.button_activity[number][y]['left'] = Math.ceil((Y.clientWidth - Y.openapp.button_activity[number][y]['width'])/2);
				}
				else
				{
					if (!(Y.openapp.button_activity[number][y]['left']))
					if (Y.openapp.button_activity[number][y]['right'])
						Y.openapp.button_activity[number][y]['left']=Math.ceil(Y.clientWidth - Y.openapp.button_activity[number][y]['right'] - Y.openapp.button_activity[number][y]['width']);
				}
				
				if ((Y.openapp.button_activity[number][y]['width'])==-1)//全屏
				{
					Y.openapp.button_activity[number][y]['width'] = Y.clientWidth + 2;
					Y.openapp.button_activity[number][y]['left'] = -1;
				}
				
				if ((Y.openapp.button_activity[number][y]['width'])==-2||!Y.openapp.button_activity[number][y]['width'])//全屏
				{
					Y.openapp.button_activity[number][y]['width'] = Y.clientWidth - 40;
					Y.openapp.button_activity[number][y]['left'] = 20;
				}
				
				if ((Y.openapp.button_activity[number][y]['height'])==-1)//全屏
				{
					Y.openapp.button_activity[number][y]['height'] = Y.clientHeight;
					Y.openapp.button_activity[number][y]['top'] = 0;
				}
				
				if (Y.openapp.button_activity[number][y]['height']==-2||!Y.openapp.button_activity[number][y]['height'])//最大化
				{
					Y.openapp.button_activity[number][y]['height'] = Y.clientHeight - HH - Y.foot_height;
					Y.openapp.button_activity[number][y]['top'] = HH - 20;
				}
				
				if ((Y.openapp.button_activity[number][y]['height'])==-1)
				{
					Y.openapp.button_activity[number][y]['height'] = Y.clientHeight;
				}
			}
			//alert(Y.addleft + " " + Y.addtop);
			if (!(Y.openapp.course))
			{
				var course = $('<div id="course" class="course"></div>');
				$("#topbox").append(course);
				//$(document.body).append(course);
				Y.openapp.course = course;
			}
			Y.openapp.course.css({display:"",height:"10px",width:"10px","z-index":Y.zIndex++});
			
			if(Y.openWx&&Y.openWy)
			{
				//----------------从原点打开----------------------------------------------------------------------
				Y.openapp.course.offset({ top: Y.openWy, left: Y.openWx });
				Y.openWx = 0;
				Y.openWy = 0;
				//------------------------------------------------------------------------------------------------
			}
			else
			{
				//----------------从中间打开----------------------------------------------------------------------
				Y.openapp.course.offset({ top: Math.abs(((Y.clientHeight)/2)*1), left: Math.abs(((Y.clientWidth)/2)*1) });
				//------------------------------------------------------------------------------------------------
			}
			Y.openapp.course.css({position : "absolute"});
			Y.width = Y.openapp.button_activity[number][y]['width'];
			Y.height = Y.openapp.button_activity[number][y]['height'];
			//alert(Y.addwidth + " " + Y.addheight + " " + Y.addleft + " " + Y.addtop);
			//Y.owin();
			//----------------------------op--------------------------------------
			var op = function(){
				var options = {
					logout_window:function(){
						if(!Y.openapp.button_activity[number][y]) return false;
						Y.openapp.button_activity[number][y] = null;
						if ($("#window" + number + "_" + y).length) 
						{
							$("#window" + number + "_" + y).animate(
							{
								opacity:0
							},
							500, "easeInOutQuart",function(){$("#window" + number + "_" + y).remove();});
							//easeInOutQuart easeOutQuint easeInOutQuint easeOutExpo easeInOutCirc
						}
						else
						{
							return false; 
						}
					},
					size_window:function(ev){
						var dom = $("#window" + number + "_" + y);
						dom.find();
						if (!Y.openapp.button_activity[number][y]['max'])
						{
							Y.size_height = dom.height();
							Y.size_width = dom.width();
							var offset = dom.offset();
							Y.size_top = offset.top;
							Y.size_left = offset.left;
							var HH = Y.HH;
							
							dom.animate(
							{
								width:$(document.body).width() + 2, left:-1,height:$(document.body).height() - Y.foot_height - HH,top:HH
							},
							200, "easeOutQuint",function(){});
							dom.find(".iframes").animate(
							{
								width:$(document.body).width() + 2, left:-1,height:$(document.body).height() - Y.foot_height - HH - 30,top:HH
							},
							200, "easeOutQuint");
							Y.openapp.button_activity[number][y]['max'] = true;
							//Y.ding_window(number);
							//Y.look_window(x,y);
							//$("#size" + x + "_" + y).attr({"src" : "/images/last.gif"});
						}
						else
						{	
							//dom.removeClass("ui-windows-shadow");
							dom.animate(
							{
								width:Y.size_width, left:Y.size_left,height:Y.size_height,top:Y.size_top
							},
							300, "easeInOutCirc",function(){});
							dom.find(".iframes").animate(
							{
								width:Y.size_width,height:Y.size_height - 30
							},
							300, "easeInOutCirc");
							Y.openapp.button_activity[number][y]['max'] = false;
						}
						ev.stopPropagation();
					},
					close_window:function(){},
					windowsfun : [
						{
							name:"mousedown",
							fun:function(ev){
								if (!ev) ev = window.event;
								var temponc = (typeof ev.target != "undefined")?ev.target:ev.srcElement;
								var dt = ev.originalEvent.dataTransfer;
								var dom = $(temponc);
								var pdom = dom.parents(".ui-blackhole").length?dom.parents(".ui-blackhole"):dom.parents(".ui-blackhole_win7");
								if(!pdom.length) pdom = dom.parents(".ui-blackhole_mac");
								var xy = pdom.attr("id").replace(/window/gi,"").split("_");
								if(!Y.openapp.button_activity[xy[0]][xy[1]]['mask'])
								dom.parents("div[_type=\"appwindow\"]").css({"z-index":Y.zIndex++});
								
							}
						}
					],
					zIndex : Y.zIndex++,
					display : "none"
				};
				var Win = Y.UI.app(Y.openapp.button_activity,Y.openapp.active_number,options);
				Win.fadeIn("normal");
				if(!Y.openapp.button_activity[number][y]['mask'])
				{
					Win.YuanDrag(function(dom){
						if(Y.openapp.button_activity[number][y]["movdisplay"])Win.find("iframe").css({display:""});
					},function(dom){
						if(Y.openapp.button_activity[number][y]["movdisplay"])Win.find("iframe").css({display:"none"});
					});
				}
				else
				{
					Funpool["BKJSON"]["maskwin"] = Win;
				}
				Y.openapp.openclock[number] = false;
			};
			op();
			//----------------------------op--------------------------------------
			/*
			Y.openapp.course.animate(
				{
					width:Y.width, left:Y.openapp.button_activity[number][y]['left'],height: Y.height ,top:Y.openapp.button_activity[number][y]['top']
				},
				200, "easeOutQuint",function(){
						Y.openapp.course.css({display:"none"});
						
						if ($("#window" + Y.openapp.active_number[2]).length)//窗口是否已经存在
						{
							$("#window" + Y.openapp.active_number[2]).css({display:""});
							$("#window" + Y.openapp.active_number[2]).css({"z-index":Y.zIndex++});
							
							//alert($("#window" + Y.openapp.active_number).innerHTML);
							//置顶默认窗口
							if (Y.ding&&$("#window" + Y.ding[2]).length)
							$("#window" + Y.ding[2]).css({"z-index":Y.zIndex++});
						}
						else
						{
							
							var options = {
								logout_window:function(){
									if(!Y.openapp.button_activity[number][y]) return false;
									Y.openapp.button_activity[number][y] = null;
									if ($("#window" + number + "_" + y).length) 
									{
										$("#window" + number + "_" + y).animate(
										{
											opacity:0
										},
										500, "easeInOutQuart",function(){$("#window" + number + "_" + y).remove();});
										//easeInOutQuart easeOutQuint easeInOutQuint easeOutExpo easeInOutCirc
									}
									else
									{
										return false; 
									}
								},
								size_window:function(){
									var dom = $("#window" + number + "_" + y);
									dom.find();
									if (!Y.openapp.button_activity[number][y]['max'])
									{
										Y.size_height = dom.height();
										Y.size_width = dom.width();
										var offset = dom.offset();
										Y.size_top = offset.top;
										Y.size_left = offset.left;
										if(Y.Background)
										{
											var HH = 43;
										}
										else
										{
											var HH = 0;
										}
										dom.animate(
										{
											width:$(document.body).width() + 2, left:-1,height:$(document.body).height() - Y.foot_height - HH,top:HH
										},
										200, "easeOutQuint",function(){});
										dom.find(".iframes").animate(
										{
											width:$(document.body).width() + 2, left:-1,height:$(document.body).height() - Y.foot_height - HH - 30,top:HH
										},
										200, "easeOutQuint");
										Y.openapp.button_activity[number][y]['max'] = true;
										//Y.ding_window(number);
										//Y.look_window(x,y);
										//$("#size" + x + "_" + y).attr({"src" : "/images/last.gif"});
									}
									else
									{	
										//dom.removeClass("ui-windows-shadow");
										dom.animate(
										{
											width:Y.size_width, left:Y.size_left,height:Y.size_height,top:Y.size_top
										},
										300, "easeInOutCirc",function(){});
										dom.find(".iframes").animate(
										{
											width:Y.size_width,height:Y.size_height - 30
										},
										300, "easeInOutCirc");
										Y.openapp.button_activity[number][y]['max'] = false;
									}
								},
								close_window:function(){},
								windowsfun : [
									{
										name:"mousedown",
										fun:function(ev){
											if (!ev) ev = window.event;
											var temponc = (typeof ev.target != "undefined")?ev.target:ev.srcElement;
											var dt = ev.originalEvent.dataTransfer;
											var dom = $(temponc);
											var pdom = dom.parents(".ui-blackhole");
											var xy = pdom.attr("id").replace(/window/gi,"").split("_");
											if(!Y.openapp.button_activity[xy[0]][xy[1]]['mask'])
											dom.parents("div[_type=\"appwindow\"]").css({"z-index":Y.zIndex++});
											
										}
									}
								],
								zIndex : Y.zIndex++
							};
							var Win = Y.UI.app(Y.openapp.button_activity,Y.openapp.active_number,options);
							if(!Y.openapp.button_activity[number][y]['mask'])
							{
								Win.YuanDrag(function(dom){
									if(Y.openapp.button_activity[number][y]["movdisplay"])Win.find("iframe").css({display:""});
								},function(dom){
									if(Y.openapp.button_activity[number][y]["movdisplay"])Win.find("iframe").css({display:"none"});
								});
							}
							else
							{
								Funpool["BKJSON"]["maskwin"] = Win;
							}
						}
						Y.openapp.openclock[number] = false;
					});
			//easeInOutQuart easeOutQuint easeInOutQuint easeOutExpo easeInOutCirc
			*/
		}
		//***************************打开窗口函数*************************
	};
	/**************************/

	/**************************
	**********默认函数*********
	**************************/
	function $A(iterable){
		if (iterable.item){
			var l = iterable.length, array = new Array(l);
			while (l--) array[l] = iterable[l];
			return array;
		}
		return Array.prototype.slice.call(iterable);
	};

	function $arguments(i){
		return function(){
			return arguments[i];
		};
	};

	function $chk(obj){
		return !!(obj || obj === 0);
	};

	function $clear(timer){
		clearTimeout(timer);
		clearInterval(timer);
		return null;
	};

	function $defined(obj){
		return (obj != undefined);
	};

	function $each(iterable, fn, bind){
		var type = $type(iterable);
		((type == 'arguments' || type == 'collection' || type == 'array') ? Array : Hash).each(iterable, fn, bind);
	};

	function $empty(){};

	function $extend(original, extended){
		for (var key in (extended || {})) original[key] = extended[key];
		return original;
	};

	function $H(object){
		return new Hash(object);
	};

	function $lambda(value){
		return ($type(value) == 'function') ? value : function(){
			return value;
		};
	};

	if (Array.slice === void 0) {
		Array.slice = function(self, start, end)
		{
			if (self && typeof self === 'object')
			{
				return Array.prototype.slice.call(self, start || 0, end || self.length);
				if (arguments.length < 2) { start = 0; }
				if (arguments.length < 3) { end = self.length; }
				return Array.prototype.slice.call(self, start, end);
			} 
			else
			{
				return [];
			}
		}
	}

	function $merge(){
		var args = Array.slice(arguments);
		args.unshift({});
		return $mixin.apply(null, args);
	};

	function $mixin(mix){
		for (var i = 1, l = arguments.length; i < l; i++){
			var object = arguments[i];
			if ($type(object) != 'object') continue;
			for (var key in object){
				var op = object[key], mp = mix[key];
				mix[key] = (mp && $type(op) == 'object' && $type(mp) == 'object') ? $mixin(mp, op) : $unlink(op);
			}
		}
		return mix;
	};

	function $pick(){
		for (var i = 0, l = arguments.length; i < l; i++){
			if (arguments[i] != undefined) return arguments[i];
		}
		return null;
	};

	var $random = window.$random = function (min, max){
		if(!min) min = 0;
		if(!max) max = 100;
		return Math.floor(Math.random() * (max - min + 1) + min);
	};

	function $splat(obj){
		var type = $type(obj);
		return (type) ? ((type != 'array' && type != 'arguments') ? [obj] : obj) : [];
	};

	var $time = Date.now || function(){
		return +new Date;
	};

	function $try(){
		for (var i = 0, l = arguments.length; i < l; i++){
			try {
				return arguments[i]();
			} catch(e){}
		}
		return null;
	};

	function $type(obj){
		if (obj == undefined) return false;
		if (obj.$family) return (obj.$family.name == 'number' && !isFinite(obj)) ? false : obj.$family.name;
		if (obj.nodeName){
			switch (obj.nodeType){
				case 1: return 'element';
				case 3: return (/\S/).test(obj.nodeValue) ? 'textnode' : 'whitespace';
			}
		} else if (typeof obj.length == 'number'){
			if (obj.callee) return 'arguments';
			else if (obj.item) return 'collection';
		}
		return typeof obj;
	};

	function $unlink(object){
		var unlinked;
		switch ($type(object)){
			case 'object':
				unlinked = {};
				for (var p in object) unlinked[p] = $unlink(object[p]);
			break;
			case 'hash':
				unlinked = new Hash(object);
			break;
			case 'array':
				unlinked = [];
				for (var i = 0, l = object.length; i < l; i++) unlinked[i] = $unlink(object[i]);
			break;
			default: return object;
		}
		return unlinked;
	};
	/**************************/
	
	/**************************
	********浏览器检查*********
	**************************/
	var curtain = Y.curtain = {
		open : function(fun,boo)
		{
			var curtain = $('<div class="curtain" />');
			curtain.css({
				"display":(boo?"":"none"),
				"background-color": "#000",
				"height": "100%",
				"width": "100%",
				"position": "absolute",
				"z-index": "30000",
				"background-image": "url(/BlackHole/images/nike.png)",
				"background-repeat": "no-repeat",
				"background-position": "center center"});

			$(document.body).append(curtain);
			if(!boo)
			{
				curtain.fadeIn("slow",function(){fun&&fun();});
			}
			else
			{
				fun&&fun();
			}
			return curtain;
		},
		close : function(curtain,fun)
		{
			if(!curtain||!curtain.length) return false;
			curtain.fadeOut("slow",function(){curtain.remove();fun&&fun();});
		}
	};
	/**************************/

	/**************************
	********浏览器检查*********
	**************************/
	var Browser = Y.Browser = $merge({

		Engine: {name: 'unknown', version: 0},

		Platform: {name: (window.orientation != undefined) ? 'ipod' : (navigator.platform.match(/mac|win|linux/i) || ['other'])[0].toLowerCase()},

		Features: {xpath: !!(document.evaluate), air: !!(window.runtime), query: !!(document.querySelector)},

		Plugins: {},

		Engines: {

			presto: function(){
				return (!window.opera) ? false : ((arguments.callee.caller) ? 960 : ((document.getElementsByClassName) ? 950 : 925));
			},

			trident: function(){
				return (!window.ActiveXObject) ? false : ((window.XMLHttpRequest) ? ((document.querySelectorAll) ? 6 : 5) : 4);
			},

			webkit: function(){
				return (navigator.taintEnabled) ? false : ((Browser.Features.xpath) ? ((Browser.Features.query) ? 525 : 420) : 419);
			},

			gecko: function(){
				return (!document.getBoxObjectFor && window.mozInnerScreenX == null) ? false : ((document.getElementsByClassName) ? 19 : 18);
			}

		}

	}, Browser || {});

	Browser.Platform[Browser.Platform.name] = true;

	Browser.detect = function(){

		for (var engine in this.Engines){
			var version = this.Engines[engine]();
			if (version){
				this.Engine = {name: engine, version: version};
				this.Engine[engine] = this.Engine[engine + version] = true;
				break;
			}
		}

		return {name: engine, version: version};

	};

	Browser.detect();

	Browser.Request = function(){
		return $try(function(){
			return new XMLHttpRequest();
		}, function(){
			return new ActiveXObject('MSXML2.XMLHTTP');
		}, function(){
			return new ActiveXObject('Microsoft.XMLHTTP');
		});
	};

	Browser.Features.xhr = !!(Browser.Request());

	Browser.Plugins.Flash = (function(){
		var version = ($try(function(){
			return navigator.plugins['Shockwave Flash'].description;
		}, function(){
			return new ActiveXObject('ShockwaveFlash.ShockwaveFlash').GetVariable('$version');
		}) || '0 r0').match(/\d+/g);
		return {version: parseInt(version[0] || 0 + '.' + version[1], 10) || 0, build: parseInt(version[2], 10) || 0};
	})();
	/**************************/

	/**************************
	********动态载入***********
	**************************/
	var IncJsFiles = Y.IncJsFiles = (function(){
		function DelScript(dom,fun){
			if(Browser.Engine.trident)
			{
				if(dom.readyState=="loaded"||dom.readyState=="complete")
				{
					fun && fun();
					dom.parentNode.removeChild(dom);
				}
			}
			else
			{
				fun && fun();
				if(dom)dom.parentNode.removeChild(dom);
			}
		}
		function DoIncJs(sSrc,fun)
		{
			if(typeof(fun)=="function")
			{
				var Fun = fun;
			}
			else
			{
				var Fun = function(){};
			}
			if(!Browser.Engine.trident)
			{
				var oHead = document.getElementsByTagName('head')[0];
				var oScript = document.createElement('script');
				oScript.type = "text/javascript";
				oScript.src = sSrc;
				oHead.appendChild(oScript);
				if(window.addEventListener)
				{
					oScript.addEventListener("load",function(){
						DelScript(this);
						Fun();
					},false);
				}
			}
			else
			{
				var oHead = document.getElementsByTagName('head')[0];
				var oScript = document.createElement('script');
				oScript.type = "text/javascript";
				oScript.src = sSrc;
				oHead.appendChild(oScript);
				if(window.attachEvent)
				{
					oScript.attachEvent("onreadystatechange", bindAsEvt(oScript, function(e){DelScript(this,Fun);}));
				}
			}
		}
		
		function bindAsEvt()
		{
			var args = Array.prototype.slice.call(arguments, 0), obj = args.shift(), fn = args.shift();
			return function(event){ fn.apply(obj, [event||window.event].concat(args))};
		}
		
		return function(sUrls,funpool) 
		{
			var sUrls=sUrls.split(",");
			var fun;
			for(var i=0;i<sUrls.length;i++) 
			{
				fun = funpool&&funpool[i]?funpool[i]:(typeof(funpool)=="function"?funpool:null);
				DoIncJs(sUrls[i],fun);
			}
		}
	})();

	var IncCssFiles = Y.IncCssFiles = (function(){
		function DoIncCss(sSrc)
		{
			var oHead = document.getElementsByTagName('head')[0];
			var oScript = document.createElement('link');
			oScript.type = "text/css";
			oScript.rel = "stylesheet";
			oScript.href = sSrc;
			oHead.appendChild(oScript);
		}
		
		return function(sUrls) 
		{
			var sUrls=sUrls.split(",");
			for(var i=0;i<sUrls.length;i++) 
			{
				DoIncCss(sUrls[i]);
			}
		}
	})();
	/*************************/

	/**************************
	********打开窗口***********
	**************************/
	var openw = Y.openw = function (theURL,winName,features,titlename)
	{
		var s1 = features.split(",");
		var w,h,featuresx=features;
		for (var i=0; i<s1.length; i++)
		{
			switch (s1[i].split("=")[0])
			{
				case "width":
					w = s1[i].split("=")[1];
					break;
				case "height":
					h = s1[i].split("=")[1];
					break;
			}
		}
		if (w&&h)
		{
			var t = Math.ceil((window.screen.height-h-400)/2);
			var l = Math.ceil((window.screen.width-w)/2);
			var text = "top=" + t + ",left=" + l;
		}
		if (text) featuresx += "," + text;
		var popupWin = window.open(theURL,winName,featuresx);
	};
	/*************************/


	/**************************
	********code操作***********
	**************************/
	var base6 = Y.base6={
		base64EncodeChars:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
		
		base64DecodeChars:[
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
		52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
		-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
		15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
		-1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
		41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1
		],
		
		base64encode:function(str)
		{
			var out, i, len;
			var c1, c2, c3;

			len = str.length;
			i = 0;
			out = "";
			while(i < len) {
			c1 = str.charCodeAt(i++) & 0xff;
			if(i == len)
			{
				out += base6.base64EncodeChars.charAt(c1 >> 2);
				out += base6.base64EncodeChars.charAt((c1 & 0x3) << 4);
				out += "==";
				break;
			}
			c2 = str.charCodeAt(i++);
			if(i == len)
			{
				out += base6.base64EncodeChars.charAt(c1 >> 2);
				out += base6.base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
				out += base6.base64EncodeChars.charAt((c2 & 0xF) << 2);
				out += "=";
				break;
			}
			c3 = str.charCodeAt(i++);
			out += base6.base64EncodeChars.charAt(c1 >> 2);
			out += base6.base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
			out += base6.base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6));
			out += base6.base64EncodeChars.charAt(c3 & 0x3F);
			}
			return out;
		},

		base64decode:function(str) {
			var c1, c2, c3, c4;
			var i, len, out;

			len = str.length;
			i = 0;
			out = "";
			while(i < len) {
			do {
				c1 = base6.base64DecodeChars[str.charCodeAt(i++) & 0xff];
			} while(i < len && c1 == -1);
			if(c1 == -1)
				break;

			do {
				c2 = base6.base64DecodeChars[str.charCodeAt(i++) & 0xff];
			} while(i < len && c2 == -1);
			if(c2 == -1)
				break;

			out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));

			do {
				c3 = str.charCodeAt(i++) & 0xff;
				if(c3 == 61)
				return out;
				c3 = base6.base64DecodeChars[c3];
			} while(i < len && c3 == -1);
			if(c3 == -1)
				break;

			out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));

			do {
				c4 = str.charCodeAt(i++) & 0xff;
				if(c4 == 61)
				return out;
				c4 = base6.base64DecodeChars[c4];
			} while(i < len && c4 == -1);
			if(c4 == -1)
				break;
			out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
			}
			return out;
		},

		utf16to8:function(str) {
			var out, i, len, c;

			out = "";
			len = str.length;
			for(i = 0; i < len; i++) 
			{
				c = str.charCodeAt(i);
				if ((c >= 0x0001) && (c <= 0x007F))
				{
					out += str.charAt(i);
				}
				else if (c > 0x07FF) 
				{
					out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
					out += String.fromCharCode(0x80 | ((c >> 6) & 0x3F));
					out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
				}
				else
				{
					out += String.fromCharCode(0xC0 | ((c >> 6) & 0x1F));
					out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
				}
			}
			return out;
		},

		utf8to16:function(str){
			var out, i, len, c;
			var char2, char3;

			out = "";
			len = str.length;
			i = 0;
			while(i < len) 
			{
				c = str.charCodeAt(i++);
				switch(c >> 4)
				{
					case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
						
						out += str.charAt(i-1);
						break;
					case 12: case 13:
						char2 = str.charCodeAt(i++);
						out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
						break;
					case 14:
						char2 = str.charCodeAt(i++);
						char3 = str.charCodeAt(i++);
						out += String.fromCharCode(((c & 0x0F) << 12)|((char2 & 0x3F) << 6)|((char3 & 0x3F) << 0));
						break;
				}
			}
			return out;
		},
		
		encode:function(str)
		{
			return base6.base64encode(base6.utf16to8(str));
		},
		
		decode:function(str)
		{
			return base6.utf8to16(base6.base64decode(str));
		}
	};

	//还原成字符串
	var JSON = Y.JSON = { 
		/*
		encode : function(input) { 
			if (typeof(input)=="undefined"||input==null) return 'null';
			switch (input.constructor) { 
				case String: return '"' + ((input.replace(/\"/gi,"\\\"")).replace(/\n/gi,"")).replace(/\r/gi,"") + '"';
				case Number: return input.toString();//number
				case Boolean: return input.toString();//boolean
				case Array : 
					var buf = [];
					for (i in input)
					{
						buf.push(JSON.encode(input[i]));
					}
					buf.length--;
					return '[' + buf.join(',') + ']';
				case Object: //object
					var buf = [];
					for (k in input) 
					{
						buf.push('"' + k + '":' + JSON.encode(input[k]));
					}
					return '{' + buf.join(',') + '}';
				case Function: //object
				default: 
					return 'null';
			} 
		} ,
		*/
		encode : function(input) { 
			if (typeof(input)=="undefined"||input==null) return 'null';
			
			switch (typeof(input)) { 
				case "string": return '"' + ((input.replace(/\"/gi,"\\\"")).replace(/\n/gi,"")).replace(/\r/gi,"") + '"';
				case "number": return input.toString();//number
				case "boolean": return input.toString();//boolean
				case "object": //object
					if(input.length==undefined)
					{
						var buf = [];
						for (k in input) 
						{
							buf.push('"' + k + '":' + JSON.encode(input[k]));
						}
						return '{' + buf.join(',') + '}';
					}
					else
					{
						var buf = [];
						/*
						for (i in input)
						{
							if(JSON.encode(input[i]))
							{
								buf.push(JSON.encode(input[i]));
							}
						}
						*/
						for (var i=0; i<input.length; i++)
						{
							if(JSON.encode(input[i]))
							{
								buf.push(JSON.encode(input[i]));
							}
						}
						//buf.length--;
						return '[' + buf.join(',') + ']';
					}
				case "function": //object
					return false;
				default: 
					return false;
			}
		}
	};
	
	var GetDomin = Y.GetDomin = function()
	{
		var domin = document.location.href;
		domin = domin.slice(7);
		domin = domin.split('/');
		domin = domin[0];
		return domin;
	};

	var GetTimeName = Y.GetTimeName = function(s)
	{
		var today = new Date();
		switch(s)
		{
			case "d":
				return today.getFullYear() + (today.getMonth()+1) + today.getDate() + today.getHours() + today.getMinutes() + today.getSeconds();
				break;
			case "mi":
			case "m":
				return today.getFullYear() + (today.getMonth()+1) + today.getDate() + today.getHours() + today.getMinutes();
				break;
			case "s":
				return today.getFullYear() + (today.getMonth()+1) + today.getDate() + today.getHours() + today.getMinutes() + today.getSeconds();
				break;
			case "ms":
				return today.getTime();
				break;
			default :
				return today.getFullYear() + (today.getMonth()+1)+ + today.getDate() + today.getHours() + today.getMinutes() + today.getSeconds();
				break;;
		}
		
	};

	var GetTimeString = Y.GetTimeString = function(time,s)
	{
		if(!time)
			var today = new Date();
		else
			var today = new Date(time);
		switch(s)
		{
			case "d":
				return today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate();
				break;
			case "h":
				return today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate() + " " + today.getHours();
				break;
			case "mi":
			case "m":
				return today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate() + " " + today.getHours() + ":" + today.getMinutes();
				break;
			case "s":
				return today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate() + " " + today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
				break;
			case "ms":
				return today.getTime();
				break;
			default :
				return today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate() + " " + today.getHours() + ":" + today.getMinutes();
				break;;
		}
		
	};
	

	var Code = Y.Code = {
		Ec94:function(){
		/*
		 * Ec94加密算法
		 * Author:Dron
		 * Date:2007-4-18
		 * Contact:ucren.com
		 */
			function MD5(){
				var sAscii=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ";
				var sAscii=sAscii+"[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
				var sHex="0123456789ABCDEF";
				function hex(i){
					h="";
					for(j=0;j<=3;j++){
						h+=sHex.charAt((i>>(j*8+4))&0x0F)+sHex.charAt((i>>(j*8))&0x0F);

					};
					return h;

				};
				function add(x,y){
					return ((x&0x7FFFFFFF)+(y&0x7FFFFFFF))^(x&0x80000000)^(y&0x80000000);

				};
				function R1(A,B,C,D,X,S,T){
					q=add(add(A,(B&C)|(~B&D)),add(X,T));
					return add((q<<S)|((q>>(32-S))&(Math.pow(2,S)-1)),B);

				};
				function R2(A,B,C,D,X,S,T){
					q=add(add(A,(B&D)|(C&~D)),add(X,T));
					return add((q<<S)|((q>>(32-S))&(Math.pow(2,S)-1)),B);

				};
				function R3(A,B,C,D,X,S,T){
					q=add(add(A,B^C^D),add(X,T));
					return add((q<<S)|((q>>(32-S))&(Math.pow(2,S)-1)),B);

				};
				function R4(A,B,C,D,X,S,T){
					q=add(add(A,C^(B|~D)),add(X,T));
					return add((q<<S)|((q>>(32-S))&(Math.pow(2,S)-1)),B);

				};
				this.calc=function (sInp,we){
					wLen=(((sInp.length+8)>>6)+1)<<4;
					var X=new Array(wLen);
					j=4;
					for(i=0;(i*4)<sInp.length;i++){
						X[i]=0;
						for(j=0;(j<4)&&((j+i*4)<sInp.length);j++){
							X[i]+=(sAscii.indexOf(sInp.charAt((i*4)+j))+32)<<(j*8);

						}
					};
					if(j==4){
						X[i++]=0x80;

					}else {
						X[i-1]+=0x80<<(j*8);

					};
					for(;i<wLen;i++){
						X[i]=0;

					};
					X[wLen-2]=sInp.length*8;
					a=0x67452301;
					b=0xefcdab89;
					c=0x98badcfe;
					d=0x10325476;
					for(i=0;i<wLen;i+=16){
						aO=a;
						bO=b;
						cO=c;
						dO=d;
						a=R1(a,b,c,d,X[i+0],7,0xd76aa478);
						d=R1(d,a,b,c,X[i+1],12,0xe8c7b756);
						c=R1(c,d,a,b,X[i+2],17,0x242070db);
						b=R1(b,c,d,a,X[i+3],22,0xc1bdceee);
						a=R1(a,b,c,d,X[i+4],7,0xf57c0faf);
						d=R1(d,a,b,c,X[i+5],12,0x4787c62a);
						c=R1(c,d,a,b,X[i+6],17,0xa8304613);
						b=R1(b,c,d,a,X[i+7],22,0xfd469501);
						a=R1(a,b,c,d,X[i+8],7,0x698098d8);
						d=R1(d,a,b,c,X[i+9],12,0x8b44f7af);
						c=R1(c,d,a,b,X[i+10],17,0xffff5bb1);
						b=R1(b,c,d,a,X[i+11],22,0x895cd7be);
						a=R1(a,b,c,d,X[i+12],7,0x6b901122);
						d=R1(d,a,b,c,X[i+13],12,0xfd987193);
						c=R1(c,d,a,b,X[i+14],17,0xa679438e);
						b=R1(b,c,d,a,X[i+15],22,0x49b40821);
						a=R2(a,b,c,d,X[i+1],5,0xf61e2562);
						d=R2(d,a,b,c,X[i+6],9,0xc040b340);
						c=R2(c,d,a,b,X[i+11],14,0x265e5a51);
						b=R2(b,c,d,a,X[i+0],20,0xe9b6c7aa);
						a=R2(a,b,c,d,X[i+5],5,0xd62f105d);
						d=R2(d,a,b,c,X[i+10],9,0x2441453);
						c=R2(c,d,a,b,X[i+15],14,0xd8a1e681);
						b=R2(b,c,d,a,X[i+4],20,0xe7d3fbc8);
						a=R2(a,b,c,d,X[i+9],5,0x21e1cde6);
						d=R2(d,a,b,c,X[i+14],9,0xc33707d6);
						c=R2(c,d,a,b,X[i+3],14,0xf4d50d87);
						b=R2(b,c,d,a,X[i+8],20,0x455a14ed);
						a=R2(a,b,c,d,X[i+13],5,0xa9e3e905);
						d=R2(d,a,b,c,X[i+2],9,0xfcefa3f8);
						c=R2(c,d,a,b,X[i+7],14,0x676f02d9);
						b=R2(b,c,d,a,X[i+12],20,0x8d2a4c8a);
						a=R3(a,b,c,d,X[i+5],4,0xfffa3942);
						d=R3(d,a,b,c,X[i+8],11,0x8771f681);
						c=R3(c,d,a,b,X[i+11],16,0x6d9d6122);
						b=R3(b,c,d,a,X[i+14],23,0xfde5380c);
						a=R3(a,b,c,d,X[i+1],4,0xa4beea44);
						d=R3(d,a,b,c,X[i+4],11,0x4bdecfa9);
						c=R3(c,d,a,b,X[i+7],16,0xf6bb4b60);
						b=R3(b,c,d,a,X[i+10],23,0xbebfbc70);
						a=R3(a,b,c,d,X[i+13],4,0x289b7ec6);
						d=R3(d,a,b,c,X[i+0],11,0xeaa127fa);
						c=R3(c,d,a,b,X[i+3],16,0xd4ef3085);
						b=R3(b,c,d,a,X[i+6],23,0x4881d05);
						a=R3(a,b,c,d,X[i+9],4,0xd9d4d039);
						d=R3(d,a,b,c,X[i+12],11,0xe6db99e5);
						c=R3(c,d,a,b,X[i+15],16,0x1fa27cf8);
						b=R3(b,c,d,a,X[i+2],23,0xc4ac5665);
						a=R4(a,b,c,d,X[i+0],6,0xf4292244);
						d=R4(d,a,b,c,X[i+7],10,0x432aff97);
						c=R4(c,d,a,b,X[i+14],15,0xab9423a7);
						b=R4(b,c,d,a,X[i+5],21,0xfc93a039);
						a=R4(a,b,c,d,X[i+12],6,0x655b59c3);
						d=R4(d,a,b,c,X[i+3],10,0x8f0ccc92);
						c=R4(c,d,a,b,X[i+10],15,0xffeff47d);
						b=R4(b,c,d,a,X[i+1],21,0x85845dd1);
						a=R4(a,b,c,d,X[i+8],6,0x6fa87e4f);
						d=R4(d,a,b,c,X[i+15],10,0xfe2ce6e0);
						c=R4(c,d,a,b,X[i+6],15,0xa3014314);
						b=R4(b,c,d,a,X[i+13],21,0x4e0811a1);
						a=R4(a,b,c,d,X[i+4],6,0xf7537e82);
						d=R4(d,a,b,c,X[i+11],10,0xbd3af235);
						c=R4(c,d,a,b,X[i+2],15,0x2ad7d2bb);
						b=R4(b,c,d,a,X[i+9],21,0xeb86d391);
						a=add(a,aO);
						b=add(b,bO);
						c=add(c,cO);
						d=add(d,dO);
					};
					if(we==16)return (hex(b)+hex(c));
					if(we==32)return (hex(a)+hex(b)+hex(c)+hex(d));
					return 0;

				}
			};
			var numbase="!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"+"[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
			var md5=new MD5;
			function to94scale(n){
				var re="";
				while(n>=94){
					re=numbase.charAt(n%94)+re; 
					n=Math.floor(n/94);

				};
				re=numbase.charAt(n%94)+re;
				re="!!!".substr(0,3-re.length)+re;
				return re;

			};
			function to10scale(word){
				var re=0;
				re=numbase.indexOf(word.charAt(0))*8836;
				re+=numbase.indexOf(word.charAt(1))*94;
				re+=numbase.indexOf(word.charAt(2));
				return re;

			};
			this.Encode=function (str,password){
				if(str==""||password=="")return false;
				var re="";
				for(var i=0;i<str.length;i++)re+=to94scale(str.charCodeAt(i)+password.charCodeAt(i%password.length));re=md5.calc(password,32).substr(3,3).toLowerCase()+re;return re;
			};
			this.Decode=function (str,password){
				if(str==""||password=="")return false;
				if(md5.calc(password,32).substr(3,3).toLowerCase()!=str.substr(0,3))return false;
				var re="",l=password.length;
				for(var i=3;i+3<=str.length;i+=3)re+=String.fromCharCode(to10scale(str.substr(i,3))-password.charCodeAt((i/3-1)%l));return re;
			};
		},

		encode:function(password,input_area)
		{
			if(!password||!input_area)return false;
			var ec94 = new Y.Code.Ec94;
			var values = ec94.Encode(input_area, password);
			return base6.encode(values);
		},

		decode:function(password,input_area)
		{
			if(!password||!input_area)return false;
			var ec94 = new Y.Code.Ec94;
			var value = input_area;
			value = base6.decode(value);
			var d = ec94.Decode(value, password);
			if (d)
			{
				return d;
			}
			else
			{
				return false;
			}
		},

		cookie:function(key, value, options)
		{
			if(value)
			{
				try
				{
					var value_c = this.encode(($.cookie("PHPSESSID")||"yuan.io"),value);
					$.cookie(key, value_c,options||{});
					return true;
				}
				catch(e){
					return false;
				}
			}
			else
			{
				try
				{
					var value_c = $.cookie(key);
					return this.decode(($.cookie("PHPSESSID")||"yuan.io"),value_c);
				}
				catch(e){
					return false;
				}
			}
		}
	};
	/*************************/

	/**************************
	*******String扩展**********
	**************************/
	String.prototype.Trim = function()
	{
		return	this.replace(/(^\s*)|(\s*$)/g,"");
	};
	String.prototype.trim = function()
	{
		return	this.replace(/(^\s*)|(\s*$)/g,"");
	};

	String.prototype.delpx = function()   
	{   
		return this.replace(/px/gi,"");
	};

	String.prototype.Htmlspecialchars = function()
	{ 
		var string = this;
		string = string.toString();

		string = string.replace(/&/g, '&amp;');
		string = string.replace(/</g, '&lt;');
		string = string.replace(/>/g, '&gt;');

		string = string.replace(/"/g, '&quot;');
		string = string.replace(/\'/g, '&#039;');

		return string;
	};

	String.prototype.isFileName = function()   
	{   
		var reg = /^[0-9a-zA-Z_\.]+$/gi;
		reg.lastIndex = 0;
		return reg.test(this);
	};

	String.prototype.isDouName = function(str)   
	{   
		var ignoreStr="'\"\/\\<>$%^?|:&* !+()~";
		if(typeof(str)=="string")
		{
			var strs = str.split("");
			for(var i=0; i<strs.length; i++)
			{
				ignoreStr = ignoreStr.replace(strs[i],"");
			}
		}
		var dou = 1;
		for(i=0;i<this.length;i++)
		{
			if(ignoreStr.indexOf(this.substring(i,i+1)) != -1)
			{
				return false;
			}
			if(this.charCodeAt(i)>255)
			{
				dou = 2;
			}
		}
		return dou;
	};

	String.prototype.isName = function(str)   
	{   
		//var ignoreStr="'\"\/\\<>$%^?|:&* !+-()~";
		var ignoreStr="'\"\/\\$%^|&* ~";
		if(typeof(str)=="string")
		{
			ignoreStr = ignoreStr.replace(str,"");
		}
		for(i=0;i<this.length;i++)
		{
			if(ignoreStr.indexOf(this.substring(i,i+1)) != -1)
			{
				return false;
			}
		}
		return true;
	};

	String.prototype.isUserName = function()   
	{   
		if (!this.isFileName())
		{
			return false;
		}
		if(this.split("")[0].isNumber())
		{
			return false;
		}
		if(this.split("")[0]=="."||this.split("")[0]=="_")
		{
			return false;
		}
		return true;
	};

	String.prototype.isEmail = function()   
	{   
		if(!/(\S)+[@]{1}(\S)+[.]{1}(\w)+/.test(this)) 
		{
			return false;
		} 
		else 
		{
			return true;
		}
	};

	String.prototype.cnslice = function(len)   
	{  
		if(!len) { return this; }

		var a = 0;

		var i = 0;

		var temp = '';

		for (i=0;i<this.length;i++)
		{
			if (this.charCodeAt(i)>255)  
			{
				a+=2;
			}
			else
			{
				a++;
			}
			if(a > len) { return temp; }
			temp += this.charAt(i);
		}
		return this;
	};

	String.prototype.isUrl = function()   
	{  
		var reg = /^http:\/\/.{0,93}/;
		return reg.test(this);
	 
		var regUrl = /^((https?|ftp|news):\/\/)?([a-z]([a-z0-9\-]*[\.。])+([a-z]{2}|aero|arpa|biz|com|coop|edu|gov|info|int|jobs|mil|museum|name|nato|net|org|pro|travel)|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))(\/[a-z0-9_\-\.~]+)*(\/([a-z0-9_\-\.]*)(\?[a-z0-9+_\-\.%=&]*)?)?(#[a-z][a-z0-9_]*)?/;

		//return regUrl.test(this);
		var result = this.match(regUrl); 
		if(result!=null)
		{
			return true;
		}
		else
		{ 
			return false;
		}
	};

	String.prototype.isurl = function()   
	{  
		var reg = /^http:\/\/.{0,93}/;
		return reg.test(this);
	 
		var regUrl = /^((https?|ftp|news):\/\/)?([a-z]([a-z0-9\-]*[\.。])+([a-z]{2}|aero|arpa|biz|com|coop|edu|gov|info|int|jobs|mil|museum|name|nato|net|org|pro|travel)|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))(\/[a-z0-9_\-\.~]+)*(\/([a-z0-9_\-\.]*)(\?[a-z0-9+_\-\.%=&]*)?)?(#[a-z][a-z0-9_]*)?/;

		//return regUrl.test(this);
		var result = this.match(regUrl); 
		if(result!=null)
		{
			return true;
		}
		else
		{ 
			return false;
		}
	};

	String.prototype.isIp = function()   
	{  
		var haveChar=0;
		var ip=this.split(".");
		for(i=0;i<4;i++)
		{
			if(ip[i].match(/\D/g))
			{
				haveChar=1;
				ip[i]=ip[i].replace(/\D/g,"");
			}
		}
		if(haveChar==1)
		{
			return false;
		}
		if(parseInt(ip[0])>0&&parseInt(ip[0])<256&&parseInt(ip[1])>-1&&parseInt(ip[1])<256&&parseInt(ip[2])>-1&&parseInt(ip[2])<256&&parseInt(ip[3])>-1&&parseInt(ip[3])<256)
		{
			return true;
		}
		else
		{
			return false;
		}
	};

	String.prototype.lenB = function() {
		return this.replace(/[^\x00-\xff]/g,"**").length;
	};

	String.prototype.Br = function() {
		return this.replace(/\n/g,"<br />");
	};

	String.prototype.isNumber = function(DU)
		{
			if(DU)
			{
				var Letters = "1234567890-.";
			}
			else
			{
				var Letters = "1234567890";
			}
			var i;
			var c;
			for( i = 0; i < this.length; i ++ )
			{
				c = this.charAt( i );
				if (Letters.indexOf( c ) ==-1)
				{
					return false;
				}
			}
			return true; 
		};

	String.prototype.getName = function()
		{
			var names = this.split("/");
			var name = names[names.length - 1];
			return name; 
		};

	String.prototype.strip_tags = function(allowed)
		{
			allowed = (((allowed || "") + "").toLowerCase().match(/<[a-z][a-z0-9]*>/g) || []).join(''); 
			var tags = /<\/?([a-z][a-z0-9]*)\b[^>]*>/gi, commentsAndPhpTags = /<!--[\s\S]*?-->|<\?(?:php)?[\s\S]*?\?>/gi;
			return this.replace(commentsAndPhpTags, '').replace(tags, function ($0, $1) {
				return allowed.indexOf('<' + $1.toLowerCase() + '>') > -1 ? $0 : '';
			});
		};
	/*************************/

	/**************************
	********Array扩展**********
	**************************/
	window.objectClone = function(obj)
	{
		var newArr = {};
		for(var x in obj)
		{
			newArr[x] = obj[x];
		}
		return newArr;
	};
	Array.prototype.clone = function()
	{
		var newArr = new Array();
		for(i=0;i<this.length;i++)
		{
			newArr[i] = this[i];
		}
		return newArr;
	};
	Array.prototype.del = function() { 
		var a = {}, c = [], l = this.length; 
		for (var i = 0; i < l; i++)
		{ 
			var b = this[i]; 
			var d = (typeof b) + b; 
			if (a[d] === undefined)
			{ 
				c.push(b);
				a[d] = 1;
			} 
		} 
		return c; 
	};
	/*************************/

	/**************************
	**********url分析**********
	**************************/
	var $nt = window.$nt = function (id)
	{
		return document.getElementsByTagName(id);
	};

	var REQUEST = Y.REQUEST = {
		QS: function(names)
		{
			var URLParams = "";
			var aParams = document.location.search.substr(1).split('&');
			for (i=0; i < aParams.length ; i++)
			{
				var aParam = aParams[i].split('=');
				if (aParam[0]==names)
					URLParams = aParam[1];
			}
			return URLParams;
		},
		QSM: function()
		{
			return document.location.search.slice(1);
			var URLParams = "";
			var aParams = document.location.search.substr(1).split('&');
			if (aParams.length==1)
			{
				var aParam = aParams[0].split('=');
				if (aParam.length==1)
				{
					URLParams = aParam[0];
				}
				else
				{
					URLParams = aParams;
				}
			}
			else
			{
				URLParams = aParams;
			}
			return URLParams;
		},
		
		meta:function(name)
		{
			var metas = $nt("meta");
			for(var i=0; i<metas.length; i++)
			{
				if(metas[i]["name"]==name)
				{
					if(metas[i]["content"]) return metas[i]["content"];
				}
			}
			return false;
		}
	};

	var request = Y.request = function(names)
	{
		if(names)
		{
			var URLParams = "";
			var aParams = document.location.search.substr(1).split('&');
			for (i=0; i < aParams.length ; i++)
			{
				var aParam = aParams[i].split('=');
				if (aParam[0]==names)
					URLParams = aParam[1];
			}
			return URLParams;
		}
		else
		{
			return document.location.search.slice(1);
			var URLParams = "";
			var aParams = document.location.search.substr(1).split('&');
			if (aParams.length==1)
			{
				var aParam = aParams[0].split('=');
				if (aParam.length==1)
				{
					URLParams = aParam[0];
				}
				else
				{
					URLParams = aParams;
				}
			}
			else
			{
				URLParams = aParams;
			}
			return URLParams;
		}
	};
	/*************************/

	/**************************
	**********url分析**********
	**************************/
	Y.PURL = {};
	Y.PURL.URLParser = function(url) {  

		this._fields = {  
			'Username' : 4,   
			'Password' : 5,   
			'Port' : 7,   
			'Protocol' : 2,   
			'Host' : 6,   
			'Pathname' : 8,   
			'URL' : 0,   
			'Querystring' : 9,   
			'Fragment' : 10  
		};  

		this._values = {};  
		this._regex = null;  
		this.version = 0.1;  
		this._regex = /^((\w+):\/\/)?((\w+):?(\w+)?@)?([^\/\?:]+):?(\d+)?(\/?[^\?#]+)?\??([^#]+)?#?(\w*)/;
		for(var f in this._fields)  
		{  
			this['get' + f] = this._makeGetter(f);  
		}  

		if (typeof url != 'undefined')  
		{  
			this._parse(url);  
		}  
	};
	Y.PURL.URLParser.prototype.setURL = function(url) {  
		this._parse(url);
	};

	Y.PURL.URLParser.prototype._initValues = function() {
		for(var f in this._fields)
		{
			this._values[f] = '';
		}
	};

	Y.PURL.URLParser.prototype._parse = function(url) {
		this._initValues();
		var r = this._regex.exec(url);
		if (!r) throw "DPURLParser::_parse -> Invalid URL";

		for(var f in this._fields) if (typeof r[this._fields[f]] != 'undefined')
		{
			this._values[f] = r[this._fields[f]];
		}
	};

	Y.PURL.URLParser.prototype._makeGetter = function(field) {  
		return function() {
			return this._values[field];
		}
	};
	/*************************/
	
	var is_iPad = Y.is_iPad = function (){
		var ua = navigator.userAgent.toLowerCase();
		if(ua.match(/iPad/i)=="ipad") {
			return true;
		} else {
			return false;
		}
	};
	
	var ImgLoads = Y.ImgLoads = function(options)
	{
		var defaults = {
				img: "",
				par:[{}],
				onerror : function(){},
				onload : function(){}
		};
		var options = $.extend(defaults, options);
		var image = new Image();
		for(var i=0; i<defaults.par.length; i++)
		{
			if(defaults.par[i])
			{
				$(image).attr(defaults.par[i]);
			}
		}
		image.src = defaults.img;
		image.onerror = function(dv){
			defaults.onerror(dv,this);
		};
		image.onload = function(){
			defaults.onload(this);
		};
	};
	
	var color16 = Y.color16 = function(color)
	{
		var c1="",c2="",c3="";
		var colors = color.replace("#","");
		var length = (colors + "").split("").length;
		if(length>5)
		{
			c1 = colors.slice(0,2);
			c2 = colors.slice(2,4);
			c3 = colors.slice(4,6);
		}
		else if(length==3)
		{
			c1 = colors.slice(0,1);
			c2 = colors.slice(1,2);
			c3 = colors.slice(2,3);
			
			c1 = c1 + c1;
			c2 = c2 + c2;
			c3 = c3 + c3;
		}
		else if(length>0)
		{
			for(var i=0; i<(6 - length); i++)
			{
				colors = "0" + colors;
			}
			c1 = colors.slice(0,2);
			c2 = colors.slice(2,4);
			c3 = colors.slice(4,6);
		}
		return parseInt( c1,16) + "," + parseInt( c2,16) + "," + parseInt( c3,16);
		
	};
	/**************************/
	
	/**************************
	*********鼠标滚珠**********
	**************************/
	Y.wheel = function(fun,cfun)
	{
		function wheel(e,fun,cfun)
		{
			if (!e) e = window.event;
			var dom = (typeof e.target != "undefined")?e.target:e.srcElement;
			
			if(!cfun)cfun = function(){return true};
			if(cfun(e,dom))
			{
				if (e.wheelDelta)
				{
					(typeof(fun)=="function") && fun(e.wheelDelta/120,$(dom));
				} 
				else if (e.detail)
				{
					(typeof(fun)=="function") && fun(e.detail/3,$(dom));
				}
			}
		};
		if (window.onmousewheel)
		{
			window.onmousewheel = document.onmousewheel = function(e){wheel(e,fun,cfun);};
		}
		else
		{
			window.addEventListener('DOMMouseScroll', function(e){wheel(e,fun,cfun);}, false);
			window.addEventListener('mousewheel', function(e){wheel(e,fun,cfun);}, false);
		}
	};
	/**************************/
	
	/**************************
	*********超级拖拽**********
	**************************/
	var SuperDrag = Y.SuperDrag = function(par)
	{
		if(!par) par = {};
		if(!par["dom"]||!par["dom"].length) return false;
		par["dom"]
				.bind('dragenter', function(ev) {	//add
					if (!ev) ev = window.event;
					var dom = (typeof ev.target != "undefined")?ev.target:ev.srcElement;
					var dom = $(dom);
					(typeof(par["dragenter"])=="function") && par["dragenter"](ev,dom);
					return false;
				})
				.bind('dragleave', function(ev) {	//del
					if (!ev) ev = window.event;
					var dom = (typeof ev.target != "undefined")?ev.target:ev.srcElement;
					var dom = $(dom);
					(typeof(par["dragenter"])=="function") && par["dragleave"](ev,dom);
					return false;
				})
				.bind('dragover', function(ev) {	//add
					if (!ev) ev = window.event;
					var dom = (typeof ev.target != "undefined")?ev.target:ev.srcElement;
					var dom = $(dom);
					(typeof(par["dragenter"])=="function") && par["dragover"](ev,dom);
					return false;
				})
				.bind('drop', function(ev) {		//del
					if (!ev) ev = window.event;
					var dom = (typeof ev.target != "undefined")?ev.target:ev.srcElement;
					var dom = $(dom);
					(typeof(par["drop"])=="function") && par["drop"](ev,dom);
					var dt = ev.originalEvent.dataTransfer;
					var texts = dt.getData('Text');
					var files = ev.originalEvent.dataTransfer.files;
					
					if(!files||!files.length)
					{
						(typeof(par["gettext"])=="function") && par["gettext"](ev,dom,texts);
					}
					else
					{
						(typeof(par["getfile"])=="function") && par["getfile"](ev,dom,files);
					}
					return false;
				});
	};
	
	/**************************
	*********配置管理**********
	**************************/
	var Getjson = Y.Getjson = function(par)
	{
		var tips = $.tips("正在读取数据...",{auto:false,load:true});
		if(!par["name"])
		{
			tips.close();
			return false;
		}
		//hosts,users,name,fun,defreturn
		var nowusers = Y.getobj("Y.loginarray.current");
		if(!par["domain"])
		{
			par["domain"] = nowusers["dname"];
		}
		if(!par["hosts"])
		{
			par["hosts"] = nowusers["hname"];
		}
		var API = Y.Getapi();
		var code = {"domain":par["domain"],"hosts":par["hosts"],"name":par["name"],"class":"Os","fun":"get_json"};
		$.post(API,{code:Y.base6.encode(Y.JSON.encode(code))},function(data){
					try
					{
						tips && tips.close();
						var array;
						var json = eval("(" + data + ")");
						if(json)
						{
							//if(par["defreturn"])
							//{
							//	array = $.extend(par["defreturn"], json);
							//}
							//else
							//{
								array = json;
							//}
						}
						else
						{
							if(par["defreturn"])
							{
								array = par["defreturn"];
							}
						}
						(typeof(par["fun"])=="function")&&par["fun"](array);
					}
					catch(e){
						if(par["defreturn"])
						{
							array = par["defreturn"];
						}
						(typeof(par["fun"])=="function")&&par["fun"](array,data);
					}
				});
	};
	
	var Savejson = Y.Savejson =  function(par){
		//hosts,users,name,jsons,fun
		if(!Y.isMaster())
		{
			return false;
		}
		var tips = $.tips("正在更新数据...",{auto:false,load:true});
		if(!par["name"])
		{
			tips.close();
			return false;
		}
		var API = Y.Getapi();
		if(typeof(par["jsons"])=="object")
		{
			var json = Y.JSON.encode(par["jsons"]);
		}
		else
		{
			var json = par["jsons"];
		}
		var nowusers = Y.getobj("Y.loginarray.current");
		if(!par["hosts"])
		{
			par["domain"] = nowusers["dname"];
		}
		if(!par["hosts"])
		{
			par["hosts"] = nowusers["hname"];
		}
		var code = {"domain":par["domain"],"hosts":par["hosts"],"name":par["name"],"class":"Os","fun":"save_json"};
		$.post(API,{code:Y.base6.encode(Y.JSON.encode(code)),json:json},function(data){
					try
					{
						tips.close();
						var json = eval("(" + data + ")");
						(typeof(par["fun"])=="function")&&par["fun"](json);
					}
					catch(e){
						(typeof(par["fun"])=="function")&&par["fun"](false,data);
					}
				});
	};
	
	var Gethub = Y.Gethub = function(par)
	{
		var tips = $.tips("正在读取数据...",{auto:false,load:true});
		if(!par["name"])
		{
			tips.close();
			return false;
		}
		var key = par["key"] || "yuanos";
		key = key + "";
		var name = Y.Code.decode(key,par["name"].Trim());
		if(!name)
		{
			(typeof(par["fun"])=="function")&&par["fun"](false);
			tips && tips.close();
			return false;
		}
		var API = Y.Getapi();
		var code = {"name":name,"class":"Os","fun":"gethub"};
		$.post(API,{code:Y.base6.encode(Y.JSON.encode(code))},function(data){
					try
					{
						tips && tips.close();
						var array;
						//var json = eval("(" + data + ")");
						var json = eval("(" + Y.base6.decode(data) + ")");
						if(json)
						{
							array = json;
						}
						else
						{
							array = false;
						}
						(typeof(par["fun"])=="function")&&par["fun"](array);
					}
					catch(e){
						(typeof(par["fun"])=="function")&&par["fun"](data);
					}
		});
	};
	
	var Savehub = Y.Savehub =  function(par){
		//hosts,users,name,jsons,fun
		if(!Y.isMaster())
		{
			return false;
		}
		var tips = $.tips("正在更新数据...",{auto:false,load:true});
		if(!par["name"])
		{
			var today = new Date();
			var member = Y.GetMember();
			par["name"] = member["number"] + today.getTime();
		}
		var API = Y.Getapi();
		if(typeof(par["jsons"])=="object")
		{
			var json = Y.JSON.encode(par["jsons"]);
		}
		else
		{
			var json = par["jsons"];
		}
		var code = {"name":par["name"],"class":"Os","fun":"savehub"};
		$.post(API,{code:Y.base6.encode(Y.JSON.encode(code)),json:json},function(data){
			try
			{
				tips.close();
				//var json = eval("(" + data + ")");
				(typeof(par["fun"])=="function")&&par["fun"](Y.Code.encode(par["key"] || "yuanos",par["name"]));
			}
			catch(e){
				(typeof(par["fun"])=="function")&&par["fun"](false);
			}
		});
	};
	var current = Y.getobj("Y.loginarray.current");

	Y.isMaster = function(){
		var loginarray = Y.getobj("Y.loginarray");
		if(loginarray&&loginarray["master"])
		{
			return true;
		}
		else
		{
			return false;
		}
	};

	Y.GetDomain = function(){
		var nowusers = Y.getobj("Y.loginarray.current");
		return {"name":nowusers["dname"],"number":nowusers["domain"]};
	};
	
	Y.GetHost = function(){
		var current = Y.getobj("Y.loginarray.current");
		return {"name":current["hname"],"number":current["number"]};
	};
	
	Y.GetHosts = function(){
		var hosts = Y.getobj("Y.loginarray.hosts");
		return hosts;
	};
	
	Y.GetMember = function(){
		var member = Y.getobj("Y.loginarray.member");
		return member;
	};
	
	Y.AddSysInfo = function(json,boo){
		var array = json;
		array["domain"] = Y.GetDomain();
		array["host"] = Y.GetHost();
		if(boo)array["member"] = Y.GetMember();
		return array;
	};
	
	Y.Read = function(jsons,fun,datas,boo){
		
		if(jsons["tips"]) var tips = $.tips(((typeof(jsons["tips"])=="string")?jsons["tips"]:"正在处理数据..."),{auto:false,load:true});
		var API = Y.Getapi();
		//boo是否附带主机和账号
		if(boo)
		{
			if(typeof(jsons)=="object")
			{
				var current = Y.getobj("Y.loginarray.current");
				if(!jsons["domain"])
				{
					jsons["domain"] = current["domain"];
					jsons["dname"] = current["dname"];
				}
				if(!jsons["hosts"])
				{
					jsons["hosts"] = current["number"];
					jsons["hname"] = current["hname"];
				}
			}
			else if(typeof(jsons)=="string")
			{
				try
				{
					var jsons = eval("(" + jsons + ")");
					if(jsons)
					{
						var nowusers = Y.getobj("Y.loginarray.current");
						if(!jsons["domain"])
						{
							jsons["domain"] = current["domain"];
							jsons["dname"] = current["dname"];
						}
						if(!jsons["hosts"])
						{
							jsons["hosts"] = current["number"];
							jsons["hname"] = current["hname"];
						}
					}
					else
					{
						return false;
					}
				}
				catch(e){
					return false;
				}
			}
		}
		if(typeof(jsons)=="object")
		{
			var json = Y.JSON.encode(jsons);
		}
		else
		{
			var json = jsons;
		}
		
		var array = {code:Y.base6.encode(json)};
		array = $.extend(array, datas);
		$.post(API,array,function(data){
			//try
			{
				tips && tips.close();
				var array = eval("(" + data + ")");
				if(array)
				{
					(typeof(fun)=="function")&&fun(array);
				}
				else
				{
					(typeof(fun)=="function")&&fun(false);
				}
			}
			//catch(e){
			//	(typeof(fun)=="function")&&fun(false,data);
			//}
		});
	};
	
	Y.Write = function(jsons,fun,datas,boo){
		
		if(!Y.isMaster())
		{
			return false;
		}
		if(jsons["tips"]) var tips = $.tips(((typeof(jsons["tips"])=="string")?jsons["tips"]:"正在处理数据..."),{auto:false,load:true});
		var API = Y.Getapi();
		//boo是否附带主机和账号
		if(boo)
		{
			if(typeof(jsons)=="object")
			{
				var current = Y.getobj("Y.loginarray.current");
				if(!jsons["domain"])
				{
					jsons["domain"] = current["domain"];
					jsons["dname"] = current["dname"];
				}
				if(!jsons["hosts"])
				{
					jsons["hosts"] = current["number"];
					jsons["hname"] = current["hname"];
				}
			}
			else if(typeof(jsons)=="string")
			{
				try
				{
					var jsons = eval("(" + jsons + ")");
					if(jsons)
					{
						var nowusers = Y.getobj("Y.loginarray.current");
						if(!jsons["domain"])
						{
							jsons["domain"] = current["domain"];
							jsons["dname"] = current["dname"];
						}
						if(!jsons["hosts"])
						{
							jsons["hosts"] = current["number"];
							jsons["hname"] = current["hname"];
						}
					}
					else
					{
						return false;
					}
				}
				catch(e){
					return false;
				}
			}
		}
		if(typeof(jsons)=="object")
		{
			var json = Y.JSON.encode(jsons);
		}
		else
		{
			var json = jsons;
		}
		
		var array = {code:Y.base6.encode(json)};
		array = $.extend(array, datas);
		$.post(API,array,function(data){
			try
			{
				tips && tips.close();
				var array = eval("(" + data + ")");
				if(array)
				{
					(typeof(fun)=="function")&&fun(array);
				}
				else
				{
					(typeof(fun)=="function")&&fun(false);
				}
			}
			catch(e){
				(typeof(fun)=="function")&&fun(false,data);
			}
		});
	};
	
	var POST = Y.POST =  function(jsons,fun,datas,boo){
		
		if(jsons["tips"]) var tips = $.tips(((typeof(jsons["tips"])=="string")?jsons["tips"]:"正在处理数据..."),{auto:false,load:true});
		var API = Y.Getapi();
		//boo是否附带主机和账号
		if(boo)
		{
			if(typeof(jsons)=="object")
			{
				var current = Y.getobj("Y.loginarray.current");
				if(!jsons["domain"])
				{
					jsons["domain"] = current["domain"];
					jsons["dname"] = current["dname"];
				}
				if(!jsons["hosts"])
				{
					jsons["hosts"] = current["number"];
					jsons["hname"] = current["hname"];
				}
			}
			else if(typeof(jsons)=="string")
			{
				try
				{
					var jsons = eval("(" + jsons + ")");
					if(jsons)
					{
						var nowusers = Y.getobj("Y.loginarray.current");
						if(!jsons["domain"])
						{
							jsons["domain"] = current["domain"];
							jsons["dname"] = current["dname"];
						}
						if(!jsons["hosts"])
						{
							jsons["hosts"] = current["number"];
							jsons["hname"] = current["hname"];
						}
					}
					else
					{
						return false;
					}
				}
				catch(e){
					return false;
				}
			}
		}
		if(typeof(jsons)=="object")
		{
			var json = Y.JSON.encode(jsons);
		}
		else
		{
			var json = jsons;
		}
		
		var array = {code:Y.base6.encode(json)};
		array = $.extend(array, datas);
		$.post(API,array,function(data){
			try
			{
				tips && tips.close();
				var array = eval("(" + data + ")");
				if(array)
				{
					(typeof(fun)=="function")&&fun(array);
				}
				else
				{
					(typeof(fun)=="function")&&fun(false);
				}
			}
			catch(e){
				(typeof(fun)=="function")&&fun(false,data);
			}
		});
	};
	/**************************/
	(function($){
		$.fn.stretch = function(options){
			this.each(function(){
				this.posRange = {minX:0,minY:0,maxX:(document.compatMode == "CSS1Compat"?document.documentElement.clientWidth:document.body.clientWidth),maxY:(document.compatMode == "CSS1Compat"?document.documentElement.clientHeight:document.body.clientHeight)};
				this.onmousedown = function(e)
				{
					this.drag(e,options);
					options["down"] && options["down"](this);
					e.stopPropagation();
				};
				this.drag = function(e,options)
				{
					var element = this,ev = e || window.event;
					ev.rScreenX = ev.screenX;
					ev.rScreenY = ev.screenY;

					element.dragConfig = {pdomW : parseInt(options["pdom"].width(),10),pdomH : parseInt(options["pdom"].height(),10)};
					document.onmouseup = function()
					{
						element.drop();
						options["up"] && options["up"](this);
						e.stopPropagation();
					};
					document.onmousemove = function(e)
					{
						var ev2 = e || window.event;
						var mx = element.dragConfig.pdomW + (ev2.screenX - ev.rScreenX);
						var my = element.dragConfig.pdomH + (ev2.screenY - ev.rScreenY);
						options["move"] && options["move"](mx,my);
						e.stopPropagation();
						return false;
					};
					document.onselectstart = function(){return false;};
				};
				this.drop = function()
				{
					document.onmousemove = document.onselectstart = document.onmouseup = null;
				};
			});
		};
	})(jQuery);
	//jQuery插件--------------------------------------------------------------------------------------------------------------------------
	//------------------------------------------------------------------------------------------------------------------------------------
	(function($){
		$.fn.inputdef = function(text){
			this.each(function(){
				if($(this)[0].tagName=="INPUT"||$(this)[0].tagName=="TEXTAREA")
				{
					$(this).val(text);
					$(this)
					.bind("focusout",function(){
						if($(this).val()=="")
						{
							$(this).val(text);
						}
					})
					.bind("focusin",function(){
						if($(this).val()==text)
						{
							$(this).val("");
						}
					});
				}
			});
		};
	})(jQuery);
	//拖拽
	(function($){
		$.fn.draggable = function(fun,dragend,base){
			var obj = this;
			this.each(function(){
				$(this)
				.attr('draggable', 'true')
				.bind('dragstart', function (Event){
					if (!Event) Event = window.event;
					var dom = (typeof Event.target != "undefined")?Event.target:Event.srcElement;
					var dom = $(dom);
					if(typeof(fun)=="function")
					{
						var text = fun(Event,dom);
					}
					var dt = Event.originalEvent.dataTransfer;
					if(base) text = base6.encode(text);
					dt.setData("Text", text);
					return true;
				})
				.bind('dragend', function (Event){
					if (!Event) Event = window.event;
					var dom = (typeof Event.target != "undefined")?Event.target:Event.srcElement;
					var dom = $(dom);
					if(typeof(dragend)=="function")
					{
						dragend(Event,dom);
					}
					return false;
				});
			});
		};
	})(jQuery);	
	
	(function($){
		$.fn.YuanDrag = function(callback,func,alignment){
			var M = false;
			this.each(function(){
				this.posRange = {minX:0,minY:0,maxX:(document.compatMode == "CSS1Compat"?document.documentElement.clientWidth:document.body.clientWidth),maxY:(document.compatMode == "CSS1Compat"?document.documentElement.clientHeight:document.body.clientHeight)};
				this.onmousedown = function(e)
				{
					this.style.position = "absolute";
					this.drag(e,callback,func);
				};
				this.drag = function(e,callback,func)
				{
					var element = this,ev = e || window.event;
					ev.rScreenX = ev.screenX;
					ev.rScreenY = ev.screenY;
					var pos = $(this).offset();
					element.dragConfig = {defaultX : parseInt(pos.left,10),defaultY : parseInt((alignment?$(this).css("bottom").delpx():pos.top),10),defaultW: parseInt($(this).width(),10),defaultH : parseInt($(this).height(),10)};
					//alert($(this).css("bottom").delpx());
					var thiss = $(this);
					document.onmouseup = function(ev)
					{
						element.drop();
						if(M)
						{
							callback && callback(this);
							M = false;
						}
						return false;
					};
					document.onmousemove = function(e)
					{
						var ev2 = e || window.event;
						/*
						if($.browser.msie&& ev2.button!=1)
						{
							return (element.drop(),callback && callback());
						}
						*/
						var mx = element.dragConfig.defaultX + (ev2.screenX - ev.rScreenX);
						
						if(alignment)
						{
							var my = element.dragConfig.defaultY - (ev2.screenY - ev.rScreenY);
						}
						else
						{
							var my = element.dragConfig.defaultY + (ev2.screenY - ev.rScreenY);
						}
						var pr = element.posRange;
						var mw = element.dragConfig.defaultW;
						var mh = element.dragConfig.defaultH;
						with(element.style)
						{
							//left = (mx<pr.minX?pr.minX:((mx+mw)>pr.maxX?(pr.maxX-mw):mx)) + "px";
							//top = (my<pr.minY?pr.minY:((my+mh)>pr.maxY?(pr.maxY-mh):my)) + "px";
							left = mx + "px";
							if(alignment)
							{
								bottom = my + "px";
							}
							else
							{
								top = my + "px";
							}
						}
						M = true;
						func && func(this);
						return false;
					};
					document.onselectstart = function(){return false;};
				};
				this.drop = function()
				{
					document.onmousemove = document.onselectstart = document.onmouseup = null;
				};
			});
		};
		$.YuanDrag = true;
	})(jQuery);

	(function($){
		$.fn.YuanDrags = function(par){
			var M = false;
			this.each(function(){
				this.posRange = {minX:0,minY:0,maxX:(document.compatMode == "CSS1Compat"?document.documentElement.clientWidth:document.body.clientWidth),maxY:(document.compatMode == "CSS1Compat"?document.documentElement.clientHeight:document.body.clientHeight)};
				this.onmousedown = function(e)
				{
					this.style.position = "absolute";
					if(!par["drag"]||par["drag"](e,$(this)))
					{
						this.drag(e,par);
					}
				};
				this.drag = function(e,par)
				{
					var element = this,ev = e || window.event;
					ev.rScreenX = ev.screenX;
					ev.rScreenY = ev.screenY;
					var pos = $(this).offset();
					element.dragConfig = {defaultX : parseInt(pos.left,10),defaultY : parseInt((par["alignment"]?$(this).css("bottom").delpx():pos.top),10),defaultW: parseInt($(this).width(),10),defaultH : parseInt($(this).height(),10)};
					//alert($(this).css("bottom").delpx());
					var thiss = $(this);
					document.onmouseup = function(e)
					{
						var ev2 = e || window.event;
						element.drop();
						if(M)
						{
							par["up"] && par["up"](ev2,thiss);
							M = false;
						}
						else
						{
							par["ups"] && par["ups"](ev2,thiss);
						}
					};
					document.onmousemove = function(e)
					{
						var ev2 = e || window.event;
						/*
						if($.browser.msie&& ev2.button!=1)
						{
							return (element.drop(),callback && callback());
						}
						*/
						//$("#temp").html((ev2.screenX - ev.rScreenX) + " " + (ev2.screenY - ev.rScreenY));
						//console.log(element.dragConfig.defaultX + " " + element.dragConfig.defaultY);
						
						var S = (typeof(par["s"])=="function") ? (par["s"]() || 0) : ((typeof(par["s"])=="number") ? par["s"]*1 : 1);
						var mx = element.dragConfig.defaultX + (ev2.screenX - ev.rScreenX);
						if(par["alignment"])
						{
							var my = element.dragConfig.defaultY - (ev2.screenY - ev.rScreenY);
						}
						else
						{
							var my = element.dragConfig.defaultY + (ev2.screenY - ev.rScreenY);
						}
						var pr = element.posRange;
						var mw = element.dragConfig.defaultW;
						var mh = element.dragConfig.defaultH;
						mx += (typeof(par["x"])=="function") ? (par["x"]() || 0) : ((typeof(par["x"])=="number") ? par["x"]*1 : 0);
						my += (typeof(par["y"])=="function") ? (par["y"]() || 0) : ((typeof(par["y"])=="number") ? par["y"]*1 : 0);
						//console.log(S + " " + mx);
						mx = mx/S;
						my = my/S;
						//console.log(element.dragConfig.defaultX + " " + (ev2.screenX - ev.rScreenX) + " " + mx);
						with(element.style)
						{
							//left = (mx<pr.minX?pr.minX:((mx+mw)>pr.maxX?(pr.maxX-mw):mx)) + "px";
							//top = (my<pr.minY?pr.minY:((my+mh)>pr.maxY?(pr.maxY-mh):my)) + "px";
							left = mx + "px";
							if(par["alignment"])
							{
								bottom = my + "px";
							}
							else
							{
								top = my + "px";
							}
						}
						M = true;
						par["move"] && par["move"](ev2,thiss);
						return false;
					};
					document.onselectstart = function(){return false;};
				};
				this.drop = function()
				{
					document.onmousemove = document.onselectstart = document.onmouseup = null;
				};
			});
		};
	})(jQuery);


	(function($){
		$.fn.YDrags = function(par){
			var M = false;
			var clientY,clientX;
			this.each(function(){
				this.onmousedown = function(e)
				{
					clientY = e.clientY;
					clientX = e.clientX;
					if(par["drag"](e,clientX,clientY))
					this.drag(e,par);
				};
				this.drag = function(e,par)
				{
					var element = this,ev = e || window.event;
					ev.rScreenX = ev.screenX;
					ev.rScreenY = ev.screenY;
					document.onmouseup = function(e)
					{
						var ev2 = e || window.event;
						element.drop();
						if(M)
						{
							par["up"] && par["up"](e,e.clientY - clientY,e.clientX - clientX);
							M = false;
						}
					};
					document.onmousemove = function(e)
					{
						var ev2 = e || window.event;
						par["move"] && par["move"](e,ev2.screenX - ev.rScreenX,ev2.screenY - ev.rScreenY);
						M = true;
						return false;
					};
					document.onselectstart = function(){return false;};
				};
				this.drop = function()
				{
					document.onmousemove = document.onselectstart = document.onmouseup = null;
				};
			});
		};
	})(jQuery);
	//--------------------------------------------------
	//-------------------分页插件-----------------------
	(function($){
		$.fn.Pagination = function(options){
			var defaults = {
				pages: 1,//当前页
				pagesize: 10,//每页大小
				onclick : function(){},
				style : {
					"TEXT-ALIGN": "left",
					"font-family": "Verdana, '微软雅黑', 'Microsoft YaHei', Arial, Helvetica, sans-serif",
					"font-size": "12px",
					"padding": "0px",
					"margin-top": "3px",
					"margin-right": "3px",
					"margin-bottom": "3px",
					"margin-left": "0px",
					"cursor" : "pointer"
				},
				number : 6
			};
			var options = $.extend(defaults, options);
			var number5 = (defaults.number % 2)?defaults.number:defaults.number-1;
			var number1 = Math.floor(number5/2);
			var number2 = number1 + 1;
			var Previous,Next,DomKey;
			var pagehtml = function(dom)
			{
				DomKey = dom;
				if(defaults.pages<1) return false;
				var div = $('<div class="quotes" />'),a;
				div.css(defaults.style);
				if(defaults.pages==1)
				{
					div.append('<span class="disabled"> &lt; </span>');
					var Previous = false;
				}
				else
				{
					a = $('<a _i="' + (defaults.pages-1) + '"> &lt; </a>');
					Previous = a;
					a.bind("click",function(){click(this,dom)});
					div.append(a);
				}
				var Pages = Math.ceil((defaults.amount/defaults.pagesize));
				if(defaults.pages>Pages) return false;
				if(Pages<11)
				{
					for(var i=1; i<Pages+1; i++)
					{
						if(i==defaults.pages)
						{
							div.append('<span class="current">' + i + '</span>');
						}
						else
						{
							a = $('<a _i="' + i + '">' + i + '</a>');
							a.bind("click",function(){click(this,dom)});
							div.append(a);
						}
					}
				}
				else
				{
					if(defaults.pages<defaults.number)
					{
						for(var i=1; i<defaults.number+1; i++)
						{
							if(i==defaults.pages)
							{
								div.append('<span class="current">' + i + '</span>');
							}
							else
							{
								a = $('<a _i="' + i + '">' + i + '</a>');
								a.bind("click",function(){click(this,dom)});
								div.append(a);
							}
						}
						div.append('&#8226;&#8226;&#8226;');
						a = $('<a _i="' + (Pages-1) + '">' + (Pages-1) + '</a>');
						a.bind("click",function(){click(this,dom)});
						div.append(a);
						a = $('<a _i="' + (Pages) + '">' + (Pages) + '</a>');
						a.bind("click",function(){click(this,dom)});
						div.append(a);
					}
					else if(defaults.pages>(Pages-defaults.number))
					{
						a = $('<a _i="1">1</a>');
						a.bind("click",function(){click(this,dom)});
						div.append(a);
						a = $('<a _i="2">2</a>');
						a.bind("click",function(){click(this,dom)});
						div.append(a);
						div.append('&#8226;&#8226;&#8226;');
						
						for(var i=Pages-defaults.number; i<Pages+1; i++)
						{
							if(i==defaults.pages)
							{
								div.append('<span class="current">' + i + '</span>');
							}
							else
							{
								a = $('<a _i="' + i + '">' + i + '</a>');
								a.bind("click",function(){click(this,dom)});
								div.append(a);
							}
						}
					}
					else if(defaults.pages<(Pages-number5)&&defaults.pages>number5)
					{
						a = $('<a _i="1">1</a>');
						a.bind("click",function(){click(this,dom)});
						div.append(a);
						a = $('<a _i="2">2</a>');
						a.bind("click",function(){click(this,dom)});
						div.append(a);
						div.append('&#8226;&#8226;&#8226;');
						
						for(var i=(defaults.pages*1)-number1; i<(defaults.pages*1)+number2; i++)
						{
							if(i==defaults.pages*1)
							{
								div.append('<span class="current">' + i + '</span>');
							}
							else
							{
								a = $('<a _i="' + i + '">' + i + '</a>');
								a.bind("click",function(){click(this,dom)});
								div.append(a);
							}
						}
						
						div.append('&#8226;&#8226;&#8226;');
						a = $('<a _i="' + (Pages-1) + '">' + (Pages-1) + '</a>');
						a.bind("click",function(){click(this,dom)});
						div.append(a);
						a = $('<a _i="' + (Pages) + '">' + (Pages) + '</a>');
						a.bind("click",function(){click(this,dom)});
						div.append(a);
					}
				}
				
				if(defaults.pages==Pages)
				{
					div.append('<span class="disabled"> &gt; </span>');
					Next = false;
				}
				else
				{
					a = $('<a _i="' + (defaults.pages*1+1) + '"> &gt; </a>');
					var Next = a;
					a.bind("click",function(){click(this,dom)});
					div.append(a);
				}
				
				dom.html("");
				dom.append(div);
				/*
				$(window).bind("keydown",function(ev){
								if (!ev) ev = window.event;
								var keyCode = ev.keyCode;
								if(keyCode=="37")
								{
									Previous && Next && click(Previous,DomKey);
								}
								if(keyCode=="39")
								{
									Previous && Next && click(Next,DomKey);
								}
							}
						);
				*/
			};
			this.each(function(){
				pagehtml($(this));
			});
			
			//defaults.pages
			var click = function(dom,doms)
			{
				Previous = false;
				Next = false;
				defaults.pages = $(dom).attr("_i");
				defaults.onclick(defaults.pages,defaults.pagesize);
				pagehtml(doms);
			};
		};
	})(jQuery);

	//--------------------------------------------------
	//-------------------右键菜单-----------------------
	(function($){
		
		var MenuPool = {};
		var ShadowPool = {};
		var NowMenu;
		var OnMenu;
		$.fn.YuanMenu = function(options){
			var defaults = {
				menulist : [
					{
						icon		:	"/images/menu/hourglass.png",
						text		:	"重新载入程序",
						obj			:	function(){window.location.reload();},
						HotZone		:	{
											"default"	:	true,
											id			:	{},
											className	:	{}
										},
						son			:	null
					}
				],
				
				Only : {
					className : {},
					id : {temp:true}
				},
				eventPosX: 'pageX',
				eventPosY: 'pageY',
				shadow : true,
				onContextMenu: null,
				onShowMenu: null
				
			};
			
			var options = $.extend(defaults, options);
			
			this.each(function(){
				$(this).bind('contextmenu', function(e){
					// Check if onContextMenu() defined
					if (!e) e = window.event;
					var dom = (typeof e.target != "undefined")?e.target:e.srcElement;
					if(NowMenu)
					{
						NowMenu["menu"].hide();
					}
					NowMenu = GetMenuHtml(dom);
					var left,top;
					var width = NowMenu["menu"].width();
					var height = NowMenu["menu"].height();
					//左右显示判断
					if ($(document.body).width() - e[defaults.eventPosX] < width + 50)
					{
						left = e[defaults.eventPosX] - width;
					}
					else
					{
						left = e[defaults.eventPosX];
					}
					
					//上下显示判断
					if ($(document.body).height() - e[defaults.eventPosY] < height + 50)
					{
						top = (e[defaults.eventPosY] - height);
					}
					else
					{
						top = e[defaults.eventPosY];
					}

					NowMenu["menu"].css({'left':left + "px",'top':top + "px"}).fadeIn(100);
					//alert(NowMenu["menu"].html());
					if(typeof(defaults["menufun"])=="function")
					{
						defaults["menufun"](e);
					}
					e.preventDefault();
					return false;
				});
				$(document.body).bind('click', function(e){
					// Check if onContextMenu() defined
					if (!e) e = window.event;
					var dom = (typeof e.target != "undefined")?e.target:e.srcElement;
					if(NowMenu)
					{
						NowMenu["menu"].fadeOut(100);
						//NowMenu["shadow"].fadeOut(100);
					}
				});
				$(document.body).bind('mousedown', function(e){
					// Check if onContextMenu() defined
					if (!e) e = window.event;
					var dom = (typeof e.target != "undefined")?e.target:e.srcElement;
					if(NowMenu&&!OnMenu)
					{
						NowMenu["menu"].fadeOut(100);
						//NowMenu["shadow"].fadeOut(100);
					}
				});
			});
			
			function GetMenuHtml(dom)
			{
				dom = $(dom);
				
				if(!dom.attr("class")&&!dom.attr("id")&&!dom.attr("menutag"))
				{
					//default
					if(MenuPool["default"])
					{
						return ExMenu(MenuPool["default"],dom);
					}
					else
					{
						return ExMenu(SetMenuHtml(["default",null,dom]),dom);
					}
				}
				
				if(dom.attr("id"))
				{
					if(MenuPool["id"]&&MenuPool["id"][dom.attr("id")])
					{
						return ExMenu(MenuPool["id"][dom.attr("id")],dom);
					}
					else
					{
						if(isClassId({"id":dom.attr("id")}))
						{
							return ExMenu(SetMenuHtml(["id",dom.attr("id"),dom]),dom);
						}
					}
				}
				if(dom.attr("class"))
				{
					//default
					if(MenuPool["class"]&&MenuPool["class"][dom.attr("class")])
					{
						return ExMenu(MenuPool["class"][dom.attr("class")],dom);
					}
					else
					{
						if(isClassId({"class":dom.attr("class")}))
						{
							return ExMenu(SetMenuHtml(["class",dom.attr("class"),dom]),dom);
						}
					}
				}
				if(dom.attr("menutag"))
				{
					if(MenuPool["menutag"]&&MenuPool["menutag"][dom.attr("menutag")])
					{
						return ExMenu(MenuPool["menutag"][dom.attr("menutag")],dom);
					}
					else
					{
						if(isClassId({"menutag":dom.attr("menutag")}))
						{
							return ExMenu(SetMenuHtml(["menutag",dom.attr("menutag"),dom]),dom);
						}
					}
				}
				if(MenuPool["default"])
				{
					return ExMenu(MenuPool["default"],dom);
				}
				else
				{
					return ExMenu(SetMenuHtml(["default",null,dom]),dom);
				}
			}

			function ExMenu(menu,dom)
			{
				var I;
				for(var i=0; i<menu["menu"].find("li").length; i++)
				{
					I = $(menu["menu"].find("li")[i]).attr("_i");
					if((typeof(I)!="undefined"))
					{
						if(typeof(defaults.menulist[I]["return"])=="function")
						{
							if(defaults.menulist[I]["return"](dom))
							{
								$(menu["menu"].find("li")[i]).show();
							}
							else
							{
								$(menu["menu"].find("li")[i]).hide();
							}
						}
					}
				}
				return menu;
			}
			
			function SetMenuHtml(array)
			{
				//if(array[0]=="default")
				//{
					if(array[0]=="default")
					{
						MenuPool["default"] = {};
						var returnMenu = MenuPool["default"];
					}
					else if(array[0]=="id")
					{
						if(!MenuPool["id"]) MenuPool["id"] = {};
						MenuPool["id"][array[1]] = {};
						var returnMenu = MenuPool["id"][array[1]];
					}
					else if(array[0]=="class")
					{
						if(!MenuPool["class"]) MenuPool["class"] = {};
						MenuPool["class"][array[1]] = {};
						var returnMenu = MenuPool["class"][array[1]];
					}
					else if(array[0]=="menutag")
					{
						if(!MenuPool["menutag"]) MenuPool["menutag"] = {};
						MenuPool["menutag"][array[1]] = {};
						var returnMenu = MenuPool["menutag"][array[1]];
					}
					returnMenu["menu"] = {};
					returnMenu["menu"] = $('<div></div>')
						.hide()
						.css({position:'absolute', zIndex:'10000'})
						.hover(
							function(){OnMenu = true},
							function(){OnMenu = false}
						)
						.appendTo('body');
						
					var ul = $('<ul />')
						.appendTo(returnMenu["menu"])
						.attr({"class":"menuStyle"});
					var li,I=0;
					var uls,lis,son,shadow;
					var x = $.browser.msie?0:2;
					var n = $.browser.msie?24:22;
					var boo;
					for(var i=0; i<defaults.menulist.length; i++)
					{
						if(array[0]=="default")
						{
							boo = defaults.menulist[i]["HotZone"]["default"];
						}
						else if(array[0]=="id")
						{
							if(defaults.Only.id&&defaults.Only.id[array[1]])
							{
								boo = (defaults.menulist[i].HotZone.id&&defaults.menulist[i].HotZone.id[array[1]]);
							}
							else
							{
								boo = ((defaults.menulist[i].HotZone.id&&defaults.menulist[i].HotZone.id[array[1]]) || defaults.menulist[i]["HotZone"]["default"]);
							}
						}
						else if(array[0]=="class")
						{
							if(defaults.Only.className&&defaults.Only.className[array[1]])
							{
								boo = (defaults.menulist[i].HotZone.className&&defaults.menulist[i].HotZone.className[array[1]]);
							}
							else
							{
								boo = ((defaults.menulist[i].HotZone.className&&defaults.menulist[i].HotZone.className[array[1]]) || defaults.menulist[i]["HotZone"]["default"]);
							}
						}
						else if(array[0]=="menutag")
						{
							if(defaults.Only.menutag&&defaults.Only.menutag[array[1]])
							{
								boo = (defaults.menulist[i].HotZone.menutag&&defaults.menulist[i].HotZone.menutag[array[1]]);
							}
							else
							{
								boo = ((defaults.menulist[i].HotZone.menutag&&defaults.menulist[i].HotZone.menutag[array[1]]) || defaults.menulist[i]["HotZone"]["default"]);
							}
						}

						if(boo)
						{
							if(defaults.menulist[i]["cutoff"])
							{
								li = $('<li _i="' + (I++) + '" class="itemCutoff" _h="10" />')
								.appendTo(ul);
							}
							else
							{
								li = $('<li _i="' + (I++) + '" _h="22" />')
								.attr({"class":(defaults.menulist[i]["son"]?"itemStyle":"itemStyle")})
								.appendTo(ul)
								.bind('click', defaults.menulist[i]["obj"]?defaults.menulist[i]["obj"]:function(e){})
								.append('<span class="imgem">' + (defaults.menulist[i]["icon"]?'<img style="vertical-align: middle; padding-right: 3px;" src="' + defaults.menulist[i]["icon"] + '">':'') + '</span><span' + (defaults.menulist[i]["id"]?' id="' + defaults.menulist[i]["id"] + '"':'') + '>' + defaults.menulist[i]["text"] + '</span>');
								if(defaults.menulist[i]["son"])
								{
									li.append('<span class="sons"></span>');
								}
								if(defaults.menulist[i]["son"])
								{
									li.hover(
										function() {
											var dom = $(this);
											var topi = dom.attr("_i");
											var n = $.browser.msie?24:22;
											
											var top = (topi*n + x - ($.browser.msie?(topi-1)*2:0));
											var pul = dom.parents("ul");
											var top = 0;
											//alert(pul.children().length);
											for(var ii=0; ii<pul.children().length; ii++)
											{
												if(pul.children().eq(ii).attr("_i")==topi)
												{
													break;
												}
												else
												{
													if(pul.children().eq(ii).css("display")!="none")top += pul.children().eq(ii).attr("_h")*1;
												}
											}
											top = top + 3;
											var offset = NowMenu["menu"].offset();
											var W = (offset.left + dom.find('.son').width() + NowMenu["menu"].width());
											var H = (offset.top + dom.find('.son').height() + top);
											
											//左右显示判断
											if ($(document).width() < W)
											{
												left = (dom.find('.son').width() - 16)*-1;
												if(left*-1>offset.left)
												{
													left = offset.left * -1;
												}
											}
											else
											{
												left = (dom.find('.son').width() - 16);
											}
											
											//上下显示判断
											if ($(document).height() < H)
											{
												top = top - dom.find('.son').height() + n;
											}
											else
											{
												top = top;
											}
											
											var W = dom.find('.son').width();
											var H = dom.find('.son').height();
											dom.find('.son').css({left:left + "px",top:top + "px"});
											dom.find('.son').show();
										},
										function(){
											var dom = $(this);
											dom.find('.son').hide();
										}
									);
								}
								if(defaults.menulist[i]["son"])
								{
									son = $('<div class="son"></div>')
										.hide()
										.css({position:'absolute', zIndex:'10000'})
										.appendTo(li);
										
									uls = $('<ul />')
										.appendTo(son)
										.attr({"class":"menuStyle"});
										
									for(var j=0; j<defaults.menulist[i]["son"].length; j++)
									{
										if(array[0]=="default")
										{
											boo = defaults.menulist[i]["son"][j]["HotZone"]["default"];
										}
										else if(array[0]=="id")
										{
											boo = (defaults.menulist[i]["son"][j].HotZone.id&&defaults.menulist[i]["son"][j].HotZone.id[array[1]]) || defaults.menulist[i]["son"][j]["HotZone"]["default"];
										}
										else if(array[0]=="class")
										{
											boo = (defaults.menulist[i]["son"][j].HotZone.className&&defaults.menulist[i]["son"][j].HotZone.className[array[1]]) || defaults.menulist[i]["son"][j]["HotZone"]["default"];
										}
										else if(array[0]=="menutag")
										{
											boo = (defaults.menulist[i]["son"][j].HotZone.menutag&&defaults.menulist[i]["son"][j].HotZone.menutag[array[1]]) || defaults.menulist[i]["son"][j]["HotZone"]["default"];
										}
										if(boo)
										{
											if(defaults.menulist[i]["son"][j]["cutoff"])
											{
												li = $('<li _i="' + (I++) + '" class="itemCutoff" />')
												.appendTo(uls);
											}
											else
											{
												$('<li />')
												.attr({"class":"itemStyle"})
												.appendTo(uls)
												.bind('click', defaults.menulist[i]["son"][j]["obj"]?defaults.menulist[i]["son"][j]["obj"]:function(e){})
												.append('<span class="imgem">' + (defaults.menulist[i]["son"][j]["icon"]?'<img style="vertical-align: middle; padding-right: 3px;" src="' + defaults.menulist[i]["son"][j]["icon"] + '">':'') + '</span><span' + (defaults.menulist[i]["id"]?' id="' + defaults.menulist[i]["id"] + '"':'') + '>' + defaults.menulist[i]["son"][j]["text"] + '</span>');
											}
										}
									}
								}
							}
						}
					}
				//}
				return returnMenu;
			}
			
			function isClassId(array)
			{
				if(array["id"])
				{
					for(var i=0; i<defaults.menulist.length; i++)
					{
						if(!defaults.menulist[i].HotZone["default"])
						{
							if(defaults.menulist[i].HotZone.id&&defaults.menulist[i].HotZone.id[array["id"]]) return true;
						}
					}
				}
				if(array["class"])
				{
					for(var i=0; i<defaults.menulist.length; i++)
					{
						if(!defaults.menulist[i].HotZone["default"])
						{
							if(defaults.menulist[i].HotZone.className&&defaults.menulist[i].HotZone.className[array["class"]]) return true;
						}
					}
				}
				if(array["menutag"])
				{
					for(var i=0; i<defaults.menulist.length; i++)
					{
						if(!defaults.menulist[i].HotZone["default"])
						{
							if(defaults.menulist[i].HotZone.menutag&&defaults.menulist[i].HotZone.menutag[array["menutag"]]) return true;
						}
					}
				}
				return false;
			}
		};
		$.YuanMenu = true;
		if(typeof(window.MenuStart) == "function")
		{
			window.MenuStart();
		}
	})(jQuery);

	//--------------------------------------------------
	//-----------------html5拖拽上传--------------------
	(function ($) {
	
		$.fn.html5Uploader = function (options) {
			
			if(!Y.isMaster())
			{
				return false;
			}
			var crlf = '\r\n';
			var boundary = "iloveigloo";
			var dashes = "--";
			
			/*
			参数设定：
			name: 上传字段标示
			postUrl: 文件数据处理URL
			onClientAbort: 读取操作终止时调用
			onClientError: 出错时调用
			onClientLoad: 读取操作成功时调用
			onClientLoadEnd: 无论是否成功，读取完成时调用。通常在onload和onerror后调用
			onClientLoadStart: 读取将要开始时调用
			onClientProgress: 数据在读取过程中周期性调用
			onServerAbort: post操作结束时调用
			onServerError: 错误发生时调用
			onServerLoad: post操作成功时调用
			onServerLoadStart: post数据将要开始时调用
			onServerProgress: 数据正在被post的过程中周期性调用
			onServerReadyStateChange: 一个javascript功能对象无论任何时候readyState属性变化时调用。callback由用户界面现成调用。
			*/
			
			//var code = '{"d":"' + ud + '","sd":"' + Enter_object.loginarray["nowusers"]["usersystemdir"] + '","filename":"' + fromfile.fileName + '","member":"' + (Enter_object.loginarray["member"]&&Enter_object.loginarray["member"]["number"]?Enter_object.loginarray["member"]["number"]:"GuestAccount") + '","mkdirs":true,"class":"Html5upload","fun":"upload"}';
			
			//Y.JSON.encode(jsons)
			//Getapi() + "?code=" + base6.encode(code));
			var itop = 150;
			var settings = {
				"json": null,
				"name": "filedata",
				"upExt": "jpg,pdf,doc,xlsx,docx,csv,ppt,txt,mp3,png,rar",
				"postUrl": Getapi(),
				"amount": 8,
				"begin": function(dom){return true},
				"getpostUrl": null,
				"onClientAbort": null,
				"onClientError": null,
				"onClientLoad": null,
				"onClientLoadEnd": null,
				"onClientLoadStart": null,
				"onClientProgress": function(e, file){},
				"onServerAbort": function(){
					//alert("b");
				},
				"onServerError": function(){
					//alert("d");
				},
				"onServerLoad": function(e ,file,windows,filename){
					windows.windows.find('p[_name="percentage"]').html("100%");
					windows.windows.find('div[_name="schedules"]').css({width:"100%"});
					windows.windows.delay(500).fadeOut("slow",function(){windows.windows.remove();});
				},
				"onOk" : null,
				"onServerLoadStart": function(e ,file){
				},
				"onServerProgress": function(e ,file ,windows){
					var sPercent = Math.round((e.loaded * 100) / e.total)+'%';
					windows.windows.find('p[_name="percentage"]').html(sPercent);
					windows.windows.find('div[_name="schedules"]').css({width:sPercent});
				},
				"onServerReadyStateChange": null,
				"onSuccess": null
			};
			
			//var upExt = "jpg,jpeg,gif,png,pdf,doc,xlsx,docx,csv,ppt,txt,mp3,mpg,rar,zip";
			//var upExt = "jpg,pdf,doc,xlsx,docx,csv,ppt,txt,mp3,png,rar";
			//检查扩展名
			function checkFileExt(filename,limitExt)
			{
				if(limitExt=='*'||filename.match(new RegExp('\.('+limitExt.replace(/,/g,'|')+')$','i')))
				{
					return true;
				}
				else
				{
					return false;
				}
			}
			
			if (options) {
				$.extend(settings, options);
			}
			var OKi = 0;
			return this.each(function (options) {
				var $this = $(this);
				if ($this.is("[type=\"file\"]")) {
					$this.bind("change", function () {
						var files = this.files;
						for (var i = 0; i < files.length && i < settings.amount; i++) {
							fileHandler(files[i]);
						}
					});
				} else {
					$this.bind("dragenter dragover", function () {
						return false;
					}).bind("drop", function (e) {
						
						if (!e) e = window.event;
						var dom = (typeof e.target != "undefined")?e.target:e.srcElement;
						var dom = $(dom);
						var begin = (typeof(settings.begin)=="function") && settings.begin(dom);
						if(begin||!settings.begin)
						{
							var files = e.originalEvent.dataTransfer.files;
							itop = 150;
							OKi = 0;
							for (var i = 0; i < files.length && i < settings.amount; i++) {
								fileHandler(files[i],e,begin);
							}
						}
						return false;
					});
				}
			});
			
			function fileHandler(file,e,begin) {
				if(!checkFileExt(file.name,settings.upExt))
				{
					return false;
				}
				OKi++;

				var Fin = file.name.replace(/\s/gi,"_");
				var Fi = Fin.isDouName("-._");
				var Tya = Fin.split(".");
				var Ty = Tya[Tya.length - 1];
				if(!Fi||Fi==2)
				{
					var today = new Date();
					var member = Y.GetMember();
					var finame = (member["number"]||"GuestAccount") + "." + today.getTime() + "." + Ty;
					var Names = finame;
				}
				else
				{
					var Names = file.name;
				}
				//文件名合法性判断
				if(settings.getpostUrl)
				{
					var url = settings.getpostUrl(e,Names);
					if(!url) return false;
				}
				else if(settings.json)
				{
					settings.json["filename"] = Names;
					var url = Y.Getapi() + "?code=" + base6.encode(Y.JSON.encode(settings.json));
				}
				else
				{
					var url = settings.postUrl;
				}

				//弹出输入框----------------------------------------------------------------
				//--------------------------------------------------------------------------
				var json = {
					title : "正在上传" + file.name,
					info:[
						{
							type:"boxs",
							name:"schedule"
						},
						{
							type:"boxs",
							name:"percentage"
						}
					],
					ui : {
						opacity : 0.5,
						enter : false,
						close : true,
						left : "20px",
						top : (document.body.clientHeight - itop) + "px"
					}
				};
				itop = itop + 120;
				
				//进度窗口
				var promp = Y.UI.windows(json);
				promp.bind("esc","click",function(){promp.windows.remove();promp.Mask.remove();});
				promp.bind("enter","click",function(){
					promp.windows.remove();
					promp.Mask.remove();
					delete promp;
				});
				var schedule = $('<div _name="schedules" style="background-color: #0099FF;height: 20px;width:1%;"></div>');
				promp.windows.find('p[_name="schedule"]').append(schedule);
				//--------------------------------------------------------------------------
				var fileReader = new FileReader();
				fileReader.onabort = function (e) {
					if (settings.onClientAbort) {
						settings.onClientAbort(e, file, begin);
					}
				};
				fileReader.onerror = function (e) {
					if (settings.onClientError) {
						settings.onClientError(e, file, begin);
					}
				};
				fileReader.onload = function (e) {
					if (settings.onClientLoad) {
						settings.onClientLoad(e, file, begin);
					}
				};
				fileReader.onloadend = function (e) {
					if (settings.onClientLoadEnd) {
						settings.onClientLoadEnd(e, file, begin);
					}
				};
				fileReader.onloadstart = function (e) {
					if (settings.onClientLoadStart) {
						settings.onClientLoadStart(e, file, begin);
					}
				};
				fileReader.onprogress = function (e) {
					if (settings.onClientProgress) {
						settings.onClientProgress(e, file, begin);
					}
				};
				fileReader.readAsDataURL(file);

				var xmlHttpRequest = new XMLHttpRequest();
				xmlHttpRequest.upload.onabort = function (e) {
					if (settings.onServerAbort) {
						settings.onServerAbort(e, file, begin);
					}
				};
				xmlHttpRequest.upload.onerror = function (e) {
					if (settings.onServerError) {
						settings.onServerError(e, file, begin);
					}
				};
				xmlHttpRequest.upload.onload = function (e) {
					if (settings.onServerLoad) {
						settings.onServerLoad(e, file, promp, Names, begin);
					}
					OKi--;
					if(OKi==0)
					{
						if (settings.onOk) {
							settings.onOk(begin);
						}
					}
				};
				xmlHttpRequest.upload.onloadstart = function (e) {
					if (settings.onServerLoadStart) {
						settings.onServerLoadStart(e, file, begin);
					}
				};
				xmlHttpRequest.upload.onprogress = function (e) {
					if (settings.onServerProgress) {
						settings.onServerProgress(e, file, promp, begin);
					}
				};
				xmlHttpRequest.onreadystatechange = function (e) {
					if (settings.onServerReadyStateChange) {
						settings.onServerReadyStateChange(e, file, xmlHttpRequest.readyState, begin);
					}
					if (settings.onSuccess && xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) {
						settings.onSuccess(e, file, xmlHttpRequest.responseText, begin);
					}
				};

				xmlHttpRequest.open("POST", url, true);

				if (file.getAsBinary) { // Firefox
					var data = dashes + boundary + crlf +
						"Content-Disposition: form-data;" +
						"name=\"" + settings.name + "\";" +
						"filename=\"" + unescape(encodeURIComponent(file.name)) + "\"" + crlf +
						"Content-Type: application/octet-stream" + crlf + crlf +
						file.getAsBinary() + crlf +
						dashes + boundary + dashes;

					xmlHttpRequest.setRequestHeader("Content-Type", "multipart/form-data;boundary=" + boundary);
					xmlHttpRequest.sendAsBinary(data);

				} else if (window.FormData) { // Chrome

					var formData = new FormData();
					formData.append(settings.name, file);

					xmlHttpRequest.send(formData);

				}
			}
			
		};
		
	})(jQuery);
	//--------------------------------------------------

	//------------------------------------------------------------------------------------------------------------------------------------
	//fn----------------------------------------------------------------------------------------------------------------------------------
	Y.fn = {};
	var GetClipboard = Y.fn.GetClipboard = function()
	{
		if (window.clipboardData) 
		{
			return (window.clipboardData.getData('text'));
		}
		else 
		{
			if (window.netscape) 
			{
				try 
				{
					netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
					var clip = Components.classes["@mozilla.org/widget/clipboard;1"].createInstance(Components.interfaces.nsIClipboard);
					if (!clip) 
					{
						return;
					}
					var trans = Components.classes["@mozilla.org/widget/transferable;1"].createInstance(Components.interfaces.nsITransferable);
					if (!trans) 
					{
						return;
					}
					trans.addDataFlavor("text/unicode");
					clip.getData(trans, clip.kGlobalClipboard);
					var str = new Object();
					var len = new Object();
					trans.getTransferData("text/unicode", str, len);
				}
				catch (e) 
				{
					alert("您的firefox安全限制限制您进行剪贴板操作，请打开'about:config'将signed.applets.codebase_principal_support'设置为true'之后重试，相对路径为firefox根目录/greprefs/all.js");
					return null;
				}
				if (str) 
				{
					if (Components.interfaces.nsISupportsWString) 
					{
						str = str.value.QueryInterface(Components.interfaces.nsISupportsWString);
					} 
					else 
					{
						if (Components.interfaces.nsISupportsString) 
						{
							str = str.value.QueryInterface(Components.interfaces.nsISupportsString);
						} 
						else 
						{
							str = null;
						}
					}
				}
				if (str) 
				{
					return (str.data.substring(0, len.value / 2));
				}
			}
		}
		return null;
	};
	Y.Paste = function(par)
	{
		$(window).bind("keydown",function(ev){
				if (!ev) ev = window.event;
				var keyCode = ev.keyCode;
				if(keyCode=="32"||keyCode=="37"||keyCode=="38"||keyCode=="39"||keyCode=="40")
				{
					return false;
				}
				if(ev.ctrlKey&&keyCode=="86")
				{
					if(document.activeElement.tagName!="INPUT")
					{
						var text = Y.fn.GetClipboard();
						(typeof(par["fun"])=="function") && par["fun"](text);
						ev.stopPropagation();
					}
				}
			}
		);
	};
	//------------------------------------------------------------------------------------------------------------------------------------

	Y.Tween = {
		Linear: function(t,b,c,d){ return c*t/d + b; },
		Quad: {
			easeIn: function(t,b,c,d){
				return c*(t/=d)*t + b;
			},
			easeOut: function(t,b,c,d){
				return -c *(t/=d)*(t-2) + b;
			},
			easeInOut: function(t,b,c,d){
				if ((t/=d/2) < 1) return c/2*t*t + b;
				return -c/2 * ((--t)*(t-2) - 1) + b;
			}
		},
		Cubic: {
			easeIn: function(t,b,c,d){
				return c*(t/=d)*t*t + b;
			},
			easeOut: function(t,b,c,d){
				return c*((t=t/d-1)*t*t + 1) + b;
			},
			easeInOut: function(t,b,c,d){
				if ((t/=d/2) < 1) return c/2*t*t*t + b;
				return c/2*((t-=2)*t*t + 2) + b;
			}
		},
		Quart: {
			easeIn: function(t,b,c,d){
				return c*(t/=d)*t*t*t + b;
			},
			easeOut: function(t,b,c,d){
				return -c * ((t=t/d-1)*t*t*t - 1) + b;
			},
			easeInOut: function(t,b,c,d){
				if ((t/=d/2) < 1) return c/2*t*t*t*t + b;
				return -c/2 * ((t-=2)*t*t*t - 2) + b;
			}
		},
		Quint: {
			easeIn: function(t,b,c,d){
				return c*(t/=d)*t*t*t*t + b;
			},
			easeOut: function(t,b,c,d){
				return c*((t=t/d-1)*t*t*t*t + 1) + b;
			},
			easeInOut: function(t,b,c,d){
				if ((t/=d/2) < 1) return c/2*t*t*t*t*t + b;
				return c/2*((t-=2)*t*t*t*t + 2) + b;
			}
		},
		Sine: {
			easeIn: function(t,b,c,d){
				return -c * Math.cos(t/d * (Math.PI/2)) + c + b;
			},
			easeOut: function(t,b,c,d){
				return c * Math.sin(t/d * (Math.PI/2)) + b;
			},
			easeInOut: function(t,b,c,d){
				return -c/2 * (Math.cos(Math.PI*t/d) - 1) + b;
			}
		},
		Expo: {
			easeIn: function(t,b,c,d){
				return (t==0) ? b : c * Math.pow(2, 10 * (t/d - 1)) + b;
			},
			easeOut: function(t,b,c,d){
				return (t==d) ? b+c : c * (-Math.pow(2, -10 * t/d) + 1) + b;
			},
			easeInOut: function(t,b,c,d){
				if (t==0) return b;
				if (t==d) return b+c;
				if ((t/=d/2) < 1) return c/2 * Math.pow(2, 10 * (t - 1)) + b;
				return c/2 * (-Math.pow(2, -10 * --t) + 2) + b;
			}
		},
		Circ: {
			easeIn: function(t,b,c,d){
				return -c * (Math.sqrt(1 - (t/=d)*t) - 1) + b;
			},
			easeOut: function(t,b,c,d){
				return c * Math.sqrt(1 - (t=t/d-1)*t) + b;
			},
			easeInOut: function(t,b,c,d){
				if ((t/=d/2) < 1) return -c/2 * (Math.sqrt(1 - t*t) - 1) + b;
				return c/2 * (Math.sqrt(1 - (t-=2)*t) + 1) + b;
			}
		},
		Elastic: {
			easeIn: function(t,b,c,d,a,p){
				if (t==0) return b;  if ((t/=d)==1) return b+c;  if (!p) p=d*.3;
				if (!a || a < Math.abs(c)) { a=c; var s=p/4; }
				else var s = p/(2*Math.PI) * Math.asin (c/a);
				return -(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b;
			},
			easeOut: function(t,b,c,d,a,p){
				if (t==0) return b;  if ((t/=d)==1) return b+c;  if (!p) p=d*.3;
				if (!a || a < Math.abs(c)) { a=c; var s=p/4; }
				else var s = p/(2*Math.PI) * Math.asin (c/a);
				return (a*Math.pow(2,-10*t) * Math.sin( (t*d-s)*(2*Math.PI)/p ) + c + b);
			},
			easeInOut: function(t,b,c,d,a,p){
				if (t==0) return b;  if ((t/=d/2)==2) return b+c;  if (!p) p=d*(.3*1.5);
				if (!a || a < Math.abs(c)) { a=c; var s=p/4; }
				else var s = p/(2*Math.PI) * Math.asin (c/a);
				if (t < 1) return -.5*(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b;
				return a*Math.pow(2,-10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )*.5 + c + b;
			}
		},
		Back: {
			easeIn: function(t,b,c,d,s){
				if (s == undefined) s = 1.70158;
				return c*(t/=d)*t*((s+1)*t - s) + b;
			},
			easeOut: function(t,b,c,d,s){
				if (s == undefined) s = 1.70158;
				return c*((t=t/d-1)*t*((s+1)*t + s) + 1) + b;
			},
			easeInOut: function(t,b,c,d,s){
				if (s == undefined) s = 1.70158; 
				if ((t/=d/2) < 1) return c/2*(t*t*(((s*=(1.525))+1)*t - s)) + b;
				return c/2*((t-=2)*t*(((s*=(1.525))+1)*t + s) + 2) + b;
			}
		},
		Bounce: {
			easeIn: function(t,b,c,d){
				return c - Tween.Bounce.easeOut(d-t, 0, c, d) + b;
			},
			easeOut: function(t,b,c,d){
				if ((t/=d) < (1/2.75)) {
					return c*(7.5625*t*t) + b;
				} else if (t < (2/2.75)) {
					return c*(7.5625*(t-=(1.5/2.75))*t + .75) + b;
				} else if (t < (2.5/2.75)) {
					return c*(7.5625*(t-=(2.25/2.75))*t + .9375) + b;
				} else {
					return c*(7.5625*(t-=(2.625/2.75))*t + .984375) + b;
				}
			},
			easeInOut: function(t,b,c,d){
				if (t < d/2) return Tween.Bounce.easeIn(t*2, 0, c, d) * .5 + b;
				else return Tween.Bounce.easeOut(t*2-d, 0, c, d) * .5 + c*.5 + b;
			}
		}
	};

	/*
	* 移动浏览器版本信息:
	*/

	Y.browser = {
		versions:function(){ 
			var u = navigator.userAgent, app = navigator.appVersion; 
			return {//移动终端浏览器版本信息 
				trident: u.indexOf('Trident') > -1, //IE内核
				presto: u.indexOf('Presto') > -1, //opera内核
				webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核
				gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1, //火狐内核
				mobile: !!u.match(/AppleWebKit.*Mobile.*/)||!!u.match(/AppleWebKit/), //是否为移动终端
				ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
				android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1, //android终端或者uc浏览器
				iPhone: u.indexOf('iPhone') > -1 || u.indexOf('Mac') > -1, //是否为iPhone或者QQHD浏览器
				iPad: u.indexOf('iPad') > -1, //是否iPad
				webApp: u.indexOf('Safari') == -1 //是否web应该程序，没有头部与底部
			};
		}(),
		language:(navigator.browserLanguage || navigator.language).toLowerCase()
	};

	Y.keydown = function(json){
		$(window).bind("keydown",function(ev){
			if (!ev) ev = window.event;
			var keyCode = ev.charCode || ev.keyCode || ev.which;
			try
			{
				(typeof(json[keyCode])=="function") && json[keyCode]();
			}
			catch(e){
				;
			}
		});
	};

})(window);




if (typeof _PURL == 'undefined')  
{  
	var _PURL = {};  
}
_PURL.URLParser = function(url) {  

	this._fields = {  
		'Username' : 4,   
		'Password' : 5,   
		'Port' : 7,   
		'Protocol' : 2,   
		'Host' : 6,   
		'Pathname' : 8,   
		'URL' : 0,   
		'Querystring' : 9,   
		'Fragment' : 10  
	};  

	this._values = {};  
	this._regex = null;  
	this.version = 0.1;  
	this._regex = /^((\w+):\/\/)?((\w+):?(\w+)?@)?([^\/\?:]+):?(\d+)?(\/?[^\?#]+)?\??([^#]+)?#?(\w*)/;
	for(var f in this._fields)  
	{  
		this['get' + f] = this._makeGetter(f);  
	}  

	if (typeof url != 'undefined')  
	{  
		this._parse(url);  
	}  
};
_PURL.URLParser.prototype.setURL = function(url) {  
	this._parse(url);
};

_PURL.URLParser.prototype._initValues = function() {
	for(var f in this._fields)
	{
		this._values[f] = '';
	}
};

_PURL.URLParser.prototype._parse = function(url) {
	this._initValues();
	var r = this._regex.exec(url);
	if (!r) throw "DPURLParser::_parse -> Invalid URL";

	for(var f in this._fields) if (typeof r[this._fields[f]] != 'undefined')
	{
		this._values[f] = r[this._fields[f]];
	}
};

_PURL.URLParser.prototype._makeGetter = function(field) {  
	return function() {
		return this._values[field];
	}
};