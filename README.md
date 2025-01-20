# Welcome Home Bot - Smart Door Camera Notification System

## Overview
The **Welcome Home Bot** is a real-time door monitoring system engineered using a **Raspberry Pi** and **Python**. This system offers instant notifications with 99.9% uptime and utilizes **facial recognition** for efficient visitor detection. The project also includes secure user authentication, real-time notifications, and a lightweight web interface for system control.

## Features
- **Facial Recognition**: 
  - Integrated **OpenCV** and the **face_recognition** library for detecting visitors with less than **95ms latency**.
  
- **Secure Authentication & Notifications**:
  - Implemented **Firebase Cloud Messaging** for reliable, real-time notifications and user authentication.
  
- **Web Interface**:
  - Developed a simple web interface using **Vanilla JavaScript** and **WebSocket** for real-time video streaming and control.

- **Low-light Optimization**:
  - Optimized image processing with the **Raspberry Pi Camera Module 3** for reliable monitoring in low-light conditions, ensuring 24/7 operation.

- **Cost-Effective Solution**:
  - Designed the entire system for under **$200**, showcasing efficient hardware selection and budget management.

## Technologies Used
- **Python**
- **OpenCV**
- **Firebase**
- **WebSocket**
- **JavaScript**
- **Raspberry Pi**
- **Face Recognition**

## Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jaysaavedra18/welcome-home-bot.git
   cd welcome-home-bot
   ```

2. **Install dependencies**:

   - Install Python libraries:

     ```bash
     pip install -r requirements.txt
     ```

   - Install JavaScript dependencies (if applicable):

     ```bash
     npm install
     ```

3. **Set up Firebase**:
   - Create a Firebase project and configure Firebase Cloud Messaging (FCM).
   - Add Firebase configuration to your project and update the relevant keys.

4. **Run the system**:
   - Start the facial recognition system on Raspberry Pi:

     ```bash
     python facial_recognition.py
     ```

   - Run the web interface (if applicable):

     ```bash
     npm start
     ```

5. **Access the Web Interface**:
   - Open your browser and navigate to the provided local address for real-time video streaming and system control.

## License
This project is licensed under the MIT License.

## Acknowledgements
- **OpenCV** and **face_recognition** libraries for facial detection.
- **Firebase** for real-time notifications and secure user authentication.
- **Raspberry Pi** for its versatility and affordability in IoT projects. 

## Demo Video
Check out the live demo of this system in action on [YouTube](https://youtu.be/mMnXhzSfBOw).
