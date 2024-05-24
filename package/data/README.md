# Data 

Databases used in our package containing : 
- `raw_database_products.csv` :  Informations (name, ingredients,...) about a variety of cosmetics, sourced here : https://fr.openbeautyfacts.org/data
- `database_products.csv` : This database was obtained by filtering the `raw_database_products.csv` file. Certain categories of information were deleted because they were irrelevant for our project, we only kept the barcode, name of the product (french and english) and list of ingredients (french and english). The products that did not a list of ingredients were also deleted. Finally, for the products having their names and ingredients in french and english, the english language was selected to be able to have only one column with the lists of ingredients.
- `raw_database_carcinogenic.csv`, `raw_database_paraben.csv` and `raw_database_endocrine.csv` : In this project we consider only 3 categories of dangerous products: the paraben, carcinogenic products and endocrine. The database for each categories were found on PubChem (https://pubchem.ncbi.nlm.nih.gov). The original databases extracted on this website contained informations about the compounds like their name, synonym, SMILES, the exact name, the iupac name… .
- `database_dangers.csv` : This database was obtained by filtering the `raw_database_carcinogenic.csv`, `raw_database_paraben.csv` and `raw_database_endocrine.csv` databases. Certain categories of information were deleted because they were irrelevant for our project, we only kept the compound name, iupac name and synonyms. The three databases of dangerous compounds were then merged and a column was added to specifying the type of danger corresponding to each compound. This means that the function does not have to search for dangerous products in three different csv files but only in one.

All the codes used in order to simplify and to merge the initial databases can be found in the folder `code_database`.
  

