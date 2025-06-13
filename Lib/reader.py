from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Dict, Optional, Any, Tuple

class PageReader:
	def __init__(self, driver: webdriver.Chrome):
		self.driver = driver
		self.wait = WebDriverWait(driver, 10)
	
	def GetPageTitle(self) -> str:
		"""获取页面标题"""
		return self.driver.title
	
	def GetPageUrl(self) -> str:
		"""获取当前页面URL"""
		return self.driver.current_url
	
	def GetPageSource(self) -> str:
		"""获取页面源代码"""
		return self.driver.page_source
	
	def GetElementText(self, selector: str, byType: By = By.CSS_SELECTOR) -> Optional[str]:
		"""获取单个元素的文本内容"""
		try:
			element = self.driver.find_element(byType, selector)
			return element.text.strip()
		except NoSuchElementException:
			return None
	
	def GetElementsText(self, selector: str, byType: By = By.CSS_SELECTOR) -> List[str]:
		"""获取多个元素的文本内容"""
		try:
			elements = self.driver.find_elements(byType, selector)
			return [element.text.strip() for element in elements if element.text.strip()]
		except NoSuchElementException:
			return []
	
	def GetElementAttribute(self, selector: str, attribute: str, byType: By = By.CSS_SELECTOR) -> Optional[str]:
		"""获取元素属性值"""
		try:
			element = self.driver.find_element(byType, selector)
			return element.get_attribute(attribute)
		except NoSuchElementException:
			return None
	
	def GetAllLinks(self) -> List[Dict[str, str]]:
		"""获取页面所有链接"""
		links = []
		try:
			elements = self.driver.find_elements(By.TAG_NAME, "a")
			for element in elements:
				href = element.get_attribute("href")
				text = element.text.strip()
				if href:
					links.append({
						"text": text,
						"href": href
					})
		except Exception as e:
			print(f"获取链接失败: {e}")
		return links
	
	def GetAllImages(self) -> List[Dict[str, str]]:
		"""获取页面所有图片"""
		images = []
		try:
			elements = self.driver.find_elements(By.TAG_NAME, "img")
			for element in elements:
				src = element.get_attribute("src")
				alt = element.get_attribute("alt") or ""
				if src:
					images.append({
						"alt": alt,
						"src": src
					})
		except Exception as e:
			print(f"获取图片失败: {e}")
		return images
	
	def GetTableData(self, selector: str, byType: By = By.CSS_SELECTOR) -> List[List[str]]:
		"""获取表格数据"""
		try:
			table = self.driver.find_element(byType, selector)
			rows = table.find_elements(By.TAG_NAME, "tr")
			tableData = []
			
			for row in rows:
				cells = row.find_elements(By.TAG_NAME, "td")
				if not cells:  # 如果没有td，尝试th
					cells = row.find_elements(By.TAG_NAME, "th")
				
				if cells:
					rowData = [cell.text.strip() for cell in cells]
					tableData.append(rowData)
			
			return tableData
		except NoSuchElementException:
			return []
	
	def GetFormData(self, selector: str, byType: By = By.CSS_SELECTOR) -> Dict[str, Any]:
		"""获取表单数据"""
		formData = {}
		try:
			form = self.driver.find_element(byType, selector)
			
			inputs = form.find_elements(By.TAG_NAME, "input")
			for input_elem in inputs:
				name = input_elem.get_attribute("name")
				value = input_elem.get_attribute("value")
				inputType = input_elem.get_attribute("type")
				
				if name:
					if inputType in ["checkbox", "radio"]:
						formData[name] = input_elem.is_selected()
					else:
						formData[name] = value or ""
			
			selects = form.find_elements(By.TAG_NAME, "select")
			for select in selects:
				name = select.get_attribute("name")
				if name:
					selectedOptions = select.find_elements(By.CSS_SELECTOR, "option:checked")
					if selectedOptions:
						formData[name] = [option.get_attribute("value") for option in selectedOptions]
					else:
						formData[name] = []
			
			textareas = form.find_elements(By.TAG_NAME, "textarea")
			for textarea in textareas:
				name = textarea.get_attribute("name")
				if name:
					formData[name] = textarea.text
					
		except NoSuchElementException:
			pass
		
		return formData
	
	def GetMetaTags(self) -> Dict[str, str]:
		"""获取页面meta标签信息"""
		metaData = {}
		try:
			metaTags = self.driver.find_elements(By.TAG_NAME, "meta")
			for meta in metaTags:
				name = meta.get_attribute("name") or meta.get_attribute("property")
				content = meta.get_attribute("content")
				if name and content:
					metaData[name] = content
		except Exception as e:
			print(f"获取meta标签失败: {e}")
		
		return metaData
	
	def GetPageText(self, removeEmpty: bool = True) -> str:
		"""获取页面所有文本内容"""
		try:
			bodyText = self.driver.find_element(By.TAG_NAME, "body").text
			if removeEmpty:
				lines = [line.strip() for line in bodyText.split('\n') if line.strip()]
				return '\n'.join(lines)
			return bodyText
		except NoSuchElementException:
			return ""
	
	def SearchTextInPage(self, searchText: str, caseSensitive: bool = False) -> List[Dict[str, Any]]:
		"""在页面中搜索文本"""
		results = []
		try:
			pageText = self.GetPageText()
			pattern = searchText if caseSensitive else searchText.lower()
			targetText = pageText if caseSensitive else pageText.lower()
			
			if pattern in targetText:
				# 使用XPath查找包含文本的元素
				xpath = f"//*[contains(text(), '{searchText}')]"
				elements = self.driver.find_elements(By.XPATH, xpath)
				
				for element in elements:
					results.append({
						"tag": element.tag_name,
						"text": element.text.strip(),
						"location": element.location
					})
		except Exception as e:
			print(f"搜索文本失败: {e}")
		
		return results
	
	def WaitForTextToAppear(self, text: str, timeout: int = 10) -> bool:
		"""等待指定文本出现在页面中"""
		try:
			WebDriverWait(self.driver, timeout).until(
				lambda driver: text in driver.page_source
			)
			return True
		except TimeoutException:
			return False
	
	def GetPageInfo(self) -> Dict[str, Any]:
		"""获取页面完整信息"""
		return {
			"title": self.GetPageTitle(),
			"url": self.GetPageUrl(),
			"meta": self.GetMetaTags(),
			"links_count": len(self.GetAllLinks()),
			"images_count": len(self.GetAllImages()),
			"text_length": len(self.GetPageText())
		}
		
	def GetElementCenter(self, selector: str, byType: By = By.CSS_SELECTOR) -> Optional[Tuple[int, int]]:
		"""获取元素中心坐标"""
		try:
			element = self.driver.find_element(byType, selector)
			# 获取元素位置和大小
			location = element.location
			size = element.size
			
			# 计算中心坐标
			center_x = location['x'] + size['width'] // 2
			center_y = location['y'] + size['height'] // 2
			
			return (center_x, center_y)
		except NoSuchElementException:
			return None