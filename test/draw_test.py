import unittest
import sys

import pygame
from pygame import draw
from pygame import draw_py
from pygame.locals import SRCALPHA
from pygame.tests import test_utils
from pygame.math import Vector2

PY3 = sys.version_info >= (3, 0, 0)

RED = BG_RED = pygame.Color('red')
GREEN = FG_GREEN = pygame.Color('green')


def get_border_values(surface, width, height):
    """Returns a list containing lists with the values of the surface's
    borders.
    """
    border_top = [surface.get_at((x, 0)) for x in range(width)]
    border_left = [surface.get_at((0, y)) for y in range(height)]
    border_right = [
        surface.get_at((width - 1, y)) for y in range(height)]
    border_bottom = [
        surface.get_at((x, height - 1)) for x in range(width)]

    return [border_top, border_left, border_right, border_bottom]


def corners(surface):
    """Returns a tuple with the corner positions of the given surface.

    Clockwise from the top left corner.
    """
    width, height = surface.get_size()
    return ((0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1))


def rect_corners_mids_and_center(rect):
    """Returns a tuple with each corner, mid, and the center for a given rect.

    Clockwise from the top left corner and ending with the center point.
    """
    return (rect.topleft, rect.midtop, rect.topright, rect.midright,
            rect.bottomright, rect.midbottom, rect.bottomleft,
            rect.midleft, rect.center)


def border_pos_and_color(surface):
    """Yields each border position and its color for a given surface.

    Clockwise from the top left corner.
    """
    width, height = surface.get_size()
    right, bottom = width - 1, height - 1

    # Top edge.
    for x in range(width):
        pos = (x, 0)
        yield pos, surface.get_at(pos)

    # Right edge.
    # Top right done in top edge loop.
    for y in range(1, height):
        pos = (right, y)
        yield pos, surface.get_at(pos)

    # Bottom edge.
    # Bottom right done in right edge loop.
    for x in range(right - 1, -1, -1):
        pos = (x, bottom)
        yield pos, surface.get_at(pos)

    # Left edge.
    # Bottom left done in bottom edge loop. Top left done in top edge loop.
    for y in range(bottom - 1, 0, -1):
        pos = (0, y)
        yield pos, surface.get_at(pos)


class DrawTestCase(unittest.TestCase):
    """Base class to test draw module functions."""
    draw_rect    = staticmethod(draw.rect)
    draw_polygon = staticmethod(draw.polygon)
    draw_circle  = staticmethod(draw.circle)
    draw_ellipse = staticmethod(draw.ellipse)
    draw_arc     = staticmethod(draw.arc)
    draw_line    = staticmethod(draw.line)
    draw_lines   = staticmethod(draw.lines)
    draw_aaline  = staticmethod(draw.aaline)
    draw_aalines = staticmethod(draw.aalines)


class PythonDrawTestCase(unittest.TestCase):
    """Base class to test draw_py module functions."""
    # draw_py is currently missing some functions.
    #draw_rect    = staticmethod(draw_py.draw_rect)
    draw_polygon = staticmethod(draw_py.draw_polygon)
    #draw_circle  = staticmethod(draw_py.draw_circle)
    #draw_ellipse = staticmethod(draw_py.draw_ellipse)
    #draw_arc     = staticmethod(draw_py.draw_arc)
    draw_line    = staticmethod(draw_py.draw_line)
    draw_lines   = staticmethod(draw_py.draw_lines)
    draw_aaline  = staticmethod(draw_py.draw_aaline)
    draw_aalines = staticmethod(draw_py.draw_aalines)


### Ellipse Testing ###########################################################

class DrawEllipseMixin(object):
    """Mixin tests for drawing ellipses.

    This class contains all the general ellipse drawing tests.
    """
    def test_ellipse__args(self):
        """Ensures draw ellipse accepts the correct args."""
        bounds_rect = self.draw_ellipse(pygame.Surface((3, 3)),
            (0, 10, 0, 50), pygame.Rect((0, 0), (3, 2)), 1)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_ellipse__args_without_width(self):
        """Ensures draw ellipse accepts the args without a width."""
        bounds_rect = self.draw_ellipse(pygame.Surface((2, 2)), (1, 1, 1, 99),
                                        pygame.Rect((1, 1), (1, 1)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_ellipse__kwargs(self):
        """Ensures draw ellipse accepts the correct kwargs
        with and without a width arg.
        """
        kwargs_list = [{'surface' : pygame.Surface((4, 4)),
                        'color'   : pygame.Color('yellow'),
                        'rect'    : pygame.Rect((0, 0), (3, 2)),
                        'width'   : 1 },

                       {'surface' : pygame.Surface((2, 1)),
                        'color'   : (0, 10, 20),
                        'rect'    : (0, 0, 1, 1)}]

        for kwargs in kwargs_list:
            bounds_rect = self.draw_ellipse(**kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_ellipse__kwargs_order_independent(self):
        """Ensures draw ellipse's kwargs are not order dependent."""
        bounds_rect = self.draw_ellipse(color=(1, 2, 3),
                                        surface=pygame.Surface((3, 2)),
                                        width=0,
                                        rect=pygame.Rect((1, 0), (1, 1)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_ellipse__args_missing(self):
        """Ensures draw ellipse detects any missing required args."""
        surface = pygame.Surface((1, 1))

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_ellipse(surface, pygame.Color('red'))

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_ellipse(surface)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_ellipse()

    def test_ellipse__kwargs_missing(self):
        """Ensures draw ellipse detects any missing required kwargs."""
        kwargs = {'surface' : pygame.Surface((1, 2)),
                  'color'   : pygame.Color('red'),
                  'rect'    : pygame.Rect((1, 0), (2, 2)),
                  'width'   : 2}

        for name in ('rect', 'color', 'surface'):
            invalid_kwargs = dict(kwargs)
            invalid_kwargs.pop(name)  # Pop from a copy.

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_ellipse(**invalid_kwargs)

    def test_ellipse__arg_invalid_types(self):
        """Ensures draw ellipse detects invalid arg types."""
        surface = pygame.Surface((2, 2))
        color = pygame.Color('blue')
        rect = pygame.Rect((1, 1), (1, 1))

        with self.assertRaises(TypeError):
            # Invalid width.
            bounds_rect = self.draw_ellipse(surface, color, rect, '1')

        with self.assertRaises(TypeError):
            # Invalid rect.
            bounds_rect = self.draw_ellipse(surface, color, (1, 2, 3, 4, 5), 1)

        with self.assertRaises(TypeError):
            # Invalid color.
            bounds_rect = self.draw_ellipse(surface, 'blue', rect, 0)

        with self.assertRaises(TypeError):
            # Invalid surface.
            bounds_rect = self.draw_ellipse(rect, color, rect, 2)

    def test_ellipse__kwarg_invalid_types(self):
        """Ensures draw ellipse detects invalid kwarg types."""
        surface = pygame.Surface((3, 3))
        color = pygame.Color('green')
        rect = pygame.Rect((0, 1), (1, 1))
        kwargs_list = [{'surface' : pygame.Surface,  # Invalid surface.
                        'color'   : color,
                        'rect'    : rect,
                        'width'   : 1 },

                       {'surface' : surface,
                        'color'   : 'green',  # Invalid color.
                        'rect'    : rect,
                        'width'   : 1 },

                       {'surface' : surface,
                        'color'   : color,
                        'rect'    : (0, 0, 0),  # Invalid rect.
                        'width'   : 1 },

                       {'surface' : surface,
                        'color'   : color,
                        'rect'    : rect,
                        'width'   : 1.1 }]  # Invalid width.

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_ellipse(**kwargs)

    def test_ellipse__kwarg_invalid_name(self):
        """Ensures draw ellipse detects invalid kwarg names."""
        surface = pygame.Surface((2, 3))
        color = pygame.Color('cyan')
        rect = pygame.Rect((0, 1), (2, 2))
        kwargs_list = [{'surface' : surface,
                        'color'   : color,
                        'rect'    : rect,
                        'width'   : 1,
                        'invalid' : 1},

                       {'surface' : surface,
                        'color'   : color,
                        'rect'    : rect,
                        'invalid' : 1 }]

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_ellipse(**kwargs)

    def test_ellipse__args_and_kwargs(self):
        """Ensures draw ellipse accepts a combination of args/kwargs"""
        surface = pygame.Surface((3, 1))
        color = (255, 255, 0, 0)
        rect = pygame.Rect((1, 0), (2, 1))
        width = 0
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'rect'    : rect,
                  'width'   : width}

        for name in ('surface', 'color', 'rect', 'width'):
            kwargs.pop(name)

            if 'surface' == name:
                bounds_rect = self.draw_ellipse(surface, **kwargs)
            elif 'color' == name:
                bounds_rect = self.draw_ellipse(surface, color, **kwargs)
            elif 'rect' == name:
                bounds_rect = self.draw_ellipse(surface, color, rect, **kwargs)
            else:
                bounds_rect = self.draw_ellipse(surface, color, rect, width,
                                                **kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    # This decorator can be removed when the ellipse portion of issues #975
    # and #976 are resolved.
    @unittest.expectedFailure
    def test_ellipse__valid_width_values(self):
        """Ensures draw ellipse accepts different width values."""
        pos = (1, 1)
        surface_color = pygame.Color('white')
        surface = pygame.Surface((3, 4))
        color = (10, 20, 30, 255)
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'rect'    : pygame.Rect(pos, (3, 1)),
                  'width'   : None}

        for width in (-1000, -10, -1, 0, 1, 10, 1000):
            surface.fill(surface_color)  # Clear for each test.
            kwargs['width'] = width
            expected_color = color if width >= 0 else surface_color

            bounds_rect = self.draw_ellipse(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_ellipse__valid_rect_formats(self):
        """Ensures draw ellipse accepts different rect formats."""
        pos = (1, 1)
        expected_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((4, 4))
        kwargs = {'surface' : surface,
                  'color'   : expected_color,
                  'rect'    : None,
                  'width'   : 0}
        rects = (pygame.Rect(pos, (1, 3)), (pos, (2, 1)),
                 (pos[0], pos[1], 1, 1))

        for rect in rects:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['rect'] = rect

            bounds_rect = self.draw_ellipse(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_ellipse__valid_color_formats(self):
        """Ensures draw ellipse accepts different color formats."""
        pos = (1, 1)
        green_color = pygame.Color('green')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        kwargs = {'surface' : surface,
                  'color'   : None,
                  'rect'    : pygame.Rect(pos, (1, 2)),
                  'width'   : 0}
        reds = ((0, 255, 0), (0, 255, 0, 255), surface.map_rgb(green_color),
                green_color)

        for color in reds:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['color'] = color

            if isinstance(color, int):
                expected_color = surface.unmap_rgb(color)
            else:
                expected_color = green_color

            bounds_rect = self.draw_ellipse(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_ellipse__invalid_color_formats(self):
        """Ensures draw ellipse handles invalid color formats correctly."""
        pos = (1, 1)
        surface_color = pygame.Color('black')
        surface = pygame.Surface((4, 3))
        kwargs = {'surface' : surface,
                  'color'   : None,
                  'rect'    : pygame.Rect(pos, (2, 2)),
                  'width'   : 1}

        # These color formats are currently not supported (it would be
        # nice to eventually support them).
        for expected_color in ('green', '#00FF00FF', '0x00FF00FF'):
            kwargs['color'] = expected_color

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_ellipse(**kwargs)

    def test_ellipse(self):
        """Tests ellipses of differing sizes on surfaces of differing sizes.

        Checks if the number of sides touching the border of the surface is
        correct.
        """
        left_top = [(0, 0), (1, 0), (0, 1), (1, 1)]
        sizes = [(4, 4), (5, 4), (4, 5), (5, 5)]
        color = (1, 13, 24, 255)

        def same_size(width, height, border_width):
            """Test for ellipses with the same size as the surface."""
            surface = pygame.Surface((width, height))

            self.draw_ellipse(surface, color, (0, 0, width, height),
                              border_width)

            # For each of the four borders check if it contains the color
            borders = get_border_values(surface, width, height)
            for border in borders:
                self.assertTrue(color in border)

        def not_same_size(width, height, border_width, left, top):
            """Test for ellipses that aren't the same size as the surface."""
            surface = pygame.Surface((width, height))

            self.draw_ellipse(surface, color,
                              (left, top, width - 1, height - 1), border_width)

            borders = get_border_values(surface, width, height)

            # Check if two sides of the ellipse are touching the border
            sides_touching = [
                color in border for border in borders].count(True)
            self.assertEqual(sides_touching, 2)

        for width, height in sizes:
            for border_width in (0, 1):
                same_size(width, height, border_width)
                for left, top in left_top:
                    not_same_size(width, height, border_width, left, top)

    def _check_1_pixel_sized_ellipse(self, surface, collide_rect,
                                     surface_color, ellipse_color):
        # Helper method to check the surface for 1 pixel wide and/or high
        # ellipses.
        surf_w, surf_h = surface.get_size()

        surface.lock()  # For possible speed up.

        for pos in ((x, y) for y in range(surf_h) for x in range(surf_w)):
            # Since the ellipse is just a line we can use a rect to help find
            # where it is expected to be drawn.
            if collide_rect.collidepoint(pos):
                expected_color = ellipse_color
            else:
                expected_color = surface_color

            self.assertEqual(surface.get_at(pos), expected_color,
                'collide_rect={}, pos={}'.format(collide_rect, pos))

        surface.unlock()

    def test_ellipse__1_pixel_width(self):
        """Ensures an ellipse with a width of 1 is drawn correctly.

        An ellipse with a width of 1 pixel is a vertical line.
        """
        ellipse_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surf_w, surf_h = 10, 20

        surface = pygame.Surface((surf_w, surf_h))
        rect = pygame.Rect((0, 0), (1, 0))
        collide_rect = rect.copy()

        # Calculate some positions.
        off_left = -1
        off_right = surf_w
        off_bottom = surf_h
        center_x = surf_w // 2
        center_y = surf_h // 2

        # Test some even and odd heights.
        for ellipse_h in range(6, 10):
            # The ellipse is drawn on the edge of the rect so collide_rect
            # needs +1 height to track where it's drawn.
            collide_rect.h = ellipse_h + 1
            rect.h = ellipse_h

            # Calculate some variable positions.
            off_top = -(ellipse_h + 1)
            half_off_top = -(ellipse_h // 2)
            half_off_bottom = surf_h - (ellipse_h // 2)

            # Draw the ellipse in different positions: fully on-surface,
            # partially off-surface, and fully off-surface.
            positions = ((off_left, off_top),
                         (off_left, half_off_top),
                         (off_left, center_y),
                         (off_left, half_off_bottom),
                         (off_left, off_bottom),

                         (center_x, off_top),
                         (center_x, half_off_top),
                         (center_x, center_y),
                         (center_x, half_off_bottom),
                         (center_x, off_bottom),

                         (off_right, off_top),
                         (off_right, half_off_top),
                         (off_right, center_y),
                         (off_right, half_off_bottom),
                         (off_right, off_bottom))

            for rect_pos in positions:
                surface.fill(surface_color)  # Clear before each draw.
                rect.topleft = rect_pos
                collide_rect.topleft = rect_pos

                self.draw_ellipse(surface, ellipse_color, rect)

                self._check_1_pixel_sized_ellipse(surface, collide_rect,
                                                  surface_color, ellipse_color)

    def test_ellipse__1_pixel_width_spanning_surface(self):
        """Ensures an ellipse with a width of 1 is drawn correctly
        when spanning the height of the surface.

        An ellipse with a width of 1 pixel is a vertical line.
        """
        ellipse_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surf_w, surf_h = 10, 20

        surface = pygame.Surface((surf_w, surf_h))
        rect = pygame.Rect((0, 0), (1, surf_h + 2))  # Longer than the surface.

        # Draw the ellipse in different positions: on-surface and off-surface.
        positions = ((-1,          -1),  # (off_left,   off_top)
                     (0,           -1),  # (left_edge,  off_top)
                     (surf_w // 2, -1),  # (center_x,   off_top)
                     (surf_w - 1,  -1),  # (right_edge, off_top)
                     (surf_w,      -1))  # (off_right,  off_top)

        for rect_pos in positions:
            surface.fill(surface_color)  # Clear before each draw.
            rect.topleft = rect_pos

            self.draw_ellipse(surface, ellipse_color, rect)

            self._check_1_pixel_sized_ellipse(surface, rect, surface_color,
                                              ellipse_color)

    def test_ellipse__1_pixel_height(self):
        """Ensures an ellipse with a height of 1 is drawn correctly.

        An ellipse with a height of 1 pixel is a horizontal line.
        """
        ellipse_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surf_w, surf_h = 20, 10

        surface = pygame.Surface((surf_w, surf_h))
        rect = pygame.Rect((0, 0), (0, 1))
        collide_rect = rect.copy()

        # Calculate some positions.
        off_right = surf_w
        off_top = -1
        off_bottom = surf_h
        center_x = surf_w // 2
        center_y = surf_h // 2

        # Test some even and odd widths.
        for ellipse_w in range(6, 10):
            # The ellipse is drawn on the edge of the rect so collide_rect
            # needs +1 width to track where it's drawn.
            collide_rect.w = ellipse_w + 1
            rect.w = ellipse_w

            # Calculate some variable positions.
            off_left = -(ellipse_w + 1)
            half_off_left = -(ellipse_w // 2)
            half_off_right = surf_w - (ellipse_w // 2)

            # Draw the ellipse in different positions: fully on-surface,
            # partially off-surface, and fully off-surface.
            positions = ((off_left,       off_top),
                         (half_off_left,  off_top),
                         (center_x,       off_top),
                         (half_off_right, off_top),
                         (off_right,      off_top),

                         (off_left,       center_y),
                         (half_off_left,  center_y),
                         (center_x,       center_y),
                         (half_off_right, center_y),
                         (off_right,      center_y),

                         (off_left,       off_bottom),
                         (half_off_left,  off_bottom),
                         (center_x,       off_bottom),
                         (half_off_right, off_bottom),
                         (off_right,      off_bottom))

            for rect_pos in positions:
                surface.fill(surface_color)  # Clear before each draw.
                rect.topleft = rect_pos
                collide_rect.topleft = rect_pos

                self.draw_ellipse(surface, ellipse_color, rect)

                self._check_1_pixel_sized_ellipse(surface, collide_rect,
                                                  surface_color, ellipse_color)

    def test_ellipse__1_pixel_height_spanning_surface(self):
        """Ensures an ellipse with a height of 1 is drawn correctly
        when spanning the width of the surface.

        An ellipse with a height of 1 pixel is a horizontal line.
        """
        ellipse_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surf_w, surf_h = 20, 10

        surface = pygame.Surface((surf_w, surf_h))
        rect = pygame.Rect((0, 0), (surf_w + 2, 1))  # Wider than the surface.

        # Draw the ellipse in different positions: on-surface and off-surface.
        positions = ((-1, -1),           # (off_left, off_top)
                     (-1, 0),            # (off_left, top_edge)
                     (-1, surf_h // 2),  # (off_left, center_y)
                     (-1, surf_h - 1),   # (off_left, bottom_edge)
                     (-1, surf_h))       # (off_left, off_bottom)

        for rect_pos in positions:
            surface.fill(surface_color)  # Clear before each draw.
            rect.topleft = rect_pos

            self.draw_ellipse(surface, ellipse_color, rect)

            self._check_1_pixel_sized_ellipse(surface, rect, surface_color,
                                              ellipse_color)

    def test_ellipse__1_pixel_width_and_height(self):
        """Ensures an ellipse with a width and height of 1 is drawn correctly.

        An ellipse with a width and height of 1 pixel is a single pixel.
        """
        ellipse_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surf_w, surf_h = 10, 10

        surface = pygame.Surface((surf_w, surf_h))
        rect = pygame.Rect((0, 0), (1, 1))

        # Calculate some positions.
        off_left = -1
        off_right = surf_w
        off_top = -1
        off_bottom = surf_h
        left_edge = 0
        right_edge = surf_w - 1
        top_edge = 0
        bottom_edge = surf_h - 1
        center_x = surf_w // 2
        center_y = surf_h // 2

        # Draw the ellipse in different positions: center surface,
        # top/bottom/left/right edges, and off-surface.
        positions = ((off_left, off_top),
                     (off_left, top_edge),
                     (off_left, center_y),
                     (off_left, bottom_edge),
                     (off_left, off_bottom),

                     (left_edge, off_top),
                     (left_edge, top_edge),
                     (left_edge, center_y),
                     (left_edge, bottom_edge),
                     (left_edge, off_bottom),

                     (center_x, off_top),
                     (center_x, top_edge),
                     (center_x, center_y),
                     (center_x, bottom_edge),
                     (center_x, off_bottom),

                     (right_edge, off_top),
                     (right_edge, top_edge),
                     (right_edge, center_y),
                     (right_edge, bottom_edge),
                     (right_edge, off_bottom),

                     (off_right, off_top),
                     (off_right, top_edge),
                     (off_right, center_y),
                     (off_right, bottom_edge),
                     (off_right, off_bottom))

        for rect_pos in positions:
            surface.fill(surface_color)  # Clear before each draw.
            rect.topleft = rect_pos

            self.draw_ellipse(surface, ellipse_color, rect)

            self._check_1_pixel_sized_ellipse(surface, rect, surface_color,
                                              ellipse_color)


class DrawEllipseTest(DrawEllipseMixin, DrawTestCase):
    """Test draw module function ellipse.

    This class inherits the general tests from DrawEllipseMixin. It is also
    the class to add any draw.ellipse specific tests to.
    """


# Commented out to avoid cluttering the test output. Add back in if draw_py
# ever properly supports drawing ellipses.
#@unittest.skip('draw_py.draw_ellipse not supported yet')
#class PythonDrawEllipseTest(DrawEllipseMixin, PythonDrawTestCase):
#    """Test draw_py module function draw_ellipse.
#
#    This class inherits the general tests from DrawEllipseMixin. It is also
#    the class to add any draw_py.draw_ellipse specific tests to.
#    """


### Line/Lines/AALine/AALines Testing #########################################

class BaseLineMixin(object):
    """Mixin base for drawing various lines.

    This class contains general helper methods and setup for testing the
    different types of lines.
    """

    COLORS = ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
              (255, 0, 255), (0, 255, 255), (255, 255, 255))

    @staticmethod
    def _create_surfaces():
        # Create some surfaces with different sizes, depths, and flags.
        surfaces = []
        for size in ((49, 49), (50, 50)):
            for depth in (8, 16, 24, 32):
                for flags in (0, SRCALPHA):
                    surface = pygame.display.set_mode(size, flags, depth)
                    surfaces.append(surface)
                    surfaces.append(surface.convert_alpha())
        return surfaces

    @staticmethod
    def _rect_lines(rect):
        # Yields pairs of end points and their reverse (to test symmetry).
        # Uses a rect with the points radiating from its midleft.
        for pt in rect_corners_mids_and_center(rect):
            if pt == rect.midleft or pt == rect.center:
                # Don't bother with these points.
                continue
            yield (rect.midleft, pt)
            yield (pt, rect.midleft)

    @staticmethod
    def _create_line_bounding_rect(surface, start, end, surf_color):
        # Helper method to create a bounding rect for a given line.
        # This method checks the surface for drawn points, then creates a
        # bounding rect to enclose all the points.
        width, height = surface.get_clip().size
        xmin, ymin = width, height
        xmax, ymax = -1, -1

        surface.lock() # For possible speed up.
        for y in range(height):
            for x in range(width):
                if surface.get_at((x, y)) != surf_color:
                    xmin = min(x, xmin)
                    xmax = max(x, xmax)
                    ymin = min(y, ymin)
                    ymax = max(y, ymax)

        surface.unlock()

        if -1 == xmax:
            # No points means 0 sized rect with the position at the start.
            return pygame.Rect(start, (0, 0))

        return pygame.Rect((xmin, ymin), (xmax - xmin + 1, ymax - ymin + 1))


### Line Testing ##############################################################

class LineMixin(BaseLineMixin):
    """Mixin test for drawing a single line.

    This class contains all the general single line drawing tests.
    """
    def test_line__args(self):
        """Ensures draw line accepts the correct args."""
        bounds_rect = self.draw_line(pygame.Surface((3, 3)), (0, 10, 0, 50),
                                     (0, 0), (1, 1), 1)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__args_without_width(self):
        """Ensures draw line accepts the args without a width."""
        bounds_rect = self.draw_line(pygame.Surface((2, 2)), (0, 0, 0, 50),
                                     (0, 0), (2, 2))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__kwargs(self):
        """Ensures draw line accepts the correct kwargs
        with and without a width arg.
        """
        surface = pygame.Surface((4, 4))
        color = pygame.Color('yellow')
        start_pos = (1, 1)
        end_pos = (2, 2)
        kwargs_list = [{'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'width'     : 1},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos}]

        for kwargs in kwargs_list:
            bounds_rect = self.draw_line(**kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__kwargs_order_independent(self):
        """Ensures draw line's kwargs are not order dependent."""
        bounds_rect = self.draw_line(start_pos=(1, 2),
                                     end_pos=(2, 1),
                                     width=2,
                                     color=(10, 20, 30),
                                     surface=pygame.Surface((3, 2)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__args_missing(self):
        """Ensures draw line detects any missing required args."""
        surface = pygame.Surface((1, 1))
        color = pygame.Color('blue')

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_line(surface, color, (0, 0))

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_line(surface, color)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_line(surface)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_line()

    def test_line__kwargs_missing(self):
        """Ensures draw line detects any missing required kwargs."""
        kwargs = {'surface'   : pygame.Surface((3, 2)),
                  'color'     : pygame.Color('red'),
                  'start_pos' : (2, 1),
                  'end_pos'   : (2, 2),
                  'width'     : 1}

        for name in ('end_pos', 'start_pos', 'color', 'surface'):
            invalid_kwargs = dict(kwargs)
            invalid_kwargs.pop(name)  # Pop from a copy.

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_line(**invalid_kwargs)

    def test_line__arg_invalid_types(self):
        """Ensures draw line detects invalid arg types."""
        surface = pygame.Surface((2, 2))
        color = pygame.Color('blue')
        start_pos = (0, 1)
        end_pos = (1, 2)

        with self.assertRaises(TypeError):
            # Invalid width.
            bounds_rect = self.draw_line(surface, color, start_pos, end_pos,
                                         '1')

        with self.assertRaises(TypeError):
            # Invalid end_pos.
            bounds_rect = self.draw_line(surface, color, start_pos, (1, 2, 3))

        with self.assertRaises(TypeError):
            # Invalid start_pos.
            bounds_rect = self.draw_line(surface, color, (1,), end_pos)

        with self.assertRaises(TypeError):
            # Invalid color.
            bounds_rect = self.draw_line(surface, 'blue', start_pos, end_pos)

        with self.assertRaises(TypeError):
            # Invalid surface.
            bounds_rect = self.draw_line((1, 2, 3, 4), color, start_pos,
                                         end_pos)

    def test_line__kwarg_invalid_types(self):
        """Ensures draw line detects invalid kwarg types."""
        surface = pygame.Surface((3, 3))
        color = pygame.Color('green')
        start_pos = (1, 0)
        end_pos = (2, 0)
        width = 1
        kwargs_list = [{'surface'   : pygame.Surface,  # Invalid surface.
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'width'     : width},

                       {'surface'   : surface,
                        'color'     : 'green',  # Invalid color.
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'width'     : width},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : (0, 0, 0),  # Invalid start_pos.
                        'end_pos'   : end_pos,
                        'width'     : width},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : (0,),  # Invalid end_pos.
                        'width'     : width},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'width'     : 1.2}]  # Invalid width.

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_line(**kwargs)

    def test_line__kwarg_invalid_name(self):
        """Ensures draw line detects invalid kwarg names."""
        surface = pygame.Surface((2, 3))
        color = pygame.Color('cyan')
        start_pos = (1, 1)
        end_pos = (2, 0)
        kwargs_list = [{'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'width'     : 1,
                        'invalid'   : 1},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'invalid'   : 1}]

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_line(**kwargs)

    def test_line__args_and_kwargs(self):
        """Ensures draw line accepts a combination of args/kwargs"""
        surface = pygame.Surface((3, 2))
        color = (255, 255, 0, 0)
        start_pos = (0, 1)
        end_pos = (1, 2)
        width = 0
        kwargs = {'surface'   : surface,
                  'color'     : color,
                  'start_pos' : start_pos,
                  'end_pos'   : end_pos,
                  'width'     : width}

        for name in ('surface', 'color', 'start_pos', 'end_pos', 'width'):
            kwargs.pop(name)

            if 'surface' == name:
                bounds_rect = self.draw_line(surface, **kwargs)
            elif 'color' == name:
                bounds_rect = self.draw_line(surface, color, **kwargs)
            elif 'start_pos' == name:
                bounds_rect = self.draw_line(surface, color, start_pos,
                                             **kwargs)
            elif 'end_pos' == name:
                bounds_rect = self.draw_line(surface, color, start_pos,
                                             end_pos, **kwargs)
            else:
                bounds_rect = self.draw_line(surface, color, start_pos,
                                             end_pos, width, **kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__valid_width_values(self):
        """Ensures draw line accepts different width values."""
        line_color = pygame.Color('yellow')
        surface_color = pygame.Color('white')
        surface = pygame.Surface((3, 4))
        pos = (2, 1)
        kwargs = {'surface'   : surface,
                  'color'     : line_color,
                  'start_pos' : pos,
                  'end_pos'   : (2, 2),
                  'width'     : None}
        pos = kwargs['start_pos']

        for width in (-100, -10, -1, 0, 1, 10, 100):
            surface.fill(surface_color)  # Clear for each test.
            kwargs['width'] = width
            expected_color = line_color if width > 0 else surface_color

            bounds_rect = self.draw_line(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__valid_start_pos_formats(self):
        """Ensures draw line accepts different start_pos formats."""
        expected_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((4, 4))
        kwargs = {'surface'   : surface,
                  'color'     : expected_color,
                  'start_pos' : None,
                  'end_pos'   : (2, 2),
                  'width'     : 2}
        x, y = 2, 1 # start position

        # The point values can be ints or floats.
        for start_pos in ((x, y), (x + .1, y), (x, y + .1), (x + .1, y + .1)):
            # The point type can be a tuple/list/Vector2.
            for seq_type in (tuple, list, Vector2):
                surface.fill(surface_color)  # Clear for each test.
                kwargs['start_pos'] = seq_type(start_pos)

                bounds_rect = self.draw_line(**kwargs)

                self.assertEqual(surface.get_at((x, y)), expected_color)
                self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__valid_end_pos_formats(self):
        """Ensures draw line accepts different end_pos formats."""
        expected_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((4, 4))
        kwargs = {'surface'   : surface,
                  'color'     : expected_color,
                  'start_pos' : (2, 1),
                  'end_pos'   : None,
                  'width'     : 2}
        x, y = 2, 2 # end position

        # The point values can be ints or floats.
        for end_pos in ((x, y), (x + .2, y), (x, y + .2), (x + .2, y + .2)):
            # The point type can be a tuple/list/Vector2.
            for seq_type in (tuple, list, Vector2):
                surface.fill(surface_color)  # Clear for each test.
                kwargs['end_pos'] = seq_type(end_pos)

                bounds_rect = self.draw_line(**kwargs)

                self.assertEqual(surface.get_at((x, y)), expected_color)
                self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__invalid_start_pos_formats(self):
        """Ensures draw line handles invalid start_pos formats correctly."""
        kwargs = {'surface'   : pygame.Surface((4, 4)),
                  'color'     : pygame.Color('red'),
                  'start_pos' : None,
                  'end_pos'   : (2, 2),
                  'width'     : 1}

        start_pos_fmts = ((2,),      # Too few coords.
                          (2, 1, 0), # Too many coords.
                          (2, '1'),        # Wrong type.
                          set([2, 1]),     # Wrong type.
                          dict(((2, 1),))) # Wrong type.

        for start_pos in start_pos_fmts:
            kwargs['start_pos'] = start_pos

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_line(**kwargs)

    def test_line__invalid_end_pos_formats(self):
        """Ensures draw line handles invalid end_pos formats correctly."""
        kwargs = {'surface'   : pygame.Surface((4, 4)),
                  'color'     : pygame.Color('red'),
                  'start_pos' : (2, 2),
                  'end_pos'   : None,
                  'width'     : 1}

        end_pos_fmts = ((2,),      # Too few coords.
                        (2, 1, 0), # Too many coords.
                        (2, '1'),        # Wrong type.
                        set([2, 1]),     # Wrong type.
                        dict(((2, 1),))) # Wrong type.

        for end_pos in end_pos_fmts:
            kwargs['end_pos'] = end_pos

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_line(**kwargs)

    def test_line__valid_color_formats(self):
        """Ensures draw line accepts different color formats."""
        green_color = pygame.Color('green')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        pos = (1, 1)
        kwargs = {'surface'   : surface,
                  'color'     : None,
                  'start_pos' : pos,
                  'end_pos'   : (2, 1),
                  'width'     : 3}
        greens = ((0, 255, 0), (0, 255, 0, 255), surface.map_rgb(green_color),
                  green_color)

        for color in greens:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['color'] = color

            if isinstance(color, int):
                expected_color = surface.unmap_rgb(color)
            else:
                expected_color = green_color

            bounds_rect = self.draw_line(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_line__invalid_color_formats(self):
        """Ensures draw line handles invalid color formats correctly."""
        kwargs = {'surface'   : pygame.Surface((4, 3)),
                  'color'     : None,
                  'start_pos' : (1, 1),
                  'end_pos'   : (2, 1),
                  'width'     : 1}

        # These color formats are currently not supported (it would be
        # nice to eventually support them).
        for expected_color in ('green', '#00FF00FF', '0x00FF00FF'):
            kwargs['color'] = expected_color

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_line(**kwargs)

    def test_line__color(self):
        """Tests if the line drawn is the correct color."""
        pos = (0, 0)
        for surface in self._create_surfaces():
            for expected_color in self.COLORS:
                self.draw_line(surface, expected_color, pos, (1, 0))

                self.assertEqual(surface.get_at(pos), expected_color,
                                 'pos={}'.format(pos))

    def todo_test_line__color_with_thickness(self):
        """Ensures a thick line is drawn using the correct color."""
        self.fail()

    def test_line__gaps(self):
        """Tests if the line drawn contains any gaps."""
        expected_color = (255, 255, 255)
        for surface in self._create_surfaces():
            width = surface.get_width()
            self.draw_line(surface, expected_color, (0, 0), (width - 1, 0))

            for x in range(width):
                pos = (x, 0)
                self.assertEqual(surface.get_at(pos), expected_color,
                                 'pos={}'.format(pos))

    def todo_test_line__gaps_with_thickness(self):
        """Ensures a thick line is drawn without any gaps."""
        self.fail()

    def test_line__bounding_rect(self):
        """Ensures draw line returns the correct bounding rect.

        Tests lines with endpoints on and off the surface and a range of
        width/thickness values.
        """
        if isinstance(self, PythonDrawTestCase):
            self.skipTest('bounding rects not supported in draw_py.draw_line')

        line_color = pygame.Color('red')
        surf_color = pygame.Color('black')
        width = height = 30
        # Using a rect to help manage where the lines are drawn.
        helper_rect = pygame.Rect((0, 0), (width, height))

        # Testing surfaces of different sizes. One larger than the helper_rect
        # and one smaller (to test lines that span the surface).
        for size in ((width + 5, height + 5), (width - 5, height - 5)):
            surface = pygame.Surface(size, 0, 32)
            surf_rect = surface.get_rect()

            # Move the helper rect to different positions to test line
            # endpoints on and off the surface.
            for pos in rect_corners_mids_and_center(surf_rect):
                helper_rect.center = pos

                # Draw using different thicknesses.
                for thickness in range(-1, 5):
                    for start, end in self._rect_lines(helper_rect):
                        surface.fill(surf_color) # Clear for each test.

                        bounding_rect = self.draw_line(surface, line_color,
                                                       start, end, thickness)

                        if 0 < thickness:
                            # Calculating the expected_rect after the line is
                            # drawn (it uses what is actually drawn).
                            expected_rect = self._create_line_bounding_rect(
                                surface, start, end, surf_color)
                        else:
                            # Nothing drawn.
                            expected_rect = pygame.Rect(start, (0, 0))

                        self.assertEqual(bounding_rect, expected_rect,
                            'start={}, end={}, size={}, thickness={}'.format(
                                start, end, size, thickness))


# Commented out to avoid cluttering the test output. Add back in if draw_py
# ever fully supports drawing single lines.
#@unittest.skip('draw_py.draw_line not fully supported yet')
#class PythonDrawLineTest(LineMixin, PythonDrawTestCase):
#    """Test draw_py module function line.
#
#    This class inherits the general tests from LineMixin. It is also the class
#    to add any draw_py.draw_line specific tests to.
#    """


class DrawLineTest(LineMixin, DrawTestCase):
    """Test draw module function line.

    This class inherits the general tests from LineMixin. It is also the class
    to add any draw.line specific tests to.
    """

    def test_line_endianness(self):
        """ test color component order """
        for depth in (24, 32):
            surface = pygame.Surface((5, 3), 0, depth)
            surface.fill(pygame.Color(0, 0, 0))
            self.draw_line(surface, pygame.Color(255, 0, 0), (0, 1), (2, 1), 1)

            self.assertGreater(surface.get_at((1, 1)).r, 0,
                               'there should be red here')

            surface.fill(pygame.Color(0, 0, 0))
            self.draw_line(surface, pygame.Color(0, 0, 255), (0, 1), (2, 1), 1)

            self.assertGreater(surface.get_at((1, 1)).b, 0,
                               'there should be blue here')

    def test_line(self):
        # (l, t), (l, t)
        self.surf_size = (320, 200)
        self.surf = pygame.Surface(self.surf_size, pygame.SRCALPHA)
        self.color = (1, 13, 24, 205)

        drawn = draw.line(self.surf, self.color, (1, 0), (200, 0))
        self.assertEqual(drawn.right, 201,
                     "end point arg should be (or at least was) inclusive")

        # Should be colored where it's supposed to be
        for pt in test_utils.rect_area_pts(drawn):
            self.assertEqual(self.surf.get_at(pt), self.color)

        # And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(drawn):
            self.assertNotEqual(self.surf.get_at(pt), self.color)

        # Line width greater that 1
        line_width = 2
        offset = 5
        a = (offset, offset)
        b = (self.surf_size[0] - offset, a[1])
        c = (a[0], self.surf_size[1] - offset)
        d = (b[0], c[1])
        e = (a[0] + offset, c[1])
        f = (b[0], c[0] + 5)
        lines = [(a, d), (b, c), (c, b), (d, a),
                 (a, b), (b, a), (a, c), (c, a),
                 (a, e), (e, a), (a, f), (f, a),
                 (a, a),]

        for p1, p2 in lines:
            msg = "%s - %s" % (p1, p2)
            if p1[0] <= p2[0]:
                plow = p1
                phigh = p2
            else:
                plow = p2
                phigh = p1

            self.surf.fill((0, 0, 0))
            rec = draw.line(self.surf, (255, 255, 255), p1, p2, line_width)
            xinc = yinc = 0

            if abs(p1[0] - p2[0]) > abs(p1[1] - p2[1]):
                yinc = 1
            else:
                xinc = 1

            for i in range(line_width):
                p = (p1[0] + xinc * i, p1[1] + yinc * i)

                self.assertEqual(self.surf.get_at(p), (255, 255, 255), msg)

                p = (p2[0] + xinc * i, p2[1] + yinc * i)

                self.assertEqual(self.surf.get_at(p), (255, 255, 255), msg)

            p = (plow[0] - 1, plow[1])

            self.assertEqual(self.surf.get_at(p), (0, 0, 0), msg)

            p = (plow[0] + xinc * line_width, plow[1] + yinc * line_width)

            self.assertEqual(self.surf.get_at(p), (0, 0, 0), msg)

            p = (phigh[0] + xinc * line_width, phigh[1] + yinc * line_width)

            self.assertEqual(self.surf.get_at(p), (0, 0, 0), msg)

            if p1[0] < p2[0]:
                rx = p1[0]
            else:
                rx = p2[0]

            if p1[1] < p2[1]:
                ry = p1[1]
            else:
                ry = p2[1]

            w = abs(p2[0] - p1[0]) + 1 + xinc * (line_width - 1)
            h = abs(p2[1] - p1[1]) + 1 + yinc * (line_width - 1)
            msg += ", %s" % (rec,)

            self.assertEqual(rec, (rx, ry, w, h), msg)

    @unittest.expectedFailure
    def test_line_for_gaps(self):
        """ |tags: ignore|
        """
        # This checks bug Thick Line Bug #448

        width = 200
        height = 200
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        def white_surrounded_pixels(x, y):
            offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            WHITE = (255, 255, 255, 255)
            return len([1 for dx, dy in offsets
                        if surf.get_at((x+dx, y+dy)) == WHITE])

        def check_white_line(start, end):
            surf.fill((0, 0, 0))
            pygame.draw.line(surf, (255, 255, 255), start, end, 30)

            BLACK = (0, 0, 0, 255)
            for x in range(1, width-1):
                for y in range(1, height-1):
                    if surf.get_at((x, y)) == BLACK:
                        self.assertTrue(white_surrounded_pixels(x, y) < 3)

        check_white_line((50, 50), (140, 0))
        check_white_line((50, 50), (0, 120))
        check_white_line((50, 50), (199, 198))


### Lines Testing #############################################################

class LinesMixin(BaseLineMixin):
    """Mixin test for drawing lines.

    This class contains all the general lines drawing tests.
    """
    def test_lines__color(self):
        """Tests if the lines drawn are the correct color.

        Draws lines around the border of the given surface and checks if all
        borders of the surface only contain the given color.
        """
        for surface in self._create_surfaces():
            for expected_color in self.COLORS:
                self.draw_lines(surface, expected_color, True,
                                corners(surface))

                for pos, color in border_pos_and_color(surface):
                    self.assertEqual(color, expected_color,
                                     'pos={}'.format(pos))

    def todo_test_lines__color_with_thickness(self):
        """Ensures thick lines are drawn using the correct color."""
        self.fail()

    def test_lines__gaps(self):
        """Tests if the lines drawn contain any gaps.

        Draws lines around the border of the given surface and checks if
        all borders of the surface contain any gaps.
        """
        expected_color = (255, 255, 255)
        for surface in self._create_surfaces():
            self.draw_lines(surface, expected_color, True, corners(surface))

            for pos, color in border_pos_and_color(surface):
                self.assertEqual(color, expected_color, 'pos={}'.format(pos))

    def todo_test_lines__gaps_with_thickness(self):
        """Ensures thick lines are drawn without any gaps."""
        self.fail()

    def todo_test_lines__bounding_rect(self):
        """Ensures draw lines returns the correct bounding rect."""
        self.fail()


class PythonDrawLinesTest(LinesMixin, PythonDrawTestCase):
    """Test draw_py module function lines.

    This class inherits the general tests from LinesMixin. It is also the class
    to add any draw_py.draw_lines specific tests to.
    """


class DrawLinesTest(LinesMixin, DrawTestCase):
    """Test draw module function lines.

    This class inherits the general tests from LinesMixin. It is also the class
    to add any draw.lines specific tests to.
    """


### AALine Testing ############################################################

class AALineMixin(BaseLineMixin):
    """Mixin test for drawing a single aaline.

    This class contains all the general single aaline drawing tests.
    """
    def test_aaline__args(self):
        """Ensures draw aaline accepts the correct args."""
        bounds_rect = self.draw_aaline(pygame.Surface((3, 3)), (0, 10, 0, 50),
                                       (0, 0), (1, 1), 1)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_aaline__args_without_blend(self):
        """Ensures draw aaline accepts the args without a blend."""
        bounds_rect = self.draw_aaline(pygame.Surface((2, 2)), (0, 0, 0, 50),
                                       (0, 0), (2, 2))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_aaline__kwargs(self):
        """Ensures draw aaline accepts the correct kwargs
        with and without a blend arg.
        """
        surface = pygame.Surface((4, 4))
        color = pygame.Color('yellow')
        start_pos = (1, 1)
        end_pos = (2, 2)
        kwargs_list = [{'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'blend'     : 1},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos}]

        for kwargs in kwargs_list:
            bounds_rect = self.draw_aaline(**kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_aaline__kwargs_order_independent(self):
        """Ensures draw aaline's kwargs are not order dependent."""
        bounds_rect = self.draw_aaline(start_pos=(1, 2),
                                       end_pos=(2, 1),
                                       blend=1,
                                       color=(10, 20, 30),
                                       surface=pygame.Surface((3, 2)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_aaline__args_missing(self):
        """Ensures draw aaline detects any missing required args."""
        surface = pygame.Surface((1, 1))
        color = pygame.Color('blue')

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_aaline(surface, color, (0, 0))

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_aaline(surface, color)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_aaline(surface)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_aaline()

    def test_aaline__kwargs_missing(self):
        """Ensures draw aaline detects any missing required kwargs."""
        kwargs = {'surface'   : pygame.Surface((3, 2)),
                  'color'     : pygame.Color('red'),
                  'start_pos' : (2, 1),
                  'end_pos'   : (2, 2),
                  'blend'     : 1}

        for name in ('end_pos', 'start_pos', 'color', 'surface'):
            invalid_kwargs = dict(kwargs)
            invalid_kwargs.pop(name)  # Pop from a copy.

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_aaline(**invalid_kwargs)

    def test_aaline__arg_invalid_types(self):
        """Ensures draw aaline detects invalid arg types."""
        surface = pygame.Surface((2, 2))
        color = pygame.Color('blue')
        start_pos = (0, 1)
        end_pos = (1, 2)

        with self.assertRaises(TypeError):
            # Invalid blend.
            bounds_rect = self.draw_aaline(surface, color, start_pos, end_pos,
                                           '1')

        with self.assertRaises(TypeError):
            # Invalid end_pos.
            bounds_rect = self.draw_aaline(surface, color, start_pos,
                                           (1, 2, 3))

        with self.assertRaises(TypeError):
            # Invalid start_pos.
            bounds_rect = self.draw_aaline(surface, color, (1,), end_pos)

        with self.assertRaises(TypeError):
            # Invalid color.
            bounds_rect = self.draw_aaline(surface, 'blue', start_pos, end_pos)

        with self.assertRaises(TypeError):
            # Invalid surface.
            bounds_rect = self.draw_aaline((1, 2, 3, 4), color, start_pos,
                                           end_pos)

    def test_aaline__kwarg_invalid_types(self):
        """Ensures draw aaline detects invalid kwarg types."""
        surface = pygame.Surface((3, 3))
        color = pygame.Color('green')
        start_pos = (1, 0)
        end_pos = (2, 0)
        blend = 1
        kwargs_list = [{'surface'   : pygame.Surface,  # Invalid surface.
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'blend'     : blend},

                       {'surface'   : surface,
                        'color'     : 'green',  # Invalid color.
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'blend'     : blend},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : (0, 0, 0),  # Invalid start_pos.
                        'end_pos'   : end_pos,
                        'blend'     : blend},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : (0,),  # Invalid end_pos.
                        'blend'     : blend},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'blend'     : 1.2}]  # Invalid blend.

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_aaline(**kwargs)

    def test_aaline__kwarg_invalid_name(self):
        """Ensures draw aaline detects invalid kwarg names."""
        surface = pygame.Surface((2, 3))
        color = pygame.Color('cyan')
        start_pos = (1, 1)
        end_pos = (2, 0)
        kwargs_list = [{'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'blend'     : 1,
                        'invalid'   : 1},

                       {'surface'   : surface,
                        'color'     : color,
                        'start_pos' : start_pos,
                        'end_pos'   : end_pos,
                        'invalid'   : 1}]

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_aaline(**kwargs)

    def test_aaline__args_and_kwargs(self):
        """Ensures draw aaline accepts a combination of args/kwargs"""
        surface = pygame.Surface((3, 2))
        color = (255, 255, 0, 0)
        start_pos = (0, 1)
        end_pos = (1, 2)
        blend = 0
        kwargs = {'surface'   : surface,
                  'color'     : color,
                  'start_pos' : start_pos,
                  'end_pos'   : end_pos,
                  'blend'     : blend}

        for name in ('surface', 'color', 'start_pos', 'end_pos', 'blend'):
            kwargs.pop(name)

            if 'surface' == name:
                bounds_rect = self.draw_aaline(surface, **kwargs)
            elif 'color' == name:
                bounds_rect = self.draw_aaline(surface, color, **kwargs)
            elif 'start_pos' == name:
                bounds_rect = self.draw_aaline(surface, color, start_pos,
                                               **kwargs)
            elif 'end_pos' == name:
                bounds_rect = self.draw_aaline(surface, color, start_pos,
                                               end_pos, **kwargs)
            else:
                bounds_rect = self.draw_aaline(surface, color, start_pos,
                                               end_pos, blend, **kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_aaline__valid_blend_values(self):
        """Ensures draw aaline accepts different blend values."""
        expected_color = pygame.Color('yellow')
        surface_color = pygame.Color('white')
        surface = pygame.Surface((3, 4))
        pos = (2, 1)
        kwargs = {'surface'   : surface,
                  'color'     : expected_color,
                  'start_pos' : pos,
                  'end_pos'   : (2, 2),
                  'blend'     : None}
        pos = kwargs['start_pos']

        for blend in (-10, -2, -1, 0, 1, 2, 10):
            surface.fill(surface_color)  # Clear for each test.
            kwargs['blend'] = blend

            bounds_rect = self.draw_aaline(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_aaline__valid_start_pos_formats(self):
        """Ensures draw aaline accepts different start_pos formats."""
        expected_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((4, 4))
        kwargs = {'surface'   : surface,
                  'color'     : expected_color,
                  'start_pos' : None,
                  'end_pos'   : (2, 2),
                  'blend'     : 0}
        x, y = 2, 1 # start position
        positions = ((x, y), (x + .01, y), (x, y + .01), (x + .01, y + .01))

        for start_pos in positions:
            for seq_type in (tuple, list, Vector2):
                surface.fill(surface_color)  # Clear for each test.
                kwargs['start_pos'] = seq_type(start_pos)

                bounds_rect = self.draw_aaline(**kwargs)

                color = surface.get_at((x, y))
                for i, sub_color in enumerate(expected_color):
                    # The color could be slightly off the expected color due to
                    # any fractional position arguments.
                    self.assertGreaterEqual(color[i] + 5, sub_color, start_pos)
                self.assertIsInstance(bounds_rect, pygame.Rect, start_pos)

    def test_aaline__valid_end_pos_formats(self):
        """Ensures draw aaline accepts different end_pos formats."""
        expected_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((4, 4))
        kwargs = {'surface'   : surface,
                  'color'     : expected_color,
                  'start_pos' : (2, 1),
                  'end_pos'   : None,
                  'blend'     : 0}
        x, y = 2, 2 # end position
        positions = ((x, y), (x + .02, y), (x, y + .02), (x + .02, y + .02))

        for end_pos in positions:
            for seq_type in (tuple, list, Vector2):
                surface.fill(surface_color)  # Clear for each test.
                kwargs['end_pos'] = seq_type(end_pos)

                bounds_rect = self.draw_aaline(**kwargs)

                color = surface.get_at((x, y))
                for i, sub_color in enumerate(expected_color):
                    # The color could be slightly off the expected color due to
                    # any fractional position arguments.
                    self.assertGreaterEqual(color[i] + 15, sub_color, end_pos)
                self.assertIsInstance(bounds_rect, pygame.Rect, end_pos)

    def test_aaline__invalid_start_pos_formats(self):
        """Ensures draw aaline handles invalid start_pos formats correctly."""
        kwargs = {'surface'   : pygame.Surface((4, 4)),
                  'color'     : pygame.Color('red'),
                  'start_pos' : None,
                  'end_pos'   : (2, 2),
                  'blend'     : 0}

        start_pos_fmts = ((2,),      # Too few coords.
                          (2, 1, 0), # Too many coords.
                          (2, '1'),        # Wrong type.
                          set([2, 1]),     # Wrong type.
                          dict(((2, 1),))) # Wrong type.

        for start_pos in start_pos_fmts:
            kwargs['start_pos'] = start_pos

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_aaline(**kwargs)

    def test_aaline__invalid_end_pos_formats(self):
        """Ensures draw aaline handles invalid end_pos formats correctly."""
        kwargs = {'surface'   : pygame.Surface((4, 4)),
                  'color'     : pygame.Color('red'),
                  'start_pos' : (2, 2),
                  'end_pos'   : None,
                  'blend'     : 0}

        end_pos_fmts = ((2,),      # Too few coords.
                        (2, 1, 0), # Too many coords.
                        (2, '1'),        # Wrong type.
                        set([2, 1]),     # Wrong type.
                        dict(((2, 1),))) # Wrong type.

        for end_pos in end_pos_fmts:
            kwargs['end_pos'] = end_pos

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_aaline(**kwargs)

    def test_aaline__valid_color_formats(self):
        """Ensures draw aaline accepts different color formats."""
        green_color = pygame.Color('green')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        pos = (1, 1)
        kwargs = {'surface'   : surface,
                  'color'     : None,
                  'start_pos' : pos,
                  'end_pos'   : (2, 1),
                  'blend'     : 0}
        greens = ((0, 255, 0), (0, 255, 0, 255), surface.map_rgb(green_color),
                  green_color)

        for color in greens:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['color'] = color

            if isinstance(color, int):
                expected_color = surface.unmap_rgb(color)
            else:
                expected_color = green_color

            bounds_rect = self.draw_aaline(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_aaline__invalid_color_formats(self):
        """Ensures draw aaline handles invalid color formats correctly."""
        kwargs = {'surface'   : pygame.Surface((4, 3)),
                  'color'     : None,
                  'start_pos' : (1, 1),
                  'end_pos'   : (2, 1),
                  'blend'     : 0}

        # These color formats are currently not supported (it would be
        # nice to eventually support them).
        for expected_color in ('green', '#00FF00FF', '0x00FF00FF'):
            kwargs['color'] = expected_color

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_aaline(**kwargs)

    def test_aaline__color(self):
        """Tests if the aaline drawn is the correct color."""
        pos = (0, 0)
        for surface in self._create_surfaces():
            for expected_color in self.COLORS:
                self.draw_aaline(surface, expected_color, pos, (1, 0))

                self.assertEqual(surface.get_at(pos), expected_color,
                                 'pos={}'.format(pos))

    def test_aaline__gaps(self):
        """Tests if the aaline drawn contains any gaps.

        See: #512
        """
        expected_color = (255, 255, 255)
        for surface in self._create_surfaces():
            width = surface.get_width()
            self.draw_aaline(surface, expected_color, (0, 0), (width - 1, 0))

            for x in range(width):
                pos = (x, 0)
                self.assertEqual(surface.get_at(pos), expected_color,
                                 'pos={}'.format(pos))

    def todo_test_aaline__bounding_rect(self):
        """Ensures draw aaline returns the correct bounding rect."""
        self.fail()


# Commented out to avoid cluttering the test output. Add back in if draw_py
# ever fully supports drawing single aalines.
#class PythonDrawAALineTest(AALineMixin, PythonDrawTestCase):
#    """Test draw_py module function aaline.
#
#    This class inherits the general tests from AALineMixin. It is also the
#    class to add any draw_py.draw_aaline specific tests to.
#    """


class DrawAALineTest(AALineMixin, DrawTestCase):
    """Test draw module function aaline.

    This class inherits the general tests from AALineMixin. It is also the
    class to add any draw.aaline specific tests to.
    """

    def test_aaline_endianness(self):
        """ test color component order """
        for depth in (24, 32):
            surface = pygame.Surface((5, 3), 0, depth)
            surface.fill(pygame.Color(0, 0, 0))
            self.draw_aaline(surface, pygame.Color(255, 0, 0), (0, 1), (2, 1),
                             1)

            self.assertGreater(surface.get_at((1, 1)).r, 0,
                               'there should be red here')

            surface.fill(pygame.Color(0, 0, 0))
            self.draw_aaline(surface, pygame.Color(0, 0, 255), (0, 1), (2, 1),
                             1)

            self.assertGreater(surface.get_at((1, 1)).b, 0,
                               'there should be blue here')

    def _check_antialiasing(self, from_point, to_point, should, check_points,
                            set_endpoints=True):
        """Draw a line between two points and check colors of check_points."""
        if set_endpoints:
            should[from_point] = should[to_point] = FG_GREEN

        def check_one_direction(from_point, to_point, should):
            self.draw_aaline(self.surface, FG_GREEN, from_point, to_point,
                             True)

            for pt in check_points:
                color = should.get(pt, BG_RED)
                if PY3: # "subTest" is sooo helpful, but does not exist in PY2
                    with self.subTest(from_pt=from_point, pt=pt, to=to_point):
                        self.assertEqual(self.surface.get_at(pt), color)
                else:
                    self.assertEqual(self.surface.get_at(pt), color)

            # reset
            draw.rect(self.surface, BG_RED, (0, 0, 10, 10), 0)

        # it is important to test also opposite direction, the algorithm
        # is (#512) or was not symmetric
        check_one_direction(from_point, to_point, should)
        if from_point != to_point:
            check_one_direction(to_point, from_point, should)

    def test_short_non_antialiased_lines(self):
        """test very short not anti aliased lines in all directions."""
        if isinstance(self, DrawTestCase):
            self.skipTest('not working with draw.aaline')

        # Horizontal, vertical and diagonal lines should not be anti-aliased,
        # even with draw.aaline ...
        self.surface = pygame.Surface((10, 10))
        draw.rect(self.surface, BG_RED, (0, 0, 10, 10), 0)

        check_points = [(i, j) for i in range(3, 8) for j in range(3, 8)]

        def check_both_directions(from_pt, to_pt, other_points):
            should = {pt: FG_GREEN for pt in other_points}
            self._check_antialiasing(from_pt, to_pt, should, check_points)

        # 0. one point
        check_both_directions((5, 5), (5, 5), [])
        # 1. horizontal
        check_both_directions((4, 7), (5, 7), [])
        check_both_directions((5, 4), (7, 4), [(6, 4)])

        # 2. vertical
        check_both_directions((5, 5), (5, 6), [])
        check_both_directions((6, 4), (6, 6), [(6, 5)])
        # 3. diagonals
        check_both_directions((5, 5), (6, 6), [])
        check_both_directions((5, 5), (7, 7), [(6, 6)])
        check_both_directions((5, 6), (6, 5), [])
        check_both_directions((6, 4), (4, 6), [(5, 5)])

    def test_short_line_anti_aliasing(self):
        if isinstance(self, DrawTestCase):
            self.skipTest('not working with draw.aaline')

        self.surface = pygame.Surface((10, 10))
        draw.rect(self.surface, BG_RED, (0, 0, 10, 10), 0)

        check_points = [(i, j) for i in range(3, 8) for j in range(3, 8)]

        def check_both_directions(from_pt, to_pt, should):
            self._check_antialiasing(from_pt, to_pt, should, check_points)

        # lets say dx = abs(x0 - x1) ; dy = abs(y0 - y1)
        brown = (127, 127, 0)

        # dy / dx = 0.5
        check_both_directions((4, 4), (6, 5), {(5, 4): brown, (5, 5): brown})
        check_both_directions((4, 5), (6, 4), {(5, 4): brown, (5, 5): brown})

        # dy / dx = 2
        check_both_directions((4, 4), (5, 6), {(4, 5): brown, (5, 5): brown})
        check_both_directions((5, 4), (4, 6), {(4, 5): brown, (5, 5): brown})

        # some little longer lines; so we need to check more points:
        check_points = [(i, j) for i in range(2, 9) for j in range(2, 9)]
        # dy / dx = 0.25
        reddish = (191, 63, 0)
        greenish = (63, 191, 0)
        should = {(4, 3): greenish, (5, 3): brown, (6, 3): reddish,
                  (4, 4): reddish,  (5, 4): brown, (6, 4): greenish}
        check_both_directions((3, 3), (7, 4), should)

        should = {(4, 3): reddish,  (5, 3): brown, (6, 3): greenish,
                  (4, 4): greenish, (5, 4): brown, (6, 4): reddish}
        check_both_directions((3, 4), (7, 3), should)

        # dy / dx = 4
        should = {(4, 4): greenish, (4, 5): brown, (4, 6): reddish,
                  (5, 4): reddish,  (5, 5): brown, (5, 6): greenish,
                 }
        check_both_directions((4, 3), (5, 7), should)

        should = {(4, 4): reddish,  (4, 5): brown, (4, 6): greenish,
                  (5, 4): greenish, (5, 5): brown, (5, 6): reddish}
        check_both_directions((5, 3), (4, 7), should)

    def test_anti_aliasing_float_coordinates(self):
        """Float coordinates should be blended smoothly."""
        if isinstance(self, DrawTestCase):
            self.skipTest('not working with draw.aaline')

        self.surface = pygame.Surface((10, 10))
        draw.rect(self.surface, BG_RED, (0, 0, 10, 10), 0)

        check_points = [(i, j) for i in range(5) for j in range(5)]
        brown = (127, 127, 0)

        # 0. identical point : current implementation does no smoothing...
        expected = {(1, 2): FG_GREEN}
        self._check_antialiasing((1.5, 2), (1.5, 2), expected,
                                 check_points, set_endpoints=False)
        expected = {(2, 2): FG_GREEN}
        self._check_antialiasing((2.5, 2.7), (2.5, 2.7), expected,
                                 check_points, set_endpoints=False)

        # 1. horizontal lines
        #  a) blend endpoints
        expected = {(1, 2): brown, (2, 2): FG_GREEN}
        self._check_antialiasing((1.5, 2), (2, 2), expected,
                                 check_points, set_endpoints=False)
        expected = {(1, 2): brown, (2, 2): FG_GREEN, (3, 2): brown}
        self._check_antialiasing((1.5, 2), (2.5, 2), expected,
                                 check_points, set_endpoints=False)
        expected = {(2, 2): brown, (1, 2): FG_GREEN, }
        self._check_antialiasing((1, 2), (1.5, 2), expected,
                                 check_points, set_endpoints=False)
        expected = {(1, 2): brown, (2, 2):  (63, 191, 0)}
        self._check_antialiasing((1.5, 2), (1.75, 2), expected,
                                 check_points, set_endpoints=False)

        #  b) blend y-coordinate
        expected = {(x, y): brown for x  in range(2, 5) for y in (1, 2)}
        self._check_antialiasing((2, 1.5), (4, 1.5), expected,
                                 check_points, set_endpoints=False)

        # 2. vertical lines
        #  a) blend endpoints
        expected = {(2, 1): brown, (2, 2): FG_GREEN, (2, 3): brown}
        self._check_antialiasing((2, 1.5), (2, 2.5), expected,
                                 check_points, set_endpoints=False)
        expected = {(2, 1): brown, (2, 2):  (63, 191, 0)}
        self._check_antialiasing((2, 1.5), (2, 1.75), expected,
                                 check_points, set_endpoints=False)
        #  b) blend x-coordinate
        expected = {(x, y): brown for x in (1, 2) for y in range(2, 5)}
        self._check_antialiasing((1.5, 2), (1.5, 4), expected,
                                 check_points, set_endpoints=False)
        # 3. diagonal lines
        #  a) blend endpoints
        expected = {(1, 1): brown, (2, 2): FG_GREEN, (3, 3): brown}
        self._check_antialiasing((1.5, 1.5), (2.5, 2.5), expected,
                                 check_points, set_endpoints=False)
        expected = {(3, 1): brown, (2, 2): FG_GREEN, (1, 3): brown}
        self._check_antialiasing((2.5, 1.5), (1.5, 2.5), expected,
                                 check_points, set_endpoints=False)
        #  b) blend sidewards
        expected = {(2, 1): brown, (2, 2): brown, (3, 2): brown, (3, 3): brown}
        self._check_antialiasing((2, 1.5), (3, 2.5), expected,
                                 check_points, set_endpoints=False)

        reddish = (191, 63, 0)
        greenish = (63, 191, 0)
        expected = {(2, 1): greenish, (2, 2): reddish,
                    (3, 2): greenish, (3, 3): reddish,
                    (4, 3): greenish, (4, 4): reddish}

        self._check_antialiasing((2, 1.25), (4, 3.25), expected,
                                 check_points, set_endpoints=False)

    def test_anti_aliasing_at_and_outside_the_border(self):
        """Ensures antialiasing works correct at a surface's borders."""
        if isinstance(self, DrawTestCase):
            self.skipTest('not working with draw.aaline')

        self.surface = pygame.Surface((10, 10))
        draw.rect(self.surface, BG_RED, (0, 0, 10, 10), 0)

        check_points = [(i, j) for i in range(10) for j in range(10)]

        reddish = (191, 63, 0)
        brown = (127, 127, 0)
        greenish = (63, 191, 0)
        from_point, to_point = (3, 3), (7, 4)
        should = {(4, 3): greenish, (5, 3): brown, (6, 3): reddish,
                  (4, 4): reddish,  (5, 4): brown, (6, 4): greenish}

        for dx, dy in ((-4, 0), (4, 0), # moved to left and right borders
                       (0, -5), (0, -4), (0, -3), # upper border
                       (0, 5), (0,  6), (0,  7), # lower border
                       (-4, -4), (-4, -3), (-3, -4)):  # upper left corner
            first = from_point[0] + dx, from_point[1] + dy
            second = to_point[0] + dx,  to_point[1] + dy
            expected = {(x + dx, y + dy): color
                        for (x, y), color in should.items()}

            self._check_antialiasing(first, second, expected, check_points)


### AALines Testing ###########################################################

class AALinesMixin(BaseLineMixin):
    """Mixin test for drawing aalines.

    This class contains all the general aalines drawing tests.
    """

    def test_aalines__color(self):
        """Tests if the aalines drawn are the correct color.

        Draws aalines around the border of the given surface and checks if all
        borders of the surface only contain the given color.
        """
        for surface in self._create_surfaces():
            for expected_color in self.COLORS:
                self.draw_aalines(surface, expected_color, True,
                                  corners(surface))

                for pos, color in border_pos_and_color(surface):
                    self.assertEqual(color, expected_color,
                                     'pos={}'.format(pos))

    def test_aalines__gaps(self):
        """Tests if the aalines drawn contain any gaps.

        Draws aalines around the border of the given surface and checks if
        all borders of the surface contain any gaps.

        See: #512
        """
        expected_color = (255, 255, 255)
        for surface in self._create_surfaces():
            self.draw_aalines(surface, expected_color, True, corners(surface))

            for pos, color in border_pos_and_color(surface):
                self.assertEqual(color, expected_color, 'pos={}'.format(pos))

    def todo_test_aalines__bounding_rect(self):
        """Ensures draw aalines returns the correct bounding rect."""
        self.fail()


class PythonDrawAALinesTest(AALinesMixin, PythonDrawTestCase):
    """Test draw_py module function aalines.

    This class inherits the general tests from AALinesMixin. It is also the
    class to add any draw_py.draw_aalines specific tests to.
    """


class DrawAALinesTest(AALinesMixin, DrawTestCase):
    """Test draw module function aalines.

    This class inherits the general tests from AALinesMixin. It is also the
    class to add any draw.aalines specific tests to.
    """


### Polygon Testing ###########################################################

SQUARE = ([0, 0], [3, 0], [3, 3], [0, 3])
DIAMOND = [(1, 3), (3, 5), (5, 3), (3, 1)]
CROSS = ([2, 0], [4, 0], [4, 2], [6, 2],
         [6, 4], [4, 4], [4, 6], [2, 6],
         [2, 4], [0, 4], [0, 2], [2, 2])


class DrawPolygonMixin(object):
    """Mixin tests for drawing polygons.

    This class contains all the general polygon drawing tests.
    """

    def setUp(self):
        self.surface = pygame.Surface((20, 20))

    def test_polygon__args(self):
        """Ensures draw polygon accepts the correct args."""
        bounds_rect = self.draw_polygon(pygame.Surface((3, 3)), (0, 10, 0, 50),
                                        ((0, 0), (1, 1), (2, 2)), 1)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_polygon__args_without_width(self):
        """Ensures draw polygon accepts the args without a width."""
        bounds_rect = self.draw_polygon(pygame.Surface((2, 2)), (0, 0, 0, 50),
                                       ((0, 0), (1, 1), (2, 2)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_polygon__kwargs(self):
        """Ensures draw polygon accepts the correct kwargs
        with and without a width arg.
        """
        surface = pygame.Surface((4, 4))
        color = pygame.Color('yellow')
        points = ((0, 0), (1, 1), (2, 2))
        kwargs_list = [{'surface' : surface,
                        'color'   : color,
                        'points'  : points,
                        'width'   : 1},

                       {'surface' : surface,
                        'color'   : color,
                        'points'  : points}]

        for kwargs in kwargs_list:
            bounds_rect = self.draw_polygon(**kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_polygon__kwargs_order_independent(self):
        """Ensures draw polygon's kwargs are not order dependent."""
        bounds_rect = self.draw_polygon(color=(10, 20, 30),
                                        surface=pygame.Surface((3, 2)),
                                        width=0,
                                        points=((0, 1), (1, 2), (2, 3)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_polygon__args_missing(self):
        """Ensures draw polygon detects any missing required args."""
        surface = pygame.Surface((1, 1))
        color = pygame.Color('blue')

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_polygon(surface, color)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_polygon(surface)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_polygon()

    def test_polygon__kwargs_missing(self):
        """Ensures draw polygon detects any missing required kwargs."""
        kwargs = {'surface' : pygame.Surface((1, 2)),
                  'color'   : pygame.Color('red'),
                  'points'  : ((2, 1), (2, 2), (2, 3)),
                  'width'   : 1}

        for name in ('points', 'color', 'surface'):
            invalid_kwargs = dict(kwargs)
            invalid_kwargs.pop(name)  # Pop from a copy.

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_polygon(**invalid_kwargs)

    def test_polygon__arg_invalid_types(self):
        """Ensures draw polygon detects invalid arg types."""
        surface = pygame.Surface((2, 2))
        color = pygame.Color('blue')
        points = ((0, 1), (1, 2), (1, 3))

        with self.assertRaises(TypeError):
            # Invalid width.
            bounds_rect = self.draw_polygon(surface, color, points, '1')

        with self.assertRaises(TypeError):
            # Invalid points.
            bounds_rect = self.draw_polygon(surface, color, (1, 2, 3))

        with self.assertRaises(TypeError):
            # Invalid color.
            bounds_rect = self.draw_polygon(surface, 'blue', points)

        with self.assertRaises(TypeError):
            # Invalid surface.
            bounds_rect = self.draw_polygon((1, 2, 3, 4), color, points)

    def test_polygon__kwarg_invalid_types(self):
        """Ensures draw polygon detects invalid kwarg types."""
        surface = pygame.Surface((3, 3))
        color = pygame.Color('green')
        points = ((0, 0), (1, 0), (2, 0))
        width = 1
        kwargs_list = [{'surface' : pygame.Surface,  # Invalid surface.
                        'color'   : color,
                        'points'  : points,
                        'width'   : width},

                       {'surface' : surface,
                        'color'   : 'green',  # Invalid color.
                        'points'  : points,
                        'width'   : width},

                       {'surface' : surface,
                        'color'   : color,
                        'points'  : ((1,), (1,), (1,)),  # Invalid points.
                        'width'   : width},

                       {'surface' : surface,
                        'color'   : color,
                        'points'  : points,
                        'width'   : 1.2}]  # Invalid width.

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_polygon(**kwargs)

    def test_polygon__kwarg_invalid_name(self):
        """Ensures draw polygon detects invalid kwarg names."""
        surface = pygame.Surface((2, 3))
        color = pygame.Color('cyan')
        points = ((1, 1), (1, 2), (1, 3))
        kwargs_list = [{'surface' : surface,
                        'color'   : color,
                        'points'  : points,
                        'width'   : 1,
                        'invalid' : 1},

                       {'surface' : surface,
                        'color'   : color,
                        'points'  : points,
                        'invalid' : 1}]

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_polygon(**kwargs)

    def test_polygon__args_and_kwargs(self):
        """Ensures draw polygon accepts a combination of args/kwargs"""
        surface = pygame.Surface((3, 1))
        color = (255, 255, 0, 0)
        points = ((0, 1), (1, 2), (2, 3))
        width = 0
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'points'  : points,
                  'width'   : width}

        for name in ('surface', 'color', 'points', 'width'):
            kwargs.pop(name)

            if 'surface' == name:
                bounds_rect = self.draw_polygon(surface, **kwargs)
            elif 'color' == name:
                bounds_rect = self.draw_polygon(surface, color, **kwargs)
            elif 'points' == name:
                bounds_rect = self.draw_polygon(surface, color, points,
                                                **kwargs)
            else:
                bounds_rect = self.draw_polygon(surface, color, points, width,
                                                **kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_polygon__valid_width_values(self):
        """Ensures draw polygon accepts different width values."""
        surface_color = pygame.Color('white')
        surface = pygame.Surface((3, 4))
        color = (10, 20, 30, 255)
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'points'  : ((1, 1), (2, 1), (2, 2), (1, 2)),
                  'width'   : None}
        pos = kwargs['points'][0]

        for width in (-100, -10, -1, 0, 1, 10, 100):
            surface.fill(surface_color)  # Clear for each test.
            kwargs['width'] = width
            expected_color = color if width >= 0 else surface_color

            bounds_rect = self.draw_polygon(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_polygon__valid_points_format(self):
        """Ensures draw polygon accepts different points formats."""
        expected_color = (10, 20, 30, 255)
        surface_color = pygame.Color('white')
        surface = pygame.Surface((3, 4))
        kwargs = {'surface' : surface,
                  'color'   : expected_color,
                  'points'  : None,
                  'width'   : 0}

        # The point type can be a tuple/list/Vector2.
        point_types = ((tuple, tuple, tuple, tuple), # all tuples
                       (list, list, list, list),     # all lists
                       (Vector2, Vector2, Vector2, Vector2), # all Vector2s
                       (list, Vector2, tuple, Vector2))      # mix

        # The point values can be ints or floats.
        point_values = (((1, 1), (2, 1), (2, 2), (1, 2)),
                        ((1, 1), (2.2, 1), (2.1, 2.2), (1, 2.1)))

        # Each sequence of points can be a tuple or a list.
        seq_types = (tuple, list)

        for point_type in point_types:
            for values in point_values:
                check_pos = values[0]
                points = [point_type[i](pt) for i, pt in enumerate(values)]

                for seq_type in seq_types:
                    surface.fill(surface_color)  # Clear for each test.
                    kwargs['points'] = seq_type(points)

                    bounds_rect = self.draw_polygon(**kwargs)

                    self.assertEqual(surface.get_at(check_pos), expected_color)
                    self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_polygon__invalid_points_formats(self):
        """Ensures draw polygon handles invalid points formats correctly."""
        kwargs = {'surface' : pygame.Surface((4, 4)),
                  'color'   : pygame.Color('red'),
                  'points'  : None,
                  'width'   : 0}

        points_fmts = (((1, 1), (2, 1), (2,)),      # Too few coords.
                       ((1, 1), (2, 1), (2, 2, 2)), # Too many coords.
                       ((1, 1), (2, 1), (2, '2')),    # Wrong type.
                       ((1, 1), (2, 1), set([2, 3])), # Wrong type.
                       ((1, 1), (2, 1), dict(((2, 2), (3, 3)))), # Wrong type.
                       set(((1, 1), (2, 1), (2, 2), (1, 2))),    # Wrong type.
                       dict(((1, 1), (2, 2), (3, 3), (4, 4))))   # Wrong type.

        for points in points_fmts:
            kwargs['points'] = points

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_polygon(**kwargs)

    def test_polygon__invalid_points_values(self):
        """Ensures draw polygon handles invalid points values correctly."""
        kwargs = {'surface' : pygame.Surface((4, 4)),
                  'color'   : pygame.Color('red'),
                  'points'  : None,
                  'width'   : 0}

        points_fmts = (tuple(),          # Too few points.
                       ((1, 1),),        # Too few points.
                       ((1, 1), (2, 1))) # Too few points.

        for points in points_fmts:
            for seq_type in (tuple, list):  # Test as tuples and lists.
                kwargs['points'] = seq_type(points)

                with self.assertRaises(ValueError):
                    bounds_rect = self.draw_polygon(**kwargs)

    def test_polygon__valid_color_formats(self):
        """Ensures draw polygon accepts different color formats."""
        green_color = pygame.Color('green')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        kwargs = {'surface' : surface,
                  'color'   : None,
                  'points'  : ((1, 1), (2, 1), (2, 2), (1, 2)),
                  'width'   : 0}
        pos = kwargs['points'][0]
        greens = ((0, 255, 0), (0, 255, 0, 255), surface.map_rgb(green_color),
                  green_color)

        for color in greens:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['color'] = color

            if isinstance(color, int):
                expected_color = surface.unmap_rgb(color)
            else:
                expected_color = green_color

            bounds_rect = self.draw_polygon(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_polygon__invalid_color_formats(self):
        """Ensures draw polygon handles invalid color formats correctly."""
        kwargs = {'surface' : pygame.Surface((4, 3)),
                  'color'   : None,
                  'points'  : ((1, 1), (2, 1), (2, 2), (1, 2)),
                  'width'   : 0}

        # These color formats are currently not supported (it would be
        # nice to eventually support them).
        for expected_color in ('green', '#00FF00FF', '0x00FF00FF'):
            kwargs['color'] = expected_color

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_polygon(**kwargs)

    def test_draw_square(self):
        self.draw_polygon(self.surface, RED, SQUARE, 0)
        # note : there is a discussion (#234) if draw.polygon should include or
        # not the right or lower border; here we stick with current behavior,
        # eg include those borders ...
        for x in range(4):
            for y in range(4):
                self.assertEqual(self.surface.get_at((x, y)), RED)

    def test_draw_diamond(self):
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        self.draw_polygon(self.surface, GREEN, DIAMOND, 0)
        # this diamond shape is equivalent to its four corners, plus inner square
        for x, y in DIAMOND:
            self.assertEqual(self.surface.get_at((x, y)), GREEN, msg=str((x, y)))
        for x in range(2, 5):
            for y in range(2, 5):
                self.assertEqual(self.surface.get_at((x, y)), GREEN)

    def test_1_pixel_high_or_wide_shapes(self):
        # 1. one-pixel-high, filled
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        self.draw_polygon(self.surface, GREEN, [(x, 2) for x, _y in CROSS], 0)
        cross_size = 6 # the maximum x or y coordinate of the cross
        for x in range(cross_size + 1):
            self.assertEqual(self.surface.get_at((x, 1)), RED)
            self.assertEqual(self.surface.get_at((x, 2)), GREEN)
            self.assertEqual(self.surface.get_at((x, 3)), RED)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        # 2. one-pixel-high, not filled
        self.draw_polygon(self.surface, GREEN, [(x, 5) for x, _y in CROSS], 1)
        for x in range(cross_size + 1):
            self.assertEqual(self.surface.get_at((x, 4)), RED)
            self.assertEqual(self.surface.get_at((x, 5)), GREEN)
            self.assertEqual(self.surface.get_at((x, 6)), RED)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        # 3. one-pixel-wide, filled
        self.draw_polygon(self.surface, GREEN, [(3, y) for _x, y in CROSS], 0)
        for y in range(cross_size + 1):
            self.assertEqual(self.surface.get_at((2, y)), RED)
            self.assertEqual(self.surface.get_at((3, y)), GREEN)
            self.assertEqual(self.surface.get_at((4, y)), RED)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        # 4. one-pixel-wide, not filled
        self.draw_polygon(self.surface, GREEN, [(4, y) for _x, y in CROSS], 1)
        for y in range(cross_size + 1):
            self.assertEqual(self.surface.get_at((3, y)), RED)
            self.assertEqual(self.surface.get_at((4, y)), GREEN)
            self.assertEqual(self.surface.get_at((5, y)), RED)

    def test_draw_symetric_cross(self):
        """non-regression on issue #234 : x and y where handled inconsistently.

        Also, the result is/was different whether we fill or not the polygon.
        """
        # 1. case width = 1 (not filled: `polygon` calls  internally the `lines` function)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        self.draw_polygon(self.surface, GREEN, CROSS, 1)
        inside = [(x, 3) for x in range(1, 6)] + [(3, y) for y in range(1, 6)]
        for x in range(10):
            for y in range(10):
                if (x, y) in inside:
                    self.assertEqual(self.surface.get_at((x, y)), RED)
                elif (x in range(2, 5) and y <7) or (y in range(2, 5) and x < 7):
                    # we are on the border of the cross:
                    self.assertEqual(self.surface.get_at((x, y)), GREEN)
                else:
                    # we are outside
                    self.assertEqual(self.surface.get_at((x, y)), RED)

        # 2. case width = 0 (filled; this is the example from #234)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        self.draw_polygon(self.surface, GREEN, CROSS, 0)
        inside = [(x, 3) for x in range(1, 6)] + [(3, y) for y in range(1, 6)]
        for x in range(10):
            for y in range(10):
                if (x in range(2, 5) and y <7) or (y in range(2, 5) and x < 7):
                    # we are on the border of the cross:
                    self.assertEqual(self.surface.get_at((x, y)), GREEN, msg=str((x, y)))
                else:
                    # we are outside
                    self.assertEqual(self.surface.get_at((x, y)), RED)

    def test_illumine_shape(self):
        """non-regression on issue #313"""
        rect = pygame.Rect((0, 0, 20, 20))
        path_data = [(0, 0), (rect.width-1, 0), # upper border
                     (rect.width-5,  5-1), (5-1, 5-1),  # upper inner
                     (5- 1, rect.height-5), (0,  rect.height-1)]   # lower diagonal
        # The shape looks like this (the numbers are the indices of path_data)

        # 0**********************1              <-- upper border
        # ***********************
        # **********************
        # *********************
        # ****3**************2                  <-- upper inner border
        # *****
        # *****                   (more lines here)
        # *****
        # ****4
        # ****
        # ***
        # **
        # 5
        #

        # the current bug is that the "upper inner" line is not drawn, but only
        # if 4 or some lower corner exists
        pygame.draw.rect(self.surface, RED, (0, 0, 20, 20), 0)

        # 1. First without the corners 4 & 5
        self.draw_polygon(self.surface, GREEN, path_data[:4], 0)
        for x in range(20):
            self.assertEqual(self.surface.get_at((x, 0)), GREEN)  # upper border
        for x in range(4, rect.width-5 +1):
            self.assertEqual(self.surface.get_at((x, 4)), GREEN)  # upper inner

        # 2. with the corners 4 & 5
        pygame.draw.rect(self.surface, RED, (0, 0, 20, 20), 0)
        self.draw_polygon(self.surface, GREEN, path_data, 0)
        for x in range(4, rect.width-5 +1):
            self.assertEqual(self.surface.get_at((x, 4)), GREEN)  # upper inner

    def test_invalid_points(self):
        self.assertRaises(TypeError, lambda: self.draw_polygon(self.surface,
                          RED, ((0, 0), (0, 20), (20, 20), 20), 0))


class DrawPolygonTest(DrawPolygonMixin, DrawTestCase):
    """Test draw module function polygon.

    This class inherits the general tests from DrawPolygonMixin. It is also
    the class to add any draw.polygon specific tests to.
    """


# Commented out to avoid cluttering the test output. Add back in if draw_py
# ever fully supports drawing polygons.
#@unittest.skip('draw_py.draw_polygon not fully supported yet')
#class PythonDrawPolygonTest(DrawPolygonMixin, PythonDrawTestCase):
#    """Test draw_py module function draw_polygon.
#
#    This class inherits the general tests from DrawPolygonMixin. It is also
#    the class to add any draw_py.draw_polygon specific tests to.
#    """


### Rect Testing ##############################################################

class DrawRectMixin(object):
    """Mixin tests for drawing rects.

    This class contains all the general rect drawing tests.
    """
    def test_rect__args(self):
        """Ensures draw rect accepts the correct args."""
        bounds_rect = self.draw_rect(pygame.Surface((2, 2)), (20, 10, 20, 150),
                                     pygame.Rect((0, 0), (1, 1)), 2)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_rect__args_without_width(self):
        """Ensures draw rect accepts the args without a width."""
        bounds_rect = self.draw_rect(pygame.Surface((3, 5)), (0, 0, 0, 255),
                                     pygame.Rect((0, 0), (1, 1)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_rect__kwargs(self):
        """Ensures draw rect accepts the correct kwargs
        with and without a width arg.
        """
        kwargs_list = [{'surface' : pygame.Surface((5, 5)),
                        'color'   : pygame.Color('red'),
                        'rect'    : pygame.Rect((0, 0), (1, 2)),
                        'width'   : 1},

                       {'surface' : pygame.Surface((1, 2)),
                        'color'   : (0, 100, 200),
                        'rect'    : (0, 0, 1, 1)}]

        for kwargs in kwargs_list:
            bounds_rect = self.draw_rect(**kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_rect__kwargs_order_independent(self):
        """Ensures draw rect's kwargs are not order dependent."""
        bounds_rect = self.draw_rect(color=(0, 1, 2),
                                     surface=pygame.Surface((2, 3)),
                                     width=-2,
                                     rect=pygame.Rect((0, 0), (0, 0)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_rect__args_missing(self):
        """Ensures draw rect detects any missing required args."""
        surface = pygame.Surface((1, 1))

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_rect(surface, pygame.Color('white'))

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_rect(surface)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_rect()

    def test_rect__kwargs_missing(self):
        """Ensures draw rect detects any missing required kwargs."""
        kwargs = {'surface' : pygame.Surface((1, 3)),
                  'color'   : pygame.Color('red'),
                  'rect'    : pygame.Rect((0, 0), (2, 2)),
                  'width'   : 5}

        for name in ('rect', 'color', 'surface'):
            invalid_kwargs = dict(kwargs)
            invalid_kwargs.pop(name)  # Pop from a copy.

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_rect(**invalid_kwargs)

    def test_rect__arg_invalid_types(self):
        """Ensures draw rect detects invalid arg types."""
        surface = pygame.Surface((3, 3))
        color = pygame.Color('white')
        rect = pygame.Rect((1, 1), (1, 1))

        with self.assertRaises(TypeError):
            # Invalid width.
            bounds_rect = self.draw_rect(surface, color, rect, '2')

        with self.assertRaises(TypeError):
            # Invalid rect.
            bounds_rect = self.draw_rect(surface, color, (1, 2, 3), 2)

        with self.assertRaises(TypeError):
            # Invalid color.
            bounds_rect = self.draw_rect(surface, 'yellow', rect, 3)

        with self.assertRaises(TypeError):
            # Invalid surface.
            bounds_rect = self.draw_rect(rect, color, rect, 4)

    def test_rect__kwarg_invalid_types(self):
        """Ensures draw rect detects invalid kwarg types."""
        surface = pygame.Surface((2, 3))
        color = pygame.Color('red')
        rect = pygame.Rect((0, 0), (1, 1))
        kwargs_list = [{'surface' : pygame.Surface,  # Invalid surface.
                        'color'   : color,
                        'rect'    : rect,
                        'width'   : 1},

                       {'surface' : surface,
                        'color'   : 'red',  # Invalid color.
                        'rect'    : rect,
                        'width'   : 1},

                       {'surface' : surface,
                        'color'   : color,
                        'rect'    : (1, 1, 2),  # Invalid rect.
                        'width'   : 1},

                       {'surface' : surface,
                        'color'   : color,
                        'rect'    : rect,
                        'width'   : 1.1}]  # Invalid width.

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_rect(**kwargs)

    def test_rect__kwarg_invalid_name(self):
        """Ensures draw rect detects invalid kwarg names."""
        surface = pygame.Surface((2, 1))
        color = pygame.Color('green')
        rect = pygame.Rect((0, 0), (3, 3))
        kwargs_list = [{'surface' : surface,
                        'color'   : color,
                        'rect'    : rect,
                        'width'   : 1,
                        'invalid' : 1},

                       {'surface' : surface,
                        'color'   : color,
                        'rect'    : rect,
                        'invalid' : 1}]

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_rect(**kwargs)

    def test_rect__args_and_kwargs(self):
        """Ensures draw rect accepts a combination of args/kwargs"""
        surface = pygame.Surface((3, 1))
        color = (255, 255, 255, 0)
        rect = pygame.Rect((1, 0), (2, 5))
        width = 0
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'rect'    : rect,
                  'width'   : width}

        for name in ('surface', 'color', 'rect', 'width'):
            kwargs.pop(name)

            if 'surface' == name:
                bounds_rect = self.draw_rect(surface, **kwargs)
            elif 'color' == name:
                bounds_rect = self.draw_rect(surface, color, **kwargs)
            elif 'rect' == name:
                bounds_rect = self.draw_rect(surface, color, rect, **kwargs)
            else:
                bounds_rect = self.draw_rect(surface, color, rect, width,
                                             **kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_rect__valid_width_values(self):
        """Ensures draw rect accepts different width values."""
        pos = (1, 1)
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        color = (1, 2, 3, 255)
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'rect'    : pygame.Rect(pos, (2, 2)),
                  'width'   : None}

        for width in (-1000, -10, -1, 0, 1, 10, 1000):
            surface.fill(surface_color)  # Clear for each test.
            kwargs['width'] = width
            expected_color = color if width >= 0 else surface_color

            bounds_rect = self.draw_rect(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_rect__valid_rect_formats(self):
        """Ensures draw rect accepts different rect formats."""
        pos = (1, 1)
        expected_color = pygame.Color('yellow')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        kwargs = {'surface' : surface,
                  'color'   : expected_color,
                  'rect'    : None,
                  'width'   : 0}
        rects = (pygame.Rect(pos, (1, 1)), (pos, (2, 2)),
                 (pos[0], pos[1], 3, 3), [pos, (2.1, 2.2)])

        for rect in rects:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['rect'] = rect

            bounds_rect = self.draw_rect(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_rect__invalid_rect_formats(self):
        """Ensures draw rect handles invalid rect formats correctly."""
        kwargs = {'surface' : pygame.Surface((4, 4)),
                  'color'   : pygame.Color('red'),
                  'rect'    : None,
                  'width'   : 0}

        invalid_fmts = ([], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4, 5],
                        set([1, 2, 3, 4]), [1, 2, 3, '4'])

        for rect in invalid_fmts:
            kwargs['rect'] = rect

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_rect(**kwargs)

    def test_rect__valid_color_formats(self):
        """Ensures draw rect accepts different color formats."""
        pos = (1, 1)
        red_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        kwargs = {'surface' : surface,
                  'color'   : None,
                  'rect'    : pygame.Rect(pos, (1, 1)),
                  'width'   : 3}
        reds = ((255, 0, 0), (255, 0, 0, 255), surface.map_rgb(red_color),
                red_color)

        for color in reds:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['color'] = color

            if isinstance(color, int):
                expected_color = surface.unmap_rgb(color)
            else:
                expected_color = red_color

            bounds_rect = self.draw_rect(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_rect__invalid_color_formats(self):
        """Ensures draw rect handles invalid color formats correctly."""
        pos = (1, 1)
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        kwargs = {'surface' : surface,
                  'color'   : None,
                  'rect'    : pygame.Rect(pos, (1, 1)),
                  'width'   : 1}

        # These color formats are currently not supported (it would be
        # nice to eventually support them).
        for expected_color in ('red', '#FF0000FF', '0xFF0000FF'):
            kwargs['color'] = expected_color

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_rect(**kwargs)

    def test_rect__fill(self):
        self.surf_w, self.surf_h = self.surf_size = (320, 200)
        self.surf = pygame.Surface(self.surf_size, pygame.SRCALPHA)
        self.color = (1, 13, 24, 205)
        rect = pygame.Rect(10, 10, 25, 20)
        drawn = self.draw_rect(self.surf, self.color, rect, 0)

        self.assertEqual(drawn, rect)

        # Should be colored where it's supposed to be
        for pt in test_utils.rect_area_pts(rect):
            color_at_pt = self.surf.get_at(pt)

            self.assertEqual(color_at_pt, self.color)

        # And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(rect):
            color_at_pt = self.surf.get_at(pt)

            self.assertNotEqual(color_at_pt, self.color)

        # Issue #310: Cannot draw rectangles that are 1 pixel high
        bgcolor = pygame.Color('black')
        self.surf.fill(bgcolor)
        hrect = pygame.Rect(1, 1, self.surf_w - 2, 1)
        vrect = pygame.Rect(1, 3, 1, self.surf_h - 4)

        drawn = self.draw_rect(self.surf, self.color, hrect, 0)

        self.assertEqual(drawn, hrect)

        x, y = hrect.topleft
        w, h = hrect.size

        self.assertEqual(self.surf.get_at((x - 1, y)), bgcolor)
        self.assertEqual(self.surf.get_at((x + w, y)), bgcolor)
        for i in range(x, x + w):
            self.assertEqual(self.surf.get_at((i, y)), self.color)

        drawn = self.draw_rect(self.surf, self.color, vrect, 0)

        self.assertEqual(drawn, vrect)

        x, y = vrect.topleft
        w, h = vrect.size

        self.assertEqual(self.surf.get_at((x, y - 1)), bgcolor)
        self.assertEqual(self.surf.get_at((x, y + h)), bgcolor)
        for i in range(y, y + h):
            self.assertEqual(self.surf.get_at((x, i)), self.color)

    def test_rect__one_pixel_lines(self):
        self.surf = pygame.Surface((320, 200), pygame.SRCALPHA)
        self.color = (1, 13, 24, 205)

        rect = pygame.Rect(10, 10, 56, 20)

        drawn = self.draw_rect(self.surf, self.color, rect, 1)

        self.assertEqual(drawn, rect)

        # Should be colored where it's supposed to be
        for pt in test_utils.rect_perimeter_pts(drawn):
            color_at_pt = self.surf.get_at(pt)

            self.assertEqual(color_at_pt, self.color)

        # And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(drawn):
            color_at_pt = self.surf.get_at(pt)

            self.assertNotEqual(color_at_pt, self.color)


class DrawRectTest(DrawRectMixin, DrawTestCase):
    """Test draw module function rect.

    This class inherits the general tests from DrawRectMixin. It is also the
    class to add any draw.rect specific tests to.
    """


# Commented out to avoid cluttering the test output. Add back in if draw_py
# ever properly supports drawing rects.
#@unittest.skip('draw_py.draw_rect not supported yet')
#class PythonDrawRectTest(DrawRectMixin, PythonDrawTestCase):
#    """Test draw_py module function draw_rect.
#
#    This class inherits the general tests from DrawRectMixin. It is also the
#    class to add any draw_py.draw_rect specific tests to.
#    """


### Circle Testing ############################################################

class DrawCircleMixin(object):
    """Mixin tests for drawing circles.

    This class contains all the general circle drawing tests.
    """
    def test_circle__args(self):
        """Ensures draw circle accepts the correct args."""
        bounds_rect = self.draw_circle(pygame.Surface((3, 3)), (0, 10, 0, 50),
                                       (0, 0), 3, 1)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_circle__args_without_width(self):
        """Ensures draw circle accepts the args without a width."""
        bounds_rect = self.draw_circle(pygame.Surface((2, 2)), (0, 0, 0, 50),
                                       (1, 1), 1)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_circle__kwargs(self):
        """Ensures draw circle accepts the correct kwargs
        with and without a width arg.
        """
        kwargs_list = [{'surface' : pygame.Surface((4, 4)),
                        'color'   : pygame.Color('yellow'),
                        'center'  : (2, 2),
                        'radius'  : 2,
                        'width'   : 1},

                       {'surface' : pygame.Surface((2, 1)),
                        'color'   : (0, 10, 20),
                        'center'  : (1, 1),
                        'radius'  : 1}]

        for kwargs in kwargs_list:
            bounds_rect = self.draw_circle(**kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_circle__kwargs_order_independent(self):
        """Ensures draw circle's kwargs are not order dependent."""
        bounds_rect = self.draw_circle(color=(10, 20, 30),
                                       surface=pygame.Surface((3, 2)),
                                       width=0,
                                       center=(1, 0),
                                       radius=2)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_circle__args_missing(self):
        """Ensures draw circle detects any missing required args."""
        surface = pygame.Surface((1, 1))
        color = pygame.Color('blue')

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_circle(surface, color, (0, 0))

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_circle(surface, color)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_circle(surface)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_circle()

    def test_circle__kwargs_missing(self):
        """Ensures draw circle detects any missing required kwargs."""
        kwargs = {'surface' : pygame.Surface((1, 2)),
                  'color'   : pygame.Color('red'),
                  'center'  : (1, 0),
                  'radius'  : 2,
                  'width'   : 1}

        for name in ('radius', 'center', 'color', 'surface'):
            invalid_kwargs = dict(kwargs)
            invalid_kwargs.pop(name)  # Pop from a copy.

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_circle(**invalid_kwargs)

    def test_circle__arg_invalid_types(self):
        """Ensures draw circle detects invalid arg types."""
        surface = pygame.Surface((2, 2))
        color = pygame.Color('blue')
        center = (1, 1)
        radius = 1

        with self.assertRaises(TypeError):
            # Invalid width.
            bounds_rect = self.draw_circle(surface, color, center, radius, '1')

        with self.assertRaises(TypeError):
            # Invalid radius.
            bounds_rect = self.draw_circle(surface, color, center, '2')

        with self.assertRaises(TypeError):
            # Invalid center.
            bounds_rect = self.draw_circle(surface, color, (1, 2, 3), radius)

        with self.assertRaises(TypeError):
            # Invalid color.
            bounds_rect = self.draw_circle(surface, 'blue', center, radius)

        with self.assertRaises(TypeError):
            # Invalid surface.
            bounds_rect = self.draw_circle((1, 2, 3, 4), color, center, radius)

    def test_circle__kwarg_invalid_types(self):
        """Ensures draw circle detects invalid kwarg types."""
        surface = pygame.Surface((3, 3))
        color = pygame.Color('green')
        center = (0, 1)
        radius = 1
        width = 1
        kwargs_list = [{'surface' : pygame.Surface,  # Invalid surface.
                        'color'   : color,
                        'center'  : center,
                        'radius'  : radius,
                        'width'   : width},

                       {'surface' : surface,
                        'color'   : 'green',  # Invalid color.
                        'center'  : center,
                        'radius'  : radius,
                        'width'   : width},

                       {'surface' : surface,
                        'color'   : color,
                        'center'  : (1, 1, 1),  # Invalid center.
                        'radius'  : radius,
                        'width'   : width},

                       {'surface' : surface,
                        'color'   : color,
                        'center'  : center,
                        'radius'  : 1.1,  # Invalid radius.
                        'width'   : width},

                       {'surface' : surface,
                        'color'   : color,
                        'center'  : center,
                        'radius'  : radius,
                        'width'   : 1.2}]  # Invalid width.

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_circle(**kwargs)

    def test_circle__kwarg_invalid_name(self):
        """Ensures draw circle detects invalid kwarg names."""
        surface = pygame.Surface((2, 3))
        color = pygame.Color('cyan')
        center = (0, 0)
        radius = 2
        kwargs_list = [{'surface' : surface,
                        'color'   : color,
                        'center'  : center,
                        'radius'  : radius,
                        'width'   : 1,
                        'invalid' : 1},

                       {'surface' : surface,
                        'color'   : color,
                        'center'  : center,
                        'radius'  : radius,
                        'invalid' : 1}]

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_circle(**kwargs)

    def test_circle__args_and_kwargs(self):
        """Ensures draw circle accepts a combination of args/kwargs"""
        surface = pygame.Surface((3, 1))
        color = (255, 255, 0, 0)
        center = (1, 0)
        radius = 2
        width = 0
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'center'  : center,
                  'radius'  : radius,
                  'width'   : width}

        for name in ('surface', 'color', 'center', 'radius', 'width'):
            kwargs.pop(name)

            if 'surface' == name:
                bounds_rect = self.draw_circle(surface, **kwargs)
            elif 'color' == name:
                bounds_rect = self.draw_circle(surface, color, **kwargs)
            elif 'center' == name:
                bounds_rect = self.draw_circle(surface, color, center,
                                               **kwargs)
            elif 'radius' == name:
                bounds_rect = self.draw_circle(surface, color, center, radius,
                                               **kwargs)
            else:
                bounds_rect = self.draw_circle(surface, color, center, radius,
                                               width, **kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    # This decorator can be removed when the circle portion of issues #975
    # and #976 are resolved.
    @unittest.expectedFailure
    def test_circle__valid_width_values(self):
        """Ensures draw circle accepts different width values."""
        center = (2, 2)
        radius = 1
        pos = (center[0] - radius, center[1])
        surface_color = pygame.Color('white')
        surface = pygame.Surface((3, 4))
        color = (10, 20, 30, 255)
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'center'  : center,
                  'radius'  : radius,
                  'width'   : None}

        for width in (-100, -10, -1, 0, 1, 10, 100):
            surface.fill(surface_color)  # Clear for each test.
            kwargs['width'] = width
            expected_color = color if width >= 0 else surface_color

            bounds_rect = self.draw_circle(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    # This decorator can be removed when issue #983 is resolved.
    @unittest.expectedFailure
    def test_circle__valid_radius_values(self):
        """Ensures draw circle accepts different radius values."""
        pos = center = (2, 2)
        surface_color = pygame.Color('white')
        surface = pygame.Surface((3, 4))
        color = (10, 20, 30, 255)
        kwargs = {'surface' : surface,
                  'color'   : color,
                  'center'  : center,
                  'radius'  : None,
                  'width'   : 0}

        for radius in (-10, -1, 0, 1, 10):
            surface.fill(surface_color)  # Clear for each test.
            kwargs['radius'] = radius
            expected_color = color if radius > 0 else surface_color

            bounds_rect = self.draw_circle(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_circle__valid_center_formats(self):
        """Ensures draw circle accepts different center formats."""
        expected_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((4, 4))
        kwargs = {'surface' : surface,
                  'color'   : expected_color,
                  'center'  : None,
                  'radius'  : 1,
                  'width'   : 0}
        x, y = 2, 2 # center position

        # The center values can be ints or floats.
        for center in ((x, y), (x + .1, y), (x, y + .1), (x + .1, y + .1)):
            # The center type can be a tuple/list/Vector2.
            for seq_type in (tuple, list, Vector2):
                surface.fill(surface_color)  # Clear for each test.
                kwargs['center'] = seq_type(center)

                bounds_rect = self.draw_circle(**kwargs)

                self.assertEqual(surface.get_at((x, y)), expected_color)
                self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_circle__valid_color_formats(self):
        """Ensures draw circle accepts different color formats."""
        center = (2, 2)
        radius = 1
        pos = (center[0] - radius, center[1])
        green_color = pygame.Color('green')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((3, 4))
        kwargs = {'surface' : surface,
                  'color'   : None,
                  'center'  : center,
                  'radius'  : radius,
                  'width'   : 0}
        greens = ((0, 255, 0), (0, 255, 0, 255), surface.map_rgb(green_color),
                  green_color)

        for color in greens:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['color'] = color

            if isinstance(color, int):
                expected_color = surface.unmap_rgb(color)
            else:
                expected_color = green_color

            bounds_rect = self.draw_circle(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_circle__invalid_color_formats(self):
        """Ensures draw circle handles invalid color formats correctly."""
        kwargs = {'surface' : pygame.Surface((4, 3)),
                  'color'   : None,
                  'center'  : (1, 2),
                  'radius'  : 1,
                  'width'   : 0}

        # These color formats are currently not supported (it would be
        # nice to eventually support them).
        for expected_color in ('green', '#00FF00FF', '0x00FF00FF'):
            kwargs['color'] = expected_color

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_circle(**kwargs)

    def test_circle__floats(self):
        """Ensure that floats are accepted."""
        draw.circle(
            surface=pygame.Surface((4, 4)),
            color=(255, 255, 127),
            center=(1.5, 1.5),
            radius=1,
            width=0,
        )

        draw.circle(
            surface=pygame.Surface((4, 4)),
            color=(255, 255, 127),
            center=Vector2(1.5, 1.5),
            radius=1,
            width=0,
        )


class DrawCircleTest(DrawCircleMixin, DrawTestCase):
    """Test draw module function circle.

    This class inherits the general tests from DrawCircleMixin. It is also
    the class to add any draw.circle specific tests to.
    """


# Commented out to avoid cluttering the test output. Add back in if draw_py
# ever properly supports drawing circles.
#@unittest.skip('draw_py.draw_circle not supported yet')
#class PythonDrawCircleTest(DrawCircleMixin, PythonDrawTestCase):
#    """Test draw_py module function draw_circle."
#
#    This class inherits the general tests from DrawCircleMixin. It is also
#    the class to add any draw_py.draw_circle specific tests to.
#    """


### Arc Testing ###############################################################

class DrawArcMixin(object):
    """Mixin tests for drawing arcs.

    This class contains all the general arc drawing tests.
    """

    def test_arc__args(self):
        """Ensures draw arc accepts the correct args."""
        bounds_rect = self.draw_arc(pygame.Surface((3, 3)),
            (0, 10, 0, 50), (1, 1, 2, 2), 0, 1, 1)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_arc__args_without_width(self):
        """Ensures draw arc accepts the args without a width."""
        bounds_rect = self.draw_arc(pygame.Surface((2, 2)), (1, 1, 1, 99),
                                    pygame.Rect((0, 0), (2, 2)), 1.1, 2.1)

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_arc__kwargs(self):
        """Ensures draw arc accepts the correct kwargs
        with and without a width arg.
        """
        kwargs_list = [{'surface'     : pygame.Surface((4, 4)),
                        'color'       : pygame.Color('yellow'),
                        'rect'        : pygame.Rect((0, 0), (3, 2)),
                        'start_angle' : 0.5,
                        'stop_angle'  : 3,
                        'width'       : 1},

                       {'surface'     : pygame.Surface((2, 1)),
                        'color'       : (0, 10, 20),
                        'rect'        : (0, 0, 2, 2),
                        'start_angle' : 1,
                        'stop_angle'  : 3.1}]

        for kwargs in kwargs_list:
            bounds_rect = self.draw_arc(**kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_arc__kwargs_order_independent(self):
        """Ensures draw arc's kwargs are not order dependent."""
        bounds_rect = self.draw_arc(stop_angle=1,
                                    start_angle=2.2,
                                    color=(1, 2, 3),
                                    surface=pygame.Surface((3, 2)),
                                    width=1,
                                    rect=pygame.Rect((1, 0), (2, 3)))

        self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_arc__args_missing(self):
        """Ensures draw arc detects any missing required args."""
        surface = pygame.Surface((1, 1))
        color = pygame.Color('red')
        rect = pygame.Rect((0, 0), (2, 2))

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_arc(surface, color, rect, 0.1)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_arc(surface, color, rect)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_arc(surface, color)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_arc(surface)

        with self.assertRaises(TypeError):
            bounds_rect = self.draw_arc()

    def test_arc__kwargs_missing(self):
        """Ensures draw arc detects any missing required kwargs."""
        kwargs = {'surface'     : pygame.Surface((1, 2)),
                  'color'       : pygame.Color('red'),
                  'rect'        : pygame.Rect((1, 0), (2, 2)),
                  'start_angle' : 0.1,
                  'stop_angle'  : 2,
                  'width'       : 1}

        for name in ('stop_angle', 'start_angle', 'rect', 'color', 'surface'):
            invalid_kwargs = dict(kwargs)
            invalid_kwargs.pop(name)  # Pop from a copy.

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_arc(**invalid_kwargs)

    def test_arc__arg_invalid_types(self):
        """Ensures draw arc detects invalid arg types."""
        surface = pygame.Surface((2, 2))
        color = pygame.Color('blue')
        rect = pygame.Rect((1, 1), (3, 3))

        with self.assertRaises(TypeError):
            # Invalid width.
            bounds_rect = self.draw_arc(surface, color, rect, 0, 1, '1')

        with self.assertRaises(TypeError):
            # Invalid stop_angle.
            bounds_rect = self.draw_arc(surface, color, rect, 0, '1', 1)

        with self.assertRaises(TypeError):
            # Invalid start_angle.
            bounds_rect = self.draw_arc(surface, color, rect, '1', 0, 1)

        with self.assertRaises(TypeError):
            # Invalid rect.
            bounds_rect = self.draw_arc(surface, color, (1, 2, 3, 4, 5),
                                        0, 1, 1)

        with self.assertRaises(TypeError):
            # Invalid color.
            bounds_rect = self.draw_arc(surface, 'blue', rect, 0, 1, 1)

        with self.assertRaises(TypeError):
            # Invalid surface.
            bounds_rect = self.draw_arc(rect, color, rect, 0, 1, 1)

    def test_arc__kwarg_invalid_types(self):
        """Ensures draw arc detects invalid kwarg types."""
        surface = pygame.Surface((3, 3))
        color = pygame.Color('green')
        rect = pygame.Rect((0, 1), (4, 2))
        start = 3
        stop = 4
        kwargs_list = [{'surface'     : pygame.Surface,  # Invalid surface.
                        'color'       : color,
                        'rect'        : rect,
                        'start_angle' : start,
                        'stop_angle'  : stop,
                        'width'       : 1},

                       {'surface'     : surface,
                        'color'       : 'green',  # Invalid color.
                        'rect'        : rect,
                        'start_angle' : start,
                        'stop_angle'  : stop,
                        'width'       : 1},

                       {'surface'     : surface,
                        'color'       : color,
                        'rect'        : (0, 0, 0),  # Invalid rect.
                        'start_angle' : start,
                        'stop_angle'  : stop,
                        'width'       : 1},

                       {'surface'     : surface,
                        'color'       : color,
                        'rect'        : rect,
                        'start_angle' : '1',  # Invalid start_angle.
                        'stop_angle'  : stop,
                        'width'       : 1},

                       {'surface'     : surface,
                        'color'       : color,
                        'rect'        : rect,
                        'start_angle' : start,
                        'stop_angle'  : '1',  # Invalid stop_angle.
                        'width'       : 1},

                       {'surface'     : surface,
                        'color'       : color,
                        'rect'        : rect,
                        'start_angle' : start,
                        'stop_angle'  : stop,
                        'width'       : 1.1}]  # Invalid width.

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_arc(**kwargs)

    def test_arc__kwarg_invalid_name(self):
        """Ensures draw arc detects invalid kwarg names."""
        surface = pygame.Surface((2, 3))
        color = pygame.Color('cyan')
        rect = pygame.Rect((0, 1), (2, 2))
        start = 0.9
        stop = 2.3
        kwargs_list = [{'surface'     : surface,
                        'color'       : color,
                        'rect'        : rect,
                        'start_angle' : start,
                        'stop_angle'  : stop,
                        'width'       : 1,
                        'invalid'     : 1},

                       {'surface'     : surface,
                        'color'       : color,
                        'rect'        : rect,
                        'start_angle' : start,
                        'stop_angle'  : stop,
                        'invalid'     : 1}]

        for kwargs in kwargs_list:
            with self.assertRaises(TypeError):
                bounds_rect = self.draw_arc(**kwargs)

    def test_arc__args_and_kwargs(self):
        """Ensures draw arc accepts a combination of args/kwargs"""
        surface = pygame.Surface((3, 1))
        color = (255, 255, 0, 0)
        rect = pygame.Rect((1, 0), (2, 3))
        start = 0.6
        stop = 2
        width = 1
        kwargs = {'surface'     : surface,
                  'color'       : color,
                  'rect'        : rect,
                  'start_angle' : start,
                  'stop_angle'  : stop,
                  'width'       : width}

        for name in ('surface', 'color', 'rect', 'start_angle', 'stop_angle'):
            kwargs.pop(name)

            if 'surface' == name:
                bounds_rect = self.draw_arc(surface, **kwargs)
            elif 'color' == name:
                bounds_rect = self.draw_arc(surface, color, **kwargs)
            elif 'rect' == name:
                bounds_rect = self.draw_arc(surface, color, rect, **kwargs)
            elif 'start_angle' == name:
                bounds_rect = self.draw_arc(surface, color, rect, start,
                                            **kwargs)
            elif 'stop_angle' == name:
                bounds_rect = self.draw_arc(surface, color, rect, start,
                                            stop, **kwargs)
            else:
                bounds_rect = self.draw_arc(surface, color, rect, start,
                                            stop, width, **kwargs)

            self.assertIsInstance(bounds_rect, pygame.Rect)

    # This decorator can be removed when the arc portion of issues #975
    # and #976 are resolved.
    @unittest.expectedFailure
    def test_arc__valid_width_values(self):
        """Ensures draw arc accepts different width values."""
        arc_color = pygame.Color('yellow')
        surface_color = pygame.Color('white')
        surface = pygame.Surface((6, 6))
        rect = pygame.Rect((0, 0), (4, 4))
        rect.center = surface.get_rect().center
        pos = rect.centerx + 1, rect.centery + 1
        kwargs = {'surface'     : surface,
                  'color'       : arc_color,
                  'rect'        : rect,
                  'start_angle' : 0,
                  'stop_angle'  : 7,
                  'width'       : None}

        for width in (-50, -10, -3, -2, -1, 0, 1, 2, 3, 10, 50):
            msg = 'width={}'.format(width)
            surface.fill(surface_color)  # Clear for each test.
            kwargs['width'] = width
            expected_color = arc_color if width > 0 else surface_color

            bounds_rect = self.draw_arc(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color, msg)
            self.assertIsInstance(bounds_rect, pygame.Rect, msg)

    def test_arc__valid_stop_angle_values(self):
        """Ensures draw arc accepts different stop_angle values."""
        expected_color = pygame.Color('blue')
        surface_color = pygame.Color('white')
        surface = pygame.Surface((6, 6))
        rect = pygame.Rect((0, 0), (4, 4))
        rect.center = surface.get_rect().center
        pos = rect.centerx, rect.centery + 1
        kwargs = {'surface'     : surface,
                  'color'       : expected_color,
                  'rect'        : rect,
                  'start_angle' : -17,
                  'stop_angle'  : None,
                  'width'       : 1}

        for stop_angle in (-10, -5.5, -1, 0, 1, 5.5, 10):
            msg = 'stop_angle={}'.format(stop_angle)
            surface.fill(surface_color)  # Clear for each test.
            kwargs['stop_angle'] = stop_angle

            bounds_rect = self.draw_arc(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color, msg)
            self.assertIsInstance(bounds_rect, pygame.Rect, msg)

    def test_arc__valid_start_angle_values(self):
        """Ensures draw arc accepts different start_angle values."""
        expected_color = pygame.Color('blue')
        surface_color = pygame.Color('white')
        surface = pygame.Surface((6, 6))
        rect = pygame.Rect((0, 0), (4, 4))
        rect.center = surface.get_rect().center
        pos = rect.centerx + 1, rect.centery + 1
        kwargs = {'surface'     : surface,
                  'color'       : expected_color,
                  'rect'        : rect,
                  'start_angle' : None,
                  'stop_angle'  : 17,
                  'width'       : 1}

        for start_angle in (-10.0, -5.5, -1, 0, 1, 5.5, 10.0):
            msg = 'start_angle={}'.format(start_angle)
            surface.fill(surface_color)  # Clear for each test.
            kwargs['start_angle'] = start_angle

            bounds_rect = self.draw_arc(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color, msg)
            self.assertIsInstance(bounds_rect, pygame.Rect, msg)

    def test_arc__valid_rect_formats(self):
        """Ensures draw arc accepts different rect formats."""
        expected_color = pygame.Color('red')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((6, 6))
        rect = pygame.Rect((0, 0), (4, 4))
        rect.center = surface.get_rect().center
        pos = rect.centerx + 1, rect.centery + 1
        kwargs = {'surface'     : surface,
                  'color'       : expected_color,
                  'rect'        : None,
                  'start_angle' : 0,
                  'stop_angle'  : 7,
                  'width'       : 1}
        rects = (rect, (rect.topleft, rect.size),
                 (rect.x, rect.y, rect.w, rect.h))

        for rect in rects:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['rect'] = rect

            bounds_rect = self.draw_arc(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_arc__valid_color_formats(self):
        """Ensures draw arc accepts different color formats."""
        green_color = pygame.Color('green')
        surface_color = pygame.Color('black')
        surface = pygame.Surface((6, 6))
        rect = pygame.Rect((0, 0), (4, 4))
        rect.center = surface.get_rect().center
        pos = rect.centerx + 1, rect.centery + 1
        kwargs = {'surface'     : surface,
                  'color'       : None,
                  'rect'        : rect,
                  'start_angle' : 0,
                  'stop_angle'  : 7,
                  'width'       : 1}
        greens = ((0, 255, 0), (0, 255, 0, 255), surface.map_rgb(green_color),
                  green_color)

        for color in greens:
            surface.fill(surface_color)  # Clear for each test.
            kwargs['color'] = color

            if isinstance(color, int):
                expected_color = surface.unmap_rgb(color)
            else:
                expected_color = green_color

            bounds_rect = self.draw_arc(**kwargs)

            self.assertEqual(surface.get_at(pos), expected_color)
            self.assertIsInstance(bounds_rect, pygame.Rect)

    def test_arc__invalid_color_formats(self):
        """Ensures draw arc handles invalid color formats correctly."""
        pos = (1, 1)
        surface_color = pygame.Color('black')
        surface = pygame.Surface((4, 3))
        kwargs = {'surface'     : surface,
                  'color'       : None,
                  'rect'        : pygame.Rect(pos, (2, 2)),
                  'start_angle' : 5,
                  'stop_angle'  : 6.1,
                  'width'       : 1}

        # These color formats are currently not supported (it would be
        # nice to eventually support them).
        for expected_color in ('green', '#00FF00FF', '0x00FF00FF'):
            kwargs['color'] = expected_color

            with self.assertRaises(TypeError):
                bounds_rect = self.draw_arc(**kwargs)

    def todo_test_arc(self):
        """Ensure draw arc works correctly."""
        self.fail()


class DrawArcTest(DrawArcMixin, DrawTestCase):
    """Test draw module function arc.

    This class inherits the general tests from DrawArcMixin. It is also the
    class to add any draw.arc specific tests to.
    """


# Commented out to avoid cluttering the test output. Add back in if draw_py
# ever properly supports drawing arcs.
#@unittest.skip('draw_py.draw_arc not supported yet')
#class PythonDrawArcTest(DrawArcMixin, PythonDrawTestCase):
#    """Test draw_py module function draw_arc.
#
#    This class inherits the general tests from DrawArcMixin. It is also the
#    class to add any draw_py.draw_arc specific tests to.
#    """


### Draw Module Testing #######################################################

class DrawModuleTest(unittest.TestCase):
    """General draw module tests."""

    def test_path_data_validation(self):
        """Test validation of multi-point drawing methods.

        See bug #521
        """
        surf = pygame.Surface((5, 5))
        rect = pygame.Rect(0, 0, 5, 5)
        bad_values = ('text', b'bytes', 1 + 1j,  # string, bytes, complex,
                       object(), (lambda x: x))  # object, function
        bad_points = list(bad_values) + [(1,) , (1, 2, 3)] # wrong tuple length
        bad_points.extend((1, v) for v in bad_values)  # one wrong value
        good_path = [(1, 1), (1, 3), (3, 3), (3, 1)]
        # A) draw.lines
        check_pts = [(x, y) for x in range(5) for y in range(5)]

        for method, is_polgon in ((draw.lines, 0), (draw.aalines, 0),
                                  (draw.polygon, 1)):
            for val in bad_values:
                # 1. at the beginning
                draw.rect(surf, RED, rect, 0)
                with self.assertRaises(TypeError):
                    if is_polgon:
                        method(surf, GREEN, [val] + good_path, 0)
                    else:
                        method(surf, GREEN, True, [val] + good_path)

                # make sure, nothing was drawn :
                self.assertTrue(
                    all(surf.get_at(pt) == RED for pt in check_pts))

                # 2. not at the beginning (was not checked)
                draw.rect(surf, RED, rect, 0)
                with self.assertRaises(TypeError):
                    path = good_path[:2] + [val] + good_path[2:]
                    if is_polgon:
                        method(surf, GREEN, path, 0)
                    else:
                        method(surf, GREEN, True, path)

                # make sure, nothing was drawn :
                self.assertTrue(
                    all(surf.get_at(pt) == RED for pt in check_pts))

    def test_color_validation(self):
        surf = pygame.Surface((10, 10))
        colors = 123456, (1, 10, 100), RED # but not '#ab12df' or 'red' ...
        points = ((0, 0), (1, 1), (1, 0))

        # 1. valid colors
        for col in colors:
            draw.line(surf, col, (0, 0), (1, 1))
            draw.aaline(surf, col, (0, 0), (1, 1))
            draw.aalines(surf, col, True, points)
            draw.lines(surf, col, True, points)
            draw.arc(surf, col, pygame.Rect(0, 0, 3, 3), 15, 150)
            draw.ellipse(surf, col, pygame.Rect(0, 0, 3, 6), 1)
            draw.circle(surf, col, (7, 3), 2)
            draw.polygon(surf, col, points, 0)

        # 2. invalid colors
        for col in ('invalid', 1.256, object(), None, '#ab12df', 'red'):
            with self.assertRaises(TypeError):
                draw.line(surf, col, (0, 0), (1, 1))

            with self.assertRaises(TypeError):
                draw.aaline(surf, col, (0, 0), (1, 1))

            with self.assertRaises(TypeError):
                draw.aalines(surf, col, True, points)

            with self.assertRaises(TypeError):
                draw.lines(surf, col, True, points)

            with self.assertRaises(TypeError):
                draw.arc(surf, col, pygame.Rect(0, 0, 3, 3), 15, 150)

            with self.assertRaises(TypeError):
                draw.ellipse(surf, col, pygame.Rect(0, 0, 3, 6), 1)

            with self.assertRaises(TypeError):
                draw.circle(surf, col, (7, 3), 2)

            with self.assertRaises(TypeError):
                draw.polygon(surf, col, points, 0)


###############################################################################


if __name__ == '__main__':
    unittest.main()
