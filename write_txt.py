import os
paths= "E:\qj\yolov7-main\VisDrone2019\images\\test\\"
f=open('test.txt', 'w')
filenames=os.listdir(paths)
filenames.sort()
for filename in filenames:

    out_path="E:\qj\yolov7-main\VisDrone2019\images\\test\\" + filename
    print(out_path)
    f.write(out_path+'\n')
f.close()

