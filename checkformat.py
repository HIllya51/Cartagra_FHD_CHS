import os, re
for f in os.listdir('SCRIPT_FHD/text'):
    #if f!='0206-05-03':continue
    #if f!='a2-7-1ED02':continue
    if f=='_varstr':continue
    with open('SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
        bs=ff.read()
    if len(bs)==0:continue
    if bs[0]=='\ufeff':
        with open('SCRIPT_FHD/text/'+f,'w',encoding='utf8') as ff:
            ff.write(bs[1:])
    with open('SCRIPT_FHD/text/'+f,'r',encoding='utf8') as ff:
        lines=ff.read().split('\n')
    with open('SCRIPT_FHD/text2/'+f,'r',encoding='utf8') as ff:
        lines2=ff.read().split('\n')
    with open('SCRIPT_FHD/SCRIPT_FHD/'+f,'rb') as ff:
        cankao=ff.read()
    for i in range(len(lines)-1):
        if i%3==2:
            if lines[i]!='':raise Exception(i,f)
        else:
            if lines[i]=='':raise Exception(i,f)
         
        if i%3 in [0,2] and lines[i]!=lines2[i]:
            print( lines[i])
            print( lines2[i])
            print(list(lines[i]))
            print(list(lines2[i]))
            raise Exception(i,f)
        elif i%3==1 :
            
            if lines2[i].endswith('＄') and not lines[i].endswith('＄'):
                print( lines[i])
                print( lines2[i])  
            lines[i]=lines[i].replace('―。','―')
            lines[i]=lines[i].replace('—。','—')
            lines[i]=lines[i].replace('。」','」')
            if '—' in lines[i]:
                lines[i] = re.sub(r'(?<!—)(—)(?!—)', '——', lines[i])
                
    with open('SCRIPT_FHD/text/'+f,'w',encoding='utf8') as ff:
        ff.write('\n'.join(lines))