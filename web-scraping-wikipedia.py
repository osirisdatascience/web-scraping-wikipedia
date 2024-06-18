import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea'


request = requests.get(url)

# checking the HTTP status code. (200 -> Ok)
request.status_code

# # stored the content obtained from the URL in a variable
html_content = request.content

type(html_content)

# # needed to convert the variable type to a BeautifulSoup object to use the library's methods
wikipedia = BeautifulSoup(html_content, 'html.parser')

type(wikipedia)

# # check how the variable looks, if we can analyze the tags easily
print(wikipedia)

# # analyzing the inspect element and the wikipedia variable, I noticed that I need the table, so I will get only the table tag, specifying the class (if not specifying the class attribute, it would get the first table tag)
wikipedia.find('table', attrs={'class': 'wikitable'})

# # stored the desired table tag in a variable
capital_table = wikipedia.find('table', attrs={'class': 'wikitable'})

print(capital_table)

# # even though we can read and analyze the tags to work with, there is a very interesting method that makes reading the variable even easier, using indentation and making separations clearer
print(capital_table.prettify())

# # time to find the names of the capitals and their respective HREFs for later consultation on Wikipedia. For this, I created two lists to store the values during the loop
capitals = []
links = []

for each_tr in capital_table.findAll('tr')[1:]:  # fetching all 'tr' tags from the second one (index 1) to skip the header

    a_tag = each_tr.findAll('td')[1].find('a')  # of all 'td' tags from the second td, find the first 'a' tag which corresponds to the capital name

    if a_tag:  # if the 'a' tag is found
        capital_name = a_tag.text  # get the text of the tag and store it in a variable
        link_href = a_tag.get('href')  # get the HREF of the tag and store it in a variable
        if capital_name and capital_name.lower() != 'none':  # check if it is not of type None
            capitals.append(capital_name)  # store the obtained name in the capitals list
            links.append(link_href)  # store the obtained HREF in the links list

# now I have a list of capital names and another with the links of the respective capitals
print(capitals)
print(links)

# # Checking the number of capitals using the len method. It tells the size of the list, which is the total number of capitals. They are the 26 states and the Federal District.
len(capitals)

len(links)

# # I will need to access two values at a time in a loop to search the site, so it's interesting to zip the two lists into a dictionary so I can access two values (key and value) for each item without needing two for loops (one for each list).
capital_with_link = dict(zip(capitals, links))
print(capital_with_link)

# # Idea of the for loop: For each item (Capital and respective link) access the link, look for the second paragraph (observed through inspect element on the site that it would be the summary paragraph) get the paragraph text and store it in my summary list declared before the loop.
summary = []

for capital, link in capital_with_link.items():  # iterating through each item (key + value) in the dictionary

    url2 = f'https://pt.wikipedia.org{link}'  # visit the site that contains information about the respective capital

    request = requests.get(url2)  # store the request of the site in a variable

    if request.status_code == 200:  # check the generated HTTP status code (Remember -> 200 = Ok)

        page = BeautifulSoup(request.text, 'html.parser')  # used BeautifulSoup to get the request text, analyze the HTML with the parser (Access the HTML intelligently)

        paragraphs = page.find_all('p')  # access all 'p' tags on the site

        if len(paragraphs) >= 2:  # analyzing the inspect element as well as the wikipedia variable, I noticed that the second 'p' tag corresponded to the brief summary of the capital. that's why the if (to avoid pages with less than 2 'p' tags)

            paragraph_text = paragraphs[1].get_text()  # get the text of the second 'p' tag

            summary.append(paragraph_text)  # add the text to the summary list

            # print(f'{capital}\nSummary of {capital}:\n {paragraph_text}\n') print for testing and to verify if everything went right in acquiring the text
        else:
            print(f'Could not find the second paragraph for {capital}.\n')  # if the page had less than 2 paragraphs

    else:
        print(f"Error, page access not obtained. HTTP Status Code: {request.status_code}")  # similar to error handling, to display the obtained HTTP status code, if different from 200 (OK)

# # same idea as the capital acquisition loop. But for the states, I just want to get the text, to organize it in the DataFrame.
states = []

for each_tr in capital_table.findAll('tr')[1:]:  # passing index 1 onward to skip the header
    # access the fourth 'td' and then access the first 'a' tag
    a_tag = each_tr.findAll('td')[3].find('a', recursive=False)  # recursive false, only 'a' tags that are direct children of the 'td' (do not have another parent tag). Because there is a tag in the state Pará that is inside a span

    if a_tag:
        state_name = a_tag.text  # if there is the 'a' tag, get the text and store it in a variable
        if state_name and state_name.lower() != 'none':  # check if the variable is compatible with the type
            states.append(state_name)  # add to the list

print(states)

# # check the number of elements in the list
print(len(states))

# # Created a variable to store the DataFrame generated by the capitals, states, and summary lists. But using a dictionary. With each key being the column name, and its values being the table values
df = pd.DataFrame({'Capital Name': capitals, 'State': states, 'Summary': summary})

df
