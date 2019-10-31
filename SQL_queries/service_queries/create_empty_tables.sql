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
    ('Microsoft', 'microsoft.com'),
    ('Google', 'google.com'),
    ('Red Hat', 'redhat.com'),
    ('IBM', 'ibm.com'),
    ('Intel', 'intel.com'),
    ('Amazon', 'amazon.com'),
    ('SAP', 'sap.com'),
    ('ThoughtWorks', 'thoughtworks.com'),
    ('Alibaba', 'alibaba-inc.com'),
    ('GitHub', 'github.com'),
    ('Facebook', 'fb.com'),
    ('Apache', 'apache.org'),
    ('Pivotal', 'pivotal.io'),
    ('EPAM', 'epam.com'),
    ('Baidu', 'baidu.com'),
    ('Mozilla', 'mozilla.com'),
    ('Oracle', 'oracle.com'),
    ('Unity Technologies', 'unity3d.com'),
    ('Tencent', 'tencent.com'),
    ('Uber', 'uber.com'),
    ('Yandex', 'yandex-team.ru'),
    ('Shopify', 'shopify.com'),
    ('LinkedIn', 'linkedin.com'),
    ('SUSE', 'suse.com'),
    ('ESRI', 'esri.com'),
    ('Apple', 'apple.com'),
    ('Salesforce', 'salesforce.com'),
    ('VMware', 'vmware.com'),
    ('Adobe', 'adobe.com'),
    ('Andela', 'andela.com'),
    ('Cisco Systems', 'cisco.com'),
    ('WIX', 'wix.com'),
    ('Netflix', 'netflix.com'),
    ('CERN', 'cern.ch'),
    ('Kitware', 'kitware.com'),
    ('ARM', 'arm.com'),
    ('NVidia', 'nvidia.com'),
    ('Travis CI', 'travis-ci.org'),
    ('Liferay', 'liferay.com'),
    ('JetBrains', 'jetbrains.com'),
    ('Osrfoundation' ,'osrfoundation.org'),
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
    ('Renovateapp', 'renovateapp.com'),
    ('Exoplatform', 'exoplatform.com'),
    ('Pyup', 'pyup.io'),
    ('Odoo', 'odoo.com'),
    ('Infosiftr', 'infosiftr.com'),
    ('Shopkeep', 'shopkeep.com'),
    ('Dynatrace', 'dynatrace.com'),
    ('Spryker', 'spryker.com'),
    ('WSO2', 'wso2.com'),
    ('Chef', 'chef.io'),
    ('Datadoghq', 'datadoghq.com'),
    ('Iohk', 'iohk.io'),
    ('Elastic', 'elastic.co'),
    ('Alfresco', 'alfresco.com'),
    ('Nuxeo' ,'nuxeo.com'),
    ('Adguard', 'adguard.com'),
    ('5minds', '5minds.de'),
    ('Couchbase', 'couchbase.com'),
    ('Autonomous', 'autonomous.nyc'),
    ('Com3elles', 'com3elles.com'),
    ('The guardian', 'guardian.co.uk'),
    ('Gradle', 'gradle.com'),
    ('Kaltura', 'kaltura.com'),
    ('SecOps Solutions', 'secops.in'),
    ('Automattic', 'automattic.com'),
    ('Mapbox', 'mapbox.com'),
    ('Scality', 'scality.com'),
    ('Collabora', 'collabora.com'),
    ('HashiCorp', 'hashicorp.com'),
    ('Atomist', 'atomist.com'),
    ('Igalia', 'igalia.com'),
    ('MuleSoft', 'mulesoft.com'),
    ('Palantir', 'palantir.com'),
    ('Puppet', 'puppet.com'),
    ('Shopware', 'shopware.com'),
    ('Brave', 'brave.com'),
    ('D2iQ', 'mesosphere.com'),
    ('Lightcurve', 'lightcurve.io'),
    ('Origin', 'originprotocol.com'),
    ('mongoDB', 'mongodb.com'),
    ('NXP', 'nxp.com'),
    ('Acsone', 'acsone.eu'),
    ('Camunda', 'camunda.com'),
    ('Analog Devices', 'analog.com'),
    ('Decred', 'decred.org'),
    ('Percona', 'percona.com'),
    ('Nextcloud', 'nextcloud.com'),
    ('Tutanota', 'tutanota.com'),
    ('Cockroachlabs', 'cockroachlabs.com'),
    ('Obvious', 'obvious.in'),
    ('Vaadin', 'vaadin.com'),
    ('Stripe', 'stripe.com'),
    ('SiFive', 'sifive.com'),
    ('TI', 'ti.com'),
    ('Bosch', 'bosch.com'),
    ('Confluent', 'confluent.io'),
    ('Indexdata', 'indexdata.com'),
    ('Yahoo', 'yahoo-inc.com'),
    ('Endlessm', 'endlessm.com'),
    ('Balena', 'balena.io'),
    ('MariaDB', 'mariadb.com'),
    ('Shopsys', 'shopsys.com'),
    ('Azavea', 'azavea.com'),
    ('Cloudera', 'hortonworks.com'),
    ('Joyent', 'joyent.com'),
    ('Galera Cluster', 'galeracluster.com'),
    ('Flatiron school', 'flatironschool.com'),
    ('SignalFx', 'signalfx.com'),
    ('mySociety', 'mysociety.org'),
    ('Eficent', 'eficent.com'),
    ('Giant Swarm', 'giantswarm.io'),
    ('Nymea', 'nymea.io'),
    ('Finbourne', 'finbourne.com'),
    ('H2O.ai', 'h2o.ai'),
    ('tweag.io', 'tweag.io'),
    ('Digital Bazaar', 'digitalbazaar.com'),
    ('Instructure', 'instructure.com');
END;