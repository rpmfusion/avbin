Summary:        Cross-platform media decoding library
Name:           avbin
Version:        7
Release:        8%{?dist}
# Note that this license is implicitly converted to GPLv3 because we are linking to
# a GPLv2+ ffmpeg:
License:        LGPLv3+
Group:          System Environment/Libraries
URL:            http://code.google.com/p/avbin/
Source0:        http://avbin.googlecode.com/files/%{name}-src-%{version}.tar.gz
# avbin is patched to use sws_scale() instead of the obsolete img_convert().
# Patch sent upstream:
# http://code.google.com/p/avbin/issues/detail?id=8
Patch0:         avbin-swscale.patch
# SAMPLE_FMT_S24 is deprecated on ffmpeg rev > 16176:
Patch1:         avbin-SAMPLE_FMT_S24.patch
# The original Makefile links ffmpeg statically. This is the modified 
# Makefile that tells the compiler to link dynamically to ffmpeg:
Patch9:         avbin-Makefile-shared.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  doxygen
BuildRequires:  ffmpeg >= 0.4.9-0.48.20080908
BuildRequires:  ffmpeg-devel >= 0.4.9-0.48.20080908

%description
AVbin is a thin wrapper around FFmpeg, providing binary compatibility for 
applications and languages that need it. AVbin allows programs that require 
dynamic linkage to use FFmpeg. It does this by providing

* an accurate version number within the shared library, allowing applications 
  to select the appropriate data structures and functions to use at runtime, 
* a simplified interface with an unchanging ABI to the most common decoding 
  functionality within FFmpeg. 

%package        devel
Summary:        Development package for AVbin
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
AVbin is a thin wrapper around FFmpeg, providing binary compatibility for 
applications and languages that need it. This package provides the header 
and the documentation files for AVbin.

%prep
%setup -q -n %{name}-src-%{version}

%patch0 -p1
%patch1 -p1
%patch9 -p1

# Fix permissions and end of line encoding issues:
sed 's/\r//' CHANGELOG > CHANGELOG.bak
touch -r CHANGELOG CHANGELOG.bak
mv -f CHANGELOG.bak CHANGELOG

%build
# Now compile avbin
make %{?_smp_mflags} \
     AVBIN_VERSION=$(cat VERSION) \
     FFMPEG_REVISION=$(ffmpeg -version |grep FFmpeg |sed 's|[^0-9]*||') \
     FFMPEG=%{_includedir}/ffmpeg
# Generate the doc files:
doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT
# buildsys sometimes fails without this:
sleep 1m
make install AVBIN_VERSION=$(cat VERSION) \
             INCLUDEDIR=%{_includedir} \
             LIBDIR=%{_libdir} \
             DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING.LESSER CHANGELOG README
%{_libdir}/lib%{name}.so.%{version}

%files devel
%defattr(-,root,root,-)
%doc doc/html/* COPYING.LESSER
%{_includedir}/*
%{_libdir}/lib%{name}.so

%changelog
* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 7-8
- rebuild for new F11 features

* Fri Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 7-7
- Add "sleep 1m" to avoid buildsys failures

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 7-6
- The S24 was actually needed for ffmpeg revision >= 15124. Updated the patch

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 7-5
- Fix license again
- Fix description length
- Patch for compilation against ffmpeg revision >= 16176

* Thu Dec 04 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 7-4
- Update the Makefile patch to do the linking in a proper way
- Preserve the timestamp of the Changelog

* Wed Dec 03 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 7-3
- Set the license to GPLv3 since we are linking to sws_scale which is from the
  GPL part of ffmpeg.

* Sat Nov 22 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 7-2
- Patch to use ffmpeg's sws_scale() instead of the deprecated img_convert().

* Thu Oct 23 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 7-1
- Linked avbin to ffmpeg dynamically
- Use the release version 7 because the avbin code hasn't changed since in svn.
- Update the description

* Thu Oct 23 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 7-0.20081023svn.1
- Initial build. This is ffmpeg's SPEC file modified.
