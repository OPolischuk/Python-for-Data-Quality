import re

# Step 1: Define helper functions
def split_sentences(text):
    """Split the text into sentences, keeping punctuation."""
    return re.split(r'([.!?])', text)

def normalize_sentence(sentence):
    """Normalize a single sentence: correct capitalization and fix specific spelling."""
    sentence = sentence.strip()
    if sentence:
        # Capitalize first letter, lowercase others
        sentence = sentence[0].upper() + sentence[1:].lower()
        # Fix specific misspellings
        sentence = sentence.replace("Iz", "is")
    return sentence

def process_sentences(sentences):
    """Process each sentence to normalize it and add punctuation back."""
    normalized_sentences = [
        normalize_sentence(sentences[i]) + sentences[i + 1]
        for i in range(0, len(sentences) - 1, 2)
        if sentences[i].strip()
    ]
    return ''.join(normalized_sentences)

# Step 2: Define the main function
def normalize_text(text):
    """Normalize the entire text."""
    sentences = split_sentences(text)
    return process_sentences(sentences)

# Example text
text = '''tHis iz your homeWork, copy these Text to variable.
You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence
and add it to the END OF this Paragraph. it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.
last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

# Normalize and display the text
normalized_text = normalize_text(text)
print(normalized_text)
