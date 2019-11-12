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


 with base as(select [AuthorName]
                    ,[AuthorMailDomain]
                    ,[Sha]
                    ,ROW_NUMBER() over (partition by [Sha]
                                            order by [EventCreated]) rn
                 from AllCommits
                where [OrgId] is not Null
  ),
      one_commit as(select [AuthorMailDomain]
						   ,count(*) as [Commits >= 1]
				      from (select [AuthorName]
							      ,[AuthorMailDomain]
							      ,count([Sha]) as commits
						      from base
						     where rn = 1
						     group by [AuthorName]
								     ,[AuthorMailDomain]
					        ) t1
				      group by [AuthorMailDomain]
       ),
	  ten_commits as(select [AuthorMailDomain]
					        ,count(*) as [Commits >= 10]
					   from (select [AuthorName]
								   ,[AuthorMailDomain]
								   ,count([Sha]) as commits
							   from base
							  where rn = 1
							  group by [AuthorName]
									   ,[AuthorMailDomain]
							 having count([Sha]) >= 10
							) t2
				     group by [AuthorMailDomain]
       )
select top(50) [OrgName]
               ,tc.[Commits >= 10]
			   ,oc.[Commits >= 1]
  from one_commit oc
  left join ten_commits tc
    on tc.[AuthorMailDomain] = oc.[AuthorMailDomain]
  left join OrganizationsNames orgs
    on orgs.[OrgDomain] = oc.[AuthorMailDomain]
  order by tc.[Commits >= 10] desc;
