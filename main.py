from selenium import webdriver
import os
import stat
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client
import time

def clean_text(text):
  output = float(text[:-1])
  print(output)
  return output

def notify(value):
  if value <= 0.03:
    account_sid = os.environ['TWILIO_ACC_SID']
    auth_token  = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to= os.environ['TO_PHONE_NUMBER'], 
        from_= os.environ['FROM_PHONE_NUMBER'],
        body= f"Stock value is now {value}")
    print(message.sid)
  else: 
    print("Stock value is not below threshold")

def get_driver():
  st = os.stat('chromedriver')
  os.chmod('chromedriver', st.st_mode | stat.S_IEXEC)
  chrome_options = Options()
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome('./chromedriver',options=chrome_options)
  driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
  time.sleep(2)
  return driver

def main():
  driver = get_driver()

  element = driver.find_element(by="xpath", value="/html/body/div[2]/div/section[1]/div/div/div[2]/span[2]")

  value = clean_text(element.text)
  notify(value)


main()