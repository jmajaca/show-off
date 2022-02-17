import React, {createRef, Dispatch, SetStateAction, useEffect, useState} from 'react';

import {makeStyles} from '@mui/styles';

import {ProcessState} from '../enums/ProcessState';
import {ImageWrapper} from '../types/ImageWrapper';

const useStyles = makeStyles({
    videoWrapper: {
        width: '100vw',
        height: '100vh',
        zIndex: -1,
        position: 'absolute'
    },
    video: {
        width: '100%',
        height: '100%',
        objectFit: 'cover',
    },
    hide: {
        display: 'none'
    }
});

type VideoBackgroundProps = {
    processState: ProcessState,
    image: ImageWrapper | undefined,
    setImage: Dispatch<SetStateAction<ImageWrapper | undefined>>,
    className?: string,
}

export default function VideoBackground({processState, image, setImage, className}: VideoBackgroundProps) {

    const [imageURL, setImageURL] = useState<string>("");
    const classes = useStyles();

    const videoRef = createRef<HTMLVideoElement>();
    const canvasRef = createRef<HTMLCanvasElement>();
    const photoRef = createRef<HTMLImageElement>();
    const footerRef = createRef<HTMLDivElement>();

    useEffect(() => {
        if (footerRef.current) {
            footerRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [footerRef])

    useEffect(() => {
        switch (processState) {
            case ProcessState.UPLOAD:
                setImageURL("");
                break;
            case ProcessState.SEND:
                if (image === undefined || image.source != 'file') {
                    takePicture();
                }
                break;
            default:
                break;
        }
    }, [processState]);

    useEffect(() => {
        if (imageURL !== "") {
            photoRef.current!.setAttribute('src', imageURL);
        } else {
            startVideo();
        }
    }, [imageURL])

    const startVideo = () => {
        navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment', frameRate: 60}, audio: false}).then(stream => {
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
        }, error => console.log(error))
    }

    const generateBlob = () => {
        return new Promise<File>(resolve => {
            let canvas = canvasRef.current!
            canvas.toBlob((blob) => {
                let file = new File([blob!], 'image/png', {type: 'image/png'})
                resolve(file)
            }, 'image/png', 100);
        })
    }

    const takePicture = () => {
        let canvas = canvasRef.current!
        let context = canvas.getContext('2d');
        canvas.width = videoRef.current!.videoWidth;
        canvas.height = videoRef.current!.videoHeight;
        if (context) {
            context.drawImage(videoRef.current!, 0, 0, videoRef.current!.videoWidth, videoRef.current!.videoHeight);
            let data = canvas.toDataURL('image/png');
            setImageURL(data)
            generateBlob().then(blob => {
                setImage({image: blob, width: canvas.width, height: canvas.height, source: 'video'});
            })
        }
    }
    // TODO use ImageBackground for this element
    return (
        <div className={classes.videoWrapper}>
            {imageURL === "" && <video ref={videoRef} muted autoPlay className={classes.video} />}
            <canvas ref={canvasRef} className={classes.hide} />
            {imageURL !== "" && <img className={classes.video} ref={photoRef} alt=""/>}
            <div ref={footerRef} className={classes.hide}/>
        </div>
    );

}