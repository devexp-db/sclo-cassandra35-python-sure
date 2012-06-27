# Created by pyp2rpm-0.5.1
%global pypi_name sure

Name:           python-%{pypi_name}
Version:        0.10.3
Release:        2%{?dist}
Summary:        Assertion toolbox for python

License:        MIT
URL:            https://github.com/gabrielfalcao/sure
Source0:        http://pypi.python.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Already asked upstream to include COPYING in the source tar:
# https://github.com/gabrielfalcao/sure/issues/17
Source1:        https://raw.github.com/gabrielfalcao/sure/master/COPYING
# To get tests:
# git clone https://github.com/gabrielfalcao/sure.git && cd sure
# git checkout 0.10.3 && tar czf sure-0.10.3-tests.tgz test_sure.py
Source2:        %{pypi_name}-%{version}-tests.tgz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-setuptools
# the library claims to be using these, but it actually isn't
# Requires:       python-nose
# Requires:       python-ipdb

%description
A Python assertion toolbox that works fine with nose.


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
cp %{SOURCE1} .


%build
%{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot}


%check
tar xzf %{SOURCE2}
nosetests


%files
%doc COPYING
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Tue Jun 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.3-2
- python-devel should be python2-devel
- URL now points to the real homepage of the project

* Fri Jun 22 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.3-1
- Initial package.
