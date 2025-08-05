from sky_engine import *
import time
import math

sun_obj = None
earth_obj = None
mars_obj = None
jupiter_obj = None
asteroid_obj = None
comet_obj = None
satellite_obj = None
audio_obj = None
clock_obj = None

def create_global_objects(engine):
	global sun_obj, earth_obj, mars_obj, jupiter_obj, asteroid_obj, comet_obj, satellite_obj, audio_obj, clock_obj
	

	sun_obj = engine.create_object("Sun")
	sun_comp = SunComponent()
	sun_obj.add_component(sun_comp)
	sun_obj.set_position(Vec(0, 0, 0))
	sun_obj.set_scale(Vec(3, 3, 3))
	sun_comp.set_intensity(2.0) ## <-
	

	sun_comp.set_corona_intensity(0.3)
	sun_comp.set_photosphere_intensity(1.0)
	sun_comp.set_magnetic_lines_intensity(0.2)
	sun_comp.set_habitable_zone_intensity(0.1)
	sun_comp.set_habitable_zone_color(Vec(0, 1, 0))
	

	earth_obj = engine.create_object("Earth")
	earth_comp = PlanetComponent(Planet.PlanetName.Earth)
	earth_obj.add_component(earth_comp)
	earth_obj.set_local_position(Vec(50, 0, 0))
	earth_obj.set_scale(Vec(2, 2, 2))
	sun_obj.add_child(earth_obj)
	

	earth_comp.set_clouds_intensity(0.7)
	earth_comp.set_cloud_speed(1.5)
	earth_comp.set_cloud_direction(1.0)
	earth_comp.set_cloud_thickness(0.7)
	earth_comp.set_cloud_raininess(0.3)
	earth_comp.set_scattering_intensity(0.8)
	earth_comp.set_terrain_intensity(0.9)
	earth_comp.set_terrain_rendering_mode("TOPOGRAPHY")
	earth_comp.set_sea_level_rendering_mode("WATER")
	earth_comp.set_tree_intensity(0.6)
	earth_comp.set_equatorial_grid_intensity(0.3)
	

	mars_obj = engine.create_object("Mars")
	mars_comp = PlanetComponent(Planet.PlanetName.Mars)
	mars_obj.add_component(mars_comp)
	mars_obj.set_local_position(Vec(-80, 0, 0))
	mars_obj.set_scale(Vec(1.5, 1.5, 1.5))
	sun_obj.add_child(mars_obj)
	

	mars_comp.set_terrain_intensity(1.0)
	mars_comp.set_terrain_rendering_mode("PHOTOGRAY")
	mars_comp.set_elevation_scale(3.0)
	mars_comp.set_shadow_strength(0.8)
	

	jupiter_obj = engine.create_object("Jupiter")
	jupiter_comp = PlanetComponent(Planet.PlanetName.Jupiter)
	jupiter_obj.add_component(jupiter_comp)
	jupiter_obj.set_local_position(Vec(120, 0, 0))
	jupiter_obj.set_scale(Vec(3, 3, 3)) 
	sun_obj.add_child(jupiter_obj)
	

	jupiter_comp.set_equatorial_grid_intensity(0.4)
	jupiter_comp.set_ecliptic_grid_intensity(0.2)
	

	asteroid_obj = engine.create_object("Asteroid Belt")
	asteroid_comp = AsteroidComponent(Asteroid.AsteroidName.Asteroid001)
	asteroid_obj.add_component(asteroid_comp)
	asteroid_obj.set_position(Vec(100, 0, 0))
	asteroid_obj.set_scale(Vec(0.5, 0.5, 0.5))
	asteroid_comp.set_orbit_intensity(0.5)
	asteroid_comp.set_trajectory_intensity(0.3)
	

	comet_obj = engine.create_object("Comet")
	comet_comp = CometComponent(Comet.CometName.Comet001)
	comet_obj.add_component(comet_comp)
	comet_obj.set_position(Vec(0, 60, 0))
	comet_obj.set_scale(Vec(1, 1, 1))
	comet_comp.set_tail_intensity(0.8)
	comet_comp.set_nucleus_intensity(1.0)
	comet_comp.set_trajectory_intensity(0.6)
	

	satellite_obj = engine.create_object("Moon")
	satellite_comp = SatelliteComponent(Satellite.SatelliteName.Moon)
	satellite_obj.add_component(satellite_comp)
	satellite_obj.set_position(Vec(0, 0, 10))
	satellite_obj.set_scale(Vec(0.3, 0.3, 0.3))
	satellite_comp.set_orbit_intensity(0.7)
	satellite_comp.set_trajectory_intensity(0.4)
	satellite_comp.set_model_intensity(1.0)
	

	clock_obj = engine.create_object("Time System")
	clock_comp = ClockComponent()
	clock_obj.add_component(clock_comp)
	clock_obj.set_position(Vec(0, 0, 0))
	clock_comp.start()
	clock_comp.set_time_scale(100.0)


@keyframe(transition_time=2.0, duration=1.0, frame_number=0)
def frame_0_initial_setup(engine):
	engine.set_camera_position(Vec(0, 0, 200))
	engine.set_camera_rotation(Vec(0, 0, 0))
	engine.set_camera_zoom(1.0)

@keyframe(transition_time=1.5, duration=2.0, frame_number=1)
def frame_1_camera_setup(engine):
	engine.set_camera_position(Vec(0, 50, 150))
	engine.set_camera_rotation(Vec(-20, 0, 0))
	engine.set_camera_zoom(0.8)
	
	engine.set_camera_focus(0.7)
	engine.set_camera_stereo_ratio(0.1)
	engine.set_camera_eye_distance(0.05)

def advanced_example():
	print("=== Advanced Sky Engine Example ===")
	print("Demonstrating all high-priority features:")
	print("- Advanced planet features (clouds, terrain, atmosphere)")
	print("- Advanced sun features (corona, magnetic, habitable zone)")
	print("- Audio system (single and layered)")
	print("- Time management (Clock and DateManager)")
	print("- Enhanced camera features (stereo, focus, screenshots)")
	print("- Additional celestial objects (asteroids, comets, satellites)")
	

	print("\nInitializing Sky Engine...")
	engine = SkyEngine()
	print("Sky Engine initialized!")
	create_global_objects(engine)

	print("\nStarting keyframe animation sequence...")
	engine.runAll()
	
	print("\n=== Demo Complete! ===")

if __name__ == "__main__":

	advanced_example()