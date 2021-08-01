%bcond_without tests

%global pypi_name scikit-uplift
%global short_name sklift
%global pretty_name scikit_uplift

%global _description %{expand:
scikit-uplift (sklift) is an uplift modeling python package that provides 
fast sklearn-style models implementation, evaluation metrics and visualization
tools. Uplift modeling estimates a causal effect of treatment and uses it to 
effectively target customers that are most likely to respond to a marketing
campaign.}

Name:           python-%{pypi_name}
Version:        0.3.2
Release:        1%{?dist}
Summary:        Uplift modeling in scikit-learn style in python

License:        MIT
URL:            https://github.com/maks-sh/scikit-uplift
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

%description %_description

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %_description

%package -n python-%{pypi_name}-doc
Summary:        Scikit-uplift documentation

%description -n python-%{pypi_name}-doc
Documentation for scikit-uplift package

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%generate_buildrequires
# No setup.cfg, tox.ini or pyproject.toml
echo 'python3dist(pip) >= 19'
echo 'python3dist(packaging)'
echo 'python3dist(setuptools) >= 40.8'
echo 'python3dist(wheel)'
echo 'python3dist(sphinx)'
echo 'python3dist(recommonmark)'
echo 'python3dist(sphinxcontrib-bibtex)'
echo 'python3dist(sphinx-rtd-theme)'
echo 'python3dist(pytest)'
echo 'python3dist(scikit-learn)'
echo 'python3dist(pandas)'

%build
%pyproject_wheel

# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%pyproject_install

# Remove extra install files
rm -rf %{buildroot}/%{python3_sitelib}/tests

%pyproject_save_files %{short_name}

%check
%if %{with tests}
# Disable network tests
%pytest -k 'not test_fetch_hillstrom and not test_fetch_criteo10 and not test_return_X_y_t'
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc Readme.rst

%files -n python-%{pypi_name}-doc
%doc html
%doc notebooks/
%license LICENSE

%changelog
* Fri Jul 23 2021 Iztok Fister Jr. <iztokf AT fedoraproject DOT org> - 0.3.2-1
- Initial package
