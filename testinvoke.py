from typing import List
from basicutils.applications.Credit import generate_sign_log, gen_fortune
from fapi.models.Routiner import imaseconds
import datetime
from PIL import Image as PImage
from PIL import ImageDraw, ImageFont
from basicutils.media import pimg_base64

rep = generate_sign_log(5)

print(rep)
import random
from PIL import Image as PImage
from PIL import ImageDraw, ImageFont
# from basicutils.media import pimg_base64
tegaki_zatsu = 'Assets/851tegaki_zatsu_normal_0883.ttf'
seto_font = 'Assets/setofont.ttf'

font_tegaki = ImageFont.truetype(tegaki_zatsu, 24)

fortune_size = 80
font_fortune = ImageFont.truetype(seto_font, fortune_size)
rp_size = 20
font_rp = ImageFont.truetype(seto_font, rp_size)

font_yj = ImageFont.truetype(seto_font, 40)

emotion_type = 'B' if rep.rp >= 62.5 else ('C' if rep.rp <= 47.5 else 'N')
time_now = imaseconds()
time_period = 'light' if time_now > 6 * 3600 else ('normal' if 19*3600 > time_now > 12*3600 else 'dark')

template = PImage.open(f'Assets/sign/alpha/small/{emotion_type}{time_period}.png').convert('RGBA')

backgroundRGB = random.randint(0,255), random.randint(0,255), random.randint(0,255), 255
background_grey = backgroundRGB[0] * 0.299 + backgroundRGB[1] * 0.587 + backgroundRGB[2] * 0.114

layer3 = PImage.new('RGBA',template.size,backgroundRGB) # 上底色
w, h = template.size

font_color = (255, 255, 255, 255) if background_grey < 128 else (0, 0, 0, 255)

template = PImage.alpha_composite(layer3,template,)

layer2 = PImage.new('RGBA',template.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(layer2)

text = rep.msg
fortune = gen_fortune(rep.rp)

def write_center(text, font, height, percentage=0.5):
    lines = text.split('\n')
    W = max(font.getsize(tx)[0] for tx in lines)
    draw.text(((w-W)*percentage , height), text, fill=font_color, font=font)

write_center(fortune, font_fortune, h * 0.04)
write_center(f"{rep.rp:.3f}%", font_rp, h * 0.115)
write_center("宜", font_yj, h * 0.142, 0.5)
write_center("忌", font_yj, h * 0.310, 0.5)

def write_yj_items(li: List[str], font, begin_height):
    H = font.getsize(li[0])[1]
    for i in li:
        C = i.strip().split('\t')
        if len(C) == 2:
            A, B = C
            draw.text((w * 0.05 , begin_height), A, fill=font_color, font=font)
            draw.text((w * 0.95 , begin_height), B, fill=font_color, font=font, anchor='ra')
        else:
            write_center(C[0], font, begin_height)
        begin_height += H

write_yj_items(rep.y, font_tegaki, h*0.183)
write_yj_items(rep.j, font_tegaki, h*0.351)

import re
def disassemble_msg(token: str, msg):
    t = re.search(token + r'\n(.*?)\n\n', msg, re.M | re.DOTALL).group(1)
    return t.split('\n')

disassemble_msg('宜:', rep.msg)

PImage.alpha_composite(template,layer2).show()
