%global         soversion 1.9

Name:           sword
Epoch:          1
Version:        1.9.0
Release:        22%{?dist}
Summary:        Free Bible Software Project
License:        GPLv2 AND LicenseRef-Fedora-Public-Domain AND Apache-2.0 AND LGPL-2.0-or-later AND Zlib AND LGPL-2.1-or-later AND (0BSD OR MIT-0 OR MIT)
URL:            http://www.crosswire.org/sword/
Source0:        sword-1.9.0.tar.gz
Source1:        sword_gen_free_tarball.sh
Source2:        LICENSE_README
Patch0:         cmake-perl-bindings.diff
Patch1:         migrate-to-setuptools.diff
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  libidn-devel
BuildRequires:  libicu-devel
BuildRequires:  icu
BuildRequires:  clucene-core-devel
BuildRequires:  cppunit-devel
BuildRequires:  swig
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  gcc
BuildRequires:  gcc-c++

%description
The SWORD Project is the CrossWire Bible Society's free Bible software
project. Its purpose is to create cross-platform open-source tools--
covered by the GNU General Public License-- that allow programmers and
Bible societies to write new Bible software more quickly and easily. We
also create Bible study software for all readers, students, scholars,
and translators of the Bible, and have a growing collection of over 200
texts in over 50 languages.

%package devel
Summary:  Development files for the sword project
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Requires: curl-devel clucene-core-devel libicu-devel

%description devel
This package contains the development headers and libraries for the
sword API. You need this package if you plan on compiling software
that uses the sword API, such as Gnomesword or Bibletime.

%package utils
Summary:  Utilities for the sword project
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description utils
This package contains the pre-built utilities for use with the SWORD
Project. The SWORD Project developers encourage you to use the latest
development version of the utilities rather than those released with
a packaged release as updates to the utilities do not affect the
release schedule of the library. However, these utilities were the
latest at the time of the current library release.

%package -n python3-sword
%{?python_provide:%python_provide python3-sword}
Summary: Python bindings for Sword
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: python3
%py_provides python3-Sword

%description -n python3-sword
Python bindings for The SWORD Library.

%package -n perl-sword
%{?perl_provide:%perl_provide perl-sword}
Summary: Perl bindings for Sword
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: perl-interpreter
Requires: perl-XML-LibXML
Requires: perl-HTML-Strip

%description -n perl-sword
Perl bindings for The SWORD Library.

%prep
%setup -q

%autosetup -p1

%build
%cmake -DLIBSWORD_LIBRARY_TYPE=Shared \
       -DSWORD_PYTHON_3:BOOL=TRUE \
       -DSWORD_PERL:BOOL=TRUE \
       -DSWORD_BUILD_UTILS="Yes" \
       -DLIBSWORD_SOVERSION=%{soversion} \
       -DLIBDIR=%{_libdir} \
       -DSWORD_BUILD_TESTS=Yes \
       -DSWORD_PYTHON_INSTALL_ROOT="%{buildroot}" \
       -DSWORD_PYTHON_INSTALL_DIR="%{_prefix}"
%cmake_build

%install
%cmake_install
mkdir -p %{buildroot}%{_datadir}/sword/modules

%check
make tests

%files
%doc AUTHORS ChangeLog NEWS README
%doc samples doc
%license COPYING LICENSE
# Re-enable after upstream includes it with CMake builds
%config(noreplace) %{_sysconfdir}/sword.conf
%{_libdir}/libsword.so.%{soversion}
%{_datadir}/sword/

%files devel
%doc CODINGSTYLE
%{_includedir}/sword/
%{_libdir}/libsword.so
%{_libdir}/pkgconfig/sword.pc

%files utils
%{_bindir}/vs2osisref
%{_bindir}/vs2osisreftxt
%{_bindir}/mod2vpl
%{_bindir}/imp2ld
%{_bindir}/diatheke
%{_bindir}/mkfastmod
%{_bindir}/mod2zmod
%{_bindir}/xml2gbs
%{_bindir}/imp2vs
%{_bindir}/installmgr
%{_bindir}/osis2mod
%{_bindir}/tei2mod
%{_bindir}/vpl2mod
%{_bindir}/mod2imp
%{_bindir}/addld
%{_bindir}/imp2gbs
%{_bindir}/mod2osis
%{_bindir}/emptyvss

%files -n python3-sword
%pycached %{python3_sitearch}/Sword.py
%{python3_sitearch}/_Sword%{python3_ext_suffix}
%{python3_sitearch}/sword-%{version}-py%{python3_version}.egg-info

%files -n perl-sword
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/


%changelog
* Fri Sep 29 2023 Aaron Rainbolt <arraybolt3@fedoraproject.org> - 1:1.9.0-22
- Replace distutils with setuptools in python setup scripts (rhbz#2220606)
- Don't install the INSTALL file as part of the documentation
- Remove Android bindings as they contain a prebuild binary
- Remove gSOAP bindings as they contain a non-free source file
- Remove Objective C bindings as they contain a non-free source file
- Remove win32-related utility code as it is non-free
- Remove some sort of pre-built PalmOS application binary

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 1:1.9.0-20
- Rebuilt for ICU 73.2

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9.0-19
- Perl 5.38 rebuild

* Fri Jun 30 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9.0-18
- Replace requirement of meta-package perl by perl-interpreter

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1:1.9.0-17
- Rebuilt for Python 3.12

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 1:1.9.0-15
- Rebuild for ICU 72

* Mon Dec 12 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9.0-14
- Add BR perl-generators to automatically generates run-time dependencies
  for installed Perl files

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 1:1.9.0-13
- Rebuilt for ICU 71.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1:1.9.0-11
- Rebuilt for Python 3.11

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.9.0-10
- Perl 5.36 rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 09 2021 Greg Hellings <greg.hellings@gmail.com> - 1:1.9.0-7
- Correct dependencies for subpackages

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:1.9.0-6
- Rebuilt for Python 3.10

* Mon May 24 2021 Greg Hellings <greg.hellings@gmail.com> - 1:1.9.0-5
- Add Epoch tag

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.0-5
- Perl 5.34 rebuild

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 1.9.0-4
- Rebuild for ICU 69

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Greg Hellings <greg.hellings@gmail.com> - 1.9.0-2
- Restore Perl bindings

* Tue Dec 1 2020 Greg Hellings <greg.hellings@gmail.com> - 1.9.0-1
- Upstream 1.9.0 release

* Fri Oct 2 2020 Greg Hellings <greg.hellings@gmail.com> - 1.8.903-1
- Upstream 1.9.0RC3 release

* Fri Sep 11 2020 Greg Hellings <greg.hellings@gmail.com> - 1.8.901-1
- Upstream 1.9.0RC1 release

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-24
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.1-22
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-21
- Rebuilt for Python 3.9

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 1.8.1-20
- Rebuild for ICU 67

* Sun Apr 26 2020 Greg Hellings <greg.hellings@gmail.com> - 1.8.1-19
- Added patch to fix upstream markup bug

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 1.8.1-17
- Rebuild for ICU 65

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-16
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Jaak Ristioja <jaak@ristioja.ee> - 1.8.1-15
- Fixed conflicting integer types being defined

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-14
- Rebuilt for Python 3.8

* Sun Aug 04 2019 Dominique Corbex <dominique@corbex.org> - 1.8.1-13
- Added Perl bindings

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 1.8.1-10
- Rebuild for ICU 63

* Mon Sep 24 2018 Greg Hellings <greg.hellings@gmail.com> - 1.8.1-9
- Remove Python 2 binding build: BZ1627373

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Greg Hellings <greg.hellings@gmail.com> - 1.8.1-7
- Add flags for building ICU 61+
- Patch Python building for Python 2/3 combined

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 1.8.1-6
- Rebuild for ICU 62

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 1.8.1-5
- Rebuild for ICU 61.1

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.8.1-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Feb 18 2018 Gregory Hellings <greg.hellings@gmail.com> - 1.8.1-3
- Remove post/postun for F28+
- Rename python-sword to python2-sword
- Add BR for gcc/g++ per F28+ changes

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Greg Hellings <greg.hellings@gmail.com> - 1.8.1-1
- Upstream release 1.8.1
- Add check section

* Sat Dec 23 2017 Greg Hellings <greg.hellings@gmail.com> - 1.8.0-1
- Upstream release 1.8.0

* Tue Dec 5 2017 Greg Hellings <greg.hellings@gmail.com> - 1.7.906-1
- Testing 1.8.0RC6

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 1.7.4-15
- Rebuild for ICU 60.1

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.7.4-14
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.7.4-13
- Python 2 binary package renamed to python2-sword
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 1.7.4-7
- rebuild for ICU 57.1

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 1.7.4-5
- rebuild for ICU 56.1

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.7.4-3
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 1.7.4-2
- rebuild for ICU 54.1

* Wed Dec 24 2014 Greg Hellings <greg.hellings@gmail.com> - 1.7.4-1
- New upstream release
- Removed upstreamed patches

* Tue Dec 09 2014 Greg Hellings <greg.hellings@gmail.com> - 1.7.3.900-3
- Fixed invalid pkg-config

* Mon Dec 08 2014 Greg Hellings <greg.hellings@gmail.com> - 1.7.3.900-2
- Changed to CMake
- Added Python bindings

* Wed Dec 03 2014 Greg Hellings <greg.hellings@gmail.com> - 1.7.3.900-1
- Upstream pre-release version bump

* Mon Oct 27 2014 Greg Hellings <greg.hellings@gmail.com> - 1.7.3-9
- Release bump

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 1.7.3-7
- rebuild for ICU 53.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.7.3-5
- revert some incompatible "cleanup" (%%make_build undefined on < f21)
- -devel: drop extraneous lib deps (let pkgconfig autoreq handle it as needed)

* Mon Aug 11 2014 Greg Hellings <greg.hellings@gmail.com> - 1.7.3-4
- Change curl-devel for libcurl-devel

* Sat Aug 02 2014 Christopher Meng <rpm@cicku.me> - 1.7.3-3
- devel subpkg cleanup

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Greg Hellings <greg.hellings@gmail.com> - 1.7.3-1
- New upstream version

* Thu Feb 13 2014 Greg Hellings <greg.hellings@gmail.com> - 1.7.2-2
- Rebuilt for ICU 52

* Wed Jan 29 2014 Deji Akingunola <dakingun@gmail.com> - 1.7.2-1
- Update to sword-1.7.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 01 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.6.2-10
- Rebuild for icu 50

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Deji Akingunola <dakingun@gmail.com> - 1.6.2-8
- Rebuild for icu soname change

* Wed Feb 22 2012 Deji Akingunola <dakingun@gmail.com> - 1.6.2-7
- Fix compile error with gcc-4.7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 1.6.2-5
- fix compile against clucene2

* Fri Sep 09 2011 Caolán McNamara <caolanm@redhat.com> - 1.6.2-4
- rebuild for icu 4.8.1

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 1.6.2-3
- rebuild for icu 4.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 22 2010 Deji Akingunola <dakingun@gmail.com> - 1.6.2-1
- Update to version 1.6.2

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 1.6.1-3
- rebuild for icu 4.4

* Sat Mar 20 2010 Deji Akingunola <dakingun@gmail.com> - 1.6.1-2
- Work around regression in curl-7.20.0 (Patch by Karl Kleinpaste), fix #569685

* Wed Jan 13 2010 Deji Akingunola <dakingun@gmail.com> - 1.6.1-1
- Update to version 1.6.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 14 2009 Deji Akingunola <dakingun@gmail.com> - 1.6.0-1
- Update to version 1.6.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Deji Akingunola <dakingun@gmail.com> - 1.5.11-3
- Add patch to build with gcc-4.4

* Tue Jun 03 2008 Caolán McNamara <caolanm@redhat.com> - 1.5.11-2
- rebuild for new icu

* Mon May 26 2008 Deji Akingunola <dakingun@gmail.com> - 1.5.11-1
- Update to version 1.5.11

* Thu Feb 21 2008 Deji Akingunola <dakingun@gmail.com> - 1.5.10-3
- Fix command injection bug (Bug #433723) 

* Thu Jan 10 2008 Deji Akingunola <dakingun@gmail.com> - 1.5.10-2
- Fix build issue with gcc43 

* Mon Nov 05 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.10-1
- Update to version 1.5.10

* Tue Sep 25 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-7
- Fix the build failure due to glibc open() check

* Sat Aug 25 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-6
- Rebuild

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-5
- License tag update
- Rebuild for new icu

* Sat Jan 20 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-4
- Fix an error (libicu-devel not icu-devel)

* Sat Jan 20 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-3
- Add Requires for the -devel subpackage

* Sun Jan 14 2007 Deji Akingunola <dakingun@gmail.com> - 1.5.9-2
- Rebuild with lucene support

* Wed Nov 08 2006 Deji Akingunola <dakingun@gmail.com> - 1.5.9-1
- New release
- Build with icu support

* Wed Sep 20 2006 Deji Akingunola <dakingun@gmail.com> - 1.5.8-9
- Take over from Michael A. Peters
- Rebuild for FC6

* Sat Jun 03 2006 Michael A. Peters <mpeters@mac.com> - 1.5.8-8
- Added pkgconfig to devel package Requires

* Fri Feb 17 2006 Michael A. Peters <mpeters@mac.com> - 1.5.8-7
- Rebuild in devel branch

* Wed Dec 14 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-6
- rebuild in devel branch with new compiler suite
- remove specific release from devel requires of main package
- do not build with %%{_smp_mflags}

* Mon Nov 21 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-5
- disable static library

* Sun Nov 13 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-4.1
- Rebuild against new openssl

* Sat Oct 29 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-4
- Added Arabic support files from Developer mailing list (they have
- been added to the upstream SVN version)

* Thu Jun 09 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-3
- fix line breaks

* Mon Jun 06 2005 Michael A. Peters <mpeters@mac.com> - 1.5.8-1
- initial CVS checkin for Fedora Extras
