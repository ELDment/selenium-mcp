from mcp.server.fastmcp import FastMCP
from Lib.manager import SeleniumManager
from Lib.controller import BrowserController
from Lib.reader import PageReader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import Optional, List, Dict, Any
import json
import os
import time

class SeleniumMCPConfig:
	def __init__(self):
		self.configPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
		self.LoadConfig()
	
	def LoadConfig(self):
		"""从配置文件加载配置"""
		try:
			if os.path.exists(self.configPath):
				with open(self.configPath, 'r', encoding='utf-8') as f:
					config = json.load(f)
					browserConfig = config.get('browser', {})
					self.chromedriverPath = browserConfig.get('chromedriverPath', r'D:\Chrome\chromedriver-win64\chromedriver.exe')
					self.chromeBinPath = browserConfig.get('chromeBinPath', r'D:\Chrome\chrome-win64\chrome.exe')
					self.debug = browserConfig.get('debug', False)
					self.headless = browserConfig.get('headless', False)
			else:
				self.chromedriverPath = r'D:\Chrome\chromedriver-win64\chromedriver.exe'
				self.chromeBinPath = r'D:\Chrome\chrome-win64\chrome.exe'
				self.debug = False
				self.headless = False
		except Exception as e:
			self.chromedriverPath = r'D:\Chrome\chromedriver-win64\chromedriver.exe'
			self.chromeBinPath = r'D:\Chrome\chrome-win64\chrome.exe'
			self.debug = False
			self.headless = False

class SeleniumMCPUtils:	
	@staticmethod
	def GetByType(byType: str) -> By:
		"""获取By类型映射"""
		byMap = {
			"css": By.CSS_SELECTOR,
			"id": By.ID,
			"xpath": By.XPATH,
			"class": By.CLASS_NAME,
			"tag": By.TAG_NAME
		}
		return byMap.get(byType, By.CSS_SELECTOR)
	
	@staticmethod
	def SanitizeFilename(filename: str) -> str:
		"""清理文件名中的非法字符"""
		invalidChars = "/\\|:*?\"<>"
		for char in invalidChars:
			filename = filename.replace(char, "_")
		return filename
	
	@staticmethod
	def EnsureTempDir() -> str:
		"""确保temp目录存在并返回路径"""
		tempDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
		if not os.path.exists(tempDir):
			os.makedirs(tempDir)
		return tempDir

class SeleniumMCPApp:	
	def __init__(self):
		self.config = SeleniumMCPConfig()
		self.manager = SeleniumManager(
			debug=self.config.debug,
			chromedriverPath=self.config.chromedriverPath,
			chromeBinPath=self.config.chromeBinPath,
			headless=self.config.headless
		)
		self.controller: Optional[BrowserController] = None
		self.reader: Optional[PageReader] = None
		self.mcp = FastMCP("selenium-mcp")
		self.__registerTools()
	
	def __ensureInstances(self):
		"""确保controller和reader实例存在"""
		if not self.manager.HasDriver():
			self.manager.GetOrCreateDriver()
		if self.controller is None:
			self.controller = BrowserController(self.manager.driver)
		if self.reader is None:
			self.reader = PageReader(self.manager.driver)
	
	def __registerTools(self):
		"""注册所有MCP工具"""
		self.__registerConnectionTools()
		self.__registerNavigationTools()
		self.__registerElementTools()
		self.__registerReaderTools()
		self.__registerUtilityTools()
	
	def __registerConnectionTools(self):
		"""注册连接和实例管理相关工具"""
		@self.mcp.tool()
		async def check_connection() -> str:
			"""查看MCP服务器是否已连接"""
			return "connected"
		
		@self.mcp.tool()
		async def get_selenium_instance() -> str:
			"""获取Selenium是否存在实例"""
			return "appeared" if self.manager.HasDriver() else "absent"
		
		@self.mcp.tool()
		async def create_browser_instance(headless: bool = False, debug: bool = False) -> str:
			"""创建新的浏览器实例"""
			try:
				if self.manager.HasDriver():
					self.manager.QuitDriver()
					self.controller = None
					self.reader = None
				
				self.manager.headless = headless
				self.manager.debug = debug
				
				driver = self.manager.GetOrCreateDriver()
				if driver:
					self.controller = BrowserController(driver)
					self.reader = PageReader(driver)
					return f"success: browser instance created (headless={headless}, debug={debug})"
				else:
					return "error: failed to create browser instance"
			except Exception as e:
				return f"error: {str(e)}"
		
		@self.mcp.tool()
		async def get_or_create_browser_instance(headless: bool = False, debug: bool = False) -> str:
			"""获取现有实例或创建新实例"""
			try:
				if self.manager.HasDriver():
					self.__ensureInstances()
					return "success: using existing browser instance"
				else:
					self.manager.headless = headless
					self.manager.debug = debug
					
					driver = self.manager.GetOrCreateDriver()
					if driver:
						self.controller = BrowserController(driver)
						self.reader = PageReader(driver)
						return f"success: new browser instance created (headless={headless}, debug={debug})"
					else:
						return "error: failed to create browser instance"
			except Exception as e:
				return f"error: {str(e)}"
		
		@self.mcp.tool()
		async def set_browser_config(chromedriver_path: str = "", chrome_bin_path: str = "") -> str:
			"""设置浏览器配置路径"""
			try:
				if chromedriver_path:
					self.manager.chromedriverPath = chromedriver_path
				if chrome_bin_path:
					self.manager.chromeBinPath = chrome_bin_path
				return f"success: browser config updated (chromedriver={chromedriver_path or 'unchanged'}, chrome_bin={chrome_bin_path or 'unchanged'})"
			except Exception as e:
				return f"error: {str(e)}"
		
		@self.mcp.tool()
		async def get_browser_config() -> str:
			"""获取当前浏览器配置"""
			try:
				config = {
					"chromedriver_path": self.manager.chromedriverPath,
					"chrome_bin_path": self.manager.chromeBinPath,
					"headless": self.manager.headless,
					"debug": self.manager.debug,
					"has_driver": self.manager.HasDriver()
				}
				return json.dumps(config, ensure_ascii=False)
			except Exception as e:
				return f"error: {str(e)}"
		
		@self.mcp.tool()
		async def quit_selenium_instance() -> str:
			"""关闭Selenium实例"""
			self.controller = None
			self.reader = None
			return "closed" if self.manager.QuitDriver() else "failed"

	def __registerNavigationTools(self):
		"""注册浏览器导航相关工具"""
		@self.mcp.tool()
		async def navigate_to_url(url: str) -> str:
			"""导航到指定URL"""
			self.__ensureInstances()
			try:
				self.manager.driver.get(url)
				return f"success: navigated to {url}"
			except Exception as e:
				return f"error: {str(e)}"
		
		@self.mcp.tool()
		async def go_back() -> str:
			"""浏览器后退"""
			self.__ensureInstances()
			try:
				self.manager.driver.back()
				return "success: navigated back"
			except Exception as e:
				return f"error: {str(e)}"
		
		@self.mcp.tool()
		async def go_forward() -> str:
			"""浏览器前进"""
			self.__ensureInstances()
			try:
				self.manager.driver.forward()
				return "success: navigated forward"
			except Exception as e:
				return f"error: {str(e)}"
		
		@self.mcp.tool()
		async def refresh_page() -> str:
			"""刷新页面"""
			self.__ensureInstances()
			try:
				self.manager.driver.refresh()
				return "success: page refreshed"
			except Exception as e:
				return f"error: {str(e)}"

	def __registerElementTools(self):
		"""注册元素操作相关工具"""
		@self.mcp.tool()
		async def click_element(selector: str, by_type: str = "css", timeout: int = 10) -> str:
			"""点击页面元素"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			success = self.controller.ClickElement(selector, byTypeObj, timeout)
			return "success: element clicked" if success else "error: failed to click element"
		
		@self.mcp.tool()
		async def click_coordinates(x: int, y: int) -> str:
			"""根据坐标点击页面"""
			self.__ensureInstances()
			success = self.controller.ClickElementByCoordinates(x, y)
			return "success: clicked coordinates" if success else "error: failed to click coordinates"
		
		@self.mcp.tool()
		async def send_keys_to_element(selector: str, text: str, by_type: str = "css", clear_first: bool = True) -> str:
			"""向元素输入文本"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			success = self.controller.SendKeys(selector, text, byTypeObj, clear_first)
			return "success: text sent" if success else "error: failed to send text"
		
		@self.mcp.tool()
		async def scroll_page(delta_y: int, element_selector: Optional[str] = None) -> str:
			"""滚动页面"""
			self.__ensureInstances()
			success = self.controller.ScrollWheel(delta_y, element_selector)
			return "success: page scrolled" if success else "error: failed to scroll"
		
		@self.mcp.tool()
		async def scroll_to_element(selector: str, by_type: str = "css") -> str:
			"""滚动到指定元素"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			success = self.controller.ScrollToElement(selector, byTypeObj)
			return "success: scrolled to element" if success else "error: failed to scroll to element"
		
		@self.mcp.tool()
		async def hover_element(selector: str, by_type: str = "css") -> str:
			"""悬停在元素上"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			success = self.controller.HoverElement(selector, byTypeObj)
			return "success: element hovered" if success else "error: failed to hover element"
		
		@self.mcp.tool()
		async def drag_and_drop(source_selector: str, target_selector: str, by_type: str = "css") -> str:
			"""拖拽元素"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			success = self.controller.DragAndDrop(source_selector, target_selector, byTypeObj)
			return "success: drag and drop completed" if success else "error: failed to drag and drop"

	def __registerReaderTools(self):
		"""注册页面读取相关工具"""
		@self.mcp.tool()
		async def get_page_title() -> str:
			"""获取页面标题"""
			self.__ensureInstances()
			return self.reader.GetPageTitle()
		
		@self.mcp.tool()
		async def get_page_url() -> str:
			"""获取当前页面URL"""
			self.__ensureInstances()
			return self.reader.GetPageUrl()
		
		@self.mcp.tool()
		async def get_element_text(selector: str, by_type: str = "css") -> str:
			"""获取元素文本"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			text = self.reader.GetElementText(selector, byTypeObj)
			return text if text is not None else "error: element not found"
		
		@self.mcp.tool()
		async def get_elements_text(selector: str, by_type: str = "css") -> str:
			"""获取多个元素的文本"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			texts = self.reader.GetElementsText(selector, byTypeObj)
			return json.dumps(texts, ensure_ascii=False)
		
		@self.mcp.tool()
		async def get_element_attribute(selector: str, attribute: str, by_type: str = "css") -> str:
			"""获取元素属性值"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			attrValue = self.reader.GetElementAttribute(selector, attribute, byTypeObj)
			return attrValue if attrValue is not None else "error: element or attribute not found"
		
		@self.mcp.tool()
		async def get_all_links() -> str:
			"""获取页面所有链接"""
			self.__ensureInstances()
			links = self.reader.GetAllLinks()
			return json.dumps(links, ensure_ascii=False)
		
		@self.mcp.tool()
		async def get_all_images() -> str:
			"""获取页面所有图片"""
			self.__ensureInstances()
			images = self.reader.GetAllImages()
			return json.dumps(images, ensure_ascii=False)
		
		@self.mcp.tool()
		async def get_table_data(selector: str, by_type: str = "css") -> str:
			"""获取表格数据"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			tableData = self.reader.GetTableData(selector, byTypeObj)
			return json.dumps(tableData, ensure_ascii=False)
		
		@self.mcp.tool()
		async def get_form_data(selector: str, by_type: str = "css") -> str:
			"""获取表单数据"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			formData = self.reader.GetFormData(selector, byTypeObj)
			return json.dumps(formData, ensure_ascii=False)
		
		@self.mcp.tool()
		async def get_page_text(remove_empty: bool = True) -> str:
			"""获取页面所有文本"""
			self.__ensureInstances()
			return self.reader.GetPageText(remove_empty)
		
		@self.mcp.tool()
		async def search_text_in_page(search_text: str, case_sensitive: bool = False) -> str:
			"""在页面中搜索文本"""
			self.__ensureInstances()
			results = self.reader.SearchTextInPage(search_text, case_sensitive)
			return json.dumps(results, ensure_ascii=False)
		
		@self.mcp.tool()
		async def get_page_info() -> str:
			"""获取页面完整信息"""
			self.__ensureInstances()
			pageInfo = self.reader.GetPageInfo()
			return json.dumps(pageInfo, ensure_ascii=False)

	def __registerUtilityTools(self):
		"""注册实用工具"""
		@self.mcp.tool()
		async def get_page_source() -> str:
			"""获取页面HTML源代码，并将源码保存到temp目录，返回文件绝对路径"""
			self.__ensureInstances()
			source = self.reader.GetPageSource()
			title = self.reader.GetPageTitle() or "page"
			timestamp = int(time.time())
			filename = f"{title}_{timestamp}.html"
			filename = SeleniumMCPUtils.SanitizeFilename(filename)
			tempDir = SeleniumMCPUtils.EnsureTempDir()
			filePath = os.path.join(tempDir, filename)
			with open(filePath, "w", encoding="utf-8") as f:
				f.write(source)
			return filePath
		
		@self.mcp.tool()
		async def get_rendered_html() -> str:
			"""获取渲染后的页面HTML（包含JavaScript动态生成的内容），并将HTML保存到temp目录，返回文件绝对路径"""
			self.__ensureInstances()
			renderedHtml = self.manager.driver.execute_script("return document.documentElement.outerHTML;")
			title = self.reader.GetPageTitle() or "rendered_page"
			timestamp = int(time.time())
			filename = f"{title}_rendered_{timestamp}.html"
			filename = SeleniumMCPUtils.SanitizeFilename(filename)
			tempDir = SeleniumMCPUtils.EnsureTempDir()
			filePath = os.path.join(tempDir, filename)
			with open(filePath, "w", encoding="utf-8") as f:
				f.write(renderedHtml)
			return filePath
		
		@self.mcp.tool()
		async def wait_for_element(selector: str, by_type: str = "css", timeout: int = 10) -> str:
			"""等待元素出现"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			success = self.controller.WaitForElement(selector, byTypeObj, timeout)
			return "success: element appeared" if success else "error: element did not appear"
		
		@self.mcp.tool()
		async def is_element_visible(selector: str, by_type: str = "css") -> str:
			"""检查元素是否可见"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			visible = self.reader.IsElementVisible(selector, byTypeObj)
			return "visible" if visible else "hidden"
		
		@self.mcp.tool()
		async def get_element_center(selector: str, by_type: str = "css") -> str:
			"""获取元素中心坐标"""
			self.__ensureInstances()
			byTypeObj = SeleniumMCPUtils.GetByType(by_type)
			center = self.reader.GetElementCenter(selector, byTypeObj)
			if center:
				return json.dumps({"x": center[0], "y": center[1]}, ensure_ascii=False)
			else:
				return "error: element not found"
	
	def Run(self):
		"""运行MCP服务器"""
		self.mcp.run(transport="stdio")

if __name__ == "__main__":
	SeleniumMCPApp().Run()