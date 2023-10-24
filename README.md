<p align="center">
  <img src="docs/images/themis_large.png" alt="Opis obrazka">
</p>
<div align="center">
  <h1 style="font-size: 36px;">Temida</h1>
</div>
<p align="justify">
The design of an application that performs arbitrage in the betting market. It uses data of legal bookmakers in Poland in accordance with the document "Mutual betting and gambling over the Internet" published on 24.08.2023 by the Ministry of Finance of the Republic of Poland located at 12 Świętokrzyska Street in Warsaw.

A version of a working application has been made that allows screper implementations for various bookmakers.
#### Features
- [x] A fully functioning environment that supports data scrapers regardless of the number of data scrapers
- [x] A fully functioning scrapers for Fortuna, Betclic, STS and Superbet
- [x] Support of the most popular sports bets
- [x] A module that allows matching events between bookmakers:
  - single Jaccard similarity algorithm (fast but not very efficient - mandated for certain tests)
  - double Jaccard similarity algorithm - it checks the probability of similarity of two pairs of strings representing the names of events at equal bookmakers and then if such a pair reaches a probability greater than 0.6 it checks whether the names of home and away players are similar with a probability of at least 0.5 (a fast and almost flawless method - recommended for production tasks)
  - String matching using the AgglomerativeClustering machine learning algorithm (more information: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html) - slow but very effective. Unfortunately, it is very sensitive to the differences between texts by which it causes a large loss of dnaych. It needs work developing its capabilities
- [x] Data parsers
- [x] Module performing arbitrage calculations on betting data for all sports events
#### Plans for the futures:
- [ ] Mailing messages
- [ ] Improving the speed of scrapers
- [ ] Development of the base of supported bookmakers

## Tests status <img src="https://github.com/dominikteodorczyk/temida/actions/workflows/tox_tests.yml/badge.svg" alt="Badge">
<p align="justify">
Status of unit tests for Python 3.10 on the most recent versions of Ubuntu and Windows. Here is used tox tool for creating envs. Code is also tested for formatting with flake8 before being <code>git push</code> to the remote repository.
</p>

### Installation Instructions
- Make sure you have Python version 3.9 or 3.10 installed (confirmed to work by testing). You can check this by running the following command on the command line:<br>
<code>python --version</code><br>
If Python is not installed or you have an older version, visit the official Python website (https://www.python.org) and follow the installation instructions for your operating system.<br>
- Clone the project repository from GitHub using the command:<br>
<code>git clone https://github.com/dominikteodorczyk/temida.git</code><br>
You can also download the repository as a ZIP file and unzip it on your computer.<br>
- We recommend creating a virtual Python environment to isolate the project's dependencies. You can do this by running the following command:<br>
<code>python -m venv venv</code><br>
This command will create a virtual environment named "venv" in the project directory.<br>
- install the required project dependencies using pip package manager:<br>
<code>pip install -r requirements.txt</code><br>
This command will download and install all the required modules and libraries that the project requires for proper operation. The `requirements.txt` file should be located in the project's root directory and contain a list of dependencies with their versions.<br>
- The project has been successfully installed!<br>
- In case the application displays an error about the wrong version of chromedriver.exe compatible with your browser you can find at : https://chromedriver.chromium.org/downloads
