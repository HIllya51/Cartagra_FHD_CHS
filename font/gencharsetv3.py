import os,shutil,json

remap_charset2={}
remap_charset4={}
r_remap_charset4={}
            
for _type in  [2,4,1,3]:
    
    #print((chars))
    #newcharset=origin+''.join(list(chars-set(origin)))
    
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
            chars=set()
            with open(r'info12_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
                origin=ff.read()

            for f in os.listdir('../SCRIPT_FHD/text'):
                with open('../SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
                    newtexts=ff.read().split('\n') 
                for i in range(len(newtexts)):
                    if i%3!=1:continue
                    chars=chars.union(set(''.join(newtexts))) 
        elif _type==2:
            chars=set()
            with open(r'infosys41_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
                origin=ff.read()

            for f in os.listdir('../SCRIPT_FHD/text'):
                if f!='0000-op1':continue
                
                with open('../SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
                    newtexts=ff.read().split('\n') 
                for i in range(len(newtexts)):
                    if i%3!=1:continue
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
            for i in range(len(newtexts)):
                if i%3!=1:continue
                chars=chars.union(set(''.join(newtexts)))
        origin=list(origin) 
    
        chars=sorted(chars)
        print(len(chars))
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
            os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m export -f "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\infosys{size}v"  ')
            with open(rf'C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\infosys{size}_dicStr_sort2.txt','r',encoding='utf-16') as ff:
                infos=ff.read().split('\n')
        if _type in [1,2 ]:
            for c in chars:
                 
                ok=False
                if c in remap_charset2:
                    for i in range(len(origin)):
                        _idx=len(origin)-1-i
                        if (origin[_idx]==remap_charset2[c]):
                            origin[_idx]=c   
                            ok=True
                            break 
                if ok:
                    continue
                if c not in origin :
                    #print(c)
                    for i in range(len(origin)):
                        _idx=len(origin)-1-i
                        if origin[_idx] not in chars and (origin[_idx] not in ['n','o','l']) and origin[_idx] not in r_remap_charset4:
                            remap_charset2[c]=origin[_idx]
                            r_remap_charset4[origin[_idx]]=c
                            origin[_idx]=c  
                             
                            break 
            if 1:
              
                for i in range(2,len(infos)-1): 
                    _line=infos[i].split('\t')  
                    if _line[1] in list(remap_charset2.values()) or _line[1] in chars:
                        _line[-1]=('00%02x00'%int(size)).upper() 
                        _line[-2]=('0000' ).upper() 
                        infos[i]='\t'.join(_line)  

        elif _type in [4]:
            for c in chars:
                 
                ok=False
                if c in remap_charset4:
                    for i in range(len(origin)):
                        _idx=len(origin)-1-i
                        if (origin[_idx]==remap_charset4[c]):
                            origin[_idx]=c   
                            ok=True
                            break 
                if ok:
                    continue
                if c not in origin :
                    #print(c)
                    for i in range(len(origin)):
                        _idx=len(origin)-1-i
                        if origin[_idx] not in chars and (origin[_idx] not in ['n','o','l']) and origin[_idx] not in r_remap_charset4:
                            remap_charset4[c]=origin[_idx]
                            r_remap_charset4[origin[_idx]]=c
                            origin[_idx]=c  
                             
                            break 
            if 1:
                for i in range(2,len(infos)-1): 
                    _line=infos[i].split('\t')  
                    if 1:#_line[1] in list(remap_charset4.values()):
                        try: 
                            #r_remap_charset4.get(_line[1],_line[1]).encode('ascii')
                            _line[1].encode('ascii')
                            isascii=True
                        except:
                            isascii=False 
                        if _line[1] in  '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM()' : 
                            #_line[-1]=('00%02x00'%(int(size)//2)).upper() 
                            pass
                            #print(r_remap_charset4.get(_line[1],_line[1]),_line[-1]
                        elif _line[1] in ':':
                            _line[-1]=('00%02x00'%(int(size)//2)).upper() 
                        else:
                            _line[-1]=('00%02x00'%int(size)).upper() 
                        _line[-2]=('0000' ).upper() 
                        infos[i]='\t'.join(_line)   
        elif _type in [3]:
            for i in range(len(origin)) :
                for k in remap_charset2:
                    if remap_charset2[k]==origin[i]:
                        origin[i]=k 
                        _line=infos[i+2].split('\t')  
                        _line[-1]=('00%02x00'%int(size)).upper() 
                        _line[-2]=('0000' ).upper() 
                        infos[i+2]='\t'.join(_line)  
                        break 
        with open(f'remap_charset2.txt','w',encoding='utf8') as ff:
            ff.write(json.dumps(remap_charset2,ensure_ascii=False))
        with open(f'remap_charset4.txt','w',encoding='utf8') as ff:
            ff.write(json.dumps(remap_charset4,ensure_ascii=False))
        with open(f'remap_charset{_type}2.txt','w',encoding='utf8') as ff:
            ff.write(json.dumps(remap_charset2,ensure_ascii=False))
        with open(f'newcharset{_type}.txt','w',encoding='utf-8-sig') as ff:
            ff.write(''.join(origin))
        
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
    # with open('charset.txt','w',encoding='utf8') as ff:
    #     ff.write( (newcharset))
    # for f in ['12','16','33','40','41']:#,'11','72']: 
    #     os.system(rf'.\LuckSystem.exe font edit --redraw --input_charset ".\charset.txt" -f ".\SourceHanSansCN-Regular.ttf" -s "C:\InnocentGrey\カルタグラ FHD\files\FONT\明朝{f}" -S "C:\InnocentGrey\カルタグラ FHD\files\FONT\info{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW\明朝{f}" -O "C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW\info{f}"')
    # #LuckSystem.exe font edit --redraw 这个程序弄出来的字符集前面多个东西。