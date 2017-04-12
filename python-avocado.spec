%global srcname avocado

# Conditional for release vs. snapshot builds. Set to 1 for release build.
%if ! 0%{?rel_build:1}
%global rel_build 1
%endif

# Settings used for build from snapshots.
%if 0%{?rel_build}
%global gittar		%{srcname}-%{version}.tar.gz
%else
%if ! 0%{?commit:1}
%global commit		337b333e1b58f18f876c993121454f2f6cb599db
%endif
%if ! 0%{?commit_date:1}
%global commit_date	20170213
%endif
%global shortcommit	%(c=%{commit};echo ${c:0:7})
%global gitrel		.%{commit_date}git%{shortcommit}
%global gittar		%{srcname}-%{shortcommit}.tar.gz
%endif

# selftests are provided but may need to skipped because many of
# functional tests are time and resource sensitive and can
# cause race conditions and random build failures.  they are
# enabled by default.
%global with_tests 1

Name: python-%{srcname}
Version: 48.0
Release: 1%{?gitrel}%{?dist}
Summary: Framework with tools and libraries for Automated Testing
Group: Development/Tools
# Found licenses:
# avocado/utils/external/gdbmi_parser.py: MIT
# avocado/utils/external/spark.py: MIT
# optional_plugins/html/avocado_result_html/resources/static/css/*: MIT
# optional_plugins/html/avocado_result_html/resources/static/js/*: MIT
# Other files: GPLv2 and GPLv2+
License: GPLv2 and MIT
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

%if %{with_tests}
BuildRequires: libvirt-python
BuildRequires: perl(TAP::Parser)
%endif

%if 0%{?rhel}
BuildRequires: python-psutil
BuildRequires: python-requests
BuildRequires: python-setuptools
BuildRequires: python-sphinx
BuildRequires: python-stevedore
BuildRequires: python-yaml
%else
BuildRequires: python2-psutil
BuildRequires: python2-requests
BuildRequires: python2-setuptools
BuildRequires: python2-sphinx
BuildRequires: python2-stevedore
BuildRequires: python2-yaml
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


%package -n python2-%{srcname}
Summary: %{summary}
License: GPLv2 and MIT
%{?python_provide:%python_provide python2-%{srcname}}
Requires: fabric
Requires: gdb
Requires: gdb-gdbserver
Requires: libvirt-python
Requires: pyliblzma
Requires: pystache
Requires: python2

%if 0%{?rhel}
Requires: python-requests
Requires: python-stevedore
Requires: python-yaml
%else
Requires: python2-requests
Requires: python2-stevedore
Requires: python2-yaml
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


%description -n python2-%{srcname}
Avocado is a set of tools and libraries (what people call
these days a framework) to perform automated testing.


%package -n python2-%{srcname}-plugins-output-html
Summary: Avocado HTML report plugin
%{?python_provide:%python_provide python2-%{srcname}-plugins-output-html}
Requires: python2-%{srcname} == %{version}-%{release}
Requires: pystache

%description -n python2-%{srcname}-plugins-output-html
Adds to avocado the ability to generate an HTML report at every job results
directory. It also gives the user the ability to write a report on an
arbitrary filesystem location.


%package -n python2-%{srcname}-plugins-runner-remote
Summary: Avocado Runner for Remote Execution
%{?python_provide:%python_provide python2-%{srcname}-plugins-runner-remote}
Requires: python2-%{srcname} == %{version}-%{release}
Requires: fabric
%if 0%{?fedora} == 24
Requires: python-crypto
%endif

%description -n python2-%{srcname}-plugins-runner-remote
Allows Avocado to run jobs on a remote machine, by means of an SSH
connection. Avocado must be previously installed on the remote machine.


%package -n python2-%{srcname}-plugins-runner-vm
Summary: Avocado Runner for libvirt VM Execution
%{?python_provide:%python_provide python2-%{srcname}-plugins-runner-vm}
Requires: python2-%{srcname} == %{version}-%{release}
Requires: python2-%{srcname}-plugins-runner-remote == %{version}-%{release}
Requires: libvirt-python

%description -n python2-%{srcname}-plugins-runner-vm
Allows Avocado to run jobs on a libvirt based VM, by means of
interaction with a libvirt daemon and an SSH connection to the VM
itself. Avocado must be previously installed on the VM.


%package -n python2-%{srcname}-plugins-runner-docker
Summary: Avocado Runner for Execution on Docker Containers
%{?python_provide:%python_provide python2-%{srcname}-plugins-runner-docker}
Requires: python2-%{srcname} == %{version}-%{release}
Requires: python2-%{srcname}-plugins-runner-remote == %{version}-%{release}
Requires: python2-aexpect

%description -n python2-%{srcname}-plugins-runner-docker
Allows Avocado to run jobs on a Docker container by interacting with a
Docker daemon and attaching to the container itself. Avocado must
be previously installed on the container.


%package -n python-%{srcname}-examples
Summary: Avocado Test Framework Example Tests
License: GPLv2
# documentation does not require main package, but needs to be in lock-step if present
Conflicts: python-%{srcname} < %{version}-%{release}, python-%{srcname} > %{version}-%{release}

%description -n python-%{srcname}-examples
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
%{__python} setup.py build
popd
pushd optional_plugins/runner_vm
%{__python} setup.py build
popd
pushd optional_plugins/runner_docker
%{__python} setup.py build
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
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__install} -m 0644 man/avocado.1 %{buildroot}%{_mandir}/man1/avocado.1
%{__install} -m 0644 man/avocado-rest-client.1 %{buildroot}%{_mandir}/man1/avocado-rest-client.1
# relocate examples to documentation directory
%{__mkdir_p} %{buildroot}%{_docdir}/avocado
%{__mv} %{buildroot}%{_datadir}/avocado/tests %{buildroot}%{_docdir}/avocado/tests
%{__mv} %{buildroot}%{_datadir}/avocado/wrappers %{buildroot}%{_docdir}/avocado/wrappers
find %{buildroot}%{_docdir}/avocado -type f -name '*.py' -exec %{__chmod} -c -x {} ';'


%check
%if %{with_tests}
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
selftests/run
%endif

%files -n python2-%{srcname}
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
%dir %{_docdir}/avocado
%{_docdir}/avocado/avocado.rst
%{_docdir}/avocado/avocado-rest-client.rst
%dir %{_libexecdir}/avocado
%{_libexecdir}/avocado/avocado-bash-utils
%{_libexecdir}/avocado/avocado_debug
%{_libexecdir}/avocado/avocado_error
%{_libexecdir}/avocado/avocado_info
%{_libexecdir}/avocado/avocado_warn


%files -n python2-%{srcname}-plugins-output-html
%{python2_sitelib}/avocado_result_html/
%{python2_sitelib}/avocado_framework_plugin_result_html-%{version}-py%{python2_version}.egg-info


%files -n python2-%{srcname}-plugins-runner-remote
%{python2_sitelib}/avocado_runner_remote/
%{python2_sitelib}/avocado_framework_plugin_runner_remote-%{version}-py%{python2_version}.egg-info


%files -n python2-%{srcname}-plugins-runner-vm
%{python2_sitelib}/avocado_runner_vm/
%{python2_sitelib}/avocado_framework_plugin_runner_vm-%{version}-py%{python2_version}.egg-info


%files -n python2-%{srcname}-plugins-runner-docker
%{python2_sitelib}/avocado_runner_docker/
%{python2_sitelib}/avocado_framework_plugin_runner_docker-%{version}-py%{python2_version}.egg-info


%files -n python-%{srcname}-examples
%dir %{_docdir}/avocado
%{_docdir}/avocado/tests
%{_docdir}/avocado/wrappers

%changelog
* Mon Apr 10 2017 Merlin Mathesius <mmathesi@redhat.com> - 48.0-1
- Sync with upstream release 48.0. (BZ#1431413)
- Allow rel_build macro to be defined outside of the SPEC file.

* Mon Mar 27 2017 Merlin Mathesius <mmathesi@redhat.com> - 47.0-1
- Sync with upstream release 47.0.
- Enable self-tests during build.
- Add example test to be run by Taskotron.

* Mon Feb 27 2017 Merlin Mathesius <mmathesi@redhat.com> - 46.0-2
- Incorporate upstream SPEC file changes to split plugins into subpackages.
- Remove obsolete CC-BY-SA license, which went away with the halflings font.

* Tue Feb 14 2017 Merlin Mathesius <mmathesi@redhat.com> - 46.0-1
- Sync with upstream release 46.0.
- Remove halflings license since font was removed from upstream.
- SPEC updates to easily switch between release and snapshot builds.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 43.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Merlin Mathesius <mmathesi@redhat.com> - 43.0-7
- SPEC updates to build and install for EPEL.

* Mon Nov 21 2016 Merlin Mathesius <mmathesi@redhat.com> - 43.0-6
- Initial packaging for Fedora.
