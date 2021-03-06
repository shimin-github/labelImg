import os
import os.path
import xml.dom.minidom
import sys
import cv2

def Transform_txt_xml(pre_file,after_file):
    line=[]
    isExists = os.path.exists(after_file)
    if not isExists:
        os.makedirs(after_file)
    
    files1 =os.listdir(pre_file)
    count = 0
    for xmlFile in files1:
        with open(os.path.join(pre_file,xmlFile),'r') as fs:
            managerList=[]
            doc = xml.dom.minidom.Document()
            root = doc.createElement('Recognition') 
            root.setAttribute('type', 'face') 
            doc.appendChild(root)
            
            str=fs.read()
            line=str.split()
            
            for i in range(0,int(line[1])):
                managerList.append([{'xmin':line[2+i*4],'ymin':line[3+i*4],'xmax':line[4+i*4],'ymax':line[5+i*4]}])
            
            for i in managerList :
                for j in range(len(i)):
                    nodeManager = doc.createElement('bndbox')
                    nodeXmin = doc.createElement("xmin")
                    nodeXmin.appendChild(doc.createTextNode(i[j]['xmin']))
                    nodeYmin = doc.createElement("ymin")
                    nodeYmin.appendChild(doc.createTextNode(i[j]['ymin']))
                    nodeXmax = doc.createElement("xmax")
                    nodeXmax.appendChild(doc.createTextNode(i[j]['xmax']))
                    nodeYmax = doc.createElement("ymax")
                    nodeYmax.appendChild(doc.createTextNode(i[j]['ymax']))
        
                 
                    nodeManager.appendChild(nodeXmin)
                    nodeManager.appendChild(nodeYmin)
                    nodeManager.appendChild(nodeXmax)
                    nodeManager.appendChild(nodeYmax)
                    root.appendChild(nodeManager)
    
            pathn=os.path.join(after_file,line[0])
            #pathn=os.path.join(pathn,".xml")
            pathn+=".xml"
            fp = open(pathn, 'w')
            doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
            count += 1
    print 'Transform_txt_xml() is OK'
    print "%d txt files have been convert to xml."%count

def Transform_xml_txt_wh(pre_file,after_file):

    isExists = os.path.exists(after_file)
    if not isExists:
        os.makedirs(after_file)
        
    xmlfiles =os.listdir(pre_file)
    count = 0
    for xmlFile in xmlfiles:
        if not os.path.isdir(xmlFile) and xmlFile.endswith('.xml'):
            dom=xml.dom.minidom.parse(os.path.join(pre_file, xmlFile))
            
            root=dom.documentElement
 
            print(root.getElementsByTagName('xmin'))
            print(len(root.getElementsByTagName('xmin')))
            if len(root.getElementsByTagName('xmin'))==0:
                continue
            filename=root.getElementsByTagName('filename')
            xmin=root.getElementsByTagName('xmin')
            xmax=root.getElementsByTagName('xmax')
            ymin=root.getElementsByTagName('ymin')
            ymax=root.getElementsByTagName('ymax')
            
            rectnum = len(xmin)
        
    #check datas
            n0=filename[0]
            Name = n0.firstChild.data
            meg = Name+' '+str(rectnum)
            
            for i in range(0,rectnum):
                n1=xmin[i]
                n2=xmax[i]
                n3=ymin[i]
                n4=ymax[i]
                Xmin = n1.firstChild.data
                Xmax = n2.firstChild.data
                Ymin = n3.firstChild.data
                Ymax = n4.firstChild.data
                a= int(Xmax)-int(Xmin)
                b= int(Ymax)-int(Ymin)
            
                #writing txt file to specific location
                meg +=' ' + str(Xmin)+' '+str(Ymin)+' '+str(a)+' '+str(b)   
            full_path = after_file + Name + '.txt' 
            file = open(full_path,'w')             
            print "txt message: ", meg
            file.write(meg)
            file.close()
            count+=1
    print 'Transform_xml_txt_wh() is OK'
    print "%d xml files have been convert to txt."%count

def Transform_xml_txt_xy(pre_file,after_file):

    isExists = os.path.exists(after_file)
    if not isExists:
        os.makedirs(after_file)
    
    xmlfiles =os.listdir(pre_file)
    count = 0
    for xmlFile in xmlfiles:
        if not os.path.isdir(xmlFile) and xmlFile.endswith('.xml'):
            
            dom=xml.dom.minidom.parse(os.path.join(pre_file,xmlFile))
            
            root=dom.documentElement
 
            print(root.getElementsByTagName('xmin'))
            print(len(root.getElementsByTagName('xmin')))
            if len(root.getElementsByTagName('xmin'))==0:
                continue
            filename=root.getElementsByTagName('filename')
            xmin=root.getElementsByTagName('xmin')
            xmax=root.getElementsByTagName('xmax')
            ymin=root.getElementsByTagName('ymin')
            ymax=root.getElementsByTagName('ymax')
            
            rectnum = len(xmin)
            
        
    #check datas
            n0=filename[0]
            Name = n0.firstChild.data
            meg = Name+' '+str(rectnum)
            
            for i in range(0,rectnum):
                n1=xmin[i]
                n2=xmax[i]
                n3=ymin[i]
                n4=ymax[i]
                Xmin = n1.firstChild.data
                Xmax = n2.firstChild.data
                Ymin = n3.firstChild.data
                Ymax = n4.firstChild.data
            
                #writing txt file to specific location
                meg +=' ' + str(Xmin)+' '+str(Ymin)+' '+str(Xmax)+' '+str(Ymax) 
            full_path = after_file + Name + '.txt' 
            file = open(full_path,'w')
            print "txt message: ", meg             
            file.write(meg)
            file.close()
            count+=1
        
    print 'Transform_xml_txt_xy() is OK'
    print "%d xml files have been convert to txt."%count
    
    
def detectimg(classifer, imagepath):
    image = cv2.imread(imagepath)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
 
    objects = classifer.detectMultiScale(
            gray,
            scaleFactor = 1.15,
            minNeighbors = 5,
            minSize = (5,5),
            flags = cv2.CASCADE_SCALE_IMAGE
    )
    for i in range(0,len(objects)):
        objects[i][2] = objects[i][0] + objects[i][2]
        objects[i][3] = objects[i][1] + objects[i][3]
    
    imgFile = str(imagepath).split('\\')[-1]
    meg = imgFile[:-4]
    length = len(objects)
    meg = meg + ' ' + str(length)
    if length == 0:
        return 0
        #continue
    else:
        for i in range(0,length):
            for j in range(0, 4):
                meg = meg+' '+ str(objects[i][j])
        print (meg)
        return meg
    #for(x,y,w,h) in hands:
    # cv2.rectangle(image,(x,y),(x+w,y+w),(0,255,0),2)
        #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
 
    #cv2.imshow("Find Hands!",image)
    #cv2.waitKey(0)

def detect(imgDirPath, cascadeXmlPath, testTxtPath):
    
    imgdirpath=imgDirPath
    txtdirpath=testTxtPath
    files = os.listdir(imgdirpath)
    cascade = cv2.CascadeClassifier(cascadeXmlPath)
    
    isExists = os.path.exists(txtdirpath)
    if not isExists:
        os.makedirs(txtdirpath)
    
    for imgFile in files:
        if not os.path.isdir(imgFile) and (imgFile.endswith('.png') or imgFile.endswith('.jpg')):
            imagePath = os.path.join(imgdirpath, imgFile)
            #get the test result
            testResult = detectimg(cascade, imagePath)
            if testResult != 0:
                print (testResult)
                txtFilePath = os.path.join(txtdirpath, imgFile[:-4]+'.txt')
                file = open(txtFilePath,'w')
                file.write(testResult)
                file.close()
