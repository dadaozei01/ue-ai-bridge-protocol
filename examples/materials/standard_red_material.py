import unreal

FOLDER = "/Game/AI材质"
NAME = "M_AI_Red_Standard"
PATH = FOLDER + "/" + NAME


def ensure_folder(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)


ensure_folder(FOLDER)

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

base_color = unreal.MaterialEditingLibrary.create_material_expression(
    material,
    unreal.MaterialExpressionVectorParameter,
    -420,
    -120,
)
base_color.set_editor_property("parameter_name", "BaseColor")
base_color.set_editor_property("default_value", unreal.LinearColor(1.0, 0.0, 0.0, 1.0))
unreal.MaterialEditingLibrary.connect_material_property(
    base_color,
    "",
    unreal.MaterialProperty.MP_BASE_COLOR,
)

roughness = unreal.MaterialEditingLibrary.create_material_expression(
    material,
    unreal.MaterialExpressionScalarParameter,
    -420,
    80,
)
roughness.set_editor_property("parameter_name", "Roughness")
roughness.set_editor_property("default_value", 0.45)
unreal.MaterialEditingLibrary.connect_material_property(
    roughness,
    "",
    unreal.MaterialProperty.MP_ROUGHNESS,
)

unreal.MaterialEditingLibrary.layout_material_expressions(material)
unreal.MaterialEditingLibrary.recompile_material(material)
unreal.EditorAssetLibrary.save_loaded_asset(material)
unreal.log("[UEAIBridge] Created standard red material: " + PATH)
