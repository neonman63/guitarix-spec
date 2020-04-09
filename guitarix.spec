# guitarix has merged with gx_head branch and tarball is distributed as guitarix2
# project name remains guitarix however
%global altname gx_head
%global altname2 guitarix2

# Workaround for rhbz#1721348
%define __brp_strip_static_archive %{nil}

Name:           guitarix
Version:        0.39.0
Release:        1%{?dist}
Summary:        Mono amplifier to JACK
License:        GPLv2+
URL:            https://guitarix.sourceforge.net/
Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{altname2}-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  python3
BuildRequires:  %{_bindir}/find
BuildRequires:  %{_bindir}/pathfix.py
BuildRequires:  desktop-file-utils
BuildRequires:  faust
BuildRequires:  fftw-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtkmm24-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  ladspa-devel
BuildRequires:  libsigc++20-devel
BuildRequires:  libsndfile-devel
BuildRequires:  zita-convolver-devel >= 3.0.2
BuildRequires:  zita-resampler-devel >= 0.1.1-3
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  boost-devel
BuildRequires:  liblrdf-devel
BuildRequires:  lv2-devel
BuildRequires:  lilv-devel
BuildRequires:  gperf
BuildRequires:  avahi-gobject-devel
BuildRequires:  eigen3-devel
BuildRequires:  libcurl-devel
Requires:       clearlooks-compact-gnome-theme
Requires:       jack_capture
Requires:       jconv
Requires:       ladspa-%{name}-plugins = %{version}-%{release}
Requires:       qjackctl
Requires:       vorbis-tools
Requires:       google-roboto-condensed-fonts

%description
Guitarix is a simple mono amplifier to be used in a 'JACKified' environment,
i.e. a system using the JACK Audio Connection Kit, a professionally-capable
audio/MIDI server and master transport control.

Guitarix provides one JACK input port and two JACK output ports. It is designed
to produce nice trash/metal/rock/blues guitar sounds. Controls for bass, treble,
gain, compressor, preamp, balance, distortion, freeverb, crybaby (wah) and echo
are available. A fixed resonator is used when distortion is disabled. To modify
the sound 'pressure', you can use the feedback and feedforward sliders.

Guitarix includes an experimental tuner and a JACK MIDI output port with 3
channels. They are fed by a mix from a pitch tracker and a beat detector. You
can pitch the octave (2 octaves up or down), choose the MIDI channel, the MIDI
program, the velocity and the sensitivity, which translates into how fast the
note will read after the beat detector emits a signal. Values for the beat
detector can be set for all channels.

%package -n libgxw
Summary:        Guitarix GTK library
License:        GPLv2+ 

%description -n libgxw
This package contains the Guitarix GTK widget library

%package -n libgxwmm
Summary:        Guitarix GTK C++ library
License:        GPLv2+ 

%description -n libgxwmm
This package contains the Guitarix GTK C++ widget library

%package -n libgxw-devel
Summary:        Development files for libgxw
License:        GPLv2+ 
Requires:       libgxw%{?_isa} = %{version}-%{release}

%description -n libgxw-devel
This package contains files required to use the libgxw C Guitarix 
widget library

%package -n libgxwmm-devel
Summary:        Development files for libgxwmm
License:        GPLv2+ 
Requires:       libgxwmm%{?_isa} = %{version}-%{release}

%description -n libgxwmm-devel
This package contains files required to use the libgxwmm C++ Guitarix widget 
library

%package -n gxw-glade
Summary:        Guitarix GTK library glade support
License:        GPLv2+ 
Requires:       glade
Requires:       libgxw-devel%{?_isa} = %{version}-%{release}

%description -n gxw-glade
This package contains support for using the Guitarix GTK widget library
with glade

%package -n ladspa-%{name}-plugins
Summary:        Collection of Ladspa plug-ins
# ladspa/distortion.cpp and ladspa/guitarix-ladspa.cpp are BSD
# The rest of ladspa/* is GPLv+
License:        GPL+ and BSD
Requires:       ladspa

%description -n ladspa-%{name}-plugins
This package contains the crybaby, distortion, echo, impulseresponse, monoamp,
and monocompressor ladspa plug-ins that come together with guitarix, but can
also be used by any other ladspa host.

%package -n lv2-%{name}-plugins
Summary:        Collection of LV2 guitarix plug-ins
# ladspa/distortion.cpp and ladspa/guitarix-ladspa.cpp are BSD
# The rest of ladspa/* is GPLv+
License:        GPLv2+ 
Requires:       lv2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n lv2-%{name}-plugins
This package contains the guitarix amp plug-ins that come together with 
guitarix, but can also be used by any other ladspa host.

%prep
%setup -q -n %{name}-%{version}

# Fix unversioned python shebangs
pathfix.py -pni %{_bindir}/python3 \
    $(find -name wscript) \
    waf \
    tools/make_jsonrpc_methods \
    src/gx_head/builder/make \
    .

# The build system does not use these bundled libraries by default. But
# just to make sure:
rm -fr src/zita-convolver src/zita-resampler
sed -i -e 's|-O3||' wscript

%build
%set_build_flags
./waf -vv configure --prefix=%{_prefix} --libdir=%{_libdir}                  \
      --cxxflags="-std=c++0x -fomit-frame-pointer -ftree-loop-linear         \
      -ffinite-math-only -fno-math-errno -fno-signed-zeros -fstrength-reduce \
%ifarch %ix86 x86_64
      -msse                                                                  \
%endif
      %{optflags}"                                                           \
      --shared-lib --lib-dev          \
      --ladspa --ladspadir=%{_libdir}/ladspa --lv2dir=%{_libdir}/lv2 \
      --glade-support --glade-catalog-dir=%{_datadir}/glade/catalogs    \
      --glade-modules-dir=%{_libdir}/glade/modules
./waf -vv build %{?_smp_mflags}

%install
./waf -vv install --destdir="%{buildroot}" --libdir="%{_libdir}"

desktop-file-install                                    \
--add-category="X-DigitalProcessing"                    \
--dir=%{buildroot}%{_datadir}/applications              \
%{buildroot}/%{_datadir}/applications/%{name}.desktop

chmod 755 %{buildroot}%{_libdir}/libgxw*.so.0.1
rm -rf %{buildroot}%{_libdir}/libgxw*.so
ln -s %{_libdir}/libgxwmm.so.0.1 %{buildroot}%{_libdir}/libgxwmm.so
ln -s %{_libdir}/libgxw.so.0.1 %{buildroot}%{_libdir}/libgxw.so
chmod 755 %{buildroot}%{_libdir}/glade/modules/libgladegx.so

%find_lang %{name}


%files -f %{name}.lang
%doc changelog README
%license COPYING
%{_bindir}/%{name}
%{_datadir}/%{altname}/
%{_datadir}/pixmaps/*
%{_datadir}/applications/%{name}.desktop

%files -n libgxw
%{_libdir}/libgxw.so.0*

%files -n libgxwmm
%{_libdir}/libgxwmm.so.0*

%files -n libgxw-devel
%{_libdir}/libgxw.so
%{_includedir}/gxw
%{_includedir}/gxw.h
%{_libdir}/pkgconfig/gxw.pc

%files -n libgxwmm-devel
%{_libdir}/libgxwmm.so
%{_includedir}/gxwmm
%{_includedir}/gxwmm.h
%{_libdir}/pkgconfig/gxwmm.pc

%files -n gxw-glade
%{_libdir}/glade/modules/libgladegx.so
%{_datadir}/%{name}/icons
%{_datadir}/glade/catalogs/*

%files -n ladspa-%{name}-plugins
%{_libdir}/ladspa/*.so
%{_datadir}/ladspa

%files -n lv2-%{name}-plugins
%{_libdir}/lv2/*

%changelog
* Sat Feb 29 2020 Guido Aulisi <guido.aulisi@gmail.com> - 0.39.0-1
- Update to 0.39.0
- Use python3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Guido Aulisi <guido.aulisi@gmail.com> - 0.38.1-1
- Update to 0.38.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Jonathan Wakely <jwakely@redhat.com> - 0.37.3-2
- Patched for Boost 1.69.0 header changes

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 0.37.3-2
- Rebuilt for Boost 1.69

* Sat Sep 08 2018 Nils Philippsen <nils@tiptoe.de> - 0.37.3-1
- update to 0.37.3
- add BR: libcurl-devel

* Sat Jul 21 2018 Adam Huffman <bloch@verdurin.com> - 0.36.1-6
- Add BR for gcc-c++ and python

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 12 2018 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.36.1-4
- Added Requires: clearlooks-compact-gnome-theme. RHBZ#1565827

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.36.1-2
- Rebuilt for Boost 1.66

* Tue Dec 26 2017 Brendan Jones <brendan.jones.it@gmail.com> - 0.36.1-1
- Update to 0.36.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.35.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.35.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Jonathan Wakely <jwakely@redhat.com> - 0.35.2-4
- Rebuilt for s390x binutils bug

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 0.35.2-3
- Rebuilt for Boost 1.64

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Apr 21 2017 Brendan Jones <brendan.jones.it@gmail.com> - 0.35.2-1
- Remove webkit

* Sun Feb 19 2017 Brendan Jones <brendan.jones.it@gmail.com> - 0.35.2-1
- Update to 0.35.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.35.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Jonathan Wakely <jwakely@redhat.com> - 0.35.0-4
- Patched for GCC 7

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.35.0-4
- Rebuilt for Boost 1.63

* Thu Dec 29 2016 Rich Mattes <richmattes@gmail.com> - 0.35.0-3
- Rebuild for eigen3-3.3.1
- Add patch to fix Glib::RefPtr null checks

* Sat May 07 2016 Brendan Jones <brendan.jones.it@gmail.com> 0.35.0-2
- Add Roboto-condensed requires

* Sun Apr 24 2016 Brendan Jones <brendan.jones.it@gmail.com> 0.35.0-1
- Update to 0.35.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.34.0-2
- Rebuilt for Boost 1.60

* Fri Nov 20 2015 Brendan Jones <brendan.jones.it@gmail.com> 0.34.0-1
- Update to 0.34.0
- add webkitgtk-devel
- remove patches

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.33.0-2
- Rebuilt for Boost 1.59

* Sat Aug 01 2015 Brendan Jones <brendan.jones.it@gmail.com> 0.33.0-1
- Update to 0.33.0
- New plugins and fuzz models

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32.3-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.32.3-5
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.32.3-3
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 0.32.3-2
- Bump for rebuild.

* Tue Feb 03 2015 Brendan Jones <brendan.jones.it@gmail.com> 0.32.3-1
- Update to 0.32.3

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.32.0-2
- Rebuild for boost 1.57.0

* Mon Nov 24 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.32.0-1
- Update to 0.32.1

* Mon Oct 06 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.31.0-1
- Update to 0.31.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 09 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.30.0-1
- Update to 0.30.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 0.28.2-4
- Rebuild for boost 1.55.0

* Fri Oct 04 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.28.2-3
- Add missing avahi-gobject-devel

* Fri Oct 04 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.28.2-2
- Add gperf BR

* Sun Sep 29 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.28.2-1
- Update to 0.28.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.27.1-2
- Rebuild for boost 1.54.0

* Sun Apr 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.27.1-1
- Update to 0.27.1

* Fri Apr 12 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.26.1-1
- Remove patches included upstream
- Update to 0.26.1

* Mon Feb 11 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.25.2-1
- Remove patches present in new upstream release

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.25.1-6
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.25.1-5
- Rebuild for Boost-1.53.0

* Tue Jan 15 2013 Dan Horák <dan[at]danny.cz> 0.25.1-4
- fix build on non-x86 arches (gxamp shouldn't append x86-only flags)
- set %%{optflags} only once

* Sun Jan 13 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.25.1-3
- Add missing BR lv2-devel

* Sun Jan 13 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.25.1-2
- Clean up descriptions/summary

* Sat Jan 05 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.25.1-1
- Update to 0.25.1
- Add LV2 sub-package
- Add libs

* Wed Oct 24 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.24.2-1
- New upstream release

* Fri Aug 10 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.23.3-2
- Rebuild for new boost

* Sat Jul 28 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.23.3-1
- Update to 0.23.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.23.2-2
- Add missing BuildRequires (lrdf)

* Sun Jul 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.23.2-1
- Update to upstream 0.23.3

* Mon Jul 02 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.22.4-1
- Update to upstream 0.22.4

* Tue May 15 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.22.3-1
- Update to upstream 0.22.3

* Thu May 03 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.22.2-1
- Update to upstream 0.22.2

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.0-2
- Rebuilt for c++ ABI breakage

* Tue Jan 17 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.21.0-1
- Update to upstream 0.21.0, correct fail to build (missing glibmm headers)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 12 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.20.2-3
- Add boost-devel build requires

* Sat Nov 12 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.20.2-2
- Removed libboost library detection fix

* Sat Nov 12 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.20.2-1
- Update to upstream release 0.20.2

* Tue Nov 08 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.20.0-2
- Update to upstream release 0.20.0

* Sun Oct 30 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.20.0-1.0.svn1278
- Grab source from latest svn, and removed FSF patch
- Rebuild for libpng 1.5
- Removed obsolete tags and clean section from spec

* Sun Oct 30 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.19.0-1.0.svn1245
- Grab source from svn to rebuild against zita-convolver-3

* Fri Jul 15 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.17.0-1
- Update to 0.17.0, replace define macro with global

* Wed Jun 15 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.16.0-3
- Add BuildRequires gettext

* Wed Jun 15 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.16.0-2
- Add BuildRequires gettext

* Mon Jun 13 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.16.0-1
- Updated to version 0.16.0-1 which combines guitarix and gx_head
- Obsoletes gx_head
- Correct build of ladspa plugins and removed O3 optimizations

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.11.1-1
- Update to 0.11.1

* Wed Aug 04 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.11.0-1
- Update to 0.11.0

* Tue Jul 27 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.10.0-3
- Rebuild against new boost on F-14

* Fri Jul 16 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.10.0-2
- Add missing BR: gtkmm24-devel

* Sun Jul 11 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.10.0-1
- Update to 0.10.0

* Sat Jun 26 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.09.0-1
- Update to 0.09.0
- Split the ladspa plugins into a separate package as they can also be used by
  other hosts than guitarix.

* Sat May 15 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.08.0-1
- Update to 0.08.0

* Sat Feb 20 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.06.0-1
- Update to 0.06.0

* Sat Jan 30 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.05.8-1
- Update to 0.05.8

* Thu Dec 24 2009 Orcan Ogetbil <orcan@desitter> - 0.05.5-1
- Update to 0.05.5
- Add Requires: qjackctl. RHBZ #549566

* Wed Aug 05 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.05.0-2
- Update .desktop file

* Mon Jul 27 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.05.0-1
- Update to 0.05.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.04.6-1
- Update to 0.04.6 (build system uses waf now)
- License is GPLv2+
- Add missing Requires: ladspa

* Tue May 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.04.5-1
- Update to 0.04.5

* Thu May 21 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.04.4-1
- Update to 0.04.4
- Drop upstreamed patches

* Sat May 09 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.04.3-1
- Initial build
