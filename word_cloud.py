def word_cloud(file_name, raw_text):
    from os import path
    from wordcloud import WordCloud

    d = path.dirname(__file__)

    # Read the whole text.
    if raw_text == '':
        text = open(path.join(d, file_name)).read()
    else:
        text = raw_text

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    # wordcloud = WordCloud(max_font_size=40).generate(text)
    # plt.figure()
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    plt.show()

if __name__ == '__main__':
    '''
    1. pip install wordcloud
    2. if you want to pass text by file, use first argument and leave the 2nd argument as empty string
       if you want to pass a single string variable, pass in second argument and leave 1st arguement empty string
    '''
    word_cloud('', 'plain text here')
