![OSCI Logo](https://github.com/epam/OSCI/blob/master/images/OSCI_Logo.png)
# OSCI, the Open Source Contributor Index

## NEWS UPDATE (March 10th 2020)

The OSCI ranking has now been updated with the data for February 2020.  
The latest ranking can be viewed on the EPAM SolutionsHub [OSCI page](https://solutionshub.epam.com/osci).
Alternatively the updated ranking can be downloaded (Excel format) from our [Archive folder](Archive): [2020.02 OSCI Ranking.xlsx](Archive/2020.02_OSCI_Ranking.xlsx).

We have also published the [OSCI 2016-2019 Deep Dive](https://solutionshub.epam.com/blog/post/open-source-contributor-index) which analyses the OSCI ranking changes from 2016 until now.

## What is OSCI?

* OSCI ranks corporate contributions to open source based on the organization’s number of Active Contributors to GitHub
* OSCI also tracks the Total Community of open source contributors for these companies
* The OSCI rankings are published monthly to dynamically track corporate contributions to GitHub. The latest result can be found at EPAM SolutionsHub website's [OSCI page](https://solutionshub.epam.com/osci)

## How does OSCI work?

* OSCI analyses push event data from [GH Archive](https://www.gharchive.org/)
* The Author Email address field in the commit event data is used to identify the organization to which the commit author belongs
* OSCI measures the Active Community (10+ commits) and the Total Community (1+ commit) at each organization
* Analysis is done for the current year-to-date
* OSCI’s algorithm is transparently published as an open source project on GitHub


![GitHub OSCI Schematic Diagram](https://github.com/epam/OSCI/blob/master/images/GitHub_OSCI_Schematic.png)

## How did we decide on the ranking logic?

We realize that there are many approaches which could be used to develop this ranking. We experimented extensively with these before arriving at the logic now used.

We concluded the Author's Email Domain in the Push Event data is the most reliable way to identify the organization to which a commit author belongs. It is a single unambiguous identifier. 
It is true that many people on GitHub do not use the email address of their employer or keep it private, but it is still a more reliable single measure compared with alternatives.  The org of the repo is not a good measure of the employer of an individual because the employees of most companies maintain projects in multiple GitHub orgs.

We concluded that 10+ commits in a year - while arbitrary - is a reasonable measure of whether a person is an active contributor to GitHub. 
It is interesting to compare this with the size of the broader community at an organization - this is why we also record the number of people with just 1 or more commits in the time period.

We decided to base the ranking on the number of people making commits, rather than the number of commits.  The GitHub push event data includes large numbers of pushes made by automated processes using an email domain from an organization. Counting the number of pushes is not a good measure of the community at an organization, when the results are considerably skewed by these automated processes. 

Our technical design assessed multiple source of data and we concluded that [GHArchive](https://www.gharchive.org/) is best suited for our needs, based on ease of access to the data, the amount of data it records, and the size of the data. 
[GHTorrent](http://ghtorrent.org/) is also very interesting for  future use, since it contains a richer set of data, however the data sizes are considerably larger which drove our decision to go with GHArchive.

## What does OSCI not do?

OSCI does not include educational and research institutions, contributions from free email providers, etc. The focus is on commercial organizations.

## Prior work in this area

Our inspiration for OSCI is the work done earlier in the Open Source community, so we wish to give credit to these:
* GitHub published an analysis for 2016 which included the organizations with the most open source contributors https://octoverse.github.com/2016/. GitHub have also published similar studies in 2017 and 2018.
* Felipe Hoffa published a detailed analysis of 2017 data at https://medium.freecodecamp.org/the-top-contributors-to-github-2017-be98ab854e87. Felipe's logic used email domain to identify organizations, counted commits only to projects with more than 20 stars during the period, and counted users with more than 3 pushes during the period. Further details are available in the article.
* Fil Maj also analysed 2017 data and counted users with 10 or more commits during the period https://www.infoworld.com/article/3253948/who-really-contributes-to-open-source.html


## Where can I see the latest rankings
This project is sponsored by EPAM Systems and the latest results are visible on the EPAM SolutionsHub [OSCI page](https://solutionshub.epam.com/osci). The results will be updated and published each month.

## How I can contribute to OSCI
If you would like to contribute to OSCI, please take a look at our guidelines [here.](https://github.com/epam/OSCI/blob/master/CONTRIBUTING.md)

## What if your think your organization is missing or you believe there is an error in our logic
This is a new project. We are more than happy to listen to any feedback which will help us improve.
Contact us at OSCI@epam.com

## Technical Note
We built OSCI this an Azure cloud environment using Azure SQL Server. The code published here on GitHub does not require the Azure cloud, however in the current version MS SQL Server is required. Our future plans include support for an open source database.

# Instructions for using the OSCI code

These scripts are for downloading data from gharchive.org, processing and loading to the SQL Server.

1) Install MS SQL Server.

2) Create a file `local.yml` (by default this file added to .gitignore) in the directory [`configs`](osci/config/files). 
A sample file [`default.yml`](osci/config/files/default.yml) is included, please don't change values in this file
3) Fill fields "year" and "month" in function "get_month_data('year', 'month')" in the file 
   file_loader.py if you want to load data for a specific month.  Use get_year('year') for loading data for whole year.
   For example: 
        
        get_month_data('2019', '05')
        
        get_year('2019')
   
   If necessary, repeat this function for other months or years.

4) Finally run script file_loader.py and wait for successful script execution. It can take some time to download and transform the data.

Once the data is prepared, you can generate reports as shown below. The reports will be generated on all the downloaded data in the AllCommits table. So to make a report for 2019 - for example - download all the 2019 data as described above.

    top_employees_combined.sql - the top 50 companies ordered by employees with 10+ commits and also showing count of employees with 1+ commit. 
    top_commits_ranking.sql - the count of commits per company.
    
    
# License
OSCI is GNU General Public License v3.0.
