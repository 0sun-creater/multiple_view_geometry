import numpy as np
from transform_utils import normalize_homogeneous_coordinates, points_to_homogeneous_coordinates

class Camera(object):
    def __init__(self, name, extrinsic, f=350, image_resolution=(1024, 768)):
        self._extrinsic = extrinsic # camera wrt world
        self._f = f # in pixel
        u0, v0 = np.array(image_resolution)/2
        self._image_resolution = image_resolution
        self._intrinsic = np.array([[f, 0, u0, 0], [0, f, v0, 0], [0,0,1,0]])
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def focal_length_in_pixels(self):
        return self._f

    @property
    def image_resolution(self):
        return self._image_resolution

    @property
    def intrinsic(self):
        return self._intrinsic

    @property
    def pixel_center(self):
        return np.array([self._intrinsic[0,2], self._intrinsic[1,2]])

    @property
    def extrinsic(self):
        return self._extrinsic

    def project(self, key_points):
        key_points_wrt_camera = self._extrinsic.inv().dot(key_points)
        points_in_image_frame = normalize_homogeneous_coordinates(self._intrinsic.dot(key_points_wrt_camera))
        #print(points_in_image_frame)
        image = np.zeros(self._image_resolution)

        return key_points_wrt_camera[:3,:], points_in_image_frame

    def points_2d_to_homogeneous_coordinates(self, points_2d):
        points_in_homogeneous_coordinates = points_to_homogeneous_coordinates(points_2d - self.pixel_center[:,np.newaxis], self._f)
        return points_in_homogeneous_coordinates/self._f


