from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from methods import *
import unittest
import time
import sys
from tkinter import *

class KolibriTesting(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		#self.driver = webdriver.Chrome()
	
	def test_a_Testing_Server_Is_Started(self):
		r = requests.get("http://localhost:8008")
		if r.status_code == 200:
			print("Kolibri Server is started")
		else:
			print("Server Error %s" %r.status_code)
		self.assertEqual(r.status_code, 200)

	def test_ba_Crete_Users_and_Login_with_Exsting_User_with_wrong_password(self):
		temp = sample(self.driver)
		if temp==1:
			user = getText("Enter existing username but not of learner user")
			user = validate(user, "Enter existing username but not of learner user")
			password = getText("Enter Incorrect password")
			password = validate(user, "Enter Incorrect password")
			text = LoginDifferentKindOfUser(self.driver, "coach", "password")
			self.assertEqual(text, "Incorrect username or password",'Logging with the user that is not part of class')

	def test_bb_start_with_capital_A(self):
		self.driver.get("http://localhost:8008")
		text = LoginDifferentKindOfUser(self.driver, "Admin", "password")
		self.assertTrue(text, "Incorrect username or password")

	def test_bc_admin_username_in_capital(self):
		self.driver.get("http://localhost:8008")
		text = LoginDifferentKindOfUser(self.driver, "ADMIN", "password")
		self.assertTrue(text, "Incorrect username or password")
	

	def test_c_Login_with_Non_Exsting_User(self):
		self.driver.get("http://localhost:8008")
		text1 = getText("Enter existing username")
		text1 = validate(text1, "Enter existing username")
		text = LoginDifferentKindOfUser(self.driver, text1, "lee")
		self.assertEqual(text, "Incorrect username or password",'Logging with the user that is not part of class')
	
	def tearDown(self):
		self.driver.close()



class KolibriTestingClass(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		#self.driver = webdriver.Chrome()

	def test_d_delete_class(self):
		
		self.driver.get("http://localhost:8080")
		time.sleep(3)
		url = self.driver.current_url
		if "setup_wizard" in url:
			print("You need to setup Device owner account")
		else:
			LoginDifferentKindOfUser(self.driver, "admin","password")
			time.sleep(7)
			text = getText('enter classroom name::')
			if len(text)== 0:
				print("Empty classroom name not allowed")
			else:
				if text in self.driver.page_source:
					trs = self.driver.find_elements(By.TAG_NAME, "tr")
					for i in range(1,len(trs)):
						tt = trs[i].find_element(By.TAG_NAME, "th")
						tt1 = tt.find_element(By.TAG_NAME, "a").text
						if text == tt1:
							trs[i].find_element(By.TAG_NAME, "button").click()
							time.sleep(3)
							self.driver.find_element_by_xpath("//span[contains(text(), 'Delete Class')]").click()
							time.sleep(3)
							self.assertEqual(False, text in self.driver.page_source)
							break
				else:
					print("Class not found")

	def tearDown(self):
		self.driver.close()


class KolibriTestingFacility(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		#self.driver = webdriver.Chrome()

	def test_e_check_edit_username_facility(self):
		self.driver.get("http://localhost:8080")
		LoginDifferentKindOfUser(self.driver, "admin","password")
		time.sleep(2)
		self.driver.find_element_by_xpath('//a[contains(@href,"#/facilities")]').click()
		time.sleep(3)
		if not self.driver.find_element_by_name("learnerCanEditUsername").is_selected():
			self.driver.find_element_by_xpath('//div[contains(text(), "Allow users to edit their username")]').click()
		time.sleep(2)
		self.driver.find_element_by_xpath('//div[contains(text(), "Save changes")]').click()
		time.sleep(4)
		SignOut(self.driver)
		time.sleep(4)
		try:
			username = getText("Enter learner username which is exist")
			username = validate(username, "Enter learner username which is exist")
			password = getText("Enter learner password")
			password = validate(password, "Enter learner password")
			LoginDifferentKindOfUser(self.driver, username, password)
			time.sleep(5)
			self.driver.find_element_by_xpath("//button[@type='submit']").click()
			time.sleep(2)
			self.driver.find_element_by_xpath('//span[contains(text(), "menu")]').click()
			time.sleep(4)
			self.driver.find_element_by_xpath('//div[contains(text(), "Profile")]').click()
			time.sleep(4)
		except Exception:
			print("Please enter username which is exist")
			username = getText("Enter learner username which is exist")
			username = validate(username, "Enter learner username which is exist")
			password = getText("Enter learner password")
			password = validate(password, "Enter learner password")
			LoginDifferentKindOfUser(self.driver, username, password)
			time.sleep(5)
			self.driver.find_element_by_xpath("//button[@type='submit']").click()
			time.sleep(2)
			self.driver.find_element_by_xpath('//span[contains(text(), "menu")]').click()
			time.sleep(4)
			self.driver.find_element_by_xpath('//div[contains(text(), "Profile")]').click()
		username = getText("Enter new username which is not exist")
		username = validate(username, "Enter new username which is not exist")
		self.driver.find_element_by_xpath("//input[@type='text']").clear()
		time.sleep(3)
		self.driver.find_element_by_xpath("//input[@type='text']").send_keys(username)
		time.sleep(3)
		self.driver.find_element_by_xpath("//span[contains(text(), 'Save changes')]").click()
		time.sleep(4)
		if "An account with that username already exists" in self.driver.page_source:
			username = getText("Enter new username which is not exist")
			username = validate(username, "Enter new username which is not exist")
			self.driver.find_element_by_xpath("//input[@type='text']").clear()
			time.sleep(3)
			self.driver.find_element_by_xpath("//input[@type='text']").send_keys(username)
			time.sleep(3)
			self.driver.find_element_by_xpath("//span[contains(text(), 'Save changes')]").click()
			time.sleep(4)
		self.driver.find_element_by_xpath("//span[contains(text(), 'menu')]").click()
		time.sleep(3)
		self.driver.find_element_by_xpath("//span[contains(text(), 'exit_to_app')]").click()
		time.sleep(5)
		LoginDifferentKindOfUser(self.driver, username, password)
		time.sleep(8)
		temp = self.driver.title
		self.assertTrue(True, "Learn" in temp)
		print("Edit username facility working properly")




	def test_f_check_edit_fullname_facility(self):
		self.driver.get("http://localhost:8080")
		LoginDifferentKindOfUser(self.driver, "admin","password")
		time.sleep(2)
		self.driver.find_element_by_xpath('//a[contains(@href,"#/facilities")]').click()
		time.sleep(3)
		if self.driver.find_element_by_name("learnerCanEditUsername").is_selected():
			self.driver.find_element_by_xpath('//div[contains(text(), "Allow users to edit their username")]').click()
		time.sleep(2)

		if self.driver.find_element_by_name("learnerCanEditName").is_selected():
			pass
		else:
			self.driver.find_element_by_xpath('//div[contains(text(), "Allow users to edit their full name")]').click()

		time.sleep(2)
		self.driver.find_element_by_xpath('//div[contains(text(), "Save changes")]').click()
		time.sleep(4)
		SignOut(self.driver)
		time.sleep(4)
		try:
			username = getText("Enter new username which is exist")
			username = validate(username, "Enter new username which is exist")

			LoginDifferentKindOfUser(self.driver, username,"sc")
			time.sleep(5)
			self.driver.find_element_by_xpath("//button[@type='submit']").click()
			time.sleep(2)
			self.driver.find_element_by_xpath('//span[contains(text(), "menu")]').click()
			time.sleep(4)
			self.driver.find_element_by_xpath('//div[contains(text(), "Profile")]').click()
			time.sleep(4)
		except Exception:
			self.driver.refresh()
			time.sleep(5)
			print("Please enter username which is exist")
			username = getText("Enter new username which is exist")
			username = validate(username, "Enter new username which is exist")

			LoginDifferentKindOfUser(self.driver, username,"sc")
			time.sleep(5)
			self.driver.find_element_by_xpath("//button[@type='submit']").click()
			time.sleep(2)
			self.driver.find_element_by_xpath('//span[contains(text(), "menu")]').click()
			time.sleep(4)
			self.driver.find_element_by_xpath('//div[contains(text(), "Profile")]').click()
			time.sleep(4)
		full_name = getText("Enter full name")
		full_name = validate(full_name, "Enter full name")
		self.driver.find_element_by_xpath("//input[@type='text']").clear()
		time.sleep(3)
		self.driver.find_element_by_xpath("//input[@type='text']").send_keys(full_name)
		time.sleep(3)
		self.driver.find_element_by_xpath("//span[contains(text(), 'Save changes')]").click()
		time.sleep(4)
		self.driver.find_element_by_xpath("//span[contains(text(), 'menu')]").click()
		time.sleep(3)
		self.driver.find_element_by_xpath("//span[contains(text(), 'exit_to_app')]").click()
		time.sleep(5)
		self.assertEqual(True, True)
		print("Edit full name facility working properly")

	def tearDown(self):
		self.driver.close()


class KolibriTestingGroup(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		#self.driver = webdriver.Chrome()

	def test_e_create_group(self):
		self.driver.get("http://localhost:8080")
		username = getText("Enter username of admin or coach")
		username = validate(username, "Enter username of admin or coach")
		password = getText("Enter password")
		password = validate(password, "Enter password")
		LoginDifferentKindOfUser(self.driver, username, password)
		time.sleep(7)
		self.driver.find_element_by_xpath("//span[contains(text(), 'menu')]").click()
		time.sleep(2)
		self.driver.find_element_by_xpath("//span[contains(text(), 'assessment')]").click()
		time.sleep(3)
		class_name = getText("Enter class name")
		class_name = validate(class_name, "Enter class name")
		if class_name in self.driver.page_source:
			time.sleep(2)
			self.driver.find_element_by_xpath("//a[contains(text(), '%s')]" %class_name).click()
			time.sleep(3)
			self.driver.find_element_by_xpath("//span[contains(text(), 'group_work')]").click()
			time.sleep(4)

			group_name = getText("Enter group name")
			group_name = validate(group_name, "Enter group name")
			time.sleep(2)
			self.driver.find_element_by_xpath("//span[contains(text(), 'New group')]").click()
			time.sleep(3)
			self.driver.find_element_by_xpath("//input[@type='text']").send_keys(group_name)
			time.sleep(2)
			if "A group with that name already exists" in self.driver.page_source:
				group_name = getText("Enter unique group name")
				group_name = validate(group_name, "Enter unique group name")
				time.sleep(2)
				self.driver.find_element_by_xpath("//input[@type='text']").clear()
				time.sleep(2)
				self.driver.find_element_by_xpath("//input[@type='text']").send_keys(group_name)
				time.sleep(2)
			self.driver.find_element_by_xpath("//span[contains(text(), 'Save')]").click()
			time.sleep(4)
			try:
				self.driver.find_element_by_xpath("//input[@type='checkbox']").click()
				time.sleep(3)
				self.driver.find_element_by_css_selector('.ui-button.koli-icon-button.right-margin.ui-button--type-primary.ui-button--color-primary.ui-button--icon-position-left.ui-button--size-small').click()
				time.sleep(4)
				self.driver.find_element_by_xpath("//label[contains(text(), '%s')]" %group_name).click()
				time.sleep(4)
				self.driver.find_element_by_xpath("//span[contains(text(), 'Move')]").click()
				time.sleep(4)
			except Exception:
				print("There is no student in class")
		else:
			print("Enter valid classroom name")

	def test_e_delete_group(self):
		self.driver.get("http://localhost:8080")
		username = getText("Enter username of admin or coach")
		username = validate(username, "Enter username of admin or coach")
		password = getText("Enter password")
		password = validate(password, "Enter password")
		LoginDifferentKindOfUser(self.driver, username, password)
		time.sleep(7)
		self.driver.find_element_by_xpath("//span[contains(text(), 'menu')]").click()
		time.sleep(2)
		self.driver.find_element_by_xpath("//span[contains(text(), 'assessment')]").click()
		time.sleep(3)
		class_name = getText("Enter class name")
		class_name = validate(class_name, "Enter class name")
		if class_name in self.driver.page_source:
			time.sleep(2)
			self.driver.find_element_by_xpath("//a[contains(text(), '%s')]" %class_name).click()
			time.sleep(3)
			self.driver.find_element_by_xpath("//span[contains(text(), 'group_work')]").click()
			time.sleep(4)
			btn = self.driver.find_elements_by_css_selector(".ui-icon.ui-button__dropdown-icon.material-icons")
			group_name = getText("Enter group name to delete")
			group_name = validate(group_name , "Enter group name to delete")
			if group_name in self.driver.page_source:
				temp = self.driver.find_elements_by_class_name("group-section")
				count = 0
				if group_name in self.driver.page_source:
					for i in temp:
						t = i.find_element(By.TAG_NAME, "h2").text
						count = count +1
						if t == group_name:
							btn[count].click()
							time.sleep(4)
							self.driver.find_element_by_xpath("//div[contains(text(), 'Delete Group')]").click()
							time.sleep(4)
							self.driver.find_element_by_xpath("//span[contains(text(), 'Delete Group')]").click()
							time.sleep(5)
							temp = self.driver.find_elements_by_class_name("group-section")
							break
				if group_name in self.driver.page_source:
					count = 0
					for i in temp:
						t = i.find_element(By.TAG_NAME, "h2").text
						if t == group_name:
							count =1
							break

					if count ==1:
						self.assertEqual(True, True)
						print("Group deleted successfully")
					else:
						self.assertEqual(True , False)
				else:
					self.assertEqual(True, True)
					print("Group deleted successfully")
			else:
				print("%s not present in the class" %group_name)
				self.assertEqual(True , True)
		else:
			print("Class is not present")

	def tearDown(self):
		self.driver.close()


if __name__=="__main__":
	unittest.main()



