from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

# 크롬 드라이버 경로 설정
chrome_driver_path = 'c:/Users/fkdle/Downloads/pa/chromedriver_win32/chromedriver.exe'  # 여기에 실제 chromedriver.exe 경로를 지정해야 합니다.

# 다운로드 폴더 설정
download_folder = "C:/Users/fkdle/Desktop/pa/Downloads"

# 옵션 설정
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_folder}
chrome_options.add_experimental_option("prefs", prefs)

# 드라이버 서비스 설정
service = Service(executable_path=chrome_driver_path)

# 웹 드라이버 설정
driver = webdriver.Chrome(service=service, options=chrome_options)


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
    # 날짜 입력
    wait.until(EC.visibility_of_element_located((By.ID, "searchFromDt"))).send_keys(start_date.strftime("%Y%m%d"))
    wait.until(EC.visibility_of_element_located((By.ID, "searchToDt"))).send_keys(end_date.strftime("%Y%m%d"))

    # 팝업 처리
    handle_popups(driver)

    # 파일 형식 선택 (CSV)
    driver.find_element(By.ID, "fileType").click()
    driver.find_element(By.CSS_SELECTOR, "option[value='CSV']").click()

    # 다운로드 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, "a[onclick*='fn_load(fileType)']").click()

    # 파일 다운로드 대기
    time.sleep(10)  # 실제 환경에 맞게 대기 시간을 조정해야 합니다.

try:
    # 목표 웹 페이지 접속
    driver.get('https://rtdown.molit.go.kr/')

    # 대기 설정
    wait = WebDriverWait(driver, 100)

    # 1996년1월 01일부터 시작하여 현재까지 각 달의 첫 날과 마지막 날을 사용하여 파일 다운로드
    start_year = 1996
    end_year = datetime.now().year
    start_month = 1  # 시작 월

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

finally:
    # 브라우저 종료
    driver.quit()
