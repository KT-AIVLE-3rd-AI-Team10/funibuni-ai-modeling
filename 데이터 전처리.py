import os,json
import glob,shutil

#json 파일 경로 지정
json_path = '/content/drive/MyDrive/BIG_PROJECT/labels/'
temp_list = ['train','val']

#json 파일 txt 파일 변환 및 라벨링 뽑기
# train
for i in os.listdir('/content/drive/MyDrive/BIG_PROJECT/labels/train'):
    with open('/content/drive/MyDrive/BIG_PROJECT/labels/train/'+i, encoding='UTF-8') as json_file:
        data=json.load(json_file)
        bounding = data['Bounding']
        {0: '의자', 1: '티비', 2: '자전거', 3: '선풍기', 4: '소파', 5: '책상', 6: '서랍장', 7: '화분', 8: '항아리', 9: '침대', 10: 'ston_jade_bed'}
        #바운딩 박스가 POLYGON 형태일때 BOX 형태로 변환
        if bounding[0]['Drawing'] =='POLYGON':
            n = int(bounding[0]['PolygonCount'])
            x_point_list =[]
            y_point_list = []
            for j in range(0,n):
                x_point_list.append( int(list(bounding[0]['PolygonPoint'][j].values())[0].split(',')[0]) )
                y_point_list.append( int(list(bounding[0]['PolygonPoint'][j].values())[0].split(',')[1]))
            x1 = min(x_point_list)
            x2 = max(x_point_list)
            y1 = min(y_point_list)
            y2 = max(y_point_list)
            width = x2-x1
            height = y2-y1
            w1 = int(data['RESOLUTION'].split('*')[0])
            h1 = int(data['RESOLUTION'].split('*')[1])
            x_center = (x1+width/2) / w1
            y_center = (y1+height/2) / h1
            normalized_width = width / w1
            normalized_height = height / h1
            if bounding[0]['DETAILS']=='의자':
                class_name = 0
            elif bounding[0]['DETAILS']=='TV':
                class_name=1
            elif bounding[0]['DETAILS']=='두발자전거' or bounding[0]['DETAILS']=='세발자전거':
                class_name=2
            elif bounding[0]['DETAILS']=='선풍기':
                class_name=3
            elif bounding[0]['DETAILS']=='소파':
                class_name=4
            elif bounding[0]['DETAILS']=='책상':
                class_name=5
            elif bounding[0]['DETAILS']=='서랍장':
                class_name=6
            elif bounding[0]['DETAILS']=='화분':
                class_name=7     
            elif bounding[0]['DETAILS']=='항아리':
                class_name=8  

                                 
            info= [class_name, x_center, y_center, normalized_width, normalized_height ]
        #바운딩 박스가 BOX 형태일 때 
        elif bounding[0]['Drawing'] =='BOX':
            if bounding[0]['DETAILS']=='의자':
                class_name = 0
            elif bounding[0]['DETAILS']=='TV':
                class_name=1
            elif bounding[0]['DETAILS']=='두발자전거' or bounding[0]['DETAILS']=='세발자전거':
                class_name=2
            elif bounding[0]['DETAILS']=='선풍기':
                class_name=3
            elif bounding[0]['DETAILS']=='소파':
                class_name=4
            elif bounding[0]['DETAILS']=='책상':
                class_name=5
            elif bounding[0]['DETAILS']=='서랍장':
                class_name=6
            elif bounding[0]['DETAILS']=='화분':
                class_name=7     
            elif bounding[0]['DETAILS']=='항아리':
                class_name=8  
            x1,y1 = int(bounding[0]['x1']), int(bounding[0]['y1'])
            x2,y2 = int(bounding[0]['x2']), int(bounding[0]['y2'])
            width = x2-x1
            height = y2-y1
            w1 = int(data['RESOLUTION'].split('*')[0])
            h1 = int(data['RESOLUTION'].split('*')[1])
            x_center = (x1+width/2) / w1
            y_center = (y1+height/2) / h1
            normalized_width = width / w1
            normalized_height = height / h1
            info= [class_name, x_center, y_center, normalized_width, normalized_height ]
        filename = i.replace('.Json','.txt')
        with open('/content/drive/MyDrive/BIG_PROJECT/labels/train/'+filename, "w") as f:
            for item in info:
                f.write(f"{item} ")
            f.close()
    os.remove('/content/drive/MyDrive/BIG_PROJECT/labels/train/'+i)