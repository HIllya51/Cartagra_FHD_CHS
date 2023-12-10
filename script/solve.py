
# int __thiscall sub_43CD60(int this, const char* a2) a2：s文件名
# ……
# for (i = 0; i < *(_DWORD*)(this + 6620); *v17 = ~*v17)
# {
#     v17 = (_BYTE*)(i + *(_DWORD*)(this + 6604));        (this + 6604)：.s文件内容指针
#     ++i;
# }
import os
for f in os.listdir('script_zh_not'):
    with open('script_zh_not/'+f,'rb') as ff:
        bs=ff.read()

    xx=b''
    for b in bs:  
        xx+= ((~(b))&0xff).to_bytes(1,'little')
    with open('script_zh/'+f,'wb') as ff:
        ff.write(xx)
def readopning(fname,cp):
    with open(fname,'rb') as ff:
        bs=ff.read()
    i=0
    texts=[]
    while i<len(bs):
        try:
            while 1:  
                if bs[i+1]!=0:break
                length=bs[i]
                if length<=10 or length>300:break
                length-=4
                string=bs[i+2:i+length]
                
                #print(hex(i),string.hex()) 
                for ii in range(1,5):
                    if bs[i+length+ii]!=0:
                        string=bs[i+2:i+length+ii+1] 
                    else: break 
                if 0 not in string:  
                    text=(string.decode(cp))  
                    texts.append(text)
                    i+=length
                break
        except IndexError:
            pass
        i+=1
    return texts
def readallstrings(fname,cp):
    if fname.endswith('opning.s'):return readopning(fname,cp)
    with open(fname,'rb') as ff:
        bs=ff.read()
    i=0
    texts=[]
    while i<len(bs):
        try:
            while 1:  
                if bs[i-2:i+1]!=b'\x00\x04\x00':break
                length=bs[i+1] 
                if length<=4 or length>300:break
                length-=4 
                string=bs[i+2:i+length] 
                for ii in range(1,5):
                    if bs[i+length+ii]!=0:
                        string=bs[i+2:i+length+ii+1] 
                    else: break 
                #print(hex(i),string.decode(cp), 0 not in string)
                if 0 not in string:  
                    text=(string.decode(cp))
                    
                    texts.append(text)
                    i+=length
                
                break
        except IndexError:
            pass
        i+=1
    return texts
 
for f in os.listdir('script_zh'):
    #if '0207-04-00.s'!=f:continue
    #if '0220-02-06.s'!=f:continue
    #print(f)
    with open('script_zh/'+f,'rb') as ff:
        zh=ff.read()
    with open('script_ja/'+f,'rb') as ff:
        ja=ff.read()
    
    _zh=(readallstrings('script_zh/'+f,'gbk'))
    _ja=(readallstrings('script_ja/'+f,'shiftjis'))
    errors=['肉棒が入る時には、ぐぷっと愛液は音を立て、出てくるときには薄紅い液体をまとわせて姿を見せる。','きゅ……。','遊女のような技巧が無いと思っていた。','恥ずかしがる事無く喘ぐ和菜の様子に喜び、締まりもどんどんよくなっていく。','しかしそれも根本からくる痛みで、先端や竿部分には絡みついてくる暖かい粘液と膣壁に快感だけが送られてくる。']
    for error in errors:    
        if error in _ja:
            _ja.pop(_ja.index(error))
    if len(_zh)!=len(_ja):
        print(f,len(_ja),len(_zh))
    fff2=open('script_pair/'+f+'.txt','w',encoding='utf8')

    for i in range(len(_zh)): 
        print(_ja[i],file=fff2)
        if '侐' in _zh[i]:
            if _zh[i][0]!='侐':
                #print(_zh[i])
                _zh[i]=_zh[i].replace('侐','♪')
            else:
                _zh[i]=_zh[i].replace('侐','♯')
        
        _zh[i]=_zh[i].replace('亹','＄')
         
        print(_zh[i],file=fff2)
        print('',file=fff2)
