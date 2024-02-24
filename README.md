# sd-webui-folder-categories

Extension for [a1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

Adds a quick setting to pick a folder to save images.

Maybe one time you want to generate profile pictures, another generate art for your project, another time you want to test different models, another time you want to generate images randomly...
And you want to quickly switch between these scopes back and fort without cluttering a single folder.
Well this extension is for you!

## Usage

- Add this extension to the extensions folder.
- Go to Settings tab -> User Interface -> User interface -> Quicksettings list. And add `nicocat_folder_category` to the list.
- Go to Settings tab -> Uncategorized -> Nico Folder Categories -> Categories to show on Dropdown. Add your desired folders separated by comma and space.

Warning: this overrides the default save path settings, as it's not possible to build upon them, without injecting code into the original modules.

## Possible features for later

- Add option to choose if a single custom folder goes in the root directory, and multiple grid/samples/native folders are created (one for each category). Or if single grid/samples/native folders are left untouched, and have multiple nicocat folders.



