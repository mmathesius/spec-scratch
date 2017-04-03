%global srcname pdfsandwich

Name: %{srcname}
Version: 0.1.6
Release: 1%{?dist}
Summary: A tool to make "sandwich" OCR pdf files

License: GPLv2+
URL: http://www.tobias-elze.de/pdfsandwich/

#Source0: http://downloads.sourceforge.net/%{srcname}/%{srcname}-%{version}.tar.bz2
Source0: https://sourceforge.net/projects/%{srcname}/files/%{srcname}%20%{version}/%{srcname}-%{version}.tar.bz2/download#%/%{srcname}-%{version}.tar.bz2

BuildRequires: ocaml
BuildRequires: perl
Requires: ImageMagick
Requires: tesseract
Requires: unpaper

%description
pdfsandwich generates "sandwich" OCR pdf files, i.e. pdf files which contain
only images (no text) will be processed by optical character recognition (OCR)
and the text will be added to each page invisibly "behind" the images. 

%global debug_package %{nil}

%prep
%autosetup -n %{srcname}-%{version}

%build
#./configure
#make
%{_configure} --prefix=%{_prefix}
%make_build

%install
%make_install

%check

%files
%license copyright
%doc manual.txt
%{_bindir}/pdfsandwich
%{_mandir}/man1/pdfsandwich.1.gz
%{_docdir}/pdfsandwich/

%changelog
