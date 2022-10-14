import pickle, random, collections, string, re, requests, os

def func(rawinputs: str):
    """#约稿 [#waifu, #召唤, #产粮]
    ai画图，txt2img，容易被封所以还是建议优先直接用网页
    """
    ses = requests.session()
    authdir = 'waifusd_auth.pickle'
    apibase = 'http://127.0.0.1:7860'
    if os.path.exists(authdir):
        with open(authdir, 'rb') as f:
            usr, pw = pickle.load(f)
        ses.post(apibase+'/login', data={'username':usr,'password':pw})
    

    filter_p = re.compile('<.*?>', re.MULTILINE)
    def filter(src):
        b = []
        for i in filter_p.sub(' ', src).replace('\n', ' ').strip():
            if b[-1:] == [' '] and ' ' == i:
                continue
            else:
                b.append(i)
        return ''.join(b)

    def parser(src):
        pm = [
            'prompt:', 'negative prompt:', 'steps:', 'sampler:', 'cfg scale:',
            'seed:', 'size:', 'model hash:', 'denoising strength:', 'clip skip:',
        ]
        b = [[] for i in pm]

        cur = b[0]
        p = 0

        def chk():
            nonlocal p
            nonlocal cur
            for ind, token in enumerate(pm):
                if src[p:p+len(token)].lower() == token:
                    p += len(token)
                    cur = b[ind]
                    return False
            return True

        while p < len(src):
            if chk():
                cur.append(src[p])
                p += 1
        for p, i in enumerate(b):
            b[p] = ''.join(i).strip().removesuffix(',')
        return {j:i for i, j in zip(b, pm) if i}
        
    if rawinputs == '样例':
        with open('Assets/waifusd/prompts.pickle', 'rb') as f:
            li = pickle.load(f)
        return random.choice(li)
    if rawinputs == '词汇表':
        with open('Assets/waifusd/chat_tokens.txt', 'r', encoding='utf-8') as f:
            li = f.read().split('\n')
        return '\n'.join(random.sample(li, 10))
    if rawinputs == '模板':
        return """((masterpiece)), best quality, illustration, 1 girl, beautiful,beautiful detailed sky, catgirl,beautiful detailed water, cinematic lighting, Ice Wings, (few clothes),loli,(small breasts),light aero blue hair, Cirno(Touhou), wet clothes,underwater,hold breath,bubbles,cat ears ,dramatic angle
Negative prompt: lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, huge breasts
Steps: 75, Sampler: DDIM, CFG scale: 11, Seed: 3323485853, Size: 512x768, Model hash: e6e8e1fc, Clip skip: 2"""

    txt2img_inputs = collections.namedtuple('txt2img_inputs',
        field_names=[
            "prompt", "negative_prompt", "prompt_style", "prompt_style2", "steps",
            "sampler", "restore_faces", "tiling", "batch_count", "batch_size",
            "cfg_scale", "seed", "sub_seed", "subseed_strength", "seed_resize_from_h",
            "seed_resize_from_w", "unk_1", "width", "height", "highres_fix",
            "scale_latent", "denoising_strength", "script",
        ], defaults=[
            "loli", "nsfw", "None", "None", 30,
            "DDIM", False, False, 1, 1,
            7, -1, -1, 0, 0,
            0, False, 512, 512, False,
            False, 0.85, "None",
        ])

    def nums(src):
        b = []
        for i in src:
            if i in string.digits+'-':
                b.append(i)
        return int(''.join(b))
    def floats(src):
        b = []
        for i in src:
            if i in string.digits+'.':
                b.append(i)
        return float(''.join(b))
    
    mapping_string = { # 迫真萃取
        float: floats,
        int: nums,
        str: lambda x: x
    }
    
    parsed = parser(filter(rawinputs))
    if len(parsed) > 1: # 有东西，高级模式
        modify = {}
        for k, v in parsed.items():
            pk = k[:-1].replace(' ', '_')
            if pk in txt2img_inputs._fields:
                modify[pk] = mapping_string[type(txt2img_inputs._field_defaults[pk])](v)

        if sz := parsed.get('size:', ''):
            w, h = re.compile('([0-9]+)[x\*]([0-9]+)').search(sz).groups()
            modify['width'] = int(w)
            modify['height'] = int(h)
        model = txt2img_inputs(**modify)
    else: # 简易模式
        model = txt2img_inputs(
            prompt='((masterpiece)), best quality, illustration, beautiful, beautiful detailed eyes,' + parsed['prompt:'],
            negative_prompt='nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry'
        )
    args = model + (
        False, False, None, "", "Seed",
        "", "Nothing", "", True, False,
        False, None,
        "", # json like object
        ""  # html like object
    )
    # return args
    # print(args)
    jj = ses.post(f"{apibase}/api/predict", json={'fn_index':13, 'data':args}).json()
    print(jj)
    j = ses.post(f"{apibase}/api/predict", json={'fn_index':13, 'data':args}).json()['data']
    return j
    return [Image(base64=j[0][0][22:]), Plain(filter(j[2]))]
    

def banner(): print("==========================")

a1 = func("""robot,blue,gun,death""")
banner()
a2 = func("""masterpiece, best quility ,official art,extremely detailed CG unity 8k wallpaper,delicate scene,2 young girl,symmetrical docking,hug,beautiful detailed eyes, look at the viewer,small breasts,undressing
Negative prompt: lowres, bad anatomy, bad hands,text, error, missing fingers,extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,dick,cum
Steps: 32, Sampler: Heun, CFG scale: 12, Seed: 84833071, Size: 512x768, Model hash: e6e8e1fc, Hypernet: anime_3, Clip skip: 2""")
print(a1,'\n', a2)
for p, (i, j) in enumerate(zip(a1, a2)):
    if (type(i)!=type(j)):
        print('Err', p, type(i), type(j))