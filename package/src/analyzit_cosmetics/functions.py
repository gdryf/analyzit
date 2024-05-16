

def search_ingredients(barcode : str, csv_file : str) -> list:
    """
    Return a list that contains the ingredients corresponding to the barcode entered.

    Parameters 
    ----------
    barcode : str
      A number string representing a barcode of a cosmetic.

    csv_file : str
      One of our databases which contains barcodes in a row named "code" and 
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
    try:
        df = pd.read_csv(csv_file, encoding='utf-8', dtype={'code': str}) # Allows to access the data in the csv file
        row = df[df['code'] == barcode] # Accesses to the values of the barcodes in the csv file
        if not row.empty:  # Check if the barcode has a list of ingredients in the database
            ingredients_str = row['ingredients_text'].iloc[0] # Take into account the first value in the row of the ingredients 
            ingredients = ingredients_str.split(", ") # Make a list out of the series of ingredients which are seprated by a coma
            return ingredients
        else:
            return "No ingredients found for this barcode." # Handles the possibility of not finding ingredients for a barcode
    except Exception as e:
        return f"An error occurred while loading the file or during the search : {e}" # Handles other errors : not finding a file/unsuccessful search

def danger_list(barcode : str, csv_file1 : str, csv_file2: str) -> dict:
    """
    Returns a dictionary that contains the dangerous ingredients corresponding to the barcode entered 
    with their corresponding types of dangers using the function search_ingredients.

    Parameters 
    ----------
    barcode : str
      A number string representing a barcode of a cosmetic.

    csv_file1 : str
        One of our databases which contains barcodes in a row named "code" and     
        ingredients of the barcode product in a row named "ingredients_text".

    csv_file2 : str    
        Another one of our databases which contains names of dangerous compounds in the column "cmpdname", 
        synonyms of those compounds in "cmpdsynonym" and there type(s) of dangers in the column "dangers" (Paraben, Carcinogenic or Endocrine).

    Returns 
    -------
    dict 
      A dictionary containing all of the dangerous compounds of the cosemtic corrsponding to the barcode and their type(s) of danger.

    Examples 
    --------
    >>> danger_list ("12345", database1.csv, database2.csv)
    {'compound1' : [danger1,danger2] , 'compound2' : [danger1]}
    """
    # Uses the function search_ingredients to access the list of ingredients in the barcode database
    ingredients = search_ingredients(barcode, csv_file1)

    # Checks if search_ingredients returned an error, if so, return the error
    if isinstance(ingredients, str):  
            return ingredients
        
    # Accesses another databse containing chemicals and their dangers
    dangers = pd.read_csv(csv_file2)

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
        else:
            return "No ingredients found for this barcode." # Handles the possibility of not finding ingredients for a barcode
   
