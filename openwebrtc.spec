#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Flexible cross-platform WebRTC client framework based on GStreamer
Summary(pl.UTF-8):	Elastyczny, wieloplatformowy szkielet klienta WebRTC oparty na GStreamerze
Name:		openwebrtc
Version:	0.3.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/EricssonResearch/openwebrtc/releases/download/v%{version}/%{name}-%{version}-linux-sources.tar.bz2
# Source0-md5:	68c3cb69408740fd7ae94dfed6597ca8
Patch0:		%{name}-ac.patch
URL:		http://www.openwebrtc.org/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gstreamer-devel >= 1.4
BuildRequires:	gstreamer-plugins-base-devel >= 1.4
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	json-glib-devel
BuildRequires:	libnice-devel >= 0.1.7.1
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libusrsctp-devel
BuildRequires:	orc-devel >= 0.4
BuildRequires:	pulseaudio-devel
BuildRequires:	seed-devel
BuildRequires:	xxd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenWebRTC is a flexible cross-platform WebRTC client framework based
on GStreamer.

%description -l pl.UTF-8
OpenWebRTC to elastyczny, wieloplatformowy szkielet klienta WebRTC
oparty na GStreamerze.

%package devel
Summary:	Header files for OpenWebRTC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenWebRTC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	gstreamer-devel >= 1.4
Requires:	libnice-devel >= 0.1.7.1
Requires:	seed-devel

%description devel
Header files for OpenWebRTC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenWebRTC.

%package static
Summary:	Static OpenWebRTC library
Summary(pl.UTF-8):	Statyczna biblioteka OpenWebRTC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenWebRTC library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenWebRTC.

%prep
%setup -q -c -T -n openwebrtc-%{version}-linux-sources
# unpack manually to skip several hundreds MB of unwanted junk
%{__tar} xjf %{SOURCE0} -C .. \
	--exclude cerbero/sources/local/seed \
	--exclude cerbero/sources/local/libnice-0.1.10 \
	--exclude cerbero/sources/local/libxml2-2.9.2 \
	--exclude cerbero/sources/local/bzip2-1.0.6 \
	--exclude cerbero/sources/local/openh264-1.4.0 \
	--exclude cerbero/sources/local/gnome-js-common-0.1.2 \
	--exclude cerbero/sources/local/gettext-tools-0.19.4 \
	--exclude cerbero/sources/local/json-glib-1.0.2 \
	--exclude cerbero/sources/local/intltool-0.40.6 \
	--exclude cerbero/sources/local/pkg-config-0.28 \
	--exclude cerbero/sources/local/m4-1.4.17 \
	--exclude cerbero/sources/local/intltool-m4-0.40.6 \
	--exclude cerbero/sources/local/gst-plugins-good-1.0 \
	--exclude cerbero/sources/local/libffi \
	--exclude cerbero/sources/local/javascriptcoregtk-2.4.6 \
	--exclude cerbero/sources/local/gst-plugins-base-1.0 \
	--exclude cerbero/sources/local/libtool-2.4.5 \
	--exclude cerbero/sources/local/openssl-1.0.2a \
	--exclude cerbero/sources/local/libvpx \
	--exclude cerbero/sources/local/orc-tool \
	--exclude cerbero/sources/local/autoconf-2.69 \
	--exclude cerbero/sources/local/gnome-common-3.14.0 \
	--exclude cerbero/sources/local/glib-2.44.0 \
	--exclude cerbero/sources/local/gstreamer-1.0 \
	--exclude cerbero/sources/local/gettext-0.19.4 \
	--exclude cerbero/sources/local/automake-1.15 \
	--exclude cerbero/sources/local/gtk-doc-lite-1.21 \
	--exclude cerbero/sources/local/gettext-m4-0.19.4 \
	--exclude cerbero/sources/local/orc \
	--exclude cerbero/sources/local/libsrtp-1.5.2 \
	--exclude cerbero/sources/local/gst-plugins-bad-1.0 \
	--exclude cerbero/sources/local/gobject-introspection-1.44.0 \
	--exclude cerbero/sources/local/libsoup-2.50.0 \
	--exclude cerbero/sources/local/icu-53.1 \
	--exclude cerbero/sources/local/opus-1.1 \
	--exclude cerbero/sources/local/zlib-1.2.8 \
	--exclude cerbero/sources/local/libnice-static-0.1.10 \
	--exclude cerbero/sources/local/libusrsctp-master

%patch0 -p1

%build
cd cerbero/sources/local/openwebrtc-gst-plugins
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make} -j1

cd ../openwebrtc
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	GSTREAMER_SCTP_CFLAGS="-I$(pwd)/../openwebrtc-gst-plugins/gst-libs" \
	GSTREAMER_SCTP_LIBS="-L$(pwd)/../openwebrtc-gst-plugins/gst-libs/gst/sctp/.libs -lgstsctp-1.0" \
	--enable-owr-gst \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C cerbero/sources/local/openwebrtc-gst-plugins install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C cerbero/sources/local/openwebrtc install \
	DESTDIR=$RPM_BUILD_ROOT

# tests/examples
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{list-devices,test-*}
# dlopened modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.la
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc cerbero/sources/local/openwebrtc/{COPYING,README.md,ROADMAP.md}
%attr(755,root,root) %{_bindir}/openwebrtc-daemon
%attr(755,root,root) %{_libdir}/libgstsctp-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstsctp-1.0.so.0
%attr(755,root,root) %{_libdir}/libopenwebrtc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenwebrtc.so.4201
%attr(755,root,root) %{_libdir}/libopenwebrtc_bridge.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenwebrtc_bridge.so.0
%attr(755,root,root) %{_libdir}/libopenwebrtc_gst.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenwebrtc_gst.so.0
%{_libdir}/girepository-1.0/Owr-0.3.typelib
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstsctp.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstvideorepair.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgstsctp-1.0.so
%attr(755,root,root) %{_libdir}/libopenwebrtc.so
%attr(755,root,root) %{_libdir}/libopenwebrtc_bridge.so
%attr(755,root,root) %{_libdir}/libopenwebrtc_gst.so
%{_includedir}/gstreamer-1.0/gst/sctp
%{_includedir}/owr
%{_datadir}/gir-1.0/Owr-0.3.gir
%{_pkgconfigdir}/gstreamer-sctp-1.0.pc
%{_pkgconfigdir}/openwebrtc-0.3.pc
%{_pkgconfigdir}/openwebrtc-bridge-0.3.pc
%{_pkgconfigdir}/openwebrtc-gst-0.3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgstsctp-1.0.a
%{_libdir}/libopenwebrtc.a
%{_libdir}/libopenwebrtc_bridge.a
%{_libdir}/libopenwebrtc_gst.a
%endif
