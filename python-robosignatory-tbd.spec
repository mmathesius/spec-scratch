#%%global prerelease b1

Name:               python-robosignatory-tbd
Version:            0.0.0
Release:            1%{?prerelease}%{?dist}
Summary:            A robosignatory backend for TBD.
 
License:            MIT
URL:                https://pagure.io/robosignatory/
Source0:            https://pagure.io/releases/robosignatory/robosignatory-tbd-%{version}%{?prerelease}.tar.gz
 
BuildArch:          noarch
 
BuildRequires:      python3-devel
BuildRequires:      python3-robosignatory
BuildRequires:      python3-setuptools

# Tests
BuildRequires:      python3-pytest

%description
A robosignatory backend for TBD.

%package -n python3-robosignatory-tbd
Summary: %summary
Requires: python3-robosignatory

%description -n python3-robosignatory-tbd
A robosignatory backend for TBD.

%prep
%setup -q -n robosignatory-tbd-%{version}%{?prerelease}
# Remove bundled egg-info in case it exists
rm -rf robosignatory_tbd.egg-info
 
%build
%py3_build

%install
%py3_install

%check
%{__python3} -m pytest -v
 
%files -n python3-robosignatory-tbd
%doc README.md LICENSE
%{python3_sitelib}/robosignatory_tbd/
%{python3_sitelib}/robosignatory_tbd-%{version}*
%{_bindir}/robosignatory-tbd
 
 
%changelog
* Fri Jul 16 2021 Merlin Mathesius <mmathesi@redhat.com> - 0.0.0-1
- Initial packaging
