import cv2,math ,os,threading
from PIL import Image, ImageDraw, ImageFont
import numpy as np
basic=r'''!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~；♪—'''

ts=[]
for _font_file,_fontname in [('simsun.ttc','ゴシック'),('SourceHanSansCN-Regular.otf','明朝'),('SIMKAI.TTF','モダン'),('SIMLI.ttf','丸ゴシック'),('simhei.ttf','太丸ゴシック')]:
    def xx(font_file,fontname):
        for _type in [2,1,4]:
            if fontname!='明朝' and _type in [2,4]:continue
            charsetfile=f'newcharset{_type}.txt' #必须保持行高不变。 
            with open(charsetfile,'r',encoding='utf-8-sig') as ff:
                chars=ff.read()
            
            if _type==1:    
                sizes=['12','16','33','40','41']
            elif _type==2:
                sizes=['41'] 
            elif _type==3:
                sizes=['16','40']
            elif _type==4:
                sizes=['15','25','27','30','32','33','36']
            for f in sizes:
                size=int(f)+1
                if 0:
                    if _type==1: 
                        os.system(rf'.\LuckSystem.exe image export -i  "C:\InnocentGrey\カルタグラ FHD\files\FONT\{fontname}{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\FONT\{fontname}{f}.png"')
                    elif _type==2:
                        os.system(rf'.\LuckSystem.exe image export -i  "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_明朝{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_明朝{f}.png"')
                    elif _type==3:
                        os.system(rf'.\LuckSystem.exe image export -i  "C:\InnocentGrey\カルタグラ FHD\files\FONT_V\{fontname}{f}v" -o "C:\InnocentGrey\カルタグラ FHD\files\FONT_V\{fontname}{f}v.png"')
                    elif _type==4:
                        os.system(rf'.\LuckSystem.exe image export -i  "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_ゴシック{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_ゴシック{f}.png"')
                if _type==1: 
                    originpng=rf"C:\InnocentGrey\カルタグラ FHD\files\FONT\{fontname}{f}.png"
                elif _type==2:
                    originpng=rf"C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_明朝{f}.png"
                elif _type==3:
                    originpng=rf"C:\InnocentGrey\カルタグラ FHD\files\FONT_V\{fontname}{f}v.png"
                elif _type==4:
                    originpng=rf"C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_ゴシック{f}.png"
                originimg=Image.open(originpng)
                _addition={
                    13:4,
                    17:4,
                    34:0,
                    41:4,
                    42:0,
                    16:0,
                    26:0,
                    28:0,
                    31:4,
                    33:4,
                    37:4
                }
                imageW=size*100+_addition[size]

                imageH=size * int(math.ceil((len(chars))/100.0))
                print(imageW,imageH)
                pic = np.zeros((imageH, imageW, 4), dtype=np.uint8)
                if font_file =='SourceHanSansCN-Regular.ttf':
                    #diff=-0.23*(size)
                    diff={
                        42:-13,
                        41:-12,
                        37:-11,
                        34:-10,
                        33:-10,
                        31:-9,
                        28:-8,
                        26:-7,
                        17:-5,
                        16:-4,
                        13:-3
                    }[size]
                elif font_file=='msyh.ttc':
                    diff=-0.2*(size)
                # elif font_file=='simhei.ttf':
                #     diff=-0.05*size
                else:
                    diff=0
                originfile=['info12_string_sort_utf-8.txt','infosys41_string_sort_utf-8.txt','info40v_string_sort_utf-8.txt','infosys36_string_sort_utf-8.txt'][_type-1]
                with open(originfile,'r',encoding='utf8') as ff:
                    origin=ff.read()
                try:
                    fontStyle = ImageFont.truetype(
                       rf'C:\Windows\Fonts\{font_file}', size-1, encoding="utf-8")
                except:
                    fontStyle = ImageFont.truetype(
                       rf'{os.environ["LOCALAPPDATA"]}\Microsoft\Windows\Fonts\{font_file}', size-1, encoding="utf-8")
                img = Image.fromarray(cv2.cvtColor( pic, cv2.COLOR_BGRA2RGBA))
                draw = ImageDraw.Draw(img)
                for i in range(len(chars)):
                    pic1 = np.zeros((size, size, 4), dtype=np.uint8)
                    charimg=Image.fromarray(cv2.cvtColor( pic1, cv2.COLOR_BGRA2RGBA))
                    draw = ImageDraw.Draw(charimg)
                    y = i // 100
                    x = i % 100
                    if i==0:
                        char=' '
                    else:
                        char = chars[i] 
                    if char in basic and char in origin:
                        __i=origin.index(char)-1
                        __y=__i//100
                        __x=__i%100
                        crop=originimg.crop([__x * size, __y * size,__x * size+size,__y * size+size ])
                        img.paste(crop,(x * size, y * size ))
                    else:
                    # draw.text((x * size, y * size-14), char, (255, 255, 255), font=fontStyle)
                        #一些中文字体会有14个像素的向下偏移
                        draw.text((0,0+diff), char, (255, 255, 255), font=fontStyle)
                        img.paste(charimg,(x * size, y * size ))
                img.save(f'{fontname}.png') 
                if 0:
                    r,g,b,_=img.split()
                    Image.merge('RGB',(r,g,b)).save(f'{fontname}_{size}.png') 
                    continue
                # img=Image.open('1.png') 
                # img=np.array(img)  
                # img[img[:,:,-1]==0]=0
                # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                # h,w,c=img.shape
                # cv2.imwrite('2.png',img )
                if 1:   #cz2字体部分字下半部分莫名向右偏移
                        #LuckSystem确实有问题，部分字体导入后闪退，cz4就没问题。
                    if _type==1: 
                        os.system(rf'..\image\czximage\build\Release\image2cz.exe "C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG\03b" {fontname}.png  "C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW\{fontname}{f}"')
                    elif _type==2:
                        os.system(rf'..\image\czximage\build\Release\image2cz.exe "C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG\03b" {fontname}.png  "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT_NEW\システム_明朝{f}"')
                    elif _type==3:
                        os.system(rf'..\image\czximage\build\Release\image2cz.exe "C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG\03b" {fontname}.png  "C:\InnocentGrey\カルタグラ FHD\files\FONT_V_NEW\{fontname}{f}v"')
                    elif _type==4:
                        os.system(rf'..\image\czximage\build\Release\image2cz.exe "C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG\03b" {fontname}.png  "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT_NEW\システム_ゴシック{f}"')
                
                else:
                    if _type==1: 
                        os.system(rf'.\LuckSystem.exe image import -i {fontname}.png -s "C:\InnocentGrey\カルタグラ FHD\files\FONT\明朝{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW\{fontname}{f}"')
                    elif _type==2:
                        os.system(rf'.\LuckSystem.exe image import -i {fontname}.png -s "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_明朝{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT_NEW\システム_明朝{f}"')
                    elif _type==3:
                        os.system(rf'.\LuckSystem.exe image import -i {fontname}.png -s "C:\InnocentGrey\カルタグラ FHD\files\FONT_V\明朝{f}v" -o "C:\InnocentGrey\カルタグラ FHD\files\FONT_V_NEW\{fontname}{f}v"')
                    elif _type==4:
                        os.system(rf'.\LuckSystem.exe image import -i {fontname}.png -s "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_ゴシック{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT_NEW\システム_ゴシック{f}"')
    t=threading.Thread(target=xx,args=(_font_file,_fontname))
    ts.append(t)
for t in ts:
    t.start()
for t in ts:
    t.join()