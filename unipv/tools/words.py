def reverse_words(input_string):
    input_words = input_string.split(" ")
    input_words = input_words[-1::-1]
    output = ' '.join(input_words)
    return output
