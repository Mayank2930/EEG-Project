# EEG-Controlled Wheelchair 🧠➡️🦽

## 🚀 Overview
This project is an **EEG-controlled wheelchair** that allows users to navigate using brainwave signals. By analyzing EEG data, the system classifies user intentions and translates them into movement commands. 

## 🔬 Technologies Used
- **Machine Learning**: Fine-tuned `RandomForestClassifier` for EEG signal classification  
- **Deep Learning**: CNN-based emotion detection (75% accuracy on FER-2013 dataset)  
- **Backend**: Django REST Framework (DRF) for API communication  
- **Frontend**: React (for real-time interaction)  
- **Database**: SQLite3  
- **Hardware**: Working wheelchair connected to the web app

## 🎯 Features
✔️ **Real-time EEG signal processing**  
✔️ **Classification of mental commands (e.g., Forward, Left, Right, Stop)**  
✔️ **Emotion detection for adaptive control**  
✔️ **API for signal transmission**  
✔️ **Scalable backend for future extensions**  

## 🛠️ Setup Instructions
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/eeg-wheelchair.git
cd eeg-wheelchair
