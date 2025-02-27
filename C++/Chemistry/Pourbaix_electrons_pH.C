#include "Pourbaix_electrons_pH.h"

registerMooseObject("BabblerApp", Pourbaix_electrons_pH);



InputParameters
Pourbaix_electrons_pH::validParams()
{
  InputParameters params = Kernel::validParams();
  params.addRequiredParam<Real>("z", "Charge number");
  params.addParam<Real>("F", 96485, "Faraday constant (C/mol)");
  params.addParam<Real>("R", 8.314, "Gas constant (J/mol/K)");
  params.addParam<Real>("T", 298.0, "Temperature (K)");
  params.addParam<Real>("lambda", 0.0, "Slope adjustment parameter (0 if horizontal)");
  params.addParam<Real>("E0",0.728, "E0 Potential (V)");
  params.addParam<Real>("concIons", 10e-06, "The concentration of dissolved species (mol/L)");
  params.addClassDescription("This kernel applies the Nernst equation for Pourbaix diagrams");
  return params;
}

Pourbaix_electrons_pH::Pourbaix_electrons_pH(const InputParameters & parameters) :
    Kernel(parameters),
    _z(getParam<Real>("z")),
    _F(getParam<Real>("F")),
    _R(getParam<Real>("R")),
    _T(getParam<Real>("T")),
    _lambda(getParam<Real>("lambda")),
    _E0(getParam<Real>("E0")),
    _concIons(getParam<Real>("concIons"))
{
}

Real
Pourbaix_electrons_pH::computeQpResidual()
{
  return (_E0 - _lambda * (_R * _T) / _F /_z *(6* _u[_qp] + log( pow(_concIons,2))))* _test[_i][_qp];
}

Real
Pourbaix_electrons_pH::computeQpJacobian()
{
  return - _lambda * (_R * _T) / _F /_z *(6)*_phi[_j][_qp] * _test[_i][_qp];
}

Real
Pourbaix_electrons_pH::computeQpOffDiagJacobian(unsigned int jvar)
{
  return - _lambda * (_R * _T) / _F /_z *(6) *_phi[_j][_qp] * _test[_i][_qp];
}
