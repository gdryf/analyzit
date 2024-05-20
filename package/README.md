<p align="center">
   <img src="https://github.com/gdryf/analyzit/blob/main/package/assets/logo_maj.png" alt="Project Logo" style="display: block; margin-left: auto; margin-right: auto;">
</p>


![Coverage Status](https://github.com/gdryf/analyzit/blob/main/package/assets/coverage-badge.svg)

<h1 align="center">
AnalyzIt
</h1>

<br>


Analysis of the composition of cosmetics, customizable grading system of their dangers and tracking of the grades of products entered by the user.

## 🔥 Usage

```python
from src.analyzit_cosmetics import search_ingredients, danger_list, amount_dangers, coefficient, grading, commentary, graph_grades

# Obtains the grade corresponding to the baarcode of the product
grade_product = grading (barcode, grade_paraben, grade_carcinogenic, grade endocrine)

# Initializes empty lists for the barplot
grades_products = []
index_products = []

# Initiates the barplot, adds the grade of the barcode to it and shows it
plt.figure()
add_grade_graph = graph_grades (barcode, grade_paraben, grade_carcinogenic, grade endocrine)
plt.show()
```

## 👩‍💻 Installation

Create a new environment, you may also give the environment a different name. 

```
conda create -n analyzit_cosmetics python=3.10 
```

```
conda activate analyzit_cosmetics
(conda_env) $ pip install .
```

If you need jupyter lab, install it 

```
(analyzit_cosmetics) $ pip install jupyterlab
```


## 🛠️ Development installation

Initialize Git (only for the first time). 

Note: You should have create an empty repository on `https://github.com:gdryf/analyzit`.

```
git init
git add * 
git add .*
git commit -m "Initial commit" 
git branch -M main
git remote add origin git@github.com:gdryf/analyzit.git 
git push -u origin main
```

Then add and commit changes as usual. 

To install the package, run

```
(analyzit_cosmetics) $ pip install -e ".[test,doc]"
```

### Run tests and coverage

```
(conda_env) $ pip install tox
(conda_env) $ tox
```



