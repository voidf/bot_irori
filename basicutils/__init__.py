def make_banner(src: str, filler: str ='=') -> str:
    l = len(src)
    return filler * l + '\n' + src + '\n' + filler * l

