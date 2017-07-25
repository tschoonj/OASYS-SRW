import numpy

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from syned.beamline.optical_elements.gratings.grating import Grating

from wofrysrw.beamline.optical_elements.mirrors.srw_mirror import Orientation
from wofrysrw.beamline.optical_elements.gratings.srw_grating import SRWGrating

from orangecontrib.srw.widgets.gui.ow_srw_optical_element import OWSRWOpticalElement

class OWSRWGrating(OWSRWOpticalElement):

    tangential_size                    = Setting(1.2)
    sagittal_size                      = Setting(0.01)
    horizontal_position_of_mirror_center = Setting(0.0)
    vertical_position_of_mirror_center = Setting(0.0)

    has_height_profile = Setting(0)
    height_profile_data_file           = Setting("mirror.dat")
    height_profile_data_file_dimension = Setting(0)
    height_amplification_coefficient   = Setting(1.0)

    diffraction_order                  = Setting(1)
    grooving_density_0                 = Setting(800) # groove density [lines/mm] (coefficient a0 in the polynomial groove density: a0 + a1*y + a2*y^2 + a3*y^3 + a4*y^4)
    grooving_density_1                 = Setting(0.0) # groove density polynomial coefficient a1 [lines/mm^2]
    grooving_density_2                 = Setting(0.0) # groove density polynomial coefficient a2 [lines/mm^3]
    grooving_density_3                 = Setting(0.0) # groove density polynomial coefficient a3 [lines/mm^4]
    grooving_density_4                 = Setting(0.0)  # groove density polynomial coefficient a4 [lines/mm^5]

    def __init__(self):
        super().__init__(azimuth_hor_vert=True)

    def draw_specific_box(self):
        
        self.grating_setting = oasysgui.tabWidget(self.tab_bas)
        
        substrate_tab = oasysgui.createTabPage(self.grating_setting, "Substrate Mirror Setting")
        grooving_tab = oasysgui.createTabPage(self.grating_setting, "Grooving Setting")

        self.substrate_box = oasysgui.widgetBox(substrate_tab, "", addSpace=False, orientation="vertical")
        self.grooving_box = oasysgui.widgetBox(grooving_tab, "", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(self.substrate_box, self, "tangential_size", "Tangential Size [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.substrate_box, self, "sagittal_size", "Sagittal_Size [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.substrate_box, self, "horizontal_position_of_mirror_center", "Horizontal position of mirror center [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.substrate_box, self, "vertical_position_of_mirror_center", "Vertical position of mirror center [m]", labelWidth=260, valueType=float, orientation="horizontal")

        gui.comboBox(self.substrate_box, self, "has_height_profile", label="Use Height Error Profile",
                     items=["No", "Yes"], labelWidth=300,
                     sendSelectedValue=False, orientation="horizontal", callback=self.set_HeightProfile)

        self.height_profile_box_1 = oasysgui.widgetBox(self.substrate_box, "", addSpace=False, orientation="vertical", height=100)

        self.height_profile_box_2 = oasysgui.widgetBox(self.substrate_box, "", addSpace=False, orientation="vertical", height=100)

        file_box =  oasysgui.widgetBox(self.height_profile_box_2, "", addSpace=False, orientation="horizontal")

        self.le_height_profile_data_file = oasysgui.lineEdit(file_box, self, "height_profile_data_file", "Height profile data file", labelWidth=185, valueType=str, orientation="horizontal")
        gui.button(file_box, self, "...", callback=self.selectHeightProfileDataFile)

        gui.comboBox(self.height_profile_box_2, self, "height_profile_data_file_dimension", label="Dimension",
                     items=["1", "2"], labelWidth=300,
                     sendSelectedValue=False, orientation="horizontal")

        oasysgui.lineEdit(self.height_profile_box_2, self, "height_amplification_coefficient", "Height Amplification Coefficient", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_HeightProfile()
        
        oasysgui.lineEdit(self.grooving_box, self, "diffraction_order", "Diffraction order", labelWidth=260, valueType=int, orientation="horizontal")
        oasysgui.lineEdit(self.grooving_box, self, "grooving_density_0", "Groove density [lines/mm]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.grooving_box, self, "grooving_density_1", "Groove den. poly. coeff. a1 [lines/mm^2]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.grooving_box, self, "grooving_density_2", "Groove den. poly. coeff. a2 [lines/mm^3]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.grooving_box, self, "grooving_density_3", "Groove den. poly. coeff. a3 [lines/mm^4]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.grooving_box, self, "grooving_density_4", "Groove den. poly. coeff. a4 [lines/mm^5]", labelWidth=260, valueType=float, orientation="horizontal")

    def selectHeightProfileDataFile(self):
        self.le_height_profile_data_file.setText(oasysgui.selectFileFromDialog(self, self.height_profile_data_file, "Height profile data file"))

    def set_HeightProfile(self):
        self.height_profile_box_1.setVisible(self.has_height_profile==0)
        self.height_profile_box_2.setVisible(self.has_height_profile==1)

    def get_optical_element(self):

        grating = self.get_grating_instance()

        grating.name=self.oe_name
        grating.tangential_size=self.tangential_size
        grating.sagittal_size=self.sagittal_size
        grating.grazing_angle=numpy.radians(self.angle_radial)
        grating.orientation_of_reflection_plane=self.orientation_azimuthal
        grating.height_profile_data_file=self.height_profile_data_file if self.has_height_profile else None
        grating.height_profile_data_file_dimension=self.height_profile_data_file_dimension + 1
        grating.height_amplification_coefficient=self.height_amplification_coefficient
        grating.diffraction_order=self.diffraction_order
        grating.grooving_density_0=self.grooving_density_0
        grating.grooving_density_1=self.grooving_density_1
        grating.grooving_density_2=self.grooving_density_2
        grating.grooving_density_3=self.grooving_density_3
        grating.grooving_density_4=self.grooving_density_4

        return grating

    def get_grating_instance(self):
        return SRWGrating()

    def receive_specific_syned_data(self, optical_element):
        if not optical_element is None:
            if isinstance(optical_element, Grating):
                boundaries = optical_element._boundary_shape.get_boundaries()

                self.tangential_size=round(abs(boundaries[3] - boundaries[2]), 6)
                self.sagittal_size=round(abs(boundaries[1] - boundaries[0]), 6)

                self.vertical_position_of_mirror_center = round(0.5*(boundaries[3] + boundaries[2]), 6)
                self.horizontal_position_of_mirror_center = round(0.5*(boundaries[1] + boundaries[0]), 6)
                
                self.grooving_density_0=optical_element._ruling
                
                self.receive_shape_specific_syned_data(optical_element)
            else:
                raise Exception("Syned Data not correct: Optical Element is not a Grating")
        else:
            raise Exception("Syned Data not correct: Empty Optical Element")

    def receive_shape_specific_syned_data(self, optical_element):
        raise NotImplementedError


    def check_data(self):
        super().check_data()

        congruence.checkStrictlyPositiveNumber(self.tangential_size, "Tangential Size")
        congruence.checkStrictlyPositiveNumber(self.sagittal_size, "Sagittal Size")

        if self.has_height_profile:
            congruence.checkFile(self.height_profile_data_file)

        congruence.checkPositiveNumber(self.diffraction_order, "Diffraction Order")