'''
 The script below utilizes europepmc Articles RESTful API
 https://europepmc.org/RestfulWebService to scrape through the fulltext of
 a subset of peer-reviewed articles with the sole objective of knowing the country
 and in the case of Kenya, the county where the study sites were located.

 Alex Maina - Librarian KEMRI-Wellcome Trust Research Programme

'''

import requests
from bs4 import BeautifulSoup
import re
import geonamescache
import spacy
from spacy.matcher import PhraseMatcher
import pycountry
from openpyxl import Workbook



pmcids = ['PMC11525066','PMC10864294','PMC11064105','PMC11438083','PMC11069174','PMC10716622','PMC11349107',
'PMC11338195','PMC11718159','PMC11285936','PMC11289976','PMC11723863','PMC11462847','PMC10950691',
'PMC10996164','PMC10919173','PMC11345449','PMC11542398','PMC11562111','PMC11094066','PMC11375402',
'PMC11549274','PMC11287631','PMC11149845','PMC10927117','PMC7616702','PMC10852234','PMC10952650',
'PMC11357821','PMC11404254','PMC10923414','PMC11637338','PMC11367973','PMC11087563','PMC11622353',
'PMC11046809','PMC11293692','PMC10867106','PMC11103839','PMC11654438','PMC10854052','PMC11192416',
'PMC11106534','PMC10877892','PMC10823747','PMC11229757','PMC11409615','PMC10937349','PMC7616653',
'PMC11197641','PMC11464403','PMC10765698','PMC11420681','PMC11088304','PMC11131180','PMC10977907',
'PMC11387285','PMC10832137','PMC11536953','PMC11613948','PMC11624724','PMC10864189','PMC11342035',
'PMC11232189','PMC11097591','PMC11005831','PMC11590815','PMC10906885','PMC11365168','PMC11370027',
'PMC10905788','PMC10840034','PMC11253331','PMC11436855','PMC11603168','PMC7616119','PMC11216587',
'PMC11410205','PMC11438207','PMC11737602','PMC10892224','PMC11399766','PMC11254782','PMC11530017',
'PMC10901986','PMC10871522','PMC11441138','PMC11618498','PMC10832587','PMC11499763','PMC10945606',
'PMC11375914','PMC11293042','PMC10846728','PMC11139289','PMC7617250','PMC11382623','PMC11675204',
'PMC10949706','PMC10773318','PMC10977730','PMC11552008','PMC11329769','PMC11461663','PMC11581349',
'PMC10935770','PMC10921557','PMC11289910','PMC11337709','PMC11106525','PMC11392261','PMC11605845',
'PMC11097862','PMC10928745','PMC11253580','PMC10800037','PMC11581619','PMC11331881','PMC11163641',
'PMC11450608','PMC10849973','PMC10842664','PMC11464310','PMC11004247','PMC7616506','PMC11300237',
'PMC11515546','PMC10902387','PMC11349500','PMC11216563','PMC10900964']



data = []
for i in pmcids:
    url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/'+i+'/fullTextXML'

    xml_data = requests.get(url).content
    soup = BeautifulSoup(xml_data, 'xml')
    #get PMID
    pmid_tag = soup.find("article-id", {"pub-id-type": "pmid"})

    # Extract the PMID if not exist return None
    pmid = pmid_tag.text if pmid_tag else None


    sections = []
    for sec in soup.find_all("sec"):
        sec_data = {
            "id": sec.get("id"),
            "sec_type": sec.get("sec-type"),
            "title": sec.find("title").text if sec.find("title") else None,
            "content": sec.find("p").text.strip() if sec.find("p") else None
        }
        sections.append(sec_data)

    # Print structured data
    for section in sections:
        if section['title'] == 'Methods':
            paragraph = section['content']
            country_names = re.findall(r'\((.*?)\)', paragraph)
            gc = geonamescache.GeonamesCache()
            countries = gc.get_countries()
            country_names = [country['name'] for country in countries.values()]

            # Extract mentioned country names
            mentioned_countries = [country for country in country_names if country in paragraph]

            kenyan_counties = [ "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo-Marakwet", "Embu", 
                        "Garissa", "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho", 
            "Kiambu", "Kilifi", "Kirinyaga", "Kisii", "Kisumu", "Kitui", "Kwale", 
            "Laikipia", "Lamu", "Machakos", "Makueni", "Mandera", "Marsabit", 
            "Meru", "Migori", "Mombasa", "Murang'a", "Nairobi", "Nakuru", 
            "Nandi", "Narok", "Nyamira", "Nyandarua", "Nyeri", "Samburu", 
            "Siaya", "Taita-Taveta", "Tana River", "Tharaka-Nithi", "Trans Nzoia", 
            "Turkana", "Uasin Gishu", "Vihiga", "Wajir", "West Pokot"
                ]

            # Load spaCy's English language model
            nlp = spacy.load("en_core_web_sm")

            # Create a PhraseMatcher and add counties
            matcher = PhraseMatcher(nlp.vocab)
            patterns = [nlp.make_doc(county) for county in kenyan_counties]
            matcher.add("KenyanCounties", patterns)

            def find_counties_spacy(text, matcher):
                doc = nlp(text)
                matches = matcher(doc)
                found_counties = set([doc[start:end].text for match_id, start, end in matches])
                found_counties = list(found_counties)
                return found_counties

            #find the counties
            found_counties = find_counties_spacy(paragraph, matcher)
            ##print("Found Counties:", found_counties)
            output = [[pmid],mentioned_countries,found_counties,[url]]
    #Append the output as a list named data
    data.append(output)

#print(data)
# Create a new Excel workbook
workbook = Workbook()
sheet = workbook.active
sheet.title = "List Data"

# Add column headers
sheet.cell(row=1, column=1, value="PMID")
sheet.cell(row=1, column=2, value="Countries")
sheet.cell(row=1, column=3, value="Counties")
sheet.cell(row=1, column=4, value="url")

# Write the data to Excel starting from the second row
row = 2
for record in data:
    col = 1
    for sublist in record:
        cleaned_sublist = [str(item) if item is not None else "" for item in sublist]
 
        sheet.cell(row=row, column=col, value=", ".join(cleaned_sublist))
        col += 1
    row += 1

# Save the workbook
output_file = "new_list_data_with_headers.xlsx"
workbook.save(output_file)

print(f"Data with headers saved to {output_file}!")

    
