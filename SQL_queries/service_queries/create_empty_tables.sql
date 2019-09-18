IF OBJECT_ID('Actors', 'U') IS NULL CREATE TABLE Actors (
	 ActorId BIGINT
	,ActorLogin NVARCHAR(250) NULL
	,ActorUrl NVARCHAR(250) NULL
	);

IF OBJECT_ID('Repositories', 'U') IS NULL CREATE TABLE Repositories (
	 Id BIGINT
	,RepoName NVARCHAR(250) NULL
	,RepoUrl NVARCHAR(250) NULL
	,OrgId BIGINT NULL
	);

IF OBJECT_ID('Organizations', 'U') IS NULL CREATE TABLE Organizations (
	 Id BIGINT
	,OrgName NVARCHAR(250) NULL
	,OrgUrl NVARCHAR(250) NULL
	);

IF OBJECT_ID('GitEvents', 'U') IS NULL CREATE TABLE GitEvents (
	 EventId BIGINT
	,EventType NVARCHAR(50)
	,EventCreated DATETIME2(7)
	,RepoId BIGINT
	,ActorId BIGINT
	,OrgId BIGINT NULL
	);

IF OBJECT_ID('GitCommits', 'U') IS NULL CREATE TABLE GitCommits (
	 GitEventId BIGINT
	,RepoId BIGINT
	,Sha NVARCHAR(100) NULL
	,AuthorName NVARCHAR(250) NULL
	,AuthorMailDomain NVARCHAR(250) NULL
	);

IF OBJECT_ID('OrganizationsNames', 'U') IS NULL
BEGIN
    CREATE TABLE OrganizationsNames(
         OrgName nvarchar(250)
        ,OrgDomain nvarchar(250)
        );

    INSERT INTO OrganizationsNames(OrgName, OrgDomain)
    VALUES
    ('Cisco Systems', 'cisco.com'),
    ('Unity Technologies', 'unity3d.com'),
    ('LinkedIn', 'linkedin.com'),
    ('Shopify', 'shopify.com'),
    ('Tencent', 'tencent.com'),
    ('Uber', 'uber.com'),
    ('Andela', 'andela.com'),
    ('Apple', 'apple.com'),
    ('ESRI', 'esri.com'),
    ('Adobe', 'adobe.com'),
    ('Baidu', 'baidu.com'),
    ('ThoughtWorks', 'thoughtworks.com'),
    ('SUSE', 'suse.com'),
    ('VMware', 'vmware.com'),
    ('Mozilla', 'mozilla.com'),
    ('Alibaba', 'alibaba-inc.com'),
    ('Salesforce', 'salesforce.com'),
    ('Oracle', 'oracle.com'),
    ('Amazon', 'amazon.com'),
    ('SAP', 'sap.com'),
    ('GitHub', 'github.com'),
    ('Pivotal', 'pivotal.io'),
    ('Facebook', 'fb.com'),
    ('Intel', 'intel.com'),
    ('Red Hat', 'redhat.com'),
    ('Google', 'google.com'),
    ('Yandex', 'yandex-team.ru'),
    ('IBM', 'ibm.com'),
    ('EPAM', 'epam.com'),
    ('Microsoft', 'microsoft.com'),
    ('WIX', 'wix.com'),
    ('Netflix', 'netflix.com'),
    ('CERN', 'cern.ch'),
    ('Kitware', 'kitware.com'),
    ('ARM', 'arm.com'),
    ('NVidia', 'nvidia.com'),
    ('Travis CI', 'travis-ci.org'),
    ('Liferay', 'liferay.com'),
    ('Open Robotics', 'osrfoundation.org'),
    ('Docker', 'docker.com'),
    ('Sonarsource', 'sonarsource.com'),
    ('Linaro', 'linaro.org'),
    ('Cloudbees', 'cloudbees.com'),
    ('Canonical', 'canonical.com'),
    ('Camptocamp', 'camptocamp.com'),
    ('Samsung', 'samsung.com'),
    ('Huawei', 'huawei.com'),
    ('AMD', 'amd.com'),
    ('Ericsson', 'ericsson.com'),
    ('Capgemini', 'capgemini.com'),
    ('Talend', 'talend.com'),
    ('BBC', 'bbc.co.uk'),
    ('Twitter', 'twitter.com'),
    ('Sonymobile', 'sonymobile.com'),
    ('Autodesk', 'autodesk.com'),
    ('JetBrains', 'jetbrains.com');
END;