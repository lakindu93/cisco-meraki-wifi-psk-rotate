# Automating Cisco Meraki WiFi PSK Rotation Using the Meraki Dashboard API

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Cisco Meraki](https://img.shields.io/badge/Cisco-Meraki-1BA0D7?logo=cisco&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux-orange?logo=linux&logoColor=white)
![Systemd](https://img.shields.io/badge/systemd-Timer-blue)

Automatically rotate the **Pre-Shared Key (PSK)** of a Cisco Meraki WiFi SSID using **Python** and the **Meraki Dashboard API**.

This project generates a secure random WiFi password, updates the configured SSID through the Meraki Dashboard API, and emails the new password to the configured recipients using **AWS SES (SMTP)**. It is designed to run as a **systemd oneshot service** triggered by a **systemd timer**, making it lightweight, reliable, and suitable for unattended production environments.

---

## Features

- 🔐 Generate a cryptographically secure WiFi PSK
- 📡 Update Cisco Meraki SSID passwords using the Meraki Dashboard API
- 📧 Email the new password using AWS SES (SMTP)
- ⏰ Schedule automatic password rotation with systemd timers
- 📝 Production-ready logging
- 🚀 Lightweight and easy to deploy

---

## Documentation

A complete step-by-step guide is available on **SysOps Technix**, including:

- Installation
- Configuration
- Prerequisites
- Meraki Dashboard API setup
- AWS SES configuration
- Finding the SSID number
- systemd service and timer setup
- Usage examples
- Troubleshooting
- Security best practices

📖 **Read the full guide here:**

### https://sysopstechnix.com/automating-cisco-meraki-wifi-psk-rotation/
