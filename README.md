# 🌐 UM-NMS (Network Management System)  

Welcome to the **NMS (Network Management System)**! This project provides tools for managing and monitoring networks with multiple configuration options. Below is a complete guide to get started. 🚀

---

## 📜 Features  
- **Cross-Platform**: Works on Linux 🐧, macOS 🍎, and Windows 🖥️.  
- **Dynamic Configuration**: Easily specify custom IPs, ports, and configuration files.  
- **Flexible Modes**:
  - **Server Mode** 🖧
  - **Client Mode** 👨‍💻
  - Development & Production environments.  
- **Live Documentation**:
  - Compile and watch reports in real time 📄.  

---

## 🛠️ Requirements  
- **Python 3.x** 🐍  
- **Make Utility** 🛠️  
- **Typst** (for compiling reports) ✍️  

---

## 🔧 Setup
Make sure you have Make, Python and Typst installed.  

## 🚀 Usage
### Run the Server 🌟  
Start the server with default settings:  

```bash
make server
```  

You can customize the server settings by overriding environment variables:  

```bash
make server IP=127.0.0.1 PORT=9090
```  

Or specify a custom configuration file:  

```bash
make server CONFIG=data/configure-copy.json
```  

### Run the Client 🌐  
Run the client with default or custom settings:  

```bash
make client  
# or:  
make client IP=192.168.1.100 PORT=8888  
```  

### Development Mode 🛠️  
For testing and debugging, you can start the server or client in development mode:  

```bash
make dev-server  
make dev-client  
```  

### Compile Reports 📄  
Generate documentation or reports using **Typst**:  

```bash
make relatorio  
```  

Watch for changes and auto-update the report:  

```bash
make relatorio_watch  
```  

Clean up generated files:  

```bash
make relatorio_clean  
```

---

## 📂 Project Structure

```
├── data/                # Configuration and data files
├── relatorio/           # Reports and documentation   
├── main.py              # Entry point of the application
├── Makefile             # Automates build and run tasks 
└── README.md            # Project documentation
```  

---

## 💡 Tips

-   Customize the `IP` and `PORT` variables for different network setups.
-   Use the `CONFIG` variable to load specific settings for the server.
-   Run `make relatorio_watch` during editing for real-time updates.
