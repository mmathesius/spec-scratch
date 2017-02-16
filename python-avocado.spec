%global srcname avocado

# Conditional for release vs. snapshot builds. Set to 1 for release build.
%global rel_build 1

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

# selftests are provided but skipped because many contain race conditions
# causing random build failures
%global with_tests 0

Name: python-%{srcname}
Version: 46.0
Release: 1%{?gitrel}%{?dist}
Summary: Framework with tools and libraries for Automated Testing
Group: Development/Tools
# Found licenses:
# avocado/utils/external/gdbmi_parser.py: MIT
# avocado/utils/external/spark.py: MIT
# optional_plugins/html/avocado_result_html/resources/static/css/*: MIT
# optional_plugins/html/avocado_result_html/resources/static/js/*: MIT
# Other files: GPLv2 and GPLv2+
License: GPLv2 and MIT and CC-BY-SA
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
Requires: python2-aexpect

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
License: GPLv2 and MIT and CC-BY-SA
%{?python_provide:%python_provide python2-%{srcname}-plugins-output-html}
Requires: python2-%{srcname} == %{version}-%{release}
Requires: pystache

%description -n python2-%{srcname}-plugins-output-html
Adds to avocado the ability to generate an HTML report at every job results
directory. It also gives the user the ability to write a report on an
arbitrary filesystem location.


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

%build
%{__python2} setup.py build
pushd optional_plugins/html
%{__python2} setup.py build
popd
%{__make} man

%install
%{__python2} setup.py install --root %{buildroot} --skip-build
pushd optional_plugins/html
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
%{python2_sitelib}/avocado_result_html-%{version}-py%{python2_version}.egg-info


%files -n python-%{srcname}-examples
%dir %{_docdir}/avocado
%{_docdir}/avocado/tests
%{_docdir}/avocado/wrappers

%changelog
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
