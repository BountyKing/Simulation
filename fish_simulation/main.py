import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class Fish:
    def __init__(self, identifier, c0, v0):
        self.id = identifier
        self.c = np.array(c0)
        self.v = np.array(v0)
        self.d = self.v
        self.dr = np.zeros(self.d.shape)
        self.do = np.zeros(self.d.shape)
        self.da = np.zeros(self.d.shape)
        self.zor = []
        self.zoo = []
        self.zoa = []

    def reset(self):
        self.d = self.v
        self.dr = np.zeros(self.d.shape)
        self.do = np.zeros(self.d.shape)
        self.da = np.zeros(self.d.shape)
        self.zor = []
        self.zoo = []
        self.zoa = []

    def near_fish(self):
        for k in range(self.id, num_elements):
            if not k == self.id:
                if FISH[k].in_zone(self, 0):
                    self.zor.append(FISH[k])
                    FISH[k].zor.append(self)
                elif FISH[k].in_zone(self, 1):
                    self.zoo.append(FISH[k])
                    FISH[k].zoo.append(self)
                elif FISH[k].in_zone(self, 2):
                    self.zoa.append(FISH[k])
                    FISH[k].zoa.append(self)

    def update_directions(self):
        nr = len(self.zor)
        no = len(self.zoo)
        na = len(self.zoa)
        if not nr == 0:
            for k in range(nr):
                rij = (self.zor[k].c - self.c) / np.linalg.norm(self.zor[k].c - self.c)
                self.dr -= rij / np.linalg.norm(rij)
        elif not (no == 0 and na == 0):
            for k in range(no):
                self.do += self.zoo[k].v / np.linalg.norm(self.zoo[k].v)
            for k in range(na):
                rij = (self.zoa[k].c - self.c) / np.linalg.norm(self.zoa[k].c - self.c)
                self.da += rij / np.linalg.norm(rij)

    def update_velocity(self):
        nr = len(self.zor)
        no = len(self.zoo)
        na = len(self.zoa)
        if not nr == 0:
            self.d = self.dr
        elif nr == 0 and (not no == 0 or not na == 0):
            self.d = 0.5 * (self.do + self.da)
        else:
            self.d = self.v

        theta_vd = (np.arccos(np.dot(self.v, self.d) / (np.linalg.norm(self.v) * np.linalg.norm(self.d)))
                    + np.random.normal(0, deviation)) * np.sign(np.cross(self.v, self.d))

        if np.abs(theta_vd) <= theta_max * tau:
            self.v = self.d
        else:
            if theta_vd <= 0:
                theta_rot = -theta_max
            else:
                theta_rot = theta_max

            rot = np.array([[np.cos(theta_rot * tau), -np.sin(theta_rot * tau)],
                            [np.sin(theta_rot * tau), np.cos(theta_rot * tau)]])
            self.v = np.dot(rot, self.v)

        for dim in range(self.c.shape[0]):
            if ((self.c[dim] - radius_collision <= 0.0 and self.v[dim] <= 0.0) or
                    (self.c[dim] + radius_collision >= L_box and self.v[dim] >= 0.0)):
                self.v[dim] *= -1.0
        self.v = speed_normalize(self.v)

    def update_position(self):
        self.c += self.v*tau

    def in_zone(self, fish, zone_id):
        if zone_id == 0:
            return np.linalg.norm(self.c-fish.c) <= radius_collision
        elif zone_id == 1:
            return np.linalg.norm(self.c-fish.c) <= radius_orientation
        elif zone_id == 2:
            return np.linalg.norm(self.c-fish.c) <= radius_attraction

    def trace(self, plot):
        plot.scatter(self.c[0], self.c[1], color="black", edgecolor="none", s=10)
        plt.quiver(self.c[0], self.c[1], -self.v[0], -self.v[1], angles="uv",
                   width=5, headlength=5, headaxislength=5, units="dots", minlength=0,
                   headwidth=1)


def speed_normalize(speed):
    speed /= np.linalg.norm(speed)
    return coeff_speed*speed


def animation_function(frame):
    fig.clear()
    plt.xlim(0, L_box)
    plt.ylim(0, L_box)
    plt.text(0.01, 0.01, f"{frame}", color="red")

    velocity_mean = 0.0
    for j in range(num_elements):
        FISH[j].reset()

    for j in range(num_elements):
        FISH[j].near_fish()

    for j in range(num_elements):
        FISH[j].update_directions()
        FISH[j].update_velocity()
        FISH[j].update_position()
        FISH[j].trace(plt)


num_elements = 50
theta_max = np.pi/3
deviation = np.pi/50
tau = 0.2
L_box = 100

radius_collision = 2.0
radius_orientation = 10.0
radius_attraction = 20.0

coeff_speed = 10.0

C0 = np.random.rand(2, num_elements)*L_box
V0 = speed_normalize((np.random.rand(2, num_elements)*2-1.))
FISH = []
for i in range(num_elements):
    FISH.append(Fish(i, C0[:, i], V0[:, i]))

fig, ax = plt.subplots()
plt.axis("off")
plt.tight_layout(pad=0)

ani = FuncAnimation(fig, animation_function, interval=20, frames=500)
plt.show()
