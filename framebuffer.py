import pygame


RGB565 = 1


class FrameBuffer:

    def __init__(self, buffer, width, height, format):
        self.buffer = buffer
        self.width = width
        self.height = height
        self.format = format
        self.cached = None


    # -----------------------------
    # Pixel access
    # -----------------------------

    def pixel(self, x, y, color=None):

        if x < 0 or y < 0:
            return None

        if x >= self.width or y >= self.height:
            return None


        index = (y * self.width + x) * 2


        # SET PIXEL
        if color is not None:

            self.buffer[index] = (color >> 8) & 0xff
            self.buffer[index + 1] = color & 0xff

            self.cached = None
            return


        # GET PIXEL
        return (
            self.buffer[index] << 8 |
            self.buffer[index + 1]
        )


    # -----------------------------
    # Fill
    # -----------------------------

    def fill(self, color):

        for y in range(self.height):

            for x in range(self.width):

                self.pixel(x, y, color)



    # -----------------------------
    # Lines
    # -----------------------------

    def hline(self, x, y, length, color):

        for i in range(length):
            self.pixel(x + i, y, color)



    def vline(self, x, y, length, color):

        for i in range(length):
            self.pixel(x, y + i, color)



    def line(self, x1, y1, x2, y2, color):

        # Simple Bresenham line

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        err = dx - dy


        while True:

            self.pixel(x1, y1, color)

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x1 += sx

            if e2 < dx:
                err += dx
                y1 += sy



    # -----------------------------
    # Rectangle
    # -----------------------------

    def rect(self, x, y, w, h, color, fill=False):

        if fill:

            for yy in range(y, y + h):

                for xx in range(x, x + w):

                    self.pixel(xx, yy, color)

        else:

            self.hline(x, y, w, color)
            self.hline(x, y + h - 1, w, color)

            self.vline(x, y, h, color)
            self.vline(x + w - 1, y, h, color)



    # -----------------------------
    # RGB565 -> RGB888
    # -----------------------------

    def rgb565(self, color):

        r = ((color >> 11) & 0x1F) << 3
        g = ((color >> 5) & 0x3F) << 2
        b = (color & 0x1F) << 3

        return (r, g, b)



    # -----------------------------
    # Convert framebuffer to pygame
    # -----------------------------

    def to_surface(self, transparent=None):

        if self.cached is not None:
            return self.cached


        surface = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )


        for y in range(self.height):

            for x in range(self.width):

                color = self.pixel(x, y)


                if color is None:
                    continue


                if transparent is not None and color == transparent:

                    surface.set_at(
                        (x, y),
                        (0, 0, 0, 0)
                    )

                else:

                    surface.set_at(
                        (x, y),
                        self.rgb565(color)
                    )


        self.cached = surface

        return surface
