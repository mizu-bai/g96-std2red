from dataclasses import dataclass

import numpy as np

from .libg96 import G96Mol
import warnings

warnings.warn(
    "\n"
    ">>> This package shall only be used in processing **WRONG** g96 files "
    "generated by such command:\n"
    ">>> $ gmx trjconv -f traj.trr -s mol.tpr -o traj.g96 -sep\n"
    ">>> Assuming users clearly know what they are doing."
)

@dataclass
class WrongG96Mol(G96Mol):
    @staticmethod
    def from_file(
        file: str,
    ) -> "G96Mol":
        """Load molecule from input **WRONG** g96 file.

        Args:
            file (str): Path to input g96 file

        Returns:
            g96_mol (G96Mol): A g96 molecule
        """
        title = ""
        timestep = [0, 0.0]
        position = []
        velocity = []
        box_vector = np.zeros(3)

        with open(file, "r") as f:
            while line := f.readline():
                # title
                """WRONG g96 file contains NO TIMESTEP section. Alternatively,
                parsing from TITLE section.
                """
                if "TITLE" in line:
                    line = f.readline()
                    (title, timestep) = line.rstrip().split("t=")
                    timestep = timestep.split("step=")
                    timestep = [int(timestep[1]), float(timestep[0])]
                    continue

                # time step
                # if "TIMESTEP" in line:
                #     line = f.readline()
                #     timestep = line.split()
                #     timestep = [int(timestep[0]), float(timestep[1])]
                #     continue

                # position
                """In WRONG g96 file, the POSITIONRED identifier loses its RED
                suffix.
                """
                # if "POSITIONRED" in line:
                if "POSITION" in line:
                    while True:
                        line = f.readline()

                        if "END" in line:
                            break

                        """The last 3 columns contains the positions needed."""
                        position.append([float(x) for x in line.split()[-3:]])

                    continue
                """In WRONG g96 file, the VELOCITYRED identifier loses its RED
                suffix.
                """
                # if "VELOCITYRED" in line:
                if "VELOCITY" in line:
                    while True:
                        line = f.readline()

                        if "END" in line:
                            break
                        
                        """The last 3 columns contains the positions needed."""
                        velocity.append([float(x) for x in line.split()[-3:]])

                    continue

                """Thankfully, nothing goes wrong in the BOX section."""
                if "BOX" in line:
                    line = f.readline()
                    box_vector = np.array([float(x) for x in line.split()])
                    continue

        position = np.array(position)

        if len(position) != len(velocity):
            velocity = np.zeros_like(position)

        return G96Mol(
            title=title,
            timestep=timestep,
            position=position,
            velocity=velocity,
            box_vector=box_vector,
        )
