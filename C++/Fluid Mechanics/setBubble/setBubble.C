/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) 2023 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Application
    setBubble

Description

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
using namespace constant::mathematical;
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{

   argList::addBoolOption
   (
    "noWritePrgh",
    "do not initialise p_rgh"
   );
    #include "setRootCase.H" //argList args
    #include "createTime.H" //Time runTime
    #include "createMesh.H" //fvMesh mesh
    #include "createFields.H"
    #include "readGravitationalAcceleration.H"

    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
    
    const volVectorField& C = mesh.C();
    const DimensionedField<scalar, volMesh>& V= mesh.V();
    scalar bubbleVolume = 0.0;
    DynamicList<label> bubbleCells;
    
    forAll(C, celli)
    {
        const vector& Ci = C[celli];
        
        if (mag(Ci- centre) < radius)
        {
            alpha[celli] = 0;
            p[celli] = pB;
            T[celli] = TB;
            bubbleVolume += V[celli];
            bubbleCells.append(celli);
        }
        else if (-(Ci & g.value())/mag(g.value()) > height)
        {
            alpha[celli] = 0;
        }
    }
    reduce(bubbleVolume, sumOp<scalar>());
    //p_rgh = p;
    
    scalar bubbleRatio = pi*sqr(radius)/bubbleVolume;
    switch (mesh.nSolutionD())
    {
        case 2:
        {
            const vector n
            (
                //Vector<scalar> == vector
                0.5*(Vector<label>::one - mesh.solutionD())
            );
            bubbleRatio *= (n & mesh.bounds().span());
            break;
        }
        case 3:
        {
            bubbleRatio *= 4.0*radius/3.0;
            break;
        }
        
    }
    Info<< "bubbleRatio = " << bubbleRatio << endl;
    
    const scalar gamma = 1.4;
    pB *= Foam::pow(bubbleRatio, gamma);
    TB *= Foam::pow(bubbleRatio, (gamma -1));
    
    forAll(bubbleCells,i)
    {
        const label& celli = bubbleCells[i];
        p[celli] = pB;
        T[celli] = TB;
    }
    p_rgh = p;
    
    runTime.writeNow();
    
    Info<< nl << "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
        << "  ClockTime = " << runTime.elapsedClockTime() << " s"
        << nl << endl;

    Info<< "End\n" << endl;

    return 0;
}


// ************************************************************************* //
