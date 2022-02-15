import React, {createRef, Dispatch, SetStateAction, useEffect, useState} from 'react';

import {makeStyles} from '@mui/styles';

import {ProcessState} from '../enums/ProcessState';

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
    },
    hideCanvas: {
        display: 'none'
    }
});

type VideoBackgroundProps = {
    processState: ProcessState,
    setImage: Dispatch<SetStateAction<File | undefined>>,
    className?: string,
}

export default function VideoBackground({processState, setImage, className}: VideoBackgroundProps) {

    const [imageURL, setImageURL] = useState<string>("");
    const classes = useStyles();

    const videoRef = createRef<HTMLVideoElement>();
    const canvasRef = createRef<HTMLCanvasElement>();
    const photoRef = createRef<HTMLImageElement>();

    useEffect(() => {
        startVideo()
        console.log('video')
    }, [videoRef]);

    useEffect(() => {
        switch (processState) {
            case ProcessState.UPLOAD:
                setImageURL("");
                break;
            case ProcessState.SEND:
                takePicture();
                break;
            default:
                break;
        }
    }, [processState]);

    useEffect(() => {
        if (imageURL !== "") {
            photoRef.current!.setAttribute('src', imageURL);
        }
    })

    const startVideo = () => {
        navigator.mediaDevices.getUserMedia({video: true, audio: false}).then(stream => {
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
                setImage(blob);
            })
        }
    }

    return (
        <div className={classes.videoWrapper}>
            {imageURL === "" && <video ref={videoRef} muted autoPlay className={classes.video} />}
            <canvas ref={canvasRef} className={classes.hideCanvas} />
            {imageURL !== "" && <img className={classes.video} ref={photoRef} alt=""/>}
        </div>
    );

}