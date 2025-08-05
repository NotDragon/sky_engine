from sky_engine import *

sun_obj = None

def create_global_objects(engine):
	global sun_obj

	sun_obj = engine.create_object("Sun")
	sun_comp = SunComponent()
	sun_obj.add_component(sun_comp)
	sun_obj.set_position(Vec(0, 0, 0))
	sun_obj.set_scale(Vec(1, 1, 1))

	sun_comp.set_intensity(300.0)
	sun_comp.set_photosphere_intensity(1.0)

def usra_story():

	engine = SkyEngine()

	create_global_objects(engine)

	engine.runAll()


if __name__ == "__main__":

	usra_story()