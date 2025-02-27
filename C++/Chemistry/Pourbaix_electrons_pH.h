#pragma once
#ifndef POURBAIX_ELECTRONS_PH_H
#define POURBAIX_ELECTRONS_PH_H

#include "Kernel.h"
#include "Function.h"

// This kernel computes the Nernst equation for Pourbaix diagrams


class Pourbaix_electrons_pH : public Kernel
{
public:
  static InputParameters validParams();
  
  Pourbaix_electrons_pH(const InputParameters & parameters);

protected:
  virtual Real computeQpResidual() override;
  virtual Real computeQpJacobian() override;
  virtual Real computeQpOffDiagJacobian(unsigned int jvar) override;

private:
  const Real _z;  // electrons
  const Real _F;  // Faraday constant (coulumb/mol)
  const Real _R;  // gas constant (J/mol/K)
  const Real _T;  // temperature (K)
  const Real _lambda; // Thermal voltage (V)
  const Real _E0; // Potential (V)
  const Real _concIons; // Dissolved species concentration (mol/L)
  
};

#endif //POURBAIX_ELECTRONS_PH_H
