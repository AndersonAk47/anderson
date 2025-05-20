from selenium import  webdriver
from selenium.webdriver.common.by import By     
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

OPTIONS: list[str]=[
    "--disable-extensions",
    "-disable-gpu",
    "start-maximized",

]

def get_driver(options:list[str]=[]) -> WebDriver:

    opt: webdriver.ChromeOptions= webdriver.ChromeOptions()
    for option in options:
        opt.add_argument(option)

    driver = webdriver.Chrome(options=opt)
    driver.get("https://demoqa.com/automation-practice-form")
    return driver


def  scroll_to_element(drive: WebDriver , elemet: WebElement) -> None:
    drive.execute_script("arguments[0].scrollIntoView();", elemet)
    sleep(1)

def llenar_texto_by_id(driver: WebDriver , id_element: str, texto) -> WebElement:
    element: WebElement = driver.find_element(By.ID , id_element)
    element.send_keys(texto)
    scroll_to_element(drive=driver , elemet=element)
    return element

def texto_autocompletado(driver: WebDriver , id_element: str, texto: str) -> None:
    llenar_texto_by_id(driver=driver , id_element=id_element , texto=texto)
    element_autocomplete: WebElement =  WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            ( 
                By.XPATH,
                f'//div[contains(@class, "subjects-auto-complete__option") and text()="{texto}"]'
             )
        )
    )    
    element_autocomplete.click()





def seleccionar_fecha(driver:WebDriver)-> None:

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dateOfBirthInput")) 
    ).click()

    year_select: WebElement = driver.find_element(
        By.CLASS_NAME, "react-datepicker__year-select"
    )
    sleep(1)
    Select(year_select).select_by_value("1999")

    month_select: WebElement = driver.find_element(
        By.CLASS_NAME, "react-datepicker__month-select"
    )
    sleep(1)
    Select(month_select).select_by_visible_text("January")

    day_select: WebElement = driver.find_element(
        By.CLASS_NAME, "react-datepicker__day--017"
    )
    sleep(1)
    day_select.click()

    sleep(1)


def llenar_formulario(driver: WebDriver) -> None:
    campos_texto: dict[str , str] = {
        "firstName": "Anderson",
        "lastName": "Romero" ,
        "userEmail": "aromero@inter.edu.co",
        "userNumber": "1234567890",
        "currentAddress" : "Calle # 40" ,
         
    }
    for key, value in campos_texto.items():
        llenar_texto_by_id(driver=driver, id_element=key , texto=value)
        sleep(1)

def main()-> None:
    driver: WebDriver= get_driver(options=OPTIONS)
    llenar_formulario(driver=driver)
    sleep(3)
    for subject in [ "Maths" , "Physics" , "Chemistry"]:
        texto_autocompletado(
            driver=driver,
            id_element="subjectsInput",
            texto=subject,
        )
    seleccionar_fecha(driver=driver)
    sleep(3)
    driver.save_screenshot("screenshot.png")
    driver.quit()   

if __name__ == "__main__":
    main()