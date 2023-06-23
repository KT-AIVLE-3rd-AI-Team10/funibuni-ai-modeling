# aivle-ai-team10-ai-modeling
대형 폐기물 사진을 자동분류 해주는 AI 모델을 만듭니다.
(송파구 기준)
* 대분류 모델 : 의자, TV, 자전거, 선풍기, 소파, 책상, 서랍장, 화분, 항아리 (9개 Class)
* 소분류 모델 : 의자 - 일반의자, 회전의자, 장의자 / 자전거 - 성인용, 아동용

# 데이터 수집
| Site                 | URL                                                                       |
|----------------------|---------------------------------------------------------------------------|
| 공공데이터포털        |<https://data.seoul.go.kr/etc/aiEduData.do>                                 |
| AI Hub               |<https://www.aihub.or.kr/unitysearch/list.do?kwd=%ED%8F%90%EA%B8%B0%EB%AC%BC>|

# mini test를 통한 데이터 질 검증과 모델 선택
의자 100장, TV 100장, 자전거 100장, 선풍기 100장 총 400장의 데이터로 모델 선정을 위해 간단한 실험 진행
YOLOv5, YOLOv8, CNN 사용

* YOLO Documents
  
    YOLOv5 : <https://github.com/ultralytics/yolov5>

    YOLOv8 : <https://github.com/ultralytics/ultralytics>

* Code

진행결과 가장 실질적으로 Detection이 뛰어난 YOLOv8n을 사용하기로 결정

# 데이터 전처리
데이터 수가 많고 질이 좋은 AI Hub 데이터를 사용

Json 파일 구조 확인을 위한 예시



1. YOLO 학습을 위해 Bounding Box가 하나가 아닌 파일 삭제

    for i in os.listdir(labels_folder_path):
        file_name = i.replace('.Json','')
        label_file_path = labels_folder_path + '/'+ i
        image_file_path = images_folder_path + '/'+ i.replace('.Json','.jpg')
        
        with open(label_file_path,'r', encoding='UTF8') as file:
            data = json.load(file)
            if data['BoundingCount']!='1':
                print(file_name +'을 삭제합니다.')
                file.close()
                os.remove(label_file_path)
                os.remove(image_file_path)

2. Bounding Drawing 방식이 'POLYGON'인 경우에는 좌표 x1, x2, y1, y2로 변환

            elif data['Bounding'][0]['Drawing'] == 'POLYGON':
                x_point_list=[]
                y_point_list=[]
                for i in range(int(data['Bounding'][0]['PolygonCount'])):
                    x_point_list.append(int(list(data['Bounding'][0]['PolygonPoint'][i].values())[0].split(',')[0]))
                    y_point_list.append(int(list(data['Bounding'][0]['PolygonPoint'][i].values())[0].split(',')[1]))
                x1 = min(x_point_list)
                x2 = max(x_point_list)
                y1 = min(y_point_list)
                y2 = max(y_point_list)

3. class name과 좌표 정보가 담긴 txt 파일 생성

            x_center = ((x1 + x2) / 2) / img_width
            y_center = ((y1 + y2) / 2) / img_height
            width_norm = (x2 - x1) / img_width
            height_norm = (y2 - y1) / img_height

            if not os.path.exists(output_path):  # if the path does not exist
                os.makedirs(output_path)  # create the path

            # Determine the class based on the label
            if '의자' == label:
                class_id = '0'
            #...
     
            elif '항아리' in label:
                class_id = '10'
            else:
                class_id = None

            # If we have a valid class, write it to file
            if class_id is not None:
                with open(os.path.join(output_path, name+'.txt'), 'w') as file:
                    file.write(f"{class_id} {x_center:f} {y_center:f} {width_norm:f} {height_norm:f}\n")



