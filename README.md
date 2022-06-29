# Deepl Translation

Two pyhton scripts to :
- translate a csv file (respecting a certain format)
- cut a csv file into multiple parts (based on the number of lines you want in a part)

# Translation

Replace "auth_key" with your deepl api account auth_key.
Replace the file_to_translate by your file.

## Document format:
- it should contain a column "source_locale" or "source_locale_code", containing the source languages's code
- same for the target language
- the columns to translate must contain "source" in them
- they should be followed by a blank column (and there should not be two in a row)

## Functionalities
- finding the source and target languages automaticaly
- finding the columns to translate automaticaly
- sending grouped api calls for better speed

## Exemple document

 target_name | source_description             | target_description_ | source_locale | target_locale |
| ------------ | ----------- | ----------- | ------------------------------ | ------------------- | ------------- | ------------- |
| 1            | Un voyage   |             | C'est fantastique !            |                     | fr            | en-us         |
| 2            | Un bateau   |             | Un moyen de transport maritime |                     | fr            | en-us         |
| 3            | Une voiture |             | Très pratique                  |                     | fr            | en-us         |

## Exemple output

 target_name | source_description             | target_description_ | source_locale | target_locale |
| ------------ | ----------- | ----------- | ------------------------------ | ------------------- | ------------- | ------------- |
| 1            | Un voyage   |  A journey  | C'est fantastique !            | This is fantastic!  | fr            | en-us         |
| 2            | Un bateau   |  A boat     | Un moyen de transport maritime | A means of maritime transport | fr            | en-us         |
| 3            | Une voiture |  A car      | Très pratique                  | Very practical      | fr            | en-us         |

# Cut 

This script cuts a document, you just have to specify the number of rows you want per docment and it will cut it into the according number of parts, while adding the first line of the document to all of the parts
