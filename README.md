# SMR-X-H2

## Application
- To use the Application the only Output folder can be downloaded and used independently.
- In this folder the main.exe can be started to launch the application.
- In the _Internal folder, the 3 Excels can be found. In this Excel, the Data can be modified according to each usage.
- The 3 following Excel are read from the script, and can be modified.
- The criteria Ranking Excel gives the weighting for each Criterion. The Data SMR Sheet will have a list of all the projects and the calculation of each criterion for each project. The electrolyser datasheet reads the electrolyser technical data and criteria according to each technology.

Criteria Ranking.xlsx
DATA SMR.xlsx
Electrolyser data.xlsx

Importantly, the name of the criteria must not be modified as well as the first rows of every sheet. If a project has to be added, it should be added at the bottom of the existing list.







## Python setup

- Create a venv: `python3 -m venv venv`
- Source the venv: `/venv/Scripts/activate.ps1`
- Install the requirements: `pip install -r requirements.txt`

