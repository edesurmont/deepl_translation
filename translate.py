# imports
import csv
import deepl
import numpy

# import sys
# file_to_translate = sys.argv[0]

# The file containing the data to translate
file_to_translate = "train_translations.csv"

# the file where the translated data will be written
# by default : 
# if the file_to_translate is 'hello.csv' it will be : 'hello_finished.csv'
file_translated = file_to_translate.split(".")[0] + "_finished.csv"

# an array storing all the data to translate
data = []

# Extract all of the data from the file, and store it into 'data'
def get_data():
    with open(file_to_translate, newline='') as data_file:
        datareader = csv.reader(data_file, delimiter=',', quotechar='"')
        for row in datareader:
            data.append(row)

# Reads the data to find the source language automaticaly
def find_source():
    # We look for "source_locale" or "source_locale_code"
    # in the first row, and if it is in it, whe get the
    # source language from the second row
    if "source_locale" in data[0]:
        return data[1][data[0].index("source_locale")]
    elif "source_locale_code" in data[0]:
        return data[1][data[0].index("source_locale_code")]
    else:
        raise "Error : no source language"

# Reads the data to find the source language automaticaly
def find_target():
    if "target_locale" in data[0]:
        return data[1][data[0].index("target_locale")]
    elif "target_locale_code" in data[0]:
        return data[1][data[0].index("target_locale_code")]
    else:
        raise "Error : no target language"

# Reads the data to find the columns to translate
def find_cols_to_translate():
    # we loof for the index of the columns which 
    return [index for (value, index) in zip(data[0], range(len(data[0]))) if (("source" in value) and (value != "source_locale") and ("resource" not in value))]

# Creates a function to translate text using the deepl api
translator = deepl.Translator("auth_key") 
def translate(text, source_lang, target_lang):
    return translator.translate_text(text=text, source_lang=source_lang, target_lang=target_lang)

# Translates the data
def translate_data(cols_to_translate, source_lang, target_lang):
    # we will regroup all the data ti translate in one array, 
    # to give it to the api which will be faster then passing 
    # every field to translate one at a time
    to_translate = []

    # We append the fields to it
    for row in data:
        # we only look at the fields in the columns to translate
        for i in cols_to_translate:
            # if the field is not empty and the field cointaning
            # the translation is empty (we don't want to 
            # translate twice the same content), we add the field
            # to the list to_translate
            if (row[i] != '') and (row[i+1] == ''):
                to_translate.append(row[i])
    
    # The api has a limit of elements in an array that we can pass
    # at a time
    # As it is not very clear what it is, we choose 50 to be sure 
    # not to have any issues

    max_text_nb = 50

    # We translate everything, sending max_text_nb texts at a time :

    # we have to break to_translate in nb_it parts (+1 if there is a rest)
    nb_it = len(to_translate) // max_text_nb

    # array containing the translations
    translation = []

    # breaking it into parts, translating them and adding the translation
    # to the translation arrray
    for i in range(nb_it):
        # we create a part
        parti = [to_translate[k] for k in range(i*max_text_nb, (i+1)*max_text_nb)]
        # we translate this part and append it to the translation array
        translation = numpy.append(translation, translate(text=parti, source_lang=source_lang, target_lang=target_lang))
    # we do the same with the rest
    rest = [to_translate[k] for k in range(nb_it*max_text_nb, len(to_translate))]
    # if it is empty, we get an error message
    if len(rest) != 0:
        translation = numpy.append(translation, translate(text=rest, source_lang=source_lang, target_lang=target_lang))

    # translation = translate(text=to_translate, source_lang=source_lang, target_lang=target_lang)

    # a variable to keep track of which translation we currently are using
    j = 0
    # for every row, for every field that was to translate, if it has been trnslated, we insert the 
    # translation in the next field
    for row in data:
        for i in cols_to_translate:
            if (row[i] != "") and (row[i+1] == ""):
                row[i+1] = translation[j]
                # we can now move on to the next translation
                j += 1

# Write the data to file_translated
def write_data():
    with open(file_translated, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            spamwriter.writerow(row)

# the main function, bringing everything together
def main():
    # our variables
    cols_to_translate = []
    source_lang = ""
    target_lang = ""

    get_data()

    source_lang = find_source()
    target_lang = find_target()
    cols_to_translate = find_cols_to_translate()

    # to verify everything was done correctly
    print(source_lang)
    print(target_lang)
    print(cols_to_translate)

    translate_data(cols_to_translate, source_lang, target_lang)

    write_data()

# if this file is run, we execute main()
if __name__ == "__main__":
    main()
