Info<< "Reading physicalProperties\n" << endl;

IOdictionary physicalProperties
(
    IOobject
    (
        "physicalProperties",
        runTime.constant(),
        mesh,
        IOobject::MUST_READ_IF_MODIFIED,
        IOobject::NO_WRITE
    )
);

dimensionedScalar nu
(
    "nu",
    dimViscosity,
    physicalProperties.lookup("nu")
);

Info<< "Reading field p\n" << endl;
volScalarField p
(
    IOobject
    (
        "p",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);


Info<< "Reading field U\n" << endl;
volVectorField U
(
    IOobject
    (
        "U",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);


#include "createPhi.H"


label pRefCell = 0;
scalar pRefValue = 0.0;
setRefCell(p, mesh.solution().dict().subDict("PISO"), pRefCell, pRefValue);
mesh.schemes().setFluxRequired(p.name());

const labelList& porousCells = mesh.cellZones()[0];

Info<< "Creating D\n"<< endl;//Darcy momentum coefficient
volScalarField::Internal D
(
    IOobject
    (
        "D",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh,
    dimensionedScalar("D", dimViscosity/dimArea, 0.0)
);
//precalculate for efficiency
scalar dNu = 1000*nu.value(); //nu is dimScalar

forAll(porousCells,i)
{
    D[porousCells[i]] = dNu;
}
    
        
