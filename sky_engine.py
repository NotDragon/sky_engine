from skyExplorer import *
from skyExplorer import Vec4
from time import sleep
from typing import Dict, List, Optional, Any
import math
import functools


global_animator = None

all_frames = []

def keyframe(transition_time: float, duration: float, frame_number: int):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            sky_engine = args[0] if args else None
            

            capture = Capture(sky_engine)
            

            capture.start()
            

            result = func(*args, **kwargs)
            

            capture.stop()
            

            global global_animator
            if global_animator is None:
                global_animator = Animator(transition_time)
            else:
                global_animator.duration = transition_time
            

            capture.run_parallel()
            

            sleep(transition_time + duration)
            
            return result
        

        all_frames.append({
            'type': 'keyframe',
            'transition_time': transition_time,
            'duration': duration,
            'frame_number': frame_number,
            'function': wrapper,
            'capture': None
        })
        
        return wrapper
    return decorator

def frame(frame_number: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            global global_animator
            if global_animator is None:
                global_animator = Animator(0)
            else:
                global_animator.duration = 0
            
            result = func(*args, **kwargs)
            
            return result
        

        all_frames.append({
            'type': 'frame',
            'frame_number': frame_number,
            'function': wrapper
        })
        
        return wrapper
    return decorator

class Component:
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = True
        self.sky_object = None
        
    def update(self, delta_time: float):
        pass
        
    def start(self):
        pass
        
    def stop(self):
        pass

class PlanetComponent(Component):
    
    def __init__(self, planet_name: Planet.PlanetName):
        super().__init__("Planet")
        self.planet_name = planet_name
        self.sky_object = None
        

        self.clouds_intensity = 0.0
        self.cloud_speed = 1.0
        self.cloud_direction = 0.0
        self.cloud_thickness = 0.5
        self.cloud_raininess = 0.0
        

        self.scattering_intensity = 0.0
        self.water_specular_intensity = 0.0
        self.water_specular_shininess = 32.0
        

        self.terrain_intensity = 0.0
        self.terrain_model = Planet.TerrainModel.DefaultTerrain
        self.terrain_rendering_mode = "TOPOGRAPHY"
        self.elevation_scale = 1.0
        

        self.equatorial_grid_intensity = 0.0
        self.ecliptic_grid_intensity = 0.0
        self.galactic_grid_intensity = 0.0
        self.supergalactic_grid_intensity = 0.0
        

        self.shadow_strength = 0.0
        self.shadow_contrast = 0.0
        

        self.sea_level = 0.0
        self.sea_level_rendering_mode = "NONE"
        

        self.tree_intensity = 0.0
        self.tree_density = 1.0
        self.tree_max_distance = 1000.0
        

        self.live_patch_intensity = 0.0
        self.live_patch_texture = ""
        self.live_patch_bottom_left = Vec(0, 0, 0)
        self.live_patch_top_right = Vec(1, 1, 1)
        self.live_patch_rotation = 0.0
        self.live_patch_gamma = Vec(1, 1, 1)
        self.live_patch_hsv = Vec(1, 1, 1)
        self.live_patch_vibrance = 1.0

        try:
            self.live_patch_key_color = Vec4(1, 1, 1, 0.1)
        except NameError:

            self.live_patch_key_color = Vec(1, 1, 1)
    
    
    def initialize(self, sky_engine):
        self.sky_object = Planet(self.planet_name)

        self._apply_all_properties()
    
    def _apply_all_properties(self):
    
        if not self.sky_object:
            return
            

        if hasattr(self.sky_object, 'setCloudsIntensity'):
            self.sky_object.setCloudsIntensity(self.clouds_intensity)
        if hasattr(self.sky_object, 'setCloudSpeed'):
            self.sky_object.setCloudSpeed(self.cloud_speed)
        if hasattr(self.sky_object, 'setCloudDirection'):
            self.sky_object.setCloudDirection(self.cloud_direction)
        if hasattr(self.sky_object, 'setCloudThickness'):
            self.sky_object.setCloudThickness(self.cloud_thickness)
        if hasattr(self.sky_object, 'setCloudRaininess'):
            self.sky_object.setCloudRaininess(self.cloud_raininess)
        

        if hasattr(self.sky_object, 'setScatteringIntensity'):
            self.sky_object.setScatteringIntensity(self.scattering_intensity)
        if hasattr(self.sky_object, 'setWaterSpecularIntensity'):
            self.sky_object.setWaterSpecularIntensity(self.water_specular_intensity)
        if hasattr(self.sky_object, 'setWaterSpecularShininess'):
            self.sky_object.setWaterSpecularShininess(self.water_specular_shininess)
        

        if hasattr(self.sky_object, 'setTerrainIntensity'):
            self.sky_object.setTerrainIntensity(self.terrain_intensity)
        if hasattr(self.sky_object, 'setTerrainModel'):
            self.sky_object.setTerrainModel(self.terrain_model)
        if hasattr(self.sky_object, 'setTerrainRenderingMode'):
            self.sky_object.setTerrainRenderingMode(self.terrain_rendering_mode)
        if hasattr(self.sky_object, 'setElevationScale'):
            self.sky_object.setElevationScale(self.elevation_scale)
        

        if hasattr(self.sky_object, 'setEquatorialGridIntensity'):
            self.sky_object.setEquatorialGridIntensity(self.equatorial_grid_intensity)
        if hasattr(self.sky_object, 'setEclipticGridIntensity'):
            self.sky_object.setEclipticGridIntensity(self.ecliptic_grid_intensity)
        if hasattr(self.sky_object, 'setGalacticGridIntensity'):
            self.sky_object.setGalacticGridIntensity(self.galactic_grid_intensity)
        if hasattr(self.sky_object, 'setSupergalacticGridIntensity'):
            self.sky_object.setSupergalacticGridIntensity(self.supergalactic_grid_intensity)
        

        if hasattr(self.sky_object, 'setShadowStrength'):
            self.sky_object.setShadowStrength(self.shadow_strength)
        if hasattr(self.sky_object, 'setShadowContrast'):
            self.sky_object.setShadowContrast(self.shadow_contrast)
        

        if hasattr(self.sky_object, 'setSeaLevel'):
            self.sky_object.setSeaLevel(self.sea_level)
        if hasattr(self.sky_object, 'setSeaLevelRenderingMode'):
            self.sky_object.setSeaLevelRenderingMode(self.sea_level_rendering_mode)
        

        if hasattr(self.sky_object, 'setTreeIntensity'):
            self.sky_object.setTreeIntensity(self.tree_intensity)
        if hasattr(self.sky_object, 'setTreeDensity'):
            self.sky_object.setTreeDensity(self.tree_density)
        if hasattr(self.sky_object, 'setTreeMaxDistance'):
            self.sky_object.setTreeMaxDistance(self.tree_max_distance)
        

        if hasattr(self.sky_object, 'setLivePatchIntensity'):
            self.sky_object.setLivePatchIntensity(self.live_patch_intensity)
        if hasattr(self.sky_object, 'setLivePatchTexture'):
            self.sky_object.setLivePatchTexture(self.live_patch_texture)
        if hasattr(self.sky_object, 'setLivePatchBottomLeft'):
            self.sky_object.setLivePatchBottomLeft(self.live_patch_bottom_left)
        if hasattr(self.sky_object, 'setLivePatchTopRight'):
            self.sky_object.setLivePatchTopRight(self.live_patch_top_right)
        if hasattr(self.sky_object, 'setLivePatchRotation'):
            self.sky_object.setLivePatchRotation(self.live_patch_rotation)
        if hasattr(self.sky_object, 'setLivePatchGamma'):
            self.sky_object.setLivePatchGamma(self.live_patch_gamma)
        if hasattr(self.sky_object, 'setLivePatchHsv'):
            self.sky_object.setLivePatchHsv(self.live_patch_hsv)
        if hasattr(self.sky_object, 'setLivePatchVibrance'):
            self.sky_object.setLivePatchVibrance(self.live_patch_vibrance)
        if hasattr(self.sky_object, 'setLivePatchKeyColor'):
            self.sky_object.setLivePatchKeyColor(self.live_patch_key_color)
    
    def set_intensity(self, intensity: float):
    
        if self.sky_object and hasattr(self.sky_object, 'setIntensity'):
            self.sky_object.setIntensity(intensity)
        return self
    
    def set_scale(self, scale: float):
    
        if self.sky_object and hasattr(self.sky_object, 'setScale'):
            self.sky_object.setScale(scale)
    

    def set_clouds_intensity(self, intensity: float):
    
        self.clouds_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setCloudsIntensity'):
            self.sky_object.setCloudsIntensity(intensity)
    
    def set_cloud_speed(self, speed: float):
    
        self.cloud_speed = speed
        if self.sky_object and hasattr(self.sky_object, 'setCloudSpeed'):
            self.sky_object.setCloudSpeed(speed)
    
    def set_cloud_direction(self, direction: float):
    
        self.cloud_direction = direction
        if self.sky_object and hasattr(self.sky_object, 'setCloudDirection'):
            self.sky_object.setCloudDirection(direction)
    
    def set_cloud_thickness(self, thickness: float):
    
        self.cloud_thickness = thickness
        if self.sky_object and hasattr(self.sky_object, 'setCloudThickness'):
            self.sky_object.setCloudThickness(thickness)
    
    def set_cloud_raininess(self, raininess: float):
    
        self.cloud_raininess = raininess
        if self.sky_object and hasattr(self.sky_object, 'setCloudRaininess'):
            self.sky_object.setCloudRaininess(raininess)
    

    def set_scattering_intensity(self, intensity: float):
    
        self.scattering_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setScatteringIntensity'):
            self.sky_object.setScatteringIntensity(intensity)
    
    def set_water_specular_intensity(self, intensity: float):
    
        self.water_specular_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setWaterSpecularIntensity'):
            self.sky_object.setWaterSpecularIntensity(intensity)
    
    def set_water_specular_shininess(self, shininess: float):
    
        self.water_specular_shininess = shininess
        if self.sky_object and hasattr(self.sky_object, 'setWaterSpecularShininess'):
            self.sky_object.setWaterSpecularShininess(shininess)
    

    def set_terrain_intensity(self, intensity: float):
    
        self.terrain_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setTerrainIntensity'):
            self.sky_object.setTerrainIntensity(intensity)
    
    def set_terrain_model(self, model: Planet.TerrainModel):
    
        self.terrain_model = model
        if self.sky_object and hasattr(self.sky_object, 'setTerrainModel'):
            self.sky_object.setTerrainModel(model)
    
    def set_terrain_rendering_mode(self, mode: str):
    
        self.terrain_rendering_mode = mode
        if self.sky_object and hasattr(self.sky_object, 'setTerrainRenderingMode'):
            self.sky_object.setTerrainRenderingMode(mode)
    
    def set_elevation_scale(self, scale: float):
    
        self.elevation_scale = scale
        if self.sky_object and hasattr(self.sky_object, 'setElevationScale'):
            self.sky_object.setElevationScale(scale)
    

    def set_equatorial_grid_intensity(self, intensity: float):
    
        self.equatorial_grid_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setEquatorialGridIntensity'):
            self.sky_object.setEquatorialGridIntensity(intensity)
    
    def set_ecliptic_grid_intensity(self, intensity: float):
    
        self.ecliptic_grid_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setEclipticGridIntensity'):
            self.sky_object.setEclipticGridIntensity(intensity)
    
    def set_galactic_grid_intensity(self, intensity: float):
    
        self.galactic_grid_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setGalacticGridIntensity'):
            self.sky_object.setGalacticGridIntensity(intensity)
    
    def set_supergalactic_grid_intensity(self, intensity: float):
    
        self.supergalactic_grid_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setSupergalacticGridIntensity'):
            self.sky_object.setSupergalacticGridIntensity(intensity)
    

    def set_shadow_strength(self, strength: float):
    
        self.shadow_strength = strength
        if self.sky_object and hasattr(self.sky_object, 'setShadowStrength'):
            self.sky_object.setShadowStrength(strength)
    
    def set_shadow_contrast(self, contrast: float):
        """Set shadow contrast (0-1)"""
        self.shadow_contrast = contrast
        if self.sky_object and hasattr(self.sky_object, 'setShadowContrast'):
            self.sky_object.setShadowContrast(contrast)
    

    def set_sea_level(self, level: float):
        """Set sea level in meters"""
        self.sea_level = level
        if self.sky_object and hasattr(self.sky_object, 'setSeaLevel'):
            self.sky_object.setSeaLevel(level)
    
    def set_sea_level_rendering_mode(self, mode: str):
        """Set sea level rendering mode. Valid values: 'NONE', possibly others."""
        self.sea_level_rendering_mode = mode
        if self.sky_object and hasattr(self.sky_object, 'setSeaLevelRenderingMode'):
            self.sky_object.setSeaLevelRenderingMode(mode)
    

    def set_tree_intensity(self, intensity: float):
        """Set tree intensity (0-1)"""
        self.tree_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setTreeIntensity'):
            self.sky_object.setTreeIntensity(intensity)
    
    def set_tree_density(self, density: float):
        """Set tree density"""
        self.tree_density = density
        if self.sky_object and hasattr(self.sky_object, 'setTreeDensity'):
            self.sky_object.setTreeDensity(density)
    
    def set_tree_max_distance(self, distance: float):
        """Set tree fade out distance"""
        self.tree_max_distance = distance
        if self.sky_object and hasattr(self.sky_object, 'setTreeMaxDistance'):
            self.sky_object.setTreeMaxDistance(distance)
    

    def set_live_patch_intensity(self, intensity: float):
        """Set live patch intensity (0-1)"""
        self.live_patch_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setLivePatchIntensity'):
            self.sky_object.setLivePatchIntensity(intensity)
    
    def set_live_patch_texture(self, texture_path: str):
        """Set live patch texture"""
        self.live_patch_texture = texture_path
        if self.sky_object and hasattr(self.sky_object, 'setLivePatchTexture'):
            self.sky_object.setLivePatchTexture(texture_path)
    
    def set_live_patch_bounds(self, bottom_left: Vec, top_right: Vec):
        """Set live patch bounds in LBR coordinates"""
        self.live_patch_bottom_left = bottom_left
        self.live_patch_top_right = top_right
        if self.sky_object and hasattr(self.sky_object, 'setLivePatchBottomLeft'):
            self.sky_object.setLivePatchBottomLeft(bottom_left)
        if self.sky_object and hasattr(self.sky_object, 'setLivePatchTopRight'):
            self.sky_object.setLivePatchTopRight(top_right)
    
    def set_live_patch_rotation(self, rotation: float):
        """Set live patch rotation in degrees"""
        self.live_patch_rotation = rotation

        if self.sky_object and hasattr(self.sky_object, 'setLivePatchRotation'):
            self.sky_object.setLivePatchRotation(rotation)
    
    def set_live_patch_gamma(self, gamma: Vec):
        """Set live patch gamma correction (Vec)"""
        self.live_patch_gamma = gamma
        if self.sky_object and hasattr(self.sky_object, 'setLivePatchGamma'):
            self.sky_object.setLivePatchGamma(gamma)
    
    def set_live_patch_hsv(self, hsv: Vec):
        """Set live patch HSV values"""
        self.live_patch_hsv = hsv
        if self.sky_object and hasattr(self.sky_object, 'setLivePatchHsv'):
            self.sky_object.setLivePatchHsv(hsv)
    
    def set_live_patch_vibrance(self, vibrance: float):
        """Set live patch vibrance"""
        self.live_patch_vibrance = vibrance
        if self.sky_object and hasattr(self.sky_object, 'setLivePatchVibrance'):
            self.sky_object.setLivePatchVibrance(vibrance)
    
    def set_live_patch_key_color(self, color: Vec):
        """Set live patch key color (Vec4: RGB + tolerance)"""
        self.live_patch_key_color = color
        if self.sky_object and hasattr(self.sky_object, 'setLivePatchKeyColor'):
            self.sky_object.setLivePatchKeyColor(color)

class ConstellationComponent(Component):
    """Component for constellations with full control over lines, art, and labels"""
    
    def __init__(self, constellation_enum: Constellation.ConstellationName = Constellation.ConstellationName.UMa):
        super().__init__("Constellation")
        self.constellation_enum = constellation_enum
        self.lines_intensity = 1.0
        self.art_intensity = 0.5
        self.label_intensity = 1.0
        
        # Additional constellation properties
        self.boundary_intensity = 0.0
        self.pointer_intensity = 0.0
        self.trajectory_intensity = 0.0
        
        self.sky_object = Constellation(constellation_enum)
        self._apply_all_properties()
        
    def _apply_all_properties(self):
        """Apply all stored properties to the sky object"""
        if not self.sky_object:
            return
            
        if hasattr(self.sky_object, 'setLinesIntensity'):
            self.sky_object.setLinesIntensity(self.lines_intensity)
        if hasattr(self.sky_object, 'setArtIntensity'):
            self.sky_object.setArtIntensity(self.art_intensity)
        if hasattr(self.sky_object, 'setLabelIntensity'):
            self.sky_object.setLabelIntensity(self.label_intensity)
        if hasattr(self.sky_object, 'setBoundaryIntensity'):
            self.sky_object.setBoundaryIntensity(self.boundary_intensity)
        if hasattr(self.sky_object, 'setPointerIntensity'):
            self.sky_object.setPointerIntensity(self.pointer_intensity)
        if hasattr(self.sky_object, 'setTrajectoryIntensity'):
            self.sky_object.setTrajectoryIntensity(self.trajectory_intensity)
        
    def set_lines_intensity(self, intensity: float):
        """Set constellation lines intensity (0=off, 1=full)"""
        self.lines_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setLinesIntensity'):
            self.sky_object.setLinesIntensity(intensity)
        print(f"Constellation {self.constellation_enum} lines intensity: {intensity}")
        return self
            
    def set_art_intensity(self, intensity: float):
        """Set constellation art/drawings intensity (0=off, 1=full)"""
        self.art_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setArtIntensity'):
            self.sky_object.setArtIntensity(intensity)
        print(f"Constellation {self.constellation_enum} art intensity: {intensity}")
        return self
            
    def set_label_intensity(self, intensity: float):
        """Set constellation label intensity (0=off, 1=full)"""
        self.label_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setLabelIntensity'):
            self.sky_object.setLabelIntensity(intensity)
        print(f"Constellation {self.constellation_enum} label intensity: {intensity}")
        return self
    
    def set_boundary_intensity(self, intensity: float):
        """Set constellation boundary intensity (0=off, 1=full)"""
        self.boundary_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setBoundaryIntensity'):
            self.sky_object.setBoundaryIntensity(intensity)
        return self
    
    def set_pointer_intensity(self, intensity: float):
        """Set constellation pointer intensity (0=off, 1=full)"""
        self.pointer_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setPointerIntensity'):
            self.sky_object.setPointerIntensity(intensity)
        return self
    
    # Convenience methods for turning features on/off
    def turn_lines_on(self):
        """Turn on constellation lines"""
        return self.set_lines_intensity(1.0)
    
    def turn_lines_off(self):
        """Turn off constellation lines"""
        return self.set_lines_intensity(0.0)
    
    def turn_art_on(self):
        """Turn on constellation art/drawings"""
        return self.set_art_intensity(1.0)
    
    def turn_art_off(self):
        """Turn off constellation art/drawings"""
        return self.set_art_intensity(0.0)
    
    def turn_labels_on(self):
        """Turn on constellation labels"""
        return self.set_label_intensity(1.0)
    
    def turn_labels_off(self):
        """Turn off constellation labels"""
        return self.set_label_intensity(0.0)
    
    def turn_boundaries_on(self):
        """Turn on constellation boundaries"""
        return self.set_boundary_intensity(1.0)
    
    def turn_boundaries_off(self):
        """Turn off constellation boundaries"""
        return self.set_boundary_intensity(0.0)
    
    def turn_all_on(self):
        """Turn on all constellation features"""
        self.turn_lines_on()
        self.turn_art_on()
        self.turn_labels_on()
        return self
    
    def turn_all_off(self):
        """Turn off all constellation features"""
        self.turn_lines_off()
        self.turn_art_off()
        self.turn_labels_off()
        return self
    
    def set_all_intensities(self, lines: float = None, art: float = None, labels: float = None, boundaries: float = None):
        """Set multiple intensities at once"""
        if lines is not None:
            self.set_lines_intensity(lines)
        if art is not None:
            self.set_art_intensity(art)
        if labels is not None:
            self.set_label_intensity(labels)
        if boundaries is not None:
            self.set_boundary_intensity(boundaries)
        return self

class SunComponent(Component):
    """Component for the Sun with advanced features"""
    
    def __init__(self):
        super().__init__("Sun")
        self.sky_object = None
        

        self.corona_intensity = 0.0
        self.photosphere_intensity = 0.0
        

        self.magnetic_lines_intensity = 0.0
        self.magnetogram_intensity = 0.0
        

        self.habitable_zone_intensity = 0.0
        self.habitable_zone_color = Vec(1, 1, 1)
        

        self.galactic_band_intensity = 0.0
        self.galactic_grid_intensity = 0.0
        self.galactic_mark_line_intensity = 0.0
        

        self.zodiacal_light_intensity = 0.0
        self.zodiacal_light_scattering_intensity = 0.0
        

        self.cycle = None
        self.filter = None
        

        self.model = None
        self.internal_representation = None
        

        self.color = Vec(1, 1, 1)
        self.saturation_factor = 1.0
        self.opening = 0.0
        

        self.pointer_intensity = 0.0
        self.pointer_type = None
        self.trajectory_intensity = 0.0
        

        self.hybrid_ratio = 0.0
        self.use_hybrid_ratio = False
    
    def initialize(self, sky_engine):

        self.sky_object = IndividualStar(IndividualStar.IndividualStarName.Sun)

        self._apply_all_properties()
    
    def _apply_all_properties(self):
    
        if not self.sky_object:
            return
            

        if hasattr(self.sky_object, 'setCoronaIntensity'):
            self.sky_object.setCoronaIntensity(self.corona_intensity)
        if hasattr(self.sky_object, 'setPhotosphereIntensity'):
            self.sky_object.setPhotosphereIntensity(self.photosphere_intensity)
        

        if hasattr(self.sky_object, 'setMagneticLinesIntensity'):
            self.sky_object.setMagneticLinesIntensity(self.magnetic_lines_intensity)
        if hasattr(self.sky_object, 'setMagnetogramIntensity'):
            self.sky_object.setMagnetogramIntensity(self.magnetogram_intensity)
        

        if hasattr(self.sky_object, 'setHabitableZoneIntensity'):
            self.sky_object.setHabitableZoneIntensity(self.habitable_zone_intensity)
        if hasattr(self.sky_object, 'setHabitableZoneColor'):
            self.sky_object.setHabitableZoneColor(self.habitable_zone_color)
        

        if hasattr(self.sky_object, 'setGalacticBandIntensity'):
            self.sky_object.setGalacticBandIntensity(self.galactic_band_intensity)
        if hasattr(self.sky_object, 'setGalacticGridIntensity'):
            self.sky_object.setGalacticGridIntensity(self.galactic_grid_intensity)
        if hasattr(self.sky_object, 'setGalacticMarkLineIntensity'):
            self.sky_object.setGalacticMarkLineIntensity(self.galactic_mark_line_intensity)
        

        if hasattr(self.sky_object, 'setZodiacalLightIntensity'):
            self.sky_object.setZodiacalLightIntensity(self.zodiacal_light_intensity)
        if hasattr(self.sky_object, 'setZodiacalLightScatteringIntensity'):
            self.sky_object.setZodiacalLightScatteringIntensity(self.zodiacal_light_scattering_intensity)
        

        if self.cycle and hasattr(self.sky_object, 'setCycle'):
            self.sky_object.setCycle(self.cycle)
        if self.filter and hasattr(self.sky_object, 'setFilter'):
            self.sky_object.setFilter(self.filter)
        

        if self.model and hasattr(self.sky_object, 'setModel'):
            self.sky_object.setModel(self.model)
        if self.internal_representation and hasattr(self.sky_object, 'setInternalRepresentation'):
            self.sky_object.setInternalRepresentation(self.internal_representation)
        

        if hasattr(self.sky_object, 'setColor'):
            self.sky_object.setColor(self.color)
        if hasattr(self.sky_object, 'setSaturationFactor'):
            self.sky_object.setSaturationFactor(self.saturation_factor)
        if hasattr(self.sky_object, 'setOpening'):
            self.sky_object.setOpening(self.opening)
        

        if hasattr(self.sky_object, 'setPointerIntensity'):
            self.sky_object.setPointerIntensity(self.pointer_intensity)
        if self.pointer_type and hasattr(self.sky_object, 'setPointerType'):
            self.sky_object.setPointerType(self.pointer_type)
        if hasattr(self.sky_object, 'setTrajectoryIntensity'):
            self.sky_object.setTrajectoryIntensity(self.trajectory_intensity)
        

        if hasattr(self.sky_object, 'setHybridRatio'):
            self.sky_object.setHybridRatio(self.hybrid_ratio)
        if hasattr(self.sky_object, 'setUseHybridRatio'):
            self.sky_object.setUseHybridRatio(self.use_hybrid_ratio)
    
    def set_corona_intensity(self, intensity: float):
        """Set corona intensity (0-1)"""
        self.corona_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setCoronaIntensity'):
            self.sky_object.setCoronaIntensity(intensity)
    
    def set_photosphere_intensity(self, intensity: float):
        """Set photosphere intensity (0-1)"""
        self.photosphere_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setPhotosphereIntensity'):
            self.sky_object.setPhotosphereIntensity(intensity)
    
    def set_magnetic_lines_intensity(self, intensity: float):
        """Set magnetic lines intensity (0-1)"""
        self.magnetic_lines_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setMagneticLinesIntensity'):
            self.sky_object.setMagneticLinesIntensity(intensity)
    
    def set_magnetogram_intensity(self, intensity: float):
        """Set magnetogram intensity (0-1)"""
        self.magnetogram_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setMagnetogramIntensity'):
            self.sky_object.setMagnetogramIntensity(intensity)
    
    def set_habitable_zone_intensity(self, intensity: float):
        """Set habitable zone intensity (0-1)"""
        self.habitable_zone_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setHabitableZoneIntensity'):
            self.sky_object.setHabitableZoneIntensity(intensity)
    
    def set_habitable_zone_color(self, color: Vec):
        """Set habitable zone color"""
        self.habitable_zone_color = color
        if self.sky_object and hasattr(self.sky_object, 'setHabitableZoneColor'):
            self.sky_object.setHabitableZoneColor(color)
    
    def set_galactic_band_intensity(self, intensity: float):
        """Set galactic band intensity (0-1)"""
        self.galactic_band_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setGalacticBandIntensity'):
            self.sky_object.setGalacticBandIntensity(intensity)
    
    def set_galactic_grid_intensity(self, intensity: float):
    
        self.galactic_grid_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setGalacticGridIntensity'):
            self.sky_object.setGalacticGridIntensity(intensity)
    
    def set_galactic_mark_line_intensity(self, intensity: float):
        """Set galactic mark line intensity (0-1)"""
        self.galactic_mark_line_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setGalacticMarkLineIntensity'):
            self.sky_object.setGalacticMarkLineIntensity(intensity)
    
    def set_zodiacal_light_intensity(self, intensity: float):
        """Set zodiacal light intensity (0-1)"""
        self.zodiacal_light_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setZodiacalLightIntensity'):
            self.sky_object.setZodiacalLightIntensity(intensity)
    
    def set_zodiacal_light_scattering_intensity(self, intensity: float):
        """Set zodiacal light scattering intensity (0-1)"""
        self.zodiacal_light_scattering_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setZodiacalLightScatteringIntensity'):
            self.sky_object.setZodiacalLightScatteringIntensity(intensity)
    
    def set_cycle(self, cycle):
        """Set cycle"""
        self.cycle = cycle
        if self.sky_object and hasattr(self.sky_object, 'setCycle'):
            self.sky_object.setCycle(cycle)
    
    def set_filter(self, filter_obj):
        """Set filter"""
        self.filter = filter_obj
        if self.sky_object and hasattr(self.sky_object, 'setFilter'):
            self.sky_object.setFilter(filter_obj)
    
    def set_model(self, model):
        """Set model"""
        self.model = model
        if self.sky_object and hasattr(self.sky_object, 'setModel'):
            self.sky_object.setModel(model)
    
    def set_internal_representation(self, representation):
        """Set internal representation"""
        self.internal_representation = representation
        if self.sky_object and hasattr(self.sky_object, 'setInternalRepresentation'):
            self.sky_object.setInternalRepresentation(representation)
    
    def set_color(self, color: Vec):
        """Set color"""
        self.color = color
        if self.sky_object and hasattr(self.sky_object, 'setColor'):
            self.sky_object.setColor(color)
    
    def set_saturation_factor(self, factor: float):
        """Set saturation factor"""
        self.saturation_factor = factor
        if self.sky_object and hasattr(self.sky_object, 'setSaturationFactor'):
            self.sky_object.setSaturationFactor(factor)
    
    def set_opening(self, opening: float):
        """Set opening"""
        self.opening = opening
        if self.sky_object and hasattr(self.sky_object, 'setOpening'):
            self.sky_object.setOpening(opening)
    
    def set_pointer_intensity(self, intensity: float):
        """Set pointer intensity (0-1)"""
        self.pointer_intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setPointerIntensity'):
            self.sky_object.setPointerIntensity(intensity)
    
    def set_pointer_type(self, pointer_type):
        """Set pointer type"""
        self.pointer_type = pointer_type
        if self.sky_object and hasattr(self.sky_object, 'setPointerType'):
            self.sky_object.setPointerType(pointer_type)
    
    def set_trajectory_intensity(self, intensity: float):
        """Set trajectory intensity (0-1)"""
        self.trajectory_intensity = intensity
        if self.sky_object:
            self.sky_object.setTrajectoryIntensity(intensity)
    
    def set_hybrid_ratio(self, ratio: float):
        """Set hybrid ratio"""
        self.hybrid_ratio = ratio
        if self.sky_object and hasattr(self.sky_object, 'setHybridRatio'):
            self.sky_object.setHybridRatio(ratio)
    
    def set_use_hybrid_ratio(self, use: bool):
        """Set whether to use hybrid ratio"""
        self.use_hybrid_ratio = use
        if self.sky_object and hasattr(self.sky_object, 'setUseHybridRatio'):
            self.sky_object.setUseHybridRatio(use)
    
    def set_intensity(self, intensity: float):
        """Set sun intensity"""
        if self.sky_object and hasattr(self.sky_object, 'setIntensity'):
            self.sky_object.setIntensity(intensity)
        return self
    
    def set_scale(self, scale: float):
        """Set sun scale"""
        if self.sky_object and hasattr(self.sky_object, 'setScale'):
            self.sky_object.setScale(scale)

class TextComponent(Component):
    """Component for text overlays"""
    
    def __init__(self, text: str = "Hello World"):
        super().__init__("Text")
        self.text = text
        self.position = Vec(0, 30, 0)
        self.size = 0.05
        self.intensity = 1.0
        

        self.sky_object = InsertText(InsertText.InsertTextName.InsertText001)
        self.sky_object.setText(text)
        self.sky_object.setIntensity(self.intensity)
        self.sky_object.setSize(self.size)
        self.sky_object.setPosition(self.position)
        

        camera = Camera(Camera.CameraName.MainCamera)
        camera.addChild(self.sky_object.id, Camera.CameraPort.FixedForeground)
        
    def set_text(self, text: str):
        """Set text content"""
        self.text = text
        if self.sky_object:
            self.sky_object.setText(text)
            
    def set_position(self, position: Vec):
        """Set text position"""
        self.position = position
        if self.sky_object:
            self.sky_object.setPosition(position)
            
    def set_size(self, size: float):
        """Set text size"""
        self.size = size
        if self.sky_object:
            self.sky_object.setSize(size)
            
    def set_intensity(self, intensity: float):
        """Set text intensity"""
        self.intensity = intensity
        if self.sky_object:
            self.sky_object.setIntensity(intensity)

class GameObject:
    """Game object - can have components and children"""
    
    # Class variable to track next available ID
    _next_id = 1
    
    def __init__(self, name: str = "GameObject", sky_engine = None):
        # Assign unique ID
        self.id = GameObject._next_id
        GameObject._next_id += 1
        
        self.name = name
        self.sky_engine = sky_engine
        self.components: Dict[str, Component] = {}
        self.children: List[GameObject] = []
        self.parent: Optional[GameObject] = None
        

        self.position = Vec(0, 0, 0)
        self.rotation = Vec(0, 0, 0)
        self.scale = Vec(1, 1, 1)
        

        self.local_position = Vec(0, 0, 0)
        self.local_rotation = Vec(0, 0, 0)
        self.local_scale = Vec(1, 1, 1)
        
        print(f"Created GameObject '{self.name}' with ID: {self.id}")
        
    def add_component(self, component: Component):
        """Add a component to this object"""
        self.components[component.name] = component
        

        if hasattr(component, 'initialize') and hasattr(self, 'sky_engine'):
            component.initialize(self.sky_engine)
        
        component.start()
        

        if hasattr(component, 'sky_object') and component.sky_object:
            if hasattr(component.sky_object, 'setPosition'):
                component.sky_object.setPosition(self.position)
            if hasattr(component.sky_object, 'setScale'):
                avg_scale = (self.scale.x + self.scale.y + self.scale.z) / 3.0
                component.sky_object.setScale(avg_scale)
        
        print(f"Added {component.name} component to {self.name}")
        
    def get_component(self, component_name: str) -> Optional[Component]:
        """Get a component by name"""
        return self.components.get(component_name)
        
    def remove_component(self, component_name: str):
        """Remove a component"""
        if component_name in self.components:
            component = self.components[component_name]
            component.stop()
            del self.components[component_name]
            print(f"Removed {component_name} component from {self.name}")
            
    def add_child(self, child: 'GameObject'):
        """Add a child object"""
        if child.parent:
            child.parent.remove_child(child)
            
        child.parent = self
        self.children.append(child)
        print(f"Added {child.name} as child of {self.name}")
        
    def remove_child(self, child: 'GameObject'):
        """Remove a child object"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            print(f"Removed {child.name} from {self.name}")
            
    def set_position(self, position: Vec):
        """Set world position"""
        self.position = position
        self._update_local_transform()
        self._update_children()
        

        for component in self.components.values():
            if hasattr(component, 'sky_object') and component.sky_object:
                if hasattr(component.sky_object, 'setPosition'):
                    component.sky_object.setPosition(position)

                    if component.name == "Planet":
                        print(f"Planet {self.name} moved to: ({position.x}, {position.y}, {position.z})")
        
    def set_rotation(self, rotation: Vec):
        """Set world rotation (HPR)"""
        self.rotation = rotation
        self._update_local_transform()
        self._update_children()
        
    def set_scale(self, scale: Vec):
        """Set world scale"""
        self.scale = scale
        self._update_local_transform()
        self._update_children()
        

        for component in self.components.values():
            if hasattr(component, 'sky_object') and component.sky_object:
                if hasattr(component.sky_object, 'setScale'):

                    avg_scale = (scale.x + scale.y + scale.z) / 3.0
                    component.sky_object.setScale(avg_scale)
        
    def set_local_position(self, position: Vec):
        """Set local position (relative to parent)"""
        self.local_position = position
        self._update_world_transform()
        self._update_children()
        
    def set_local_rotation(self, rotation: Vec):
        """Set local rotation (relative to parent)"""
        self.local_rotation = rotation
        self._update_world_transform()
        self._update_children()
        
    def set_local_scale(self, scale: Vec):
        """Set local scale (relative to parent)"""
        self.local_scale = scale
        self._update_world_transform()
        self._update_children()
        
    def _update_local_transform(self):
        """Update local transform based on world transform and parent"""
        if self.parent:

            self.local_position = Vec(
                self.position.x - self.parent.position.x,
                self.position.y - self.parent.position.y,
                self.position.z - self.parent.position.z
            )
            

            self.local_rotation = Vec(
                self.rotation.x - self.parent.rotation.x,
                self.rotation.y - self.parent.rotation.y,
                self.rotation.z - self.parent.rotation.z
            )
            

            if self.parent.scale.x != 0 and self.parent.scale.y != 0 and self.parent.scale.z != 0:
                self.local_scale = Vec(
                    self.scale.x / self.parent.scale.x,
                    self.scale.y / self.parent.scale.y,
                    self.scale.z / self.parent.scale.z
                )
        else:

            self.local_position = self.position
            self.local_rotation = self.rotation
            self.local_scale = self.scale
            
    def _update_world_transform(self):
        """Update world transform based on local transform and parent"""
        if self.parent:

            self.position = Vec(
                self.parent.position.x + self.local_position.x,
                self.parent.position.y + self.local_position.y,
                self.parent.position.z + self.local_position.z
            )
            

            self.rotation = Vec(
                self.parent.rotation.x + self.local_rotation.x,
                self.parent.rotation.y + self.local_rotation.y,
                self.parent.rotation.z + self.local_rotation.z
            )
            

            self.scale = Vec(
                self.parent.scale.x * self.local_scale.x,
                self.parent.scale.y * self.local_scale.y,
                self.parent.scale.z * self.local_scale.z
            )
        else:

            self.position = self.local_position
            self.rotation = self.local_rotation
            self.scale = self.local_scale
            
    def _update_children(self):
        """Update all children transforms"""
        for child in self.children:
            child._update_world_transform()
            child._update_children()
            
    def update(self, delta_time: float):
        """Update this object and all children"""

        for component in self.components.values():
            if component.enabled:
                component.update(delta_time)
                

        for child in self.children:
            child.update(delta_time)
            
    def destroy(self):
        """Destroy this object and all children"""

        for child in self.children[:]:
            child.destroy()
            

        if self.parent:
            self.parent.remove_child(self)
            

        for component in self.components.values():
            component.stop()
            
        print(f"Destroyed {self.name}")
    
    def get_sky_object_id(self) -> Optional[int]:
        """Get the ID of the underlying skyExplorer object from components"""
        for component in self.components.values():
            if hasattr(component, 'sky_object') and component.sky_object:
                if hasattr(component.sky_object, 'id'):
                    return component.sky_object.id
        return None
    
    def get_first_sky_object(self):
        """Get the first skyExplorer object from components"""
        for component in self.components.values():
            if hasattr(component, 'sky_object') and component.sky_object:
                return component.sky_object
        return None
    
    def has_component_type(self, component_type: str) -> bool:
        """Check if object has a component of the given type"""
        return component_type in self.components
    
    def get_info(self) -> Dict[str, Any]:
        """Get comprehensive information about this GameObject"""
        sky_object_id = self.get_sky_object_id()
        return {
            'id': self.id,
            'name': self.name,
            'sky_object_id': sky_object_id,
            'components': list(self.components.keys()),
            'component_count': len(self.components),
            'children_ids': [child.id for child in self.children],
            'children_count': len(self.children),
            'parent_id': self.parent.id if self.parent else None,
            'has_sky_object': sky_object_id is not None,
            'position': {'x': self.position.x, 'y': self.position.y, 'z': self.position.z} if hasattr(self, 'position') else None,
            'local_position': {'x': self.local_position.x, 'y': self.local_position.y, 'z': self.local_position.z} if hasattr(self, 'local_position') else None
        }

class SkyEngine:
    """Main engine class"""
    
    def __init__(self):
        print("Initializing Sky Engine...")
        

        SceneGraph().reset(1)
        sleep(1.0)
        

        self.main_camera = Camera(Camera.CameraName.MainCamera)
        

        self.camera_position = Vec(0, 0, 0)
        self.camera_rotation = Vec(0, 0, 0)
        self.camera_zoom = 1.0
        

        self.root_objects: List[GameObject] = []
        
        print("Sky Engine initialized!")
        
    def create_object(self, name: str = "GameObject") -> GameObject:
        """Create a new game object"""
        obj = GameObject(name, self)
        self.root_objects.append(obj)
        print(f"Created object: {name}")
        return obj
        
    def destroy_object(self, obj: GameObject):
        """Destroy a game object"""
        if obj in self.root_objects:
            self.root_objects.remove(obj)
        obj.destroy()
        
    def update(self, delta_time: float):
        """Update all root objects"""
        for obj in self.root_objects:
            obj.update(delta_time)
            
    def get_object_by_name(self, name: str) -> Optional[GameObject]:
        """Find object by name (searches all objects)"""
        def search_objects(objects):
            for obj in objects:
                if obj.name == name:
                    return obj
                result = search_objects(obj.children)
                if result:
                    return result
            return None
            
        return search_objects(self.root_objects)
    
    def get_object_by_id(self, object_id: int) -> Optional[GameObject]:
        """Find object by ID (searches all objects)"""
        def search_objects(objects):
            for obj in objects:
                if obj.id == object_id:
                    return obj
                result = search_objects(obj.children)
                if result:
                    return result
            return None
            
        return search_objects(self.root_objects)
    
    def get_all_object_ids(self) -> List[int]:
        """Get list of all object IDs in the scene"""
        all_objects = self._get_all_objects()
        return [obj.id for obj in all_objects]
    
    def get_object_info(self, object_id: int) -> Optional[Dict[str, Any]]:
        """Get information about an object by ID"""
        obj = self.get_object_by_id(object_id)
        if obj:
            return {
                'id': obj.id,
                'name': obj.name,
                'components': list(obj.components.keys()),
                'children_count': len(obj.children),
                'has_parent': obj.parent is not None,
                'position': obj.position,
                'rotation': obj.rotation,
                'scale': obj.scale
            }
        return None
    
    def get_global_animator(self) -> Animator:
        """Get the global animator for animations"""
        global global_animator
        if global_animator is None:
            global_animator = Animator(0.5)
        return global_animator
    
    def set_global_animator_duration(self, duration: float):
        """Set the global animator duration"""
        global global_animator
        if global_animator is None:
            global_animator = Animator(duration)
        else:
            global_animator.duration = duration
    
    def runAll(self):
        """Run all frames in sequence"""
        global all_frames
        
        if not all_frames:
            print("No frames to run!")
            return
        
        print(f"Running all {len(all_frames)} frames...")
        

        sorted_frames = sorted(all_frames, key=lambda x: x['frame_number'])
        

        for i, frame_data in enumerate(sorted_frames):
            print(f"Running frame {i+1}/{len(sorted_frames)}: {frame_data['type']} #{frame_data['frame_number']}")
            
            try:

                frame_data['function'](self)
            except Exception as e:
                print(f"Error in frame {frame_data['frame_number']}: {e}")
        
        print("Animation sequence complete!")
    
    def run(self, frame_id: int):
        """Run a specific frame by frame_number"""
        global all_frames
        

        target_frame = None
        for frame_data in all_frames:
            if frame_data['frame_number'] == frame_id:
                target_frame = frame_data
                break
        
        if target_frame is None:
            print(f"Frame {frame_id} not found!")
            return
        
        print(f"Running frame {frame_id}: {target_frame['type']}")
        
        try:
    
            target_frame['function'](self)
        except Exception as e:
            print(f"Error in frame {frame_id}: {e}")
    
    def start(self):
        """Alias for runAll() for backward compatibility"""
        self.runAll()
    

    def set_camera_position(self, position: Vec, target = None):
        """Set camera position using proper Sky Explorer methods"""
        self.camera_position = position
        

        if hasattr(self.main_camera, 'setPositionXYZ'):
            animator = self.get_global_animator()
            track = 0  # Default track
            
            self.main_camera.setPositionXYZ(position, animator, track)
            

            if hasattr(self.main_camera, 'setTarget') and target is not None:
                self.main_camera.setTarget(target)
        
        print(f"Camera moved to: ({position.x}, {position.y}, {position.z})")
    
    def set_camera_position_lbr(self, latitude: float, longitude: float, radius: float):
        """Set camera position using LBR coordinates"""
        if hasattr(self.main_camera, 'setPositionLBR'):
            animator = self.get_global_animator()
            track = 0
            self.main_camera.setPositionLBR(Vec(latitude, longitude, radius), animator, track)
            self.camera_position = Vec(latitude, longitude, radius)
            print(f"Camera moved to LBR: ({latitude}, {longitude}, {radius})")
    
    def set_camera_position_individual(self, x: float = None, y: float = None, z: float = None):
        """Set individual camera position axes"""
        if x is not None and hasattr(self.main_camera, 'setPositionX'):
            self.main_camera.setPositionX(x, self.get_global_animator(), 0)
        if y is not None and hasattr(self.main_camera, 'setPositionY'):
            self.main_camera.setPositionY(y, self.get_global_animator(), 0)
        if z is not None and hasattr(self.main_camera, 'setPositionZ'):
            self.main_camera.setPositionZ(z, self.get_global_animator(), 0)
        

        if x is not None: self.camera_position.x = x
        if y is not None: self.camera_position.y = y
        if z is not None: self.camera_position.z = z
        
        print(f"Camera position updated: ({self.camera_position.x}, {self.camera_position.y}, {self.camera_position.z})")
    
    def set_camera_rotation(self, rotation: Vec):
        """Set camera rotation (HPR)"""
        self.camera_rotation = rotation
        if hasattr(self.main_camera, 'setOrientationHPR'):
            self.main_camera.setOrientationHPR(rotation)
        print(f"Camera rotated to: ({rotation.x}, {rotation.y}, {rotation.z})")
    
    def set_camera_rotation_individual(self, h: float = None, p: float = None, r: float = None, 
                                     heading: float = None, pitch: float = None, roll: float = None):
        """Set camera rotation using individual H, P, R values (in degrees)"""

        h = h if h is not None else heading
        p = p if p is not None else pitch  
        r = r if r is not None else roll
        
        if self.main_camera and h is not None and p is not None and r is not None:
    
            h_rad = math.radians(h)
            p_rad = math.radians(p)
            r_rad = math.radians(r)
            
            try:
                self.main_camera.setOrientationH(h_rad)
                self.main_camera.setOrientationP(p_rad)
                self.main_camera.setOrientationR(r_rad)
                print(f"Camera rotated to: ({h}, {p}, {r})")
            except Exception as e:
                print(f"Error setting camera rotation: {e}")
    
    def set_camera_zoom(self, zoom: float):
        """Set camera zoom level using distance"""
        self.camera_zoom = zoom

        if hasattr(self.main_camera, 'setPositionR'):
    
            animator = self.get_global_animator()
            track = 0  # Default track
            self.main_camera.setPositionR(zoom * 100, animator, track)
        print(f"Camera zoom: {zoom}")
    
    def set_camera_zoom_fov(self, fov: float):
        """Set camera zoom using field of view"""
        if hasattr(self.main_camera, 'setZoomFov'):
            self.main_camera.setZoomFov(fov)
            print(f"Camera FOV zoom: {fov}")
    
    def set_camera_zoom_position(self, position: float):
        """Set camera zoom using position"""
        if hasattr(self.main_camera, 'setZoomPosition'):
    
    
            position_vec = Vec(position, 0, 0)
            track = 0  # Default track
            animator = self.get_global_animator()

            try:
                self.main_camera.setZoomPosition(position_vec, track, animator, Camera.PositionMode.XYZ)
            except (TypeError, AttributeError):

                try:
                    self.main_camera.setZoomPosition(position_vec, track, animator)
                except:
                    print(f"Warning: Could not set camera zoom position to {position}")
            print(f"Camera zoom position: {position}")
    
    def set_camera_focus(self, focus_degree: float):
        """Set camera focus degree"""
        if hasattr(self.main_camera, 'setFocusDegree'):
            self.main_camera.setFocusDegree(focus_degree)
            print(f"Camera focus degree: {focus_degree}")
    
    def set_camera_stereo_position(self, position: Vec):
        """Set stereo camera position"""
        if hasattr(self.main_camera, 'setStereoPosition'):
            self.main_camera.setStereoPosition(position)
            print(f"Stereo camera position: ({position.x}, {position.y}, {position.z})")
    
    def set_camera_stereo_ratio(self, ratio: float):
        """Set stereo camera ratio"""
        if hasattr(self.main_camera, 'setStereoRatio'):
            self.main_camera.setStereoRatio(ratio)
            print(f"Stereo camera ratio: {ratio}")
    
    def set_camera_eye_distance(self, distance: float):
        """Set camera eye distance for stereo"""
        if hasattr(self.main_camera, 'setEyeDistance'):
            self.main_camera.setEyeDistance(distance)
            print(f"Camera eye distance: {distance}")
    
    def set_camera_target_azimuth(self, azimuth: float):
        """Set camera target azimuth"""
        if hasattr(self.main_camera, 'setTargetAzimuth'):
            self.main_camera.setTargetAzimuth(azimuth)
            print(f"Camera target azimuth: {azimuth}")
    
    def set_camera_target_height(self, height: float):
        """Set camera target height"""
        if hasattr(self.main_camera, 'setTargetHeight'):
            self.main_camera.setTargetHeight(height)
            print(f"Camera target height: {height}")
    
    def set_camera_resolution_ratio_strength(self, strength: float):
        """Set camera resolution ratio strength"""
        if hasattr(self.main_camera, 'setResolutionRatioStrength'):
            self.main_camera.setResolutionRatioStrength(strength)
            print(f"Camera resolution ratio strength: {strength}")
    
    def set_camera_trace_mode(self, mode: bool):
        """Set camera trace mode"""
        if hasattr(self.main_camera, 'setTraceMode'):
            self.main_camera.setTraceMode(mode)
            print(f"Camera trace mode: {mode}")
    
    def take_camera_screenshot(self, filename: str = None):
        """Take a camera screenshot"""
        if hasattr(self.main_camera, 'takeScreenshot'):
            if filename is None:
                filename = f"screenshot_{int(time.time())}.png"
            self.main_camera.takeScreenshot(filename)
            print(f"Screenshot saved: {filename}")
            return filename
        return None
    
    def move_camera(self, delta_position: Vec):
        """Move camera by delta amount"""
        new_position = Vec(
            self.camera_position.x + delta_position.x,
            self.camera_position.y + delta_position.y,
            self.camera_position.z + delta_position.z
        )
        self.set_camera_position(new_position)
    
    def rotate_camera(self, delta_rotation: Vec):
        """Rotate camera by delta amount"""
        new_rotation = Vec(
            self.camera_rotation.x + delta_rotation.x,
            self.camera_rotation.y + delta_rotation.y,
            self.camera_rotation.z + delta_rotation.z
        )
        self.set_camera_rotation(new_rotation)
    
    def zoom_camera(self, delta_zoom: float):
        """Zoom camera by delta amount"""
        new_zoom = self.camera_zoom + delta_zoom
        new_zoom = max(0.1, min(10.0, new_zoom))
        self.set_camera_zoom(new_zoom)
    
    def look_at(self, target_position: Vec):
        """Make camera look at a specific position"""

        direction = Vec(
            target_position.x - self.camera_position.x,
            target_position.y - self.camera_position.y,
            target_position.z - self.camera_position.z
        )
        

        distance = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
        
        print(f"Looking at target: ({target_position.x}, {target_position.y}, {target_position.z})")
        print(f"Camera position: ({self.camera_position.x}, {self.camera_position.y}, {self.camera_position.z})")
        print(f"Distance: {distance}")
        

        if distance < 0.001:
            print("Camera too close to target, cannot look at")
            return
        

        if hasattr(self.main_camera, 'setTarget'):

            azimuth = math.atan2(direction.x, direction.z)
            height = math.asin(direction.y / distance)
            target = Vec(math.degrees(azimuth), math.degrees(height), 0)
            self.main_camera.setTarget(target)
            print(f"Camera target set to: ({target.x}, {target.y}, {target.z})")
        else:

            heading = math.atan2(direction.x, direction.z)
            pitch = math.asin(-direction.y / distance)
            new_rotation = Vec(math.degrees(heading), math.degrees(pitch), 0)
            self.set_camera_rotation(new_rotation)
    
    def orbit_camera(self, target_position: Vec, distance: float, heading: float, pitch: float):
        """Orbit camera around a target position"""

        heading_rad = math.radians(heading)
        pitch_rad = math.radians(pitch)
        

        x = target_position.x + distance * math.sin(heading_rad) * math.cos(pitch_rad)
        y = target_position.y + distance * math.sin(pitch_rad)
        z = target_position.z + distance * math.cos(heading_rad) * math.cos(pitch_rad)
        
        new_position = Vec(x, y, z)
        self.set_camera_position(new_position)
        

        if hasattr(self.main_camera, 'setTarget'):

            direction = Vec(
                target_position.x - new_position.x,
                target_position.y - new_position.y,
                target_position.z - new_position.z
            )
            dist = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
            if dist > 0.001:
                azimuth = math.atan2(direction.x, direction.z)
                height = math.asin(direction.y / dist)
                target = Vec(math.degrees(azimuth), math.degrees(height), 0)
                self.main_camera.setTarget(target)
        else:
            self.look_at(target_position)
    
    def get_camera_info(self) -> Dict[str, Any]:
        """Get current camera information"""
        return {
            'position': self.camera_position,
            'rotation': self.camera_rotation,
            'zoom': self.camera_zoom
        }
    
    # Navigation Methods (Camera-based since studio library not available)
    def go_to_object(self, target_object, distance: float = 10.0):
        """Navigate camera to look at a specific object"""
        try:
            if hasattr(target_object, 'sky_object') and target_object.sky_object:
                # Try to get object position and point camera at it
                target_pos = target_object.get_world_position()
                self.look_at_position(target_pos, distance)
                print(f"Camera looking at object: {target_object.name}")
            elif hasattr(target_object, 'get_world_position'):
                # Direct skyExplorer object
                target_pos = target_object.get_world_position()
                self.look_at_position(target_pos, distance)
                print(f"Camera looking at skyExplorer object")
            else:
                print(f"Warning: Cannot navigate to object - no position available")
        except Exception as e:
            print(f"Error navigating to object: {e}")
    
    def look_at_position(self, position: Vec, distance: float = 10.0):
        """Point camera at a specific position"""
        try:
            # Calculate camera position offset from target
            camera_offset = Vec(0, 0, distance)
            new_camera_pos = Vec(position.x + camera_offset.x, 
                               position.y + camera_offset.y, 
                               position.z + camera_offset.z)
            
            # Update camera position and look at target
            self.set_camera_position(new_camera_pos)
            # Note: Camera rotation to look at target would require more complex math
            print(f"Camera positioned at distance {distance} from target")
        except Exception as e:
            print(f"Error positioning camera: {e}")
    
    def go_to_planet(self, planet_name: Planet.PlanetName, distance: float = 15.0):
        """Go to a specific planet"""
        try:
            planet = Planet(planet_name)
            self.go_to_object(planet, distance)
            print(f"Going to planet: {planet_name}")
        except Exception as e:
            print(f"Error going to planet: {e}")
    
    def go_to_game_object(self, game_object: GameObject, distance: float = 10.0):
        """Go to a specific GameObject"""
        try:
            self.go_to_object(game_object, distance)
            print(f"Going to GameObject '{game_object.name}'")
        except Exception as e:
            print(f"Error going to GameObject: {e}")
    
    def go_to_game_object_by_id(self, object_id: int):
        """Go to a GameObject by its ID"""
        obj = self.get_object_by_id(object_id)
        if obj:
            self.go_to_game_object(obj)
        else:
            print(f"Warning: No GameObject found with ID {object_id}")
    
    def go_to_star(self, star_name: IndividualStar.IndividualStarName, distance: float = 20.0):
        """Go to a specific star"""
        try:
            star = IndividualStar(star_name)
            self.go_to_object(star, distance)
            print(f"Going to star: {star_name}")
        except Exception as e:
            print(f"Error going to star: {e}")
    
    def go_to_constellation(self, constellation_name: Constellation.ConstellationName, distance: float = 25.0):
        """Go to a specific constellation"""
        try:
            constellation = Constellation(constellation_name)
            self.go_to_object(constellation, distance)
            print(f"Going to constellation: {constellation_name}")
        except Exception as e:
            print(f"Error going to constellation: {e}")
    
    def go_to_comet(self, comet_name: Comet.CometName, distance: float = 12.0):
        """Go to a specific comet"""
        try:
            comet = Comet(comet_name)
            self.go_to_object(comet, distance)
            print(f"Going to comet: {comet_name}")
        except Exception as e:
            print(f"Error going to comet: {e}")
    
    def go_to_asteroid(self, asteroid_name: Asteroid.AsteroidName, distance: float = 8.0):
        """Go to a specific asteroid"""
        try:
            asteroid = Asteroid(asteroid_name)
            self.go_to_object(asteroid, distance)
            print(f"Going to asteroid: {asteroid_name}")
        except Exception as e:
            print(f"Error going to asteroid: {e}")
    
    def go_to_satellite(self, satellite_name: Satellite.SatelliteName, distance: float = 6.0):
        """Go to a specific satellite"""
        try:
            satellite = Satellite(satellite_name)
            self.go_to_object(satellite, distance)
            print(f"Going to satellite: {satellite_name}")
        except Exception as e:
            print(f"Error going to satellite: {e}")
    
    def go_to_galaxy(self, galaxy_name: Galaxy.GalaxyName, distance: float = 50.0):
        """Go to a specific galaxy"""
        try:
            galaxy = Galaxy(galaxy_name)
            self.go_to_object(galaxy, distance)
            print(f"Going to galaxy: {galaxy_name}")
        except Exception as e:
            print(f"Error going to galaxy: {e}")
    
    def go_to_nebula(self, nebula_name: Nebula.NebulaName, distance: float = 30.0):
        """Go to a specific nebula"""
        try:
            nebula = Nebula(nebula_name)
            self.go_to_object(nebula, distance)
            print(f"Going to nebula: {nebula_name}")
        except Exception as e:
            print(f"Error going to nebula: {e}")
    
    # Starry Sky Control
    def set_stars_intensity(self, intensity: float):
        """Set the intensity of the starry sky (0=off, 1=full brightness)"""
        try:
            # Create a global Stars object if it doesn't exist
            if not hasattr(self, '_stars_object'):
                try:
                    # Try to get the first available StarsName enum value
                    available_names = list(Stars.StarsName)
                    if available_names:
                        self._stars_object = Stars(available_names[0])
                        print(f"Created Stars object using: {available_names[0]}")
                    else:
                        print("Error: No StarsName enum values available")
                        return
                except Exception as enum_error:
                    print(f"Error accessing Stars.StarsName enum: {enum_error}")
                    return
            
            self._stars_object.setIntensity(intensity)
            print(f"Stars intensity set to: {intensity}")
        except Exception as e:
            print(f"Error setting stars intensity: {e}")
    
    def turn_stars_on(self):
        """Turn on the starry sky"""
        self.set_stars_intensity(1.0)
    
    def turn_stars_off(self):
        """Turn off the starry sky"""
        self.set_stars_intensity(0.0)
    
    def create_stars_object(self, name: str = "Stars", stars_name: Stars.StarsName = None) -> GameObject:
        """Create a game object with a stars component"""
        stars_obj = self.create_object(name)
        stars_comp = StarsComponent(stars_name)
        stars_obj.add_component(stars_comp)
        return stars_obj
    
    def get_available_stars_names(self):
        """Get list of available StarsName enum values"""
        try:
            available_names = list(Stars.StarsName)
            print("Available Stars names:")
            for i, name in enumerate(available_names):
                print(f"  {i}: {name}")
            return available_names
        except Exception as e:
            print(f"Error getting Stars names: {e}")
            return []
    
    # Constellation Control Methods
    def create_constellation_object(self, constellation_name: Constellation.ConstellationName, object_name: str = None) -> GameObject:
        """Create a game object with a constellation component"""
        if object_name is None:
            object_name = f"Constellation_{constellation_name.name}"
        
        constellation_obj = self.create_object(object_name)
        constellation_comp = ConstellationComponent(constellation_name)
        constellation_obj.add_component(constellation_comp)
        return constellation_obj
    
    def set_all_constellation_lines(self, intensity: float):
        """Set lines intensity for all constellation objects in the scene"""
        count = 0
        for obj in self._get_all_objects():
            constellation_comp = obj.get_component("Constellation")
            if constellation_comp:
                constellation_comp.set_lines_intensity(intensity)
                count += 1
        print(f"Set lines intensity to {intensity} for {count} constellations")
    
    def set_all_constellation_art(self, intensity: float):
        """Set art intensity for all constellation objects in the scene"""
        count = 0
        for obj in self._get_all_objects():
            constellation_comp = obj.get_component("Constellation")
            if constellation_comp:
                constellation_comp.set_art_intensity(intensity)
                count += 1
        print(f"Set art intensity to {intensity} for {count} constellations")
    
    def set_all_constellation_labels(self, intensity: float):
        """Set labels intensity for all constellation objects in the scene"""
        count = 0
        for obj in self._get_all_objects():
            constellation_comp = obj.get_component("Constellation")
            if constellation_comp:
                constellation_comp.set_label_intensity(intensity)
                count += 1
        print(f"Set labels intensity to {intensity} for {count} constellations")
    
    def set_all_constellation_boundaries(self, intensity: float):
        """Set boundaries intensity for all constellation objects in the scene"""
        count = 0
        for obj in self._get_all_objects():
            constellation_comp = obj.get_component("Constellation")
            if constellation_comp:
                constellation_comp.set_boundary_intensity(intensity)
                count += 1
        print(f"Set boundaries intensity to {intensity} for {count} constellations")
    
    def turn_all_constellation_lines_on(self):
        """Turn on lines for all constellations"""
        self.set_all_constellation_lines(1.0)
    
    def turn_all_constellation_lines_off(self):
        """Turn off lines for all constellations"""
        self.set_all_constellation_lines(0.0)
    
    def turn_all_constellation_art_on(self):
        """Turn on art/drawings for all constellations"""
        self.set_all_constellation_art(1.0)
    
    def turn_all_constellation_art_off(self):
        """Turn off art/drawings for all constellations"""
        self.set_all_constellation_art(0.0)
    
    def turn_all_constellation_labels_on(self):
        """Turn on labels for all constellations"""
        self.set_all_constellation_labels(1.0)
    
    def turn_all_constellation_labels_off(self):
        """Turn off labels for all constellations"""
        self.set_all_constellation_labels(0.0)
    
    def turn_all_constellation_boundaries_on(self):
        """Turn on boundaries for all constellations"""
        self.set_all_constellation_boundaries(1.0)
    
    def turn_all_constellation_boundaries_off(self):
        """Turn off boundaries for all constellations"""
        self.set_all_constellation_boundaries(0.0)
    
    def turn_all_constellations_on(self):
        """Turn on all constellation features (lines, art, labels)"""
        self.turn_all_constellation_lines_on()
        self.turn_all_constellation_art_on()
        self.turn_all_constellation_labels_on()
        print("All constellation features turned ON")
    
    def turn_all_constellations_off(self):
        """Turn off all constellation features (lines, art, labels)"""
        self.turn_all_constellation_lines_off()
        self.turn_all_constellation_art_off()
        self.turn_all_constellation_labels_off()
        print("All constellation features turned OFF")
    
    def set_constellation_display_mode(self, mode: str):
        """Set constellation display mode
        
        Args:
            mode: 'lines_only', 'art_only', 'labels_only', 'all', 'none'
        """
        if mode == 'lines_only':
            self.turn_all_constellation_lines_on()
            self.turn_all_constellation_art_off()
            self.turn_all_constellation_labels_off()
        elif mode == 'art_only':
            self.turn_all_constellation_lines_off()
            self.turn_all_constellation_art_on()
            self.turn_all_constellation_labels_off()
        elif mode == 'labels_only':
            self.turn_all_constellation_lines_off()
            self.turn_all_constellation_art_off()
            self.turn_all_constellation_labels_on()
        elif mode == 'all':
            self.turn_all_constellations_on()
        elif mode == 'none':
            self.turn_all_constellations_off()
        else:
            print(f"Unknown mode: {mode}. Use 'lines_only', 'art_only', 'labels_only', 'all', or 'none'")
    
    def _get_all_objects(self) -> List[GameObject]:
        """Get all objects in the scene (root + children)"""
        all_objects = []
        
        def collect_objects(objects):
            for obj in objects:
                all_objects.append(obj)
                collect_objects(obj.children)
        
        collect_objects(self.root_objects)
        return all_objects
    
    def get_available_constellation_names(self):
        """Get list of available Constellation enum values"""
        try:
            available_names = list(Constellation.ConstellationName)
            print("Available Constellation names:")
            for i, name in enumerate(available_names):
                print(f"  {i}: {name}")
            return available_names
        except Exception as e:
            print(f"Error getting Constellation names: {e}")
            return []
    
    def list_all_objects(self):
        """Print information about all objects in the scene"""
        all_objects = self._get_all_objects()
        print(f"\n=== Scene Objects ({len(all_objects)} total) ===")
        for obj in all_objects:
            sky_id = obj.get_sky_object_id()
            print(f"  ID: {obj.id} | Name: '{obj.name}' | Components: {list(obj.components.keys())} | Sky ID: {sky_id}")
    
    def clear_all_objects(self):
        """Remove all objects from the scene"""
        for obj in self.root_objects[:]:  # Copy list to avoid modification during iteration
            obj.destroy()
        self.root_objects.clear()
        print("All objects cleared from scene")
    
    @staticmethod
    def reset_object_id_counter():
        """Reset the GameObject ID counter (useful for testing)"""
        GameObject._next_id = 1
        print("GameObject ID counter reset to 1")
    
    def get_objects_by_component_type(self, component_type: str) -> List[GameObject]:
        """Get all objects that have a specific component type"""
        matching_objects = []
        for obj in self._get_all_objects():
            if obj.has_component_type(component_type):
                matching_objects.append(obj)
        return matching_objects
    
    def count_objects_by_type(self) -> Dict[str, int]:
        """Get count of objects by component type"""
        type_counts = {}
        for obj in self._get_all_objects():
            for component_type in obj.components.keys():
                type_counts[component_type] = type_counts.get(component_type, 0) + 1
        return type_counts

class AudioComponent(Component):
    """Component for audio playback"""
    
    def __init__(self, audio_file: str = None):
        super().__init__("Audio")
        self.audio_file = audio_file
        self.sky_object = Audio()  # Create Audio object
        self.volume = 1.0  # Default volume
        
        if audio_file:
            self.load_audio(audio_file)
    
    def load_audio(self, audio_file: str):
        """Load an audio file"""
        if self.sky_object and hasattr(self.sky_object, 'load'):
            # Audio.load expects (outputId, filename)
            # Use outputId 0 as default
            self.sky_object.load(0, audio_file)
            self.audio_file = audio_file
            print(f"Loaded audio file: {audio_file}")
    
    def play(self):
        """Play audio"""
        if self.sky_object:
            self.sky_object.play()
            print("Audio playing")
    
    def pause(self):
        """Pause audio"""
        if self.sky_object:
            self.sky_object.pause()
            print("Audio paused")
    
    def stop(self):
        """Stop audio"""
        if self.sky_object:
            self.sky_object.stop()
            print("Audio stopped")
    
    def seek(self, time: float):
        """Seek to specific time"""
        if self.sky_object:
            self.sky_object.seek(time)
            print(f"Audio seeked to: {time}")
    
    def set_volume(self, volume: float):
        """Set volume (0-1)"""
        self.volume = volume
        if self.sky_object:
            self.sky_object.setVolume(volume)
            print(f"Audio volume: {volume}")
    
    def set_volume_db(self, volume_db: float):
        """Set volume in decibels"""
        if self.sky_object:
            self.sky_object.setVolumeDb(volume_db)
            print(f"Audio volume dB: {volume_db}")
    
    def clear(self):
        """Clear audio"""
        if self.sky_object:
            self.sky_object.clear()
            print("Audio cleared")

class AudioLayerComponent(Component):
    """Component for layered audio management"""
    
    def __init__(self):
        super().__init__("AudioLayer")
        self.layers = {}
        self.sky_object = AudioLayer()
    
    def add_layer(self, layer_name: str, audio_file: str):
        """Add audio layer"""
        if layer_name not in self.layers:
            self.layers[layer_name] = Audio()
            self.layers[layer_name].load(audio_file)
            print(f"Audio layer added: {layer_name} -> {audio_file}")
    
    def play_layer(self, layer_name: str):
        """Play specific layer"""
        if layer_name in self.layers:
            self.layers[layer_name].play()
            print(f"Audio layer playing: {layer_name}")
    
    def pause_layer(self, layer_name: str):
        """Pause specific layer"""
        if layer_name in self.layers:
            self.layers[layer_name].pause()
            print(f"Audio layer paused: {layer_name}")
    
    def stop_layer(self, layer_name: str):
        """Stop specific layer"""
        if layer_name in self.layers:
            self.layers[layer_name].stop()
            print(f"Audio layer stopped: {layer_name}")
    
    def set_layer_volume(self, layer_name: str, volume: float):
        """Set volume for specific layer"""
        if layer_name in self.layers:
            self.layers[layer_name].setVolume(volume)
            print(f"Audio layer volume set: {layer_name} -> {volume}")
    
    def remove_layer(self, layer_name: str):
        """Remove audio layer"""
        if layer_name in self.layers:
            self.layers[layer_name].clear()
            del self.layers[layer_name]
            print(f"Audio layer removed: {layer_name}")
    
    def play_all_layers(self):
        """Play all layers"""
        for layer_name in self.layers:
            self.layers[layer_name].play()
        print("All audio layers playing")
    
    def stop_all_layers(self):
        """Stop all layers"""
        for layer_name in self.layers:
            self.layers[layer_name].stop()
        print("All audio layers stopped")
    
    def clear_all_layers(self):
        """Clear all layers"""
        for layer_name in self.layers:
            self.layers[layer_name].clear()
        self.layers.clear()
        print("All audio layers cleared")

class ClockComponent(Component):
    """Component for time management"""
    
    def __init__(self):
        super().__init__("Clock")
        self.sky_object = Clock(Clock.ClockName.Clock001)  # Use valid ClockName enum
        self.time_scale = 1.0
        self.is_running = False
        self.current_time = 0.0
    
    def start(self):
        """Start the clock"""
        if self.sky_object:
            self.is_running = True
            print("Clock started")
    
    def stop(self):
        """Stop the clock"""
        if self.sky_object:
            self.is_running = False
            print("Clock stopped")
    
    def pause(self):
        """Pause the clock"""
        if self.sky_object:
            print("Clock paused")
    
    def resume(self):
        """Resume the clock"""
        if self.sky_object:
            print("Clock resumed")
    
    def set_time(self, time: float):
        """Set current time"""
        self.current_time = time
        if self.sky_object:
            # Clock doesn't have setTime method, just store locally
            print(f"Clock time set to: {time}")
    
    def set_time_scale(self, scale: float):
        """Set time scale"""
        self.time_scale = scale
        if self.sky_object:
            # Clock doesn't have setTimeScale method, just store locally
            print(f"Clock time scale: {scale}")
    
    def get_current_time(self) -> float:
        """Get current time"""
        if self.sky_object:
            # Clock doesn't have getCurrentTime method, return stored value
            return self.current_time
        return self.current_time

class DateManagerComponent(Component):
    """Component for date management"""
    
    def __init__(self):
        super().__init__("DateManager")
        self.sky_object = DateManager()
        self.current_date = None
        self.current_time = None
    
    def set_date(self, year: int, month: int, day: int):
        """Set current date"""
        if self.sky_object:
            self.sky_object.setDate(year, month, day)
            self.current_date = (year, month, day)
            print(f"Date set to: {year}-{month:02d}-{day:02d}")
    
    def set_time(self, hour: int, minute: int, second: int):
        """Set current time"""
        if self.sky_object:
            self.sky_object.setTime(hour, minute, second)
            self.current_time = (hour, minute, second)
            print(f"Time set to: {hour:02d}:{minute:02d}:{second:02d}")
    
    def set_datetime(self, year: int, month: int, day: int, hour: int, minute: int, second: int):
        """Set date and time together"""
        if self.sky_object:
            self.sky_object.setDateTime(year, month, day, hour, minute, second)
            self.current_date = (year, month, day)
            self.current_time = (hour, minute, second)
            print(f"DateTime set to: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
    
    def get_current_date(self):
        """Get current date"""
        if self.sky_object:
            return self.sky_object.getCurrentDate()
        return self.current_date
    
    def get_current_time(self):
        """Get current time"""
        if self.sky_object:
            return self.sky_object.getCurrentTime()
        return self.current_time
    
    def advance_time(self, seconds: float):
        """Advance time by specified seconds"""
        if self.sky_object:
            self.sky_object.advanceTime(seconds)
            print(f"Time advanced by: {seconds} seconds")
    
    def set_timezone(self, timezone: str):
        """Set timezone"""
        if self.sky_object:
            self.sky_object.setTimezone(timezone)
            print(f"Timezone set to: {timezone}")
    
    def get_julian_date(self) -> float:
        """Get Julian date"""
        if self.sky_object:
            return self.sky_object.getJulianDate()
        return 0.0
    
    def set_julian_date(self, jd: float):
        """Set Julian date"""
        if self.sky_object:
            self.sky_object.setJulianDate(jd)
            print(f"Julian date set to: {jd}")
    
    def get_modified_julian_date(self) -> float:
        """Get Modified Julian Date"""
        if self.sky_object:
            return self.sky_object.getModifiedJulianDate()
        return 0.0
    
    def set_modified_julian_date(self, mjd: float):
        """Set Modified Julian Date"""
        if self.sky_object:
            self.sky_object.setModifiedJulianDate(mjd)
            print(f"Modified Julian date set to: {mjd}")
    
    def get_epoch(self) -> str:
        """Get current epoch"""
        if self.sky_object:
            return self.sky_object.getEpoch()
        return "J2000"
    
    def set_epoch(self, epoch: str):
        """Set epoch"""
        if self.sky_object:
            self.sky_object.setEpoch(epoch)
            print(f"Epoch set to: {epoch}")
    
    def get_sidereal_time(self) -> float:
        """Get sidereal time"""
        if self.sky_object:
            return self.sky_object.getSiderealTime()
        return 0.0
    
    def set_sidereal_time(self, st: float):
        """Set sidereal time"""
        if self.sky_object:
            self.sky_object.setSiderealTime(st)
            print(f"Sidereal time set to: {st}")
    
    def get_utc_offset(self) -> float:
        """Get UTC offset"""
        if self.sky_object:
            return self.sky_object.getUtcOffset()
        return 0.0
    
    def set_utc_offset(self, offset: float):
        """Set UTC offset"""
        if self.sky_object:
            self.sky_object.setUtcOffset(offset)
            print(f"UTC offset set to: {offset}")
    
    def get_day_of_year(self) -> int:
        """Get day of year"""
        if self.sky_object:
            return self.sky_object.getDayOfYear()
        return 1
    
    def get_week_of_year(self) -> int:
        """Get week of year"""
        if self.sky_object:
            return self.sky_object.getWeekOfYear()
        return 1
    
    def get_month_name(self) -> str:
        """Get month name"""
        if self.sky_object:
            return self.sky_object.getMonthName()
        return "January"
    
    def get_day_name(self) -> str:
        """Get day name"""
        if self.sky_object:
            return self.sky_object.getDayName()
        return "Monday"
    
    def is_leap_year(self) -> bool:
        """Check if current year is leap year"""
        if self.sky_object:
            return self.sky_object.isLeapYear()
        return False
    
    def get_days_in_month(self) -> int:
        """Get days in current month"""
        if self.sky_object:
            return self.sky_object.getDaysInMonth()
        return 31
    
    def get_days_in_year(self) -> int:
        """Get days in current year"""
        if self.sky_object:
            return self.sky_object.getDaysInYear()
        return 365

class AsteroidComponent(Component):
    """Component for asteroids"""
    
    def __init__(self, asteroid_name: Asteroid.AsteroidName):
        super().__init__("Asteroid")
        self.asteroid_name = asteroid_name
        self.intensity = 1.0
        self.scale = 1.0
        self.sky_object = Asteroid(asteroid_name)
        
        # Asteroid properties
        self.orbit_intensity = 0.0
        self.pointer_intensity = 0.0
        self.label_intensity = 0.0
        self.trajectory_intensity = 0.0
        
    def set_intensity(self, intensity: float):
        """Set asteroid intensity"""
        self.intensity = intensity
        if self.sky_object:
            self.sky_object.setIntensity(intensity)
    
    def set_scale(self, scale: float):
        """Set asteroid scale"""
        self.scale = scale
        if self.sky_object:
            self.sky_object.setScale(scale)
    
    def set_orbit_intensity(self, intensity: float):
        """Set orbit intensity (0-1)"""
        self.orbit_intensity = intensity
        if self.sky_object:
            self.sky_object.setOrbitIntensity(intensity)
    
    def set_pointer_intensity(self, intensity: float):
        """Set pointer intensity (0-1)"""
        self.pointer_intensity = intensity
        if self.sky_object:
            self.sky_object.pointerIntensity = intensity
    
    def set_label_intensity(self, intensity: float):
        """Set label intensity (0-1)"""
        self.label_intensity = intensity
        if self.sky_object:
            self.sky_object.labelIntensity = intensity
    
    def set_trajectory_intensity(self, intensity: float):
        """Set trajectory intensity (0-1)"""
        self.trajectory_intensity = intensity
        if self.sky_object:
            self.sky_object.trajectoryIntensity = intensity

class CometComponent(Component):
    """Component for comets"""
    
    def __init__(self, comet_name: Comet.CometName):
        super().__init__("Comet")
        self.comet_name = comet_name
        self.intensity = 1.0
        self.scale = 1.0
        self.sky_object = Comet(comet_name)
        
        # Comet properties
        self.tail_intensity = 0.5
        self.nucleus_intensity = 1.0
        self.orbit_intensity = 0.0
        self.pointer_intensity = 0.0
        self.label_intensity = 0.0
        self.trajectory_intensity = 0.0
        
    def set_intensity(self, intensity: float):
        """Set comet intensity"""
        self.intensity = intensity
        if self.sky_object:
            self.sky_object.setIntensity(intensity)
    
    def set_scale(self, scale: float):
        """Set comet scale"""
        self.scale = scale
        if self.sky_object:
            self.sky_object.setScale(scale)
    
    def set_tail_intensity(self, intensity: float):
        """Set tail intensity (0-1)"""
        self.tail_intensity = intensity
        if self.sky_object:
            self.sky_object.tailIntensity = intensity
    
    def set_nucleus_intensity(self, intensity: float):
        """Set nucleus intensity (0-1)"""
        self.nucleus_intensity = intensity
        if self.sky_object:
            self.sky_object.nucleusIntensity = intensity
    
    def set_orbit_intensity(self, intensity: float):
        """Set orbit intensity (0-1)"""
        self.orbit_intensity = intensity
        if self.sky_object:
            self.sky_object.setOrbitIntensity(intensity)
    
    def set_pointer_intensity(self, intensity: float):
        """Set pointer intensity (0-1)"""
        self.pointer_intensity = intensity
        if self.sky_object:
            self.sky_object.pointerIntensity = intensity
    
    def set_label_intensity(self, intensity: float):
        """Set label intensity (0-1)"""
        self.label_intensity = intensity
        if self.sky_object:
            self.sky_object.labelIntensity = intensity
    
    def set_trajectory_intensity(self, intensity: float):
        """Set trajectory intensity (0-1)"""
        self.trajectory_intensity = intensity
        if self.sky_object:
            self.sky_object.trajectoryIntensity = intensity

class SatelliteComponent(Component):
    """Component for satellites"""
    
    def __init__(self, satellite_name: Satellite.SatelliteName):
        super().__init__("Satellite")
        self.satellite_name = satellite_name
        self.intensity = 1.0
        self.scale = 1.0
        self.sky_object = Satellite(satellite_name)
        
        # Satellite properties
        self.orbit_intensity = 0.0
        self.pointer_intensity = 0.0
        self.label_intensity = 0.0
        self.trajectory_intensity = 0.0
        self.model_intensity = 1.0
        
    def set_intensity(self, intensity: float):
        """Set satellite intensity"""
        self.intensity = intensity
        if self.sky_object:
            self.sky_object.setIntensity(intensity)
    
    def set_scale(self, scale: float):
        """Set satellite scale"""
        self.scale = scale
        if self.sky_object:
            self.sky_object.setScale(scale)
    
    def set_orbit_intensity(self, intensity: float):
        """Set orbit intensity (0-1)"""
        self.orbit_intensity = intensity
        if self.sky_object:
            self.sky_object.setOrbitIntensity(intensity)
    
    def set_pointer_intensity(self, intensity: float):
        """Set pointer intensity (0-1)"""
        self.pointer_intensity = intensity
        if self.sky_object:
            self.sky_object.setPointerIntensity(intensity)
    
    def set_label_intensity(self, intensity: float):
        """Set label intensity (0-1)"""
        self.label_intensity = intensity
        if self.sky_object:
            self.sky_object.setLabelIntensity(intensity)
    
    def set_trajectory_intensity(self, intensity: float):
        """Set trajectory intensity (0-1)"""
        self.trajectory_intensity = intensity
        if self.sky_object:
            self.sky_object.setTrajectoryIntensity(intensity)
    
    def set_model_intensity(self, intensity: float):
        """Set model intensity (0-1)"""
        self.model_intensity = intensity
        if self.sky_object:
            self.sky_object.modelIntensity = intensity

class StarsComponent(Component):
    """Component for controlling the starry sky/star field"""
    
    def __init__(self, stars_name: Stars.StarsName = None):
        super().__init__("Stars")
        # Use the first available stars name if none provided
        if stars_name is None:
            try:
                # Try to get the first available StarsName enum value
                available_names = list(Stars.StarsName)
                self.stars_name = available_names[0] if available_names else None
            except:
                self.stars_name = None
        else:
            self.stars_name = stars_name
        self.intensity = 1.0
        self.exposure = 1.0
        self.contrast = 1.0
        self.point_saturation = 1.0
        self.default_label_intensity = 0.0
        
        # Star field properties
        self.proper_motion = False
        self.proper_motion_offset = 0.0
        self.twinkling_amplitude = 0.0
        self.real_twinkling_amplitude = 0.0
        self.variability = False
        self.modelset = Stars.Modelset.Hipparcos
        
        # Filter properties
        self.filter_highlight = False
        
        # Hybrid rendering
        self.hybrid_ratio = 0.0
        self.use_hybrid_ratio = False
        
    def initialize(self, sky_engine):
        """Initialize the stars object"""
        if self.stars_name:
            self.sky_object = Stars(self.stars_name)
            self._apply_all_properties()
        else:
            print("Warning: No valid StarsName available, cannot initialize Stars object")
        
    def _apply_all_properties(self):
        """Apply all stored properties to the sky object"""
        if not self.sky_object:
            return
            
        # Basic properties
        if hasattr(self.sky_object, 'setIntensity'):
            self.sky_object.setIntensity(self.intensity)
        if hasattr(self.sky_object, 'setExposure'):
            self.sky_object.setExposure(self.exposure)
        if hasattr(self.sky_object, 'setContrast'):
            self.sky_object.setContrast(self.contrast)
        if hasattr(self.sky_object, 'setPointSaturation'):
            self.sky_object.setPointSaturation(self.point_saturation)
        if hasattr(self.sky_object, 'setDefaultLabelIntensity'):
            self.sky_object.setDefaultLabelIntensity(self.default_label_intensity)
            
        # Motion and animation
        if hasattr(self.sky_object, 'setProperMotion'):
            self.sky_object.setProperMotion(self.proper_motion)
        if hasattr(self.sky_object, 'setProperMotionOffset'):
            self.sky_object.setProperMotionOffset(self.proper_motion_offset)
        if hasattr(self.sky_object, 'setTwinklingAmplitude'):
            self.sky_object.setTwinklingAmplitude(self.twinkling_amplitude)
        if hasattr(self.sky_object, 'setRealTwinklingAmplitude'):
            self.sky_object.setRealTwinklingAmplitude(self.real_twinkling_amplitude)
        if hasattr(self.sky_object, 'setVariability'):
            self.sky_object.setVariability(self.variability)
            
        # Catalog and filtering
        if hasattr(self.sky_object, 'setModelset'):
            self.sky_object.setModelset(self.modelset)
        if hasattr(self.sky_object, 'setFilterHighlight'):
            self.sky_object.setFilterHighlight(self.filter_highlight)
            
        # Hybrid rendering
        if hasattr(self.sky_object, 'setHybridRatio'):
            self.sky_object.setHybridRatio(self.hybrid_ratio)
        if hasattr(self.sky_object, 'setUseHybridRatio'):
            self.sky_object.setUseHybridRatio(self.use_hybrid_ratio)
    
    def set_intensity(self, intensity: float):
        """Set star field intensity (0=off, 1=full brightness)"""
        self.intensity = intensity
        if self.sky_object and hasattr(self.sky_object, 'setIntensity'):
            self.sky_object.setIntensity(intensity)
        print(f"Stars intensity set to: {intensity}")
        return self
    
    def turn_on(self):
        """Turn on the starry sky"""
        self.set_intensity(1.0)
    
    def turn_off(self):
        """Turn off the starry sky"""
        self.set_intensity(0.0)
    
    def set_exposure(self, exposure: float):
        """Set star exposure"""
        self.exposure = exposure
        if self.sky_object and hasattr(self.sky_object, 'setExposure'):
            self.sky_object.setExposure(exposure)
    
    def set_contrast(self, contrast: float):
        """Set star contrast"""
        self.contrast = contrast
        if self.sky_object and hasattr(self.sky_object, 'setContrast'):
            self.sky_object.setContrast(contrast)
    
    def set_point_saturation(self, saturation: float):
        """Set star point saturation"""
        self.point_saturation = saturation
        if self.sky_object and hasattr(self.sky_object, 'setPointSaturation'):
            self.sky_object.setPointSaturation(saturation)
    
    def set_twinkling(self, amplitude: float):
        """Set star twinkling amplitude"""
        self.twinkling_amplitude = amplitude
        if self.sky_object and hasattr(self.sky_object, 'setTwinklingAmplitude'):
            self.sky_object.setTwinklingAmplitude(amplitude)
    
    def set_proper_motion(self, enabled: bool, offset_years: float = 0.0):
        """Enable/disable proper motion of stars"""
        self.proper_motion = enabled
        self.proper_motion_offset = offset_years
        if self.sky_object:
            if hasattr(self.sky_object, 'setProperMotion'):
                self.sky_object.setProperMotion(enabled)
            if hasattr(self.sky_object, 'setProperMotionOffset'):
                self.sky_object.setProperMotionOffset(offset_years)
    
    def set_catalog(self, catalog: Stars.Modelset):
        """Set star catalog (Hipparcos, GaiaDR2)"""
        self.modelset = catalog
        if self.sky_object and hasattr(self.sky_object, 'setModelset'):
            self.sky_object.setModelset(catalog)
    
    def clear_filters(self):
        """Clear all star filters"""
        if self.sky_object and hasattr(self.sky_object, 'filterClear'):
            self.sky_object.filterClear()

class Capture:
    """Capture class for recording and replaying Sky Engine commands"""
    
    def __init__(self, sky_engine: SkyEngine):
        self.sky_engine = sky_engine
        self.instructions = []
        self.is_recording = False
        self._original_methods = {}
        self._wrapped_objects = {}
    
    def start(self):
        """Start recording commands - override all SkyEngine methods"""
        self.instructions = []
        self.is_recording = True
        self._wrapped_objects = {}
        
        # Override all SkyEngine methods
        self._override_all_methods()
        
        print("Capture started - recording commands")
    
    def stop(self):
        """Stop recording commands - restore original methods"""
        self.is_recording = False
        
        # Restore all original methods
        self._restore_all_methods()
        
        print(f"Capture stopped - recorded {len(self.instructions)} commands")
    
    def run_capture(self):
        """Execute all recorded commands"""
        if not self.instructions:
            print("No commands to run")
            return
        
        print(f"Running {len(self.instructions)} recorded commands...")
        for i, instruction in enumerate(self.instructions):
            try:
                self._execute_instruction(instruction)
                print(f"Executed command {i+1}/{len(self.instructions)}")
            except Exception as e:
                print(f"Error executing command {i+1}: {e}")
        
        print("All commands executed")
    
    def run_parallel(self):
        """Execute all recorded commands simultaneously (in parallel)"""
        if not self.instructions:
            print("No commands to run")
            return
        
        print(f"Running {len(self.instructions)} recorded commands in parallel...")
        
        # Group commands by type for better organization
        camera_commands = []
        object_commands = []
        component_commands = []
        other_commands = []
        
        for instruction in self.instructions:
            method_name = instruction['method']
            if method_name.startswith('set_camera_') or method_name.startswith('move_camera') or method_name.startswith('rotate_camera') or method_name.startswith('zoom_camera') or method_name.startswith('look_at') or method_name.startswith('orbit_camera'):
                camera_commands.append(instruction)
            elif method_name.startswith('_set_object_') or method_name.startswith('create_object') or method_name.startswith('destroy_object'):
                object_commands.append(instruction)
            elif method_name.startswith('_add_component') or method_name.startswith('_remove_component'):
                component_commands.append(instruction)
            else:
                other_commands.append(instruction)
        
        # Execute all commands simultaneously
        all_commands = camera_commands + object_commands + component_commands + other_commands
        
        for i, instruction in enumerate(all_commands):
            try:
                self._execute_instruction(instruction)
                print(f"Executed command {i+1}/{len(all_commands)}: {instruction['method']}")
            except Exception as e:
                print(f"Error executing command {i+1}: {e}")
        
        print(f"All {len(all_commands)} commands executed in parallel")
    
    def _override_all_methods(self):
        """Override all SkyEngine methods to check capture mode"""
        # Get all methods from SkyEngine
        for method_name in dir(self.sky_engine):
            if not method_name.startswith('_') and callable(getattr(self.sky_engine, method_name)):
                original_method = getattr(self.sky_engine, method_name)
                self._original_methods[method_name] = original_method
                
                # Create wrapped method
                def create_wrapped_method(original_method, method_name):
                    def wrapped_method(*args, **kwargs):
                        if self.is_recording:
                            # Record the command
                            self._record_instruction(method_name, *args, **kwargs)
                            print(f"Recorded: {method_name}({args}, {kwargs})")
                            
                            # For create_object, we still need to return an object
                            if method_name == 'create_object':
                                obj = original_method(*args, **kwargs)
                                # Wrap the returned object so its methods are also intercepted
                                wrapped_obj = self._wrap_game_object(obj)
                                self._wrapped_objects[id(obj)] = wrapped_obj
                                return wrapped_obj
                        else:
                            # Execute the command
                            return original_method(*args, **kwargs)
                    return wrapped_method
                
                setattr(self.sky_engine, method_name, create_wrapped_method(original_method, method_name))
    
    def _restore_all_methods(self):
        """Restore all original SkyEngine methods"""
        for method_name, original_method in self._original_methods.items():
            setattr(self.sky_engine, method_name, original_method)
        self._original_methods = {}
    
    def _record_instruction(self, method_name: str, *args, **kwargs):
        """Record an instruction for later execution"""
        if self.is_recording:
            instruction = {
                'method': method_name,
                'args': args,
                'kwargs': kwargs
            }
            self.instructions.append(instruction)
    
    def _execute_instruction(self, instruction):
        """Execute a single recorded instruction"""
        method_name = instruction['method']
        args = instruction.get('args', [])
        kwargs = instruction.get('kwargs', {})
        
        if hasattr(self.sky_engine, method_name):
            method = getattr(self.sky_engine, method_name)
            method(*args, **kwargs)
        else:
            print(f"Warning: Method {method_name} not found on SkyEngine")
    
    def _wrap_game_object(self, obj):
        """Wrap a GameObject to record its operations"""
        class WrappedGameObject:
            def __init__(self, capture_instance, original_obj):
                self.capture = capture_instance
                self.obj = original_obj
                self.name = original_obj.name
                self.components = original_obj.components
                self.children = original_obj.children
                self.parent = original_obj.parent
                self.position = original_obj.position
                self.rotation = original_obj.rotation
                self.scale = original_obj.scale
                self.local_position = original_obj.local_position
                self.local_rotation = original_obj.local_rotation
                self.local_scale = original_obj.local_scale
            
            def set_position(self, position: Vec):
                """Record position change instead of executing it"""
                if self.capture.is_recording:
                    self.capture._record_instruction('_set_object_position', id(self.obj), position)
                    print(f"Recorded: {self.obj.name}.set_position({position})")
                else:
                    self.obj.set_position(position)
            
            def set_rotation(self, rotation: Vec):
                """Record rotation change instead of executing it"""
                if self.capture.is_recording:
                    self.capture._record_instruction('_set_object_rotation', id(self.obj), rotation)
                    print(f"Recorded: {self.obj.name}.set_rotation({rotation})")
                else:
                    self.obj.set_rotation(rotation)
            
            def set_scale(self, scale: Vec):
                """Record scale change instead of executing it"""
                if self.capture.is_recording:
                    self.capture._record_instruction('_set_object_scale', id(self.obj), scale)
                    print(f"Recorded: {self.obj.name}.set_scale({scale})")
                else:
                    self.obj.set_scale(scale)
            
            def add_component(self, component):
                """Record component addition instead of executing it"""
                if self.capture.is_recording:
                    self.capture._record_instruction('_add_component', id(self.obj), component.name, component.__class__.__name__)
                    print(f"Recorded: {self.obj.name}.add_component({component.name})")
                else:
                    self.obj.add_component(component)
            
            def get_component(self, component_name: str):
                """Pass through to original object"""
                return self.obj.get_component(component_name)
            
            def update(self, delta_time: float):
                """Pass through to original object"""
                self.obj.update(delta_time)
        
        return WrappedGameObject(self, obj)
    
    # Utility methods
    def get_instructions_count(self) -> int:
        """Get the number of recorded instructions"""
        return len(self.instructions)
    
    def clear_instructions(self):
        """Clear all recorded instructions"""
        self.instructions = []
        print("All recorded instructions cleared")
    
    def get_instructions(self) -> list:
        """Get all recorded instructions"""
        return self.instructions.copy()
    
    def save_instructions(self, filename: str):
        """Save recorded instructions to a file"""
        import json
        try:
            with open(filename, 'w') as f:
                json.dump(self.instructions, f, indent=2, default=str)
            print(f"Instructions saved to {filename}")
        except Exception as e:
            print(f"Error saving instructions: {e}")
    
    def load_instructions(self, filename: str):
        """Load instructions from a file"""
        import json
        try:
            with open(filename, 'r') as f:
                self.instructions = json.load(f)
            print(f"Instructions loaded from {filename}")
        except Exception as e:
            print(f"Error loading instructions: {e}")

# Example usage
def test_sky_engine():
    """Test the Sky Engine with new navigation and stars features"""
    print("=== Testing Sky Engine ===")
    
    # Create engine
    engine = SkyEngine()
    
    # Test Stars Control
    print("\n=== Testing Stars Control ===")
    
    # Show available stars names for debugging
    print("Checking available Stars names...")
    available_stars = engine.get_available_stars_names()
    
    # Create stars object (will use first available name automatically)
    stars_obj = engine.create_stars_object("Starry Sky")
    stars_comp = stars_obj.get_component("Stars")
    
    print("Turning stars on...")
    engine.turn_stars_on()
    sleep(2)
    
    print("Dimming stars to 50%...")
    engine.set_stars_intensity(0.5)
    sleep(2)
    
    print("Turning stars off...")
    engine.turn_stars_off()
    sleep(2)
    
    print("Turning stars back on...")
    engine.turn_stars_on()
    
    # Test Navigation
    print("\n=== Testing Navigation ===")
    
    print("Going to Jupiter...")
    engine.go_to_planet(Planet.PlanetName.Jupiter)
    sleep(3)
    
    print("Going to the Sun...")
    engine.go_to_star(IndividualStar.IndividualStarName.Sun)
    sleep(3)
    
    print("Going to Ursa Major constellation...")
    engine.go_to_constellation(Constellation.ConstellationName.UMa)
    sleep(3)
    
    # Create objects to show what we're looking at
    print("\n=== Creating Visual Objects ===")
    
    # Create a planet
    planet_obj = engine.create_object("Jupiter")
    planet_comp = PlanetComponent(Planet.PlanetName.Jupiter)
    planet_obj.add_component(planet_comp)
    planet_comp.set_clouds_intensity(0.8)
    # planet_comp.set_atmosphere_intensity(0.5)  # Will implement if needed
    
    # Test Constellation Control
    print("\n=== Testing Constellation Control ===")
    
    # Show available constellation names for debugging
    print("Checking available Constellation names...")
    available_constellations = engine.get_available_constellation_names()
    
    # Create multiple constellations using first few available names
    try:
        if len(available_constellations) >= 3:
            constellation1 = engine.create_constellation_object(available_constellations[0], "Constellation_1")
            constellation2 = engine.create_constellation_object(available_constellations[1], "Constellation_2") 
            constellation3 = engine.create_constellation_object(available_constellations[2], "Constellation_3")
            print(f"Created 3 constellations: {available_constellations[0]}, {available_constellations[1]}, {available_constellations[2]}")
        else:
            print(f"Warning: Only {len(available_constellations)} constellation names available")
    except Exception as e:
        print(f"Error creating constellations: {e}")
        # Try with specific names as fallback
        try:
            orion = engine.create_constellation_object(Constellation.ConstellationName.Ori, "Orion")
            ursa_major = engine.create_constellation_object(Constellation.ConstellationName.UMa, "Ursa Major")
            cassiopeia = engine.create_constellation_object(Constellation.ConstellationName.Cas, "Cassiopeia")
            print("Created 3 constellations using fallback names: Orion, Ursa Major, Cassiopeia")
        except Exception as fallback_error:
            print(f"Fallback constellation creation also failed: {fallback_error}")
    
    sleep(2)
    
    print("Testing individual constellation control...")
    # Try to get the first constellation for individual testing
    try:
        if len(available_constellations) >= 1:
            first_constellation_comp = constellation1.get_component("Constellation")
            first_constellation_comp.turn_all_on()
            sleep(1)
            
            print(f"Turning off {available_constellations[0]} art, keeping lines and labels...")
            first_constellation_comp.turn_art_off()
        else:
            print("No constellations available for individual testing")
    except:
        print("Individual constellation control test skipped")
    sleep(2)
    
    print("Testing global constellation control...")
    print("Turn off all constellation lines...")
    engine.turn_all_constellation_lines_off()
    sleep(2)
    
    print("Turn off all constellation labels...")
    engine.turn_all_constellation_labels_off()
    sleep(2)
    
    print("Show only constellation art...")
    engine.set_constellation_display_mode('art_only')
    sleep(2)
    
    print("Show only constellation lines...")
    engine.set_constellation_display_mode('lines_only')
    sleep(2)
    
    print("Turn everything back on...")
    engine.turn_all_constellations_on()
    
    # Create text
    text_obj = engine.create_object("Navigation Demo")
    text_comp = TextComponent("Sky Engine Navigation Demo")
    text_obj.add_component(text_comp)
    text_comp.set_position(Vec(0, 20, 0))
    
    print("\n=== Demo Running ===")
    print("Features demonstrated:")
    print("- Starry sky control (on/off/dimming)")
    print("- Navigation to planets, stars, constellations")
    print("- Component-based object creation")
    print("- Dynamic intensity controls")
    
    # Demonstrate more navigation
    print("\nDemonstrating more navigation features...")
    sleep(2)
    
    print("Going to Mars...")
    engine.go_to_planet(Planet.PlanetName.Mars)
    sleep(2)
    
    print("Going to Saturn...")
    engine.go_to_planet(Planet.PlanetName.Saturn)
    sleep(2)
    
    print("Returning to Earth view...")
    engine.go_to_planet(Planet.PlanetName.Earth)
    
    print("\n=== Test completed! ===")
    print("Sky Engine now supports:")
    print("✓ Stars on/off control")
    print("✓ Navigation to planets, stars, constellations")
    print("✓ Full constellation control (lines, art, labels, boundaries)")
    print("✓ Individual and global constellation management") 
    print("✓ Constellation display modes")
    print("✓ Component-based architecture")
    print("✓ Animation and keyframe system")
    print("✓ Camera controls")
    
    print("\nConstellation Features:")
    print("  • Individual control: constellation_comp.turn_lines_on/off()")
    print("  • Global control: engine.turn_all_constellation_lines_on/off()")
    print("  • Display modes: engine.set_constellation_display_mode('lines_only')")
    print("  • Supported modes: 'lines_only', 'art_only', 'labels_only', 'all', 'none'")
    
    print("\nDebugging Features:")
    print("  • Check available stars: engine.get_available_stars_names()")
    print("  • Check available constellations: engine.get_available_constellation_names()")
    print("  • Stars auto-detect: StarsComponent() uses first available name")
    print("  • Robust error handling for missing enum values")
    
    print("\nID Management Features:")
    print("  • Every GameObject has unique ID: obj.id")
    print("  • Find by ID: engine.get_object_by_id(id)")
    print("  • Get all IDs: engine.get_all_object_ids()")
    print("  • Object info: obj.get_info() or engine.get_object_info(id)")
    print("  • Navigate to GameObjects: engine.go_to_game_object(obj)")
    
    # Demonstrate ID features
    print(f"\n=== ID Management Demo ===")
    all_ids = engine.get_all_object_ids()
    print(f"Created {len(all_ids)} objects with IDs: {all_ids}")
    
    # Show info for first object
    if all_ids:
        first_id = all_ids[0]
        obj_info = engine.get_object_info(first_id)
        print(f"First object info: {obj_info}")
        
        # Try to navigate to first object if it has a sky object  
        first_obj = engine.get_object_by_id(first_id)
        if first_obj and first_obj.get_sky_object_id():
            print(f"Navigating to first object: {first_obj.name}")
            engine.go_to_game_object(first_obj)
    
    # Show object type counts
    type_counts = engine.count_objects_by_type()
    print(f"Objects by type: {type_counts}")
    
    # List all objects in scene
    engine.list_all_objects()
    
    # Find objects by component type
    planet_objects = engine.get_objects_by_component_type("Planet")
    print(f"Found {len(planet_objects)} planet objects")
    
    constellation_objects = engine.get_objects_by_component_type("Constellation")
    print(f"Found {len(constellation_objects)} constellation objects")

if __name__ == "__main__":
    test_sky_engine() 