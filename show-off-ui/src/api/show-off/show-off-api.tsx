import {sendImagePath} from './paths';

async function readFromImage(image: File): Promise<any> {
    const formData = new FormData();
    formData.set('image', image);
    const response = await fetch(sendImagePath(), {
        method: 'POST',
        body: formData
    });
    return response;
}


export const showOffApi = {
    readFromImage,
}