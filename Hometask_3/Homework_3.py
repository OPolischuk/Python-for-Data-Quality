import re

def normalize_text(text):
    # Split the text for sentences and keep punctuation marks.
    sentences = re.split(r'([.!?])', text)

    normalized_sentences = []

    for i in range(0, len(sentences) - 1, 2):  
        sentence = sentences[i].strip() 

        if sentence:
            # Перша буква великою, решта маленькими
            sentence = sentence[0].upper() + sentence[1:].lower()

            # Виправляємо "iZ" на "is" тільки коли це помилка
            sentence = sentence.replace("Iz", "is")

            # Додаємо речення з відповідним розділовим знаком
            normalized_sentences.append(sentence + sentences[i + 1])

    # Об'єднуємо всі нормалізовані речення в один текст
    return ''.join(normalized_sentences)

# Приклад тексту
text = '''tHis iz your homeWork, copy these Text to variable.
You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence
and add it to the END OF this Paragraph. it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.
last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

normalized_text = normalize_text(text)
print(normalized_text)

