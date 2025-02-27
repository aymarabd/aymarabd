Info<< "Reading bubbleProperties\n" << endl;

IOdictionary bubbleProperties
(
    IOobject
    (
        "bubbleProperties",
        runTime.constant(),
        mesh,
        IOobject::MUST_READ,
        IOobject::NO_WRITE
    )
);

const dictionary& bubbleDict(bubbleProperties.subDict("bubble"));
const vector centre(bubbleDict.lookup("centre"));

const scalar radius(bubbleDict.lookup<scalar>("radius"));
scalar pB(bubbleDict.lookup<scalar>("p"));
scalar TB (bubbleDict.lookup<scalar>("T"));

const dictionary& liquidDict(bubbleProperties.subDict("liquid"));
const scalar height(liquidDict.lookup<scalar>("height"));
const scalar pL(liquidDict.lookup<scalar>("p"));
const scalar TL(liquidDict.lookup<scalar>("T"));

Info<< "Reading field p\n" << endl;
volScalarField p
(
    IOobject
    (
        "p", //name that it looks for
        runTime.timeName(), //usually reads from 0 but checks time first in runTime
        mesh, //name of object
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

p=dimensioned<scalar>("pL", p.dimensions(), pL);
//p=dimensioned<scalar>("pL", dimPressure, pL);

Info<< "Reading field p_rgh\n" << endl;
volScalarField p_rgh
(
    IOobject
    (
        "p_rgh",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
       args.optionFound("noWritePrgh")
      ? IOobject::NO_WRITE
      : IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading field alpha.water\n" << endl;
volScalarField alpha //cannot be alpha.water
(
    IOobject
    (
        "alpha.water",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading field T\n" << endl;
volScalarField T
(
    IOobject
    (
        "T", 
        runTime.timeName(),
        mesh, 
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

T=dimensioned<scalar>("TL", T.dimensions(), TL);
alpha = 1; //initially we say it is all water
