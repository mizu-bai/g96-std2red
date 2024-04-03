# g96-std2red

Standard `g96` to reduced `g96` convertor

## Introduction

The standard `g96` file be like:

```
TITLE
water box t=   0.00000 step= 0
END
POSITION
    1 SOL   OW         1    1.254972935    1.057989001    0.208974004
    1 SOL   HW1        2    1.187444448    1.026183486    0.142428458
    1 SOL   HW2        3    1.316985607    0.982989311    0.231984317
    ...
END
VELOCITY
    1 SOL   OW         1   -0.506096125    0.238763660    0.594447911
    1 SOL   HW1        2   -0.246476635   -1.150003195    0.962777019
    1 SOL   HW2        3    1.235615849    1.495466352    0.204018727
    ...
END
BOX
    2.976279974    2.976279974    2.976279974
END
```

Then we want to convert it into reduced format

```
TITLE
water box 
END
TIMESTEP
              0       0.000000
END
POSITIONRED
    1.254972935    1.057989001    0.208974004
    1.187444448    1.026183486    0.142428458
    1.316985607    0.982989311    0.231984317
    ...
END
VELOCITYRED
   -0.506096125    0.238763660    0.594447911
   -0.246476635   -1.150003195    0.962777019
    1.235615849    1.495466352    0.204018727
    ....
END
BOX
    2.976279974    2.976279974    2.976279974
END
```

## Usage

```bash
$ python3 g96_std2red.py mol.g96  # single standard g96 file
$ python3 g96_std2red.py mol1.g96 mol2.g96 ...  # a list of standard g96 files
$ python3 g96_std2red.py *.g96  # match by pattern
```

## Reference

(1) Abraham, M. J.; Murtola, T.; Schulz, R.; Páll, S.; Smith, J. C.; Hess, B.; Lindahl, E. GROMACS: High Performance Molecular Simulations through Multi-Level Parallelism from Laptops to Supercomputers. SoftwareX 2015, 1–2, 19–25. https://doi.org/10.1016/j.softx.2015.06.001.

(1) Scott, W. R. P.; Hünenberger, P. H.; Tironi, I. G.; Mark, A. E.; Billeter, S. R.; Fennen, J.; Torda, A. E.; Huber, T.; Krüger, P.; van Gunsteren, W. F. The GROMOS Biomolecular Simulation Program Package. J. Phys. Chem. A 1999, 103 (19), 3596–3607. https://doi.org/10.1021/jp984217f.

## License

BSD-2-Clause license
