%global srcname avocado
%global pkgname avocado-lts

# Conditional for release vs. snapshot builds. Set to 1 for release build.
%if ! 0%{?rel_build:1}
    %global rel_build 1
%endif

# Settings used for build from snapshots.
%if 0%{?rel_build}
    %global gittar		%{srcname}-%{version}.tar.gz
%else
    %if ! 0%{?commit:1}
        %global commit		bb62fe5a1fa93ea6573da46556928af5041c1b7d
    %endif
    %if ! 0%{?commit_date:1}
        %global commit_date	20170626
    %endif
    %global shortcommit	%(c=%{commit};echo ${c:0:7})
    %global gitrel		.%{commit_date}git%{shortcommit}
    %global gittar		%{srcname}-%{shortcommit}.tar.gz
%endif

# Selftests are provided but may need to be skipped because many of
# the functional tests are time and resource sensitive and can
# cause race conditions and random build failures. They are
# enabled by default.
# However, selftests need to be disabled when libvirt is not available.
%global with_tests 1
%if 0%{?rhel}
    # libvirt is not available for all RHEL builder architectures
    %global with_tests 0
%endif

Name: python-%{pkgname}
Version: 52.0
Release: 1%{?gitrel}%{?dist}
Summary: Framework with tools and libraries for Automated Testing (LTS branch)
Group: Development/Tools
# Found licenses:
# avocado/utils/external/gdbmi_parser.py: MIT
# avocado/utils/external/spark.py: MIT
# optional_plugins/html/avocado_result_html/resources/static/css/*: MIT
# optional_plugins/html/avocado_result_html/resources/static/js/*: MIT
# Other files: GPLv2 and GPLv2+
License: GPLv2 and MIT
# the avocado LTS releases should not co-exist with the regular feature releases
Conflicts: python-avocado
URL: http://avocado-framework.github.io/
%if 0%{?rel_build}
Source0: https://github.com/avocado-framework/%{srcname}/archive/%{version}.tar.gz#/%{gittar}
%else
Source0: https://github.com/avocado-framework/%{srcname}/archive/%{commit}.tar.gz#/%{gittar}
%endif
BuildArch: noarch
BuildRequires: fabric
BuildRequires: pystache
BuildRequires: python2-aexpect
BuildRequires: python2-devel
BuildRequires: python-docutils
BuildRequires: python-flexmock
BuildRequires: python-lxml
BuildRequires: python2-mock
BuildRequires: python-resultsdb_api

%if 0%{?with_tests}
BuildRequires: libvirt-python
BuildRequires: perl(TAP::Parser)
%if 0%{?rhel}
BuildRequires: python-yaml
%else
BuildRequires: python2-yaml
%endif
%endif

%if 0%{?rhel}
BuildRequires: python-psutil
BuildRequires: python-requests
BuildRequires: python-setuptools
BuildRequires: python-sphinx
BuildRequires: python-stevedore
%else
BuildRequires: python2-psutil
BuildRequires: python2-requests
BuildRequires: python2-setuptools
BuildRequires: python2-sphinx
BuildRequires: python2-stevedore
%endif

%if 0%{?el6}
BuildRequires: procps
BuildRequires: python-argparse
BuildRequires: python-importlib
BuildRequires: python-logutils
BuildRequires: python-unittest2
%else
BuildRequires: procps-ng
%endif

# For some strange reason, fabric on Fedora 24 does not require the
# python-crypto package, but the fabric code always imports it.  Newer
# fabric versions, such from Fedora 25 do conditional imports (try:
# from Crypto import Random; except: Random = None) and thus do not
# need this requirement.
%if 0%{?fedora} == 24
BuildRequires: python-crypto
%endif

%if 0%{?fedora} >= 25
BuildRequires: kmod
%endif
%if 0%{?rhel} >= 7
BuildRequires: kmod
%endif

%description
Avocado is a set of tools and libraries (what people call
these days a framework) to perform automated testing.

This is the LTS (Long Term Support) branch.


%package -n python2-%{pkgname}
Summary: %{summary}
License: GPLv2 and MIT
# the avocado LTS releases should not co-exist with the regular feature releases
Conflicts: python2-avocado
%{?python_provide:%python_provide python2-%{pkgname}}
Requires: fabric
Requires: gdb
Requires: gdb-gdbserver
Requires: pyliblzma
Requires: pystache
Requires: python2

%if 0%{?rhel}
Requires: python-requests
Requires: python-stevedore
%else
Requires: python2-requests
Requires: python2-stevedore
%endif

%if 0%{?el6}
Requires: procps
Requires: python-argparse
Requires: python-importlib
Requires: python-logutils
Requires: python-unittest2
%else
Requires: procps-ng
%endif


%description -n python2-%{pkgname}
Avocado is a set of tools and libraries (what people call
these days a framework) to perform automated testing.

This is the LTS (Long Term Support) branch.


%package -n python2-%{pkgname}-plugins-output-html
Summary: Avocado HTML report plugin
%{?python_provide:%python_provide python2-%{pkgname}-plugins-output-html}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: pystache

%description -n python2-%{pkgname}-plugins-output-html
Adds to avocado the ability to generate an HTML report at every job results
directory. It also gives the user the ability to write a report on an
arbitrary filesystem location.


%package -n python2-%{pkgname}-plugins-runner-remote
Summary: Avocado Runner for Remote Execution
%{?python_provide:%python_provide python2-%{pkgname}-plugins-runner-remote}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: fabric
%if 0%{?fedora} == 24
Requires: python-crypto
%endif

%description -n python2-%{pkgname}-plugins-runner-remote
Allows Avocado to run jobs on a remote machine, by means of an SSH
connection. Avocado must be previously installed on the remote machine.


%package -n python2-%{pkgname}-plugins-runner-vm
Summary: Avocado Runner for libvirt VM Execution
%{?python_provide:%python_provide python2-%{pkgname}-plugins-runner-vm}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: python2-%{pkgname}-plugins-runner-remote == %{version}-%{release}
Requires: libvirt-python

%description -n python2-%{pkgname}-plugins-runner-vm
Allows Avocado to run jobs on a libvirt based VM, by means of
interaction with a libvirt daemon and an SSH connection to the VM
itself. Avocado must be previously installed on the VM.


%package -n python2-%{pkgname}-plugins-runner-docker
Summary: Avocado Runner for Execution on Docker Containers
%{?python_provide:%python_provide python2-%{pkgname}-plugins-runner-docker}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: python2-%{pkgname}-plugins-runner-remote == %{version}-%{release}
Requires: python2-aexpect

%description -n python2-%{pkgname}-plugins-runner-docker
Allows Avocado to run jobs on a Docker container by interacting with a
Docker daemon and attaching to the container itself. Avocado must
be previously installed on the container.


%package -n python2-%{pkgname}-plugins-resultsdb
Summary: Avocado plugin to propagate job results to ResultsDB
%{?python_provide:%python_provide python2-%{pkgname}-plugins-resultsdb}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: python-resultsdb_api

%description -n python2-%{pkgname}-plugins-resultsdb
Allows Avocado to send job results directly to a ResultsDB
server.


%package -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
Summary: Avocado plugin to generate variants out of yaml files
%{?python_provide:%python_provide python2-%{pkgname}-plugins-resultsdb}
Requires: python2-%{pkgname} == %{version}-%{release}
%if 0%{?rhel}
Requires: python-yaml
%else
Requires: python2-yaml
%endif

%description -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
Can be used to produce multiple test variants with test parameters
defined in a yaml file(s).


%package -n python-%{pkgname}-examples
Summary: Avocado Test Framework Example Tests
License: GPLv2
# documentation does not require main package, but needs to be in lock-step if present
Conflicts: python-%{pkgname} < %{version}-%{release}, python-%{pkgname} > %{version}-%{release}

%description -n python-%{pkgname}-examples
The set of example tests present in the upstream tree of the Avocado framework.
Some of them are used as functional tests of the framework, others serve as
examples of how to write tests on your own.


%prep
%if 0%{?rel_build}
%setup -q -n %{srcname}-%{version}
%else
%setup -q -n %{srcname}-%{commit}
%endif
# package plugins-runner-vm requires libvirt-python, but the RPM
# version of libvirt-python does not publish the egg info and this
# causes that dep to be attempted to be installed by pip
sed -e "s/'libvirt-python'//" -i optional_plugins/runner_vm/setup.py

%build
%{__python2} setup.py build
pushd optional_plugins/html
    %{__python2} setup.py build
popd
pushd optional_plugins/runner_remote
    %{__python2} setup.py build
popd
pushd optional_plugins/runner_vm
    %{__python2} setup.py build
popd
pushd optional_plugins/runner_docker
    %{__python2} setup.py build
popd
pushd optional_plugins/resultsdb
    %{__python2} setup.py build
popd
pushd optional_plugins/varianter_yaml_to_mux
    %{__python2} setup.py build
popd
%{__make} man

%install
%{__python2} setup.py install --root %{buildroot} --skip-build
pushd optional_plugins/html
    %{__python2} setup.py install --root %{buildroot} --skip-build
popd
pushd optional_plugins/runner_remote
    %{__python2} setup.py install --root %{buildroot} --skip-build
popd
pushd optional_plugins/runner_vm
    %{__python2} setup.py install --root %{buildroot} --skip-build
popd
pushd optional_plugins/runner_docker
    %{__python2} setup.py install --root %{buildroot} --skip-build
popd
pushd optional_plugins/resultsdb
    %{__python2} setup.py install --root %{buildroot} --skip-build
popd
pushd optional_plugins/varianter_yaml_to_mux
    %{__python2} setup.py install --root %{buildroot} --skip-build
popd
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__install} -m 0644 man/avocado.1 %{buildroot}%{_mandir}/man1/avocado.1
%{__install} -m 0644 man/avocado-rest-client.1 %{buildroot}%{_mandir}/man1/avocado-rest-client.1
%{__install} -d -m 0755 %{buildroot}%{_sharedstatedir}/avocado/data
# relocate examples to documentation directory
%{__mkdir_p} %{buildroot}%{_docdir}/avocado
%{__mv} %{buildroot}%{_datadir}/avocado/tests %{buildroot}%{_docdir}/avocado/tests
%{__mv} %{buildroot}%{_datadir}/avocado/wrappers %{buildroot}%{_docdir}/avocado/wrappers
find %{buildroot}%{_docdir}/avocado -type f -name '*.py' -exec %{__chmod} -c -x {} ';'


%check
%if 0%{?with_tests}
    %{__python2} setup.py develop --user
    pushd optional_plugins/html
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/runner_remote
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/runner_vm
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/runner_docker
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/resultsdb
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/varianter_yaml_to_mux
        %{__python2} setup.py develop --user
    popd
    # Package build environments have the least amount of resources
    # we have observed so far. Let's avoid tests that require too
    # much resources or are time sensitive.
    AVOCADO_CHECK_LEVEL=0 selftests/run
%endif


%files -n python2-%{pkgname}
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/avocado
%dir %{_sysconfdir}/avocado/conf.d
%dir %{_sysconfdir}/avocado/sysinfo
%dir %{_sysconfdir}/avocado/scripts
%dir %{_sysconfdir}/avocado/scripts/job
%dir %{_sysconfdir}/avocado/scripts/job/pre.d
%dir %{_sysconfdir}/avocado/scripts/job/post.d
%config(noreplace) %{_sysconfdir}/avocado/avocado.conf
%config(noreplace) %{_sysconfdir}/avocado/conf.d/gdb.conf
%config(noreplace) %{_sysconfdir}/avocado/sysinfo/commands
%config(noreplace) %{_sysconfdir}/avocado/sysinfo/files
%config(noreplace) %{_sysconfdir}/avocado/sysinfo/profilers
%{_sysconfdir}/avocado/conf.d/README
%{_sysconfdir}/avocado/scripts/job/pre.d/README
%{_sysconfdir}/avocado/scripts/job/post.d/README
%{python2_sitelib}/avocado/
%{python2_sitelib}/avocado_framework-%{version}-py%{python2_version}.egg-info
%{_bindir}/avocado
%{_bindir}/avocado-rest-client
%{_mandir}/man1/avocado.1.gz
%{_mandir}/man1/avocado-rest-client.1.gz
%dir %{_sharedstatedir}/avocado
%dir %{_docdir}/avocado
%{_docdir}/avocado/avocado.rst
%{_docdir}/avocado/avocado-rest-client.rst
%dir %{_libexecdir}/avocado
%{_libexecdir}/avocado/avocado-bash-utils
%{_libexecdir}/avocado/avocado_debug
%{_libexecdir}/avocado/avocado_error
%{_libexecdir}/avocado/avocado_info
%{_libexecdir}/avocado/avocado_warn


%files -n python2-%{pkgname}-plugins-output-html
%{python2_sitelib}/avocado_result_html/
%{python2_sitelib}/avocado_framework_plugin_result_html-%{version}-py%{python2_version}.egg-info


%files -n python2-%{pkgname}-plugins-runner-remote
%{python2_sitelib}/avocado_runner_remote/
%{python2_sitelib}/avocado_framework_plugin_runner_remote-%{version}-py%{python2_version}.egg-info


%files -n python2-%{pkgname}-plugins-runner-vm
%{python2_sitelib}/avocado_runner_vm/
%{python2_sitelib}/avocado_framework_plugin_runner_vm-%{version}-py%{python2_version}.egg-info


%files -n python2-%{pkgname}-plugins-runner-docker
%{python2_sitelib}/avocado_runner_docker/
%{python2_sitelib}/avocado_framework_plugin_runner_docker-%{version}-py%{python2_version}.egg-info


%files -n python2-%{pkgname}-plugins-resultsdb
%{python2_sitelib}/avocado_resultsdb/
%{python2_sitelib}/avocado_framework_plugin_resultsdb-%{version}-py%{python2_version}.egg-info


%files -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
%{python2_sitelib}/avocado_varianter_yaml_to_mux/
%{python2_sitelib}/avocado_framework_plugin_varianter_yaml_to_mux-%{version}-py%{python2_version}.egg-info


%files -n python-%{pkgname}-examples
%dir %{_docdir}/avocado
%{_docdir}/avocado/tests
%{_docdir}/avocado/wrappers


%changelog
* Wed Aug 02 2017 Merlin Mathesius <mmathesi@redhat.com> - 52.0-1
- Initial packaging of LTS (Long Term Support) branch for Fedora.
