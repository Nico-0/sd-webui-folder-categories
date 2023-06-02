import html
from modules import script_callbacks, shared
import gradio as gr
import modules.scripts as scripts
from modules.shared import opts
import os
from modules.ui_components import DropdownMulti

default_tab_options = ["txt2img", "img2img", "txt2img-grids", "img2img-grids", "Extras", "favoritetabName", "Others"]
components_list = ["Sort by", "Filename keyword search", "EXIF keyword search", "Ranking Filter", "Aesthestic Score", "Generation Info"]

categories = ["Random test", "Profile pictures", "My art project"]

def add_tab():
    with gr.Blocks(analytics_enabled=False) as ui:
        with gr.Row():
            gr.HTML(f"""
                <p>Texto de prueba</p>"""
            )
            checkbox = gr.Checkbox(
                False,
                label=opts.nicardo_active_tabs
            )

    return [(ui, "Nicardo", "nicardo")]



def changed_folder():
    shared.opts.__setattr__("outdir_samples", "outputs/"+opts.nicardo_folder_category+"/samples")
    shared.opts.__setattr__("outdir_grids", "outputs/"+opts.nicardo_folder_category+"/grids")
    shared.opts.save(shared.config_filename)


def on_ui_settings():
    # [current setting_name], [old setting_name], [default], [label], [component], [component_args]
    section = ('nicardo-section', "Nicardo-section")

    shared.opts.add_option(
        "nicardo_folder_category",
        shared.OptionInfo(
            "Default",
            "Categoria a guardar imagenes",
            gr.Dropdown,
            lambda: {"choices": categories},
			onchange=changed_folder,
            section=section)
    )
	
    shared.opts.add_option(
        "nicardo_demo_set",
        shared.OptionInfo(
            "Vacio",
            "Campo de prueba para meter el resultado seleccionado",
            section=section)
    )

    nicardo_options = [
        ("nicardo_active_tabs", None, ", ".join(default_tab_options), "List of active tabs (separated by commas)"),
        ("nicardo_hidden_components", None, [], "Select components to hide", DropdownMulti, lambda: {"choices": components_list}),
        ("nicardo_with_subdirs", "images_history_with_subdirs", True, "Include images in sub directories"),
        ("nicardo_preload", "images_history_preload", False, "Preload images at startup for first tab"),
        ("nicardo_page_columns", "images_history_page_columns", 6, "Number of columns on the page"),
    ]

    for cur_setting_name, _, *option_info in nicardo_options:
        shared.opts.add_option(cur_setting_name, shared.OptionInfo(*option_info, section=section))



script_callbacks.on_ui_tabs(add_tab)
script_callbacks.on_ui_settings(on_ui_settings)