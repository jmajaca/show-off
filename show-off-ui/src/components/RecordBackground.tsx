import React, {useState} from 'react';

import {makeStyles} from '@mui/styles';

import background from '../assets/background.png'

const useStyles = makeStyles({
    image: {
        width: '100vw',
        height: '100vh',
        zIndex: -1,
        position: 'absolute'
    }
})

type RecordBackgroundProps = {
    image: File | undefined,
    className?: string,
}

export default function RecordBackground({image, className}: RecordBackgroundProps) {

    const [imageURL, setImageURL] = useState<string>();
    const classes = useStyles();

    React.useEffect(() => {
        if (image !== undefined) {
            setImageURL(URL.createObjectURL(image));
        } else {
            setImageURL(background);
        }
    }, [image]);

    return (
        <img src={imageURL} className={`${classes.image} ${className}`}/>
    );

}