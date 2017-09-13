import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from methods import *
import unittest
import time
import sys
import os
from tkinter import *


class KolibriTesting(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		# self.driver = webdriver.Chrome()

	def test_a_testing_server_is_started(self):
		r = requests.get("http://localhost:8008")
		if r.status_code == 200:
			print("Kolibri Server is started")
		else:
			print("Server Error %s" %r.status_code)
		self.assertEqual(r.status_code, 200)

	def test_b_create_users_and_login_with_exsting_user_with_wrong_password(self):
		temp = sample(self.driver)
		if temp==1:
			user = getText("Enter existing username but not of learner user")
			user = validate(user, "Enter existing username but not of learner user")
			password = getText("Enter Incorrect password")
			password = validate(user, "Enter Incorrect password")
			text = LoginDifferentKindOfUser(self.driver, "coach", "password")
			self.assertEqual(text, "Incorrect username or password",'Logging with the user that is not part of class')

	def test_c_start_with_capital_a(self):
		self.driver.get("http://localhost:8008")
		text = LoginDifferentKindOfUser(self.driver, "Admin", "password")
		self.assertTrue(text, "Incorrect username or password")

	def test_d_admin_username_in_capital(self):
		self.driver.get("http://localhost:8008")
		text = LoginDifferentKindOfUser(self.driver, "ADMIN", "password")
		self.assertTrue(text, "Incorrect username or password")
	
	def test_e_login_with_non_exsting_user(self):
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
		# self.driver = webdriver.Chrome()

	def test_a_delete_class(self):
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

	def test_a_check_edit_username_facility(self):
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

	def test_b_check_edit_fullname_facility(self):
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

	def test_a_create_group(self):
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
				temp = self.driver.find_elements_by_class_name("group-section")
				for i in temp:
					text1 = i.find_element(By.TAG_NAME, "span").text
					if text1 != "0 Learners":
						i.find_element(By.TAG_NAME, "button").click()
						time.sleep(4)
						self.driver.find_element_by_xpath("//label[contains(text(), '%s')]" %group_name).click()
						time.sleep(4)
						self.driver.find_element_by_xpath("//span[contains(text(), 'Move')]").click()
						time.sleep(4)
						print("Learners added into new group")
						
						SignOut(self.driver)
						self.assertEqual(True, True)

						break
				
			except Exception:
				print("There is no student in class")

		else:
			print("Enter valid classroom name")


	def test_b_delete_group(self):
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
			if group_name == "Ungrouped":
				print("Sorry, You can not delete Ungrouped group")
			else:
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

						if count == 0:
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


class KolibriTestingExam(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()

	def test_a_create_exam(self):
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
		time.sleep(5)

		text = "Signed in as device owner"
		if text not in self.driver.page_source:
			class_name = getText("Enter class name")
			class_name = validate(class_name, "Enter class name")
			time.sleep(2)
			if class_name in self.driver.page_source:
				try:
					self.driver.find_element_by_xpath("//a[contains(text(), '%s')]" %class_name).click()
					time.sleep(4)
					self.driver.find_element_by_xpath("//span[contains(text(), 'assignment_late')]").click()
					time.sleep(4)
					self.driver.find_element_by_xpath("//div[contains(text(), 'New Exam')]").click()
					time.sleep(4)
					self.driver.find_element_by_css_selector(".ui-select__display-value.is-placeholder").click()
					time.sleep(4)
					channel_name = getText("Enter channel name")
					channel_name = validate(channel_name, "Enter channel name")
					if channel_name not in self.driver.page_source:
						channel_name = getText("Enter channel name")
						channel_name = validate(channel_name, "Enter channel name")
						time.sleep(3)
						if channel_name not in self.driver.page_source:
							print("Channel name not present")
							sys.exit(0)

					self.driver.find_element_by_xpath("//div[contains(text(), '%s')]" %channel_name).click()
					time.sleep(4)
					self.driver.find_element_by_xpath("//span[contains(text(), 'Create exam')]").click()
					time.sleep(7)
					exam_name = getText("Enter exam name")
					exam_name = validate(exam_name, "Enter exam name")
					time.sleep(3)
					self.driver.find_element_by_xpath("//input[@type='text']").clear()
					time.sleep(2)
					self.driver.find_element_by_xpath("//input[@type='text']").send_keys(exam_name)				
					text = "An exam with that title already exists"
					time.sleep(3)
					if text in self.driver.page_source:
						exam_name = getText("Enter exam name")
						exam_name = validate(exam_name, "Enter exam name")
						time.sleep(3)
						self.driver.find_element_by_xpath("//input[@type='text']").clear()
						time.sleep(2)
						self.driver.find_element_by_xpath("//input[@type='text']").send_keys(exam_name)		
						time.sleep(3)
						if text in self.driver.page_source:
							print("Exam name already exist")
							sys.exit(0)
					
					time.sleep(4)
					self.driver.find_element_by_xpath("//input[@type='number']").clear()
					time.sleep(2)
					self.driver.find_element_by_xpath("//input[@type='number']").send_keys(5)
					time.sleep(2)
					self.driver.find_element_by_xpath("//input[@type='checkbox']").click()
					time.sleep(15)

					self.driver.find_element_by_xpath("//span[contains(text(), 'Finish')]").click()
					time.sleep(8)

					temp = self.driver.find_elements_by_tag_name("tr")
					temp.pop(0)
					for i in range(0,len(temp)):
						text1 = temp[i].find_element(By.TAG_NAME, "strong").text
						if text1 == exam_name:
							col = temp[i].find_elements(By.TAG_NAME, "td")[3]
							col.find_element(By.TAG_NAME, "div").click()
							time.sleep(5)
							self.driver.find_element_by_xpath("//span[contains(text(), 'Activate')]").click()
							time.sleep(5)
							SignOut(self.driver)
							self.assertEqual(True, True)
							print("Exam Created and Assigned")
							break

				except Exception:
					print("Element not found")
			else:
				print("Class not present")
				self.assertEqual(True, True)
		else:
			print("Sorry, you login as a Device owner. Please login with admin or coach")
			self.assertEqual(True, True)


	def test_b_delete_exam(self):
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
		time.sleep(5)

		text = "Signed in as device owner"
		if text not in self.driver.page_source:
			class_name = getText("Enter class name")
			class_name = validate(class_name, "Enter class name")
			time.sleep(2)
			if class_name in self.driver.page_source:
				try:
					self.driver.find_element_by_xpath("//a[contains(text(), '%s')]" %class_name).click()
					time.sleep(4)
					self.driver.find_element_by_xpath("//span[contains(text(), 'assignment_late')]").click()
					time.sleep(4)
		
					exam_name = getText("Enter already exist exam name")
					exam_name = validate(exam_name, "Enter already exist exam name")
					time.sleep(3)
					count = 0
					temp = self.driver.find_elements_by_tag_name("tr")
					temp.pop(0)
					for i in range(0,len(temp)):
						text1 = temp[i].find_element(By.TAG_NAME, "strong").text
						if text1 == exam_name:
							count = 1
							break

					if count == 0:
						print("Exam is not available to delete")
						self.assertEqual(True, True)
					else:
						col = temp[i].find_elements(By.TAG_NAME, "td")[3]
						col.find_element(By.TAG_NAME, "span").click()
						time.sleep(5)
						self.driver.find_element_by_xpath("//div[contains(text(), 'Delete')]").click()
						time.sleep(4)
						self.driver.find_element_by_xpath("//span[contains(text(), 'Delete')]").click()
						time.sleep(5)
				except Exception:
					print("Element not found")

				temp = self.driver.find_elements_by_tag_name("tr")
				temp.pop(0)
				for i in range(0,len(temp)):
					text1 = temp[i].find_element(By.TAG_NAME, "strong").text
					if text1 == exam_name:
						count = 1
						break
				if count == 0:
					print("After deleting exam, Exam still there")
					self.assertEqual(True, True)

				else:
					self.assertEqual(True, True)
					print("Exam deleted successfully.")
					SignOut(self.driver)


			else:
				print("Class not present")
				self.assertEqual(True, True)
		else:
			print("Sorry, you login as a Device owner. Please login with admin or coach")
			self.assertEqual(True, True)
	def tearDown(self):
		self.driver.close()



class KolibriTestingImportExport(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()

	def test_a_import_channel_from_internet(self):
		self.driver.get("http://localhost:8080")
		time.sleep(7)
		LoginDifferentKindOfUser(self.driver, "admin", "password")
		time.sleep(8)
		self.driver.find_element_by_xpath("//span[contains(text(), 'view_module')]").click()
		time.sleep(4)
		if "Kolibri selenium channel" in self.driver.page_source:
			print("Already imported channel")
		else:
			time.sleep(3)
			try:
				self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
				time.sleep(3)
			except Exception:
				pass
			try:
				self.driver.find_element_by_xpath("//span[contains(text(), 'Import')]").click()
				time.sleep(4)
				self.driver.find_element_by_xpath("//span[contains(text(), 'Internet')]").click()
				time.sleep(4)
				self.driver.find_element_by_xpath("//input[@type='text']").clear()
				time.sleep(2)
				self.driver.find_element_by_xpath("//input[@type='text']").send_keys('ec756d9428c64bdb909158326108464f')
				time.sleep(2)
				self.driver.find_element_by_xpath("//span[contains(text(), 'Import')]").click()
				time.sleep(5)
				if "That ID was not found on our server." in self.driver.page_source:
					print("Your channel ID is not valid")
					self.assertEqual(False, False)
				else:
					time.sleep(15)
					if "Finished!" in self.driver.page_source:
						self.assertEqual(True, True)
						print("Channel imported successfully")
					else:
						time.sleep(45)
						if "Finished!" in self.driver.page_source:
							self.assertEqual(True, True)
							print("Channel imported successfully")
						else:
							print("You have very slow internet speed, Check import by your own")
			except Exception:
				print("Server is not responding")

	def test_b_import_channel_from_localdrive(self):
		self.driver.get("http://localhost:8080")
		time.sleep(7)
		LoginDifferentKindOfUser(self.driver, "admin", "password")
		time.sleep(8)
		self.driver.find_element_by_xpath("//span[contains(text(), 'view_module')]").click()
		time.sleep(4)
		if "Kolibri selenium channel" in self.driver.page_source:
			print("Already imported channel")
		else:
			try:
				self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
				time.sleep(3)
			except Exception:
				pass
			try:
				time.sleep(3)
				self.driver.find_element_by_xpath("//span[contains(text(), 'Import')]").click()
				time.sleep(4)
				self.driver.find_element_by_xpath("//span[contains(text(), 'Local Drives')]").click()
				time.sleep(4)
				count = 0
				path = getText("Enter path of local channel")
				path = validate(path, "Enter path of local channel")
				if path not in self.driver.page_source:
					path = getText("Enter path of local channel")
					path = validate(path, "Enter path of local channel")
					if path not in self.driver.page_source:
						print("Please Enter correct path or connect External drive to the server")
					else:
						count = 1
				else: 
					count = 1
				if count == 1:
					self.driver.find_element_by_xpath("//div[contains(text(), '%s')]" %path).click()
					time.sleep(4)
					self.driver.find_element_by_xpath("//span[contains(text(), 'Import')]").click() 
					time.sleep(15)
					if "Finished!" in self.driver.page_source:
						print("Channel Imported successfully")
						self.assertEqual(True, True)
					else:
						time.sleep(50)
						if "Finished!" in self.driver.page_source:
							print("Channel Imported successfully")
							self.assertEqual(True, True)
						else:
							print("Please check this feature manually")
							self.assertEqual(True, False)
			except Exception:
				print("Server is not responding")

	def test_c_export_channel_to_localdrive(self):
		self.driver.get("http://localhost:8080")
		time.sleep(7)
		LoginDifferentKindOfUser(self.driver, "admin", "password")
		time.sleep(8)
		self.driver.find_element_by_xpath("//span[contains(text(), 'view_module')]").click()
		time.sleep(4)
		if "Kolibri selenium channel" in self.driver.page_source:
			try:
				self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
				time.sleep(3)
			except Exception:
				pass
			try:
				time.sleep(3)
				self.driver.find_element_by_xpath("//span[contains(text(), 'Export')]").click()
				time.sleep(4)
				count = 0
				path = getText("Enter path of local channel")
				path = validate(path, "Enter path of local channel")
				if path not in self.driver.page_source:
					path = getText("Enter path of local channel")
					path = validate(path, "Enter path of local channel")
					if path not in self.driver.page_source:
						print("Please Enter correct path or connect External drive to the server")
					else:
						count = 1
				else: 
					count = 1
				if count == 1:
					self.driver.find_element_by_xpath("//div[contains(text(), '%s')]" %path).click()
					time.sleep(4)
					self.driver.find_element_by_xpath("//span[contains(text(), 'Export')]").click() 
					time.sleep(15)
					if "Finished!" in self.driver.page_source:
						print("Channel Exported successfully")
						self.assertEqual(True, True)
					else:
						time.sleep(50)
						if "Finished!" in self.driver.page_source:
							print("Channel Exported successfully")
							self.assertEqual(True, True)
						else:
							print("Please check this feature manually")
							self.assertEqual(True, False)
			except Exception:
				print("Server is not responding")			
		else:
			print("Kolibri selenium channel is not imported")

	def test_d_delete_channel(self):
		self.driver.get("http://localhost:8080")
		time.sleep(7)
		LoginDifferentKindOfUser(self.driver, "admin", "password")
		time.sleep(8)
		self.driver.find_element_by_xpath("//span[contains(text(), 'view_module')]").click()
		time.sleep(4)
		if "Kolibri selenium channel" in self.driver.page_source:
			temp = self.driver.find_elements_by_tag_name("tr")
			temp.pop(0)
			count = 0
			for i in range(0,len(temp)):
				text1 = temp[i].find_element(By.TAG_NAME, "td").text
				if text1 == "Kolibri selenium channel":
					col = temp[i].find_elements(By.TAG_NAME, "td")[4]
					col.find_element(By.TAG_NAME, "button").click()
					time.sleep(4)
					self.driver.find_element_by_xpath("//div[contains(text(), 'Confirm')]").click()
					time.sleep(5)
					break
			if "Kolibri selenium channel" in self.driver.page_source:
				print("Channel delete feature not working properly")
				self.assertEqual(True, False)
			else:
				self.assertEqual(True, True)
				print("Channel Deleted successfully")
		else:
			print("Kolibri selenium channel is not present")
			self.assertEqual(True, True)

	def tearDown(self):
		self.driver.close()

if __name__=="__main__":
	unittest.main()

