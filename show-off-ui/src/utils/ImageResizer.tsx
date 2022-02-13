import Resizer from "react-image-file-resizer";


type ImageDimensions = {
    height: number,
    width: number,
}



export const resizeFile = (file: File, height: number) =>
    new Promise<any>((resolve) => {
        const fileAsDataURL = window.URL.createObjectURL(file);
        getHeightAndWidthFromDataUrl(fileAsDataURL).then(dimensions => {
            const img_height = dimensions.height;
            const img_width = dimensions.width;
            const ratio = height / img_height;
            Resizer.imageFileResizer(
                file,
                Math.round(img_width * ratio),
                height,
                "JPG",
                100,
                0,
                (uri) => {
                    resolve(uri);
                },
                "file"
            );
        });
    });

const getHeightAndWidthFromDataUrl = (dataURL: string) =>
    new Promise<ImageDimensions>(resolve => {
        const img = new Image();
        img.onload = () => {
            resolve({
                height: img.height,
                width: img.width
            });
        }
        img.src = dataURL;
    });