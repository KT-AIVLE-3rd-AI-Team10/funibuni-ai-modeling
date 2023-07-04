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

YOLOv5, YOLOv8n, YOLOv8s,CNN 사용

* YOLO Documents
  
    YOLOv5 : <https://github.com/ultralytics/yolov5>

    YOLOv8 : <https://github.com/ultralytics/ultralytics>

* Code

진행결과 가장 실질적으로 Detection이 뛰어난 YOLOv8n을 사용하기로 결정

# 데이터 전처리
데이터 수가 많고 질이 좋은 AI Hub 데이터를 사용


### YOLO 학습을 위한 기본 라벨링 전처리
Json 파일 구조 확인을 위한 예시
#### 1. YOLO 학습을 위해 Bounding Box가 하나가 아닌 파일 삭제

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

#### 2. Bounding Drawing 방식이 'POLYGON'인 경우에는 좌표 x1, x2, y1, y2로 변환

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

#### 3. Class Name과 좌표 정보가 담긴 txt 파일 생성

            # YOLO에 맞게 좌표 변환
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

#### 4. 데이터셋 정보가 담긴 yaml 파일 생성 ################label_dic 수정 

      label_dic = {0: 'chair', 1: 'tv', 2: 'bicycle', 3: 'fan', 4: 'sofa', 5: 'desk', 6: 'chiffonier', 7: 'pot', 8: 'jar'}
      with open('/content/drive/MyDrive/BIG_PROJECT/class.yaml', 'w') as f:
      data = {
          'path': '/content/drive/MyDrive/BIG_PROJECT',
          'train':'images/train',
          'val': 'images/val',
          'nc': len(label_dic),
          'names': label_dic,
      }
      yaml.safe_dump(data, f)

    

### 데이터 불균형 해결을 위한 전처리
#### 1. 데이터 수 맞추기
* 기존 데이터
  서랍장  약 5400장,
  선풍기 약 4000장,
  소파 약 1600장,
  의자 약 16200장,
  책상 약 1600장,
  티비 약 1700장,
  항아리 약 1500장,
  화분 약 11000장,
  자전거 약 40000장

  --> 데이터 불균형이 심각하고 데이터 용량이 너무 커서 모델 학습에 지장을 주므로 데이터 수를 줄이기로 결정

각 Class별로 train 1200장, val 300장으로 재정제  

의자나 자전거의 경우 각 소분류 항목도 총 1500장 중에서 비율을 맞추어줌

#### 2. Image Augmentation
   의자 중 장의자의 이미지 경우 200장 미만으로 다른 의자(일반의자, 회전의자)와 데이터 수 차이가 큼
   
   Image Augmentation을 활용해 데이터 증강 후 모델 성능 개선 된 것을 확인 가능


# 모델 학습

#### 1. YOLOv8n 학습
    #ultralytics설치
    !pip install --target=$my_path ultralytics
    import ultralytics
    ultralytics.checks()

    from ultralytics import YOLO
    #모델 yolov8n
    model = YOLO('yolov8n.pt')

    with open('/content/drive/MyDrive/BIG_PROJECT/class.yaml', 'w') as f:
        data = {
            'path': '/content/drive/MyDrive/BIG_PROJECT/',
            'train':'/content/drive/MyDrive/BIG_PROJECT/images/train',
            'val': '/content/drive/MyDrive/BIG_PROJECT/images/val',
            'nc': len(label_dic),
            'names': label_dic,
        }
        yaml.safe_dump(data, f)
      #모델학습
      model.train(data='/content/drive/MyDrive/BIG_PROJECT/class.yaml', epochs=5,patience=5,batch=32,imgsz=416)
#### 2. 공공데이터 포털 데이터셋 추가 후 비교 (현우님 비교 데이터 보고 삭제 or 넣기)
#### 3. YOLOv8m과 비교 (최종모델 때 멀 사용했는지 수정)

# ML Flow와 모델 연동 학습
# MLflow 실행 시작
    with mlflow.start_run(experiment_id=exp_id, run_name=myname):

    ## 학습 전

    # YOLO 모델 불러오기
        model = YOLO('yolov8n.pt')

    # 하이퍼파라미터 로깅
        epochs = 100 #100
        patience = 35 #30
        batch_size = 32
        imgsz = 416
        data_path = '/content/drive/MyDrive/BIG_PROJECT/class.yaml'

        mlflow.log_param("epochs", epochs)
        mlflow.log_param("patience", patience)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("imgsz", imgsz)
        mlflow.log_param("data_path", data_path)

        model.add_callback("on_fit_epoch_end",on_fit_epoch_end)

        ## 모델 학습
        results = model.train(data=data_path, epochs=epochs, patience=patience, batch=batch_size, imgsz=imgsz)

    ## 학습 후

    # 모델 메트릭 로깅
    mlflow.log_artifacts('/content/runs/detect/train')

    # 베스트 모델 불러오기
    checkpoint = torch.load('/content/runs/detect/train/weights/best.pt', map_location='cpu')
    best_model = checkpoint.get('model') #, checkpoint)

    # best.pt를 모델 폴더 안에 넣어줘야함!
    mlflow.log_artifact('/content/runs/detect/train/weights/best.pt', artifact_path='best_model')

    # MLflow에 모델 로깅 및 등록된 모델로 등록
    mlflow.pytorch.log_model(best_model, "best_model", registered_model_name=model_name)
# YOLO 모델 탐지 결과 text로 반환
predict의 매개 변수 save_txt,save_conf 을 이용하요 class 와 확률을 text로 반환

      result = model.predict(source = '/content/drive/MyDrive/BIG_PROJECT/images/test', save=True,save_txt=True,save_conf=True)
   






