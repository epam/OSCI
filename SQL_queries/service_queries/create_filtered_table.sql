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
    AuthorMailDomain = 'ixsystems.com' or
    AuthorMailDomain = 'polyapp.tech' or
    AuthorMailDomain = 'tensor.ru' or
    AuthorMailDomain = 'enalean.com' or
    AuthorMailDomain = 'windriver.com' or
    AuthorMailDomain = 'wolfvision.net' or
    AuthorMailDomain = 'onlyoffice.com' or
    AuthorMailDomain = 'solita.fi' or
    AuthorMailDomain = 'bjss.com' or
    AuthorMailDomain = 'vtex.com.br' or
    AuthorMailDomain = 'buoyant.io' or
    AuthorMailDomain = 'feenk.com' or
    AuthorMailDomain = 'splunk.com' or
    AuthorMailDomain = 'syndicode.com' or
    AuthorMailDomain = 'adc.sh' or
    AuthorMailDomain = 'tyro.com' or
    AuthorMailDomain = 'burohappold.com' or
    AuthorMailDomain = 'enjin.com' or
    AuthorMailDomain = 'block.one' or
    AuthorMailDomain = 'mellanox.com' or
    AuthorMailDomain = 'citrix.com' or
    AuthorMailDomain = 'itemis.de' or
    AuthorMailDomain = 'robotis.com' or
    AuthorMailDomain = 'bitnami.com' or
    AuthorMailDomain = 'sysop.cz' or
    AuthorMailDomain = 'antmicro.com' or
    AuthorMailDomain = 'wire.com' or
    AuthorMailDomain = 'silverstripe.com' or
    AuthorMailDomain = 'ptfs-europe.com' or
    AuthorMailDomain = 'insolar.io' or
    AuthorMailDomain = 'rte-france.com' or
    AuthorMailDomain = 'adhocteam.us' or
    AuthorMailDomain = 'asiantech.vn' or
    AuthorMailDomain = 'juliacomputing.com' or
    AuthorMailDomain = 'microchip.com' or
    AuthorMailDomain = 'graylog.com' or
    AuthorMailDomain = 'univention.de' or
    AuthorMailDomain = 'orange.com' or
    AuthorMailDomain = 'arbisoft.com' or
    AuthorMailDomain = 'eastagile.com' or
    AuthorMailDomain = 'improbable.io' or
    AuthorMailDomain = 't-matix.com' or
    AuthorMailDomain = 'teamdev.com' or
    AuthorMailDomain = 'switch.com.uy' or
    AuthorMailDomain = 'toucantoco.com' or
    AuthorMailDomain = 'bitrise.io' or
    AuthorMailDomain = 'softwire.com' or
    AuthorMailDomain = 'paloaltonetworks.com' or
    AuthorMailDomain = 'loodos.com' or
    AuthorMailDomain = 'commercetools.de' or
    AuthorMailDomain = 'here.com' or
    AuthorMailDomain = 'atypon.com' or
    AuthorMailDomain = 'antfin.com' or
    AuthorMailDomain = 'dynamo.com.uy' or
    AuthorMailDomain = 'jankaritech.com' or
    AuthorMailDomain = 'twilio.com' or
    AuthorMailDomain = 'yunionyun.com' or
    AuthorMailDomain = 'd2l.com' or
    AuthorMailDomain = 'dxw.com' or
    AuthorMailDomain = 'nexylan.com' or
    AuthorMailDomain = 'prism.ai' or
    AuthorMailDomain = 'athina.co.nz' or
    AuthorMailDomain = 'espressif.com' or
    AuthorMailDomain = 'pantheon.io' or
    AuthorMailDomain = 'consensys.net' or
    AuthorMailDomain = 'polidea.com' or
    AuthorMailDomain = 'mediatek.com' or
    AuthorMailDomain = 'euro-linux.com' or
    AuthorMailDomain = 'devoxsoftware.com' or
    AuthorMailDomain = 'snyk.io' or
    AuthorMailDomain = 'circleci.com' or
    AuthorMailDomain = 'accenture.com' or
    AuthorMailDomain = 'qt.io' or
    AuthorMailDomain = '4teamwork.ch' or
    AuthorMailDomain = 'dosarrest.com' or
    AuthorMailDomain = 'eyeo.com' or
    AuthorMailDomain = 'lge.com' or
    AuthorMailDomain = 'nevion.com' or
    AuthorMailDomain = 'sentry.io' or
    AuthorMailDomain = 'okta.com' or
    AuthorMailDomain = 'turner.com' or
    AuthorMailDomain = 'grafana.com' or
    AuthorMailDomain = 'lunarg.com' or
    AuthorMailDomain = 'octo.com' or
    AuthorMailDomain = 'plot.ly' or
    AuthorMailDomain = 'pixelandtonic.com' or
    AuthorMailDomain = 'nordicsemi.no' or
    AuthorMailDomain = 'talan.com' or
    AuthorMailDomain = 'plentymarkets.com' or
    AuthorMailDomain = 'kinvolk.io' or
    AuthorMailDomain = 'rackspace.com' or
    AuthorMailDomain = 'binary.com' or
    AuthorMailDomain = 'privacyone.co' or
    AuthorMailDomain = 'blockchainfoundry.co' or
    AuthorMailDomain = 'experis.com' or
    AuthorMailDomain = 'squareup.com' or
    AuthorMailDomain = 'luxoft.com' or
    AuthorMailDomain = 'magento.com' or
    AuthorMailDomain = 'ft.com' or
    AuthorMailDomain = 'cloudflare.com' or
    AuthorMailDomain = 'metasfresh.com' or
    AuthorMailDomain = 'lyft.com' or
    AuthorMailDomain = 'gatsbyjs.com' or
    AuthorMailDomain = 'b2ck.com' or
    AuthorMailDomain = 'forestry.io' or
    AuthorMailDomain = 'skbkontur.ru' or
    AuthorMailDomain = 'yoast.com' or
    AuthorMailDomain = 'reaktor.com' or
    AuthorMailDomain = 'labkey.com' or
    AuthorMailDomain = 'ongres.com' or
    AuthorMailDomain = 'atlassian.com' or
    AuthorMailDomain = 'centreon.com' or
    AuthorMailDomain = 'ptvgroup.com' or
    AuthorMailDomain = 'verizonmedia.com' or
    AuthorMailDomain = 'algolia.com' or
    AuthorMailDomain = 'arangodb.com' or
    AuthorMailDomain = 'bloomberg.net' or
    AuthorMailDomain = 'adorsys.com.ua' or
    AuthorMailDomain = 'digitalasset.com' or
    AuthorMailDomain = 'belledonne-communications.com' or
    AuthorMailDomain = 'maykinmedia.nl' or
    AuthorMailDomain = 'agaric.com' or
    AuthorMailDomain = 'kainos.com' or
    AuthorMailDomain = 'newrelic.com' or
    AuthorMailDomain = 'madetech.com' or
    AuthorMailDomain = 'silicus.com' or
    AuthorMailDomain = 'qualitykiosk.com' or
    AuthorMailDomain = 'cgi.com' or
    AuthorMailDomain = 'scylladb.com' or
    AuthorMailDomain = 'retest.de' or
    AuthorMailDomain = 'equinor.com' or
    AuthorMailDomain = 'bootlin.com' or
    AuthorMailDomain = 'zalando.de' or
    AuthorMailDomain = 'motionpicture.jp' or
    AuthorMailDomain = 'progressoft.com' or
    AuthorMailDomain = 'openlattice.com' or
    AuthorMailDomain = 'c-s.fr' or
    AuthorMailDomain = 'poviolabs.com' or
    AuthorMailDomain = 'pilz.de' or
    AuthorMailDomain = 'cloudcannon.com' or
    AuthorMailDomain = 'rstudio.com' or
    AuthorMailDomain = 'dimagi.com' or
    AuthorMailDomain = 'st.com' or
    AuthorMailDomain = 'gitlab.com' or
    AuthorMailDomain = 'supersoftware.co.jp' or
    AuthorMailDomain = 'cozycloud.cc' or
    AuthorMailDomain = 'arisan.io' or
    AuthorMailDomain = 'gvempire.com' or
    AuthorMailDomain = 'enigio.com' or
    AuthorMailDomain = 'linutronix.de' or
    AuthorMailDomain = 'broadcom.com' or
    AuthorMailDomain = 'what.digital' or
    AuthorMailDomain = 'cksource.com' or
    AuthorMailDomain = 'infragistics.com' or
    AuthorMailDomain = 'test.com' or
    AuthorMailDomain = 'hpe.com' or
    AuthorMailDomain = 'mendix.com' or
    AuthorMailDomain = 'lynxspa.com' or
    AuthorMailDomain = 'gofore.com' or
    AuthorMailDomain = 'truss.works' or
    AuthorMailDomain = 'itsyndicate.org' or
    AuthorMailDomain = 'synopsys.com' or
    AuthorMailDomain = 'ctrl.nl' or
    AuthorMailDomain = 'datavisyn.io' or
	AuthorMailDomain = 'amdocs.com' or
	AuthorMailDomain = 'mountblue.io' or
	AuthorMailDomain = 'wipro.com' or
	AuthorMailDomain = 'mountblue.tech' or
	AuthorMailDomain = 'codethink.co.uk' or
	AuthorMailDomain = 'alauda.io' or
	AuthorMailDomain = 'softtek.com' or
	AuthorMailDomain = 'cognizant.com' or
	AuthorMailDomain = 'rock-chips.com' or
	AuthorMailDomain = 'soprasteria.com' or
	AuthorMailDomain = 'ids.com.mx' or
	AuthorMailDomain = 'innovify.in' or
	AuthorMailDomain = 'no.experis.com' or
	AuthorMailDomain = 'everis.com' or
	AuthorMailDomain = 'siemens.com' or
	AuthorMailDomain = 'webmob.tech' or
	AuthorMailDomain = 'nomadic-labs.com' or
	AuthorMailDomain = 'adblockplus.org' or
	AuthorMailDomain = 'kiwi.com' or
	AuthorMailDomain = 'itential.com' or
	AuthorMailDomain = 'haulmont.com' or
	AuthorMailDomain = 'dell.com' or
	AuthorMailDomain = 'caser.es' or
	AuthorMailDomain = 't-systems.com' or
	AuthorMailDomain = 'kumparan.com' or
	AuthorMailDomain = 'jtl-software.com'
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
    update AllCommits set AuthorMailDomain = 'vaadin.com' where AuthorMailDomain like '%.vaadin.com';
    update AllCommits set AuthorMailDomain = 'bosch.com' where AuthorMailDomain like '%.bosch.com' or AuthorMailDomain = 'bosch-si.com';
    update AllCommits set AuthorMailDomain = 'confluent.io' where AuthorMailDomain = 'confluent.com';
    update AllCommits set AuthorMailDomain = 'indexdata.com' where AuthorMailDomain = 'indexdata.dk';
    update AllCommits set AuthorMailDomain = 'mariadb.com' where AuthorMailDomain = 'mariadb.org';
    update AllCommits set AuthorMailDomain = 'shopsys.com' where AuthorMailDomain = 'shopsys.cz';
    update AllCommits set AuthorMailDomain = 'hortonworks.com' where AuthorMailDomain like '%.hortonworks.com';
    update AllCommits set AuthorMailDomain = 'h2o.ai' where AuthorMailDomain = 'h2oai.com';
    update ParsedData set AuthorMailDomain = 'test.com' where AuthorMailDomain = 'gaugeonline.com';
    update ParsedData set AuthorMailDomain = 'prisme.ai' where AuthorMailDomain = 'gogowego.com';
    update ParsedData set AuthorMailDomain = 'hortonworks.com' where AuthorMailDomain = 'cloudera.com';
	update ParsedData set AuthorMailDomain = 'mountblue.io'	where AuthorMailDomain = 'mountblue.tech';
	update ParsedData set AuthorMailDomain = 'eyeo.com'	where AuthorMailDomain = 'adblockplus.org';

    commit tran;
end try
begin catch
	declare @errMsg nvarchar(4000) = error_message();
	rollback tran;
	raiserror('%s', 16, 1, @errMsg);
end catch;
