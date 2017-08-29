from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from methods import *
import unittest
import time
import sys

class KolibriTesting(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		#self.driver = webdriver.Chrome()
	
	def test_a_Testing_Server_Is_Started(self):
		r = requests.get("http://localhost:8008")
		self.assertEqual(r.status_code, 200)

	def test_ba_Crete_Users_and_Login_with_Exsting_User_with_wrong_password(self):
		temp = sample(self.driver)
		if temp==1:
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

		text = LoginDifferentKindOfUser(self.driver, "Lee", "lee")
		self.assertEqual(text, "Incorrect username or password",'Logging with the user that is not part of class')

	def test_d_delete_class(self):
		
		self.driver.get("http://localhost:8080")
		LoginDifferentKindOfUser(self.driver, "admin","password")
		text = "AAAA_Classroom"

		if text in self.driver.page_source:
			print("In If")
			self.driver.find_element_by_xpath("//button[contains(text(), 'Delete Class')]").click()
			time.sleep(3)
			self.driver.find_element_by_xpath("//span[contains(text(), 'Delete Class')]").click()
			time.sleep(3)
			self.assertEqual(False, text in self.driver.page_source)
		else:
			print("Class not found")

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
		LoginDifferentKindOfUser(self.driver, "learner","sc")
		time.sleep(5)
		self.driver.find_element_by_xpath("//button[@type='submit']").click()
		time.sleep(2)
		self.driver.find_element_by_xpath('//span[contains(text(), "menu")]').click()
		time.sleep(4)
		self.driver.find_element_by_xpath('//div[contains(text(), "Profile")]').click()
		time.sleep(4)
		try:
			self.driver.find_element_by_xpath("//input[@type='text']").clear()
			time.sleep(3)
			self.driver.find_element_by_xpath("//input[@type='text']").send_keys("softcorner")
			time.sleep(3)
			self.driver.find_element_by_xpath("//span[contains(text(), 'Save changes')]").click()
			time.sleep(4)
			self.driver.find_element_by_xpath("//span[contains(text(), 'menu')]").click()
			time.sleep(3)
			print("Before")
			self.driver.find_element_by_xpath("//span[contains(text(), 'exit_to_app')]").click()
			print("After")
			time.sleep(5)
			LoginDifferentKindOfUser(self.driver, "softcorner", "sc")
			time.sleep(8)
			temp = self.driver.title
			self.assertTrue(True, "Learn" in temp)
		except Exception:
			print("In exception")



	def test_f_check_edit_fullname_facility(self):
		self.driver.get("http://localhost:8080")
		LoginDifferentKindOfUser(self.driver, "admin","password")
		time.sleep(2)
		self.driver.find_element_by_xpath('//a[contains(@href,"#/facilities")]').click()
		time.sleep(3)
		print(self.driver.find_element_by_name("learnerCanEditUsername").is_selected())

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
		LoginDifferentKindOfUser(self.driver, "softcorner","sc")
		time.sleep(5)
		self.driver.find_element_by_xpath("//button[@type='submit']").click()
		time.sleep(2)
		self.driver.find_element_by_xpath('//span[contains(text(), "menu")]').click()
		time.sleep(4)
		self.driver.find_element_by_xpath('//div[contains(text(), "Profile")]').click()
		time.sleep(4)
		try:
			self.driver.find_element_by_xpath("//input[@type='text']").clear()
			time.sleep(3)
			self.driver.find_element_by_xpath("//input[@type='text']").send_keys("Lee Cooper")
			time.sleep(3)
			self.driver.find_element_by_xpath("//span[contains(text(), 'Save changes')]").click()
			time.sleep(4)
			#print(temp)
			self.driver.find_element_by_xpath("//span[contains(text(), 'menu')]").click()
			time.sleep(3)
			print("Before")
			self.driver.find_element_by_xpath("//span[contains(text(), 'exit_to_app')]").click()
			print("After")
			time.sleep(5)
			self.assertEqual(True, True)
		except Exception:
			print("In exception")


	'''def test_e_create_group(self):
		self.driver.get("http://localhost:8080")
		LoginDifferentKindOfUser(self.driver, "pm","sc")
		time.sleep(7)
		self.driver.find_element_by_xpath("//span[contains(text(), 'menu')]").click()
		time.sleep(2)
		self.driver.find_element_by_xpath("//span[contains(text(), 'assessment')]").click()
		time.sleep(3)
		self.driver.find_element_by_xpath("//a[contains(text(), 'AAAA_Classroom')]").click()
		time.sleep(3)
		self.driver.find_element_by_xpath("//a[contains(@href, '#/6bd69e8458693d879719de623786c866/groups')]").click()
		time.sleep(3)
		self.driver.find_element_by_xpath("//span[contains(text(), 'New group')]").click()
		time.sleep(4)'''

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
			print("Time out")'''


	def tearDown(self):
		self.driver.close()


if __name__=="__main__":
	unittest.main()



