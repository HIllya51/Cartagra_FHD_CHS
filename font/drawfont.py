import cv2,math ,os,json
from PIL import Image, ImageDraw, ImageFont
import numpy as np
for _type in [2,1,3]:
    
    charsetfile=f'newcharset{_type}.txt' #必须保持行高不变。
    #charsetfile='info12_string_sort_utf-8.txt'
    font_file='simsun.ttc'#'SourceHanSansCN-Regular.ttf'#
    with open(charsetfile,'r',encoding='utf-8-sig') as ff:
        chars=ff.read()
    
    if _type==1:    
        sizes=['12','16','33','40','41']
    elif _type==2:
        sizes=['41'] 
    elif _type==3:
        sizes=['16','40']
    for f in sizes:
        size=int(f)+1
        
        _addition={
            13:4,
            17:4,
            34:0,
            41:4,
            42:0
        }
        imageW=size*100+_addition[size]

        imageH=size * int(math.ceil((len(chars))/100.0))
        print(imageW,imageH)
        pic = np.zeros((imageH, imageW, 4), dtype=np.uint8)
        
        fontStyle = ImageFont.truetype(
                font_file, size-1, encoding="utf-8")

        img = Image.fromarray(cv2.cvtColor( pic, cv2.COLOR_BGRA2RGBA))
        draw = ImageDraw.Draw(img)
        for i in range(len(chars)):
            y = i // 100
            x = i % 100
            if i==0:
                char=' '
            else:
                char = chars[i] 
            
        # draw.text((x * size, y * size-14), char, (255, 255, 255), font=fontStyle)
            #一些中文字体会有14个像素的向下偏移
            draw.text((x * size, y * size), char, (255, 255, 255), font=fontStyle)
            
        img.save('1.png') 

        img=Image.open('1.png') 
        img=np.array(img)  
        img[img[:,:,-1]==0]=0
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        h,w,c=img.shape
        cv2.imwrite('2.png',img )

        if _type==1:
            os.system(rf'.\LuckSystem.exe image import -i 1.png -s "C:\InnocentGrey\カルタグラ FHD\files\FONT\明朝{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW\明朝{f}"')
        elif _type==2:
            os.system(rf'.\LuckSystem.exe image import -i 1.png -s "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\システム_明朝{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT_NEW\システム_明朝{f}"')
        elif _type==3:
            os.system(rf'.\LuckSystem.exe image import -i 1.png -s "C:\InnocentGrey\カルタグラ FHD\files\FONT_V\明朝{f}v" -o "C:\InnocentGrey\カルタグラ FHD\files\FONT_V_NEW\明朝{f}v"')