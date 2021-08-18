![OSCI Logo](images/OSCI_Logo.png)
# OSCI, the Open Source Contributor Index

## What is OSCI?

* OSCI ranks corporate contributions to open source based on the organization’s number of Active Contributors to GitHub
* OSCI also tracks the Total Community of open source contributors for these companies
* The OSCI rankings are published monthly to dynamically track corporate contributions to GitHub. The latest result can be found at EPAM SolutionsHub website's [OSCI page](https://opensourceindex.io/)

## [News update](news.md)
### [July 12th, 2021](news.md#july-12th-2021)

The OSCI ranking has now been updated with the data for [**June 2021**](https://opensourceindex.io/)

The table shows the OSCI ranking for GitHub activity in June 2021. The leading organisations remain consistent once again this month and the overall level of activity has stabilised approaching second half of the year. In addition Amazon and IBM are progressing well above their closest neighbours in growth figures this month.

[Previous updates](news.md)


## How does OSCI work?

* OSCI analyses push event data from [GH Archive](https://www.gharchive.org/)
* The Author Email address field in the commit event data is used to identify the organization to which the commit author belongs
* OSCI measures the Active Community (10+ commits) and the Total Community (1+ commit) at each organization
* Analysis is done for the current year-to-date
* OSCI’s algorithm is transparently published as an open source project on GitHub


![GitHub OSCI Schematic Diagram](images/OSCI_Schematic_Architecture.png)

## OSCI Versioning :newspaper:
We decided to use special versioning `(<year>.<month>.<number of patch >)` e.g. `2021.05.0`. This will provide us with a
clearer understanding of the relevance of the product.  
Also, date of 
[adding a new company](#how-can-i-add-a-company-which-is-missing-from-the-osci-ranking) is very important and versioning 
releases depending on the date looks more logical.  
This is supposed to be a monthly update of the release.


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
This project is created by EPAM Systems and the latest results are visible on the [OSCI page](https://opensourceindex.io/). The results will be updated and published each month.

## How I can contribute to OSCI
If you would like to contribute to OSCI, please take a look at our guidelines [here.](CONTRIBUTING.md)

## What if your think your organization is missing or you believe there is an error in our logic
If your organization is missing from our ranking then simply follow the instructions below to modify the companies filter and add your own organisation. We're also more than happy to listen to any feedback you have that may help us to improve. Contact us at [OSCI@epam.com](mailto:OSCI@epam.com) to share your feedback and raise any questions.

## How can I add a company which is missing from the OSCI ranking
The goal of the OSCI is to rank the GitHub contributions by companies (commercial organizations).

In order to add a company to the OSCI ranking, do the following:

1) Check whether the organization you propose to add matches our definition of a company:
   - is not an educational, governmental, non-profit or research institution;
   - is not a free-mail, like gmail.com, yahoo.com, hotmail.com, etc;
   - is a registered, commercial company;
   - a simple "rule of thumb" - does the organization's website sell a product or service? If not, it is probably not a company by our definition.

1) Create a new pull request.

1) Go to company domain match list ([company_domain_match_list.yaml](osci/preprocess/match_company/company_domain_match_list.yaml))

1) Confirm that the company you wish to add is not listed.

1) Add the **main domain** of the company and the company name to the table. For example:
    ```yaml
    - company: Facebook
      domains:
        - fb.com
      regex:
    ```     
1) If the company has more than 1 email domain for its employees, add all of them to block `domains` (or `regex` for using regular expression). For example:
    ```yaml
    - company: Facebook
      domains:
        - fb.com
        - facebook.com
      regex:
        - ^.*\.fb\.com$
        - ^.*\.facebook\.com$
    ```
1) Select the industry to which your company belongs from the following list:
   - Banking & Financial Services;
   - Government, Public Sector & Non-Profits;
   - Energy & Utilities;
   - Healthcare;
   - Technology;
   - Media & Telecoms;
   - Other (please specify);

   For example:
   ```yaml
   - company: Facebook
     domains:
       - fb.com
       - facebook.com
     regex:
       - ^.*\.fb\.com$
       - ^.*\.facebook\.com$
     industry: Media & Telecoms
   ```

We will review your pull request and if it matches our requirements, we will merge it.  
It's important to add at **the start
of the month** a new company, because the rating depends on previous data, i.e. data for the beginning of the month.
Furthermore, this will lead to OSCI release consistency.

# QuickStart
## Technical Note
We built OSCI this an Azure cloud environment using Azure DataFactory, Azure Function and Azure HDInsight. 
The code published here on GitHub does not require the Azure cloud. You can reproduce everything in the corresponding instruction with the CLI (command line interface).
## Installation
1) Clone repository
    ```shell script
         git clone https://github.com/epam/OSCI.git
    ```
1) Go to project directory
    ```shell script
         cd OSCI
    ```
1) Install requirements
    ```shell script
         pip install -r requirements.txt
   ```

## Configuration
Create a file `local.yml` (by default this file added to .gitignore) in the directory [`osci/config/files`](osci/config/files). 
A sample file [`default.yml`](osci/config/files/default.yml) is included, please don't change values in this file

## Sample run
1) Run script to download data from archive (for example for 01 January 2020)
    ```shell script
         python3 osci-cli.py get-github-daily-push-events -d 2020-01-01
    ```
1) Run script to add company field (matched by domain) (for example for 01 January 2020)
    ```shell script
         python3 osci-cli.py process-github-daily-push-events -d 2020-01-01
    ```
1) Run script to add company field (matched by domain) (for example for 01 January 2020)
    ```shell script
         python3 osci-cli.py daily-osci-rankings -td 2020-01-02
    ```
  
# License
OSCI is licensed under the [GNU General Public License v3.0](LICENSE).
