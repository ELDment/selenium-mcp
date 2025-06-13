from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from typing import Optional, Tuple
import time

class BrowserController:
	def __init__(self, driver: webdriver.Chrome):
		"""初始化浏览器控制器"""
		self.driver = driver
		self.actionChains = ActionChains(driver)
		self.wait = WebDriverWait(driver, 10)
	
	def ClickElement(self, selector: str, byType: By = By.CSS_SELECTOR, timeout: int = 10) -> bool:
		"""点击页面元素"""
		try:
			element = WebDriverWait(self.driver, timeout).until(
				EC.element_to_be_clickable((byType, selector))
			)
			element.click()
			return True
		except Exception as e:
			print(f"点击元素失败: {e}")
			return False
	
	def ClickElementByCoordinates(self, x: int, y: int) -> bool:
		"""根据绝对坐标点击页面"""
		try:
			# 使用JavaScript执行点击，确保坐标准确
			self.driver.execute_script(f"document.elementFromPoint({x}, {y}).click();")
			return True
		except Exception as e:
			print(f"坐标点击失败: {e}")
			return False
	
	def ScrollWheel(self, deltaY: int, element: Optional[str] = None) -> bool:
		"""滑动滚轮"""
		try:
			if element:
				targetElement = self.driver.find_element(By.CSS_SELECTOR, element)
				self.actionChains.move_to_element(targetElement).perform()
			
			self.driver.execute_script(f"window.scrollBy(0, {deltaY});")
			return True
		except Exception as e:
			print(f"滚轮滑动失败: {e}")
			return False
	
	def ScrollToElement(self, selector: str, byType: By = By.CSS_SELECTOR) -> bool:
		"""滚动到指定元素"""
		try:
			element = self.driver.find_element(byType, selector)
			self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
			return True
		except Exception as e:
			print(f"滚动到元素失败: {e}")
			return False
	
	def HoverElement(self, selector: str, byType: By = By.CSS_SELECTOR) -> bool:
		"""悬停在元素上"""
		try:
			element = self.driver.find_element(byType, selector)
			self.actionChains.move_to_element(element).perform()
			return True
		except Exception as e:
			print(f"元素悬停失败: {e}")
			return False
	
	def DragAndDrop(self, sourceSelector: str, targetSelector: str, byType: By = By.CSS_SELECTOR) -> bool:
		"""拖拽元素"""
		try:
			sourceElement = self.driver.find_element(byType, sourceSelector)
			targetElement = self.driver.find_element(byType, targetSelector)
			self.actionChains.drag_and_drop(sourceElement, targetElement).perform()
			return True
		except Exception as e:
			print(f"拖拽操作失败: {e}")
			return False
	
	def SendKeys(self, selector: str, text: str, byType: By = By.CSS_SELECTOR, clearFirst: bool = True) -> bool:
		"""向元素输入文本"""
		try:
			element = self.driver.find_element(byType, selector)
			if clearFirst:
				element.clear()
			element.send_keys(text)
			return True
		except Exception as e:
			print(f"文本输入失败: {e}")
			return False
	
	def PressKey(self, key: Keys) -> bool:
		"""按下键盘按键"""
		try:
			self.actionChains.send_keys(key).perform()
			return True
		except Exception as e:
			print(f"按键操作失败: {e}")
			return False
	
	def WaitForElement(self, selector: str, byType: By = By.CSS_SELECTOR, timeout: int = 10) -> bool:
		"""等待元素出现"""
		try:
			WebDriverWait(self.driver, timeout).until(
				EC.presence_of_element_located((byType, selector))
			)
			return True
		except Exception as e:
			print(f"等待元素失败: {e}")
			return False
	
	def GetElementText(self, selector: str, byType: By = By.CSS_SELECTOR) -> Optional[str]:
		"""获取元素文本"""
		try:
			element = self.driver.find_element(byType, selector)
			return element.text
		except Exception as e:
			print(f"获取元素文本失败: {e}")
			return None
	
	def IsElementVisible(self, selector: str, byType: By = By.CSS_SELECTOR) -> bool:
		"""检查元素是否可见"""
		try:
			element = self.driver.find_element(byType, selector)
			return element.is_displayed()
		except Exception:
			return False
	
	def Sleep(self, seconds: float) -> None:
		"""等待指定时间"""
		time.sleep(seconds)