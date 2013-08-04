# This package contains macros that provide functionality relating to
# Software Collections. These macros are not used in default
# Fedora builds, and should not be blindly copied or enabled.
# Specifically, the "scl" macro must not be defined in official Fedora
# builds. For more information, see:
# http://docs.fedoraproject.org/en-US/Fedora_Contributor_Documentation
# /1/html/Software_Collections_Guide/index.html

%{?scl:%scl_package python-%{pypi_name}}
%{!?scl:%global pkg_name %{name}}

# Created by pyp2rpm-0.5.1
%global pypi_name sure

Name:           %{?scl_prefix}python-%{pypi_name}
Version:        1.1.7
Release:        3%{?dist}
Summary:        Assertion toolbox for python

License:        GPLv3+
URL:            https://github.com/gabrielfalcao/sure
Source0:        http://pypi.python.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Already asked upstream to include COPYING in the source tar:
# https://github.com/gabrielfalcao/sure/issues/17
Source1:        https://raw.github.com/gabrielfalcao/sure/master/COPYING
# To get tests:
# git clone https://github.com/gabrielfalcao/sure.git && cd sure
# git checkout 1.1.7 && tar czf sure-1.1.7-tests.tgz tests/
Source2:        %{pypi_name}-%{version}-tests.tgz
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}python2-devel
BuildRequires:  %{?scl_prefix}python-nose
BuildRequires:  %{?scl_prefix}python-setuptools

%description
A Python assertion toolbox that works fine with nose.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
cp %{SOURCE1} .

%build
%{?scl:scl enable %{scl} "}
%{__python} setup.py build
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
%{__python} setup.py install --skip-build --root %{buildroot}
%{?scl:"}

%check
tar xzf %{SOURCE2}
%{?scl:scl enable %{scl} "}
nosetests
%{?scl:"}

%files
%doc COPYING
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.7-2
- Introduce SCL macros in the specfile.

* Mon Feb 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.7-1
- Update to 1.1.7.
- License change from MIT to GPLv3.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.6-1
- Update to 1.0.6.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.3-2
- python-devel should be python2-devel
- URL now points to the real homepage of the project

* Fri Jun 22 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.3-1
- Initial package.
