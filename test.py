from bs4 import BeautifulSoup

text = ''
with open('page_source.txt', 'r', encoding="utf-8") as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')

scripts = soup.select("head > script")
jsonStr = ''
for script in scripts:
    if script.text.strip() != '' and script.text.strip()[0] == 'g':
        print(script)
        jsonStr = script.text.strip().split('\n')[0].split('=')[1]

jsonStr = jsonStr.rstrip(';').strip()

print(jsonStr)