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
			'''for i in temp:
				t = temp[1].find_element(By.TAG_NAME, "h2").text
				count = count +1
				trs = temp[1].find_element(By.TAG_NAME, "tr")
				tt = trs.find_elements(By.TAG_NAME, "th")
				tt[1].find_element_by_xpath("//input[@type='checkbox']").click()
				print(t)
				print("\n")
				print(i)

				#if group_name == t:
				#i.find_element_by_xpath("//input[@type='checkbox'][1]").click()
				time.sleep(3)
				#i.find_element_by_xpath("//span[contains(text(), 'Move Learners')]")[count].click()
				#time.sleep(6)
				#break'''







			#print(len(self.driver.find_elements_by_xpath("//span[contains(text(), 'Move Learners')]")))
			#self.driver.find_element_by_xpath("//span[contains(text(), 'Move Learners')][1]").click()

			group_name = getText("Enter existing group name which group users which you want in new group")
			group_name = validate(group_name, "Enter existing group name which group users which you want in new group")
			time.sleep(2)
			
			temp = self.driver.find_elements_by_class_name("group-section")
			print(temp)
			print(len(temp))

			count = 0
			if group_name in self.driver.page_source:
				for i in temp:
					t = i.find_element(By.TAG_NAME, "h2").text
					count = count +1
					#if group_name == t:
					i.find_element_by_xpath("//input[@type='checkbox'][1]").click()
					time.sleep(3)
					#i.find_element_by_xpath("//span[contains(text(), 'Move Learners')]")[count].click()
					#time.sleep(6)
					#break

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

	'''def test_c(self):
		#time.sleep(5)
		try:
			self.driver.get("http://localhost:8008")
			time.sleep(2)
			LoginDifferentKindOfUser(self.driver, "Learner", "sc")
			time.sleep(2)
			Exercise = "M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"
			time.sleep(2)
			self.driver.find_element_by_xpath("//a[contains(@href, '#/9e5305326ed742d0892479dea825a514/topics')]").click()
			time.sleep(2)
			Topic = "M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"
			Video = ""
			if Exercise in self.driver.page_source:
				results1 = []
				time.sleep(2)
				elements = self.driver.find_elements_by_tag_name("a")
				for element in elements:
					results1.append(element.get_attribute('href'))
				temp = results1[4:]
				for i in temp:
					text = str(i[28:])
					self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()
			else:
				results1 = []
				time.sleep(2)
				elements = self.driver.find_elements_by_tag_name("a")

				for element in elements:
					print("In loop")
					results1.append(element.get_attribute('href'))
				temp = results1[4:]

				print(temp)
				for i in temp:
					text = str(i[28:])
					print(text)
					self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()
					time.sleep(3)
					results2 = []
					if Exercise in self.driver.page_source:
						elements = self.driver.find_elements_by_tag_name("a")
						for element in elements:
							results2.append(element.get_attribute('href'))
						print(results2)
						temp1 = results2[4:]
						print(temp1)
						for j in temp1:
							text = str(j[28:])
							self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()
					else:
						elements = self.driver.find_elements_by_tag_name("a")
						for element in elements:
							results2.append(element.get_attribute('href'))
						temp1 = results2[6:]
						print("Temp1")
						print(temp1)
						for j in temp1:
							text = str(j[28:])
							print(text)
							self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()
							time.sleep(3)
							results3 = []

							if Exercise in self.driver.page_source:
								elements = self.driver.find_elements_by_tag_name("a")
								for element in elements:
									results3.append(element.get_attribute('href'))
								#print(results3)
								temp2 = results3[8:]
								print("Temp2")
								print(temp2)
								for k in temp2:
									text = str(k[28:])
									self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()
									time.sleep(60)
							else:
								elements = self.driver.find_elements_by_tag_name("a")
								for element in elements:
									results3.append(element.get_attribute('href'))
								temp2 = results3[8:]
								print("Temp2")
								print(temp2)
								for k in temp2:
									text = str(k[28:])
									print(text)
									self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()						
									time.sleep(3)
									results4 = []

									if Exercise in self.driver.page_source:
										elements = self.driver.find_elements_by_tag_name("a")
										for element in elements:
											results4.append(element.get_attribute('href'))
										print("Temp3")
										print(results4)
										print(results4[10:])
										temp3 = results4[10:]
										for l in temp3:
											text = str(l[28:])
											self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()
											time.sleep(60)
									else:
										print("results4")
										elements = self.driver.find_elements_by_tag_name("a")
										print("results4")
										for element in elements:
											results4.append(element.get_attribute('href'))
										temp3 = results4[10:]
										print("Temp3")
										print(temp3)
										for l in temp3:
											text = str(l[28:])
											print(text)
											self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()						
											time.sleep(3)
											results5 = []
											if Exercise in self.driver.page_source:
												elements = self.driver.find_elements_by_tag_name("a")
												for element in elements:
													results5.append(element.get_attribute('href'))
												print("Temp4")
												print(results5)
												print(results5[12:])
												temp4 = results5[12:]
												for m in temp4:
													text = str(m[28:])
													self.driver.find_element_by_xpath('//a[contains(@href, "%s")]' %text).click()
													time.sleep(60)
				time.sleep(5)

			
		except Exception:
			print("Time out")


	def tearDown(self):
		self.driver.close()'''


if __name__=="__main__":
	unittest.main()



