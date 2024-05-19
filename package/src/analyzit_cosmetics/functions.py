import csv
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

def search_ingredients(barcode : str,  path_to_database1 = None ) -> list:
    """
    Returns a list that contains the ingredients corresponding to the barcode entered.

    Parameters 
    ----------
    barcode : str
        A number string representing a barcode of a cosmetic.
      
    path_to_database1 : str
        Path to one of our databases which contains barcodes in a row named "code" and 
        ingredients of the barcode product in a row named "ingredients_text".

    Returns 
    -------
    list 
      A list containing all of the ingredients of the cosemtic corrsponding to the barcode.

    Examples 
    --------
    >>> search_ingredients ("12345", database.csv)
    ['A','B','C']
    """
    
    if path_to_database1 is None :
        path_to_database1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'database_products.csv'))
    try:
        df = pd.read_csv(path_to_database1, encoding='utf-8', dtype={'code': str}) # Allows to access the data in the csv file
        row = df[df['code'] == barcode] # Accesses to the values of the barcodes in the csv file
        if not row.empty:  # Check if the barcode has a list of ingredients in the database
            ingredients_str = row['ingredients_text'].iloc[0] # Take into account the first value in the row of the ingredients 
            ingredients = ingredients_str.split(", ") # Make a list out of the series of ingredients which are seprated by a coma
            return ingredients
        else:
            return "No ingredients found for this barcode." # Handles the possibility of not finding ingredients for a barcode
    except Exception as e:
        return f"An error occurred while loading the file or during the search : {e}" # Handles other errors : not finding a file/unsuccessful search

def danger_list(barcode : str,  path_to_database1 = None,  path_to_database2 = None) -> dict:
    """
    Returns a dictionary that contains the dangerous ingredients corresponding to the barcode entered
    with their corresponding types of dangers using the function search_ingredients.

    Parameters
    ----------
    barcode : str
        A number string representing a barcode of a cosmetic.
    path_to_database1 : str
        One of our databases which contains barcodes in a row named "code" and
        ingredients of the barcode product in a row named "ingredients_text".
    path_to_database2 : str
        Another one of our databases which contains names of dangerous compounds in the column "cmpdname",
        synonyms of those compounds in "cmpdsynonym", and their type(s) of dangers in the column "dangers" (Paraben, Carcinogenic, or Endocrine).

    Returns
    -------
    dict
        A dictionary containing all of the dangerous compounds of the cosmetic corresponding to the barcode and their type(s) of danger.

    Examples
    --------
    >>> danger_list("12345", "database1.csv", "database2.csv")
    {'compound1': ['danger1', 'danger2'], 'compound2': ['danger1']}
    """
    if path_to_database1 is None :
        path_to_database1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'database_products.csv'))
    if path_to_database2 is None :
        path_to_database2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'database_dangers.csv'))
    # Uses the function search_ingredients to access the list of ingredients in the barcode database
    ingredients = search_ingredients(barcode, path_to_database1)
    # Checks if search_ingredients returned an error, if so, return the error
    if isinstance(ingredients, str):  
            return ingredients
        
    # Accesses another databse containing chemicals and their dangers
    dangers = pd.read_csv(path_to_database2)
    # Convert all of the names of chemicals and synonyms in lower case so that the comparison succeeds 
    dangers['cmpdname'] = dangers['cmpdname'].str.lower()
    dangers['cmpdsynonym'] = dangers['cmpdsynonym'].str.lower()
    
    # Create a dictionary to stock the potential dangerous compounds and their type(s) of danger
    dangerous_ingredients = {}
    
    # Check all of the ingredients of the list to compare them to the dangerous compounds database and see if they are dangerous
    for ingredient in ingredients:
        ingredient_lower = ingredient.lower()  # Convert the ingredients into lower case 
        
        # Check if ingredients are present in the compound name column
        found = dangers[dangers['cmpdname'] == ingredient_lower]
        
        # If not found, check if ingredients are present in the compound synonym column
        if found.empty:
            found = dangers[dangers['cmpdsynonym'] == ingredient_lower]
        
        # If a dangerous coumpound is found, add it to the dictionary with its type(s) of danger
        if not found.empty:
            dangerous_ingredients[ingredient] = found['dangers'].tolist()

    return dangerous_ingredients


def amount_dangers(dangerous_ingredients : dict , grade_paraben : int, grade_carcinogenic : int, grade_endocrine : int ) -> dict:
    """
    Returns a dictionary that contains the types of dangers and their amount corresponding to a dict of ingredients and dangers 
    using the grades given by the function A COMPLETER

    Parameters 
    ----------
    barcode : str
        Barcode of the product analyzed
      
    grade_paraben, grade_carcinogenic and grade_endocrine : int
        The grades provided by the user which define how the types of dangers will be prioritized.
    
    Returns 
    -------
    dict 
      A dictionary containing all of the types of danger of a list of ingredients and their amount by taking 
      into account how much the user prioritizes them.

    Examples 
    --------
    >>> amount_dangers (dangerous_ingredients)
    {'danger1' : [3] , 'danger2' : [6]}
    """
    
    # Sets the counters to zero before adding to them in function of the dangers encountered
    counting = {
        'Paraben': 0,
        'Carcinogenic': 0,
        'Endocrine': 0
        }
    # Handles the case of an equal priority given by the user to every type of danger
    if grade_paraben == grade_carcinogenic == grade_endocrine : 
         for produit, categories in dangerous_ingredients.items():
            for category in categories:
                  if  'Paraben' in category:
                        counting['Paraben'] += 1
                  elif  'Carcinogenic'  in category:
                        counting['Carcinogenic'] += 1
                  elif 'Endocrine' in category:
                       counting['Endocrine'] += 1
        
    # Handles the case of an unequal priority given by the user to every type of danger (the danger taken into account for each coumpound will be the one with most prority)
    else : 
        grade_max = max(grade_paraben,grade_carcinogenic ,grade_endocrine) # Defines the most important type of danger for the user
        grade_min = min(grade_paraben,grade_carcinogenic ,grade_endocrine) # Defines the least important type of danger for the user
        grades = [grade_paraben, grade_carcinogenic, grade_endocrine]
        med_grade = sum(grades) - grade_min - grade_max # Defines the type of danger that is not the most or least important for the user
        
        # Assigns the most important category
        category_max = "" 
        if grade_max == grade_paraben:
             category_max = "Paraben"
        elif grade_max == grade_carcinogenic:
            category_max = "Carcinogenic"
        elif grade_max == grade_endocrine:
            category_max = "Endocrine"
            
        # Assigns the least important category
        category_min = ""
        if grade_min  == grade_paraben:
            category_min = "Paraben"
        elif grade_min  == grade_carcinogenic:
            category_min = "Carcinogenic"
        elif grade_min  == grade_endocrine:
            category_min = "Endocrine"

        # Assigns category that is not the most or least important 
        category_med = ""
        if med_grade == grade_paraben:
            category_med = "Paraben"
        elif med_grade == grade_carcinogenic:
            category_med = "Carcinogenic"
        elif med_grade == grade_endocrine:
            category_med = "Endocrine"
    
        # For all the compounds of the list, counts the amount of dangerous compounds of each type by prioritizing the most important, the medium important and then the least important category
        for product, categories in dangerous_ingredients.items():
            for category in categories:
                  if category_max in category:
                        counting[category_max] += 1
                  elif  category_med  in category:
                        counting[category_med] += 1
                  elif category_min in category:
                       counting[category_min] += 1

    return counting # Returns the dictionary containing the types of danger and their counts


def coefficient(grade_substance : int)-> int:
    """
    Returns an integer that corresponds to the coefficient of the substance.
    Using the grade of a substance we calculate an integer that is needed to calculate the grade (another function)

    Parameters 
    ----------
    grade_substance : int
        The grade provided by the user for a certain substance within Paraben, Endocrine and Carcinogenic. 
        The grade define the importance of the substance for the user and is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot)
    
    
    Returns 
    -------
    int 
      A integer corresponding to the coefficient of the substance

    Examples 
    --------
    >>> coefficient (3)
    1
    >>> coefficient (5)
    2
    """

    # verifie that the argument (grade_substance) is an integer
    if type(grade_substance) ==int:

        #verifies that the argument is between 1 and 5
        if 1 <=grade_substance <= 5:

            #assigns a different coefficient in each case : if grade=1, 2, 3, 4 and 5
            if grade_substance==1:
                coef=0.5
            if grade_substance==2:
                coef = 0.75
            if grade_substance==3:
                coef=1
            if grade_substance==4:
                coef = 1.5
            if grade_substance==5:
                coef=2
            return coef #the function returns the correct coefficient
        else:
            return("The grade of the selected substance must be between 1 and 5") # message of error when the argument is not between 1 and 5
    else:
        return("The grade of the selected substance must be and integer number between 1 and 5") # message of error when the argument is not an integer


def grading(barcode : str, grade_paraben : int, grade_carcinogenic : int, grade_endocrine : int) -> float:
    """
    Returns a float number corresponding to the garde of the product scanned out of ten. 

    Parameters
    ----------
    barcode : str
        A number string representing a barcode of a cosmetic.
    grade_paraben : int
        A integer corresponding to the importance of paraben for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).
    grade_carcinogenic : int
        A integer corresponding to the importance of carcinogenic products for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).
    grade_endocrine : int
        A integer corresponding to the importance of endocrine for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).

    Returns
    -------
    float
        A float describing the garde of the product out of ten. 

    Examples
    --------
    >>> grading('667556796483', 4, 3, 3)
    1.5
    """
    #Extraction of the dictionary containing the count of each dangerous product (ex: {'Paraben': 3, 'Carcinogenic': 4, 'Endocrine': 0})
    dangers = amount_dangers(danger_list(barcode), grade_paraben, grade_carcinogenic, grade_endocrine)
    
    # Extraction of the count of each dangerous substance and putting them in variables
    paraben_count = dangers.get('Paraben', 0)
    carcinogenic_count = dangers.get('Carcinogenic', 0)
    endocrine_count = dangers.get('Endocrine', 0)
   
    #Calculation of the grade of the product corresponding to the barcode
    grade=10-(coefficient(grade_paraben)*paraben_count)-(coefficient(grade_carcinogenic)*carcinogenic_count)-(coefficient(grade_endocrine)*endocrine_count)
    if grade<0: #Makes the grade go to zero if the calculation above gave an negative grade
        grade=0
        return grade
    else:
        return grade

def commentary(barcode : str,grade_paraben : int, grade_carcinogenic : int, grade_endocrine : int) -> str :
    """
    Returns a float number corresponding to the garde of the product scanned out of ten. 

    Parameters
    ----------
    barcode : str
        A number string representing a barcode of a cosmetic.
    grade_paraben : int
        A integer corresponding to the importance of paraben for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).
    grade_carcinogenic : int
        A integer corresponding to the importance of carcinogenic products for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).
    grade_endocrine : int
        A integer corresponding to the importance of endocrine for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).

    Returns
    -------
    str
        A string commenting on the grade obtained with the function grading

    Examples
    --------
    >>> commentary('667556796483', 4, 3, 3)
    'The product you scanned is bad. The grade of this product is: 1.5'
    """
    
    #Use the function grading to import the garde 
    grade= grading(barcode, grade_paraben, grade_carcinogenic, grade_endocrine)
    
    #Conditions to determine the commetaries of the grades and return the appropriate one.
    if grade==10:
        return f"The product you scanned is very good. The grade of this product is: {grade}"
    elif 7<=grade<=9:
        return f"The product you scanned is good. The grade of this product is: {grade}"
    elif 4<=grade<=6:
        return f"The product you scanned is average. The grade of this product is: {grade}"
    else:
        return f"The product you scanned is bad. The grade of this product is: {grade}"

def initialize_graph_grades() :
    """
    Initializes empty lists : grades_products and index_products to be able to show all the products on the same graph.

    Parameters 
    ----------
    None
    
    Returns 
    -------
    grades_products : list
        Empty list.

    index_products : list
        Empty list.
    """
    grades_products = []
    index_products=[]
    return grades_products,index_products

def graph_grades(barcode : str, grade_paraben : int, grade_carcinogenic : int, grade_endocrine : int, grades_products : list ,index_products : list ): 
    """
    Creates a graph (barplot) that can show all the grades of the ingredients entered and their commentary with colours.

    Parameters 
    ----------
    barcode : str
        A number string representing a barcode of a cosmetic.

    grade_paraben : int
        A integer corresponding to the importance of paraben for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).
        
    grade_carcinogenic : int
        A integer corresponding to the importance of carcinogenic products for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).
        
    grade_endocrine : int
        A integer corresponding to the importance of endocrine for the user. Is between 1 and 5 (between 1 and 5 with 1 being little, 3 medium and 5 a lot).
      
    grades_products : list
        List that stocks all of the barcodes entered to be able to show their grades on the graph.

    index_products : list
        List that stocks all the indexes of the barcodes entered to be able to show how much products are represented in the graph.

    Returns 
    -------
    None
    """
    grade = grading(barcode,grade_paraben, grade_carcinogenic, grade_endocrine) # Gets the grade associated to the barcode entered
    # Ajouter la note et le numéro du produit aux listes
    grades_products.append(grade) # Adds the grade obtained to the list of grades
    index_products.append(len(grades_products))# Adds the index of the barcode to the list of indexes
    
    # Associates a colour corresponding to the commentary of the grade to the barcode
    if grade == 10:
        colour = "green"
    elif 7 <= grade < 10:
        colour = "yellow"
    elif 4 <= grade < 7:
        colour = "orange"
    else:
        colour = "red"
    # Adds a bar of the colour corresponding to the commentary
    plt.bar(index_products[-1], grades_products[-1],color=colour)
    
    # Adds labels to the axes and a title to the barplot
    plt.xlabel('Index of product')
    plt.ylabel('Grade')
    plt.title('Barplot of the grades of your products')
    
    # Defines the units of the axes
    plt.xticks(range(1, len(grades_products) + 1))
    plt.yticks(range(1, 11))

    
