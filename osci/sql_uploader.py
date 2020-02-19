"""Copyright since 2019, EPAM Systems

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


import os

from osci.sql_runner import run_query


def upload_to_database(file_path, db_name):
    """
    upload json file to SQL database
    :param file_path: path to json file
    :param db_name: name of target database
    """
    file = os.path.abspath(file_path)

    query = '''begin try
                      begin tran;
                    declare @json nvarchar(max)
                     select @json = bulkcolumn
                       from openrowset(bulk '{}', single_clob) as r
                     insert into GitEvents ([EventId]
                                           ,[EventType]
                                           ,[EventCreated]
                                           ,[RepoId]
                                           ,[ActorId]
                                           ,[OrgId]
                                           )
                     select [EventId]
                           ,[Type]
                           ,[Created_at]
                           ,[RepoId]
                           ,[ActorId]
                           ,[OrgId]
                       from openjson(@json)
                       with ([EventId] bigint '$.id'
                            ,[Type] nvarchar(50) '$.type'
                            ,[Created_at] datetime2(7) '$.created_at'
                            ,[ActorId] bigint '$.actor.id'
                            ,[RepoId] bigint '$.repo.id'
                            ,[OrgId] bigint '$.org.id'
                            ) as gevt

                    insert into Actors([ActorId]
                                      ,[ActorLogin]
                                      ,[ActorUrl]
                                      )
                    select distinct [ActorId]
                                   ,[ActorLogin]
                                   ,[ActorUrl]
                      from openjson(@json)
                      with ([ActorId] bigint '$.actor.id'
                           ,[ActorLogin] nvarchar(100) '$.actor.login'
                           ,[ActorUrl] nvarchar(250) '$.actor.url'
                           ) as gevt
                    where ActorId not in (select ActorId
                                            from Actors)

                    insert into Organizations ([Id]
                                              ,[OrgName]
                                              ,[OrgUrl]
                                              )
                    select distinct [OrgId]
                                   ,[OrgName]
                                   ,[OrgUrl]
                      from openjson(@json)
                      with ([OrgId] bigint '$.org.id'
                           ,[OrgName] nvarchar(250) '$.org.login'
                           ,[OrgUrl] nvarchar(250) '$.org.url'
                           ) as gevt
                     where OrgId not in (select Id
                                           from Organizations)
                       and OrgId is not null

                    insert into Repositories ([Id]
                                             ,[RepoName]
                                             ,[RepoUrl]
                                             ,[OrgId]
                                             )
                    select distinct [RepoId]
                                   ,[RepoName]
                                   ,[RepoUrl]
                                   ,[OrgId]
                      from openjson(@json)
                      with ([RepoId] bigint '$.repo.id'
                           ,[RepoName] nvarchar(250) '$.repo.name'
                           ,[RepoUrl] nvarchar (250) '$.repo.url'
                           ,[OrgId] bigint '$.org.id'
                           )
                     where RepoId not in (select Id
                                            from Repositories)

                    insert into GitCommits ([GitEventId]
                                           ,[RepoId]
                                           ,[Sha]
                                           ,[AuthorName]
                                           ,[AuthorMailDomain]
                                           )
                    select gevt.Id as [GitEventId]
                                     ,gevt.[RepoId]
                                     ,cmd.[Sha]
                                     ,cmd.[AuthorName]
                                     ,SUBSTRING(cmd.AuthorEmail, charindex('@', cmd.AuthorEmail) + 1, LEN(cmd.AuthorEmail) -  charindex('@', cmd.AuthorEmail)) mailDomain
                      from openjson(@json)
                      with ([Id] bigint '$.id'
                           ,[RepoId] bigint '$.repo.id'
                           ,payload nvarchar(max) as JSON
                           ) as gevt
                     cross apply openjson(gevt.payload)
                      with (commits nvarchar(max) as JSON) as pl
                     cross apply openjson(pl.commits)
                      with ([Sha] nvarchar(50) '$.sha'
                           ,[AuthorName] nvarchar(250) '$.author.name'
                           ,[AuthorEmail] nvarchar(250) '$.author.email'
                           ) as cmd;
                    commit tran;
                end try
                begin catch
                    declare @errMsg nvarchar(4000) = error_message();
                    raiserror('%s', 16, 1, @errMsg);
                    rollback tran;
                end catch;'''.format(file)

    run_query(database=db_name, query=query)
