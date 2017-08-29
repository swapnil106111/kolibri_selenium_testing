import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys




def CreateDeviceOwnerAccount(driver, user, ps, name):
	driver.find_element_by_xpath("//input[@type='text']").clear()
	time.sleep(1)
	driver.find_element_by_xpath("//input[@type='text']").send_keys(user)
	time.sleep(1)
	driver.find_element_by_xpath("//input[@type='password']").clear()
	time.sleep(1)
	driver.find_element_by_xpath("//input[@type='password']").send_keys(ps)
	time.sleep(1)
	driver.find_element_by_xpath("(//input[@type='password'])[2]").clear()
	time.sleep(1)
	driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(ps)
	time.sleep(1)
	driver.find_element_by_xpath("(//input[@type='text'])[2]").clear()
	time.sleep(1)
	driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(name)
	time.sleep(1)
	driver.find_element_by_xpath('//span[contains(text(), "Create and get started")]').click() 
	time.sleep(15)
	time.sleep(7)
	#LoginDifferentKindOfUser(driver, "admin", "password")
	time.sleep(7)
	driver.find_element_by_xpath('//a[contains(@href,"#/facilities")]').click()
	time.sleep(2)
	driver.find_element_by_xpath('//div[contains(text(), "Allow users to edit their username")]').click()
	time.sleep(1)
	driver.find_element_by_xpath('//div[contains(text(), "Allow users to edit their full name")]').click()
	time.sleep(1)
	driver.find_element_by_xpath('//div[contains(text(), "Allow users to sign-up on this device")]').click()
	time.sleep(1)
	driver.find_element_by_xpath('//div[contains(text(), "Allow learners to sign in with no password")]').click()
	time.sleep(1)
	driver.find_element_by_xpath('//div[contains(text(), "Save changes")]').click()
	time.sleep(2)
	driver.find_element_by_xpath('//a[contains(@href,"#/classes")]').click()
	time.sleep(2)
	driver.find_element_by_xpath('//span[contains(text(), "Add New Class")]').click() 
	time.sleep(2)
	driver.find_element_by_xpath("//input[@type='text']").send_keys("AAAA_Classroom")
	time.sleep(2)
	driver.find_element_by_xpath('//span[contains(text(), "Create")]').click()
	time.sleep(2)
	driver.find_element_by_xpath('//a[contains(text(), "AAAA_Classroom")]').click()
	time.sleep(2)
	driver.find_element_by_xpath('//span[contains(text(), "Enroll users")]').click()
	time.sleep(2)
	CreateUserAccount(driver, "Learner", "sc", "//div[@id='modal-window']/div/form/section/div[5]/div/div/div[3]/ul/li[1]")
	time.sleep(2)
	CreateUserAccount(driver, "coach", "sc", "//div[@id='modal-window']/div/form/section/div[5]/div/div/div[3]/ul/li[2]")
	time.sleep(2)
	CreateUserAccount(driver, "PM", "sc", "//div[@id='modal-window']/div/form/section/div[5]/div/div/div[3]/ul/li[3]")
	time.sleep(3)
	driver.find_element_by_xpath('//span[contains(text(), "Review & save")]').click()
	time.sleep(2)
	driver.find_element_by_xpath('//span[contains(text(), "Yes, enroll users")]').click()
	time.sleep(2)

	driver.find_element_by_xpath('//div[contains(text(), "(Device owner)")]').click()
	time.sleep(1)
	driver.find_element_by_xpath('//div[contains(text(), "Sign Out")]').click()
	time.sleep(3)
	


def CreateUserAccount(driver, user, ps, link):
	driver.find_element_by_xpath('//span[contains(text(), "New user account")]').click()
   	time.sleep(3)
   	driver.find_element_by_xpath("//input[@type='text']").send_keys(user)
   	time.sleep(3)
   	driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(user)
   	time.sleep(1)
   	text = "Username already exists"
   	if text in driver.page_source:
   		time.sleep(2)
   		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
   		time.sleep(2)
   		print("User already created")
   	else:
		time.sleep(3)
		driver.find_element_by_xpath("//input[@type='password']").send_keys(ps)
		time.sleep(2)
		driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(ps)
		time.sleep(2)
		driver.find_element_by_xpath("//div[@class='ui-select__label-text']").click()
		time.sleep(2)
		driver.find_element_by_xpath(link).click()
		time.sleep(4)
   		driver.find_element_by_xpath('//span[contains(text(), "Create Account")]').click() 

def LoginDifferentKindOfUser(driver, user, password):
	driver.find_element_by_xpath("//input[@type='text']").clear()
	time.sleep(1)
	driver.find_element_by_xpath("//input[@type='text']").send_keys(user)
	time.sleep(2)
	driver.find_element_by_xpath("//button[@type='submit']").click()
	time.sleep(5)
	if driver.title.startswith("Kolibri"):
		print("Not logging in with Learner")
		time.sleep(2)
		driver.find_element_by_xpath("//input[@type='password']").clear()
		time.sleep(1)
		driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
		time.sleep(2)
		driver.find_element_by_xpath("//button[@type='submit']").click()
		time.sleep(2)
		text = "Incorrect username or password"
		if text in driver.page_source:
			print(text)
			return text
	print("success")



def SignOut(driver):
	driver.find_element_by_xpath("//button[@type='submit']").click()
	time.sleep(2)
	driver.find_element_by_xpath('//div[contains(text(), "Sign Out")]').click()
	time.sleep(4)

def sample(driver):
	driver.get("http://localhost:8008")
	assert "Kolibri" in driver.title
	time.sleep(2)
	try:
		print(driver.current_url)
		if "setup_wizard" not in driver.current_url:
			LoginDifferentKindOfUser(driver, "admin", "password")
			time.sleep(1)
			driver.find_element_by_xpath('//a[contains(@href,"#/classes")]').click()
			time.sleep(2)
			driver.find_element_by_xpath('//span[contains(text(), "Add New Class")]').click() 
			time.sleep(2)
			driver.find_element_by_xpath("//input[@type='text']").send_keys("AAAA_Classroom")
			time.sleep(2)
			text = "A class with that name already exists"
			if text in driver.page_source:
				time.sleep(2)
				webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
				time.sleep(2)
			else:
				time.sleep(2)
				driver.find_element_by_xpath('//span[contains(text(), "Create")]').click()
				time.sleep(2)
			driver.find_element_by_xpath('//a[contains(text(), "AAAA_Classroom")]').click()
			time.sleep(2)
			driver.find_element_by_xpath('//span[contains(text(), "Enroll users")]').click()
			time.sleep(2)
			CreateUserAccount(driver, "Learner", "sc", "//div[@id='modal-window']/div/form/section/div[5]/div/div/div[3]/ul/li[1]")
			time.sleep(2)
			CreateUserAccount(driver, "coach", "sc", "//div[@id='modal-window']/div/form/section/div[5]/div/div/div[3]/ul/li[2]")
			time.sleep(2)
			CreateUserAccount(driver, "PM", "sc", "//div[@id='modal-window']/div/form/section/div[5]/div/div/div[3]/ul/li[3]")
			time.sleep(3)
			if "Select all on page" in driver.page_source:
				driver.find_element_by_name("Select all on page").click()
				time.sleep(2)
				btn = driver.find_element_by_xpath('//span[contains(text(), "Review & save")]')
				time.sleep(1)
				if btn.is_enabled():
					time.sleep(1)
					btn.click()
					time.sleep(2)
					driver.find_element_by_xpath('//span[contains(text(), "Yes, enroll users")]').click()
					time.sleep(2)
			else:
				print("All user already there in class AAAA_Classroom")

			SignOut(driver)


		else:
			CreateDeviceOwnerAccount(driver, "admin", "password", "Testing_Purpose")

		return 1
	except Exception :
		print("Time out for page loading")
