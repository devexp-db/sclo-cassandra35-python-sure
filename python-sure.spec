# This package contains macros that provide functionality relating to
# Software Collections. These macros are not used in default
# Fedora builds, and should not be blindly copied or enabled.
# Specifically, the "scl" macro must not be defined in official Fedora
# builds. For more information, see:
# http://docs.fedoraproject.org/en-US/Fedora_Contributor_Documentation
# /1/html/Software_Collections_Guide/index.html

%{?scl:%scl_package python-%{pypi_name}}
%{!?scl:%global pkg_name %{name}}

%global run_tests 0

# Created by pyp2rpm-0.5.1
# if building for SCL or on RHEL, don't build python3- subpackage
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%else
%global with_python3 0
%endif
%global pypi_name sure

%global sum Utility belt for automated testing in Python

Name:           %{?scl_prefix}python-%{pypi_name}
Version:        1.4.0
Release:        5%{?dist}
Summary:        %{sum}

License:        GPLv3+
URL:            https://github.com/gabrielfalcao/sure
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
# python-mock is only needed for tests
#BuildRequires:  python-mock
BuildRequires:  python-nose
BuildRequires:  python-setuptools
BuildRequires:  python-six
Requires:       python-six

%if 0%{with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-mock
BuildRequires:  python3-nose
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
%endif

%{?scl:Requires: %scl_runtime}
%{?scl:BuildRequires: %scl-scldevel}

%description
A testing library for Python with powerful and flexible assertions. Sure is
heavily inspired by should.js.

%package -n %{?scl_prefix}python2-%{pypi_name}
Summary:        %{sum} 2
%{!?scl:%{?python_provide:%python_provide python2-%{pypi_name}}}

%description -n %{?scl_prefix}python2-%{pypi_name}
A testing library for Python with powerful and flexible assertions. Sure is
heavily inspired by should.js.

%if 0%{?with_python3}
%package -n %{?scl_prefix}python3-%{pypi_name}
Summary:        %{sum} 3
%{!?scl:%{?python_provide:%python_provide python3-%{pypi_name}}}
Requires:       python3-six

%description -n %{?scl_prefix}python3-%{pypi_name}
A testing library for Python with powerful and flexible assertions. Sure is
heavily inspired by should.js.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/bin/env python|#!%{__python3}|'
%endif # with_python3

%build
%{?scl:scl enable %{scl} - << "EOF"}
%py2_build

%if 0%{with_python3}
pushd %{py3dir}
LANG=en_US.utf8 %py3_build
popd
%endif
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << "EOF"}
%{py2_install -- --prefix %{?_prefix}}

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.utf8 %{py3_install -- --prefix %{?_prefix}}
popd
%endif # with_python3
%{?scl:EOF}

%if 0%{?run_tests}
%check
%{?scl:scl enable %{scl} "}
%{__python2} setup.py test
%{?scl:"}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3
%endif

%files -n %{?scl_prefix}python2-%{pypi_name}
%doc COPYING
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n %{?scl_prefix}python3-%{pypi_name}
%doc COPYING
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Tue Oct 03 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 1.4.0-5
- scl fixing

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 1.4.0-4
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Adam Williamson <awilliam@redhat.com> - 1.4.0-1
- New release 1.4.0 (builds against Python 3.6)
- Drop sources merged upstream
- Modernize spec a bit (use modern macros)
- Rename python2 package to python2-sure

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.7-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 1.2.7-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 1.2.7-1
- Updated to 1.2.7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 31 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.5-2
- Remove unneeded dependencies from setup.py.
Resolves: rhbz#1082400

* Fri Mar 07 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.5-1
- Updated to 1.2.5
- Fix with_python3 macro definition to work correctly on EPEL, too.

* Fri Nov 29 2013 Miro Hrončok <mhroncok@redhat.com> - 1.2.3-1
- Updated
- Introduced Python 3 subpackage

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
