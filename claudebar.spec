Name:           claudebar
Version:        0.1.0
Release:        1%{?dist}
Summary:        Claude usage meter for Waybar on Sway

License:        MIT
URL:            https://github.com/alpharomercoma/claudebar-for-sway
# GitHub archives unpack to claudebar-for-sway-<version>/ (the repo name)
Source0:        %{url}/archive/v%{version}/claudebar-for-sway-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
Requires:       python3
Recommends:     waybar
Recommends:     libnotify

%description
A Waybar custom module that shows real-time Claude usage — 5-hour window
percentage and time until reset — pulled from Anthropic's API using your
existing Claude Code credentials. Ships claudebar-setup, which wires the
module into an existing Waybar configuration in one command.

%prep
%autosetup -n claudebar-for-sway-%{version}
%py3_shebang_fix claudebar-usage claudebar-setup

%build
# nothing to build — plain Python scripts

%install
install -Dpm0755 claudebar-usage %{buildroot}%{_bindir}/claudebar-usage
install -Dpm0755 claudebar-setup %{buildroot}%{_bindir}/claudebar-setup
install -Dpm0644 config.jsonc %{buildroot}%{_datadir}/%{name}/config.jsonc
install -Dpm0644 style.css %{buildroot}%{_datadir}/%{name}/style.css

%files
%license LICENSE
%doc README.md
%{_bindir}/claudebar-usage
%{_bindir}/claudebar-setup
%{_datadir}/%{name}/

%changelog
* Tue Jul 07 2026 Alpha Romer Coma <alpharomercoma@proton.me> - 0.1.0-1
- Initial package: usage script with staleness/sign-in states and claudebar-setup
