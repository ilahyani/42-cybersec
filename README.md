# Cybersecurity Tools Collection

## Arachnida
Contains two tools for web scraping and image analysis:
- **Spider**: A web crawler that recursively downloads images from websites. It supports common image formats (.jpg, .jpeg, .png, .gif, .bmp) and allows configuring max depth and download path.
- **Scorpion**: An image metadata analyzer that extracts and displays EXIF data and other metadata from image files.

## Inquisitor
An ARP spoofing tool implemented as a Docker-based environment with 3 containers:
- FTP Server (vsftpd)
- FTP Client
- Attacker running a Python script that performs ARP poisoning to intercept FTP traffic between server and client, monitoring file uploads/downloads.

## OTP
A command-line one-time password (OTP) generator implementing TOTP (Time-based One-Time Password) algorithm. Features include:
- Key generation and encryption 
- Counter-based OTP generation
- Secure key storage using Fernet encryption

## Onion
A Dockerized Tor hidden service setup containing:
- Nginx web server hosting a simple webpage
- SSH server on port 4242
- Tor configuration for creating a .onion service
- Scripts for automated deployment and .onion address retrieval

## Reverse
A collection of reverse engineering challenges with increasing difficulty:
- Level 1: Basic string comparison
- Level 2: Number encoding puzzle
- Level 3: Complex string manipulation and control flow

## Stockholm 
A WannaCry ransomware simulator that:
- Encrypts files with specific extensions in a target directory
- Adds .ft extension to encrypted files
- Provides decryption capability with correct key
- Supports silent mode and version checking