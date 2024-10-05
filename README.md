#PodGen
---
title: "Podcast Generator from PDF 🎙️"
author: "Tejas Reddy S"
date: "`r Sys.Date()`"
output: html_document
---

# 🎉 Welcome to the Podcast Generator Project!

This project transforms PDF documents into engaging podcast scripts and audio using the power of AI! 🌟 

## 📖 Project Overview

The **Podcast Generator** is designed to extract text from PDF files and generate a well-structured podcast script. It utilizes the Azure OpenAI services for both generating the dialogue and converting the text to speech. 🎤✨ 

### 🚀 Key Features

- **PDF Text Extraction**: Extracts text from various PDF files effortlessly. 📄
- **AI-Powered Script Generation**: Generates engaging podcast scripts using advanced AI algorithms. 🤖
- **Text-to-Speech Conversion**: Converts generated scripts into high-quality audio files. 🔊
- **Interactive UI**: Built using Streamlit for a seamless user experience. 💻

## 🛠️ Technologies Used

- **Python**: The primary programming language for the project. 🐍
- **Streamlit**: For creating the interactive web application. 🌐
- **Pymupdf**: For extracting text from PDF files. 📚
- **Requests**: To make API calls to Azure OpenAI. 📡
- **Azure OpenAI**: For generating dialogues and converting text to speech. ☁️

## 📦 Installation Instructions

To get started with the project, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/podgen.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd PodGen
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**: Create a `.env` file and add your Azure OpenAI credentials:

    ```bash
    AZURE_OPENAI_API_KEY=your_api_key
    AZURE_OPENAI_VERSION=your_api_version
    AZURE_OPENAI_ENDPOINT=your_endpoint
    AZURE_OPENAI_DEPLOYMENT=your_deployment
    AZURE_OPENAI_TTS_ENDPOINT=your_tts_endpoint
    AZURE_OPENAI_TTS_KEY=your_tts_key
    ```

5. **Run the application**:

    ```bash
    streamlit run app.py
    ```

## 🖥️ Usage Instructions

1. Upload a PDF file containing your content.
2. Click on the "Generate Podcast" button.
3. Listen to the generated podcast audio right in your browser! 🎧

## 🤝 Contributing

We welcome contributions! If you have suggestions for improvements or want to report a bug, please create an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Contact

For any inquiries, feel free to reach out to me:

- **Email**: tejasreddy1505@gmail.com


---

Thank you for checking out the Podcast Generator! We hope you find it useful and fun to work with! 🎊
