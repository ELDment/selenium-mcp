from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import socket
import os
import psutil
from typing import Optional

class SeleniumManager:
	def __init__(self, debuggerAddress: str = '127.0.0.1:9222', debug: bool = True, chromedriverPath: Optional[str] = None, chromeBinPath: Optional[str] = None, headless: bool = False):
		self.debuggerAddress = debuggerAddress
		self.driver = None
		self.debug = debug
		self.chromedriverPath = chromedriverPath
		self.chromeBinPath = chromeBinPath
		self.headless = headless

	def __isPortInUse(self, host: str, port: int) -> bool:
		"""检测端口是否被占用"""
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			try:
				s.bind((host, port))
				return False
			except socket.error as e:
				if e.errno == 10048:
					return True
				raise

	def __getRunningSeleniumPids(self) -> list:
		"""获取所有运行中的ChromeDriver进程ID"""
		return [
			p.info['pid'] for p in psutil.process_iter(['pid', 'name'])
			if 'chromedriver' in p.info['name'].lower()
		]

	def __getActiveDriver(self, pid: int) -> Optional[webdriver.Chrome]:
		"""尝试连接指定PID的WebDriver实例"""
		try:
			service = Service(executable_path=f'http://localhost:{pid}')
			return webdriver.Chrome(service=service)
		except Exception:
			return None

	def GetOrCreateDriver(self) -> Optional[webdriver.Chrome]:
		"""获取或创建Selenium实例"""
		for pid in self.__getRunningSeleniumPids():
			driver = self.__getActiveDriver(pid)
			if driver:
				if self.debug:
					print(f'复用现有实例 PID={pid}')
				self.driver = driver
				return self.driver
		host, portStr = self.debuggerAddress.split(':')
		port = int(portStr)
		if self.__isPortInUse(host, port):
			if self.debug:
				print(f"检测到端口 {port} 正在使用，尝试连接到现有Selenium实例...")
			options = Options()
			options.add_experimental_option("debuggerAddress", self.debuggerAddress)
			try:
				self.driver = webdriver.Chrome(options=options)
				if self.debug:
					print("成功连接到现有Selenium实例。")
				return self.driver
			except WebDriverException as e:
				if self.debug:
					print(f"连接到现有实例失败: {e}")
					print("尝试创建一个新的Selenium实例...")
				return self.CreateNewDriver()
		else:
			if self.debug:
				print(f"端口 {port} 未被使用，创建一个新的Selenium实例...")
			return self.CreateNewDriver()

	def CreateNewDriver(self) -> Optional[webdriver.Chrome]:
		"""创建新的Selenium实例"""
		options = Options()
		options.add_argument('--disable-blink-features=AutomationControlled')
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option('useAutomationExtension', False)
		options.add_argument('--disable-extensions')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		if self.headless:
			options.add_argument('--headless')
			options.add_argument('--disable-gpu')
		if self.chromeBinPath and os.path.exists(self.chromeBinPath):
			options.binary_location = self.chromeBinPath
		else:
			if self.debug:
				print("警告: Chrome.exe文件路径无效或未提供")
		service = None
		if self.chromedriverPath and os.path.exists(self.chromedriverPath):
			service = Service(executable_path=self.chromedriverPath)
		else:
			if self.debug:
				print("警告: Chromedriver.exe路径无效或未提供")
		try:
			if service:
				self.driver = webdriver.Chrome(service=service, options=options)
			else:
				self.driver = webdriver.Chrome(options=options)
			if self.debug:
				print("成功创建新的Selenium实例。")
			return self.driver
		except WebDriverException as e:
			if self.debug:
				print(f"创建新的Selenium实例失败: {e}")
			self.driver = None
			return None

	def QuitDriver(self) -> bool:
		"""关闭Selenium实例"""
		if self.driver:
			try:
				self.driver.quit()
				self.driver = None
				if self.debug:
					print("Selenium实例已关闭。")
				return True
			except Exception as e:
				if self.debug:
					print(f"关闭Selenium实例失败: {e}")
				return False
		if self.debug:
			print("没有正在运行的Selenium实例。")
		return False

	def HasDriver(self) -> bool:
		"""判断是否有Selenium实例"""
		return self.driver is not None