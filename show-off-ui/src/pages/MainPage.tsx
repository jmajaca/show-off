import React, {useEffect, useState} from 'react';

import {makeStyles} from '@mui/styles';

import {ProcessState} from '../enums/ProcessState';
import DeleteButton from '../components/button/DeleteButton';
import {showOffApi} from '../api/show-off/show-off-api';
import {getHeightAndWidthForImage, resizeFile} from '../utils/ImageResizer';
import TextPopup from '../components/popup/TextPopup';
import VideoBackground from '../components/background/VideoBackground';
import VideoButton from '../components/button/VideoButton';
import {ImageWrapper} from '../types/ImageWrapper';
import FileButton from '../components/button/FileButton';
import ImageBackground from '../components/background/ImageBackground';
import FullCircularProgressWithLabel from '../components/progress/FullCircularProgressWithLabel';
import CustomSnackbar from '../components/snackbars/CustomSnackbar';

const IMAGE_HEIGHT = parseInt(process.env.REACT_APP_IMAGE_HEIGHT!);
const PROGRESS_CYCLE = parseInt(process.env.REACT_APP_PROGRESS_CYCLE!);

const useStyles = makeStyles({
    container: {
        display: 'flex',
        justifyContent: 'center',
        width: '100vw',
        height: '100vh',
        position: 'relative',
    },
    recordButtonBox: {
        position: 'absolute',
        bottom: '50px',
        display: 'flex',
        justifyContent: 'center'
    },
    fileButton: {
        position: 'relative',
        left: '10px',
    },
    deleteButton: {
        position: 'absolute',
        top: '10px',
        right: '10px',
    },
    progress: {
        marginTop: '45vh',
        height: '20%'
    },
});

export type TextPopupData = {
    open: boolean,
    text: string,
}

export default function MainPage() {

    const [image, setImage] = useState<ImageWrapper | undefined>();
    const [requestId, setRequestId] = useState<string>('');
    const [processState, setProcessState] = useState<ProcessState>(ProcessState.UPLOAD);
    const [popupData, setPopupData] = useState<TextPopupData>({open: false, text: ''});
    const [sendAnimationFlag, setSendAnimationFlag] = useState<boolean>(false);
    const [progress, setProgress] = useState<number>(0);
    const [openCustomSnackbar, setOpenCustomSnackBar] = useState<boolean>(false);

    const classes = useStyles();

    const popupTitle = 'Text extracted from image';
    const readFromImageError = 'Error occurred while reading from image';

    useEffect(() => {
        if (processState === ProcessState.SENDING) {
            const timer = window.setInterval(() => {
                setProgress((prevProgress) => (prevProgress >= 90 ? prevProgress : prevProgress + 10));
            }, PROGRESS_CYCLE);
            resizeFile(image!, IMAGE_HEIGHT).then(resizedImage => {
                showOffApi.readFromImage(resizedImage).then(response => {
                    setRequestId(response.id);
                    setPopupData({open: true, text: response.text});
                    clearInterval(timer);
                    setProgress(0);
                    setSendAnimationFlag(false);
                    onDeleteButtonClick();
                }).catch(() => {
                    setOpenCustomSnackBar(true);
                    clearInterval(timer);
                    setProgress(0);
                    setSendAnimationFlag(false);
                    onDeleteButtonClick();
                })
            });
        } if (processState === ProcessState.SEND) {
            setSendAnimationFlag(true);
        }
    }, [processState]);

    useEffect(() => {
        if (!popupData.open && popupData.text !== '') {
            showOffApi.sendTextCorrection({id: requestId, text: popupData.text}).then(() => {
                console.log('sent text correction')
            });
        }
    }, [popupData])

    const onVideoButtonClick = () => {
        switch (processState) {
            case ProcessState.UPLOAD:
                setProcessState(ProcessState.SEND);
                break;
            case ProcessState.SEND:
                setProcessState(ProcessState.SENDING);
                break;
            default:
                break;
        }
    }

    const onDeleteButtonClick = () => {
        setProcessState(ProcessState.UPLOAD);
        setImage(undefined);
    }

    const onFileButtonClick = (inputRef:  React.RefObject<HTMLInputElement>) => {
        if (processState === ProcessState.UPLOAD) {
            inputRef.current!.click();
        } else if (processState === ProcessState.SEND) {
            setProcessState(ProcessState.SENDING);
        }
    }

    const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length !== 0) {
            const image = event.target.files[0];
            getHeightAndWidthForImage(image).then(dimensions => {
                setImage({image: image, width: dimensions.width, height: dimensions.height, source: 'file'});
                setProcessState(ProcessState.SEND);
            });
        }
    }

    return (
        <div className={classes.container}>
            {progress !== 0 && progress !== 100 && <FullCircularProgressWithLabel value={progress} className={classes.progress}/>}
            {processState === ProcessState.SEND &&
                <DeleteButton onClick={onDeleteButtonClick} className={classes.deleteButton}/>
            }
            {image?.source !== 'file' && <VideoBackground processState={processState} image={image} setImage={setImage}/>}
            {image?.source === 'file' && <ImageBackground image={image.image}/>}
            <div className={classes.recordButtonBox}>
                <VideoButton processState={processState} sendAnimationFlag={sendAnimationFlag} onClick={onVideoButtonClick}/>
                <FileButton sendAnimationFlag={sendAnimationFlag} onFileChange={onFileChange} onClick={onFileButtonClick} className={classes.fileButton}/>
            </div>
            <TextPopup open={popupData.open} text={popupData.text} title={popupTitle} setPopupData={setPopupData}/>
            <CustomSnackbar open={openCustomSnackbar} setOpen={setOpenCustomSnackBar} type='warning' message={readFromImageError}/>
        </div>
    );
}