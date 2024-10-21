from base_simulation import BaseRenderer
import numpy as np
import pygame as pg, sys
import cv2, keyboard

class SimDisplayer(BaseRenderer):

    def __init__(self, simbox, resolution=5, fps=30):

        super().__init__(simbox, resolution)
        self.PAUSE = False
        self.FPS = fps

        # this will hold the screen / window after self.initialize is called
        self.screen = None

    def _initialize(self):
        # Initializes pygame
        pg.init()

        # Initialize display window
        self.screen = pg.display.set_mode((self.size, self.size))

        # Set caption title
        pg.display.set_caption("Circle sim")

    def run_live_sim(self):
        self._initialize()
        # clock ensures adherence to self.FPS. (bounds the upper limit of sim framerate to self.FPS)
        clock = pg.time.Clock()
        while True:
            # check if the x-button has been clicked
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                # check if "space key" was pressed. toggles pause
                elif event.type == pg.KEYUP:  # Key release event
                    if event.key == pg.K_SPACE:  # Space bar release
                        self.toggle_pause()

            if not self.PAUSE:
                self.simbox.simulate_frame()

                # renders current state of sim
                frame = self.render_frame()

                # displays frame
                self._display_frame(frame)

                clock.tick(self.FPS)

    def toggle_pause(self):
        self.PAUSE = not self.PAUSE

    def _display_frame(self, image):

        # convert from pillow.image to pg.image (pg.surface)
        image_data = image.tobytes()
        pg_surface = pg.image.fromstring(image_data, image.size, image.mode)

        # Draw the surface onto the screen
        self.screen.blit(pg_surface, (0, 0))

        # Update the display
        pg.display.flip()

    def close(self):
        pg.quit()
        sys.exit()

class SimExporter(BaseRenderer):
    def __init__(self, name, simbox, fps=30, resolution=5, seconds_to_run=20, quit_hotkey='q'):
        super().__init__(simbox, resolution)
        self.FPS = fps
        self.name = name
        self.seconds_to_run = seconds_to_run
        self.quit_hotkey = quit_hotkey

        self.video_writer = None

    def _initialize(self):
        self.video_writer = cv2.VideoWriter(f"{self.name}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), self.FPS,
                        (self.size, self.size))

    def run_sim(self):
        self._initialize()
        c = 0
        # progress bar var
        max_blocks = 40
        while c < self.seconds_to_run * self.FPS:
            c += 1
            percentage_done = c / (self.seconds_to_run * self.FPS)
            # update the progress-bar
            print('\r' + int(percentage_done * max_blocks) * '\u2588' + (max_blocks - int(percentage_done * max_blocks))*'-', end='')

            self.simbox.simulate_frame()
            frame = self.render_frame()
            self._write_frame(frame)
            # early quitting... in case of long wait time )-:
            if keyboard.is_pressed(self.quit_hotkey):
                self.close()
        self.close()

    def _write_frame(self, frame):
        # Convert PIL image to NumPy array
        frame_array = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        self.video_writer.write(frame_array)

    def close(self):
        self.video_writer.release()
        sys.exit()

