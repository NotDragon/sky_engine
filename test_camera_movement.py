

from sky_engine import SkyEngine, Capture, Vec, PlanetComponent, AudioComponent
from skyExplorer import *

def capture_example():
	
	print("=== Capture Example ===")
	print("Demonstrating command recording and replay:")
	print("- Record camera movements")
	print("- Record object creation and manipulation")
	print("- Replay all recorded commands")
	

	print("\nInitializing Sky Engine...")
	sky_engine = SkyEngine()
	print("Sky Engine initialized!")
	

	capture = Capture(sky_engine)
	

	print("\nStarting capture...")
	capture.start()
	

	print("\nRecording camera movements...")
	sky_engine.set_camera_position(Vec(0, 0, 10))
	sky_engine.set_camera_rotation(Vec(0, 0, 0))
	sky_engine.set_camera_zoom(1.0)
	

	print("\nRecording object creation and manipulation...")
	obj1 = sky_engine.create_object("Recorded Object 1")
	obj1.set_position(Vec(5, 0, 0))
	obj1.set_rotation(Vec(0, 45, 0))
	
	obj2 = sky_engine.create_object("Recorded Object 2")
	obj2.set_position(Vec(-5, 0, 0))
	obj2.set_scale(Vec(2, 2, 2))
	

	planet_comp = PlanetComponent(Planet.PlanetName.Mars)
	obj1.add_component(planet_comp)
	
	audio_comp = AudioComponent("test_audio.mp3")
	obj2.add_component(audio_comp)
	

	print("\nRecording more camera movements...")
	sky_engine.move_camera(Vec(5, 0, 0))
	sky_engine.rotate_camera(Vec(0, 30, 0))
	sky_engine.zoom_camera(0.5)
	

	print("\nStopping capture...")
	capture.stop()
	

	print(f"\nRecorded {capture.get_instructions_count()} commands:")
	for i, instruction in enumerate(capture.get_instructions()):
		print(f"  {i+1}. {instruction['method']}({instruction['args']})")
	

	print("\nRunning recorded commands...")
	capture.run_capture()
	

	print("\nSaving instructions to file...")
	capture.save_instructions("captured_commands.json")
	

	print("\nCreating new capture and loading instructions...")
	new_capture = Capture(sky_engine)
	new_capture.load_instructions("captured_commands.json")
	

	print("\nRunning loaded commands...")
	new_capture.run_capture()
	
	print("\n=== Capture Example Complete! ===")

def capture_with_components_example():
	
	print("\n=== Capture with Components Example ===")
	

	sky_engine = SkyEngine()
	capture = Capture(sky_engine)
	

	capture.start()
	

	print("Recording object creation with components...")
	obj = sky_engine.create_object("Captured Planet")
	

	planet_comp = PlanetComponent(Planet.PlanetName.Earth)
	obj.add_component(planet_comp)
	
	audio_comp = AudioComponent("test_audio.mp3")
	obj.add_component(audio_comp)
	

	print("Recording object transformations...")
	obj.set_position(Vec(0, 0, 20))
	obj.set_rotation(Vec(0, 90, 0))
	obj.set_scale(Vec(1.5, 1.5, 1.5))
	

	print("Recording camera movements...")
	sky_engine.set_camera_position(Vec(0, 0, 20))
	sky_engine.look_at(Vec(0, 0, 0))
	

	capture.stop()
	

	print("Running recorded sequence...")
	capture.run_capture()
	
	print("=== Component Capture Example Complete! ===")

if __name__ == "__main__":

	capture_example()
	

	capture_with_components_example() 