from openai import OpenAI

client = OpenAI(api_key="api_key_here")

# Function to split text into 8k token chunks (approximation)
def split_into_chunks(text, chunk_size=8000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    for word in words:
        word_size = len(word)  # Approximate token size by word length

        if current_chunk_size + word_size > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_chunk_size = word_size
        else:
            current_chunk.append(word)
            current_chunk_size += word_size

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Function to process a chunk with a user prompt
def get_api_response_with_prompt(chunk, prompt, model="gpt-4o-mini"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "developer", "content": prompt},
                {"role": "user", "content": chunk}
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with chunk: {e}")
        return "Error processing chunk."

# Function to split text into 100k token chunks
def split_into_large_chunks(text, chunk_size=100000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    for word in words:
        word_size = len(word)

        if current_chunk_size + word_size > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_chunk_size = word_size
        else:
            current_chunk.append(word)
            current_chunk_size += word_size

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Function to split text into chapters
def split_text_into_chapters(chunk, model="gpt-4o-mini"):
    prompt = "Please split the following text into chapters and output the text with chapter titles."
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "developer", "content": prompt},
                {"role": "user", "content": chunk}
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with chunk: {e}")
        return "Error processing chunk."

# Main function to process the combined text, add prompts, and split into chapters
def process_combined_text(input_file, output_file, user_prompt):

    # Read the content of the input text file
    with open(input_file, 'r', encoding='utf-8') as file:
        combined_text = file.read()

    # Split the combined text into 8k token chunks
    chunks = split_into_chunks(combined_text)

    # Process each chunk with the given user prompt
    final_output = ""
    for idx, chunk in enumerate(chunks):
        print(f"Processing chunk {idx + 1}/{len(chunks)} with prompt...")
        response = get_api_response_with_prompt(chunk, user_prompt)
        final_output += f"Response for chunk {idx + 1}:\n{response}\n\n"

    # Split the final output into 100k token chunks
    large_chunks = split_into_large_chunks(final_output)

    # Split the large chunks into chapters
    chaptered_output = ""
    for idx, large_chunk in enumerate(large_chunks):
        print(f"Processing large chunk {idx + 1}/{len(large_chunks)} to split into chapters...")
        chapter_response = split_text_into_chapters(large_chunk)
        chaptered_output += f"Chapters from large chunk {idx + 1}:\n{chapter_response}\n\n"

    # Write the final output with split chapters to the output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(chaptered_output)

    print(f"All responses stored in {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "in.txt"  # Replace with your input file path
    output_file = "chaptered_output.txt"  # Replace with your output file path
    user_prompt = "Proszę o dokonanie korekty językowej, stylistycznej, składniowej oraz ortograficznej poniższego fragmentu książki. Nie skracaj treści ani nie usuwaj żadnych zdań – popraw tylko błędy, zachowując oryginalny styl i pełną długość tekstu. Zadbaj o płynność narracyjną, spójność językową i logiczny ciąg wypowiedzi."

    process_combined_text(input_file, output_file, user_prompt)
