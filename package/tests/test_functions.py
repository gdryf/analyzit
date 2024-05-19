
import pytest
from src.analyzit_cosmetics import search_ingredients, danger_list, amount_dangers, coefficient, graph_grades
def test_search_ingredients():
    # Test 1 : if the barcode is found
    assert search_ingredients('3014230002601') == ['Aqua', 'Hydrogenated Starch Hydrolysate', 'Hydrated Silica', 'Zinc Citrate', 'Sodium Lauryl Sulfate', 'Aroma', 'Cellulose Gum', 'Sodium Fluoride', 'Sodium Saccharin', 'Mentha Arvensis Leaf Oil', 'Mentha Piperita Oil', 'Mentha Spicata Flower/Leaf/Stem Oil', 'CI 42051.'], "Test 1 failed "
    # Test 2 : if the barcode isn't found
    assert search_ingredients('999999') == "No ingredients found for this barcode.",  "Test 2 failed "
    # Test 3 : if another error occurs ( file not found or search unsucessful)
    assert search_ingredients('123456', 'inexistant_file.csv') == "An error occurred while loading the file or during the search : [Errno 2] No such file or directory: 'inexistant_file.csv'",  "Test 3 failed "
    
def test_danger_list():
    # Test 1 : if a dangerous compound is found in the list of ingredients (one danger) : 
    assert danger_list ('3014230002601') == {'Sodium Fluoride': ['Carcinogenic']}, "Test 1 failed "
    # Test 2 : if a dangerous compound is found in the list of ingredients (various dangers) : 
    assert danger_list ('667556796483') == {'stearic acid': ['Carcinogenic'], 'glycerin': ['Carcinogenic'], 'methylparaben': ['Paraben'], 'propylparaben': ['Paraben'], 'butylparaben': ['Carcinogenic, Paraben'], 'benzyl alcohol': ['Carcinogenic'], 'coumarin': ['Carcinogenic']} , "Test 2 failed "
    # Test 3 : in the case where the barcode isn't found in the database : 
    assert danger_list ('999999') == "No ingredients found for this barcode." , "Test 3 failed "
    # Test 4 : if one of the csv files isn't found : 
    assert danger_list ('999999', 'inexistant_file1.csv','inexistant_file2.csv') == "An error occurred while loading the file or during the search : [Errno 2] No such file or directory: 'inexistant_file1.csv'", "Test 4 failed "

def test_amount_dangers():
    dangerous_ingredients = {'stearic acid': ['Carcinogenic'], 'glycerin': ['Carcinogenic'], 'methylparaben': ['Paraben'], 'propylparaben': ['Paraben'], 'butylparaben': ['Carcinogenic, Paraben'], 'benzyl alcohol': ['Carcinogenic'], 'coumarin': ['Carcinogenic'], 'test' : ['Endocrine']}
    # Test 1 : if the user decides to apply the same order of priority for all the types of danger
    assert amount_dangers (dangerous_ingredients,3,3,3) == {'Paraben': 3, 'Carcinogenic': 4, 'Endocrine': 1}, "Test 1 failed"
    # Test 2 : if the user decides to apply different order of priorities, prioritizes the count of the most important type of danger
    assert amount_dangers (dangerous_ingredients,2,5,4) == {'Paraben': 2, 'Carcinogenic': 5, 'Endocrine': 1}, "Test 2 failed"
    # Test 3 : other test to complete coverage (if the minimum grade is given to "Carcinogenic" and maximum garde to "Endocrine")
    assert amount_dangers (dangerous_ingredients,4,1,5) == {'Paraben': 3, 'Carcinogenic': 4, 'Endocrine': 1}, "Test 3 failed"
    # Test 4 : other test to complete coverage (if the medium grade is given to "Carcinogenic" and minimum grade given to "Endocrine")
    assert amount_dangers (dangerous_ingredients,4,2,1) =={'Paraben': 3, 'Carcinogenic': 4, 'Endocrine': 1}, "Test 4 failed"

def test_coefficient():
    #Test 1 : if the user enters the right value (integer between 1 and 5)
    assert coefficient(1) == 0.5, "Test 1 failed"
    assert coefficient(2) == 0.75, "Test 1 failed"
    assert coefficient(3) == 1, "Test 1 failed"
    assert coefficient(4) == 1.5, "Test 1 failed"
    assert coefficient(5) == 2, "Test 1 failed"
    #Test 2 : if the user enters an integer but out of range
    assert coefficient(0) == "The grade of the selected substance must be between 1 and 5", "Test 2 failed"
    assert coefficient(6) == "The grade of the selected substance must be between 1 and 5", "Test 2 failed"
    #Test 3 : if the user enters an argument of the wrong type (float, string, none)
    assert coefficient(3.5) == "The grade of the selected substance must be and integer number between 1 and 5", "Test 3 failed"
    assert coefficient("3")== "The grade of the selected substance must be and integer number between 1 and 5", "Test 3 failed"
    assert coefficient(None)== "The grade of the selected substance must be and integer number between 1 and 5", "Test 3 failed"

def test_graph_grades():
    # Creates the empty lists grades_products and index_products
    grades_products = []
    index_products = []
    
    graph_grades("855553005305", 3, 4, 5, grades_products, index_products)
    
    # Checks if the lists are filled correctly
    assert len(grades_products) == 1, "grades_products should contain 1 item."
    assert len(index_products) == 1, "index_products should contain 1 item."
    assert 1 <= grades_products[0] < 11, "The grade should be between 1 and 10."
    assert index_products[0] == 1, "The index of the product should be 1."
    # Checks if the colour of the bar is correctly added
    bars = plt.gca().patches
    bar_color = bars[0].get_facecolor()
    expected_color = "green"
    assert bar_color == expected_color, f"The color should be {expected_color} but got {bar_color}."

