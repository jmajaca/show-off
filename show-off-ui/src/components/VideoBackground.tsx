import React, {createRef, useEffect, useState} from 'react';
import {Button} from '@mui/material';
import {makeStyles} from '@mui/styles';
import background from '../assets/background.png';

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
    }
});

type VideoBackgroundProps = {
    image: File | undefined,
    setImage: any,
    className?: string,
}

export default function VideoBackground({image, setImage}: VideoBackgroundProps) {

    const [imageURL, setImageURL] = useState<string>();
    const classes = useStyles();

    const videoRef = createRef<HTMLVideoElement>();
    const canvasRef = createRef<HTMLCanvasElement>();
    const photoRef = createRef<HTMLImageElement>();

    useEffect(() => {
        startVideo()
    }, [videoRef]);

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
                // let capturedImage = new Image();
                // let url = URL.createObjectURL(blob!);
                // capturedImage.onload = function() {
                //     URL.revokeObjectURL(url);
                // };
                // capturedImage.src = url;
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
            photoRef.current!.setAttribute('src', data);
            generateBlob().then(blob => {
                console.log(blob)
                setImage(blob);
            })
        }
    }

    // React.useEffect(() => {
    //     if (image !== undefined) {
    //         setImageURL(URL.createObjectURL(image));
    //     } else {
    //         setImageURL(background);
    //     }
    // }, [image]);

    return (
        <div className={classes.videoWrapper}>
            <video ref={videoRef} muted autoPlay className={classes.video} />
            <div style={{display: 'none'}}>
                <canvas ref={canvasRef}>
                    <div>
                        <img ref={photoRef} alt=""/>
                    </div>
                </canvas>
            </div>
            <Button onClick={takePicture}>CLICK</Button>
        </div>
    );

}