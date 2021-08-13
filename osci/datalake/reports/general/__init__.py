"""Copyright since 2020, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""

from .base import Report, GeneralReportFactory
from .change_ranking import OSCIChangeRanking, OSCIGrowthSpeed, OSCIChangeRankingDTD
from .commits_ranking import OSCICommitsRankingYTD, OSCICommitsRankingMTD, OSCICommitsRankingFactory
from .osci_ranking import OSCIRankingYTD, OSCIRankingMTD, OSCIRankingFactory
from .language_commits_ranking import OSCILanguagesYTD
from .licensed_commits_ranking import OSCILicensesYTD
from .osci_contributors_ranking import OSCIContributorsRankingYTD
from .osci_general_ranking import OSCIGeneralRanking
from .company_contributors_repository_commits import CompaniesContributorsRepository, \
    CompanyContributorsRepositoryCommitsFactory
