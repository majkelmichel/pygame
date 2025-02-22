/* Auto generated file: with makeref.py .  Docs go in docs/reST/ref/ . */
#define DOC_PYGAMEMASK "pygame module for image masks."
#define DOC_PYGAMEMASKFROMSURFACE "from_surface(Surface) -> Mask\nfrom_surface(Surface, threshold=127) -> Mask\nCreates a Mask from the given surface"
#define DOC_PYGAMEMASKFROMTHRESHOLD "from_threshold(Surface, color) -> Mask\nfrom_threshold(Surface, color, threshold=(0, 0, 0, 255), othersurface=None, palette_colors=1) -> Mask\nCreates a mask by thresholding Surfaces"
#define DOC_PYGAMEMASKMASK "Mask(size=(width, height)) -> Mask\nMask(size=(width, height), fill=False) -> Mask\npygame object for representing 2D bitmasks"
#define DOC_MASKGETSIZE "get_size() -> (width, height)\nReturns the size of the mask"
#define DOC_MASKGETRECT "get_rect(**kwargs) -> Rect\nReturns a Rect based on the size of the mask"
#define DOC_MASKGETAT "get_at((x, y)) -> int\nGets the bit at the given position"
#define DOC_MASKSETAT "set_at((x, y)) -> None\nset_at((x, y), value=1) -> None\nSets the bit at the given position"
#define DOC_MASKOVERLAP "overlap(othermask, offset) -> (x, y)\noverlap(othermask, offset) -> None\nReturns the point of intersection"
#define DOC_MASKOVERLAPAREA "overlap_area(othermask, offset) -> numbits\nReturns the number of overlapping set bits"
#define DOC_MASKOVERLAPMASK "overlap_mask(othermask, offset) -> Mask\nReturns a mask of the overlapping set bits"
#define DOC_MASKFILL "fill() -> None\nSets all bits to 1"
#define DOC_MASKCLEAR "clear() -> None\nSets all bits to 0"
#define DOC_MASKINVERT "invert() -> None\nFlips all the bits"
#define DOC_MASKSCALE "scale((width, height)) -> Mask\nResizes a mask"
#define DOC_MASKDRAW "draw(othermask, offset) -> None\nDraws a mask onto another"
#define DOC_MASKERASE "erase(othermask, offset) -> None\nErases a mask from another"
#define DOC_MASKCOUNT "count() -> bits\nReturns the number of set bits"
#define DOC_MASKCENTROID "centroid() -> (x, y)\nReturns the centroid of the set bits"
#define DOC_MASKANGLE "angle() -> theta\nReturns the orientation of the set bits"
#define DOC_MASKOUTLINE "outline() -> [(x, y), ...]\noutline(every=1) -> [(x, y), ...]\nReturns a list of points outlining an object"
#define DOC_MASKCONVOLVE "convolve(othermask) -> Mask\nconvolve(othermask, outputmask=None, offset=(0, 0)) -> Mask\nReturns the convolution of this mask with another mask"
#define DOC_MASKCONNECTEDCOMPONENT "connected_component() -> Mask\nconnected_component((x, y)) -> Mask\nReturns a mask containing a connected component"
#define DOC_MASKCONNECTEDCOMPONENTS "connected_components() -> [Mask, ...]\nconnected_components(min=0) -> [Mask, ...]\nReturns a list of masks of connected components"
#define DOC_MASKGETBOUNDINGRECTS "get_bounding_rects() -> [Rect, ...]\nReturns a list of bounding rects of connected components"
#define DOC_MASKTOSURFACE "to_surface(surface)) -> Surface\nto_surface(surface, setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255)) -> Surface\nReturns a surface with the mask drawn on it"


/* Docs in a comment... slightly easier to read. */

/*

pygame.mask
pygame module for image masks.

pygame.mask.from_surface
 from_surface(Surface) -> Mask
 from_surface(Surface, threshold=127) -> Mask
Creates a Mask from the given surface

pygame.mask.from_threshold
 from_threshold(Surface, color) -> Mask
 from_threshold(Surface, color, threshold=(0, 0, 0, 255), othersurface=None, palette_colors=1) -> Mask
Creates a mask by thresholding Surfaces

pygame.mask.Mask
 Mask(size=(width, height)) -> Mask
 Mask(size=(width, height), fill=False) -> Mask
pygame object for representing 2D bitmasks

pygame.mask.Mask.get_size
 get_size() -> (width, height)
Returns the size of the mask

pygame.mask.Mask.get_rect
 get_rect(**kwargs) -> Rect
Returns a Rect based on the size of the mask

pygame.mask.Mask.get_at
 get_at((x, y)) -> int
Gets the bit at the given position

pygame.mask.Mask.set_at
 set_at((x, y)) -> None
 set_at((x, y), value=1) -> None
Sets the bit at the given position

pygame.mask.Mask.overlap
 overlap(othermask, offset) -> (x, y)
 overlap(othermask, offset) -> None
Returns the point of intersection

pygame.mask.Mask.overlap_area
 overlap_area(othermask, offset) -> numbits
Returns the number of overlapping set bits

pygame.mask.Mask.overlap_mask
 overlap_mask(othermask, offset) -> Mask
Returns a mask of the overlapping set bits

pygame.mask.Mask.fill
 fill() -> None
Sets all bits to 1

pygame.mask.Mask.clear
 clear() -> None
Sets all bits to 0

pygame.mask.Mask.invert
 invert() -> None
Flips all the bits

pygame.mask.Mask.scale
 scale((width, height)) -> Mask
Resizes a mask

pygame.mask.Mask.draw
 draw(othermask, offset) -> None
Draws a mask onto another

pygame.mask.Mask.erase
 erase(othermask, offset) -> None
Erases a mask from another

pygame.mask.Mask.count
 count() -> bits
Returns the number of set bits

pygame.mask.Mask.centroid
 centroid() -> (x, y)
Returns the centroid of the set bits

pygame.mask.Mask.angle
 angle() -> theta
Returns the orientation of the set bits

pygame.mask.Mask.outline
 outline() -> [(x, y), ...]
 outline(every=1) -> [(x, y), ...]
Returns a list of points outlining an object

pygame.mask.Mask.convolve
 convolve(othermask) -> Mask
 convolve(othermask, outputmask=None, offset=(0, 0)) -> Mask
Returns the convolution of this mask with another mask

pygame.mask.Mask.connected_component
 connected_component() -> Mask
 connected_component((x, y)) -> Mask
Returns a mask containing a connected component

pygame.mask.Mask.connected_components
 connected_components() -> [Mask, ...]
 connected_components(min=0) -> [Mask, ...]
Returns a list of masks of connected components

pygame.mask.Mask.get_bounding_rects
 get_bounding_rects() -> [Rect, ...]
Returns a list of bounding rects of connected components

pygame.mask.Mask.to_surface
 to_surface(surface)) -> Surface
 to_surface(surface, setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255)) -> Surface
Returns a surface with the mask drawn on it

*/