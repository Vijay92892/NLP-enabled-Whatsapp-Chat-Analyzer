WhatsApp Chat Analyzer 📱

SCREENSHOTS-->>
<img width="2862" height="1714" alt="Screenshot 2025-08-29 140357" src="https://github.com/user-attachments/assets/9a7fd0d9-f165-4680-8ce8-6c47e7db85d9" />



A powerful Python-based tool for extracting and visualizing meaningful insights from WhatsApp chat logs. This project combines robust data processing with static visualizations and an innovative AI-driven conversational agent for dynamic data exploration.

Features ✨
Static Dashboards: Generate pre-defined visualizations, including user activity over time, message distribution, and frequently used terms.

AI-Powered Analysis: Use natural language queries to ask specific questions about the chat data, such as "Who was most active last Tuesday?" or "Compare my message count with Jane's," and get custom plots in response.

Word Clouds: Visualize the most common terms in your chat to quickly identify key topics and trends.

Intuitive Interface: Built with seaborn to create clear, aesthetically pleasing graphs and charts.

Getting Started 🚀
These instructions will help you get a copy of the project up and running on your local machine.

Prerequisites
Make sure you have Python installed. The project relies on the following libraries:

pandas

seaborn

matplotlib

nltk

scikit-learn

transformers (for the AI agent)

You can install them all using pip:

Bash

pip install pandas seaborn matplotlib nltk scikit-learn transformers
Installation
Clone the repository:

Bash

git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
Export your WhatsApp chat:

Open the chat you want to analyze in WhatsApp.

Tap the three dots (⋮) > More > Export chat.

Exclude media to keep the file size small and the processing fast.

Save the .txt file to the project directory.

Run the analyzer:
Go to terminal and inside the project directory run >>> streamlit run app.py
