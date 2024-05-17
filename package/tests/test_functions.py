import os
import pytest

from src.analyzit_cosmetics import search_ingredients
def test_search_ingredients():
    path_to_database1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'database_products.csv'))
    # Test 1 : if the barcode is found
    assert search_ingredients('3014230002601',path_to_database1) == ['Aqua', 'Hydrogenated Starch Hydrolysate', 'Hydrated Silica', 'Zinc Citrate', 'Sodium Lauryl Sulfate', 'Aroma', 'Cellulose Gum', 'Sodium Fluoride', 'Sodium Saccharin', 'Mentha Arvensis Leaf Oil', 'Mentha Piperita Oil', 'Mentha Spicata Flower/Leaf/Stem Oil', 'CI 42051.'], "Test 1 failed "
    # Test 2 : if the barcode isn't found
    assert search_ingredients('999999', path_to_database1) == "No ingredients found for this barcode.",  "Test 2 failed "
    # Test 3 : if another error occurs ( file not found or search unsucessful)
    assert search_ingredients('123456', 'inexistant_file.csv') == "An error occurred while loading the file or during the search : [Errno 2] No such file or directory: 'inexistant_file.csv'",  "Test 3 failed "

from src.analyzit_cosmetics import danger_list
def test_danger_list():
    path_to_database1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'database_products.csv'))
    path_to_database2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'database_dangers.csv'))
    # Test 1 : if a dangerous compound is found in the list of ingredients (one danger) : 
    assert danger_list ('3014230002601',path_to_database1,path_to_database2) == {'Sodium Fluoride': ['Carcinogenic']}, "Test 1 failed "
    # Test 2 : if a dangerous compound is found in the list of ingredients (various dangers) : 
    assert danger_list ('667556796483', path_to_database1,path_to_database2) == {'stearic acid': ['Carcinogenic'], 'glycerin': ['Carcinogenic'], 'methylparaben': ['Paraben'], 'propylparaben': ['Paraben'], 'butylparaben': ['Carcinogenic, Paraben'], 'benzyl alcohol': ['Carcinogenic'], 'coumarin': ['Carcinogenic']} , "Test 2 failed "
    # Test 3 : in the case where the barcode isn't found in the database : 
    assert danger_list ('999999', path_to_database1,path_to_database2) == "No ingredients found for this barcode." , "Test 3 failed "
    # Test 4 : if one of the csv files isn't found : 
    assert danger_list ('999999', 'inexistant_file1.csv','inexistant_file2.csv') == "An error occurred while loading the file or during the search : [Errno 2] No such file or directory: 'inexistant_file1.csv'", "Test 4 failed "

from src.analyzit_cosmetics import amount_dangers
def test_amount_dangers():
    dangerous_ingredients = {'stearic acid': ['Carcinogenic'], 'glycerin': ['Carcinogenic'], 'methylparaben': ['Paraben'], 'propylparaben': ['Paraben'], 'butylparaben': ['Carcinogenic, Paraben'], 'benzyl alcohol': ['Carcinogenic'], 'coumarin': ['Carcinogenic']}
    # Test 1 : if the user decides to apply the same order of priority for all the types of danger
    assert amount_dangers (dangerous_ingredients,3,3,3) == {'Paraben': 3, 'Carcinogenic': 4, 'Endocrin': 0}, "Test 1 failed"
    # Test 2 : if the user decides to apply different order of priorities, prioritizes the count of the most important type of danger
    assert amount_dangers (dangerous_ingredients,2,5,4) == {'Paraben': 2, 'Carcinogenic': 5, 'Endocrin': 0}, "Test 2 failed"

