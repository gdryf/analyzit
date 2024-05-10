

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
        df = pd.read_csv(csv_file, encoding='utf-8', dtype={'code': str})
        row = df[df['code'] == barcode]
        if not row.empty:  # Check if the barcode has a list of ingredients in the database
            ingredients_str = row['ingredients_text'].iloc[0] # Take into account the first value in the row of the ingredients 
            ingredients = ingredients_str.split(", ") # Make a list out of the series of ingredients which are seprated by a coma
            return ingredients
        else:
            return "No ingredients found for this barcode." # Handles the possibility of not finding ingredients for a barcode
    except Exception as e:
        return f"An error occurred while loading the file or during the search : {e}" # Handles other errors : not finding a file/unsuccessful searc
