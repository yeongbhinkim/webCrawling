import os
import pandas as pd
import chardet
import logging

# pip install pandas
# pip install chardet

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 원본 파일과 새 파일의 폴더 경로
original_folder_path = 'C:/Users/yb/Desktop/pa/csv'
new_folder_path = 'C:/Users/yb/Desktop/pa/newScv'

# 새로운 헤더 설정
new_headers = [
    "CITY", "STREET", "BON_BUN", "BU_BUN", "DAN_GI_MYEONG", "SQUARE_METER",
    "CONTRACT_DATE", "CONTRACT_DAY", "AMOUNT", "LAYER", "CONSTRUCTION_DATE",
    "ROAD_NAME", "REASON_CANCELLATION_DATE", "REGISTRATION_CREATION",
    "TRANSACTION_TYPE", "LOCATION_AGENCY"
]

# 원본 폴더에서 모든 CSV 파일을 수정
for file_name in os.listdir(original_folder_path):
    if file_name.endswith('.csv'):
        original_file_path = os.path.join(original_folder_path, file_name)
        new_file_path = os.path.join(new_folder_path, file_name)

        # 파일의 인코딩을 감지
        logging.info(f'Checking encoding for {file_name}')
        with open(original_file_path, 'rb') as f:
            rawdata = f.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']

        if encoding:
            logging.info(f'Encoding detected: {encoding}')
        else:
            logging.info('Encoding not detected, using default utf-8')
            encoding = 'utf-8'

        # CSV 파일을 데이터프레임으로 읽기
        try:
            logging.info(f'Reading {file_name}')
            # 첫 15줄을 건너뛰고, 16번째 줄에 있는 헤더를 무시합니다.
            df = pd.read_csv(original_file_path, encoding=encoding, header=None, skiprows=15)
        except Exception as e:
            logging.error(f'Error reading {file_name}: {e}')
            continue

        # 첫 16줄을 제거
        if len(df.index) > 16:
            df = df.iloc[16:]
            logging.info(f'Removed first 16 lines in {file_name}')
        else:
            logging.info(f'File {file_name} has less than 16 lines, skipping')
            continue

        # 새로운 헤더 적용
        df.columns = new_headers
        logging.info(f'Applied new headers to {file_name}')

        # 수정된 내용을 새 폴더에 CSV 파일로 저장
        df.to_csv(new_file_path, index=False)
        logging.info(f'Saved updated file {file_name} to {new_file_path}')