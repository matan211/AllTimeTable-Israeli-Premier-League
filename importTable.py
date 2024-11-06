import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def importTable():
    # Step 1: Fetch the website content
    url = "https://sports.walla.co.il/category/157"  # replace with the website URL
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Find the specific table
    # Adjust selector as needed (e.g., 'table', class, id, etc.)
    table = soup.find('table')

    # Step 4: Extract table data into a DataFrame
    headers = [header.text for header in table.find_all('th')]
    length = headers.index("נק") + 1
    headers[5] = 'הפסדים'
    rows = [
        [cell.text for cell in row.find_all(['td', 'th'])]
        for row in table.find_all('tr')
    ]

    # Adjust the headers
    index = headers.index("שערים")  # Find the index of "שערים" in rows[0]
    headers[index] = "שערי זכות"    # Replace the element at that index
    headers[headers.index("נק")] = "שערי חובה"
    headers.append("נק")

    # Adjust the table rows
    for row in rows[1:]:
        goals = row[length - 2]
        dashIndex = goals.find("-")

        # Goals for
        gf = goals[:dashIndex]

        # Goals against 
        ga = goals[dashIndex + 1 : ]

        print(goals)
        print()

        row[length - 2] = gf
        row.insert(length - 2, ga)

    df = pd.DataFrame(rows[1:], columns=headers)  # Skip header row in data

    # Step 5: Kill excel task(if neccesary)
    os.system("taskkill /f /im excel.exe")
    print("Excel terminated using taskkill")

    # Step 6: Save to Excel
    path = "C://Users//Matan//PycharmProjects//allTimeTable//"
    df.to_excel(path + "table_data.xlsx", index=False)

    print("Table saved as table_data.xlsx")

    # Step 7: Open file
    os.startfile(path + "table_data.xlsx")