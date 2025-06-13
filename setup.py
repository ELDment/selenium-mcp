import json
import os
import subprocess
import sys
from pathlib import Path
import glob

class SeleniumMCPSetup:
	def __init__(self):
		self.projectRoot = Path(__file__).parent.absolute()
		self.configPath = self.projectRoot / "config.json"
		self.seleniumMcpPath = self.projectRoot / "selenium-mcp.py"
		self.requirementsPath = self.projectRoot / "requirements.txt"
	
	def installDependencies(self):
		if not self.requirementsPath.exists():
			print("requirements.txt文件不存在，跳过依赖安装")
			return
		
		print("正在安装依赖包...")
		try:
			subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(self.requirementsPath)])
			print("依赖安装完成！")
		except subprocess.CalledProcessError as e:
			print(f"依赖安装失败: {e}")
			print("请手动运行: pip install -r requirements.txt")
	
	def findChromeExecutable(self):
		possiblePaths = [
			"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
			"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
			"D:\\Chrome\\chrome-win64\\chrome.exe",
			"C:\\Users\\*\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
		]
		
		for path in possiblePaths:
			if "*" in path:
				# 处理通配符路径
				matches = glob.glob(path)
				if matches:
					return matches[0]
			elif os.path.exists(path):
				return path
		
		return None
	
	def findChromeDriverExecutable(self):
		possiblePaths = [
			"D:\\Chrome\\chromedriver-win64\\chromedriver.exe",
			"C:\\chromedriver\\chromedriver.exe",
			"C:\\Program Files\\chromedriver\\chromedriver.exe",
			"C:\\Users\\*\\Downloads\\chromedriver*.exe"
		]
		
		for path in possiblePaths:
			if "*" in path:
				# 处理通配符路径
				matches = glob.glob(path)
				if matches:
					return matches[0]
			elif os.path.exists(path):
				return path
		
		return None
	
	def getUserInput(self, prompt, defaultValue=""):
		if defaultValue:
			userInput = input(f"{prompt} (默认: {defaultValue}): ").strip()
			return userInput if userInput else defaultValue
		else:
			return input(f"{prompt}: ").strip()
	
	def getYesNoInput(self, prompt, defaultValue=False):
		defaultStr = "y" if defaultValue else "n"
		while True:
			userInput = input(f"{prompt} (y/n, 默认: {defaultStr}): ").strip().lower()
			if not userInput:
				return defaultValue
			if userInput in ['y', 'yes', '是']:
				return True
			elif userInput in ['n', 'no', '否']:
				return False
			else:
				print("请输入 y/n")
		
	def generateInteractiveConfig(self):
		print("\n=== 交互式配置 ===")
		
		chromePath = self.findChromeExecutable()
		if chromePath:
			print(f"找到Chrome浏览器: {chromePath}")
			useFoundChrome = self.getYesNoInput("是否使用找到的Chrome浏览器", True)
			if not useFoundChrome:
				chromePath = self.getUserInput("请输入Chrome浏览器路径")
		else:
			print("未找到Chrome浏览器")
			chromePath = self.getUserInput("请输入Chrome浏览器路径", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
		
		chromeDriverPath = self.findChromeDriverExecutable()
		if chromeDriverPath:
			print(f"找到ChromeDriver: {chromeDriverPath}")
			useFoundDriver = self.getYesNoInput("是否使用找到的ChromeDriver", True)
			if not useFoundDriver:
				chromeDriverPath = self.getUserInput("请输入ChromeDriver路径")
		else:
			print("未找到ChromeDriver")
			chromeDriverPath = self.getUserInput("请输入ChromeDriver路径", "D:\\Chrome\\chromedriver-win64\\chromedriver.exe")
		
		debugMode = self.getYesNoInput("是否启用调试模式", False)
		headlessMode = self.getYesNoInput("是否启用无头模式", False)
		
		config = {
			"browser": {
				"chromedriverPath": chromeDriverPath,
				"chromeBinPath": chromePath,
				"debug": debugMode,
				"headless": headlessMode
			}
		}
		
		with open(self.configPath, 'w', encoding='utf-8') as f:
			json.dump(config, f, indent=2, ensure_ascii=False)
		
		print(f"\n配置文件已生成: {self.configPath}")
		return config
	
	def generateDefaultConfig(self):
		defaultConfig = {
			"browser": {
				"chromedriverPath": "D:\\Chrome\\chromedriver-win64\\chromedriver.exe",
				"chromeBinPath": "D:\\Chrome\\chrome-win64\\chrome.exe",
				"debug": False,
				"headless": False
			}
		}
		
		with open(self.configPath, 'w', encoding='utf-8') as f:
			json.dump(defaultConfig, f, indent=2, ensure_ascii=False)
		
		print(f"配置文件已生成: {self.configPath}")
		return defaultConfig
	
	def loadConfig(self):
		if not self.configPath.exists():
			print("配置文件不存在，正在生成默认配置...")
			return self.generateDefaultConfig()
		
		try:
			with open(self.configPath, 'r', encoding='utf-8') as f:
				config = json.load(f)
			print(f"配置文件加载成功: {self.configPath}")
			return config
		except Exception as e:
			print(f"配置文件加载失败: {e}")
			print("正在生成默认配置...")
			return self.generateDefaultConfig()
	
	def generateMcpServerConfig(self):
		mcpConfig = {
			"mcpServers": {
				"selenium-mcp": {
					"command": "python",
					"args": [
						str(self.seleniumMcpPath)
					]
				}
			}
		}
		
		jsonString = json.dumps(mcpConfig, indent=2, ensure_ascii=False)
		return jsonString
	
	def saveMcpConfig(self, filename="mcp-config.json"):
		configString = self.generateMcpServerConfig()
		outputPath = self.projectRoot / filename
		
		with open(outputPath, 'w', encoding='utf-8') as f:
			f.write(configString)
		
		print(f"MCP配置文件已保存: {outputPath}")
		return outputPath
	
	def printMcpConfig(self):
		configString = self.generateMcpServerConfig()
		print("\n=== MCP服务器配置 ===")
		print(configString)
		print("=== 配置结束 ===\n")
		return configString
	
	def updateSeleniumMcpConfig(self):
		config = self.loadConfig()
		browserConfig = config.get('browser', {})
		
		print("\n=== 当前配置信息 ===")
		print(f"ChromeDriver路径: {browserConfig.get('chromedriverPath')}")
		print(f"Chrome浏览器路径: {browserConfig.get('chromeBinPath')}")
		print(f"调试模式: {browserConfig.get('debug')}")
		print(f"无头模式: {browserConfig.get('headless')}")
		print("=== 配置信息结束 ===\n")
		
		return browserConfig
	
	def setup(self):
		print("开始Selenium MCP设置...\n")
		
		self.installDependencies()
		
		configExists = self.configPath.exists()
		if configExists:
			useExistingConfig = self.getYesNoInput(f"配置文件已存在({self.configPath})，是否使用现有配置？", True)
			if not useExistingConfig:
				self.generateInteractiveConfig()
		else:
			useInteractive = self.getYesNoInput("配置文件不存在，是否开始配置？", True)
			if useInteractive:
				self.generateInteractiveConfig()
			else:
				self.generateDefaultConfig()
		
		self.updateSeleniumMcpConfig()
		self.printMcpConfig()
		self.saveMcpConfig()
		
		print("设置完成！")

if __name__ == "__main__":
	SeleniumMCPSetup().setup()