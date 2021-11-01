from gif_your_nifti.core import write_axial_gif_normal
import argparse
import glob
import os

def args():
    parser = argparse.ArgumentParser(description="Make axial visualisation.")
    parser.add_argument("--studies", default="", type=str, help="folder with data, nifti files", required=True)
    args = parser.parse_args()

    return args

def make_html(folder):
    images = glob.glob(os.path.join(folder, "*.gif"))
    images.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    data = ""
    for image in images:
        bimage = os.path.basename(image)
        current_data = "<tr>\n \
            <td>{}</td>\n \
            <td><img src=\"{}\" alt=\"image\">\n \
            </td>\n \
        </tr>\n".format(bimage, bimage)

        data = data + current_data

    html_txt = "<!DOCTYPE html>\n \
                <html>\n \
                <body>\n \
\n \
                <h2>{}</h2>\n \
\n \
                <table>\n \
                <tr>\n \
                    <th>Image</th>\n \
                    <th>View</th>\n \
                </tr>\n \
                {} \
                </table>\n \
\n \
                </body>\n \
                </html>\n".format(folder, data)

    with open(os.path.join(folder, 'index.html'), 'w') as fp:
        fp.write(html_txt)

if __name__ == "__main__":
    args = args()

    # sort by file name help from: https://stackoverflow.com/a/33159707/798093
    images = glob.glob(os.path.join(args.studies, "*.nii.gz"))
    images.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    
    # folder to save output mask
    gif_folder = os.path.join(args.studies, 'gif')
    os.makedirs(gif_folder, exist_ok=True)

    for image in images:
        write_axial_gif_normal(filename=image, out_filename=os.path.join(gif_folder, os.path.basename(image).replace(".nii.gz", ".gif")))

    make_html(gif_folder)