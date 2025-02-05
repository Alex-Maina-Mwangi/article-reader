# article-reader
A utility that uses europepmc Articles RESTful API to read the full test of articles and extract data.

# Background
At the KEMRI-Wellcome Trust Research Programme we were faced with the problem of reading 250 peer-reviewed scientific articles and extract data on the sites where the data was collected from(primarily get the study sites). We were more interested in countries where we collected the data and in the case of Kenya(where we are based). Furthermore, we were interested in knowing which counties we conducted our research from in all studies carried out in the republic of Kenya where we are domiciled.

# How could we achieve this given a tight reporting deadline?
We had two options:
1. Have someone( myself the Librarian) manually read through all the 250 articles and extract the data manually.
2. Think and come up with an automated solution ( I am happiest when doing this) to read the 250 articles and load the data neatly in a .csv file for further analysis in Pandas.

Obviously, I chose the second option.

# How did we implement the second option?
I utilised the freely available europepmc Articles RESTful API https://europepmc.org/RestfulWebService specifically the `GET fullTextXML` module.

I wrote a python script (`main.py`) that incorporated a number of libraries namely:
1. BeautifulSoup
2. geonamescache
3. spacy
4. pycountry
5. openpyxl

See also the `virtualenv` file `requirements.txt` for more details of the libraries used.

In a nutshell this script iterates through a list of PMCID numbers and reads fulltext XML and extract the study site data and finally loads this data neatly into an excel file.

# What is a PMCID number

According to the US National Institutes of Health, a PMCID number otherwise known in full as "PubMed Central Identifier," is a unique identification number assigned to a full-text scientific article deposited in the PubMed Central (PMC) database,

For more details email me at amainaster@gmail.com


