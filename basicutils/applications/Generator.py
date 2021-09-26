"""生成器类"""
import enum
import os
import sys

if os.getcwd() not in sys.path:
	sys.path.append(os.getcwd())
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
import re
import asyncio
import random
from basicutils import CONST as GLOBAL
from basicutils.chain import *
from basicutils.network import *
from basicutils.task import *

def 不会吧(ent: CoreEntity):
	"""#不会吧 []
	不会吧生成器，例：#不会吧 在会谈时脱出来"""
	return [Plain(f'不会真的有人{ent.chain.tostr()}吧？不会吧不会吧？')]

def 营销生成器(ent: CoreEntity):
	"""#营销 []
	营销号生成器，格式：#营销 <主题> <事件> <另一种说法>
	"""
	attrs = ent.chain.tostr().split(' ')
	subject = attrs[0]
	event = attrs[1]
	event2 = attrs[2]
	synthesis = f'''{subject}{event}是怎么回事呢？{subject}相信大家都很熟悉，但是{subject}{event}是怎么回事呢，下面就让小编带大家一起了解吧。\r\n{subject}{event}，其实就是{event2}，大家可能会很惊讶{subject}怎么会{event}呢？但事实就是这样，小编也感到非常惊讶。\r\n这就是关于{subject}{event}的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！'''
	return [Plain(synthesis)]


def 同学你好生成器(ent: CoreEntity):
	"""#同学 []
	同学你好生成器，格式：#同学 <群名> <这个群教什么东西>
	"""
	attrs = ent.chain.tostr().split(' ')
	if len(attrs)==1:
		ato = attrs[0]
		subject = '直播学习'
	elif len(attrs)>1:
		subject = attrs[0]
		ato = ' '.join(attrs[1:])
	else:
		return [Plain('参数不足，用法：【可选的群名】 【必选的教什么东西】')]
	pattern1 = ['同学你好','你好呀']
	synthesis = f'''{random.choice(pattern1)}，就是我建了个{subject}群，教{ato}等滴不用拉人和宣传，有兴趣学下的话给你群号阔以吧？'''
	return [Plain(synthesis)]

恶臭字典 = {
	114514: "114514",
	58596: "114*514",
	49654: "11*4514",
	45804: "11451*4",
	23256: "114*51*4",
	22616: "11*4*514",
	19844: "11*451*4",
	16030: "1145*14",
	14515: "1+14514",
	14514: "1*14514",
	14513: "-1+14514",
	11455: "11451+4",
	11447: "11451-4",
	9028: "(1+1)*4514",
	8976: "11*4*51*4",
	7980: "114*5*14",
	7710: "(1+14)*514",
	7197: "1+14*514",
	7196: "1*14*514",
	7195: "-1+14*514",
	6930: "11*45*14",
	6682: "(1-14)*-514",
	6270: "114*(51+4)",
	5818: "114*51+4",
	5810: "114*51-4",
	5808: "(1+1451)*4",
	5805: "1+1451*4",
	5804: "1*1451*4",
	5803: "-1+1451*4",
	5800: "(1-1451)*-4",
	5725: "1145*(1+4)",
	5698: "11*(4+514)",
	5610: "-11*(4-514)",
	5358: "114*(51-4)",
	5005: "11*(451+4)",
	4965: "11*451+4",
	4957: "11*451-4",
	4917: "11*(451-4)",
	4584: "(1145+1)*4",
	4580: "1145*1*4",
	4576: "(1145-1)*4",
	4525: "11+4514",
	4516: "1+1+4514",
	4515: "1+1*4514",
	4514: "1-1+4514",
	4513: "-1*1+4514",
	4512: "-1-1+4514",
	4503: "-11+4514",
	4112: "(1+1)*4*514",
	3608: "(1+1)*451*4",
	3598: "(11-4)*514",
	3435: "-1145*(1-4)",
	3080: "11*4*5*14",
	3060: "(11+4)*51*4",
	2857: "1+14*51*4",
	2856: "1*14*51*4",
	2855: "-1+14*51*4",
	2850: "114*5*(1+4)",
	2736: "114*(5+1)*4",
	2652: "(1-14)*51*-4",
	2570: "1*(1+4)*514",
	2475: "11*45*(1+4)",
	2420: "11*4*(51+4)",
	2280: "114*5*1*4",
	2248: "11*4*51+4",
	2240: "11*4*51-4",
	2166: "114*(5+14)",
	2068: "11*4*(51-4)",
	2067: "11+4*514",
	2058: "1+1+4*514",
	2057: "1/1+4*514",
	2056: "1/1*4*514",
	2055: "-1/1+4*514",
	2054: "-1-1+4*514",
	2045: "-11+4*514",
	2044: "(1+145)*14",
	2031: "1+145*14",
	2030: "1*145*14",
	2029: "-1+145*14",
	2024: "11*(45+1)*4",
	2016: "-(1-145)*14",
	1980: "11*45*1*4",
	1936: "11*(45-1)*4",
	1848: "(11+451)*4",
	1824: "114*(5-1)*4",
	1815: "11+451*4",
	1808: "1*(1+451)*4",
	1806: "1+1+451*4",
	1805: "1+1*451*4",
	1804: "1-1+451*4",
	1803: "1*-1+451*4",
	1802: "-1-1+451*4",
	1800: "1*-(1-451)*4",
	1793: "-11+451*4",
	1760: "-(11-451)*4",
	1710: "114*-5*(1-4)",
	1666: "(114+5)*14",
	1632: "(1+1)*4*51*4",
	1542: "1*-(1-4)*514",
	1526: "(114-5)*14",
	1485: "11*-45*(1-4)",
	1456: "1+1451+4",
	1455: "1*1451+4",
	1454: "-1+1451+4",
	1448: "1+1451-4",
	1447: "1*1451-4",
	1446: "-1+1451-4",
	1428: "(11-4)*51*4",
	1386: "11*(4+5)*14",
	1260: "(1+1)*45*14",
	1159: "1145+14",
	1150: "1145+1+4",
	1149: "1145+1*4",
	1148: "1145-1+4",
	1142: "1145+1-4",
	1141: "1145-1*4",
	1140: "(1145-1)-4",
	1131: "1145-14",
	1100: "11*4*5*(1+4)",
	1056: "11*4*(5+1)*4",
	1050: "(11+4)*5*14",
	1036: "(1+1)*(4+514)",
	1026: "114*-(5-14)",
	1020: "1*(1+4)*51*4",
	981: "1+14*5*14",
	980: "1*14*5*14",
	979: "-1+14*5*14",
	910: "-(1-14)*5*14",
	906: "(1+1)*451+4",
	898: "(1+1)*451-4",
	894: "(1+1)*(451-4)",
	880: "11*4*5*1*4",
	836: "11*4*(5+14)",
	827: "11+4*51*4",
	825: "(11+4)*(51+4)",
	818: "1+1+4*51*4",
	817: "1*1+4*51*4",
	816: "1*1*4*51*4",
	815: "-1+1*4*51*4",
	814: "-1-1+4*51*4",
	805: "-11+4*51*4",
	784: "(11+45)*14",
	771: "1+14*(51+4)",
	770: "1*14*(51+4)",
	769: "(11+4)*51+4",
	761: "(1+14)*51-4",
	730: "(1+145)*(1+4)",
	726: "1+145*(1+4)",
	725: "1*145*(1+4)",
	724: "-1-145*-(1+4)",
	720: "(1-145)*-(1+4)",
	719: "1+14*51+4",
	718: "1*14*51+4",
	717: "-1-14*-51+4",
	715: "(1-14)*-(51+4)",
	711: "1+14*51-4",
	710: "1*14*51-4",
	709: "-1+14*51-4",
	705: "(1+14)*(51-4)",
	704: "11*4*(5-1)*4",
	688: "114*(5+1)+4",
	680: "114*(5+1)-4",
	667: "-(1-14)*51+4",
	660: "(114+51)*4",
	659: "1+14*(51-4)",
	658: "1*14*(51-4)",
	657: "-1+14*(51-4)",
	649: "11*(45+14)",
	644: "1*(1+45)*14",
	641: "11+45*14",
	632: "1+1+45*14",
	631: "1*1+45*14",
	630: "1*1*45*14",
	629: "1*-1+45*14",
	628: "114+514",
	619: "-11+45*14",
	616: "1*-(1-45)*14",
	612: "-1*(1-4)*51*4",
	611: "(1-14)*-(51-4)",
	609: "11*(4+51)+4",
	601: "11*(4+51)-4",
	595: "(114+5)*(1+4)",
	584: "114*5+14",
	581: "1+145*1*4",
	580: "1*145/1*4",
	579: "-1+145*1*4",
	576: "1*(145-1)*4",
	575: "114*5+1+4",
	574: "114*5/1+4",
	573: "114*5-1+4",
	567: "114*5+1-4",
	566: "114*5*1-4",
	565: "114*5-1-4",
	561: "11/4*51*4",
	560: "(1+1)*4*5*14",
	558: "11*4+514",
	556: "114*5-14",
	545: "(114-5)*(1+4)",
	529: "1+14+514",
	528: "1*14+514",
	527: "-1+14+514",
	522: "(1+1)*4+514",
	521: "11-4+514",
	520: "1+1+4+514",
	519: "1+1*4+514",
	518: "1-1+4+514",
	517: "-1+1*4+514",
	516: "-1-1+4+514",
	514: "(1-1)/4+514",
	513: "-11*(4-51)-4",
	512: "1+1-4+514",
	511: "1*1-4+514",
	510: "1-1-4+514",
	509: "11*45+14",
	508: "-1-1-4+514",
	507: "-11+4+514",
	506: "-(1+1)*4+514",
	502: "11*(45+1)-4",
	501: "1-14+514",
	500: "11*45+1+4",
	499: "11*45*1+4",
	498: "11*45-1+4",
	495: "11*(4+5)*(1+4)",
	492: "11*45+1-4",
	491: "11*45-1*4",
	490: "11*45-1-4",
	488: "11*(45-1)+4",
	481: "11*45-14",
	480: "11*(45-1)-4",
	476: "(114+5)/1*4",
	470: "-11*4+514",
	466: "11+451+4",
	460: "114*(5-1)+4",
	458: "11+451-4",
	457: "1+1+451+4",
	456: "1*1+451+4",
	455: "1-1+451+4",
	454: "-1+1*451+4",
	453: "-1-1+451+4",
	452: "114*(5-1)-4",
	450: "(1+1)*45*(1+4)",
	449: "1+1+451-4",
	448: "1+1*451-4",
	447: "1/1*451-4",
	446: "1*-1+451-4",
	445: "-1-1+451-4",
	444: "-11+451+4",
	440: "(1+1)*4*(51+4)",
	438: "(1+145)*-(1-4)",
	436: "-11+451-4",
	435: "-1*145*(1-4)",
	434: "-1-145*(1-4)",
	432: "(1-145)*(1-4)",
	412: "(1+1)*4*51+4",
	404: "(1+1)*4*51-4",
	400: "-114+514",
	396: "11*4*-(5-14)",
	385: "(11-4)*(51+4)",
	376: "(1+1)*4*(51-4)",
	375: "(1+14)*5*(1+4)",
	368: "(1+1)*(45+1)*4",
	363: "(1+1451)/4",
	361: "(11-4)*51+4",
	360: "(1+1)*45*1*4",
	357: "(114+5)*-(1-4)",
	353: "(11-4)*51-4",
	352: "(1+1)*(45-1)*4",
	351: "1+14*-5*-(1+4)",
	350: "1*(1+4)*5*14",
	349: "-1+14*5*(1+4)",
	341: "11*(45-14)",
	337: "1-14*-(5+1)*4",
	336: "1*14*(5+1)*4",
	335: "-1+14*(5+1)*4",
	329: "(11-4)*(51-4)",
	327: "-(114-5)*(1-4)",
	325: "-(1-14)*5*(1+4)",
	318: "114+51*4",
	312: "(1-14)*-(5+1)*4",
	300: "(11+4)*5/1*4",
	297: "-11*(4+5)*(1-4)",
	291: "11+4*5*14",
	286: "(1145-1)/4",
	285: "(11+4)*(5+14)",
	282: "1+1+4*5*14",
	281: "1+14*5/1*4",
	280: "1-1+4*5*14",
	279: "1*-1+4*5*14",
	278: "-1-1+4*5*14",
	275: "1*(1+4)*(51+4)",
	270: "(1+1)*45*-(1-4)",
	269: "-11+4*5*14",
	268: "11*4*(5+1)+4",
	267: "1+14*(5+14)",
	266: "1*14*(5+14)",
	265: "-1+14*(5+14)",
	260: "1*(14+51)*4",
	259: "1*(1+4)*51+4",
	257: "(1+1)/4*514",
	252: "(114-51)*4",
	251: "1*-(1+4)*-51-4",
	248: "11*4+51*4",
	247: "-(1-14)*(5+14)",
	240: "(11+4)*(5-1)*4",
	236: "11+45*(1+4)",
	235: "1*(1+4)*(51-4)",
	234: "11*4*5+14",
	231: "11+4*(51+4)",
	230: "1*(1+45)*(1+4)",
	229: "1145/(1+4)",
	227: "1+1+45*(1+4)",
	226: "1*1+45*(1+4)",
	225: "11*4*5+1+4",
	224: "11*4*5/1+4",
	223: "11*4*5-1+4",
	222: "1+1+4*(51+4)",
	221: "1/1+4*(51+4)",
	220: "1*1*(4+51)*4",
	219: "1+14+51*4",
	218: "1*14+51*4",
	217: "11*4*5+1-4",
	216: "11*4*5-1*4",
	215: "11*4*5-1-4",
	214: "-11+45*(1+4)",
	212: "(1+1)*4+51*4",
	211: "11-4+51*4",
	210: "1+1+4+51*4",
	209: "1+1*4*51+4",
	208: "1*1*4+51*4",
	207: "-1+1*4*51+4",
	206: "11*4*5-14",
	204: "(1-1)/4+51*4",
	202: "1+1-4+51*4",
	201: "1/1-4+51*4",
	200: "1/1*4*51-4",
	199: "1*-1+4*51-4",
	198: "-1-1+4*51-4",
	197: "-11+4+51*4",
	196: "-(1+1)*4+51*4",
	195: "(1-14)*5*(1-4)",
	192: "(1+1)*4*(5+1)*4",
	191: "1-14+51*4",
	190: "1*-14+51*4",
	189: "-11-4+51*4",
	188: "1-1-(4-51)*4",
	187: "1/-1+4*(51-4)",
	186: "1+1+(45+1)*4",
	185: "1-1*-(45+1)*4",
	184: "114+5*14",
	183: "-1+1*(45+1)*4",
	182: "1+1+45/1*4",
	181: "1+1*45*1*4",
	180: "1*1*45*1*4",
	179: "-1/1+45*1*4",
	178: "-1-1+45*1*4",
	177: "1+1*(45-1)*4",
	176: "1*1*(45-1)*4",
	175: "-1+1*(45-1)*4",
	174: "-1-1+(45-1)*4",
	172: "11*4*(5-1)-4",
	171: "114*(5+1)/4",
	170: "(11-45)*-(1+4)",
	169: "114+51+4",
	168: "(11+45)*-(1-4)",
	165: "11*-45/(1-4)",
	161: "114+51-4",
	160: "1+145+14",
	159: "1*145+14",
	158: "-1+145+14",
	157: "1*(1-4)*-51+4",
	154: "11*(4-5)*-14",
	152: "(1+1)*4*(5+14)",
	151: "1+145+1+4",
	150: "1+145*1+4",
	149: "1*145*1+4",
	148: "1*145-1+4",
	147: "-1+145-1+4",
	146: "11+45*-(1-4)",
	143: "1+145+1-4",
	142: "1+145*1-4",
	141: "1+145-1-4",
	140: "1*145-1-4",
	139: "-1+145-1-4",
	138: "-1*(1+45)*(1-4)",
	137: "1+1-45*(1-4)",
	136: "1*1-45*(1-4)",
	135: "-1/1*45*(1-4)",
	134: "114+5/1*4",
	133: "114+5+14",
	132: "1+145-14",
	131: "1*145-14",
	130: "-1+145-14",
	129: "114+5*-(1-4)",
	128: "1+1+(4+5)*14",
	127: "1-14*(5-14)",
	126: "1*(14-5)*14",
	125: "-1-14*(5-14)",
	124: "114+5+1+4",
	123: "114-5+14",
	122: "114+5-1+4",
	121: "11*(45-1)/4",
	120: "-(1+1)*4*5*(1-4)",
	118: "(1+1)*(45+14)",
	117: "(1-14)*(5-14)",
	116: "114+5+1-4",
	115: "114+5*1-4",
	114: "11*4+5*14",
	113: "114-5/1+4",
	112: "114-5-1+4",
	111: "11+4*5*(1+4)",
	110: "-(11-451)/4",
	107: "11-4*-(5+1)*4",
	106: "114-5+1-4",
	105: "114+5-14",
	104: "114-5-1-4",
	103: "11*(4+5)+1*4",
	102: "11*(4+5)-1+4",
	101: "1+1*4*5*(1+4)",
	100: "1*(1+4)*5*1*4",
	99: "11*4+51+4",
	98: "1+1+4*(5+1)*4",
	97: "1+1*4*(5+1)*4",
	96: "11*(4+5)+1-4",
	95: "114-5-14",
	94: "114-5/1*4",
	93: "(1+1)*45-1+4",
	92: "(1+1)*(45-1)+4",
	91: "11*4+51-4",
	90: "-114+51*4",
	89: "(1+14)*5+14",
	88: "1*14*(5+1)+4",
	87: "11+4*(5+14)",
	86: "(1+1)*45*1-4",
	85: "1+14+5*14",
	84: "1*14+5*14",
	83: "-1+14+5*14",
	82: "1+1+4*5/1*4",
	81: "1/1+4*5*1*4",
	80: "1-1+4*5*1*4",
	79: "1*-1+4*5/1*4",
	78: "(1+1)*4+5*14",
	77: "11-4+5*14",
	76: "1+1+4+5*14",
	75: "1+14*5*1+4",
	74: "1/1*4+5*14",
	73: "1*14*5-1+4",
	72: "-1-1+4+5*14",
	71: "(1+14)*5-1*4",
	70: "11+45+14",
	69: "1*14+51+4",
	68: "1+1-4+5*14",
	67: "1-1*4+5*14",
	66: "1*14*5-1*4",
	65: "1*14*5-1-4",
	64: "11*4+5*1*4",
	63: "11*4+5+14",
	62: "1+14+51-4",
	61: "1+1+45+14",
	60: "11+45*1+4",
	59: "114-51-4",
	58: "-1+1*45+14",
	57: "1+14*5-14",
	56: "1*14*5-14",
	55: "-1+14*5-14",
	54: "11-4+51-4",
	53: "11+45+1-4",
	52: "11+45/1-4",
	51: "11+45-1-4",
	50: "1+1*45/1+4",
	49: "1*1*45/1+4",
	48: "-11+45+14",
	47: "1/-1+45-1+4",
	46: "11*4+5+1-4",
	45: "11+4*5+14",
	44: "114-5*14",
	43: "1+1*45+1-4",
	42: "11+45-14",
	41: "1/1*45*1-4",
	40: "-11+4*51/4",
	39: "-11+45+1+4",
	38: "-11+45*1+4",
	37: "-11+45-1+4",
	36: "11+4*5+1+4",
	35: "11*4+5-14",
	34: "1-14+51-4",
	33: "1+1+45-14",
	32: "1*1+45-14",
	31: "1/1*45-14",
	30: "1*-1+45-14",
	29: "-11+45-1-4",
	28: "11+4*5+1-4",
	27: "11+4*5/1-4",
	26: "11-4+5+14",
	25: "11*4-5-14",
	24: "1+14-5+14",
	23: "1*14-5+14",
	22: "1*14+5-1+4",
	21: "-1-1+4+5+14",
	20: "-11+45-14",
	19: "1+1+4*5+1-4",
	18: "1+1+4*5*1-4",
	17: "11+4*5-14",
	16: "11-4-5+14",
	15: "1+14-5+1+4",
	14: "11+4-5/1+4",
	13: "1*14-5/1+4",
	12: "-11+4+5+14",
	11: "11*-4+51+4",
	10: "-11/4+51/4",
	9: "11-4+5+1-4",
	8: "11-4+5/1-4",
	7: "11-4+5-1-4",
	6: "1-14+5+14",
	5: "11-4*5+14",
	4: "-11-4+5+14",
	3: "11*-4+51-4",
	2: "-11+4-5+14",
	1: "11/(45-1)*4",
	0: "(1-1)*4514",
	"d": "11-4-5+1-4"
}

恶臭键值 = sorted(list(这 for 这 in 恶臭字典.keys() if 这!='d'))


def 这么臭的函数有必要定义吗(ent: CoreEntity):
	"""#论证 []
	这么臭的功能有必要解释吗
	"""
	attrs = ent.chain.tostr().split(' ')
	def 最小(数):
		左 = 0
		右 = len(GLOBAL.恶臭键值)-1
		中 = (左+右+1) >> 1
		while 左<右:
			if 数>=GLOBAL.恶臭键值[中]:
				左 = 中
			else:
				右 = 中-1
			中 = (左+右+1) >> 1
		return GLOBAL.恶臭键值[左]

	def 恶臭递归(恶臭数):
		if 恶臭数<0:
			return '-'+恶臭递归(-恶臭数)
		恶臭串 = str(恶臭数)
		正则 = re.compile(r'''\.\d+''')
		if re.search(正则,恶臭串) is not None:
			长 = re.search(正则,恶臭串).span()
			长 = 长[1] - 长[0] - 1
			return '('+恶臭递归(int(恶臭数*10**长)) + ')/('+恶臭递归(10**长) +')'
			
		if 恶臭数 in GLOBAL.恶臭字典:
			return GLOBAL.恶臭字典[恶臭数]
		除 = 最小(恶臭数)
		print('num=>',恶臭数,'\t','div=>',除)
		
		return str(f'({GLOBAL.恶臭字典[除]}*{恶臭递归(恶臭数//除)}+{恶臭递归(恶臭数%除)})')

	try:
		try:
			待证数 = int(attrs[0])
		except:
			待证数 = float(attrs[0])
			if 待证数 == 1e114514:
				raise NameError('大粪溢出')
		return [Plain(恶臭递归(待证数))]
	except Exception as e:
		print(e)
		return [Plain('这么恶臭的字串有必要论证吗')]

emoji_font = 'Assets/851tegaki_zatsu_normal_0883.ttf'

def 猫图生成器(ent: CoreEntity):
	"""#nya []
	生成猫表情，目前大概最多放4个中文字，例:#nya 要命
	"""
	attrs = ent.chain.tostr().split(' ')
	font = ImageFont.truetype(emoji_font, 18)
	nyaSrc = PImage.open('Assets/nya.png').convert('RGBA')
	layer2 = PImage.new('RGBA',nyaSrc.size,(255,255,255,0))
	draw = ImageDraw.Draw(layer2)
	
	text = ' '.join(attrs)
	beginPixel = (34-len(text)*9,55)

	draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
	# p = generateTmpFileName('Nya')
	# bio = BytesIO()
	# PImage.alpha_composite(nyaSrc,layer2).save(bio)
	# bio.seek(0)
	# b64 = base64.b64encode(bio.read()).decode()

	# asyncio.ensure_future(rmTmpFile(p),loop=None)
	return [Image(base64=pimg_base64(PImage.alpha_composite(nyaSrc,layer2)))]

def 优质解答生成器(ent: CoreEntity):
	"""#解答 []
	生成优质解答图片,例:#解答 自分で百度しろ
	"""
	attrs = ent.chain.tostr().split(' ')
	font = ImageFont.truetype(emoji_font,25)
	nyaSrc = PImage.open('Assets/answer.jpg').convert('RGBA')
	layer2 = PImage.new('RGBA',nyaSrc.size,(255,255,255,0))
	draw = ImageDraw.Draw(layer2)
	
	text = ent.chain.tostr()
	beginPixel = (50,120)

	draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
	# p = generateTmpFileName('Ans')

	# PImage.alpha_composite(nyaSrc,layer2).save(p)
	# asyncio.ensure_future(rmTmpFile(p),loop=None)
	return [Image(base64=pimg_base64(PImage.alpha_composite(nyaSrc,layer2)))]

def 自己不會百度嗎(ent: CoreEntity):
	"""#百度 [#baidu]
	自己不會百度嗎?那我來幫你百度一下
	"""
	return [Plain(f"http://iwo.im/?q={ent.chain.tostr()}")]

def IPlay生成器(ent: CoreEntity):
	"""#iplay [#口罩]
	自己试试效果吧，例:#iplay I play BanG Dream!
	"""

	font = ImageFont.truetype(emoji_font,25)
	Src = PImage.open('Assets/IPlayRhythmGame.png').convert('RGBA')
	layer2 = PImage.new('RGBA',Src.size,(255,255,255,0))
	draw = ImageDraw.Draw(layer2)
	
	text = ent.chain.tostr()
	beginPixel = (308,1004)

	draw.text(beginPixel,text,fill=(255,255,255,255),font=font)
	return [Image(base64=pimg_base64(PImage.alpha_composite(Src,layer2)))]
	
def 希望没事生成器(ent: CoreEntity):
	"""#希望 []
	希望人没事生成器（莲华）,例:#希望 人别死我家门口
	"""
	font = ImageFont.truetype(emoji_font,100)
	nyaSrc = PImage.open('Assets/wish.png').convert('RGBA')
	layer2 = PImage.new('RGBA', nyaSrc.size, (255, 255, 255, 0))
	draw = ImageDraw.Draw(layer2)
	attrs = ent.chain.tostr().split(' ')
	text = attrs[0]
	beginPixel = (640-len(text)*50,600)
	if len(attrs)>1:
		r = int(attrs[1][:2],16)
		g = int(attrs[1][2:4],16)
		b = int(attrs[1][4:],16)
		draw.text(beginPixel,text,fill=(r,g,b,255),font=font)
	else:
		draw.text(beginPixel,text,fill=(255,255,255,255),font=font)

	return [Image(base64=pimg_base64(PImage.alpha_composite(nyaSrc,layer2)))]

def 希望工程(ent: CoreEntity):
	"""#希望工程 []
	希望人没事生成器（一般）,例:#希望 人别死我家门口
	"""
	font = ImageFont.truetype(emoji_font,100)
	nyaSrc = PImage.open('Assets/wish.jpg').convert('RGBA')
	layer2 = PImage.new('RGBA', nyaSrc.size, (255, 255, 255, 0))
	draw = ImageDraw.Draw(layer2)
	attrs = ent.chain.tostr().split(' ')
	
	text = attrs[0]
	beginPixel = (540-len(text)*50,900)
	if len(attrs)>1:
		r = int(attrs[1][:2],16)
		g = int(attrs[1][2:4],16)
		b = int(attrs[1][4:],16)
		draw.text(beginPixel,text,fill=(r,g,b,255),font=font)
	else:
		draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
	return [Image(base64=pimg_base64(PImage.alpha_composite(nyaSrc,layer2)))]

def 出拳(ent: CoreEntity): 
	"""#拳 []
	轮到我出拳了！（
	格式:
		#拳 <事件> <主体>
	例:
		#拳 我们女孩子到底要怎么活着 女性
	"""
	attrs = ent.chain.tostr().split(' ')
	return [Plain(f'''看到这句话我气得浑身发抖，大热天的全身冷汗手脚冰凉，这个社会还能不能好了，{attrs[0]}你们才满意，眼泪不争气的流了下来，这个国到处充斥着对{attrs[1]}的压迫，{attrs[1]}何时才能真正的站起来。''')]

def 懂的都懂(ent: CoreEntity): 
	"""#懂 []
	懂的都懂,不懂的我也不多解释
	"""
	return [Plain('这种事情见得多了，我只想说懂的都懂，不懂的我也不多解释，毕竟自己知道就好，细细品吧。你们也别来问我怎么了，利益牵扯太大，说了对你我都没好处，当不知道就行了，其余的我只能说这里面水很深，牵扯到很多东西。详细情况你们自己是很难找的，网上大部分已经删除干净了，所以我只能说懂的都懂。懂的人已经基本都获利上岸了，不懂的人永远不懂，关键懂的人都是自己悟的，你也不知道谁是懂的人也没法请教，大家都藏着掖着生怕别人知道自己懂的事，所以不懂的你甚至都不知道自己不懂。在有些时候，某些人对某些事情不懂装懂，还以为别人不懂。其实自己才是不懂的，别人懂的够多了，不仅懂，还懂的超越了这个范围，但是某些不懂的人让懂的人完全教不懂，所以不懂的人永远不懂，只能不懂装懂，别人说懂的都懂，只要点点头就行了。其实你我都懂，不懂没必要装懂，毕竟里面牵扯到很多懂不了的事，懂的人觉得没必要说出来，不懂的人看见又来问七问八，最后跟他说了他也不一定能懂，就算懂了以后也对他不好，毕竟懂的太多了不是好。懂了吗？')]

def 舔狗生成器(ent: CoreEntity):
	"""#舔 [#pr]
	稍微有点难用的舔狗生成器
	用法:
		#舔 [人名] [动词,表示待舔人的技能] [待舔人用于施展技能的身体部位] [待舔人的技能产物]
	没填的部分会用默认值填满。
	默认值:
		#舔 太太 画 手 图
	"""
	attrs = ent.chain.tostr().split(' ')
	if not any(attrs):
		attrs = []
	pat = ['太太','画','手','图']
	for i in range(min(len(attrs),len(pat))):
		pat[i] = attrs[i]
	construct = [
		Plain(f"!{pat[0]}!!!!!!"),
		Plain(f"您太会{pat[1]}了我跪下来给您用免洗洗{pat[2]}液洗{pat[2]}"),
		Plain(f"太会{pat[1]}了"),
		Plain(f"什么{pat[2]}，怎么长的"),
		Plain(f"太神了"),
		Plain(f"塞纳河畔的水我的泪"),
		Plain(f"我嚎到邻居跟我一起嚎kamisama"),
		Plain(f"整个小区声控灯被我嚎碎"),
		Plain(f"{pat[0]}您太会{pat[1]}了"),
		Plain(f"太会了"),
		Plain(f"神仙下凡普渡众生"),
		Plain(f"中西结合融会贯通的大善心"),
		Plain(f"您太会了"),
		Plain(f"绝了"),
		Plain(f"绝炸了"),
		Plain(f"我首当其冲放烟花"),
		Plain(f"您太会了"),
		Plain(f"我晚上看到{pat[3]}从床上蹦起落下三百六十度头骨错位大喊"),
		Plain(f"您太会了！！！！！！！！！"),
		Plain(f"我拿起手机一看，头骨瞬间回位"),
		Plain(f"您简直神了"),
		Plain(f"这是什么神仙连{pat[1]}都能包治百病"),
		Plain(f"{pat[1]}医双修神仙"),
		Plain(f"绝了"),
		Plain(f"您这种神仙活该位列仙班"),
		Plain(f"仙班的甲子班"),
		Plain(f"您不是kami就没有神仙了"),
		Plain(f"简直绝了"),
		Plain(f"神仙的菜想必也是极好吃的"),
		Plain(f"不仅物理炒菜"),
		Plain(f"精神上还喂饱了好多人"),
		Plain(f"简直活佛济世"),
		Plain(f"不行我要再去看看"),
		Plain(f"太神了"),
		Plain(f"神迹"),
		Plain(f"未来滚滚历史长河中名{pat[1]}必有您一份"),
		Plain(f"难道你就觉得它只是{pat[1]}"),
		Plain(f"难道你又不更远一点想到，那神仙下凡拯救众生的善心"),
		# 这里有几句话太难通用：
		# > 那个炸毛毛毛
		# > 绝了
		# > 灵活的姿态，准确的用色，美丽的线条
		# > 绝了
		Plain(f"我透过手机屏幕感受到了直击心灵的震撼"),
		Plain(f"我每个细胞带着我全身尖叫活性爆发整个人获得了超凡的能量就因为您的{pat[1]}"),
		Plain(f"我激情落泪"),
		Plain(f"我把我自己耳朵都嚎聋了"),
		Plain(f"恨不得摆上一车喇叭歌颂您的光辉事迹")
	]
	# asyncio.ensure_future(msgSerializer(construct,**kwargs))
	for p, i in enumerate(construct[1:]):
		i.meta['delay'] = len(construct[p].text) / 5
	
	return construct

def 川普生成器(ent: CoreEntity):
	"""#Trump [#trump]
	No one knows Trump Generator better than me!
	"""
	s = ent.chain.tostr()
	if not s:
		s = '中国'
	pat = f"{chr(128588)}没有人\n{chr(128080)}比我\n{chr(128076)}更懂\n{chr(9757)}{s}"
	return [Plain(pat)]

def 骰子(ent: CoreEntity):
	"""#Roll [#roll]
	44的骰娘，返回指定区间的一个整数。用法:#Roll <左区间(包含)> <右区间(包含)>
	"""
	attrs = ent.chain.tostr().split(' ')
	if (len(attrs)>=2):
		x,y=(int(i) for i in attrs[:2])
		return [Plain(f"{random.randint(min(x,y),max(x,y))}")]
	else:
		return [Plain("我要怎么给你Roll哦")]

def 军舰(ent: CoreEntity):
	"""#军舰 [#jj]
	重来！这么小声还想问"#军舰"怎么开?
	"""
	return [Plain(random.choice(["那么小声还想开军舰？","听不见！"]))]

async def 今日人品(*attrs,kwargs={}):
	player_id=kwargs['mem'].id
	if player_id not in GLOBAL.JRRP_map: #已经存在信息直接读取，否则生成新数字
		temp_rpval=random.randint(0,100)
		GLOBAL.JRRP_map[player_id]=[temp_rpval]
		#随机抽取字典值
		b=list(GLOBAL.JRRP_words)
		random.shuffle(b)
		if temp_rpval==100:
			GLOBAL.JRRP_map[player_id].extend([['诸事皆宜'],['-']])
		elif 80<=temp_rpval<=99:
			GLOBAL.JRRP_map[player_id].extend([b[0:5],b[5:6]])
		elif 60<=temp_rpval:
			GLOBAL.JRRP_map[player_id].extend([b[0:4],b[4:6]])
		elif 40<=temp_rpval:
			GLOBAL.JRRP_map[player_id].extend([b[0:3],b[3:6]])
		elif 20<=temp_rpval:
			GLOBAL.JRRP_map[player_id].extend([b[0:2],b[2:6]])
		elif 1<=temp_rpval:
			GLOBAL.JRRP_map[player_id].extend([b[0:1],b[1:6]])
		elif temp_rpval==0:
			GLOBAL.JRRP_map[player_id].extend([['-'],['诸事不宜']])

	rp_val=GLOBAL.JRRP_map[player_id][0]
	print(rp_val)
	print(GLOBAL.JRRP_map[player_id])
	ans='你今天的人品为：'+str(rp_val)+'\n'
	ans+='宜：'+','.join(GLOBAL.JRRP_map[player_id][1])+'\n'
	ans+='忌：'+','.join(GLOBAL.JRRP_map[player_id][2])+'\n'

	return [Plain(ans)]
	#rp_val=GLOBAL.JRRP_map[player_id]
	#ans='你今天的人品为：'+str(rp_val)+'\n评价：'
	#if rp_val==100:
	#    ans+='心想事成'
	#elif 80<=rp_val<=99:
	#    ans+='万事如意'
	#elif 60<=rp_val<=79:
	#    ans+='修短随化'
	#elif 40<=rp_val<=59:
	#    ans+='因祸得福'
	#elif 20<=rp_val<=39:
	#    ans+='落魄不偶'
	#elif 1<=rp_val<=19:
	#    ans+='有命无运'
	#elif rp_val==0:
	#    ans+='危！'
	#return [Plain(ans)]

functionMap = {
	"#今日人品":今日人品,
}

shortMap = {
	"#jrrp": "#今日人品",
}

functionDescript = {
	"#今日人品":'取得你今天的人品值（0~100）',
}
