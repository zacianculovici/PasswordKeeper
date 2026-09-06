# PasswordKeeper

## 📋 Overview
PasswordKeeper is a fully functional python application that uses `customtkinter`, `CTkMaker` and cryptography to store your passwords easily and securely. 

## 🛠️ Features
* Completely secure hashing and encryption method means that it is inmpossible to decrypt your passwords without the correct password. This means that even if someone gets access to your password file, all they will se is a bunch of gibberish. (Such as: )
* Intuitive and easy to use interface.
* Cross-platform compatibility.
* Multiple user capabilities, making it easy to share a single installation with multiple users.
* Easy password search, editing and deletion.

## ⏱️ Quick Start Guide
1. Download the latest release for your system from the [Downloads](#downloads) section below or [run it manually](#running-the-application-from-source) from source.
2. Install the application.
3. Run the application and create a new user account.
4. Start adding your passwords and categories and enjoy the security and convenience of PasswordKeeper!

### [Downloads](https://github.com/zacianculovici/PasswordKeeper/releases)
Download PasswordKeeper for your system:

[![Windows Download](https://img.shields.io/badge/Download-Windows_Setup-blue?logo=windows)](https://github.com/zacianculovici/PasswordKeeper/releases/latest/download/PasswordKeeper-1.0.1-Windows-Setup.exe)

[![macOS Download](https://img.shields.io/badge/Download-macOS_DMG-lightgrey?logo=apple)](https://github.com/zacianculovici/PasswordKeeper/releases/latest/download/PasswordKeeper-1.0.1-macOS-x86_64.dmg)

[![Linux Download](https://img.shields.io/badge/Download-Linux_Tarball-orange?logo=linux)](https://github.com/zacianculovici/PasswordKeeper/releases/latest/download/PasswordKeeper-1.0.1-Linux-x86_64.tar.gz)

### Running the application from source
To build the application manually from source, follow these steps:
1. Clone the repository:
```bash
git clone https://github.com/zacianculovici/PasswordKeeper.git
```
2. Navigate to the project directory:
```bash
cd PasswordKeeper
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
python src/MainPage.py
```
5. Optionally, you can build the application into a standalone executable using PyInstaller:
```bash
pyinstaller --noconfirm --clean --onedir --windowed "src\MainPage.py" --name PasswordKeeper --paths "src" --collect-all helperFiles --hidden-import=helperFiles.loadingPleaseWait --add-data "src/assets;assets" --collect-data customtkinter
```

## ✨ AI Usage
AI has been used in parts of this project for:
* Minor bug fixes - Github Copilot
* Small code generation - Github Copilot
* Minor error explanation and fixes - Github Copilot
* Code completions - Github Copilot (The fact that Github Copilot is giving me suggestions as I type right now "is a huge help, and I am very grateful for it!") (Text in "" is a quote from Github Copilot 🤣🤣🤣) 
* Github Copilot - build_installlers.yml loads of help with making it work!

## ✔️ Other declarations
* `CTkMaker` was used for most of the core UI creation, as well as the very nice-looking [src/helperFiles/toast.py](https://github.com/zacianculovici/PasswordKeeper/blob/main/src/helperFiles/toast.py) and [src/helperFiles/scrollable_dropdown.py](https://github.com/zacianculovici/PasswordKeeper/blob/main/src/helperFiles/scrollable_dropdown.py).
* Some help from Google Gemini and AI Overview with small explanation and simple tests such as [src/getWorkingAreaDimensions.py](https://github.com/zacianculovici/PasswordKeeper/blob/main/src/getWorkingAreaDimensions.py), [src/tooltiptest.py](https://github.com/zacianculovici/PasswordKeeper/blob/main/src/tooltiptest.py) and [src/tooltiptest2.py](https://github.com/zacianculovici/PasswordKeeper/blob/main/src/tooltiptest2.py).

## 📅 Coming soon!
Features I would like to add in the future include:
* Cloud storage, so that you can access your passwords from anywhere.
* Password strength checker, so that you can see how strong your passwords are.
* Password generator, so that you can generate strong passwords easily.
* OAuth login, so that you can log in with your Google, Facebook, or other accounts.
