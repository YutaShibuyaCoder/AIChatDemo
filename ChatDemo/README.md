# Internal FAQ AI Chatbot

This project is an AI chatbot that uses OpenAI's GPT model to answer questions based on uploaded internal FAQ documents. It provides a simple web interface using Streamlit.

## Features

- Upload and process FAQ documents in PDF or DOCX format
- Natural language question input
- AI-generated answers based on FAQ content
- Simple and user-friendly chat-like interface

## Requirements

- Python 3.7 or higher
- OpenAI API key

## Setup

1. Clone or download the repository.

2. Install the required packages:

```
pip install streamlit langchain openai faiss-cpu python-dotenv PyPDF2 python-docx tiktoken
```

3. Create a `.env` file in the project root directory and set your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the application with the following command:

```
streamlit run main.py
```

2. Use the interface displayed in your web browser.

3. Upload an FAQ document (PDF or DOCX) from the sidebar.

4. Enter questions in the chat interface and receive answers from the AI.

## File Structure

- `main.py`: Main script for the Streamlit application
- `chatbot.py`: Chatbot logic and OpenAI API integration
- `document_loader.py`: PDF and DOCX file loader
- `config.py`: Configuration file (e.g., OpenAI model specification)

## Customization

- You can change the OpenAI model used in `config.py`.
- Edit the `prompt_template` in `chatbot.py` to customize the AI's response style.

## Notes

- This application uses the OpenAI API, which may incur usage fees.
- Uploaded documents may contain confidential information, so ensure appropriate security measures are in place.

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).