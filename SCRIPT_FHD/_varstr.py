with open('SCRIPT_FHD/_varstr','rb') as ff:
    bs=ff.read()
import ctypes 
idx=0
target=[]
fw=open('text/_varstr','w',encoding='utf8')
while idx<len(bs):
    blocklength=ctypes.c_short.from_buffer_copy(bs[idx:idx+2]).value
    print(hex(blocklength))
    idx+=2
    target+=bs[idx:idx+6]
    print(bs[idx:idx+6].hex())
    idx+=6
    length=ctypes.c_ushort.from_buffer_copy(bs[idx:idx+2]).value
    print(hex(length))
    idx+=2
    if length:
        text=bs[idx:idx+length*2]
        print(1,text.decode('utf-16-le'),1)
        print('%04x'%idx+"|"+text.decode('utf-16-le'),file=fw)
        print('%04x'%idx+"|"+text.decode('utf-16-le'),file=fw)
        print('',file=fw)
        idx+=length*2+2
    else:
        pass
    