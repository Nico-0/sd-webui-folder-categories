import html
from modules import script_callbacks, shared
import gradio as gr
import modules.scripts as scripts
from modules.shared import opts
from modules.ui_components import DropdownMulti
from PIL import Image


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
        with gr.Row():
            # First column with a inputs
            with gr.Column():
                input_image = gr.Image(type='pil')
                incremental_seed = gr.Checkbox(value=True, label='Give incremental seed number in image parameters (todo)')
                with gr.Row():
                    image_width = gr.Number(value=1024, label="Detected image width", interactive=False, scale=1)
                    slider1 = gr.Slider(64, 2048, value=512, step=32, info="Width for each crop", scale=2)
                    slider3 = gr.Slider(1, 10, value=2, step=1, info="Columns", scale=2)
                with gr.Row():
                    image_height = gr.Number(value=1024, label="Detected image height", interactive=False, scale=1)
                    slider2 = gr.Slider(64, 2048, value=512, step=32, info="Height for each crop", scale=2)
                    slider4 = gr.Slider(1, 10, value=2, step=1, info="Rows", scale=2)
                button = gr.Button("Crop grid", variant='primary')
                message_box = gr.Textbox(placeholder="Message will appear here...", label="temp textbox", readonly=True)
            # Second column with a gallery
            with gr.Column():
                gallery = gr.Gallery(value=[], label="Gallery", show_label=False)

        # check for input image size
        # todo make it update sliders
        def update_image_size(image):
            input_width, input_height = image.size
            return input_width, input_height
        input_image.change(update_image_size, input_image, outputs=[image_width, image_height])
        # update neighbor sliders
        # todo check for newvalue == int(newvalue)
        slider1.input(lambda width, input_width: input_width / width, inputs=[slider1, image_width], outputs=slider3)
        slider3.input(lambda columns, input_width: input_width / columns, inputs=[slider3, image_width], outputs=slider1)
        slider2.input(lambda height, input_height: input_height / height, inputs=[slider2, image_height], outputs=slider4)
        slider4.input(lambda rows, input_height: input_height / rows, inputs=[slider4, image_height], outputs=slider2)
        
        def crop_grid(grid, width, height, columns, rows):
            cropped_images = []
            # Iterate cropping depending on image size and quantity
            for i in range(rows):
                y1 = i * height
                y2 = (i + 1) * height
                for j in range(columns):
                    x1 = j * width
                    x2 = (j + 1) * width
                    # Crop the image and append to the list
                    cropped_image = grid.crop((x1, y1, x2, y2))
                    cropped_images.append(cropped_image)
            return cropped_images
        button.click(crop_grid, inputs=[input_image, slider1, slider2, slider3, slider4], outputs=[gallery])

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