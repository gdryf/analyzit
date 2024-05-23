# Data 

Databases used in our package containing : 
- database_products :  informations (name, ingredients,...) about a variety of cosmetics, sourced here : https://fr.openbeautyfacts.org/data
- raw_database_carcinogenic, raw_database_paraben and raw_database_endocrine : In this project we consider only 3 categories of dangerous products: the paraben, carcinogenic products and endocrine. The database for each categories were found on PubChem (https://pubchem.ncbi.nlm.nih.gov). The original databases extracted on this website contained informations about the compounds like their name, synonym, SMILES, the exact name, the iupac name… The name of the original databases was : raw_database_substance. Not all this informations are important for our project, we only need the compound name, iupac name and synonyms. Therefore we wrote a python code "modification_and_merge_database_dangers" to extract only the information we needed. 

The three databases of dangerous products were then merged and a column was added to specifying the type of danger corresponding to each compound. This means that the function does not have to search for dangerous products  in three different csv files but only in one, named : database_dangers.

