import html
from modules import script_callbacks, shared
import gradio as gr
import modules.scripts as scripts
from modules.shared import opts
from modules.ui_components import DropdownMulti


def add_tab():
    with gr.Blocks(analytics_enabled=False) as ui:
        with gr.Row():
            gr.HTML(f"""
			    <p>Select nicocat_folder_category on Settings -> User Interface -> Quicksettings list</p>
			    <p>Config your desired folders on Settings -> Nico Folder Categories</p>
                <p>Here we have a demo tab, with a checkbox coming next</p>
				<p>The checkbox label is read from opts in config.json</p>"""
            )
            checkbox = gr.Checkbox(
                False,
                label=opts.nicocat_zztest_checkbox_label
            )

    return [(ui, "Nico Folder Categories", "nicocat-tab")]


def changed_folder():
    shared.opts.__setattr__("outdir_samples", "outputs/"+opts.nicocat_folder_category+"/samples")
    shared.opts.__setattr__("outdir_grids", "outputs/"+opts.nicocat_folder_category+"/grids")
    shared.opts.save(shared.config_filename)
	

default_categories = ["Random test", "Profile pictures", "My art project"]
def on_ui_settings():
    # [setting_name], [default], [label], [component], [component_args]
    section = ('nicocat-section', "Nico Folder Categories")

    shared.opts.add_option(
        "nicocat_categories",
        shared.OptionInfo(
            ", ".join(default_categories),
            "Categories to show on Dropdown (Apply and reload)",
            section=section)
    )

    shared.opts.add_option(
        "nicocat_folder_category",
        shared.OptionInfo(
            "Default",
            "Categoria a guardar imagenes",
            gr.Dropdown,
            lambda: {"choices": opts.nicocat_categories.split(", ")},
			onchange=changed_folder,
            section=section)
    )
	
    shared.opts.add_option(
        "nicocat_zztest_textbox",
        shared.OptionInfo(
            "Vacio",
            "(Demo) Empty field to store any text",
            section=section)
    )

    default_check_options = ["bear", "pig", "parrot", "robot"]
    components_list = ["Sortby", "Filenamekeyword", "EXIFsearch", "Ranking Filter", "Aesthestic Score", "Generation Info"]
	# (setting_name, description?, default value, label, component)
    nicocat_options = [
        ("nicocat_zztest_checkbox_label", None, ", ".join(default_check_options), "(Demo) Name for the checkbox label in the main extension tab (Apply and reload)"),
        ("nicocat_zztest_dropdownMulti", None, [], "(Demo) Multi selections dropdown", DropdownMulti, lambda: {"choices": components_list}),
        ("nicocat_zztest_checkbox", None, True, "(Demo) Dummy checkbox"),
        ("nicocat_zztest_numberbox", None, 6, "(Demo) Textbox for numbers"),
    ]

    for cur_setting_name, _, *option_info in nicocat_options:
        shared.opts.add_option(cur_setting_name, shared.OptionInfo(*option_info, section=section))


script_callbacks.on_ui_tabs(add_tab)
script_callbacks.on_ui_settings(on_ui_settings)