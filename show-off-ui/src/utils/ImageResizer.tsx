import Resizer from "react-image-file-resizer";
import {ImageWrapper} from '../types/ImageWrapper';

export const resizeFile = (imageWrapper: ImageWrapper, height: number) => {
    return new Promise<File>((resolve) => {
        const img_height = imageWrapper.height;
        const img_width = imageWrapper.width;
        const ratio = height / img_height;
        Resizer.imageFileResizer(
            imageWrapper.image,
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
}