py_mirai_version = 4 # 在这里改版本号哦！3或者4

ASK_TRIGGER = [
	r'\?',
	r'\？',
	r'\¿',
	r'吗',
	r'啥',
	r'怎么',
	r'如何',
	r'i宝',
	r'为什么',
]

randomStrLength = 4
pingCtr = 0


AtCoderHeaders = {
	"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"accept-encoding":"gzip, deflate, br",
	"accept-language":"zh-CN,zh;q=0.9",
	"cache-control":"no-cache",
	"dnt":"1",
	"pragma":"no-cache",
	"upgrade-insecure-requests":"1",
	"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}



QQFaces = {
	"unknown": 0xff,
	"jingya": 0,
	"piezui": 1,
	"se": 2,
	"fadai": 3,
	"deyi": 4,
	"liulei": 5,
	"haixiu": 6,
	"bizui": 7,
	"shui": 8,
	"daku": 9,
	"ganga": 10,
	"fanu": 11,
	"tiaopi": 12,
	"ciya": 13,
	"weixiao": 14,
	"nanguo": 15,
	"ku": 16,
	"zhuakuang": 18,
	"tu": 19,
	"touxiao": 20,
	"keai": 21,
	"baiyan": 22,
	"aoman": 23,
	"ji_e": 24,
	"kun": 25,
	"jingkong": 26,
	"liuhan": 27,
	"hanxiao": 28,
	"dabing": 29,
	"fendou": 30,
	"zhouma": 31,
	"yiwen": 32,
	"yun": 34,
	"zhemo": 35,
	"shuai": 36,
	"kulou": 37,
	"qiaoda": 38,
	"zaijian": 39,
	"fadou": 41,
	"aiqing": 42,
	"tiaotiao": 43,
	"zhutou": 46,
	"yongbao": 49,
	"dan_gao": 53,
	"shandian": 54,
	"zhadan": 55,
	"dao": 56,
	"zuqiu": 57,
	"bianbian": 59,
	"kafei": 60,
	"fan": 61,
	"meigui": 63,
	"diaoxie": 64,
	"aixin": 66,
	"xinsui": 67,
	"liwu": 69,
	"taiyang": 74,
	"yueliang": 75,
	"qiang": 76,
	"ruo": 77,
	"woshou": 78,
	"shengli": 79,
	"feiwen": 85,
	"naohuo": 86,
	"xigua": 89,
	"lenghan": 96,
	"cahan": 97,
	"koubi": 98,
	"guzhang": 99,
	"qiudale": 100,
	"huaixiao": 101,
	"zuohengheng": 102,
	"youhengheng": 103,
	"haqian": 104,
	"bishi": 105,
	"weiqu": 106,
	"kuaikule": 107,
	"yinxian": 108,
	"qinqin": 109,
	"xia": 110,
	"kelian": 111,
	"caidao": 112,
	"pijiu": 113,
	"lanqiu": 114,
	"pingpang": 115,
	"shiai": 116,
	"piaochong": 117,
	"baoquan": 118,
	"gouyin": 119,
	"quantou": 120,
	"chajin": 121,
	"aini": 122,
	"bu": 123,
	"hao": 124,
	"zhuanquan": 125,
	"ketou": 126,
	"huitou": 127,
	"tiaosheng": 128,
	"huishou": 129,
	"jidong": 130,
	"jiewu": 131,
	"xianwen": 132,
	"zuotaiji": 133,
	"youtaiji": 134,
	"shuangxi": 136,
	"bianpao": 137,
	"denglong": 138,
	"facai": 139,
	"K_ge": 140,
	"gouwu": 141,
	"youjian": 142,
	"shuai_qi": 143,
	"hecai": 144,
	"qidao": 145,
	"baojin": 146,
	"bangbangtang": 147,
	"he_nai": 148,
	"xiamian": 149,
	"xiangjiao": 150,
	"feiji": 151,
	"kaiche": 152,
	"gaotiezuochetou": 153,
	"chexiang": 154,
	"gaotieyouchetou": 155,
	"duoyun": 156,
	"xiayu": 157,
	"chaopiao": 158,
	"xiongmao": 159,
	"dengpao": 160,
	"fengche": 161,
	"naozhong": 162,
	"dasan": 163,
	"caiqiu": 164,
	"zuanjie": 165,
	"shafa": 166,
	"zhijin": 167,
	"yao": 168,
	"shouqiang": 169,
	"qingwa": 170,
	"cha": 171,
	"zhayan": 172,
	"leibeng": 173,
	"wunai": 174,
	"maimeng": 175,
	"xiaojiujie": 176,
	"penxue": 177,
	"xieyanxiao": 178,
	"dog": 179,
	"jinxi": 180,
	"saorao": 181,
	"xiaoku": 182,
	"wozuimei": 183,
	"hexie": 184,
	"yangtuo": 185,
	"banli": 186,
	"youling": 187,
	"dan": 188,
	"mofang": 189,
	"juhua": 190,
	"feizao": 191,
	"hongbao": 192,
	"daxiao": 193,
	"bukaixin": 194,
	"zhenjing": 195,
	"ganga": 196,
	"lenmo": 197,
	"ye": 198,
	"haobang": 199,
	"baituo": 200,
	"dianzan": 201,
	"wuliao": 202,
	"tuolian": 203,
	"chi": 204,
	"songhua": 205,
	"haipa": 206,
	"huachi": 207,
	"xiaoyang": 208,
	"unknown2": 209,#暂时不知道
	"biaolei": 210,
	"wobukan": 211,
	"tuosai": 212,
	"unknown3": 213,#暂时不知道
	#214-247表情在电脑版qq9.2.3无法显示
	"bobo": 214,
	"hulian": 215,
	"paitou": 216,
	"cheyiche": 217,
	"tianyitian": 218,
	"cengyiceng": 219,
	"zhaozhatian": 220,
	"dingguagua": 221,
	"baobao": 222,
	"baoji": 223,
	"kaiqiang": 224,
	"liaoyiliao": 225,
	"paizhuo": 226,
	"paishou": 227,
	"gongxi": 228,
	"ganbei": 229,
	"chaofeng": 230,
	"hen": 231,
	"foxi": 232,
	"jingdai": 234,
	"chandou": 235,
	"jiaotou": 236,
	"toukan": 237,
	"shanlian": 238,
	"yuanliang": 239,
	"penlian": 240,
	"shengrikuaile": 241,
	"touzhuangji": 242,
	"shuaitou": 243,
	"renggou": 244,
	"jiayoubisheng": 245,
	"jiayoubaobao": 246,
	"kouzhaohuti": 247,
	#248-255未定义
	"jinya": 256,
	"piezei": 257,
	"se": 258,
	"fadai": 259,
	"deyi": 260,
	"liulei": 261,
	"haixiu": 262,
	"bizui": 263,
	"shui": 264,
	"daku": 265,
	"ganga": 266,
	"falu": 267,
	"tiaopi": 268,
	"ziya": 269,
	"weixiao": 270,
	"nanguo": 271,
	"ku": 272,
	"unknown4": 273,#暂时不知道,qq安卓版本8.2.8.4440不显示
	"zhuakuang": 274,
	"tu": 275,
	"touxiao": 276,
	"keai": 277,
	"baiyan": 278,
	"aoman": 279,
	"jie": 280,
	"kun": 281,
	"jingkong": 282,
	"liuhan": 283,
	"hanxiao": 284,
	"dabing": 285,
	"fendou": 286,
	"zhouma": 287,
	"yiwen": 288,
	"xu": 289,
	"yun": 290,
	"zhemo": 291,
	"shuai": 292,
	"kulou": 293,
	"qiaoda": 294,
	"zaijian": 295,
	"unknown5": 296,#安卓版本无显示
	"dadou": 297,
	"aiqing": 298,
	"tiaotiao": 299,
	"unknown6": 300,#暂时不知道
	"unknown7": 301,#暂时不知道
	"zhutou": 302,
	"mao": 303,
	"unknown8": 304,#暂时不知道
	"baobao": 305,
	"meiyuanfuhao": 306,
	"dengpao": 307,#安卓版本不显示
	"gaijiaobei": 308,#安卓版本不显示
	"dangao": 309,
	"shandian": 310,
	"zhadan": 311,
	"shiai": 321,
	"aixin": 322,
	"xinsui": 323,
	"zhuozi": 324,#安卓qq不显示
	"liwu": 325,
}


subscribes = ('S','sub','subscribe','订阅','推送','push','enable')
unsubscribes = ('unsubscribe','cancel','td','TD','reset','stop','黙れ', '闭嘴', 'damare', 'E', 'yamero', '停','disable','clear', 'bye')


chat_log = {}
credit_cmds = {}
credit_operators = ('+', '-', '*', '//', '**', '<<', '>>', '&', '|', '^', '%')
credit_operators_weight = (0.7, 0.08, 0.07, 0.03, 0.02, 0.02, 0.02, 0.02, 0.017, 0.01, 0.003)

