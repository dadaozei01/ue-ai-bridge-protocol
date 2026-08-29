import unreal

FOLDER = "/Game/AI材质"
NAME = "M_AI_FlickerGlow"
PATH = FOLDER + "/" + NAME


def make_expression(material, cls, x, y):
    return unreal.MaterialEditingLibrary.create_material_expression(material, cls, x, y)


if not unreal.EditorAssetLibrary.does_directory_exist(FOLDER):
    unreal.EditorAssetLibrary.make_directory(FOLDER)

material = unreal.EditorAssetLibrary.load_asset(PATH)
if material is None:
    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        NAME,
        FOLDER,
        unreal.Material,
        unreal.MaterialFactoryNew(),
    )

material.set_editor_property("use_material_attributes", False)
material.set_editor_property("blend_mode", unreal.BlendMode.BLEND_OPAQUE)
material.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_DEFAULT_LIT)

for expression in list(material.expressions):
    unreal.MaterialEditingLibrary.delete_material_expression(material, expression)

base = make_expression(material, unreal.MaterialExpressionVectorParameter, -900, -120)
base.set_editor_property("parameter_name", "BaseColor")
base.set_editor_property("default_value", unreal.LinearColor(0.1, 0.25, 1.0, 1.0))
unreal.MaterialEditingLibrary.connect_material_property(base, "", unreal.MaterialProperty.MP_BASE_COLOR)

glow = make_expression(material, unreal.MaterialExpressionVectorParameter, -900, 160)
glow.set_editor_property("parameter_name", "GlowColor")
glow.set_editor_property("default_value", unreal.LinearColor(0.0, 0.8, 1.0, 1.0))

time = make_expression(material, unreal.MaterialExpressionTime, -900, 420)
speed = make_expression(material, unreal.MaterialExpressionScalarParameter, -700, 500)
speed.set_editor_property("parameter_name", "Speed")
speed.set_editor_property("default_value", 4.0)
mul_time = make_expression(material, unreal.MaterialExpressionMultiply, -520, 420)
sin_node = make_expression(material, unreal.MaterialExpressionSine, -340, 420)
half = make_expression(material, unreal.MaterialExpressionConstant, -160, 500)
half.set_editor_property("r", 0.5)
add_half = make_expression(material, unreal.MaterialExpressionAdd, 20, 420)
strength = make_expression(material, unreal.MaterialExpressionScalarParameter, -160, 260)
strength.set_editor_property("parameter_name", "GlowStrength")
strength.set_editor_property("default_value", 5.0)
mul_strength = make_expression(material, unreal.MaterialExpressionMultiply, 220, 260)
emissive = make_expression(material, unreal.MaterialExpressionMultiply, 420, 160)

unreal.MaterialEditingLibrary.connect_material_expressions(time, "", mul_time, "A")
unreal.MaterialEditingLibrary.connect_material_expressions(speed, "", mul_time, "B")
unreal.MaterialEditingLibrary.connect_material_expressions(mul_time, "", sin_node, "")
unreal.MaterialEditingLibrary.connect_material_expressions(sin_node, "", add_half, "A")
unreal.MaterialEditingLibrary.connect_material_expressions(half, "", add_half, "B")
unreal.MaterialEditingLibrary.connect_material_expressions(add_half, "", mul_strength, "A")
unreal.MaterialEditingLibrary.connect_material_expressions(strength, "", mul_strength, "B")
unreal.MaterialEditingLibrary.connect_material_expressions(glow, "", emissive, "A")
unreal.MaterialEditingLibrary.connect_material_expressions(mul_strength, "", emissive, "B")
unreal.MaterialEditingLibrary.connect_material_property(emissive, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)

unreal.MaterialEditingLibrary.layout_material_expressions(material)
unreal.MaterialEditingLibrary.recompile_material(material)
unreal.EditorAssetLibrary.save_loaded_asset(material)
unreal.log("[UEAIBridge] Created flicker glow material: " + PATH)
