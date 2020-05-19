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


IF OBJECT_ID('AllCommits', 'U') IS NOT NULL DROP TABLE AllCommits;

begin try
    begin tran;
   select ge.EventCreated
         ,ge.RepoId
         ,ge.OrgId
         ,gc.Sha
         ,gc.AuthorName
         ,gc.AuthorMailDomain
     into AllCommits
     from GitCommits gc
     join GitEvents ge
       on ge.EventId = gc.GitEventId
    where ge.EventType = 'PushEvent'
      and OrgId is not NULL
      and (
    AuthorMailDomain = 'microsoft.com' or AuthorMailDomain like '%.microsoft.com' or
    AuthorMailDomain = 'google.com' or AuthorMailDomain like '%.google.com' or
    AuthorMailDomain = 'redhat.com' or AuthorMailDomain like '%.redhat.%' or
    AuthorMailDomain = 'ibm.com' or AuthorMailDomain like '%.ibm.com' or
    AuthorMailDomain = 'intel.com' or AuthorMailDomain like '%.intel.com' or
    AuthorMailDomain = 'amazon.com' or AuthorMailDomain like '%.amazon.com' or
    AuthorMailDomain = 'sap.com' or AuthorMailDomain like '%.sap.%' or
    AuthorMailDomain = 'thoughtworks.com' or AuthorMailDomain like '%.thoughtworks.com' or
    AuthorMailDomain = 'alibaba-inc.com' or AuthorMailDomain like '%.alibaba-inc.com' or
    AuthorMailDomain = 'aliyun.com' or AuthorMailDomain like '%.aliyun.com' or
    AuthorMailDomain = 'github.com' or AuthorMailDomain = 'dependabot.com' or
    AuthorMailDomain = 'facebook.com' or AuthorMailDomain like '%.facebook.com' or
    AuthorMailDomain = 'fb.com' or AuthorMailDomain like '%.fb.com' or
    AuthorMailDomain = 'tencent.com' or AuthorMailDomain like '%.tencent.com' or
    AuthorMailDomain = 'pivotal.io' or AuthorMailDomain like '%.pivotal.io' or
    AuthorMailDomain = 'springframework.org' or
    AuthorMailDomain = 'epam.com' or AuthorMailDomain like '%.epam.com' or
    AuthorMailDomain = 'baidu.com' or AuthorMailDomain like '%.baidu.com' or
    AuthorMailDomain = 'mozilla.com' or AuthorMailDomain like '%.mozilla.%' or AuthorMailDomain like 'mozilla.%' or
    AuthorMailDomain = 'oracle.com' or AuthorMailDomain like '%.oracle.com' or
    AuthorMailDomain = 'unity3d.com' or AuthorMailDomain like '%.unity3d.com' or
    AuthorMailDomain = 'uber.com' or AuthorMailDomain like '%.uber.com' or
    AuthorMailDomain = 'yandex-team.ru' or AuthorMailDomain like '%.yandex-team.ru' or
    AuthorMailDomain = 'shopify.com' or AuthorMailDomain like '%.shopify.com' or
    AuthorMailDomain = 'linkedin.com' or AuthorMailDomain like '%.linkedin.com' or
    AuthorMailDomain = 'suse.com' or AuthorMailDomain like '%.suse.%' or AuthorMailDomain like 'suse.%' or
    AuthorMailDomain = 'esri.com' or AuthorMailDomain like '%.esri.%' or AuthorMailDomain like 'esri.%' or
    AuthorMailDomain = 'apple.com' or AuthorMailDomain like '%.apple.com' or
    AuthorMailDomain = 'salesforce.com' or AuthorMailDomain like '%.salesforce.com' or
    AuthorMailDomain = 'vmware.com' or AuthorMailDomain like '%.vmware.com' or
    AuthorMailDomain = 'adobe.com' or AuthorMailDomain like '%.adobe.com' or
    AuthorMailDomain = 'andela.com' or AuthorMailDomain like '%.andela.com' or
    AuthorMailDomain = 'cisco.com' or AuthorMailDomain like '%.cisco.com' or
    AuthorMailDomain = 'wix.com' or AuthorMailDomain like '%.wix.com' or
    AuthorMailDomain = 'netflix.com' or AuthorMailDomain like '%.netflix.com' or
    AuthorMailDomain = 'kitware.com' or AuthorMailDomain like '%.kitware.com' or AuthorMailDomain like '%.kitware.%' or
    AuthorMailDomain = 'arm.com' or AuthorMailDomain like '%.arm.com' or AuthorMailDomain like '%.arm.com.%' or
    AuthorMailDomain = 'nvidia.com' or AuthorMailDomain like '%.nvidia.com' or AuthorMailDomain like '%.nvidia.com.%' or
    AuthorMailDomain = 'travis-ci.org' or AuthorMailDomain like 'travis-ci.%' or
    AuthorMailDomain = 'liferay.com' or
    AuthorMailDomain = 'jetbrains.com' or
    AuthorMailDomain = 'docker.com' or AuthorMailDomain like 'docker.%' or
    AuthorMailDomain = 'sonarsource.com' or
    AuthorMailDomain = 'linaro.org' or
    AuthorMailDomain = 'cloudbees.com' or
    AuthorMailDomain = 'canonical.com' or
    AuthorMailDomain = 'camptocamp.com' or
    AuthorMailDomain = 'samsung.com' or AuthorMailDomain like '%.samsung.com' or
    AuthorMailDomain = 'huawei.com' or
    AuthorMailDomain = 'amd.com' or
    AuthorMailDomain = 'ericsson.com' or
    AuthorMailDomain = 'capgemini.com' or AuthorMailDomain like '%.capgemini.com' or
    AuthorMailDomain = 'talend.com' or
    AuthorMailDomain = 'bbc.co.uk' or
    AuthorMailDomain = 'twitter.com' or
    AuthorMailDomain = 'sonymobile.com' or
    AuthorMailDomain = 'autodesk.com' or
    AuthorMailDomain = 'renovateapp.com' or
    AuthorMailDomain = 'exoplatform.com' or AuthorMailDomain like '%.exoplatform.org' or
    AuthorMailDomain = 'pyup.io' or
    AuthorMailDomain = 'odoo.com' or AuthorMailDomain like '%.odoo.com' or
    AuthorMailDomain = 'infosiftr.com' or
    AuthorMailDomain = 'shopkeep.com' or
    AuthorMailDomain = 'dynatrace.com' or AuthorMailDomain like '%.dynatrace.com' or
    AuthorMailDomain = 'dynatrace.org' or AuthorMailDomain like '%.dynatrace.org' or
    AuthorMailDomain = 'spryker.com' or
    AuthorMailDomain = 'wso2.com' or AuthorMailDomain = 'wso2.org' or
    AuthorMailDomain = 'chef.io' or
    AuthorMailDomain = 'datadoghq.com' or
    AuthorMailDomain = 'iohk.io' or
    AuthorMailDomain = 'elastic.co' or AuthorMailDomain like '%.elastic.co' or
    AuthorMailDomain = 'alfresco.com' or AuthorMailDomain like '%.alfresco.com' or
    AuthorMailDomain = 'nuxeo.com' or
    AuthorMailDomain = 'adguard.com' or
    AuthorMailDomain = 'openrobotics.org' or AuthorMailDomain = 'osrfoundation.org' or
    AuthorMailDomain = '5minds.de' or AuthorMailDomain like '%.5minds.de' or
    AuthorMailDomain = 'couchbase.com' or AuthorMailDomain like '%.couchbase.com' or
    AuthorMailDomain = 'autonomous.nyc' or
    AuthorMailDomain = 'com3elles.com' or
    AuthorMailDomain = 'guardian.co.uk' or
    AuthorMailDomain = 'gradle.com' or AuthorMailDomain = 'gradle.org' or
    AuthorMailDomain = 'kaltura.com' or AuthorMailDomain = 'kaltura.org' or
    AuthorMailDomain = 'secops.in' or
    AuthorMailDomain = 'automattic.com' or
    AuthorMailDomain = 'mapbox.com' or AuthorMailDomain like '%.mapbox.com' or
    AuthorMailDomain = 'scality.com' or
    AuthorMailDomain = 'collabora.com' or AuthorMailDomain = 'collabora.co.uk' or
    AuthorMailDomain = 'hashicorp.com' or AuthorMailDomain = 'hashicorp.co' or AuthorMailDomain = 'hashicorp.io' or
    AuthorMailDomain = 'atomist.com' or
    AuthorMailDomain = 'igalia.com' or
    AuthorMailDomain = 'mulesoft.com' or
    AuthorMailDomain = 'palantir.com' or
    AuthorMailDomain = 'puppet.com' or AuthorMailDomain like '%.puppet.com' or
    AuthorMailDomain = 'shopware.com' or AuthorMailDomain = 'shopware.de' or
    AuthorMailDomain = 'brave.com' or
    AuthorMailDomain = 'mesosphere.com' or AuthorMailDomain = 'mesosphere.io' or
    AuthorMailDomain = 'lightcurve.io' or
    AuthorMailDomain = 'originprotocol.com' or
    AuthorMailDomain = 'mongodb.com' or
    AuthorMailDomain = 'nxp.com' or AuthorMailDomain like '%.nxp.com' or
    AuthorMailDomain = 'acsone.eu' or
    AuthorMailDomain = 'camunda.com' or
    AuthorMailDomain = 'analog.com' or
    AuthorMailDomain = 'decred.org' or
    AuthorMailDomain = 'percona.com' or AuthorMailDomain like '%.percona.com' or
    AuthorMailDomain = 'nextcloud.com' or
    AuthorMailDomain = 'tutanota.com' or AuthorMailDomain = 'tutanota.de' or
    AuthorMailDomain = 'cockroachlabs.com' or
    AuthorMailDomain = 'obvious.in' or
    AuthorMailDomain = 'vaadin.com' or AuthorMailDomain like '%.vaadin.com' or
    AuthorMailDomain = 'stripe.com' or
    AuthorMailDomain = 'sifive.com' or
    AuthorMailDomain = 'ti.com' or
    AuthorMailDomain = 'bosch-si.com' or AuthorMailDomain = 'bosch.com' or AuthorMailDomain like '%.bosch.com' or
    AuthorMailDomain = 'confluent.io' or AuthorMailDomain = 'confluent.com' or
    AuthorMailDomain = 'indexdata.com' or AuthorMailDomain = 'indexdata.dk' or
    AuthorMailDomain = 'yahoo-inc.com' or
    AuthorMailDomain = 'endlessm.com' or
    AuthorMailDomain = 'balena.io' or
    AuthorMailDomain = 'mariadb.com' or AuthorMailDomain = 'mariadb.org' or
    AuthorMailDomain = 'shopsys.com' or AuthorMailDomain = 'shopsys.cz' or
    AuthorMailDomain = 'azavea.com' or
    AuthorMailDomain = 'hortonworks.com' or AuthorMailDomain like '%.hortonworks.com' or
    AuthorMailDomain = 'joyent.com' or
    AuthorMailDomain = 'galeracluster.com' or
    AuthorMailDomain = 'flatironschool.com' or
    AuthorMailDomain = 'signalfx.com' or
    AuthorMailDomain = 'mysociety.org' or
    AuthorMailDomain = 'eficent.com' or
    AuthorMailDomain = 'giantswarm.io' or
    AuthorMailDomain = 'nymea.io' or
    AuthorMailDomain = 'finbourne.com' or
    AuthorMailDomain = 'h2o.ai' or AuthorMailDomain = 'h2oai.com' or
    AuthorMailDomain = 'tweag.io' or
    AuthorMailDomain = 'digitalbazaar.com' or
    AuthorMailDomain = 'instructure.com' or
    AuthorMailDomain = 'khubla.com'
    );

    update AllCommits set AuthorMailDomain = 'microsoft.com' where AuthorMailDomain like '%.microsoft.com';
    update AllCommits set AuthorMailDomain = 'google.com' where AuthorMailDomain like '%.google.com';
    update AllCommits set AuthorMailDomain = 'redhat.com' where AuthorMailDomain like '%.redhat.%';
    update AllCommits set AuthorMailDomain = 'ibm.com' where AuthorMailDomain like '%.ibm.%' or AuthorMailDomain like 'ibm.%';
    update AllCommits set AuthorMailDomain = 'intel.com' where AuthorMailDomain like '%.intel.com';
    update AllCommits set AuthorMailDomain = 'amazon.com' where AuthorMailDomain like '%.amazon.com';
    update AllCommits set AuthorMailDomain = 'sap.com' where AuthorMailDomain like '%.sap.%';
    update AllCommits set AuthorMailDomain = 'thoughtworks.com' where AuthorMailDomain like '%.thoughtworks.com';
    update AllCommits set AuthorMailDomain = 'alibaba-inc.com' where AuthorMailDomain like '%.alibaba-inc.com' or AuthorMailDomain = 'aliyun.com' or AuthorMailDomain like '%.aliyun.com';
    update AllCommits set AuthorMailDomain = 'github.com' where AuthorMailDomain = 'dependabot.com';
    update AllCommits set AuthorMailDomain = 'fb.com' where AuthorMailDomain = 'facebook.com' or AuthorMailDomain like '%.facebook.com' or AuthorMailDomain like '%.fb.com';
    update AllCommits set AuthorMailDomain = 'tencent.com' where AuthorMailDomain like '%.tencent.com';
    update AllCommits set AuthorMailDomain = 'pivotal.io' where AuthorMailDomain like '%.pivotal.io' or AuthorMailDomain = 'springframework.org';
    update AllCommits set AuthorMailDomain = 'epam.com' where AuthorMailDomain like '%.epam.com';
    update AllCommits set AuthorMailDomain = 'baidu.com' where AuthorMailDomain like '%.baidu.com';
    update AllCommits set AuthorMailDomain = 'mozilla.com' where AuthorMailDomain like '%.mozilla.%' or AuthorMailDomain like 'mozilla.%';
    update AllCommits set AuthorMailDomain = 'oracle.com' where AuthorMailDomain like '%.oracle.com';
    update AllCommits set AuthorMailDomain = 'unity3d.com' where AuthorMailDomain like '%.unity3d.com';
    update AllCommits set AuthorMailDomain = 'uber.com' where AuthorMailDomain like '%.uber.com';
    update AllCommits set AuthorMailDomain = 'yandex-team.ru' where AuthorMailDomain like '%.yandex-team.ru';
    update AllCommits set AuthorMailDomain = 'shopify.com' where AuthorMailDomain like '%.shopify.com';
    update AllCommits set AuthorMailDomain = 'linkedin.com' where AuthorMailDomain like '%.linkedin.com';
    update AllCommits set AuthorMailDomain = 'suse.com' where AuthorMailDomain like '%suse.%';
    update AllCommits set AuthorMailDomain = 'esri.com' where AuthorMailDomain like '%esri.%';
    update AllCommits set AuthorMailDomain = 'apple.com' where AuthorMailDomain like '%.apple.com';
    update AllCommits set AuthorMailDomain = 'salesforce.com' where AuthorMailDomain like '%.salesforce.com';
    update AllCommits set AuthorMailDomain = 'vmware.com' where AuthorMailDomain like '%.vmware.com';
    update AllCommits set AuthorMailDomain = 'adobe.com' where AuthorMailDomain like '%.adobe.com';
    update AllCommits set AuthorMailDomain = 'andela.com' where AuthorMailDomain like '%.andela.com';
    update AllCommits set AuthorMailDomain = 'cisco.com' where AuthorMailDomain like '%.cisco.com';
    update AllCommits set AuthorMailDomain = 'wix.com' where AuthorMailDomain like '%.wix.com';
    update AllCommits set AuthorMailDomain = 'netflix.com' where AuthorMailDomain like '%.netflix.com';
    update AllCommits set AuthorMailDomain = 'kitware.com' where AuthorMailDomain like '%.kitware.com' or AuthorMailDomain like '%.kitware.%';
    update AllCommits set AuthorMailDomain = 'arm.com' where AuthorMailDomain like '%.arm.com' or AuthorMailDomain like '%.arm.com.%';
    update AllCommits set AuthorMailDomain = 'nvidia.com' where AuthorMailDomain like '%.nvidia.com' or AuthorMailDomain like '%.nvidia.com.%';
    update AllCommits set AuthorMailDomain = 'travis-ci.org' where AuthorMailDomain like 'travis-ci.%';
    update AllCommits set AuthorMailDomain = 'docker.com' where AuthorMailDomain like 'docker.%';
    update AllCommits set AuthorMailDomain = 'samsung.com' where AuthorMailDomain like '%.samsung.com';
    update AllCommits set AuthorMailDomain = 'capgemini.com' where AuthorMailDomain like '%.capgemini.com';
    update AllCommits set AuthorMailDomain = 'collabora.com' where AuthorMailDomain = 'collabora.co.uk';
    update AllCommits set AuthorMailDomain = 'exoplatform.com' where AuthorMailDomain like '%.exoplatform.org';
    update AllCommits set AuthorMailDomain = 'odoo.com' where AuthorMailDomain like '%.odoo.com';
    update AllCommits set AuthorMailDomain = 'dynatrace.com' where AuthorMailDomain like '%.dynatrace.com' or AuthorMailDomain = 'dynatrace.org' or AuthorMailDomain like '%.dynatrace.org';
    update AllCommits set AuthorMailDomain = 'wso2.com' where AuthorMailDomain = 'wso2.org';
    update AllCommits set AuthorMailDomain = 'elastic.co' where AuthorMailDomain like '%.elastic.co';
    update AllCommits set AuthorMailDomain = 'alfresco.com' where AuthorMailDomain like '%.alfresco.com';
    update AllCommits set AuthorMailDomain = 'osrfoundation.org' where AuthorMailDomain = 'openrobotics.org';
    update AllCommits set AuthorMailDomain = '5minds.de' where AuthorMailDomain like '%.5minds.de';
    update AllCommits set AuthorMailDomain = 'couchbase.com' where AuthorMailDomain like '%.couchbase.com';
    update AllCommits set AuthorMailDomain = 'gradle.com' where AuthorMailDomain = 'gradle.org';
    update AllCommits set AuthorMailDomain = 'kaltura.com' where AuthorMailDomain = 'kaltura.org';
    update AllCommits set AuthorMailDomain = 'mapbox.com' where AuthorMailDomain like '%.mapbox.com';
    update AllCommits set AuthorMailDomain = 'hashicorp.com' where AuthorMailDomain = 'hashicorp.co' or AuthorMailDomain = 'hashicorp.io';
    update AllCommits set AuthorMailDomain = 'puppet.com' where AuthorMailDomain like '%.puppet.com';
    update AllCommits set AuthorMailDomain = 'shopware.com' where AuthorMailDomain = 'shopware.de';
    update AllCommits set AuthorMailDomain = 'mesosphere.com' where AuthorMailDomain = 'mesosphere.io';
    update AllCommits set AuthorMailDomain = 'nxp.com' where AuthorMailDomain like '%.nxp.com';
    update AllCommits set AuthorMailDomain = 'percona.com' where AuthorMailDomain like '%.percona.com';
    update AllCommits set AuthorMailDomain = 'tutanota.com' where AuthorMailDomain = 'tutanota.de';
    update AllCommits set AuthorMailDomain = 'vaadin.com' where AuthorMailDomain like '%.vaadin.com';
    update AllCommits set AuthorMailDomain = 'bosch.com' where AuthorMailDomain like '%.bosch.com' or AuthorMailDomain = 'bosch-si.com';
    update AllCommits set AuthorMailDomain = 'confluent.io' where AuthorMailDomain = 'confluent.com';
    update AllCommits set AuthorMailDomain = 'indexdata.com' where AuthorMailDomain = 'indexdata.dk';
    update AllCommits set AuthorMailDomain = 'mariadb.com' where AuthorMailDomain = 'mariadb.org';
    update AllCommits set AuthorMailDomain = 'shopsys.com' where AuthorMailDomain = 'shopsys.cz';
    update AllCommits set AuthorMailDomain = 'hortonworks.com' where AuthorMailDomain like '%.hortonworks.com';
    update AllCommits set AuthorMailDomain = 'h2o.ai' where AuthorMailDomain = 'h2oai.com';

    commit tran;
end try
begin catch
	declare @errMsg nvarchar(4000) = error_message();
	rollback tran;
	raiserror('%s', 16, 1, @errMsg);
end catch;
