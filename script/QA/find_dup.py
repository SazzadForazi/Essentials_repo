def find_dup(text):
    words = text.lower().split()
    count = {}

    for word in words:
        word = word.strip(".,!?;:")  # Optional: remove punctuation
        if word in count:
            count[word] += 1
        else:
            count[word] = 1

    for word, c in count.items():
        if c > 1:
            print(f"{word} ({c})")

# Example usage
find_dup("The more you know, the more you realize how much you don't know.")
