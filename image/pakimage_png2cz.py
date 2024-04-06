import os,sys,shutil,cv2
from PIL import Image
for _dir in ['OTHCG','PARTS','SYSCG','BGCG']:
    _path=r'C:\InnocentGrey\カルタグラ FHD\files\image\\'+_dir
    for imagepath in os.listdir(_path+'_PNG'):
        pngimagepath=os.path.join(_path+'_PNG',imagepath)
        #pngimagepath=os.path.join(_path,imagepath)
        czimagepath=os.path.join(_path, imagepath[:-4])
        czimagepng=os.path.join(_path, imagepath)
        outputczpath=os.path.join(_path+'_NEW', imagepath[:-4])
        origin=Image.open(czimagepng)
        newimg=Image.open(pngimagepath)
        if origin.size!=newimg.size:
            print(pngimagepath,origin.size,newimg.size)
            raise Exception()
        if os.path.exists(outputczpath) and  os.path.getmtime(outputczpath)>max(os.path.getmtime(pngimagepath),os.path.getctime(pngimagepath)):
            continue
        with open(czimagepath,'rb') as ff:
            magic=ff.read(3).decode()
        if magic=='CZ4' or magic=='CZ3':
            
            print(czimagepath,magic )
            os.system(rf'.\czximage\build\Release\image2cz.exe "{czimagepath}" "{pngimagepath}" "{outputczpath}"')
            print(czimagepath,magic ,'ok')
        else: #测试可以全都打成CZ4格式的
            print(czimagepath,magic )
            os.system(rf'.\czximage\build\Release\image2cz.exe "C:\InnocentGrey\カルタグラ FHD\files\image\OTHCG\03b" "{pngimagepath}" "{outputczpath}"')
        # if _dir=='OTHCG':
        #     shutil.copy(outputczpath, os.path.join(r'C:\InnocentGrey\カルタグラ FHD\CHSPAK\OTHCG', imagepath[:-4]))