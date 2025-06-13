# 🌐 Selenium MCP Server

[🇨🇳 中文版](README.md) | 🇺🇸 English

A Selenium automation server based on Model Context Protocol (MCP), providing powerful web automation capabilities.

### 🎯 Core Features
- 🌐 **Browser Control** - Complete browser instance management and navigation control
- 🖱️ **Element Interaction** - Click, input, hover, drag and other page interactions
- 📖 **Page Reading** - Get page title, text, links, images and other information
- 🔍 **Element Finding** - Element location and waiting with multiple selector support

## 🚀 Quick Start

### 📋 Requirements
- Python 3.10+
- Chrome/Chromium Browser
- ChromeDriver

### 🔧 Installation & Configuration

1. **Clone Project**
   ```bash
   git clone https://github.com/ELDment/selenium-mcp.git
   cd selenium-mcp
   ```

2. **Run Setup Script**
   ```bash
   python setup.py
   ```
   
   The setup script will automatically:
   - 🔍 Detect and install dependencies
   - 🔎 Auto-find Chrome and ChromeDriver paths
   - ⚙️ Generate configuration files
   - 📄 Create MCP server configuration

3. **Start Server**
   ```bash
   python selenium-mcp.py
   ```

   **Or add MCP server configuration to AI assistant tools and let them start automatically**

## 📁 Project Structure

```
selenium-mcp/
├── 📄 selenium-mcp.py      # Main server file
├── 📁 Lib/                 # Core library files
│   ├── 🎮 controller.py    # Browser controller
│   ├── 📊 manager.py       # Instance manager
│   └── 📖 reader.py        # Page reader
|
├── 🔧 setup.py            # Installation setup script
├── 📋 requirements.txt    # Dependencies list
└── 📖 README.md           # Project documentation
```

## ⚙️ Configuration

### 🔧 config.json
Configuration file with the following options:

```json
{
   "chromedriverPath": "path/to/chromedriver",  // ChromeDriver path
   "chromeBinPath": "path/to/chrome",           // Chrome browser path
   "debug": false,                              // Debug mode
   "headless": false                            // Headless mode
}
```

### 🔗 mcp-config.json
MCP server configuration file, can be directly copied to AI assistant tools.

## 🎯 MCP Protocol Interface

### 🌐 Browser Management
- ✅ Create/get browser instance (`create_browser_instance`, `get_or_create_browser_instance`)
- ⚙️ Configure browser options (`set_browser_config`, `get_browser_config`)
- 🔄 Instance status check (`check_connection`, `get_selenium_instance`)
- ❌ Close browser instance (`quit_selenium_instance`)

### 🧭 Page Navigation
- 🔗 Navigate to specified URL (`navigate_to_url`)
- ⬅️ Back/forward (`go_back`, `go_forward`)
- 🔄 Refresh page (`refresh_page`)

### 🖱️ Element Interaction
- 👆 Click element/coordinates (`click_element`, `click_coordinates`)
- ⌨️ Input text (`send_keys_to_element`)
- 📜 Page scrolling (`scroll_page`, `scroll_to_element`)
- 🎯 Hover operations (`hover_element`)
- 🔄 Drag operations (`drag_and_drop`)

### 📖 Information Retrieval
- 📄 Page title and URL (`get_page_title`, `get_page_url`)
- 📝 Element text and attributes (`get_element_text`, `get_elements_text`, `get_element_attribute`)
- 🔗 All links (`get_all_links`)
- 🖼️ All images (`get_all_images`)
- 📊 Table data (`get_table_data`)
- 📋 Form data (`get_form_data`)
- 📝 Page text (`get_page_text`)
- 📄 Page information (`get_page_info`)
- 💾 Page source (`get_page_source`, `get_rendered_html`)

### 🔍 Element Finding
- ⏳ Wait for element appearance (`wait_for_element`)
- 👁️ Check element visibility (`is_element_visible`)
- 📍 Get element coordinates (`get_element_center`)
- 🔍 Text search (`search_text_in_page`)

## 🛠️ Development

### 📦 Dependencies
- `selenium` - Web automation framework
- `mcp` - Model Context Protocol
- `psutil` - System process management

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

### 📋 TODO List

| Function | Status | Priority | Description |
|----------|--------|----------|-------------|
| 🤖 AI Screen Understanding | ⏳ Planned | 🔥 High | Implement AI understanding of screen content (not just DOM structure)<br/>• Integrate computer vision technology<br/>• Support screenshot analysis and element recognition<br/>• Provide vision-based element location capabilities |

## 📄 License

MIT License

## 🆘 Support

If you encounter problems or have any suggestions, please:
- 📝 Submit Issues