import Resizer from "react-image-file-resizer";

type ImageDimensions = {
    height: number,
    width: number,
}

export const resizeFile = (file: File, height: number) => {
    return new Promise<File>((resolve) => {
        const fileAsDataURL = window.URL.createObjectURL(file);
        getHeightAndWidthFromDataUrl(fileAsDataURL).then(dimensions => {
            const img_height = dimensions.height;
            const img_width = dimensions.width;
            const ratio = height / img_height;
            Resizer.imageFileResizer(
                file,
                Math.round(img_width * ratio),
                height,
                "JPEG",
                100,
                0,
                (uri) => {
                    resolve(uri as unknown as File);
                },
                "file"
            );
        });
    });
}


const getHeightAndWidthFromDataUrl = (dataURL: string) => {
    return new Promise<ImageDimensions>(resolve => {
        const img = new Image();
        img.onload = () => {
            resolve({
                height: img.height,
                width: img.width
            });
        }
        img.src = dataURL;
    });
}