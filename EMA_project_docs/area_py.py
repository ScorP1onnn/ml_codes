import pyregion
from astropy.coordinates import Angle
from astropy.cosmology import FlatLambdaCDM
import numpy as np
from astropy import units as u
cosmo = FlatLambdaCDM(H0=70, Om0=0.3,Tcmb0=2.7255,Neff=3.046) #Cosmology Used
from mpdaf.obj import Cube


zap = "/home/sai/Desktop/muse_datacubes/P183p05_DATACUBE_ZAP.fits"
cube = Cube(zap)

print(cube.info())


b = pyregion.open('/home/sai/Desktop/boxs_wcs.reg')



b_2 =  pyregion.open('/home/sai/Desktop/manual_remove.reg')

"""
b is the list of boxes used for mask. b[0].coord_list[2] and b[0].coord_list[3] gives the dimensions 
(length and width) of each box in degrees. There are around 61 boxes. Below is the code to calculate the area of all
the boxes in kpc^2.


b_2 is a list of circles I have created manually to remove some obvious contaminants. While the radius of each circle
is 0.8 arcsecond, I have only removed the area using the same circles with a radius of 0.5 arcsecond (instead of 0.8  to
prevent some overlapping between the boxes and the circles).
There are 24 circles. The area of each circle is the same. 
The "total_area_circles" gives the total area covered by the circles of radius 0.5 arcsec, which is equal to 567.71 kpc2. 

The final area (area_boxes + area_circles) is around 8956.286 kpc^2 or 0.008956 Mpc^2




I removed "20 pixels" from the edges of each side. This corresponds to 4 arcsec from each side (1px = 0.2 arcsec).
The total cube area is 64.0" x 64.6". Therefore the rest of the area is (64.0" - 8") * (64.6" - 8"), which is around
= 0.0954 Mpc^2


Two boxes overlap with the region removed by the edges (see picture). The total area of the two boxes = 674.63 kpc2
or 0.000674 Mpc2


So, The total area used for the plot = 0.0954 Mpc^2 - 0.008956 Mpc^2 + 0.000674 = 0.0872 Mpc^2 (0.08717964877429167 Mpc^2)


Feel Free to ask me anything if you have any doubt

"""
z = 6.4386 #since we are aiming at clustering at the QSO redshift.
d = cosmo.angular_diameter_distance(z)




total_area_box = 0
for i in range(len(b)):
    l = Angle(b[i].coord_list[2]/1,u.degree)
    w = Angle(b[i].coord_list[3]/1,u.degree)
    #print(l.degree)
    #print(w.degree)
    #print(l.arcsec)
    #print(w.arcsec)

    l_physical = (l * d).to(u.kpc, u.dimensionless_angles())
    w_physical = (w * d).to(u.kpc, u.dimensionless_angles())

    #print(l_physical,w_physical)
    #print(l_physical * w_physical)
    #print("")

    total_area_box = total_area_box + (l_physical * w_physical)




print(f"Total area from boxes = {total_area_box}")


total_area_circles = len(b_2) * np.pi * ((Angle(0.5,u.arcsec) * cosmo.angular_diameter_distance(z)).to(u.kpc, u.dimensionless_angles()) ** 2)
print(f"Total area of circles = {total_area_circles}")



print(f"Total Area Masked = {total_area_box + total_area_circles}")
print(f"\nTotal Area Masked in Mpc2 = {(total_area_box + total_area_circles).to(u.Mpc**2, u.dimensionless_angles())}")


cube_length = Angle(64.0 - 8,u.arcsec)
cube_width = Angle(64.6 - 8,u.arcsec)
cub_area = (cube_length * d).to(u.kpc, u.dimensionless_angles()) *  (cube_width * d).to(u.kpc, u.dimensionless_angles())
print(f"Cube area = {cub_area.to(u.Mpc ** 2, u.dimensionless_angles())}")






print()


overlap_box_1 = (Angle(0.8,u.arcsec) * d).to(u.kpc, u.dimensionless_angles()) * ( Angle(15.8,u.arcsec) * d).to(u.kpc, u.dimensionless_angles())
overlap_box_2 = (Angle(0.8,u.arcsec) * d).to(u.kpc, u.dimensionless_angles()) * ( Angle(12.2,u.arcsec) * d).to(u.kpc, u.dimensionless_angles())

print(f"area of the two boxes = {overlap_box_1 + overlap_box_2}")
print(f"area of the two boxes = {(overlap_box_1 + overlap_box_2).to(u.Mpc**2, u.dimensionless_angles())}")



print(f"\nThe total area used for the plot = {cub_area.to(u.Mpc**2, u.dimensionless_angles()) - (total_area_box + total_area_circles).to(u.Mpc**2, u.dimensionless_angles()) + (overlap_box_1 + overlap_box_2).to(u.Mpc**2, u.dimensionless_angles())}")
