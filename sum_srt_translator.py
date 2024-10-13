import re
from pathlib import Path
from openai import OpenAI

def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()

    pattern = re.compile(r'(\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n)((?:.*(?:\n|$))*?)(?:\n|$)')
    return pattern.findall(content)

def generate_summary(client, subtitles_text):
    # Define maximum tokens per chunk (adjust based on model limits, e.g., 2048 tokens)
    max_chars_per_chunk = 10000  # Approximate character limit per chunk
    chunk_summaries = []
    current_chunk = []
    current_chunk_size = 0

    # Split subtitles into chunks
    for text in subtitles_text:
        text_length = len(text) + 1  # +1 for newline or space
        if current_chunk_size + text_length > max_chars_per_chunk:
            # Generate summary for the current chunk
            chunk_summary = summarize_chunk(client, current_chunk)
            chunk_summaries.append(chunk_summary)
            # Start a new chunk
            current_chunk = [text]
            current_chunk_size = text_length
        else:
            current_chunk.append(text)
            current_chunk_size += text_length

    # Summarize the last chunk if it exists
    if current_chunk:
        chunk_summary = summarize_chunk(client, current_chunk)
        chunk_summaries.append(chunk_summary)

    # Combine chunk summaries
    combined_summaries = '\n'.join(chunk_summaries)

    # Generate final summary from chunk summaries
    final_summary = summarize_chunk(client, [combined_summaries], final=True)

    return final_summary

def summarize_chunk(client, chunk_texts, final=False):
    summary_input = '\n'.join(chunk_texts)

    # Adjust the prompt if it's the final summary
    if final:
        system_content = (
            "You are a summarization assistant. Based on the following summaries, "
            "provide a concise and comprehensive overall summary capturing the main themes and topics."
            "It should be in one paragraph"
        )
    else:
        system_content = (
            "You are a summarization assistant. Summarize the following text "
            "to provide an overview of its content. The summary should be concise "
            "and capture the main themes and topics. It should be in one paragraph"
        )

    messages = [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": summary_input
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    summary = response.choices[0].message.content.strip()
    return summary

def translate_text(client, text, prev_sentences=None, next_sentences=None, summary='', target_language='Chinese'):
    print(f"\nSummary:\n{summary}\n")
    print(f"Text to translate:\n{text}\n")
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a translator. Translate the given text to {target_language}. "
                "Your translation should pay attention to the provided context and summary. "
                "The translation should be as a native speaker would express it. "
                "Preserve any line breaks in the original text."
            )
        }
    ]

    if summary:
        messages.append({
            "role": "assistant",
            "content": f"Here is an overview of the entire content:\n{summary}"
        })

    if prev_sentences:
        prev_context = '\n'.join(prev_sentences)
        messages.append({
            "role": "assistant",
            "content": f"The previous two sentences are:\n{prev_context}"
        })

    if next_sentences:
        next_context = '\n'.join(next_sentences)
        messages.append({
            "role": "assistant",
            "content": f"The next two sentences are:\n{next_context}"
        })

    messages.append({
        "role": "user",
        "content": f"Text to translate:\n{text}"
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def translate_srt(client, input_file, output_file):
    subtitles = parse_srt(input_file)
    total_subtitles = len(subtitles)
    translated_subtitles = []

    # Extract all text from subtitles
    subtitles_text = [text.strip() for _, text in subtitles]

    # Generate summary using the entire subtitles text
    print("Generating summary for the entire subtitles text...")
    summary = generate_summary(client, subtitles_text)
    print(f"Summary generated:\n{summary}\n")

    for index in range(total_subtitles):
        header, text = subtitles[index]
        original_text = text.strip()

        # Collect context from surrounding subtitles
        prev_sentences = []
        # Previous two subtitles
        if index - 2 >= 0:
            prev_sentences.append(subtitles[index - 2][1].strip())
        if index - 1 >= 0:
            prev_sentences.append(subtitles[index - 1][1].strip())

        next_sentences = []
        # Next two subtitles
        if index + 1 < total_subtitles:
            next_sentences.append(subtitles[index + 1][1].strip())
        if index + 2 < total_subtitles:
            next_sentences.append(subtitles[index + 2][1].strip())

        translated_text = translate_text(client, original_text, prev_sentences, next_sentences, summary)
        translated_subtitles.append(f"{header}{translated_text}\n")

        if index < total_subtitles - 1:
            translated_subtitles.append("\n")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translated_subtitles)

def get_valid_file_path(prompt):
    while True:
        file_path = input(prompt).strip()
        file_path = file_path.strip('"\'')
        path = Path(file_path)
        if path.is_file():
            return str(path)
        print(f"File not found: {file_path}")
        print("Please enter a valid file path. Make sure to use forward slashes (/) or escaped backslashes (\\\\).")

if __name__ == "__main__":
    print("SRT Subtitle Translator")
    print("----------------------")

    # Get API key from user
    api_key = input("Please enter your OpenAI API key: ").strip()
    client = OpenAI(api_key=api_key)

    # Get input file path
    input_file = get_valid_file_path("Enter the path to your input SRT file: ")

    # Get output file path
    output_dir = Path(input_file).parent
    default_output = output_dir / f"{Path(input_file).stem}_translated{Path(input_file).suffix}"
    output_file = input(f"Enter the path for the output translated SRT file (default: {default_output}): ").strip()
    if not output_file:
        output_file = str(default_output)

    print("\nStarting translation...")
    translate_srt(client, input_file, output_file)
    print(f"Translation completed. Output saved to: {output_file}")
