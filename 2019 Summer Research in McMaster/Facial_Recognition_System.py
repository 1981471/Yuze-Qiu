#! usr/bin/env python
#codnig=utf-8
import cv2
import sys
import time
import numpy as np
import os
from PIL import Image
import serial
import RPi.GPIO as GPIO

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')
model=cv2.face.createLBPHFaceRecognizer()
model.load('/home/pi/FRP/trainer/trainer.yml')
path='/home/pi/FRP/dataset'
trainer_path='/home/pi/FRP/trainer'

#open named port at 9600,1s timeot
#camera=cv2.VideoCapture(0)
font=cv2.FONT_HERSHEY_SIMPLEX
t_start=time.time()
sPin=11;Gpin=12;Rpin=13
global fps
global count

def bubble_sort(alist):
    for j in range(0,len(alist) - 1):
        for i in range(0,len(alist) - 1 - j):
             if alist[i] > alist[i + 1]:
                alist[i],alist[i + 1] = alist[i + 1],alist[i]
             else:
                continue
#             print(alist)
    return alist[len(alist)-1]

def search_name(path):
    name=[]
    docpaths=[os.path.join(path,f) for f in os.listdir(path)]
    for docpath in docpaths:
        name.append("")
    for docpath in docpaths:
        imagepaths=[os.path.join(docpath,f) for f in os.listdir(docpath)]
        for imagepath in imagepaths:
            id = int(os.path.split(imagepath)[-1].split("_")[0])
        name[id]=os.path.split(docpath)[1]
#    print "name=",name
    return name

def getfaces_recog(img):
        img = cv2.flip(img, 1)  # Flip vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),)
        return img,gray,faces

def get_faces(img):
    faces_w=[];faces_h=[]
#    print "img0=",img
    img=cv2.flip(img,1);#print "img.flip=",img
    cv2.imshow("camera",img)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);#print "gray=",gray
    faces=face_cascade.detectMultiScale(gray,1.3,5);#print "faces=",faces
    cv2.waitKey(10)
    if len(faces)==0:
        print "no faces!!"
    if (len(faces)!=0):
        for (x,y,w,h) in faces:
            faces_w.append(w);faces_h.append(h);
            print "faces_w=",faces_w; print "faces_h=",faces_h
            w2=bubble_sort(faces_w);h2=bubble_sort(faces_h)
        for (x,y,w,h) in faces:
           if w==w2 & h==h2:
                x2=x;y2=y
        faces=[[x2,y2,w2,h2]];print "faces_max=",faces
    return faces,gray,img

def draw_frames(faces,gray,img,count,face_id,num,supply,i):
    if supply[0] == str(0):
        for x,y,w,h in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(192,220,240),2)
            face_gray=gray[y:y+h,x:x+w]
          #  print "face_gray=",face_gray
            access=os.path.exists('/home/pi/FRP/dataset/'+str(face_id))
            if(access==False):
                os.mkdir('/home/pi/FRP/dataset/'+str(face_id))
    #        cv2.SaveImage("dataset/User."+str(face_id)+"."+str(count)+".jpg",face_gray)
                cv2.imwrite('/home/pi/FRP/dataset/'+str(face_id)+'/'+str(num)+"_"+str(count)+".pgm",face_gray)
            elif(access==True):
                cv2.imwrite('/home/pi/FRP/dataset/'+str(face_id)+'/'+str(num)+"_"+str(count)+".pgm",face_gray)
            cv2.imshow("camera",img)
            count+=1
        print "count=",count
    if supply[0] !=str(0) :
        print "supply=",supply
        for x,y,w,h in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(192,220,240),2)
            face_gray=gray[y:y+h,x:x+w];print "now_id=",supply[i]
          #  print "face_gray=",face_gray
            access=os.path.exists('/home/pi/FRP/dataset/'+str(face_id))
            if(access==False):
                os.mkdir('/home/pi/FRP/dataset/'+str(face_id))
    #        cv2.SaveImage("dataset/User."+str(face_id)+"."+str(count)+".jpg",face_gray)
                cv2.imwrite('/home/pi/FRP/dataset/'+str(face_id)+'/'+str(supply[i])+".pgm",face_gray)
                print "whether=",os.path.exists('/home/pi/FRP/dataset/'+str(face_id)+'/'+str(supply[i])+".pgm")
            elif(access==True):
                cv2.imwrite('/home/pi/FRP/dataset/'+str(face_id)+'/'+str(supply[i])+".pgm",face_gray)
                print "whether=",os.path.exists('/home/pi/FRP/dataset/'+str(face_id)+'/'+str(supply[i])+".pgm")
            cv2.imshow("camera",img)
            count+=1;i=i+1
        print "count=",count
    return count,i

def getImageAndLabels(path):
    facesamples=[];ids=[]
    docpaths=[os.path.join(path,f) for f in os.listdir(path)]
    for docpath in docpaths:
        print "docpath=",docpath
        name=os.path.split(docpath)[1];print "train name=",name
        imagepaths=[os.path.join(docpath,f) for f in os.listdir(docpath)]
        for imagepath in imagepaths:
#            print "imagepath=",imagepath
            PIL_img = Image.open(imagepath).convert('L');#print "PIL_img=",PIL_img
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagepath)[-1].split("_")[0])
#            print "id.train=",id
            faces = face_cascade.detectMultiScale(img_numpy);#print str(name)+".faces=",faces
            for(x,y,w,h) in faces:
                facesamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
#    print "ids=",ids;#print "facesamples=",facesamples
    return facesamples,ids

def check_size(path,face_id):
    docpath=os.path.join(path,face_id)
    imagepaths=[os.path.join(docpath,f) for f in os.listdir(docpath)]
    print "whole image=",len(imagepaths)
    face_sizeW=[];face_sizeH=[];size=[];max=[];false_id=[]
    flagw2=0;flagh=0
    for imagepath in imagepaths:
        PIL_img=Image.open(imagepath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')
        id = str(os.path.split(imagepath)[-1].split(".")[0]);#print "id.check_size=",id
        faces=face_cascade.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            face_sizeW.append(w);face_sizeH.append(h);
            size.append([id,w,h]);#print "now size=",[id,w,h]
#bubble_sort(face_sizeW);bubble_sort(face_sizeH)
#    print "size=",size;print "size_length=",len(size)
#    print "face_sizeW=",face_sizeW;print "face_sizeH=",face_sizeH
 #   flagw2=face_sizeW[0];flagh=face_sizeH[0]
 #   for i in range(0,len(face_sizeW)-2):
 #       if (face_sizeW[i+1]-face_sizeW[i])>0:
 #           flagw2 = face_sizeW[i+1];print "flagw2=",flagw2
 #   for j in range(0,len(face_sizeH)-2):
 #       if (face_sizeH[j+1] - face_sizeH[j])>0:
 #           flagh = face_sizeH[j+1];print "flagh=",flagh
    flagw2=bubble_sort(face_sizeW);flagh=bubble_sort(face_sizeH)
    print "max=",[flagw2,flagh];#print size
    for (id,w,h) in size:
        print "get in,id=",id,"w=",w,"h=",h,"flagw,flagh=",flagw2,flagh
        if w<=(flagw2-50) and h<=(flagh-50) :
            print "false_id",id,"false_w=",w,"false_h=",h
            exist=os.path.exists('/home/pi/FRP/dataset/'+str(face_id)+'/'+str(id)+'.pgm')
            print exist            
            if exist==True:    
                os.remove('/home/pi/FRP/dataset/'+str(face_id)+'/'+str(id)+'.pgm' )
                false_id.append(id)
            if exist==False:
                continue
    imagepaths=[os.path.join(docpath,f) for f in os.listdir(docpath)]
    l=len(imagepaths);print "l=",l,"id=",false_id
    return l,false_id

def reload_trainer(path):
    faces,ids=getImageAndLabels(path)
    model.train(faces,np.array(ids))
    model.save('/home/pi/FRP/trainer/trainer.yml')
    print "Reload 'trainer.yml' successful"


if __name__=='__main__':
    print "open camera & reading local database, wait minutes..."
    camera=cv2.VideoCapture(0)
    reload_trainer(path)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,480)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,320)
    minW = 0.1 * camera.get(3)
    minH = 0.1 * camera.get(4)
    names=search_name(path);print "initial names=",names
    idx=m=0;name_id=str(0);confidence=confidence2=0;unknown_time=error_time=0;car='0';reload=0
    while True:
        names=search_name(path);
        if reload!=0:
            print "Present names=",names
        ret, img = camera.read()
        img,gray,faces=getfaces_recog(img)
        cv2.imshow('camera',img)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idx, confidence = model.predict(gray[y:y + h, x:x + w])
            print "confidence=",confidence
            print "idx=",idx
        # Check if confidence is less them 100 ==> "0" is perfect match
            if ((confidence < 80) & (error_time<4)):
                name_id = names[idx]
                confidence2 = "  {0}%".format(round(100 - confidence))
                print "guessed name:",name_id;print "possibility=",confidence2
                cv2.putText(img, str(name_id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence2), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                cv2.imshow('camera', img)
                answer=raw_input("Are you "+str(name_id)+"? [y/n]")
                if answer == "n":
                    error_time=error_time+1                    
                    if error_time==4:
                        print "very sorry! I'm a little confused...Would you mind me acknowledge you again?"
                    else:
                        print "sorry, re-recognition"                    
                    continue
                if answer =="y":
                    m=1;
                    print "Hello, Mr./Miss "+str(name_id)+"! What can I do for you?";
#                    car=car_start()
#                    if (car=='y'):
#                        return1=car_back()
#                        if return1=='y':
                    #car=car_start()
                    #return1=car_back()
                    print "continue"
                    continue
            if (confidence > 80 or error_time>=4) :
                name_id = "unknown";confidence=float(confidence)
                confidence2 = "  {0}%".format(round(100 - confidence))
                print "name:",name_id;print "possibility=",confidence2
                unknown_time=unknown_time+1
                if (unknown_time%3==0 or error_time>=4):
                    print "Sorry, maybe I didn't see you before. Would you like to let me remember you?[y/n]"
                    answer2=raw_input()
                    if answer2=="y":
                        print "initializing, please wait some seconds\n"
                        camera.set(cv2.CAP_PROP_FRAME_WIDTH,480)
                        camera.set(cv2.CAP_PROP_FRAME_HEIGHT,320)
                        count=0;id_cards=[];num=0;supply=[str(0),];bc=0
                        aa=[os.path.join(path,f) for f in os.listdir(path)]
                        num=len(aa) ;print "number of recorded people is ",num
                        face_id=raw_input("\n Please give me your name:")
                        check=os.path.exists('/home/pi/FRP/dataset/'+str(face_id))
                        if check==True:
                            i=raw_input("Are you sure to cover your previous record? [y/n]\n")
                            if i=="y":
                                docpath=os.path.join(path,face_id)
                                imagepaths=[os.path.join(docpath,f) for f in os.listdir(docpath)]
                                for imagepath in imagepaths:
                                    id = str(os.path.split(imagepath)[-1].split("_")[0])
                                print "start to record your face, please take off your glasses and stand alone...\n"
                                while (True):
                                    ret,img=camera.read()
                        #           print "read img=",img
                                    faces,gray,img=get_faces(img)
                                    count,bc=draw_frames(faces,gray,img,count,face_id,id,supply,bc)
                                    k=cv2.waitKey(100) & 0xff
                                    if(k==27):
                                        break
                                    elif(count==100):
                                        count,supply=check_size(path,face_id)
                                        if count==100:
                                            break
                                        if count<100:
                                            bc=0;continue
                                        if count>100:
                                             print "error!!!!";break
                                print " new dataset is ok\n"
                            if i=="n":
                                print "ok, skip to training"
                        if check==False:
                            print "start to record your face, please take off your glasses and stand alone...\n"
                            while (True):
                                ret,img=camera.read()
                    #           print "read img=",img
                                faces,gray,img=get_faces(img)
                                count,bc=draw_frames(faces,gray,img,count,face_id,num,supply,bc)
                                k=cv2.waitKey(100) & 0xff
                                if(k==27):
                                    break
                                elif(count==100):
                                    count,supply=check_size(path,face_id)
                                    if count==100:
                                        break
                                    if count<100:
                                        bc=0;continue
                                    if count>100:
                                        print "error!!!!";break                
                            print " new dataset is ok\n"
#                    camera.release()
#                    cv2.destroyAllWindows()
                        print "it needs some time to train, please wait\n"
                        faces,ids=getImageAndLabels(path)
                        model.train(faces,np.array(ids))
                        model.save('/home/pi/FRP/trainer/trainer.yml')
                        print "faces are trained".format(len(np.unique(ids)))
                        unknown_time=error_time=0
                        reload+=1
                    if answer2=="n":
                        print "OK, have a good day!"
                        error_time=0
            cv2.putText(img, str(name_id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence2), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
#            if m==1:
#                break
        cv2.imshow('camera', img)
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27 :#or m==1:
            break
# Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
#    camera.release()
#    cv2.destroyAllWindows()

