import os,shutil,json,ctypes
basic=''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'''
remap_charset2={}
r_remap_charset2={}

bigchars=set() 
for f in os.listdir('../SCRIPT_FHD/text'):
    with open('../SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
        newtexts=ff.read()
    if len(newtexts) and newtexts[0]=='\ufeff':newtexts=newtexts[1:]
    newtexts=newtexts.split('\n')
    newtexts=[newtexts[i] if i%3==1 else '' for i in range(len(newtexts))]
    bigchars=bigchars.union(set(''.join(newtexts)))  
with open('../uitext.txt','r',encoding='utf8') as ff:
    newtexts=ff.read().split('\n')  
newtexts=[newtexts[i] if i%3==1 else '' for i in range(len(newtexts))]
with open(r'info40v_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
    origin=ff.read()
bigchars=bigchars.union(set(''.join(newtexts))) 
bigchars=bigchars.union(origin) 
bigchars=sorted(list(bigchars))

print('￥' in bigchars)
with open('infosys36_string_sort_utf-8.txt','r',encoding='utf-8-sig' ) as ff:
    originset=set(ff.read())
with open(r'info12_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
    originset=originset.union(set(ff.read()))#[len(basic):]

onlyinoriginset=sorted(list(((set(originset)-set(bigchars)))),reverse=True)
for c in bigchars:
    
    if c in originset:
        remap_charset2[c]=c
        r_remap_charset2[c]=c
    else:
        remap_charset2[c]=onlyinoriginset[0]
        r_remap_charset2[onlyinoriginset[0]]=c
        onlyinoriginset=onlyinoriginset[1:]
for c in onlyinoriginset:
    remap_charset2[c]=c
    r_remap_charset2[c]=c
    
with open(f'remap_charset2.txt','w',encoding='utf8') as ff:
    ff.write(json.dumps(remap_charset2,ensure_ascii=False))

for _type in  [2,4,1,3]:
    
    #print((chars))
    #newcharset=origin+''.join(list(chars-set(origin)))
    if _type==1:
        chars=set()
        with open(r'info12_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
            origin=ff.read()

        for f in os.listdir('../SCRIPT_FHD/text'):
            with open('../SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
                newtexts=ff.read()
            if len(newtexts) and newtexts[0]=='\ufeff':newtexts=newtexts[1:]
            newtexts=newtexts.split('\n')
            newtexts=[newtexts[i] if i%3==1 else '' for i in range(len(newtexts))]
            chars=chars.union(set(''.join(newtexts))) 
    elif _type==2:
            chars=set()
            with open(r'infosys41_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
                origin=ff.read()

            for f in os.listdir('../SCRIPT_FHD/text'):
                if f!='0000-op1':continue
                
                with open('../SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
                    newtexts=ff.read()
                if len(newtexts) and newtexts[0]=='\ufeff':newtexts=newtexts[1:]
                newtexts=newtexts.split('\n')
                newtexts=[newtexts[i] if i%3==1 else '' for i in range(len(newtexts))]
                chars=chars.union(set(''.join(newtexts))) 
    elif _type==3:
        with open(r'info40v_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
            origin=ff.read()
    elif _type==4:
        with open('infosys36_string_sort_utf-8.txt','r',encoding='utf-8-sig' ) as ff:
            origin=ff.read()
        
        chars=set() 

        with open('../uitext.txt','r',encoding='utf8') as ff:
            newtexts=ff.read().split('\n') 
        newtexts=[newtexts[i] if i%3==1 else '' for i in range(len(newtexts))]

        chars=chars.union(set(''.join(newtexts)))
    origin=list(origin)
    chars=sorted(chars)

    if _type==3:
        newcharset=origin
    else:
        
        
        newcharset=basic 
        for c in chars:
            if c in newcharset:
                continue
            else:
                newcharset+=c
        onlyinoriginsetsave=sorted(list(((set(originset)-set(bigchars)))),reverse=True)
        #print(_type,len(onlyinoriginsetsave),len(newcharset),len(origin),len(originset))
        while len(newcharset)<len(origin):
            newcharset+=' '  
            if _type==4:
                badchars='删时绫薰岛马庆 其苍'   #load界面“削除”找不到在哪替换；角色声音不能改名字，改了没法调音量
                if len(newcharset)==len(origin)-len(badchars):
                    newcharset+=badchars
        #print(_type,len(newcharset))
    with open(f'newcharset{_type}.txt','w',encoding='utf-8-sig') as ff:
        ff.write(''.join(newcharset))

    if _type==1:    
        sizes=['12','16','33','40','41']
    elif _type==2:
        sizes=['41'] 
    elif _type==3:
        sizes=['16','40']
    elif _type==4:
        sizes=['15','25','27','30','32','33','36']
    for size in sizes:
        if _type==1:
            os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m export -f "C:\InnocentGrey\カルタグラ FHD\files\FONT\info{size}"  ')
            with open(rf'C:\InnocentGrey\カルタグラ FHD\files\FONT\info{size}_dicStr_sort2.txt','r',encoding='utf-16') as ff:
                infos=ff.read().split('\n')
        elif _type==2:
            os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m export -f "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\infosys{size}"  ')
            with open(rf'C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\infosys{size}_dicStr_sort2.txt','r',encoding='utf-16') as ff:
                infos=ff.read().split('\n')
        elif _type ==3:
            os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m export -f "C:\InnocentGrey\カルタグラ FHD\files\FONT_V\info{size}v"  ')
            with open(rf'C:\InnocentGrey\カルタグラ FHD\files\FONT_V\info{size}v_dicStr_sort2.txt','r',encoding='utf-16') as ff:
                infos=ff.read().split('\n')
        elif _type==4:
            os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m export -f "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\infosys{size}"  ')
            with open(rf'C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\infosys{size}_dicStr_sort2.txt','r',encoding='utf-16') as ff:
                infos=ff.read().split('\n')
        for i in range(2+len(basic), len(infos)-1):
            line=infos[i].split('\t')
            #print(i,newcharset[i-2])
            badchars='削時綾薫島馬慶のそ蒼'
            if _type==4 and i>=len(infos)-len(badchars)-1:
                char=badchars[i-(len(infos)-len(badchars)-1)]
            else:
                char=remap_charset2[newcharset[i-2]]
            line[1]=char
            line[2]=ord(char).to_bytes(2,'little').hex().upper()
            line[3]='0000'
            line[4]=('00%02x00'%int(size)).upper() 
            infos[i]='\t'.join(line)
        with open(f'newinfo{_type}.txt','w',encoding='utf-16') as ff:
            ff.write('\n'.join(infos))
          
        os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m import -f ".\newinfo{_type}.txt"   -o {size}')
        if _type==1:
            shutil.move(rf'newinfo{_type}.txt.info',rf"C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW\info{size}")
            #os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m import -f ".\newinfo{_type}.txt"   -o {size}')
        elif _type==2: 
            shutil.move(rf'newinfo{_type}.txt.info',rf"C:\InnocentGrey\カルタグラ FHD\files\SYSFONT_NEW\infosys{size}")
        elif _type==3: 
            shutil.move(rf'newinfo{_type}.txt.info',rf"C:\InnocentGrey\カルタグラ FHD\files\FONT_V_NEW\info{size}v")
        elif _type==4: 
            shutil.move(rf'newinfo{_type}.txt.info',rf"C:\InnocentGrey\カルタグラ FHD\files\SYSFONT_NEW\infosys{size}")
