from dataclasses import dataclass, field
from typing import Tuple

import numpy as np


@dataclass
class G96Mol:
    title: str
    timestep: Tuple[int, float]
    position: np.array  # nm
    velocity: np.array  # nm/ps
    box_vector: np.array = field(default_factory=lambda: np.zeros(3))

    def __str__(self) -> str:
        contents = []

        # title
        contents.append("TITLE")
        contents.append(self.title)
        contents.append("END")

        # timestep
        contents.append("TIMESTEP")
        contents.append(f"{self.timestep[0]:15d}{self.timestep[1]:15.6f}")
        contents.append("END")

        # position
        contents.append("POSITIONRED")

        for pos in self.position:
            contents.append(f"{pos[0]:15.9f}{pos[1]:15.9f}{pos[2]:15.9f}")

        contents.append("END")

        # velocity
        contents.append("VELOCITYRED")

        for vel in self.velocity:
            contents.append(f"{vel[0]:15.9f}{vel[1]:15.9f}{vel[2]:15.9f}")

        contents.append("END")

        # box
        contents.append("BOX")
        contents.append(
            f"{self.box_vector[0]:15.9f}"
            f"{self.box_vector[1]:15.9f}"
            f"{self.box_vector[2]:15.9f}"
        )
        contents.append("END")

        return "\n".join(contents)

    @staticmethod
    def from_file(
        file: str,
    ) -> "G96Mol":
        """Load molecule from input g96 file.

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
                if "TITLE" in line:
                    line = f.readline()
                    title = line.rstrip()
                    continue

                # time step
                if "TIMESTEP" in line:
                    line = f.readline()
                    timestep = line.split()
                    timestep = [int(timestep[0]), float(timestep[1])]
                    continue

                # position
                if "POSITIONRED" in line:
                    while True:
                        line = f.readline()

                        if "END" in line:
                            break

                        position.append([float(x) for x in line.split()])

                    continue

                if "VELOCITYRED" in line:
                    while True:
                        line = f.readline()

                        if "END" in line:
                            break

                        velocity.append([float(x) for x in line.split()])

                    continue

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
