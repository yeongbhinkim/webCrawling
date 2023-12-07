from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options

import time
import os
import logging

# 로그 설정
logging.basicConfig(filename='selenium_log.log', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

# 크롬 드라이버 경로 설정
chrome_driver_path = 'C:/Users/yb/Desktop/pa/webCrawling/chromedriver_win32/chromedriver.exe'

# 다운로드 폴더 설정 C:\Users\yb\Downloads
download_folder = "C:/Users/yb/Desktop/pa/webCrawling/Download"
# download_folder = "C:/Users/yb/Desktop/pa/webCrawling"
# download_folder = "C:/Users/yb/Downloads"

# 옵션 설정
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 헤드리스 모드 활성화
# chrome_options.add_argument("--disable-gpu")  # 일부 시스템에서 필요
# chrome_options.add_argument("--window-size=1920,1080")  # 필요한 경우 창 크기 지정
# chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--no-sandbox")


prefs = {
    # "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "safebrowsing_for_trusted_sources_enabled": False,
}
# "plugins.always_open_pdf_externally": True,
chrome_options.add_experimental_option("prefs", prefs)

chrome_options.add_argument("--log-level=3")

# 드라이버 서비스 설정
service = Service(executable_path=chrome_driver_path, log_path=os.path.join(download_folder, 'chromedriver.log'))

def setting_chrome_options():
    print('옵션 설정')
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # 백그라운드 작업
    return options

# 웹 드라이버 설정


driver = webdriver.Chrome(service=service, options=chrome_options)
# driver = webdriver.Chrome(service=service,options=setting_chrome_options())
def handle_popups(driver):
    # 현재 창 핸들 저장
    main_window_handle = driver.current_window_handle
    all_window_handles = driver.window_handles

    # 메인 창이 아닌 다른 창이 있다면 닫기
    for handle in all_window_handles:
        if handle != main_window_handle:
            driver.switch_to.window(handle)
            driver.close()
    
    # 메인 창으로 다시 전환
    driver.switch_to.window(main_window_handle)

    # 자바스크립트 경고/확인창 처리
    try:
        alert = driver.switch_to.alert
        alert.accept()  # 또는 alert.dismiss()
    except:
        pass  # 경고창이 없으면 무시

def download_files(start_date, end_date, driver, wait):
    try:
    
        # 팝업 처리
        handle_popups(driver)

        # iframe으로 전환
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))
        
        # 날짜 입력
        wait.until(EC.visibility_of_element_located((By.ID, "searchFromDt"))).clear()
        wait.until(EC.visibility_of_element_located((By.ID, "searchFromDt"))).send_keys(start_date.strftime("%Y%m%d"))
        wait.until(EC.visibility_of_element_located((By.ID, "searchToDt"))).clear()
        wait.until(EC.visibility_of_element_located((By.ID, "searchToDt"))).send_keys(end_date.strftime("%Y%m%d"))

        # 파일 형식 선택 (CSV)
        driver.find_element(By.ID, "fileType").click()
        driver.find_element(By.CSS_SELECTOR, "option[value='CSV']").click()

        # time.sleep(2)  # 실제 환경에 맞게 대기 시간을 조정해야 합니다.

        # 다운로드 버튼 클릭
        driver.find_element(By.CSS_SELECTOR, "a[onclick*='fn_load(fileType)']").click() 

        # 로그 기록
        logging.info(f"다운로드 시도: {start_date.strftime('%Y%m%d')} - {end_date.strftime('%Y%m%d')}")


        # iframe에서 나가기
        driver.switch_to.default_content()

        # 파일 다운로드 대기
        time.sleep(20)  # 실제 환경에 맞게 대기 시간을 조정해야 합니다.

        # 다운로드 버튼 클릭 후, 파일 다운로드가 완료될 때까지 대기
        # wait_for_download(wait, download_folder)

    except Exception as e:
        logging.exception(f"다운로드 중 오류 발생: {e}")

def wait_for_download(wait, download_folder):
    # 다운로드 폴더에서 파일이 나타날 때까지 대기
    end_time = time.time() + 60  # 최대 60초 대기
    while True:
        time.sleep(3)  # 매초 확인
        files = [filename for filename in os.listdir(download_folder) if filename.endswith('.csv')]
        if files:  # 파일이 하나라도 존재하면 다운로드가 시작됐다고 가정
            print('다운로드 시작됨:', files)
            break
        elif time.time() > end_time:
            raise Exception('다운로드 타임아웃')
    # 모든 파일의 다운로드가 완료될 때까지 추가 대기
    for file in files:
        filepath = os.path.join(download_folder, file)
        while not os.path.isfile(filepath):
            time.sleep(1)  # 파일이 나타날 때까지 대기
        print(f'{file} 다운로드 완료')


try:
    # 목표 웹 페이지 접속
    driver.get('https://rtdown.molit.go.kr/')
    # driver.get('https://rtdown.molit.go.kr/countLog.do#')
    # # 대기 설정
    wait = WebDriverWait(driver, 100)    
    # 1996년1월 01일부터 시작하여 현재까지 각 달의 첫 날과 마지막 날을 사용하여 파일 다운로드
    start_year = 2013
    end_year = datetime.now().year
    start_month = 11  # 시작 월

    for year in range(start_year, end_year + 1):
        for month in range(start_month, 13):
            start_date = datetime(year, month, 1)
            # 다음 달의 첫 날에서 하루를 빼면 현재 달의 마지막 날이 됩니다.
            end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            download_files(start_date, end_date, driver, wait)
            # 현재 달이 12월이면 다음 반복에서 연도를 증가시키고 월을 1월로 설정
            if month == 12:
                start_month = 1
                break  # 다음 연도로 넘어갑니다.

except Exception as e:
    print(f'에러 발생: {e}')
finally:
    # 브라우저 종료
    driver.quit()
