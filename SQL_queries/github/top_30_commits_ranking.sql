/* Copyright since 2019, EPAM Systems

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
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>.
*/


with base as (select [AuthorMailDomain]
                      ,ROW_NUMBER() over (partition by [Sha]
                                              order by [EventCreated]) rn
                from AllCommits
               where [OrgId] is not null)
select top(30) [OrgName]
       ,count(*) Commits
  from base b
  left join OrganizationsNames orgs
    on orgs.[OrgDomain] = b.[AuthorMailDomain]
 where rn = 1
 group by [OrgName]
 order by Commits desc;
