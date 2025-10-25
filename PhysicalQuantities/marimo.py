"""
Marimo Physics Extension - IPython-like Magic for Physical Quantities

This extension monkey-patches marimo's cell compilation to automatically transform
physics syntax like "a = 100mm" to "a = q(100, 'mm')" just like IPython magic.

Usage:
    from marimo_physics_extension import enable_physics_magic, pq
    enable_physics_magic()
    
    # Now you can use natural syntax in any cell:
    # a = 100 mm      # becomes: a = q(100, 'mm')
    # v = 10 m/s      # becomes: v = q(10, 'm/s')  
    # force = 5N      # becomes: force = q(5, 'N')
"""

from typing import Optional, Callable
from PhysicalQuantities.transform import transform_line


class PhysicsTransformer:
    """Transform physics syntax to PhysicalQuantity calls using transform_line"""

    def __init__(self):
        pass  # No regex rules needed

    def transform_code(self, code: str) -> str:
        """Transform physics syntax in code using transform_line for each line"""
        if not code.strip():
            return code

        lines = code.split('\n')
        transformed_lines = []

        for line in lines:
            # Skip empty lines, comments, and imports
            if not line.strip() or line.strip().startswith('#') or \
               line.strip().startswith('import') or line.strip().startswith('from'):
                transformed_lines.append(line)
                continue

            transformed_line = transform_line(line)
            transformed_lines.append(transformed_line)

        return '\n'.join(transformed_lines)


# Global transformer instance
_physics_transformer = PhysicsTransformer()

# Store original compile_cell function
_original_compile_cell: Optional[Callable] = None


def _physics_compile_cell(code: str, *args, **kwargs):
    """Wrapper for compile_cell that applies physics transformations"""
    # Transform the code first
    transformed_code = _physics_transformer.transform_code(code)
    
    # Call the original compile_cell with transformed code
    return _original_compile_cell(transformed_code, *args, **kwargs)


def enable_physics_magic():
    """Enable automatic physics syntax transformation in marimo cells"""
    global _original_compile_cell
    
    try:
        # First, ensure PhysicalQuantities environment is set up
        q = setup_physics_environment(verbose=False)
        if q is None:
            return False
            
        # Import marimo's compile_cell function
        from marimo._ast.compiler import compile_cell
        
        # Store the original if not already done
        if _original_compile_cell is None:
            _original_compile_cell = compile_cell
            
        # Monkey-patch the module
        import marimo._ast.compiler as compiler_module
        compiler_module.compile_cell = _physics_compile_cell
        
        # Also patch any other modules that might import compile_cell
        import marimo._runtime.runtime as runtime_module
        if hasattr(runtime_module, 'compile_cell'):
            runtime_module.compile_cell = _physics_compile_cell
            
        import marimo._islands._island_generator as islands_module  
        if hasattr(islands_module, 'compile_cell'):
            islands_module.compile_cell = _physics_compile_cell
        return True
        
    except ImportError as e:
        print(f"❌ Could not enable physics magic: {e}")
        print("Make sure you're running this inside a marimo notebook.")
        return False
    except Exception as e:
        print(f"❌ Error enabling physics magic: {e}")
        return False


def disable_physics_magic():
    """Disable physics syntax transformation and restore original behavior"""
    global _original_compile_cell
    
    if _original_compile_cell is None:
        print("⚠️  Physics magic was not enabled.")
        return False
        
    try:
        # Restore original compile_cell
        import marimo._ast.compiler as compiler_module
        compiler_module.compile_cell = _original_compile_cell
        
        # Restore in other modules too
        import marimo._runtime.runtime as runtime_module
        if hasattr(runtime_module, 'compile_cell'):
            runtime_module.compile_cell = _original_compile_cell
            
        import marimo._islands._island_generator as islands_module
        if hasattr(islands_module, 'compile_cell'):
            islands_module.compile_cell = _original_compile_cell
            
        print("✅ Physics magic disabled. Normal marimo behavior restored.")
        return True
        
    except Exception as e:
        print(f"❌ Error disabling physics magic: {e}")
        return False


def setup_physics_environment(verbose=True):
    """Setup the physics environment with PhysicalQuantities"""
    try:
        # Check if q is already available
        import builtins
        if hasattr(builtins, 'q'):
            if verbose:
                print("✅ PhysicalQuantities environment already ready.")
            return builtins.q
            
        from PhysicalQuantities import PhysicalQuantity as q
        
        # Make q available globally so transformations work
        builtins.q = q
        
        if verbose:
            print("✅ PhysicalQuantities environment ready.")
            print("Use enable_physics_magic() to activate natural syntax.")
        
        return q
        
    except ImportError:
        print("❌ PhysicalQuantities not found. Install with: pip install PhysicalQuantities")
        return None


# Convenience function to do everything at once
def activate_physics():
    """Complete physics setup - environment + magic transformations"""
    q = setup_physics_environment()
    if q is not None:
        success = enable_physics_magic()
        if success:
            print("\n🚀 Physics magic is now active! Try this in a cell:")
            print("    length = 5 m")
            print("    time = 2 s") 
            print("    velocity = length / time")
            print("    print(velocity)")
            return True
    return False


if __name__ == "__main__":
    # Demo the transformation
    code = """
a = 5 cm + 1m
b = 100 mm
v = 10 m/s  
force = 5N
energy = 1.5 kJ
result = force // N
"""
    
    transformer = PhysicsTransformer()
    transformed = transformer.transform_code(code)
    
    print("Original code:")
    print(code)
    print("\nTransformed code:")
    print(transformed) 