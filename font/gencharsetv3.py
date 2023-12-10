import os,shutil,json

remap_charset2={}
for _type in [2,1,3]:
    
    #print((chars))
    #newcharset=origin+''.join(list(chars-set(origin)))
    
    if _type==1:    
        sizes=['12','16','33','40','41']
    elif _type==2:
        sizes=['41'] 
    elif _type==3:
        sizes=['16','40']
    for size in sizes:
        if _type==1:
            chars=set()
            with open(r'info12_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
                origin=ff.read()

            for f in os.listdir('../SCRIPT_FHD/text'):
                with open('../SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
                    newtexts=ff.read().split('\n') 
                chars=chars.union(set(''.join(newtexts)))
        elif _type==2:
            chars=set()
            with open(r'infosys41_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
                origin=ff.read()

            for f in os.listdir('../SCRIPT_FHD/text'):
                if f!='0000-op1':continue
                
                with open('../SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
                    newtexts=ff.read().split('\n') 
                chars=chars.union(set(''.join(newtexts)))
        elif _type==3:
            with open(r'info40v_string_sort_utf-8.txt','r',encoding='utf-8-sig') as ff:
                origin=ff.read()
        origin=list(origin) 
    
        chars=sorted(chars)
        print(len(chars))
        if _type==1:
            os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m export -f "C:\InnocentGrey\カルタグラ FHD\files\FONT\info{size}"  ')
            with open(rf'C:\InnocentGrey\カルタグラ FHD\files\FONT\info{size}_dicStr_sort2.txt','r',encoding='utf-16') as ff:
                infos=ff.read().split('\n')
        elif _type==2:
            os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m export -f "C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\info{size}"  ')
            with open(rf'C:\InnocentGrey\カルタグラ FHD\files\SYSFONT\infosys{size}_dicStr_sort2.txt','r',encoding='utf-16') as ff:
                infos=ff.read().split('\n')
        elif _type==3:
            os.system(rf'.\LucaSystemTool\LucaSystemTools.exe -t info -m export -f "C:\InnocentGrey\カルタグラ FHD\files\FONT_V\info{size}v"  ')
            with open(rf'C:\InnocentGrey\カルタグラ FHD\files\FONT_V\info{size}v_dicStr_sort2.txt','r',encoding='utf-16') as ff:
                infos=ff.read().split('\n')
        if _type in [1,2]:
            for c in chars:
                ok=False
                if c in remap_charset2:
                    for i in range(len(origin)):
                        _idx=len(origin)-1-i
                        if (origin[_idx]==remap_charset2[c]):
                            origin[_idx]=c  
                            # _line=infos[_idx].split('\t')
                            # #_line[1]=c
                            # #_line[2]=(ord(c)).to_bytes(2,'little').hex().upper()
                            # _line[-1]=('00%02x00'%int(size)).upper() 
                            # _line[-2]=('0000' ).upper() 
                            # infos[_idx]='\t'.join(_line)
                            ok=True
                            break
                if ok:
                    continue
                if c not in origin :
                    #print(c)
                    for i in range(len(origin)):
                        _idx=len(origin)-1-i
                        if origin[_idx] not in chars :
                            remap_charset2[c]=origin[_idx]
                            origin[_idx]=c  
                            
                            # _line=infos[_idx].split('\t')
                            # #_line[1]=c
                            # #_line[2]=(ord(c)).to_bytes(2,'little').hex().upper()
                            # _line[-1]=('00%02x00'%int(size)).upper() 
                            # _line[-2]=('0000' ).upper() 
                            # infos[_idx]='\t'.join(_line) 
                            break 
            for i in range(2,len(infos)-1): 
                _line=infos[i].split('\t')  
                if _line[1] in list(remap_charset2.values()):
                    _line[-1]=('00%02x00'%int(size)).upper() 
                    _line[-2]=('0000' ).upper() 
                    infos[i]='\t'.join(_line)  

        elif _type==3:
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
    # with open('charset.txt','w',encoding='utf8') as ff:
    #     ff.write( (newcharset))
    # for f in ['12','16','33','40','41']:#,'11','72']: 
    #     os.system(rf'.\LuckSystem.exe font edit --redraw --input_charset ".\charset.txt" -f ".\SourceHanSansCN-Regular.ttf" -s "C:\InnocentGrey\カルタグラ FHD\files\FONT\明朝{f}" -S "C:\InnocentGrey\カルタグラ FHD\files\FONT\info{f}" -o "C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW\明朝{f}" -O "C:\InnocentGrey\カルタグラ FHD\files\FONT_NEW\info{f}"')
    # #LuckSystem.exe font edit --redraw 这个程序弄出来的字符集前面多个东西。