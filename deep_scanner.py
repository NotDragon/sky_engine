import inspect
import importlib
import sys
import io
from contextlib import redirect_stdout
from typing import Any, Dict, List, Tuple, Optional, Set, Union
import os
import types
import re
import inspect
 
def format_signature(obj: Any, name: str) -> str:
    """Generate a stub-style function signature for a callable."""
    try:
        sig = inspect.signature(obj)
        return f"def {name}{sig}:"
    except Exception as e:
        return f"def {name}(...):  # Signature error: {e}"
 
 
class DeepLibraryScanner:
    def __init__(self, library_name: str, max_depth: int = 10):
        """
        Initialize the deep scanner.
 
        Args:
            library_name: Name of the library to scan
            max_depth: Maximum recursion depth for nested scanning
        """
        self.library_name = library_name
        self.max_depth = max_depth
        self.library = None
        self.output_lines = []
        self.processed_items: Set[int] = set()
        self.current_depth = 0
        self.class_hierarchy = {}  # Track class relationships
 
    def import_library(self) -> bool:
        """Import the target library."""
        try:
            self.library = importlib.import_module(self.library_name)
            return True
        except ImportError as e:
            print(f"Error importing library '{self.library_name}': {e}")
            return False
 
    
 
    def get_comprehensive_signature(self, func: Any) -> str:
        """Get the most comprehensive signature possible."""
        try:
            sig = inspect.signature(func)
            return str(sig)
        except (ValueError, TypeError):
            # Fallback methods
            try:
                if hasattr(func, '__code__'):
                    code = func.__code__
                    argnames = code.co_varnames[:code.co_argcount]
                    defaults = func.__defaults__ or []
 
                    # Build signature manually
                    args = []
                    default_offset = len(argnames) - len(defaults)
 
                    for i, arg in enumerate(argnames):
                        if i >= default_offset:
                            default_val = defaults[i - default_offset]
                            args.append(f"{arg}={repr(default_val)}")
                        else:
                            args.append(arg)
 
                    if code.co_flags & 0x04:  # CO_VARARGS
                        args.append("*args")
                    if code.co_flags & 0x08:  # CO_VARKEYWORDS
                        args.append("**kwargs")
 
                    return f"({', '.join(args)})"
            except:
                pass
 
            return "(*args, **kwargs)"
 
    def get_all_attributes(self, obj: Any) -> Dict[str, Any]:
        """Get ALL attributes of an object, including special ones."""
        attributes = {}
 
        # Use dir() to get all attributes
        try:
            for name in dir(obj):
                try:
                    attr = getattr(obj, name)
                    attributes[name] = attr
                except Exception as e:
                    attributes[name] = f"<Error accessing: {e}>"
        except:
            pass
 
        # Also try __dict__ if available
        try:
            if hasattr(obj, '__dict__'):
                attributes.update(obj.__dict__)
        except:
            pass
 
        # Try __slots__ for slotted classes
        try:
            if hasattr(obj, '__slots__'):
                for slot in obj.__slots__:
                    if slot not in attributes:
                        try:
                            attributes[slot] = getattr(obj, slot)
                        except:
                            attributes[slot] = "<slot>"
        except:
            pass
 
        return attributes
 
    def categorize_class_members(self, cls: type) -> Dict[str, List[Tuple[str, Any]]]:
        """Categorize all class members by type."""
        categories = {
            'class_methods': [],
            'static_methods': [],
            'instance_methods': [],
            'properties': [],
            'descriptors': [],
            'class_variables': [],
            'nested_classes': [],
            'special_methods': [],
            'other_attributes': []
        }
 
        all_attrs = self.get_all_attributes(cls)
 
        for name, attr in all_attrs.items():
            try:
                # Get the actual attribute from the class
                class_attr = getattr(cls, name) if hasattr(cls, name) else attr
 
                # Categorize based on type and properties
                if inspect.isclass(class_attr):
                    categories['nested_classes'].append((name, class_attr))
                elif isinstance(class_attr, classmethod):
                    categories['class_methods'].append((name, class_attr))
                elif isinstance(class_attr, staticmethod):
                    categories['static_methods'].append((name, class_attr))
                elif isinstance(class_attr, property):
                    categories['properties'].append((name, class_attr))
                elif hasattr(class_attr, '__get__') or hasattr(class_attr, '__set__'):
                    categories['descriptors'].append((name, class_attr))
                elif name.startswith('__') and name.endswith('__'):
                    if callable(class_attr):
                        categories['special_methods'].append((name, class_attr))
                    else:
                        categories['other_attributes'].append((name, class_attr))
                elif callable(class_attr):
                    categories['instance_methods'].append((name, class_attr))
                else:
                    categories['class_variables'].append((name, class_attr))
 
            except Exception as e:
                categories['other_attributes'].append((name, f"<Error: {e}>"))
 
        return categories
 
    def process_method(self, name: str, method: Any, method_type: str, indent: str) -> None:
        """Process different types of methods."""
        
        # Add appropriate decorators and definitions
        if method_type == "classmethod":
            self.output_lines.append(f"{indent}@classmethod")
            sig = self.get_comprehensive_signature(method.__func__ if hasattr(method, '__func__') else method)
            self.output_lines.append(f"{indent}def {name}{sig}:")
        elif method_type == "staticmethod":
            self.output_lines.append(f"{indent}@staticmethod")
            sig = self.get_comprehensive_signature(method.__func__ if hasattr(method, '__func__') else method)
            self.output_lines.append(f"{indent}def {name}{sig}:")
        elif method_type == "property":
            self.output_lines.append(f"{indent}@property")
            self.output_lines.append(f"{indent}def {name}(self):")
        else:
            sig = self.get_comprehensive_signature(method)
            self.output_lines.append(f"{indent}def {name}{sig}:")
 
        self.output_lines.append(f"{indent}    pass")
        self.output_lines.append("")
 
    def process_class_deep(self, name: str, cls: type, indent: str = "", depth: int = 0) -> None:
        """Deep processing of a class with all its members."""
        if depth > self.max_depth:
            self.output_lines.append(f"{indent}# Max depth reached for class {name}")
            return
 
        obj_id = id(cls)
        if obj_id in self.processed_items:
            self.output_lines.append(f"{indent}# Already processed: {name}")
            return

        self.processed_items.add(obj_id)

        # Get inheritance info
        bases = []
        for base in cls.__bases__:
            if base != object:
                bases.append(base.__name__)
        bases_str = f"({', '.join(bases)})" if bases else ""
 
        # Add class definition
        self.output_lines.append(f"{indent}class {name}{bases_str}:")
        class_indent = indent + "    "
 
        # Categorize all members
        categories = self.categorize_class_members(cls)
 
        has_members = any(members for members in categories.values())
        if not has_members:
            self.output_lines.append(f"{class_indent}pass")
            self.output_lines.append("")
            return
 
        # Process each category
        if categories['class_variables']:
            self.output_lines.append(f"{class_indent}# Class Variables")
            for var_name, var_value in sorted(categories['class_variables']):
                try:

 
                    value_repr = repr(var_value)
                    if len(value_repr) > 100:
                        value_repr = value_repr[:97] + "..."
                    self.output_lines.append(f"{class_indent}{var_name} = None")
                    self.output_lines.append("")
                except Exception as e:
                    self.output_lines.append(f"{class_indent}{var_name} = None  # Error: {e}")
                    self.output_lines.append("")
 
        # Process special methods
        if categories['special_methods']:
            self.output_lines.append(f"{class_indent}# Special Methods")
            for method_name, method in sorted(categories['special_methods']):
                try:
                    self.process_method(method_name, method, "special", class_indent)
                except Exception as e:
                    self.output_lines.append(f"{class_indent}# Error processing {method_name}: {e}")
                    self.output_lines.append(f"{class_indent}def {method_name}(self, *args, **kwargs): pass")
                    self.output_lines.append("")
 
        # Process class methods
        if categories['class_methods']:
            self.output_lines.append(f"{class_indent}# Class Methods")
            for method_name, method in sorted(categories['class_methods']):
                try:
                    self.process_method(method_name, method, "classmethod", class_indent)
                except Exception as e:
                    self.output_lines.append(f"{class_indent}# Error processing classmethod {method_name}: {e}")
                    self.output_lines.append("")
 
        # Process static methods
        if categories['static_methods']:
            self.output_lines.append(f"{class_indent}# Static Methods")
            for method_name, method in sorted(categories['static_methods']):
                try:
                    self.process_method(method_name, method, "staticmethod", class_indent)
                except Exception as e:
                    self.output_lines.append(f"{class_indent}# Error processing staticmethod {method_name}: {e}")
                    self.output_lines.append("")
 
        # Process properties
        if categories['properties']:
            self.output_lines.append(f"{class_indent}# Properties")
            for prop_name, prop in sorted(categories['properties']):
                try:
                    self.process_method(prop_name, prop, "property", class_indent)
                except Exception as e:
                    self.output_lines.append(f"{class_indent}# Error processing property {prop_name}: {e}")
                    self.output_lines.append("")
 
        # Process descriptors
        if categories['descriptors']:
            self.output_lines.append(f"{class_indent}# Descriptors")
            for desc_name, desc in sorted(categories['descriptors']):
                try:

                    self.output_lines.append(f"{class_indent}{desc_name} = None  # Descriptor: {type(desc).__name__}")
                    self.output_lines.append("")
                except Exception as e:
                    self.output_lines.append(f"{class_indent}{desc_name} = None  # Descriptor error: {e}")
                    self.output_lines.append("")
 
        # Process instance methods
        if categories['instance_methods']:
            self.output_lines.append(f"{class_indent}# Instance Methods")
            for method_name, method in sorted(categories['instance_methods']):
                try:
                    self.process_method(method_name, method, "instance", class_indent)
                except Exception as e:
                    self.output_lines.append(f"{class_indent}# Error processing method {method_name}: {e}")
                    self.output_lines.append(f"{class_indent}def {method_name}(self, *args, **kwargs): pass")
                    self.output_lines.append("")
 
        # Process nested classes (recursive)
        if categories['nested_classes']:
            self.output_lines.append(f"{class_indent}# Nested Classes")
            for nested_name, nested_cls in sorted(categories['nested_classes']):
                try:
                    self.process_class_deep(nested_name, nested_cls, class_indent, depth + 1)
                except Exception as e:
                    self.output_lines.append(f"{class_indent}# Error processing nested class {nested_name}: {e}")
                    self.output_lines.append(f"{class_indent}class {nested_name}: pass")
                    self.output_lines.append("")
 
        # Process other attributes
        if categories['other_attributes']:
            self.output_lines.append(f"{class_indent}# Other Attributes")
            for attr_name, attr_value in sorted(categories['other_attributes']):
                try:
                    # if not isinstance(attr_value, str) or not attr_value.startswith("<Error"):
                    #     help_text = self.capture_help(attr_value, f"attribute {attr_name}")
                    #     for line in help_text.split('\n'):
                    #         self.output_lines.append(f"{class_indent}{line}")
 
                    value_repr = repr(attr_value)
                    if len(value_repr) > 100:
                        value_repr = value_repr[:97] + "..."
                    self.output_lines.append(f"{class_indent}{attr_name} = None")
                    self.output_lines.append("")
                except Exception as e:
                    self.output_lines.append(f"{class_indent}{attr_name} = None  # Error: {e}")
                    self.output_lines.append("")
 
        self.output_lines.append("")
 
    def process_function_deep(self, name: str, func: Any, indent: str = "") -> None:
        """Deep processing of functions."""
        if id(func) in self.processed_items:
            return
        self.processed_items.add(id(func))
 

 
        # Get signature
        sig = self.get_comprehensive_signature(func)
        self.output_lines.append(f"{indent}def {name}{sig}:")
        self.output_lines.append(f"{indent}    pass")
        self.output_lines.append("")
 
    def scan_library_deep(self) -> None:
        """Perform deep scanning of the entire library."""
        if not self.library:
            print("Library not imported. Call import_library() first.")
            return
 
        # Add comprehensive header
        self.output_lines.extend([
            f'"""',
            f'DEEP SCAN STUB for library: {self.library_name}',
            f'Generated by deep_scanner.py',
            f'',
            f'This comprehensive stub includes:',
            f'- All public and private members',
            f'- Complete class hierarchies with all methods',
            f'- Properties, descriptors, class/static methods',
            f'- Nested classes and inner classes',
            f'- Class variables and instance variables',
            f'- Special methods (__init__, __str__, etc.)',
            f'- Comprehensive help documentation',
            f'- Complete function signatures',
            f'"""',
            "",
            "from typing import Any, Optional, Union, List, Dict, Tuple, Callable, Iterator",
            ""
        ])
 
        # Get all library members
        try:
            all_members = self.get_all_attributes(self.library)
        except Exception as e:
            print(f"Error getting library attributes: {e}")
            return
 
        # Categorize all top-level members
        functions = []
        classes = []
        modules = []
        constants = []
        variables = []
 
        for name, obj in all_members.items():
            try:
                if inspect.isclass(obj):
                    classes.append((name, obj))
                elif inspect.ismodule(obj):
                    modules.append((name, obj))
                elif isinstance(obj, (int, float, str, bool, type(None))):
                    constants.append((name, obj))
                elif callable(obj):
                    # Catch ALL callable objects (functions, methods, callable classes, etc.)
                    functions.append((name, obj))
                else:
                    variables.append((name, obj))
            except Exception as e:
                variables.append((name, f"<Error: {e}>"))
 
        # Process constants
        if constants:
            self.output_lines.append("# ============= CONSTANTS =============")
            self.output_lines.append("")
            for name, const in sorted(constants):
                try:

                    self.output_lines.append(f"{name} = None")
                    self.output_lines.append("")
                except Exception as e:
                    self.output_lines.append(f"# Error processing constant {name}: {e}")
                    self.output_lines.append(f"{name} = None")
                    self.output_lines.append("")
 
        # Process variables
        if variables:
            self.output_lines.append("# ============= VARIABLES =============")
            self.output_lines.append("")
            for name, var in sorted(variables):
                try:
                    var_repr = repr(var)
                    if len(var_repr) > 200:
                        var_repr = var_repr[:197] + "..."
                    self.output_lines.append(f"{name} = None")
                    self.output_lines.append("")
                except Exception as e:
                    self.output_lines.append(f"# Error processing variable {name}: {e}")
                    self.output_lines.append(f"{name} = None")
                    self.output_lines.append("")
 
        # Process functions with deep analysis
        if functions:
            self.output_lines.append("# ============= FUNCTIONS =============")
            self.output_lines.append("")
            for name, func in sorted(functions):
                try:
                    self.process_function_deep(name, func)
                except Exception as e:
                    self.output_lines.append(f"# Error processing function {name}: {e}")
                    self.output_lines.append(f"def {name}(*args, **kwargs): pass")
                    self.output_lines.append("")
 
        # Process classes with comprehensive deep scanning
        if classes:
            self.output_lines.append("# ============= CLASSES =============")
            self.output_lines.append("")
            for name, cls in sorted(classes):
                try:
                    self.process_class_deep(name, cls)
                except Exception as e:
                    self.output_lines.append(f"# Error processing class {name}: {e}")
                    self.output_lines.append(f"class {name}: pass")
                    self.output_lines.append("")
 
        # Process submodules
        if modules:
            self.output_lines.append("# ============= SUBMODULES =============")
            self.output_lines.append("")
            for name, module in sorted(modules):
                try:

                    self.output_lines.append(f"# Submodule: {name}")
                    self.output_lines.append(f"# Import with: from {self.library_name} import {name}")
 
                    # Try to scan submodule members too (if not too deep)
                    if self.current_depth < 2:
                        try:
                            submodule_attrs = self.get_all_attributes(module)
                            if submodule_attrs:
                                self.output_lines.append(f"# {name} contains: {list(submodule_attrs.keys())}")
                        except:
                            pass
 
                    self.output_lines.append("")
                except Exception as e:
                    self.output_lines.append(f"# Error processing submodule {name}: {e}")
                    self.output_lines.append("")
 
    def save_to_file(self, output_path: str) -> None:
        """Save the deep scan results."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.output_lines))
            print(f"Deep scan stub saved to: {output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
 
    def get_comprehensive_stats(self) -> Dict[str, int]:
        """Get detailed statistics about the scan."""
        stats = {
            'total_lines': len(self.output_lines),
            'documentation_lines': sum(1 for line in self.output_lines if '"""' in line),
            'class_definitions': sum(1 for line in self.output_lines if line.strip().startswith('class ')),
            'function_definitions': sum(1 for line in self.output_lines if line.strip().startswith('def ')),
            'property_definitions': sum(1 for line in self.output_lines if line.strip() == '@property'),
            'classmethod_definitions': sum(1 for line in self.output_lines if line.strip() == '@classmethod'),
            'staticmethod_definitions': sum(1 for line in self.output_lines if line.strip() == '@staticmethod'),
            'processed_objects': len(self.processed_items),
        }
        return stats
 
def scan(library_name): 
    output_file = f"{library_name}_deep_stub.py"
 
    # Create deep scanner
    scanner = DeepLibraryScanner(library_name)
 
    # Import and scan
    if scanner.import_library():
        print(f"Successfully imported library: {library_name}")
        print("Performing deep comprehensive scan...")
        print("This may take a while for large libraries...")
 
        scanner.scan_library_deep()
 
        # Save results
        scanner.save_to_file(output_file)
 
        # Show comprehensive stats
        stats = scanner.get_comprehensive_stats()
        print("\n=== DEEP SCAN STATISTICS ===")
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
 
        print(f"\nDeep stub file created: {output_file}")
        print("This file contains EVERYTHING discoverable in the library!")
 
    else:
        print("Failed to import library")
        print("Make sure the library is accessible in your Python environment")
        sys.exit(1)
 
 
 
def main():
    """Main function for deep library scanning."""
    if len(sys.argv) < 2:
        print("Usage: python deep_scanner.py <library_name> [output_file]")
        print("Example: python deep_scanner.py skyExplorer skyExplorer_deep_stub.py")
        print()
        print("This scanner performs COMPREHENSIVE analysis including:")
        print("- All class members (public/private/special)")
        print("- Nested classes and inheritance")
        print("- Properties, descriptors, class/static methods")
        print("- Complete help documentation")
        print("- Full function signatures")
        sys.exit(1)
 
    library_name = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"{library_name}_deep_stub.py"
 
    # Create deep scanner
    scanner = DeepLibraryScanner(library_name)
 
    # Import and scan
    if scanner.import_library():
        print(f"Successfully imported library: {library_name}")
        print("Performing deep comprehensive scan...")
        print("This may take a while for large libraries...")
 
        scanner.scan_library_deep()
 
        # Save results
        scanner.save_to_file(output_file)
 
        # Show comprehensive stats
        stats = scanner.get_comprehensive_stats()
        print("\n=== DEEP SCAN STATISTICS ===")
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
 
        print(f"\nDeep stub file created: {output_file}")
        print("This file contains EVERYTHING discoverable in the library!")
 
    else:
        print("Failed to import library")
        print("Make sure the library is accessible in your Python environment")
        sys.exit(1)
 
 
if __name__ == "__main__":
    main()