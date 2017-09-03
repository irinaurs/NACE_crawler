
import lxml.html
import requests
 
from lxml.cssselect import CSSSelector
 
def get_data(cui):
    r = requests.get("http://tobecompleted".format(cui))
    # Build the DOM Tree
    tree = lxml.html.fromstring(r.text)
    # construct a CSS Selector
    sel = CSSSelector(".link_firma")
    # Apply the selector to the DOM tree.
    try:
        match = sel(tree)[0]
    except:
        print "Firma cu urmatorul CUI nu exista: {0}".format(cui)
        return
 
    url = "http://tobecompleted0}".format(match.get("href"))
    data_page = requests.get(url)
    tree = lxml.html.fromstring(data_page.text)
    sel = CSSSelector("#evolutie-ron tr")
    rows = []
    try:
        rows = sel(tree)
    except:
        print "[EROARE] Eroare la obtinerea datelor: {0}".format(cui)
        return
    data = []
    for row in rows[2:]:
        sel = CSSSelector("td")
        cells = sel(row)
        data = data + [cell.text for cell in cells]
    return data
 
def main():
    cui_list = []
    with open('cui_list.txt', 'r') as fp:
        cui_list = fp.readlines()
 
    with open('date_firme.csv', 'w') as fp:
        features = ["Cifra de afaceri", "Profit net", "Marja profit net", "Numar angajati"]
        years = ["2010", "2011", "2012", "2013"]
        labels = []
        for feature in features:
            for year in years:
                label = "{0} - {1}".format(feature, year)
                labels.append(label)
 
        fp.write(', '.join(labels) + '\n')
 
        for index, cui in enumerate(cui_list):
            print "Incepem colectarea datelor pentru firma: {0}/{1}".format(index + 1, len(cui_list) + 1)
            # Remove the newline
            cui = cui.strip()
            if not cui:
                continue
            data = get_data(cui)
            if data:
                fp.write(', '.join(data) + '\n')
                print "Am obtinut cu succes datele pentru: {0}".format(cui)
    print "Scriptul a terminat cu succes executia."
 
if __name__ == '__main__':
    main()
