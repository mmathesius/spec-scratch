%global srcname aexpect

# Conditional for release vs. snapshot builds. Set to 1 for release build.
%global rel_build 1

# Settings used for build from snapshots.
%if 0%{?rel_build}
%global gittar		%{srcname}-%{version}.tar.gz
%else
%if ! 0%{?commit:1}
%global commit		aca459d332c90c8d2db521819a4e2f83fa0b7614
%endif
%if ! 0%{?commit_date:1}
%global commit_date	20161110
%endif
%global shortcommit	%(c=%{commit};echo ${c:0:7})
%global gitrel		.%{commit_date}git%{shortcommit}
%global gittar		%{srcname}-%{shortcommit}.tar.gz
%endif

# Selftests are provided but skipped because they use unsupported tooling.
%global with_tests 0

%if 0%{?rhel}
%global with_python3 0
%else
%global with_python3 1
%endif

Name: python-%{srcname}
Version: 1.4.0
Release: 2%{?gitrel}%{?dist}
Summary: A python library to control interactive applications
Group: Development/Tools

License: GPLv2
URL: https://github.com/avocado-framework/aexpect

%if 0%{?rel_build}
Source0: https://github.com/avocado-framework/%{srcname}/archive/%{version}.tar.gz#/%{gittar}
%else
Source0: https://github.com/avocado-framework/%{srcname}/archive/%{commit}.tar.gz#/%{gittar}
%endif

BuildArch: noarch
Requires: python
BuildRequires: python2-devel

%if %{with_python3}
Requires: python3
BuildRequires: python3-devel
%endif

%if 0%{?rhel}
BuildRequires: python-setuptools
%endif

%description
Aexpect is a python library used to control interactive applications, very
similar to pexpect. You can use it to control applications such as ssh, scp
sftp, telnet, among others.

%package -n python2-%{srcname}
Summary: %{summary}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Aexpect is a python library used to control interactive applications, very
similar to pexpect. You can use it to control applications such as ssh, scp
sftp, telnet, among others.

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary: %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Aexpect is a python library used to control interactive applications, very
similar to pexpect. You can use it to control applications such as ssh, scp
sftp, telnet, among others.
PYTHON 3 SUPPORT IS CURRENTLY EXPERIMENTAL
%endif


%prep
%if 0%{?rel_build}
%autosetup -n %{srcname}-%{version}
%else
%autosetup -n %{srcname}-%{commit}
%endif

%build
%py2_build

%if %{with_python3}
%py3_build
%endif

%install
%py2_install
# move and symlink python2 version-specific executables
mv %{buildroot}%{_bindir}/aexpect-helper %{buildroot}%{_bindir}/aexpect-helper-%{python2_version}
ln -s aexpect-helper-%{python2_version} %{buildroot}%{_bindir}/aexpect-helper-2

%if %{with_python3}
%py3_install
# move and symlink python3 version-specific executables
mv %{buildroot}%{_bindir}/aexpect-helper %{buildroot}%{_bindir}/aexpect-helper-%{python3_version}
ln -s aexpect-helper-%{python3_version} %{buildroot}%{_bindir}/aexpect-helper-3
%endif

# use python2 for unversioned executable
ln -s aexpect-helper-%{python2_version} %{buildroot}%{_bindir}/aexpect-helper

%check
%if %{with_tests}
selftests/checkall
%endif

%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/aexpect/
%{python2_sitelib}/aexpect-%{version}-py%{python2_version}.egg-info
%{_bindir}/aexpect-helper
%{_bindir}/aexpect-helper-2*

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/aexpect/
%{python3_sitelib}/aexpect-%{version}-py%{python3_version}.egg-info
%{_bindir}/aexpect-helper-3*
%endif

%changelog
* Tue Apr 04 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.4.0-2
- Provide python3 version-specific executables. (BZ#1437184)

* Tue Apr 04 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.4.0-1
- Sync with upstream release 1.4.0 (BZ#1438782).
- Update source location to refer to new home.
- Provide python2 version-specific executables.

* Mon Feb 20 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.3.1-1
- Sync with upstream release 1.3.1 (BZ#1425027).

* Tue Feb 14 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.3.0-1
- Sync with upstream release 1.3.0.
- SPEC updates to easily switch between release and snapshot builds.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6.20161110gitaca459d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.2.0-5
- SPEC updates to build and install for EPEL.

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-4.20161110gitaca459d
- Rebuild for Python 3.6

* Thu Nov 10 2016 Merlin Mathesius <mmathesi@redhat.com> - 1.2.0-3
- Initial packaging for Fedora.
