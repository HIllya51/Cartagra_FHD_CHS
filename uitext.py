with open(r'C:\InnocentGrey\カルタグラ FHD\カルタグラ FHD.exe','rb') as ff:
    bs=ff.read()
def find(base,text,pf):
    idxbase=bs.find(text.encode('utf8'))
    save=[]
    idx=idxbase
    while 1:
        if bs[idx]:
            save.append(bs[idx])
        else:
            if len(save):
                try:
                    print(hex(base+idx-len(save)-idxbase)[2:].upper()+'|'+ bytes(save).decode('utf8').replace('\n','＄'),file=pf)
                    print(hex(base+idx-len(save)-idxbase)[2:].upper()+'|'+ bytes(save).decode('utf8').replace('\n','＄'),file=pf)
                    print('',file=pf)
                except:
                    break
            save=[]
        idx+=1
    
    save=[]
    idx=idxbase-1
    while 1:
        if bs[idx]: 
            save.insert(0,bs[idx])
        else:
            if len(save): 
                try:
                    print(hex(base+idx+1-idxbase)[2:].upper()+'|'+ bytes(save).decode('utf8').replace('\n','＄'),file=pf)
                    print(hex(base+idx+1-idxbase)[2:].upper()+'|'+ bytes(save).decode('utf8').replace('\n','＄'),file=pf)
                    print('',file=pf)
                except:
                    break
            save=[]
        idx-=1
#pf=open('uitext.txt','w',encoding='utf8')
#find(0x3fc5e0,'セーブしな',pf)
#find(0x3fc5e0+0x7FF76F42F528-0x7FF76F42C5E0,'メッセージ送り',pf)
def xx(text,leak=False):
    idx1=0
    while 1:
        if leak:
            idx1=bs.find(text.encode('utf8'),idx1+1)
        else:
            idx1=bs.find(b'\x00'+text.encode('utf8')+b'\x00',idx1+1)
        if idx1==-1:break
        print(idx1)
        idx2=bs.find( 'セーブしな'.encode('utf8')  )
        print(hex(0x3fc5e0+idx1+1-leak-idx2)[2:].upper()+'|'+text)

xx('OK')
xx('初期設定に戻す') 
xx('閉じる') 
xx('なし') 
xx('このページを初期設定に戻しますか？') 
xx('ロードしますか？') 
xx('セーブしますか？') 
xx('セーブが完了しました。') 
xx('上書きしますか？')
xx('音声再生')
xx('シーン再生を終了しますか？')
#pf=open('uitext1.txt','w',encoding='utf8')
#find(0x3D4F88,'上書きしますか？',pf)