# SRT Subtitle Translator

## Overview

This project is a Python-based tool for translating `.srt` subtitle files into a target language using the OpenAI API. It supports summarizing subtitle content, translating it while maintaining context, and outputting the translated subtitle file in `.srt` format. The tool divides the subtitle text into manageable chunks, generates summaries for better context handling, and provides sentence-by-sentence translations with the help of the OpenAI language models.

### Key Features:
- **SRT Parsing:** Extracts subtitle text from `.srt` files.
- **Chunk-based Summarization:** Generates concise summaries of the subtitles, chunk by chunk, to help with translation context.
- **Context-aware Translation:** Uses surrounding sentences to provide accurate translations while preserving the meaning.
- **Custom Output:** Translated subtitles are saved in a new `.srt` file.
- **Supports Multiple Languages:** Default target language is Chinese, but this can be modified.

## Prerequisites

### 1. Python 3.x
Make sure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).

### 2. OpenAI Python Client Library
The OpenAI API is required for text summarization and translation. Install the OpenAI Python library using `pip`:

```bash
pip install openai
```

### 3. OpenAI API Key
You will need an API key from OpenAI to use their language models. You can sign up and get your API key from [OpenAI](https://beta.openai.com/signup/).

### 4. Your `.srt` Subtitle File
Prepare an `.srt` file that you want to translate. Make sure it follows the typical `.srt` format with subtitle timing and text blocks.

## How to Use

1. **Clone the Repository or Download the Script:**
   You can download the script or clone this repository to your local machine.

   ```bash
   git clone https://github.com/your-repo/AI-subtitle-translator.git
   ```

2. **Install Required Dependencies:**
   Make sure you have the required dependencies installed, specifically the `openai` package:

   ```bash
   pip install openai
   ```

3. **Run the Script:**
   Run the script using Python:

   ```bash
   python sum_srt_translator.py
   ```

4. **Enter Your OpenAI API Key:**
   The program will prompt you to enter your OpenAI API key. Make sure to provide the correct API key to ensure the script works properly.

5. **Provide the Input `.srt` File:**
   Enter the path to your input `.srt` subtitle file. You can use relative or absolute paths.

6. **Choose the Output File Path:**
   You can specify the output file where the translated subtitles will be saved. If you do not provide a path, the default will be the same location as the input file with `_translated` added to the filename.

7. **Translation Process:**
   The script will parse the `.srt` file, generate summaries, and start translating the subtitles while preserving context.

8. **Translation Completed:**
   Once the translation is complete, the script will notify you and save the translated `.srt` file to the output path.
