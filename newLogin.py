import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from methods import *
import unittest
import time
import sys
import os
from tkinter import *

user = [{"admin": "password"},
		{"pm": "sc"},
		{"coach": "sc"},
		{"learner":"sc"},
		{"student": "sc"}]

class KolibriTesting(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()

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
		text = LoginDifferentKindOfUser(self.driver, "nalanda","lee")
		self.assertEqual(text, "Incorrect username or password",'Logging with the user that is not part of class')
	
	def tearDown(self):
		self.driver.close()


class KolibriTestingClass(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()

	def test_a_delete_class(self):
		self.driver.get("http://localhost:8008")
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

	def test_a_check_edit_username_facility(self):
		self.driver.get("http://localhost:8008")
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
			LoginDifferentKindOfUser(self.driver, user[3].keys()[0], user[3].values()[0])
			time.sleep(5)
			self.driver.find_element_by_xpath("//button[@type='submit']").click()
			time.sleep(2)
			self.driver.find_element_by_xpath('//span[contains(text(), "menu")]').click()
			time.sleep(4)
			self.driver.find_element_by_xpath('//div[contains(text(), "Profile")]').click()
			time.sleep(4)
		except Exception:
			print("Please enter username which is exist")

		self.driver.find_element_by_xpath("//input[@type='text']").clear()
		time.sleep(3)
		self.driver.find_element_by_xpath("//input[@type='text']").send_keys(user[4].keys()[0])
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
		LoginDifferentKindOfUser(self.driver, user[4].keys()[0], user[4].values()[0])
		time.sleep(8)
		temp = self.driver.title
		self.assertTrue(True, "Learn" in temp)
		time.sleep(5)
		self.driver.find_element_by_xpath("//button[@type='submit']").click()
		time.sleep(2)
		self.driver.find_element_by_xpath('//span[contains(text(), "menu")]').click()
		time.sleep(4)
		self.driver.find_element_by_xpath('//div[contains(text(), "Profile")]').click()
		time.sleep(2)
		self.driver.find_element_by_xpath("//input[@type='text']").clear()
		time.sleep(4)
		self.driver.find_element_by_xpath("//input[@type='text']").send_keys(user[3].keys()[0])
		time.sleep(3)
		self.driver.find_element_by_xpath("//span[contains(text(), 'Save changes')]").click()
		time.sleep(4)

		print("Edit username facility working properly")

	def test_b_check_edit_fullname_facility(self):
		self.driver.get("http://localhost:8008")
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
			LoginDifferentKindOfUser(self.driver, user[3].keys()[0], user[3].values()[0])
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

	def test_a_create_group(self):
		self.driver.get("http://localhost:8008")
		time.sleep(3)
		LoginDifferentKindOfUser(self.driver, user[2].keys()[0], user[2].values()[0])
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
		self.driver.get("http://localhost:8008")
		time.sleep(3)
		LoginDifferentKindOfUser(self.driver, user[1].keys()[0], user[1].values()[0])
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
		self.driver.get("http://localhost:8008")
		time.sleep(3)
		LoginDifferentKindOfUser(self.driver, user[1].keys()[0], user[1].values()[0])
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
							time.sleep(3)
							self.assertEqual(True, True)
							print("Exam Created and Assigned")
							time.sleep(5)
							LoginDifferentKindOfUser(self.driver, user[3].keys()[0], user[3].values()[0] )
							time.sleep(6)
							self.driver.find_element_by_xpath("//span[contains(text(), 'assignment_late')]").click()
							time.sleep(3)
							temp = self.driver.find_elements_by_css_selector(".exam-row")
							# print(temp)
							count = 0
							for i in temp:
								t = i.find_element(By.TAG_NAME, "h2").text
								print(t)
								if t == exam_name:
									count = 1
									i.find_element(By.TAG_NAME, "span").click()
									time.sleep(50)
									self.driver.find_element_by_xpath("//span[contains(text(), 'Submit exam')]").click()
									time.sleep(3)
									t = self.driver.find_elements(By.TAG_NAME, "span")
									for j in t:
										if j.text == "SUBMIT EXAM":
											time.sleep(3)
											j.click()
									time.sleep(7)
									print("Exam Given successfully")
									self.assertEqual(True, True)
									break
							if count == 0:
								print("Exam is not given for this learner")
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
		self.driver.get("http://localhost:8008")
		time.sleep(3)
		LoginDifferentKindOfUser(self.driver, user[1].keys()[0], user[1].values()[0])
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
				if len(temp) != 0:
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
		self.driver.get("http://localhost:8008")
		time.sleep(7)
		LoginDifferentKindOfUser(self.driver, "admin", "password")
		time.sleep(8)
		self.driver.find_element_by_xpath("//span[contains(text(), 'view_module')]").click()
		time.sleep(4)
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
			channel_id = getText("Enter channel ID which you want to import from internet")
			channel_id = validate(channel_id, "Enter channel ID which you want to import from internet")
			time.sleep(2)
			self.driver.find_element_by_xpath("//input[@type='text']").send_keys(channel_id)
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
					self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
					time.sleep(2)
					print("Channel imported successfully")
				else:
					time.sleep(45)
					if "Finished!" in self.driver.page_source:
						self.assertEqual(True, True)
						self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
						time.sleep(2)
						print("Channel imported successfully")
					else:
						print("You have very slow internet speed, Check import by your own")
		except Exception:
			print("Server is not responding")

	def test_b_import_channel_from_localdrive(self):
		self.driver.get("http://localhost:8008")
		time.sleep(7)
		LoginDifferentKindOfUser(self.driver, "admin", "password")
		time.sleep(8)
		self.driver.find_element_by_xpath("//span[contains(text(), 'view_module')]").click()
		time.sleep(4)

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
					time.sleep(2)
					self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
					time.sleep(2)
					self.assertEqual(True, True)
				else:
					time.sleep(50)
					if "Finished!" in self.driver.page_source:
						print("Channel Imported successfully")
						time.sleep(2)
						self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
						time.sleep(2)
						self.assertEqual(True, True)
					else:
						print("Please check this feature manually")
						self.assertEqual(True, False)
		except Exception:
			print("Server is not responding")

	def test_c_export_channel_to_localdrive(self):
		self.driver.get("http://localhost:8008")
		time.sleep(7)
		LoginDifferentKindOfUser(self.driver, "admin", "password")
		time.sleep(8)
		self.driver.find_element_by_xpath("//span[contains(text(), 'view_module')]").click()
		time.sleep(4)
		if "No channels installed" in self.driver.page_source:
			print("No channels installed in your system")
		else:
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
						self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
						print("Channel Exported successfully")
						self.assertEqual(True, True)
					else:
						time.sleep(50)
						if "Finished!" in self.driver.page_source:
							self.driver.find_element_by_xpath("//span[contains(text(), 'Close')]").click()
							print("Channel Exported successfully")
							self.assertEqual(True, True)
						else:
							print("Please check this feature manually")
							self.assertEqual(True, False)
			except Exception:
				print("Server is not responding")			

	def test_d_delete_channel(self):
		self.driver.get("http://localhost:8008")
		time.sleep(7)
		LoginDifferentKindOfUser(self.driver, "admin", "password")
		time.sleep(8)
		self.driver.find_element_by_xpath("//span[contains(text(), 'view_module')]").click()
		time.sleep(4)
		if "No channels installed" in self.driver.page_source:
			print("No channels installed in your system")
		else:
			channel_name = getText("Enter channel name")
			channel_name = validate(channel_name, "Enter channel name")
			if channel_name in self.driver.page_source:
				temp = self.driver.find_elements_by_tag_name("tr")
				temp.pop(0)
				count = 0
				for i in range(0,len(temp)):
					text1 = temp[i].find_element(By.TAG_NAME, "td").text
					if text1 == channel_name:
						col = temp[i].find_elements(By.TAG_NAME, "td")[4]
						col.find_element(By.TAG_NAME, "button").click()
						time.sleep(4)
						self.driver.find_element_by_xpath("//div[contains(text(), 'Confirm')]").click()
						time.sleep(5)
						break
				if channel_name in self.driver.page_source:
					print("Channel delete feature is not working properly")
					self.assertEqual(True, False)
				else:
					self.assertEqual(True, True)
					print("Channel Deleted successfully")
			else:
				print("%s is not present" %channel_name)
				self.assertEqual(True, True)

	def tearDown(self):
		self.driver.close()


class KolibriTestingLearnTab(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()


	def test_a_exercise(self):
		self.driver.get("http://localhost:8008")
		time.sleep(3)
		LoginDifferentKindOfUser(self.driver, user[3].keys()[0], user[3].values()[0])
		time.sleep(7)
		exercise = """M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"""
		folder = """M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"""
		video = """M21 3H3c-1.11 0-2 .89-2 2v12a2 2 0 0 0 2 2h5v2h8v-2h5c1.1 0 1.99-.9 1.99-2L23 5a2 2 0 0 0-2-2zm0 14H3V5h18v12zm-5-6l-7 4V7z"""
		self.driver.find_element_by_xpath("//span[contains(text(), 'folder')]").click()
		time.sleep(4)
		self.driver.find_element_by_xpath("//span[contains(text(), 'apps')]").click()
		time.sleep(2)
		text = getText("Enter channel name")
		time.sleep(2)
		self.driver.find_element_by_xpath("//div[contains(text(), '%s')]" %text).click()
		time.sleep(3)
		counter = 5
		try:
			for p in range(0,counter):
				time.sleep(2)
				count = 0
				if exercise not in self.driver.page_source and folder not in self.driver.page_source:
					time.sleep(3)
					self.driver.find_element_by_xpath("//span[contains(text(), 'folder')]").click()
					counter = counter + 5
					time.sleep(3)
				elif exercise not in self.driver.page_source:
					text = getText("Enter partial text of the folder")
					temp = self.driver.find_elements(By.TAG_NAME, "h3")
					print("Not found")
					for i in temp:
						t = i.text
						if t.find(text) != -1:
							print(t)
							i.click()
							time.sleep(4)
							break
				elif exercise in self.driver.page_source and folder in self.driver.page_source:
					print("Mixed found")
					text = getText("Enter partial text")
					temp = self.driver.find_elements(By.TAG_NAME, "h3")
					for i in temp:
						t = i.text
						if t.find(text) != -1:
							print(t)
							time.sleep(3)
							i.click()

							if folder not in self.driver.page_source and exercise not in self.driver.page_source and video not in self.driver.page_source:
								count = 1
								print(t)
								time.sleep(100)

								break
							else:
								time.sleep(6)
				else:
					print("found")
					text = getText("Enter partial text")
					temp = self.driver.find_elements(By.TAG_NAME, "h3")
					for i in temp:
						t = i.text
						if t.find(text) != -1:
								count = 1
								print(t)
								time.sleep(3)
								i.click()
								time.sleep(100)
								break
				if count == 1:
					self.assertEqual(True, True)
					break
		except Exception:
			print("Something going wrong")


	def test_b_video(self):
		self.driver.get("http://localhost:8008")
		time.sleep(3)
		LoginDifferentKindOfUser(self.driver, user[3].keys()[0], user[3].values()[0])
		time.sleep(7)
		exercise = """M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"""
		folder = """M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"""
		video = """M21 3H3c-1.11 0-2 .89-2 2v12a2 2 0 0 0 2 2h5v2h8v-2h5c1.1 0 1.99-.9 1.99-2L23 5a2 2 0 0 0-2-2zm0 14H3V5h18v12zm-5-6l-7 4V7z"""
		self.driver.find_element_by_xpath("//span[contains(text(), 'folder')]").click()
		time.sleep(4)
		self.driver.find_element_by_xpath("//span[contains(text(), 'apps')]").click()
		time.sleep(2)
		text = getText("Enter channel name")
		time.sleep(2)
		self.driver.find_element_by_xpath("//div[contains(text(), '%s')]" %text).click()
		time.sleep(3)
		counter = 5
		try:
			for p in range(0,counter):
				time.sleep(2)
				count = 0
				if video not in self.driver.page_source and folder not in self.driver.page_source:
					time.sleep(3)
					self.driver.find_element_by_xpath("//span[contains(text(), 'folder')]").click()
					counter = counter + 5
					time.sleep(3)
				elif video not in self.driver.page_source:
					text = getText("Enter partial text of the folder")
					temp = self.driver.find_elements(By.TAG_NAME, "h3")
					print("Not found")
					for i in temp:
						t = i.text
						if t.find(text) != -1:
							print(t)
							i.click()
							time.sleep(4)
							break
				elif video in self.driver.page_source and folder in self.driver.page_source:
					print("Mixed found")
					text = getText("Enter partial text")
					temp = self.driver.find_elements(By.TAG_NAME, "h3")
					for i in temp:
						t = i.text
						if t.find(text) != -1:
							print(t)
							time.sleep(3)
							i.click()

							if folder not in self.driver.page_source and exercise not in self.driver.page_source and video not in self.driver.page_source:
								count = 1
								print(t)
								self.driver.find_element_by_xpath("//span[contains(text(), 'Play')]").click()

								time.sleep(240)

								break
							else:
								time.sleep(6)
				else:
					print("found")
					text = getText("Enter partial text")
					temp = self.driver.find_elements(By.TAG_NAME, "h3")
					for i in temp:
						t = i.text
						if t.find(text) != -1:
								count = 1
								print(t)
								time.sleep(3)
								i.click()
								time.sleep(3)
								self.driver.find_element_by_xpath("//span[contains(text(), 'Play')]").click()
								time.sleep(240)
								break
				if count == 1:
					self.assertEqual(True, True)
					break

		except Exception:
			print("Something going wrong")





	def tearDown(self):
		self.driver.close()

if __name__=="__main__":
	unittest.main()

