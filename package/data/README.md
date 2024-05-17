# Data 

Databases used in our package containing : 
- database_products :  informations (name, ingredients,...) about a variety of cosmetics, sourced here : https://fr.openbeautyfacts.org/data
- database_carcinogenic, database_paraben and database_endocrine : In this project we consider only 3 categories of dangerous products: the paraben, carcinogenic products and endocrine. The database for each categories were found on PubChem (https://pubchem.ncbi.nlm.nih.gov). The original databases extracted on this website contained informations about the compounds like their name, synonym, SMILES, the exact name, the iupac name… The name of the original databases was :... Not all this informations are important for our project, we only need the compound name, iupac name and synonyms. Therefore we wrote a python code #ADD NAME CODE to extract only the information we needed and got the following databases with the names :...

encore compléter car database_dangers c'est la combinaison des trois database ci-dessus
