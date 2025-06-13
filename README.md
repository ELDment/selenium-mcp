# 🌐 Selenium MCP 服务器

🇨🇳 中文 | [🇺🇸 English](README_EN.md)

一个基于 Model Context Protocol (MCP) 的 Selenium 自动化服务器，提供强大的网页自动化功能。

### 🎯 核心功能
- 🌐 **浏览器控制** - 完整的浏览器实例管理和导航控制
- 🖱️ **元素交互** - 点击、输入、悬停、拖拽等页面交互
- 📖 **页面读取** - 获取页面标题、文本、链接、图片等信息
- 🔍 **元素查找** - 支持多种选择器的元素定位和等待

## 🚀 快速开始

### 📋 运行要求
- Python 3.10+
- Chrome/Chromium 浏览器
- ChromeDriver

### 🔧 安装配置

1. **克隆项目**
   ```bash
   git clone https://github.com/ELDment/selenium-mcp.git
   cd selenium-mcp
   ```

2. **运行设置脚本**
   ```bash
   python setup.py
   ```
   
   设置脚本将自动：
   - 🔍 检测并安装依赖包
   - 🔎 自动查找 Chrome 和 ChromeDriver 路径
   - ⚙️ 生成配置文件
   - 📄 创建 MCP 服务器配置

3. **启动服务器**
   ```bash
   python selenium-mcp.py
   ```

   **或填入 MCP 服务器 配置到AI协助工具，由工具自行启动**

## 📁 项目结构

```
selenium-mcp/
├── 📄 selenium-mcp.py      # 主服务器文件
├── 📁 Lib/                 # 核心库文件
│   ├── 🎮 controller.py    # 浏览器控制器
│   ├── 📊 manager.py       # 实例管理器
│   └── 📖 reader.py        # 页面读取器
|
├── 🔧 setup.py            # 安装配置脚本
├── 📋 requirements.txt    # 依赖列表
└── 📖 README.md           # 项目说明
```

## ⚙️ 配置说明

### 🔧 config.json
配置文件，包含以下选项：

```json
{
   "chromedriverPath": "path/to/chromedriver",  // ChromeDriver路径
   "chromeBinPath": "path/to/chrome",           // Chrome浏览器路径
   "debug": false,                              // 调试模式
   "headless": false                            // 无头模式
}
```

### 🔗 mcp-config.json
MCP 服务器配置文件，可直接复制到AI协助工具中。

## 🎯 MCP 协议接口

### 🌐 浏览器管理
- ✅ 创建/获取浏览器实例（`create_browser_instance`, `get_or_create_browser_instance`）
- ⚙️ 配置浏览器选项（`set_browser_config`, `get_browser_config`）
- 🔄 实例状态检查（`check_connection`, `get_selenium_instance`）
- ❌ 关闭浏览器实例（`quit_selenium_instance`）

### 🧭 页面导航
- 🔗 导航到指定URL（`navigate_to_url`）
- ⬅️ 后退/前进（`go_back`, `go_forward`）
- 🔄 刷新页面（`refresh_page`）

### 🖱️ 元素交互
- 👆 点击元素/坐标（`click_element`, `click_coordinates`）
- ⌨️ 输入文本（`send_keys_to_element`）
- 📜 页面滚动（`scroll_page`, `scroll_to_element`）
- 🎯 悬停操作（`hover_element`）
- 🔄 拖拽操作（`drag_and_drop`）

### 📖 信息获取
- 📄 页面标题和URL（`get_page_title`, `get_page_url`）
- 📝 元素文本和属性（`get_element_text`, `get_elements_text`, `get_element_attribute`）
- 🔗 所有链接（`get_all_links`）
- 🖼️ 所有图片（`get_all_images`）
- 📊 表格数据（`get_table_data`）
- 📋 表单数据（`get_form_data`）
- 📝 页面文本（`get_page_text`）
- 📄 页面信息（`get_page_info`）
- 💾 页面源码（`get_page_source`, `get_rendered_html`）

### 🔍 元素查找
- ⏳ 等待元素出现（`wait_for_element`）
- 👁️ 检查元素可见性（`is_element_visible`）
- 📍 获取元素坐标（`get_element_center`）
- 🔍 文本搜索（`search_text_in_page`）

## 🛠️ 开发说明

### 📦 依赖包
- `selenium` - Web自动化框架
- `mcp` - Model Context Protocol
- `psutil` - 系统进程管理

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 📋 TODO List

| 功能 | 状态 | 优先级 | 描述 |
|------|------|--------|------|
| 🤖 AI屏幕理解功能 | ⏳ 计划中 | 🔥 高 | 实现AI理解屏幕内容（而不仅仅依靠DOM结构）<br/>• 集成计算机视觉技术<br/>• 支持截图分析和元素识别<br/>• 提供基于视觉的元素定位能力 |

## 📄 许可证

采用 MIT 许可证

## 🆘 支持

如果您遇到问题或有任何建议，请：
- 📝 提交 Issue