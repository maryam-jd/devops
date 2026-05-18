import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

APP_URL = "http://localhost"
results = []

def log(test_name, passed, detail=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {test_name}" + (f" | {detail}" if detail else ""))
    results.append({"test": test_name, "passed": passed, "detail": detail})

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def test_homepage_loads(driver):
    print("\n[Test 1] Homepage loads...")
    driver.get(APP_URL)
    time.sleep(2)
    log("Page title contains TaskFlow", "TaskFlow" in driver.title, driver.title)
    try:
        logo = driver.find_element(By.CLASS_NAME, "logo")
        log("Logo element visible", logo.is_displayed())
    except Exception as e:
        log("Logo element visible", False, str(e))
    try:
        form = driver.find_element(By.CLASS_NAME, "add-form")
        log("Add Task form present", form.is_displayed())
    except Exception as e:
        log("Add Task form present", False, str(e))

def test_add_task(driver):
    print("\n[Test 2] Add new task...")
    driver.get(APP_URL)
    time.sleep(2)
    task_title = "Selenium Test Task " + str(int(time.time()))
    try:
        driver.find_element(By.ID, "titleInput").send_keys(task_title)
        log("Typed task title", True, task_title)
        Select(driver.find_element(By.ID, "priorityInput")).select_by_value("high")
        log("Selected high priority", True)
        driver.find_element(By.ID, "descInput").send_keys("Created by Selenium")
        driver.find_element(By.ID, "addBtn").click()
        log("Clicked Add Task button", True)
        time.sleep(2)
        toast = driver.find_element(By.ID, "toast")
        log("Success toast appeared", "added" in toast.text.lower(), toast.text)
        return task_title
    except Exception as e:
        log("Add task via form", False, str(e))
        return None

def test_task_in_list(driver, task_title):
    print("\n[Test 3] Task appears in list...")
    if not task_title:
        log("Task in list (skipped)", False); return
    time.sleep(2)
    try:
        found = task_title in driver.page_source
        log("New task visible in list", found, task_title[:30])
        count = int(driver.find_element(By.ID, "totalCount").text)
        log("Total count > 0", count > 0, f"Count: {count}")
    except Exception as e:
        log("Task in list check", False, str(e))

def test_api_health(driver):
    print("\n[Test 4] API health check...")
    try:
        driver.get(f"{APP_URL}/health")
        time.sleep(1)
        body = driver.find_element(By.TAG_NAME, "body").text
        log("Health returns status OK", '"status":"OK"' in body or '"status": "OK"' in body, body[:80])
        log("Database connected", '"connected"' in body, body[:80])
    except Exception as e:
        log("API health check", False, str(e))

def test_delete_task(driver):
    print("\n[Test 5] Delete a task...")
    driver.get(APP_URL)
    time.sleep(2)
    try:
        before = int(driver.find_element(By.ID, "totalCount").text)
        if before == 0:
            log("Delete task (no tasks)", True, "Skipped"); return
        driver.find_elements(By.CLASS_NAME, "delete-btn")[0].click()
        log("Clicked delete button", True)
        time.sleep(2)
        after = int(driver.find_element(By.ID, "totalCount").text)
        log("Count decreased after delete", after < before, f"{before} → {after}")
    except Exception as e:
        log("Delete task", False, str(e))

def main():
    print("=" * 60)
    print("  TaskFlow Selenium Tests — CSC418 DevOps Final")
    print(f"  URL: {APP_URL}")
    print("=" * 60)
    driver = get_driver()
    try:
        test_homepage_loads(driver)
        title = test_add_task(driver)
        test_task_in_list(driver, title)
        test_api_health(driver)
        test_delete_task(driver)
    finally:
        driver.quit()
    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    print(f"  Passed: {passed} ✅   Failed: {failed} ❌   Total: {len(results)}")
    print("=" * 60)
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()