from base_simulation import BaseSimbox, BaseCircle
from renderers import SimDisplayer, SimExporter
from extras import random_vectors_in_circle
class Tests:

    def __init__(self):
        # basic scene setup for testing
        self.basic_scene = BaseSimbox(radius=100,boundary_color=(255, 255, 255), boundary_thickness=1, steps_per_frame=1,
                       amount=5,
                       positions=[[1, 5], [-1, 1], [5, 6], [9, 0], [3, 3]],
                       sizes=[5, 5, 9, 5, 5],
                       speeds=[1, 1, 1, 2, 3],
                       angles=[0.73, -0.6, 2.87, 3, -1],
                       vectors=None,
                       weights=[1, 1, 5, 1, 1],
                       damping=[0, 0, 0, 0, 0],
                       colors=[(60, 120, 250) for _ in range(5)])

    def test_basic_video_ability(self):
        sim = SimExporter("test_002", self.basic_scene, resolution=5, seconds_to_run=10, quit_hotkey='q')
        sim.run_sim()

    def test_display_ability(self):
        SimDisplayer(self.basic_scene).run_live_sim()

    def test_stress_test(self):
        import random
        amount = 500
        radius = 100
        boundary_color = (255, 255, 255); boundary_thickness = 1
        positions = random_vectors_in_circle(amount, radius)
        sizes = [2 for _ in range(amount)]
        speeds = [1 for _ in range(amount)]
        angles = [random.random() * 6.28 for _ in range(amount)]
        weights = [1 for _ in range(amount)]
        damping = [0.2 for _ in range(amount)]
        colors = [(60, 120, 250) for _ in range(amount)]
        sim = BaseSimbox(radius=radius, boundary_color=boundary_color, boundary_thickness=boundary_thickness, steps_per_frame=1,
                   amount=amount, positions=positions, sizes=sizes, angles=angles, speeds=speeds, vectors=None,
                   weights=weights, damping=damping, colors=colors)
        #SimDisplayer(simbox=sim, resolution=5, fps=30).run_live_sim()
        SimExporter("test_004", sim, seconds_to_run=4).run_sim()

    def test_steps_per_frame(self):
        self.basic_scene.steps_per_frame = 5 # test for 1, 5, 50, 5000
        SimDisplayer(simbox=self.basic_scene).run_live_sim()

    def test_adding_circle(self):
        class AddCircle(BaseSimbox):
            def simulate_frame(self):
                super(AddCircle, self).simulate_frame()
                if not self.current_frame % 20:
                    self.add_circle(BaseCircle(angle=1, speed=4))

        sim = AddCircle(radius=100, boundary_color=(255, 255, 255), boundary_thickness=1, steps_per_frame=1,
                   amount=5,
                   positions=[[1, 5], [-1, 1], [5, 6], [9, 0], [3, 3]],
                   sizes=[5, 5, 9, 5, 5],
                   speeds=[1, 1, 1, 2, 3],
                   angles=[0.73, -0.6, 2.87, 3, -1],
                   vectors=None,
                   weights=[1, 1, 5, 1, 1],
                   damping=[0, 0, 0, 0, 0],
                   colors=[(60, 120, 250) for _ in range(5)])

        SimDisplayer(simbox=sim).run_live_sim()

    def test_overlapping_circles(self):
        import numpy as np
        collider1 = BaseCircle(simbox=self.basic_scene, angle=-2.2, speed=3, radius=6)
        collider1.position = np.array([1., 0.4])
        collider2 = BaseCircle(simbox=self.basic_scene, angle=1, speed=4, radius=6)
        collider2.position = np.array([1., 0.])
        self.basic_scene.circles.clear()
        self.basic_scene.circles.append(collider1)
        self.basic_scene.circles.append(collider2)
        SimDisplayer(simbox=self.basic_scene, fps=1).run_live_sim()

    def test_high_speeds(self):
        for c in self.basic_scene.circles:
            c.vector *= 10
        SimDisplayer(simbox=self.basic_scene).run_live_sim()

    def test_damping(self):
        for c in self.basic_scene.circles:
            c.damping = 0.2
        SimDisplayer(simbox=self.basic_scene).run_live_sim()

if __name__ == '__main__':
    Tests().test_display_ability()